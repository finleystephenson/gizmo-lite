"""
Configuration module for AI Flashcard Generator.

This module loads environment variables from a .env file and provides
configuration settings for the Flask application.

For students: Configuration management is important because:
- It separates secrets (API keys) from code
- Makes the app work in different environments (dev, prod)
- Keeps sensitive data out of version control
"""

import os
import secrets
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
# The .env file should be in the project root (parent of src/)
project_root = Path(__file__).parent.parent
env_path = project_root / '.env'
load_dotenv(dotenv_path=env_path)


class Config:
    """
    Application configuration class.

    Loads settings from environment variables with sensible defaults.
    Environment variables are set in the .env file (see .env.example).
    """

    # ANTHROPIC_API_KEY: Required for AI-powered flashcard generation (Phase 2)
    # Get your API key from: https://console.anthropic.com/settings/keys
    # This will be needed when we implement the AI features
    ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY', '')

    # SECRET_KEY: Used by Flask for session security and CSRF protection
    # In production, you should set this to a fixed secret value in .env
    # For development, we generate a random one each time (not persistent)
    SECRET_KEY = os.getenv('SECRET_KEY', secrets.token_hex(32))

    # DATABASE_PATH: Location of the SQLite database file
    # Defaults to 'flashcards.db' in the project root
    DATABASE_PATH = os.getenv('DATABASE_PATH', str(project_root / 'flashcards.db'))
