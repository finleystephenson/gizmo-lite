"""
FlashcardGenerator service using Anthropic's structured outputs.

This service uses Claude's structured outputs feature to reliably generate
10 Q&A flashcard pairs from study notes with guaranteed schema compliance.
"""

from anthropic import Anthropic
from src.config import Config
from src.models.schemas import FlashcardSet


class FlashcardGenerator:
    """
    Core AI service for generating educational flashcards.

    Uses Claude Sonnet 4.5 with structured outputs to ensure 100% valid JSON
    responses matching our Pydantic schema. No manual JSON parsing needed.
    """

    def __init__(self):
        """Initialize Anthropic client with API key from config."""
        self.client = Anthropic(api_key=Config.ANTHROPIC_API_KEY)

    def generate_flashcards(self, notes: str, topic: str) -> FlashcardSet:
        """
        Generate 10 flashcards from study notes using Claude.

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

        response = self.client.beta.messages.parse(
            model="claude-sonnet-4-5-20250929",
            max_tokens=2048,
            messages=[{"role": "user", "content": prompt}],
            output_format=FlashcardSet,
        )

        return response
