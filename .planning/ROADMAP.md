# Roadmap: AI Flashcard Generator

**Project:** AI Flashcard Generator
**Created:** 2026-01-14
**Status:** Active Development

## Overview

This roadmap breaks down the AI Flashcard Generator into 7 sequential phases, building from foundation to full feature set. Each phase delivers working functionality before moving to the next.

---

## Phase 1: Foundation & Database Setup ✓

**Status:** Complete (2026-01-14)

**Goal:** Set up project infrastructure and database schema for storing flashcards.

**Delivers:**
- Project structure with Flask app skeleton
- SQLite database with tables for decks and flashcards
- Basic configuration (API key management)
- Development environment setup (.gitignore, requirements.txt, README)

**Success Criteria:**
- [x] Flask app runs locally
- [x] Database tables created and queryable
- [x] Environment variables loaded from .env
- [x] README has setup instructions

**Research Needed:** No

**Completed Plans:**
- 01-01: Project Foundation (3 tasks, 1 min)
- 01-02: Database Schema & Models (3 tasks, 4 min)
- 01-03: Flask Configuration and Setup (4 tasks, 15 min)

---

## Phase 2: AI Integration ✓

**Status:** Complete (2026-01-14)

**Goal:** Integrate Anthropic Claude API to generate flashcards from notes.

**Delivers:**
- API client for Claude with structured JSON prompt
- Prompt engineering to generate 10 Q&A pairs focused on key concepts
- Error handling for API failures
- Sample output validation

**Success Criteria:**
- [x] Can send notes to Claude API
- [x] Receives 10 structured question-answer pairs
- [x] Handles API errors gracefully
- [x] Generated cards focus on active recall

**Research Completed:** 2026-01-14
- Anthropic structured outputs with client.beta.messages.parse()
- Pydantic models for type-safe responses
- Educational prompt engineering patterns

**Completed Plans:**
- 02-01: Core AI Service with Structured Outputs (2 tasks, 2 min)
- 02-02: Error Handling & Database Integration (2 tasks, 8 min)

---

## Phase 3: Card Generation Interface

**Goal:** Build web interface for pasting notes and generating flashcards.

**Delivers:**
- Homepage with textarea for notes input
- Topic name input field
- "Generate Flashcards" button triggering Claude API
- Loading state while generating
- Card preview list with modal edit functionality

**Success Criteria:**
- [ ] Can paste notes and enter topic name
- [ ] Generates 10 cards via Claude API
- [ ] Displays cards in preview list
- [ ] Can open modal popup to edit individual cards
- [ ] Can save edited deck to database

**Research Needed:** No

---

## Phase 4: Study Mode Interface

**Goal:** Create clean flashcard study interface with spaced repetition tracking.

**Delivers:**
- Deck selection page listing all saved decks
- Study mode showing one card at a time
- "Reveal Answer" button (question → answer transition)
- "Got it" / "Needs Practice" buttons
- Session end summary with stats

**Success Criteria:**
- [ ] Can select deck to study
- [ ] Cards display question first, then reveal answer
- [ ] Buttons correctly mark card status
- [ ] Session shows summary: X/Y correct, list of cards to practice
- [ ] Returns to deck selection after session

**Research Needed:** No

---

## Phase 5: Spaced Repetition Logic

**Goal:** Implement simple re-queue system for cards marked "Needs Practice".

**Delivers:**
- Cards marked "Needs Practice" added to end of current session queue
- Session doesn't end until all cards answered "Got it" at least once
- Database tracking of card performance

**Success Criteria:**
- [ ] "Needs Practice" cards re-appear at end of session
- [ ] Session completes when all cards marked "Got it"
- [ ] Card attempts tracked in database
- [ ] No complex spaced repetition algorithm (simple re-queue only)

**Research Needed:** No

---

## Phase 6: Deck Management & Statistics

**Goal:** Add deck/card management and progress tracking.

**Delivers:**
- Delete deck functionality
- Delete individual cards from deck
- Statistics page showing:
  - Cards studied count per deck
  - Success rate percentage per deck
  - Last studied timestamp
  - Study streak (consecutive days)
- Overall progress dashboard

**Success Criteria:**
- [ ] Can delete entire decks
- [ ] Can delete individual cards within deck
- [ ] Statistics page displays all 4 metrics
- [ ] Stats update after each study session
- [ ] Streak increments correctly on consecutive days

**Research Needed:** No

---

## Phase 7: Export/Import & Polish

**Goal:** Add deck sharing via JSON export/import and final polish.

**Delivers:**
- Export deck to JSON file (structured format with metadata)
- Import deck from JSON file
- Error handling for corrupted imports
- UI polish (Tailwind styling consistency)
- Mobile responsive design
- Final testing and bug fixes

**Success Criteria:**
- [ ] Can export deck as .json file
- [ ] Can import deck from .json file
- [ ] Invalid imports show helpful error messages
- [ ] UI looks clean on desktop and mobile
- [ ] All features tested end-to-end

**Research Needed:** No

---

## Research Notes

**Phase 2 - AI Integration** will require research into:
1. Anthropic API authentication and request format
2. Prompt engineering best practices for educational flashcards
3. Structured output format (ensuring consistent JSON responses)
4. Rate limiting and error handling strategies

This research should happen BEFORE planning Phase 2 to ensure the implementation approach is well-informed.

---

## Dependencies

```
Phase 1 (Foundation) → Phase 2 (AI) → Phase 3 (Generation UI) → Phase 4 (Study UI) → Phase 5 (Spaced Repetition) → Phase 6 (Management) → Phase 7 (Export/Polish)
```

Each phase builds on the previous. No parallel work possible due to linear dependencies.

---

*Roadmap created: 2026-01-14*
*Last updated: 2026-01-14 (Phase 2 complete)*
