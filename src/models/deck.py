"""
Deck model for managing flashcard deck CRUD operations.

A deck represents a collection of flashcards organized by topic.
Uses raw SQL with sqlite3 cursor (no ORM) for simplicity.
"""

import time
from .database import get_db


class Deck:
    """
    Model for flashcard decks (topic-based organization).

    Schema:
        id: INTEGER PRIMARY KEY
        name: TEXT NOT NULL UNIQUE (topic name)
        created_at: REAL (Unix timestamp)
    """

    @staticmethod
    def create(name):
        """
        Create a new deck.

        Args:
            name (str): Unique topic name for the deck

        Returns:
            dict: Created deck with id, name, and created_at
        """
        conn = get_db()
        cursor = conn.cursor()

        created_at = time.time()

        cursor.execute(
            'INSERT INTO decks (name, created_at) VALUES (?, ?)',
            (name, created_at)
        )
        conn.commit()

        deck_id = cursor.lastrowid

        # Return the created deck
        deck = Deck.get_by_id(deck_id)
        conn.close()

        return deck

    @staticmethod
    def get_by_id(deck_id):
        """
        Get a deck by ID.

        Args:
            deck_id (int): Deck ID

        Returns:
            dict: Deck data or None if not found
        """
        conn = get_db()
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM decks WHERE id = ?', (deck_id,))
        row = cursor.fetchone()
        conn.close()

        if row:
            return dict(row)
        return None

    @staticmethod
    def get_all():
        """
        Get all decks.

        Returns:
            list[dict]: List of all decks
        """
        conn = get_db()
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM decks ORDER BY created_at DESC')
        rows = cursor.fetchall()
        conn.close()

        return [dict(row) for row in rows]

    @staticmethod
    def delete(deck_id):
        """
        Delete a deck by ID.

        Cascades to delete all flashcards in the deck due to ON DELETE CASCADE.

        Args:
            deck_id (int): Deck ID to delete

        Returns:
            bool: True if deleted, False if not found
        """
        conn = get_db()
        cursor = conn.cursor()

        cursor.execute('DELETE FROM decks WHERE id = ?', (deck_id,))
        conn.commit()

        deleted = cursor.rowcount > 0
        conn.close()

        return deleted
