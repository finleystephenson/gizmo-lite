"""
FlashcardGenerator service using Anthropic's structured outputs.

This service uses Claude's structured outputs feature to reliably generate
10 Q&A flashcard pairs from study notes with guaranteed schema compliance.
"""

import time
import random
from anthropic import Anthropic, APIError, RateLimitError, InternalServerError
from src.config import Config
from src.models.schemas import FlashcardSet
from src.models.deck import Deck
from src.models.flashcard import Flashcard


class FlashcardGenerator:
    """
    Core AI service for generating educational flashcards.

    Uses Claude Sonnet 4.5 with structured outputs to ensure 100% valid JSON
    responses matching our Pydantic schema. No manual JSON parsing needed.
    """

    def __init__(self):
        """Initialize Anthropic client with API key from config."""
        self.client = Anthropic(api_key=Config.ANTHROPIC_API_KEY)

    def _retry_with_backoff(self, func, max_retries=3):
        """
        Retry API calls with exponential backoff and jitter.

        Args:
            func: Callable that performs the API call
            max_retries: Maximum number of retry attempts (default: 3)

        Returns:
            Result from func() if successful

        Raises:
            ValueError: User-friendly error message for different failure types
        """
        for attempt in range(max_retries + 1):
            try:
                return func()
            except RateLimitError as e:
                if attempt == max_retries:
                    raise ValueError(
                        "Rate limit exceeded. Please try again in a few minutes."
                    ) from e

                # Honor retry-after header if present
                retry_after = getattr(e, 'retry_after', None)
                if retry_after:
                    delay = float(retry_after)
                else:
                    # Exponential backoff: 1s, 2s, 4s, 8s with jitter
                    delay = (2 ** attempt) + random.uniform(0, 1)

                print(f"Rate limited. Retrying in {delay:.1f}s... (attempt {attempt + 1}/{max_retries})")
                time.sleep(delay)

            except InternalServerError as e:
                # 529 overloaded - retry with backoff
                if attempt == max_retries:
                    raise ValueError(
                        "API temporarily unavailable. Please try again later."
                    ) from e

                delay = (2 ** attempt) + random.uniform(0, 1)
                print(f"API overloaded. Retrying in {delay:.1f}s... (attempt {attempt + 1}/{max_retries})")
                time.sleep(delay)

            except APIError as e:
                # 400/401 and other errors - don't retry
                if e.status_code == 401:
                    raise ValueError(
                        "Invalid API key. Check your ANTHROPIC_API_KEY in .env file."
                    ) from e
                elif e.status_code == 400:
                    raise ValueError(
                        f"Invalid request: {e.message}"
                    ) from e
                else:
                    raise ValueError(
                        f"API error: {e.message}"
                    ) from e

    def generate_flashcards(self, notes: str, topic: str) -> FlashcardSet:
        """
        Generate 10 flashcards from study notes using Claude with retry logic.

        Args:
            notes: Study notes to generate flashcards from
            topic: Topic name for the flashcard deck

        Returns:
            FlashcardSet: Validated set of 10 flashcard pairs

        The prompt emphasizes active recall and educational quality:
        - Questions test understanding, not memorization
        - Avoid yes/no questions - prefer "explain", "describe", "why"
        - Focus on key concepts from the notes
        - Detailed answers that reinforce learning
        """
        prompt = f"""You are an expert educator creating flashcards for active recall study.

Topic: {topic}

Study Notes:
{notes}

Generate exactly 10 flashcards that:
1. Test understanding, not memorization
2. Use questions requiring explanation (avoid yes/no questions)
3. Focus on key concepts from the notes
4. Include detailed answers that reinforce learning
5. Progress from fundamental to more complex concepts

Each flashcard should help the student recall and understand the material."""

        def api_call():
            response = self.client.beta.messages.parse(
                model="claude-sonnet-4-5-20250929",
                max_tokens=2048,
                messages=[{"role": "user", "content": prompt}],
                output_format=FlashcardSet,
            )
            return response

        # Use retry wrapper for resilience
        response = self._retry_with_backoff(api_call)

        # Extract parsed content from response
        # beta.messages.parse returns ParsedBetaMessage with content list
        # The first content item (ParsedBetaTextBlock) has parsed_output attribute
        return response.content[0].parsed_output

    def save_to_database(self, flashcard_set: FlashcardSet) -> int:
        """
        Save generated flashcards to database.

        Args:
            flashcard_set: FlashcardSet object from generate_flashcards()

        Returns:
            deck_id: ID of created deck
        """
        # Create deck with topic name
        deck = Deck.create(name=flashcard_set.topic)
        deck_id = deck['id']

        # Create flashcards linked to deck via foreign key
        for pair in flashcard_set.flashcards:
            Flashcard.create(
                deck_id=deck_id,
                question=pair.question,
                answer=pair.answer
            )

        return deck_id

    def generate_and_save(self, notes: str, topic: str) -> dict:
        """
        Generate flashcards and save to database in one call.

        Args:
            notes: Study notes to generate flashcards from
            topic: Topic name for the flashcard deck

        Returns:
            dict with deck_id, topic, and flashcard_count
        """
        # Generate flashcards using AI
        flashcard_set = self.generate_flashcards(notes, topic)

        # Save to database
        deck_id = self.save_to_database(flashcard_set)

        return {
            'deck_id': deck_id,
            'topic': flashcard_set.topic,
            'flashcard_count': len(flashcard_set.flashcards)
        }
