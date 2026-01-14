"""
Pydantic schema models for AI flashcard generation.

These models define the structured output format for the Anthropic API,
guaranteeing type-safe responses that match our exact schema requirements.
"""

from pydantic import BaseModel, Field
from typing import List


class FlashcardPair(BaseModel):
    """Single question-answer flashcard pair."""

    question: str = Field(
        description="Question testing understanding (not memorization)"
    )
    answer: str = Field(
        description="Detailed answer with explanation to reinforce learning"
    )


class FlashcardSet(BaseModel):
    """Complete set of flashcards for a topic."""

    topic: str = Field(
        description="Topic name for the flashcard deck"
    )
    flashcards: List[FlashcardPair] = Field(
        description="List of exactly 10 question-answer pairs"
    )
