"""
Flashcard model for managing individual flashcards with study statistics.

Each flashcard belongs to a deck and tracks study performance metrics.
Uses raw SQL with sqlite3 cursor (no ORM) for simplicity.
"""

import time
from .database import get_db


class Flashcard:
    """
    Model for individual flashcards with question-answer pairs and statistics.

    Schema:
        id: INTEGER PRIMARY KEY
        deck_id: INTEGER NOT NULL (FOREIGN KEY to decks.id)
        question: TEXT NOT NULL
        answer: TEXT NOT NULL
        created_at: REAL (Unix timestamp)
        studied_count: INTEGER DEFAULT 0
        success_count: INTEGER DEFAULT 0
        last_studied: REAL (Unix timestamp, nullable)
        streak: INTEGER DEFAULT 0
    """

    @staticmethod
    def create(deck_id, question, answer):
        """
        Create a new flashcard.

        Args:
            deck_id (int): ID of the deck this flashcard belongs to
            question (str): Question text
            answer (str): Answer text

        Returns:
            dict: Created flashcard with all fields
        """
        conn = get_db()
        cursor = conn.cursor()

        created_at = time.time()

        cursor.execute(
            '''INSERT INTO flashcards
               (deck_id, question, answer, created_at, studied_count, success_count, last_studied, streak)
               VALUES (?, ?, ?, ?, 0, 0, NULL, 0)''',
            (deck_id, question, answer, created_at)
        )
        conn.commit()

        flashcard_id = cursor.lastrowid

        # Return the created flashcard
        cursor.execute('SELECT * FROM flashcards WHERE id = ?', (flashcard_id,))
        row = cursor.fetchone()
        conn.close()

        return dict(row) if row else None

    @staticmethod
    def get_by_deck(deck_id):
        """
        Get all flashcards for a specific deck.

        Args:
            deck_id (int): Deck ID to get flashcards from

        Returns:
            list[dict]: List of flashcards in the deck
        """
        conn = get_db()
        cursor = conn.cursor()

        cursor.execute(
            'SELECT * FROM flashcards WHERE deck_id = ? ORDER BY created_at ASC',
            (deck_id,)
        )
        rows = cursor.fetchall()
        conn.close()

        return [dict(row) for row in rows]

    @staticmethod
    def update_stats(flashcard_id, success):
        """
        Update study statistics for a flashcard.

        Args:
            flashcard_id (int): Flashcard ID
            success (bool): Whether the answer was correct

        Returns:
            dict: Updated flashcard data or None if not found
        """
        conn = get_db()
        cursor = conn.cursor()

        # Get current stats
        cursor.execute('SELECT * FROM flashcards WHERE id = ?', (flashcard_id,))
        row = cursor.fetchone()

        if not row:
            conn.close()
            return None

        current = dict(row)
        studied_count = current['studied_count'] + 1
        success_count = current['success_count'] + (1 if success else 0)
        last_studied = time.time()
        streak = current['streak'] + 1 if success else 0

        # Update the flashcard
        cursor.execute(
            '''UPDATE flashcards
               SET studied_count = ?, success_count = ?, last_studied = ?, streak = ?
               WHERE id = ?''',
            (studied_count, success_count, last_studied, streak, flashcard_id)
        )
        conn.commit()

        # Return updated flashcard
        cursor.execute('SELECT * FROM flashcards WHERE id = ?', (flashcard_id,))
        row = cursor.fetchone()
        conn.close()

        return dict(row) if row else None

    @staticmethod
    def update(flashcard_id, question=None, answer=None):
        """
        Update flashcard question and/or answer.

        Args:
            flashcard_id (int): Flashcard ID to update
            question (str, optional): New question text
            answer (str, optional): New answer text

        Returns:
            dict: Updated flashcard data or None if not found
        """
        conn = get_db()
        cursor = conn.cursor()

        # Build dynamic UPDATE query based on provided fields
        updates = []
        params = []

        if question is not None:
            updates.append('question = ?')
            params.append(question)

        if answer is not None:
            updates.append('answer = ?')
            params.append(answer)

        if not updates:
            conn.close()
            return None

        params.append(flashcard_id)
        query = f"UPDATE flashcards SET {', '.join(updates)} WHERE id = ?"

        cursor.execute(query, params)
        conn.commit()

        # Return updated flashcard
        cursor.execute('SELECT * FROM flashcards WHERE id = ?', (flashcard_id,))
        row = cursor.fetchone()
        conn.close()

        return dict(row) if row else None

    @staticmethod
    def delete(flashcard_id):
        """
        Delete a flashcard by ID.

        Args:
            flashcard_id (int): Flashcard ID to delete

        Returns:
            bool: True if deleted, False if not found
        """
        conn = get_db()
        cursor = conn.cursor()

        cursor.execute('DELETE FROM flashcards WHERE id = ?', (flashcard_id,))
        conn.commit()

        deleted = cursor.rowcount > 0
        conn.close()

        return deleted
