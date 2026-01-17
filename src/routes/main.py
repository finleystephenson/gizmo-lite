"""
Main routes module for AI Flashcard Generator.

This module defines the homepage and flashcard generation routes.

For students: Routes are URL endpoints that your Flask app responds to.
Each route function (called a "view") handles a specific URL pattern.
"""

from flask import Blueprint, render_template, request, redirect, url_for, jsonify, session, flash, Response
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
    It queries all decks with their study statistics.
    """
    from datetime import datetime

    # Get all decks with their statistics
    # For students: Deck.get_all_with_stats() returns deck data + aggregated flashcard stats
    decks = Deck.get_all_with_stats()

    # Format dates and add card_count alias for each deck
    # For students: We format timestamps as readable dates and ensure backward compatibility
    decks_with_dates = []
    for deck in decks:
        # Format the created_at timestamp as a human-readable date
        created_date = datetime.fromtimestamp(deck['created_at']).strftime('%b %d, %Y')

        # Format last_studied timestamp if available
        if deck.get('last_studied'):
            last_studied_date = datetime.fromtimestamp(deck['last_studied']).strftime('%b %d, %Y')
        else:
            last_studied_date = None

        # Add formatted dates and card_count alias (total_cards from stats)
        decks_with_dates.append({
            **deck,
            'card_count': deck['total_cards'],
            'created_date': created_date,
            'last_studied_date': last_studied_date
        })

    # Render decks template with the enhanced deck data
    # For students: The template receives decks with stats and formatted dates
    return render_template('decks.html', decks=decks_with_dates)


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
    # Only initialize cards_studied if starting a NEW session (not resuming existing one)
    if session.get('studying_deck_id') != deck_id:
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


@main.route('/study/<int:deck_id>/grade', methods=['POST'])
def grade_card(deck_id):
    """
    Grade a flashcard during study session and update statistics.

    For students: This endpoint receives JSON data from the JavaScript gradeCard() function.
    It validates the session state, updates the flashcard's statistics in the database,
    and tracks the result in the session for summary statistics later.
    """
    # Get JSON data from request
    # For students: The fetch() call from JavaScript sends card_id and success (boolean)
    data = request.get_json()

    # Validate request has JSON data
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    # Extract card_id and success from request
    card_id = data.get('card_id')
    success = data.get('success')

    # Validate required fields are present
    if card_id is None or success is None:
        return jsonify({'error': 'Missing card_id or success'}), 400

    # Validate session state
    # For students: We check that the deck_id matches the session to prevent
    # someone from grading cards from a different deck than they're studying
    if session.get('studying_deck_id') != deck_id:
        return jsonify({'error': 'Invalid session'}), 403

    # Update flashcard statistics in database
    # For students: Flashcard.update_stats() increments studied_count,
    # updates success_count if success=True, sets last_studied timestamp,
    # and updates the streak counter
    try:
        updated_card = Flashcard.update_stats(card_id, success)
        if not updated_card:
            return jsonify({'error': 'Flashcard not found'}), 404

        # Track this result in the session
        # For students: We append the result to the session's cards_studied list
        # This will be used later for the session summary statistics
        if 'cards_studied' not in session:
            session['cards_studied'] = []
        session['cards_studied'].append({
            'card_id': card_id,
            'success': success
        })
        # IMPORTANT: Tell Flask the session was modified (needed for mutable objects like lists)
        session.modified = True

        # DEBUG
        import sys
        print(f"DEBUG GRADE: Added card {card_id}, success={success}. Total cards studied: {len(session['cards_studied'])}", file=sys.stderr, flush=True)

        # Return success response
        return jsonify({'success': True}), 200

    except Exception as e:
        # For students: If something goes wrong with the database update,
        # return a 500 error with the error message
        return jsonify({'error': str(e)}), 500


@main.route('/study/<int:deck_id>/summary', methods=['GET', 'POST'])
def study_summary(deck_id):
    """
    Display session summary with performance statistics and cards needing practice.

    For students: This route handles two cases:
    - POST: Receives study results from JavaScript and stores them in session
    - GET: Displays the summary page with statistics

    The client-side JavaScript tracks all results and POSTs them at session end,
    which is more reliable than trying to maintain session state across many AJAX calls.

    With spaced repetition, the summary now also shows:
    - Total attempts (may be > card count if cards were re-queued)
    - All cards mastered (session only ends when all "Got it!")
    """
    # Load deck from database
    deck = Deck.get_by_id(deck_id)
    if not deck:
        return "Deck not found", 404

    # Handle POST - receiving results from JavaScript
    if request.method == 'POST':
        data = request.get_json()
        if data and 'results' in data:
            # Store results in session for the subsequent GET request
            # For students: Now includes total_attempts from spaced repetition tracking
            session['summary_results'] = data['results']
            session['summary_deck_id'] = deck_id
            session['summary_total_attempts'] = data.get('total_attempts', len(data['results']))
            session['summary_cards_mastered'] = data.get('cards_mastered', 0)
            session.modified = True
            return jsonify({'success': True}), 200
        return jsonify({'error': 'No results provided'}), 400

    # Handle GET - display summary page
    # Check if we have results from the POST
    cards_studied = session.get('summary_results', [])
    stored_deck_id = session.get('summary_deck_id')

    # Validate we have results for this deck
    if not cards_studied or stored_deck_id != deck_id:
        # No results - redirect back to study page
        return redirect(url_for('main.study', deck_id=deck_id))

    # Get spaced repetition metrics from session
    # For students: total_attempts counts how many times cards were shown overall
    # This differs from card count because "Needs Practice" cards get re-queued
    total_attempts = session.get('summary_total_attempts', len(cards_studied))
    cards_mastered = session.get('summary_cards_mastered', 0)

    # Calculate statistics from all attempts
    # For students: With spaced repetition, results array includes ALL attempts
    # including repeated attempts on re-queued cards
    total_cards = cards_mastered  # Number of unique cards (all mastered by end)

    # Count unique cards and their FINAL status (all should be success=True at end)
    # For students: Since session only ends when all cards mastered, final success rate is 100%
    # But we show the journey - how many attempts were needed
    unique_card_ids = set(card.get('card_id') for card in cards_studied)
    total_unique_cards = len(unique_card_ids) if unique_card_ids else cards_mastered

    # Use unique card count (same as cards_mastered since all are mastered at end)
    if total_unique_cards == 0:
        total_unique_cards = cards_mastered if cards_mastered > 0 else len(cards_studied)

    # Success rate based on all attempts (some were "Needs Practice")
    success_attempts = sum(1 for card in cards_studied if card.get('success'))
    needs_practice_attempts = len(cards_studied) - success_attempts
    success_rate = round((success_attempts / len(cards_studied)) * 100, 1) if cards_studied else 100

    # Get questions that needed multiple attempts
    # For students: Count how many times each card was shown to identify trouble spots
    card_attempt_counts = {}
    for result in cards_studied:
        card_id = result.get('card_id')
        if card_id:
            card_attempt_counts[card_id] = card_attempt_counts.get(card_id, 0) + 1

    # Find cards that needed extra practice (shown more than once)
    # For students: These are the cards that were re-queued at least once
    cards_needing_extra = []
    for result in cards_studied:
        card_id = result.get('card_id')
        question = result.get('question', '')
        attempt_count = card_attempt_counts.get(card_id, 1)
        if attempt_count > 1 and question not in [c['question'] for c in cards_needing_extra]:
            cards_needing_extra.append({
                'question': question,
                'attempts': attempt_count
            })

    # Clear session study data
    # For students: Important cleanup - we remove the session data after displaying it
    session.pop('summary_results', None)
    session.pop('summary_deck_id', None)
    session.pop('summary_total_attempts', None)
    session.pop('summary_cards_mastered', None)
    session.pop('studying_deck_id', None)
    session.pop('cards_studied', None)

    # Render summary template with all the calculated data
    # For students: Template now receives additional spaced repetition stats
    return render_template(
        'summary.html',
        deck=deck,
        total_cards=total_unique_cards,
        total_attempts=total_attempts,
        success_count=success_attempts,
        needs_practice_count=needs_practice_attempts,
        success_rate=success_rate,
        cards_needing_extra=cards_needing_extra
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


@main.route('/deck/<int:deck_id>/delete', methods=['POST'])
def delete_deck(deck_id):
    """
    Delete a deck and all its flashcards.

    For students: This endpoint handles POST requests to delete a deck.
    The Deck.delete() method uses CASCADE deletion, so all flashcards
    in the deck are automatically deleted when the deck is removed.
    After deletion, the user is redirected back to the decks list.
    """
    # Attempt to delete the deck
    # For students: Deck.delete() returns True if deleted, False if not found
    deleted = Deck.delete(deck_id)

    if not deleted:
        return "Deck not found", 404

    # Redirect back to decks page after successful deletion
    # For students: url_for() generates the URL for the named route
    return redirect(url_for('main.decks'))


@main.route('/deck/<int:deck_id>/export')
def export_deck(deck_id):
    """
    Export a deck as a downloadable JSON file.

    For students: This endpoint creates a JSON file download containing the deck
    name and all flashcard question-answer pairs. Users can share this file with
    classmates who can then import it to create a copy of the deck.

    The Content-Disposition header tells the browser to download the file
    rather than display it, and specifies the suggested filename.
    """
    import json

    # Get the deck data for export
    # For students: Deck.export_to_dict() returns None if deck not found
    deck_data = Deck.export_to_dict(deck_id)

    if not deck_data:
        flash('Deck not found', 'error')
        return redirect(url_for('main.decks'))

    # Create JSON string with nice formatting
    # For students: indent=2 makes the JSON human-readable
    json_content = json.dumps(deck_data, indent=2)

    # Create a safe filename from the deck name
    # For students: We replace spaces with underscores and keep it simple
    safe_name = deck_data['name'].replace(' ', '_').replace('/', '_')
    filename = f"{safe_name}_flashcards.json"

    # Return the JSON as a downloadable file
    # For students: Response() creates a custom HTTP response
    # - mimetype: tells browser this is JSON data
    # - Content-Disposition: tells browser to download as file with specified name
    return Response(
        json_content,
        mimetype='application/json',
        headers={'Content-Disposition': f'attachment; filename="{filename}"'}
    )


@main.route('/card/<int:card_id>/delete', methods=['POST'])
def delete_card(card_id):
    """
    Delete an individual flashcard.

    For students: This endpoint handles AJAX requests from JavaScript.
    It returns JSON to allow client-side UI updates without page reload.
    The Flashcard.delete() method removes the card from the database.
    """
    # Attempt to delete the flashcard
    # For students: Flashcard.delete() returns True if deleted, False if not found
    deleted = Flashcard.delete(card_id)

    if not deleted:
        return jsonify({'error': 'Flashcard not found'}), 404

    # Return JSON success response
    # For students: The JavaScript will use this to remove the card from the DOM
    return jsonify({'success': True}), 200


@main.route('/stats')
def statistics():
    """
    Display statistics dashboard showing study progress across all decks.

    For students: This route aggregates statistics from all flashcards
    to show overall progress and per-deck breakdowns. It uses helper
    methods in the Deck and Flashcard models for data aggregation.
    """
    from datetime import datetime

    # Get overall statistics across all decks
    # For students: Deck.get_overall_stats() aggregates data from all flashcards
    overall = Deck.get_overall_stats()

    # Format the last studied timestamp as human-readable date
    if overall['last_studied']:
        overall['last_studied_date'] = datetime.fromtimestamp(
            overall['last_studied']
        ).strftime('%b %d, %Y at %I:%M %p')
    else:
        overall['last_studied_date'] = 'Never'

    # Get all decks with their individual statistics
    # For students: Deck.get_all_with_stats() returns deck data + flashcard stats
    decks = Deck.get_all_with_stats()

    # Format dates for each deck
    for deck in decks:
        if deck['last_studied']:
            deck['last_studied_date'] = datetime.fromtimestamp(
                deck['last_studied']
            ).strftime('%b %d, %Y')
        else:
            deck['last_studied_date'] = 'Never'

    # Render statistics template
    return render_template('stats.html', overall=overall, decks=decks)
