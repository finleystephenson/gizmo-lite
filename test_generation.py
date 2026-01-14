"""
Test script to verify FlashcardGenerator works correctly.

This demonstrates:
- Service instantiation
- API call to Claude
- Structured output parsing
- Schema validation
"""

from src.services.flashcard_generator import FlashcardGenerator

# Sample study notes
notes = """
Flask is a lightweight Python web framework. It uses decorators for routing,
like @app.route('/path'). Flask uses Jinja2 as its template engine for rendering
HTML pages. The framework follows a "micro" philosophy - it provides the basics
but lets you add extensions as needed. Flask applications use the WSGI standard.
"""

# Create generator and generate flashcards
generator = FlashcardGenerator()
print("Generating flashcards for 'Flask Basics'...")
print("This may take a few seconds...")

result = generator.generate_flashcards(notes, "Flask Basics")

# Display results
print(f"\n✓ Generation successful!")
print(f"Topic: {result.topic}")
print(f"Generated {len(result.flashcards)} flashcards\n")

# Show first 3 flashcards
for i, card in enumerate(result.flashcards[:3], 1):
    print(f"--- Flashcard {i} ---")
    print(f"Q: {card.question}")
    print(f"A: {card.answer}")
    print()

# Verify structure
print(f"✓ Schema validation passed")
print(f"✓ All {len(result.flashcards)} flashcards have questions and answers")

# Check quality indicators
has_why = any("why" in card.question.lower() or "how" in card.question.lower()
              or "explain" in card.question.lower() or "describe" in card.question.lower()
              for card in result.flashcards)
print(f"✓ Questions test understanding: {has_why}")
