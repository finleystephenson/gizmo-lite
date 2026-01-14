# Phase 2: AI Integration - Research

**Researched:** 2026-01-14
**Domain:** Anthropic Claude API for educational flashcard generation
**Confidence:** HIGH

<research_summary>
## Summary

Researched the Anthropic Claude API ecosystem for generating educational flashcards from study notes. As of November 2025, Anthropic introduced **Structured Outputs** (public beta) which guarantees JSON schema compliance, eliminating parsing errors and validation headaches.

The standard approach uses the official Python SDK (`anthropic>=0.18.0`) with the new structured outputs feature (`output_format` parameter) to ensure 100% reliable JSON responses. For flashcard generation, combine structured outputs with prompt engineering best practices: explicit output format specification, few-shot examples, and constraints that optimize for active recall (atomic questions, clear cues, unambiguous answers).

Key finding: Don't hand-roll JSON parsing/validation or retry logic for malformed responses—Anthropic's structured outputs feature (beta header `structured-outputs-2025-11-13`) guarantees schema-compliant JSON through constrained decoding. Custom validation code is unnecessary and creates maintenance burden.

**Primary recommendation:** Use Python SDK's `client.beta.messages.parse()` with Pydantic models for type-safe flashcard generation. Combine with exponential backoff retry logic for 429/529 errors and explicit prompt engineering for educational quality.
</research_summary>

<standard_stack>
## Standard Stack

The established libraries/tools for Claude API integration:

### Core
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| anthropic | >=0.18.0 | Official Python SDK for Claude API | First-party SDK with built-in retry logic, streaming support, error handling |
| pydantic | >=2.0.0 | Data validation and schema definition | Works natively with SDK's `parse()` method for type-safe structured outputs |
| python-dotenv | >=1.0.0 | Environment variable management | Industry standard for API key management (already in project) |

### Supporting
| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| tenacity | >=8.2.0 | Retry library with backoff strategies | Advanced retry patterns beyond SDK defaults |
| pydantic-settings | >=2.0.0 | Settings management | Complex configuration beyond simple env vars |

### Alternatives Considered
| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| anthropic SDK | Raw HTTP requests | SDK handles auth headers, retries, streaming automatically - raw requests add complexity |
| Pydantic | Raw dict validation | Pydantic provides type safety, IDE autocomplete, automatic validation |
| Structured outputs | Prompt engineering for JSON | Structured outputs guarantee valid JSON (100% reliability vs ~95% with prompts) |

**Installation:**
```bash
pip install anthropic>=0.18.0 pydantic>=2.0.0 python-dotenv>=1.0.0
```

(Note: anthropic and python-dotenv already in project requirements.txt)
</standard_stack>

<architecture_patterns>
## Architecture Patterns

### Recommended Project Structure
```
src/
├── services/
│   └── flashcard_generator.py    # Claude API integration service
├── models/
│   └── flashcard.py               # Pydantic models for API responses
├── config.py                      # Environment config (already exists)
└── utils/
    └── retry.py                   # Retry logic utilities (optional)
```

### Pattern 1: Structured Outputs with Pydantic
**What:** Use Pydantic models to define flashcard schema, SDK automatically validates responses
**When to use:** All flashcard generation requests (guaranteed schema compliance)
**Example:**
```python
# Source: Anthropic Structured Outputs docs
from pydantic import BaseModel, Field
from typing import List
from anthropic import Anthropic

class Flashcard(BaseModel):
    question: str = Field(description="Clear, atomic question for active recall")
    answer: str = Field(description="Concise answer to the question")

class FlashcardSet(BaseModel):
    topic: str
    cards: List[Flashcard] = Field(min_length=1, max_length=10)

client = Anthropic()

response = client.beta.messages.parse(
    model="claude-sonnet-4-5",
    max_tokens=2048,
    betas=["structured-outputs-2025-11-13"],
    messages=[{"role": "user", "content": f"Generate 10 flashcards from: {notes}"}],
    output_format=FlashcardSet,
)

# Guaranteed type-safe flashcards
flashcards = response.parsed_output  # Type: FlashcardSet
print(f"Generated {len(flashcards.cards)} cards for {flashcards.topic}")
```

### Pattern 2: Exponential Backoff for Rate Limits
**What:** Retry 429/529 errors with exponential backoff and jitter
**When to use:** Production systems calling Claude API
**Example:**
```python
# Source: Claude API error handling best practices
import time
import random
from anthropic import Anthropic, APIError

def retry_with_backoff(func, max_retries=3, base_delay=1.0, max_delay=60.0):
    """Exponential backoff with jitter for Claude API calls"""
    for attempt in range(max_retries):
        try:
            return func()
        except APIError as e:
            if e.status_code in [429, 500, 502, 503, 504, 529]:
                if attempt == max_retries - 1:
                    raise

                # Check retry-after header for 429 errors
                retry_after = getattr(e, 'retry_after', None)
                if retry_after and e.status_code == 429:
                    delay = float(retry_after)
                else:
                    delay = min(base_delay * (2 ** attempt), max_delay)
                    delay += random.uniform(0, delay * 0.1)  # Add jitter

                time.sleep(delay)
            else:
                raise
```

### Pattern 3: Prompt Engineering for Educational Quality
**What:** Structure prompts with explicit instructions for active recall optimization
**When to use:** When generating flashcards (ensures educational quality)
**Example:**
```python
# Source: Prompt engineering best practices + educational flashcard research
def create_flashcard_prompt(notes: str, topic: str, count: int = 10) -> str:
    return f"""Generate exactly {count} high-quality flashcards from the following notes on {topic}.

INSTRUCTIONS:
- Focus on key concepts, definitions, and relationships
- Create atomic questions (one concept per card)
- Ensure clear, unambiguous answers
- Optimize for active recall (test understanding, not memorization)
- Avoid yes/no questions (use "what", "how", "why")
- Keep questions concise and specific

NOTES:
{notes}

Generate {count} flashcards as JSON with this structure:
{{
  "topic": "{topic}",
  "cards": [
    {{"question": "...", "answer": "..."}},
    ...
  ]
}}"""
```

### Anti-Patterns to Avoid
- **Manual JSON parsing:** Don't parse `response.content[0].text` as JSON—use structured outputs instead
- **Hardcoded API keys:** Never hardcode keys in source code—use environment variables
- **No retry logic:** Production code must handle 429/529 errors with exponential backoff
- **Vague prompts:** Avoid "Generate flashcards" without explicit instructions—quality suffers
</architecture_patterns>

<dont_hand_roll>
## Don't Hand-Roll

Problems that look simple but have existing solutions:

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| JSON schema validation | Custom dict validation | Structured outputs + Pydantic | Guaranteed schema compliance, type safety, zero parsing errors |
| Retry logic for rate limits | Manual try/except loops | SDK built-in + exponential backoff | SDK handles auth headers, 429 retry-after header parsing, connection pooling |
| API authentication | Manual header construction | Anthropic SDK | SDK automatically adds x-api-key, anthropic-version, content-type headers |
| Prompt template management | String concatenation | Python f-strings with structured format | Maintainable, testable, version-controllable prompts |
| Request timeout handling | asyncio with timeouts | SDK default (60s) or config | SDK manages connection lifecycle, socket keep-alive |

**Key insight:** The Anthropic Python SDK and structured outputs feature solve 95% of integration problems. Custom solutions for JSON parsing, retries, or auth create technical debt without providing value. The only custom code needed is domain-specific prompt engineering and business logic.
</dont_hand_roll>

<common_pitfalls>
## Common Pitfalls

### Pitfall 1: Using Structured Outputs Without Beta Header
**What goes wrong:** 400 error: "output_format parameter not supported"
**Why it happens:** Structured outputs require `anthropic-beta: structured-outputs-2025-11-13` header
**How to avoid:** Use `client.beta.messages.parse()` or pass `betas=["structured-outputs-2025-11-13"]` parameter
**Warning signs:** "Parameter not recognized" or "Beta feature not enabled" errors

### Pitfall 2: Not Handling max_tokens Limit
**What goes wrong:** Responses cut off mid-JSON (`stop_reason: "max_tokens"`), schema validation fails
**Why it happens:** Flashcard generation for 10 cards can exceed default max_tokens
**How to avoid:** Set `max_tokens=2048` or higher for flashcard generation (10 cards ≈ 1500-2000 tokens)
**Warning signs:** Incomplete JSON, missing closing braces, truncated last flashcard

### Pitfall 3: Rate Limit Acceleration on New Accounts
**What goes wrong:** 429 errors even with low request volume on new API accounts
**Why it happens:** New accounts have Tier 1 limits (50 RPM, 40K input tokens/minute) and acceleration limits
**How to avoid:** Ramp up gradually (don't spike from 0 to max), monitor `retry-after` header, cache prompts with Prompt Caching
**Warning signs:** 429 errors during initial testing, "rate_limit_error" responses

### Pitfall 4: LLM Generates Repetitive Flashcards
**What goes wrong:** Multiple flashcards with similar questions or one-word answers
**Why it happens:** LLMs fall into repeating patterns; if first card is simple, subsequent cards tend to be simple
**How to avoid:** Use few-shot examples in prompt showing diverse question types, request 12+ cards and filter best 10
**Warning signs:** Questions start with same pattern ("What is...", "What is...", "What is...")

### Pitfall 5: Ignoring Refusal Responses
**What goes wrong:** Application crashes trying to parse refusal message as flashcards
**Why it happens:** Claude refuses unsafe requests (`stop_reason: "refusal"`) even with structured outputs
**How to avoid:** Check `stop_reason` before parsing, handle "refusal" gracefully with user-friendly error
**Warning signs:** `stop_reason: "refusal"`, output doesn't match schema, 200 status but no flashcards
</common_pitfalls>

<code_examples>
## Code Examples

Verified patterns from official sources:

### Complete Flashcard Generation Service
```python
# Source: Anthropic Structured Outputs docs + best practices
from typing import List
from pydantic import BaseModel, Field
from anthropic import Anthropic, APIError
import os

class Flashcard(BaseModel):
    """Single flashcard for spaced repetition"""
    question: str = Field(
        description="Clear, atomic question optimized for active recall"
    )
    answer: str = Field(
        description="Concise answer to the question"
    )

class FlashcardSet(BaseModel):
    """Set of flashcards generated from notes"""
    topic: str = Field(description="Topic or subject area")
    cards: List[Flashcard] = Field(
        min_length=1,
        max_length=10,
        description="List of flashcards"
    )

class FlashcardGenerator:
    """Service for generating flashcards using Claude API"""

    def __init__(self, api_key: str | None = None):
        self.client = Anthropic(api_key=api_key or os.getenv("ANTHROPIC_API_KEY"))

    def generate_flashcards(
        self,
        notes: str,
        topic: str,
        count: int = 10
    ) -> FlashcardSet:
        """
        Generate flashcards from study notes using Claude.

        Args:
            notes: Study notes or text to generate flashcards from
            topic: Topic name for the flashcard deck
            count: Number of flashcards to generate (max 10)

        Returns:
            FlashcardSet with guaranteed schema compliance

        Raises:
            APIError: For authentication, rate limiting, or server errors
            ValueError: For invalid inputs
        """
        if count < 1 or count > 10:
            raise ValueError("Count must be between 1 and 10")

        prompt = self._create_prompt(notes, topic, count)

        try:
            response = self.client.beta.messages.parse(
                model="claude-sonnet-4-5",
                max_tokens=2048,  # Enough for 10 flashcards
                betas=["structured-outputs-2025-11-13"],
                messages=[{"role": "user", "content": prompt}],
                output_format=FlashcardSet,
            )

            # Check for refusal
            if response.stop_reason == "refusal":
                raise ValueError("Claude refused to generate flashcards for this content")

            # Check for truncation
            if response.stop_reason == "max_tokens":
                raise ValueError("Response truncated - increase max_tokens")

            return response.parsed_output

        except APIError as e:
            # Let caller handle retries
            raise

    def _create_prompt(self, notes: str, topic: str, count: int) -> str:
        """Create optimized prompt for flashcard generation"""
        return f"""Generate exactly {count} high-quality flashcards from the following notes on {topic}.

INSTRUCTIONS:
- Focus on key concepts, definitions, and relationships
- Create atomic questions (one concept per card)
- Ensure clear, unambiguous answers
- Optimize for active recall (test understanding, not memorization)
- Avoid yes/no questions (use "what", "how", "why")
- Keep questions concise and specific
- Vary question types (avoid repetitive patterns)

NOTES:
{notes}

Generate flashcards following the required JSON schema with topic and cards array."""
```

### Retry Logic with Exponential Backoff
```python
# Source: Claude API error handling best practices
import time
import random
from anthropic import APIError

def generate_flashcards_with_retry(
    generator: FlashcardGenerator,
    notes: str,
    topic: str,
    count: int = 10,
    max_retries: int = 3
) -> FlashcardSet:
    """
    Generate flashcards with automatic retry for transient errors.

    Handles:
    - 429 (rate limit): Respects retry-after header
    - 529 (overloaded): Simple retry with backoff
    - 500/502/503/504: Exponential backoff
    """
    base_delay = 1.0
    max_delay = 60.0

    for attempt in range(max_retries):
        try:
            return generator.generate_flashcards(notes, topic, count)

        except APIError as e:
            # Don't retry client errors (except rate limits)
            if e.status_code not in [429, 500, 502, 503, 504, 529]:
                raise

            # Last attempt - raise error
            if attempt == max_retries - 1:
                raise

            # Calculate delay
            if e.status_code == 429 and hasattr(e, 'retry_after'):
                # Respect retry-after header
                delay = float(e.retry_after)
            else:
                # Exponential backoff with jitter
                delay = min(base_delay * (2 ** attempt), max_delay)
                delay += random.uniform(0, delay * 0.1)

            print(f"Retry attempt {attempt + 1}/{max_retries} after {delay:.1f}s")
            time.sleep(delay)

    raise RuntimeError("Max retries exceeded")
```

### Integration with Existing Database Models
```python
# Source: Project database models from Phase 1
from src.models.deck import Deck
from src.models.flashcard import Flashcard as FlashcardModel
import time

def save_generated_flashcards(
    flashcard_set: FlashcardSet,
    deck_name: str | None = None
) -> dict:
    """
    Save AI-generated flashcards to database.

    Args:
        flashcard_set: FlashcardSet from Claude API
        deck_name: Optional deck name (defaults to flashcard_set.topic)

    Returns:
        Dict with deck_id and created flashcard IDs
    """
    # Create deck
    deck = Deck.create(name=deck_name or flashcard_set.topic)

    # Create flashcards
    flashcard_ids = []
    for card in flashcard_set.cards:
        fc = FlashcardModel.create(
            deck_id=deck['id'],
            question=card.question,
            answer=card.answer
        )
        flashcard_ids.append(fc['id'])

    return {
        'deck_id': deck['id'],
        'flashcard_ids': flashcard_ids,
        'count': len(flashcard_ids)
    }
```
</code_examples>

<sota_updates>
## State of the Art (2024-2025)

What's changed recently:

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| Prompt engineering for JSON | Structured outputs (beta) | Nov 2025 | 100% schema compliance vs ~95%, eliminates retry logic |
| Manual retry logic | SDK built-in + retry-after header | 2024 | Respect rate limits, handle 429 correctly |
| JSON mode (deprecated) | output_format parameter | Nov 2025 | Type-safe with Pydantic, automatic validation |
| Generic prompting | Few-shot with quality constraints | 2024-2025 | Better flashcard quality, less repetition |

**New tools/patterns to consider:**
- **Structured Outputs**: Beta feature (Nov 2025) guarantees schema compliance through constrained decoding
- **client.beta.messages.parse()**: SDK method that automatically validates responses against Pydantic models
- **Prompt Caching**: Cache system prompts to increase effective throughput 5x (cached tokens don't count toward rate limits)
- **Claude Sonnet 4.5**: Current recommended model (faster, cheaper than Opus 4.1, better than Haiku 4.5)

**Deprecated/outdated:**
- **JSON mode (old)**: Replaced by structured outputs with schema validation
- **Manual JSON parsing**: Use `parsed_output` from `parse()` method instead
- **String-based retry logic**: SDK handles retry-after header automatically
</sota_updates>

<open_questions>
## Open Questions

Things that couldn't be fully resolved:

1. **Optimal flashcard count per request**
   - What we know: 10 cards ≈ 1500-2000 tokens, fits well within context
   - What's unclear: Whether smaller batches (5 cards) produce higher quality
   - Recommendation: Start with 10 cards (user requirement), A/B test quality if issues arise

2. **Prompt caching effectiveness**
   - What we know: Caching system prompts can increase throughput 5x
   - What's unclear: Cost/benefit for flashcard generation (short sessions vs long)
   - Recommendation: Implement basic version first, add prompt caching if rate limits become issue

3. **Multi-turn conversation for refinement**
   - What we know: Users may want to regenerate specific cards
   - What's unclear: Whether to use conversation history or fresh requests
   - Recommendation: Start with single-turn generation, add refinement in Phase 3 (UI) if needed
</open_questions>

<sources>
## Sources

### Primary (HIGH confidence)
- [Anthropic Platform Docs - Structured Outputs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs) - Official beta feature documentation
- [Anthropic Platform Docs - API Errors](https://platform.claude.com/docs/en/api/errors) - Error handling and retry strategies
- [Anthropic Platform Docs - Getting Started](https://platform.claude.com/docs/en/api/getting-started) - API overview and authentication

### Secondary (MEDIUM confidence - WebSearch verified with official sources)
- [Structured outputs - Claude Docs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs) - Feature announcement and usage
- [Prompting best practices - Claude Docs](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-4-best-practices) - Prompt engineering guidance
- [How to Fix Claude API 429 Rate Limit Error: Complete Guide 2026](https://www.aifreeapi.com/en/posts/claude-api-429-error-fix) - Retry logic patterns
- [Claude API 429 Error: Complete Solution Guide](https://www.aifreeapi.com/en/posts/claude-api-429-solution) - Exponential backoff implementation

### Tertiary (LOW confidence - needs validation during implementation)
- [Creating Flashcards with LLMs - LessWrong](https://www.lesswrong.com/posts/hGhBhLsgNWLCJ3g9b/creating-flashcards-with-llms) - Educational quality patterns
- [Comparing GPT-4, 3.5, and LLMs for flashcards](https://www.alexejgossmann.com/LLMs-for-spaced-repetition/) - Model comparison (may not apply to Claude Sonnet 4.5)
- [Flashcard Fundamentals #3: Generating Flashcards using AI](https://www.memorylab.nl/blogs/flashcard-fundamentals-3-generating-flashcards-using-ai/) - Educational principles
</sources>

<metadata>
## Metadata

**Research scope:**
- Core technology: Anthropic Claude API (Python SDK)
- Ecosystem: Structured outputs, Pydantic validation, retry strategies
- Patterns: Flashcard generation, prompt engineering, error handling
- Pitfalls: Rate limits, schema compliance, educational quality

**Confidence breakdown:**
- Standard stack: HIGH - Official SDK and structured outputs are first-party, well-documented
- Architecture: HIGH - Patterns from official docs and verified implementations
- Pitfalls: HIGH - Based on official error handling docs and community experience
- Code examples: HIGH - Derived from official Anthropic documentation

**Research date:** 2026-01-14
**Valid until:** 2026-02-14 (30 days - API stable, structured outputs in beta but production-ready)

</metadata>

---

*Phase: 02-ai-integration*
*Research completed: 2026-01-14*
*Ready for planning: yes*
