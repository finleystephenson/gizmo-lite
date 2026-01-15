"""
Main routes module for AI Flashcard Generator.

This module defines the homepage and flashcard generation routes.

For students: Routes are URL endpoints that your Flask app responds to.
Each route function (called a "view") handles a specific URL pattern.
"""

from flask import Blueprint, render_template, request, redirect, url_for, jsonify, session
from src.services.flashcard_generator import FlashcardGenerator
from src.models.deck import Deck
from src.models.flashcard import Flashcard

# Create a Blueprint named 'main'
# Blueprints organize related routes into modules
# For students: Think of this as a collection of related URL handlers
main = Blueprint('main', __name__)


@main.route('/')
def index():
    """
    Homepage route - displays the flashcard generation form.

    For students: The @main.route('/') decorator means this function
    handles GET requests to the root URL (http://localhost:5000/).
    """
    # render_template looks for index.html in src/templates/
    # It processes Jinja2 template syntax and returns HTML
    return render_template('index.html')


@main.route('/generate', methods=['POST'])
def generate():
    """
    Generate flashcards from study notes using AI.

    For students: The methods=['POST'] parameter means this function
    only handles POST requests (form submissions).
    The form data is accessed via request.form dictionary.
    """
    # Get form data from the homepage form
    # request.form.get() safely retrieves form field values
    notes = request.form.get('notes')
    topic = request.form.get('topic')

    # Validate inputs - ensure both fields were filled in
    if not notes or not topic:
        return "Missing notes or topic", 400

    try:
        # Generate and save flashcards using the AI service
        # For students: This is the FlashcardGenerator from Phase 2
        # It handles API calls, retries, and database saving automatically
        generator = FlashcardGenerator()
        result = generator.generate_and_save(notes, topic)

        # Redirect to preview page with the new deck_id
        # For students: url_for() generates the URL for a named route
        # This creates /preview/<deck_id> URL dynamically
        return redirect(url_for('main.preview', deck_id=result['deck_id']))

    except ValueError as e:
        # API errors return ValueError with user-friendly messages
        # For students: The FlashcardGenerator wraps API errors in ValueError
        # with helpful messages like "Rate limit exceeded" or "Invalid API key"
        return render_template('error.html', error=str(e)), 500


@main.route('/preview/<int:deck_id>')
def preview(deck_id):
    """
    Preview generated flashcards before study.

    For students: The <int:deck_id> in the route means Flask will
    automatically convert the URL parameter to an integer and pass it
    as the deck_id argument to this function.
    """
    # Load deck and flashcards from database
    # For students: These are the Deck and Flashcard models from Phase 1
    deck = Deck.get_by_id(deck_id)
    if not deck:
        return "Deck not found", 404

    flashcards = Flashcard.get_by_deck(deck_id)

    # Render preview template with deck and flashcard data
    # For students: These variables become available in the template as {{ deck }} and {{ flashcards }}
    return render_template('preview.html', deck=deck, flashcards=flashcards)


@main.route('/decks')
def decks():
    """
    Display all saved decks for user to select which one to study.

    For students: This route provides the entry point to study mode.
    It queries all decks and calculates flashcard counts for each deck.
    """
    # Get all decks from database
    # For students: Deck.get_all() returns a list of deck dictionaries
    decks = Deck.get_all()

    # Add card count to each deck
    # For students: We loop through each deck and count its flashcards
    # The card_count is added to the deck dictionary for display
    decks_with_counts = []
    for deck in decks:
        # Get all flashcards for this deck
        flashcards = Flashcard.get_by_deck(deck['id'])
        card_count = len(flashcards)

        # Format the created_at timestamp as a human-readable date
        # For students: Unix timestamp (seconds since 1970) → readable string
        from datetime import datetime
        created_date = datetime.fromtimestamp(deck['created_at']).strftime('%b %d, %Y')

        # Add count and formatted date to deck data
        decks_with_counts.append({
            **deck,
            'card_count': card_count,
            'created_date': created_date
        })

    # Render decks template with the enhanced deck data
    # For students: The template receives decks with card_count and created_date fields
    return render_template('decks.html', decks=decks_with_counts)


@main.route('/study/<int:deck_id>')
def study(deck_id):
    """
    Start study session for a deck - loads all flashcards and initializes session tracking.

    For students: This route handles GET requests to /study/<deck_id>.
    It loads the deck and all flashcards, then renders the study template.
    Session tracking allows us to monitor the study session across multiple requests.
    """
    # Load deck from database
    # For students: Deck.get_by_id() returns None if the deck doesn't exist
    deck = Deck.get_by_id(deck_id)
    if not deck:
        return "Deck not found", 404

    # Load all flashcards for this deck
    # For students: Flashcard.get_by_deck() returns a list of all cards in the deck
    flashcards = Flashcard.get_by_deck(deck_id)

    # Check if deck has any flashcards
    if not flashcards:
        return "This deck has no flashcards", 400

    # Initialize session state for tracking this study session
    # For students: Flask session is a secure cookie that persists across requests
    # We store the deck_id to validate grade requests and track which cards were studied
    session['studying_deck_id'] = deck_id
    session['cards_studied'] = []  # Will store results: [{'card_id': 1, 'success': True}, ...]

    # Render study template with deck and flashcards data
    # For students: The template receives three variables:
    # - deck: dict with id and name
    # - flashcards: list of all cards (id, question, answer)
    # - total_cards: count for progress indicator
    return render_template(
        'study.html',
        deck=deck,
        flashcards=flashcards,
        total_cards=len(flashcards)
    )


@main.route('/card/<int:card_id>/edit', methods=['POST'])
def edit_card(card_id):
    """
    Update flashcard question and answer.

    For students: This endpoint handles AJAX requests from JavaScript.
    It accepts JSON data (not form data) and returns JSON response.
    The @main.route() decorator with methods=['POST'] means this only
    handles POST requests to /card/<card_id>/edit URLs.
    """
    # Get JSON data from request
    # For students: request.get_json() parses the JSON body sent by fetch()
    data = request.get_json()

    if not data:
        return jsonify({'error': 'No data provided'}), 400

    question = data.get('question')
    answer = data.get('answer')

    # Validate inputs
    if not question or not answer:
        return jsonify({'error': 'Question and answer are required'}), 400

    # Update card in database
    # For students: Flashcard.update() is from Phase 1 database models
    # It updates only the specified fields for the given card_id
    try:
        Flashcard.update(card_id, question=question, answer=answer)
        return jsonify({'success': True}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
