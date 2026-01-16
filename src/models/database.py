"""
Database initialization module for SQLite flashcard storage.

This module provides connection helpers and table creation for the flashcard application.
Uses sqlite3 standard library (no ORM) for simplicity.
"""

import sqlite3
import os
from pathlib import Path


def get_db():
    """
    Get a connection to the SQLite database.

    Returns:
        sqlite3.Connection: Connection to flashcards.db in project root
    """
    # Get project root (parent of src directory)
    project_root = Path(__file__).parent.parent.parent
    db_path = project_root / 'flashcards.db'

    conn = sqlite3.connect(str(db_path), timeout=10.0)
    # Enable foreign key constraints
    conn.execute('PRAGMA foreign_keys = ON')
    # Return rows as dictionaries
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """
    Initialize the database by creating tables if they don't exist.

    Creates two tables:
    - decks: Stores flashcard deck information (topic-based organization)
    - flashcards: Stores individual flashcards with Q&A and study statistics

    Foreign key constraints ensure flashcards belong to valid decks.
    """
    conn = get_db()
    cursor = conn.cursor()

    # Create decks table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS decks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            created_at REAL NOT NULL
        )
    ''')

    # Create flashcards table with foreign key to decks
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS flashcards (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            deck_id INTEGER NOT NULL,
            question TEXT NOT NULL,
            answer TEXT NOT NULL,
            created_at REAL NOT NULL,
            studied_count INTEGER DEFAULT 0,
            success_count INTEGER DEFAULT 0,
            last_studied REAL,
            streak INTEGER DEFAULT 0,
            FOREIGN KEY (deck_id) REFERENCES decks(id) ON DELETE CASCADE
        )
    ''')

    conn.commit()
    conn.close()
