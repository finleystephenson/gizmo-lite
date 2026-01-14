# AI Flashcard Generator

## What This Is

A local Python web app that transforms revision notes into active recall flashcards using Claude AI. Students paste their study material (e.g., "Biology Topic 4: Photosynthesis"), and the app generates structured flashcard decks stored in SQLite. Includes a clean study interface with spaced repetition - wrong answers get re-queued at the end of each session.

## Core Value

**Make creating high-quality flashcards effortless.** Instead of manually writing dozens of cards, students paste their notes and get AI-generated active recall questions in seconds, so they can focus on studying rather than card creation.

## Requirements

### Validated

(None yet — ship to validate)

### Active

- [ ] **Paste & Generate Interface**: Web page with textarea for notes, "Generate Flashcards" button, and topic name input
- [ ] **AI-Powered Card Generation**: Send notes to Claude API, receive 10 question-answer pairs as structured JSON focused on key concepts
- [ ] **Local Storage**: SQLite database storing flashcards organized into decks by topic name
- [ ] **Study Mode Interface**: Clean flashcard UI showing question first, "Reveal Answer" button, then "Got it" / "Needs Practice" buttons
- [ ] **Simple Spaced Repetition**: Cards marked "Needs Practice" get re-queued at end of current study session
- [ ] **Edit Before Saving**: Review and modify AI-generated cards before adding them to deck
- [ ] **Deck Management**: Delete entire decks or individual cards from library
- [ ] **Study Statistics**: Track cards studied, success rate per deck, overall progress
- [ ] **Export/Import Decks**: Share decks with classmates or backup flashcard collections

### Out of Scope

- **Cloud sync or multi-user support** — keeping it simple and local-first for v1
- **Advanced spaced repetition algorithms (like Anki's SM-2)** — using simple "wrong cards repeat at end" logic instead
- **Mobile app** — web interface should work on mobile browsers, but no native app
- **Image/media support in cards** — text-only flashcards for v1
- **Pre-made deck marketplace** — students create their own decks from their notes

## Context

**Inspiration:** Combines Gizmo.ai's AI generation approach with Seneca's clean study interface.

**User Journey:**
1. Student has revision notes from class/textbook
2. Pastes notes into web interface with topic name
3. Reviews AI-generated flashcards, edits if needed
4. Saves to database as a deck
5. Studies using flashcard interface with simple progress tracking
6. Wrong answers get re-shown at end of session

**Tech Stack:**
- Backend: Flask (Python web framework - lightweight and beginner-friendly)
- Frontend: HTML templates with Tailwind CSS (clean, modern styling)
- Database: SQLite (local file-based database)
- AI: Anthropic Claude API (structured JSON generation)

**Learning Focus:** User is a student learning this stack, so code should be well-organized, clearly documented, and explained step-by-step.

## Constraints

- **Tech Stack**: Flask + Tailwind + SQLite + Anthropic API (chosen for simplicity and learning)
- **Local-first**: Must run entirely on user's machine, no cloud deployment required
- **API Key**: User needs Anthropic API key (instructions in README)
- **Card Count**: Generate 10 flashcards per topic by default

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Flask over Django/FastAPI | Lightweight, easier for student to learn, less boilerplate | — Pending |
| Tailwind CSS over custom CSS | Modern utility-first approach, faster development, easy to customize | — Pending |
| SQLite over PostgreSQL | No server setup needed, perfect for local-first app, simpler for learning | — Pending |
| Simple re-queue algorithm | Easy to understand and implement, good enough for v1 before adding complex spaced repetition | — Pending |
| Interactive mode | Student wants to understand each step, not have 50 files generated at once | — Pending |

---

*Last updated: 2026-01-14 after initialization*
