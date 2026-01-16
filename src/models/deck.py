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

    @staticmethod
    def get_all_with_stats():
        """
        Get all decks with their statistics.

        For students: This method combines deck data with flashcard statistics.
        It calls Flashcard.get_deck_stats() for each deck to get aggregated stats.

        Returns:
            list[dict]: List of decks, each with additional stats fields
        """
        from .flashcard import Flashcard

        decks = Deck.get_all()
        decks_with_stats = []

        for deck in decks:
            stats = Flashcard.get_deck_stats(deck['id'])
            decks_with_stats.append({
                **deck,
                **stats
            })

        return decks_with_stats

    @staticmethod
    def get_overall_stats():
        """
        Get overall statistics across all decks.

        For students: This method aggregates statistics across the entire flashcard
        collection, useful for showing total progress on a statistics dashboard.

        Returns:
            dict: {
                'total_decks': int,
                'total_cards': int,
                'total_studied': int,
                'total_correct': int,
                'success_rate': float,
                'last_studied': float or None
            }
        """
        conn = get_db()
        cursor = conn.cursor()

        # Count total decks
        cursor.execute('SELECT COUNT(*) as count FROM decks')
        total_decks = cursor.fetchone()['count']

        # Get aggregate flashcard stats
        cursor.execute('''
            SELECT
                COUNT(*) as total_cards,
                COALESCE(SUM(studied_count), 0) as total_studied,
                COALESCE(SUM(success_count), 0) as total_correct,
                MAX(last_studied) as last_studied
            FROM flashcards
        ''')

        row = cursor.fetchone()
        conn.close()

        total_studied = row['total_studied']
        total_correct = row['total_correct']
        # Calculate success rate as percentage (avoid division by zero)
        success_rate = (total_correct / total_studied * 100) if total_studied > 0 else 0

        return {
            'total_decks': total_decks,
            'total_cards': row['total_cards'],
            'total_studied': total_studied,
            'total_correct': total_correct,
            'success_rate': round(success_rate, 1),
            'last_studied': row['last_studied']
        }
