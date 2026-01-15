"""
Main routes module for AI Flashcard Generator.

This module defines the homepage and flashcard generation routes.

For students: Routes are URL endpoints that your Flask app responds to.
Each route function (called a "view") handles a specific URL pattern.
"""

from flask import Blueprint, render_template, request

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
