"""
Flask application entry point for AI Flashcard Generator.

This module creates and configures the Flask application.

For students: This is the main file that starts your web server.
When you run this file, Flask will:
1. Load configuration (API keys, database settings)
2. Initialize the database (create tables if they don't exist)
3. Start a web server on http://localhost:5000
"""

from flask import Flask
from src.config import Config
from src.models.database import init_db

# Create Flask application instance
# template_folder: Where Flask looks for HTML templates (we'll create these in Phase 3)
# static_folder: Where Flask serves CSS, JS, and images from
app = Flask(__name__, template_folder='templates', static_folder='static')

# Load configuration from Config class
# This reads environment variables (API keys, etc.) from .env file
app.config.from_object(Config)

# Initialize database on startup
# This creates the decks and flashcards tables if they don't exist yet
# It's safe to run multiple times - won't delete existing data
init_db()


# Basic route for testing
# This is a temporary homepage - we'll build the real UI in Phase 3
@app.route('/')
def index():
    """
    Homepage route - returns simple welcome message.

    For students: Routes define the URLs your app responds to.
    The @app.route('/') decorator means this function handles requests to the root URL.
    """
    return "AI Flashcard Generator - Coming Soon"


# Run the Flask development server
# This only executes when you run this file directly (python src/app.py)
if __name__ == '__main__':
    # debug=True enables auto-reload when you change code and shows detailed error messages
    # WARNING: Never use debug=True in production!
    app.run(debug=True)
