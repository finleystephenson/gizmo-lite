# Project State

**Project:** AI Flashcard Generator
**Mode:** Interactive (standard depth)
**Last Updated:** 2026-01-15

## Current Status

**Phase:** 4 of 7 (Study Mode Interface)
**Plan:** 1 of 3 in current phase
**Status:** In progress
**Last activity:** 2026-01-15 - Completed 04-01-PLAN.md (Deck Selection Page)

Progress: █████████████░ 50% (3/7 phases, 9/13 plans)

## Roadmap Progress

- [x] **Phase 1:** Foundation & Database Setup (3/3 plans complete)
- [x] **Phase 2:** AI Integration (2/2 plans complete)
- [x] **Phase 3:** Card Generation Interface (3/3 plans complete) ✅
- [ ] **Phase 4:** Study Mode Interface (1/3 plans complete)
- [ ] **Phase 5:** Spaced Repetition Logic
- [ ] **Phase 6:** Deck Management & Statistics
- [ ] **Phase 7:** Export/Import & Polish

**Total:** 3/7 phases complete, 9/13 plans complete

## Recent Activity

**2026-01-15:**
- **Phase 4 Started:** Study Mode Interface (1/3 plans)
  - Completed 04-01: Deck Selection Page
    - Created decks.html showing all saved decks with card counts
    - Implemented /decks route with data enrichment (card counts, formatted dates)
    - Added My Decks navigation link in header visible on all pages
    - Empty state UI for when no decks exist
    - Study Now buttons link to /study/{deck_id} (next plan)
- **Phase 3 Complete:** Card Generation Interface (3/3 plans)
  - Completed 03-01: Base Templates & Homepage
    - Created base.html with Tailwind CSS CDN
    - Created index.html with flashcard generation form
    - Implemented Blueprint pattern for routes
  - Completed 03-02: Flashcard Generation & Preview
    - Implemented /generate endpoint with AI integration
    - Created preview.html showing all generated cards
    - Created error.html for API error handling
    - Fixed API response parsing: response.content[0].parsed_output
  - Completed 03-03: Modal Card Editor
    - Added modal popup for editing flashcards
    - Implemented /card/<id>/edit endpoint with JSON API
    - Added Flashcard.update() method to model
    - JavaScript updates UI without page reload
  - All checkpoints verified and approved by user
  - Working end-to-end: form → AI generation → preview → edit → study button ready

**2026-01-14:**
- Mapped existing codebase (minimal Python project with empty files)
- Initialized project with /gsd:new-project
- Gathered requirements via interactive questioning
- Created 7-phase roadmap with research assessment
- Clarified UI/UX preferences:
  - Modal popup for card editing
  - JSON export format
  - Session end summary with stats
  - All 4 statistics metrics (count, rate, timestamp, streak)
- Completed 01-01-PLAN.md (Project Foundation):
  - Created src/ directory structure with Flask layout
  - Created .gitignore with Python standard exclusions
  - Created requirements.txt with Flask, python-dotenv, anthropic
- Completed 01-02-PLAN.md (Database Schema & Models):
  - Created SQLite database initialization module
  - Implemented Deck model with CRUD operations
  - Implemented Flashcard model with statistics tracking
  - Verified foreign key CASCADE behavior
- Completed 01-03-PLAN.md (Flask Configuration and Setup):
  - Created configuration module with environment variable management
  - Updated Flask app to initialize database on startup
  - Created .env.example with API key instructions
  - Created comprehensive README with setup guide for students
  - **Phase 1 complete:** Foundation ready for Phase 2 (AI Integration)
- Researched Phase 2 with /gsd:research-phase 2:
  - Comprehensive RESEARCH.md created (509 lines)
  - Standard stack: anthropic>=0.18.0, pydantic>=2.0.0
  - Architecture: structured outputs with client.beta.messages.parse()
  - Don't hand-roll: JSON parsing, retry logic, auth headers
- User configured Anthropic API key in .env file
- Created Phase 2 plans with /gsd:plan-phase 2:
  - Plan 02-01: Core AI Service (Pydantic schemas + FlashcardGenerator)
  - Plan 02-02: Error Handling & Database Integration (retry logic + persistence)
- Completed 02-01-PLAN.md (Core AI Service):
  - Created Pydantic schema models (FlashcardPair, FlashcardSet)
  - Implemented FlashcardGenerator service with Claude Sonnet 4.5
  - Used structured outputs with output_format parameter
  - Educational prompt engineering for active recall questions
  - Test script demonstrates service functionality
- Completed 02-02-PLAN.md (Error Handling & Database Integration):
  - Implemented exponential backoff retry logic with jitter
  - Honors retry-after header for 429 rate limit errors
  - Categorized error handling (retry 429/529, fail fast 400/401)
  - Database integration: save_to_database() and generate_and_save()
  - Foreign key linking between decks and flashcards
  - **Phase 2 complete:** AI service is production-ready
- Created Phase 3 plans with /gsd:plan-phase 3:
  - Plan 03-01: Base Templates & Homepage (Tailwind + form)
  - Plan 03-02: Flashcard Generation & Preview (AI integration + card list)
  - Plan 03-03: Modal Card Editor (modal popup + edit endpoint)

## Key Decisions

| Decision | Rationale | Date |
|----------|-----------|------|
| Flask over Django/FastAPI | Lightweight, easier for student to learn, less boilerplate | 2026-01-14 |
| Tailwind CSS over custom CSS | Modern utility-first approach, faster development | 2026-01-14 |
| SQLite over PostgreSQL | No server setup needed, perfect for local-first app | 2026-01-14 |
| Simple re-queue algorithm | Easy to understand, good enough for v1 | 2026-01-14 |
| Interactive mode | Student wants to understand each step | 2026-01-14 |
| Modal edit UI | Cleaner separation between preview and edit modes | 2026-01-14 |
| JSON export format | Structured data, supports metadata, standard for web apps | 2026-01-14 |
| Full statistics tracking | Cards studied, success rate, last studied, study streak | 2026-01-14 |
| src/ directory structure | Better code organization following Flask conventions | 2026-01-14 |
| Minimum version specs | Ensure compatibility (Flask>=3.0.0, python-dotenv>=1.0.0, anthropic>=0.18.0) | 2026-01-14 |
| Raw SQL with sqlite3 (no ORM) | Simplicity and educational value for student learning | 2026-01-14 |
| Dict-based model returns | Easy JSON serialization without additional mapping layers | 2026-01-14 |
| Unix timestamps (REAL) | Cross-platform compatibility for temporal fields | 2026-01-14 |
| Foreign key CASCADE delete | Ensure data integrity when decks are removed | 2026-01-14 |
| python-dotenv for config | Industry standard, simple for students to understand | 2026-01-14 |
| Auto-initialize database on app startup | Zero-config experience, tables created automatically | 2026-01-14 |
| Run Flask from project root with src/ imports | Proper Python package structure | 2026-01-14 |
| Anthropic structured outputs | 100% schema compliance, no hand-rolled JSON parsing | 2026-01-14 |
| Claude Sonnet 4.5 model | Balance of quality and cost for flashcard generation | 2026-01-14 |
| Exponential backoff with jitter | Resilient retry logic for 429/529 API errors | 2026-01-14 |
| Pydantic for schema definition | Type-safe API responses, automatic validation | 2026-01-14 |
| output_format parameter for structured outputs | SDK 0.76.0 uses output_format instead of response_model | 2026-01-14 |
| Max tokens 2048 for flashcard generation | Sufficient for 10 detailed Q&A pairs with explanations | 2026-01-14 |
| Educational prompt pattern | Emphasize understanding, avoid yes/no, require explanation | 2026-01-14 |
| Honor retry-after header | Server-guided retry timing optimizes API usage | 2026-01-14 |
| Fail fast for client errors | 400/401 errors need code fixes, not retries | 2026-01-14 |
| Convenience generate_and_save method | One-call workflow for common use case | 2026-01-14 |
| Tailwind CDN for styling | No build step, instant utilities, simple for student | 2026-01-14 |
| Jinja2 templates for views | Flask standard, student-friendly template syntax | 2026-01-14 |
| Modal for card editing | Cleaner UX, no page navigation, modern pattern | 2026-01-14 |
| Fetch API for AJAX updates | Modern JavaScript, updates without page reload | 2026-01-14 |
| Sequential wave execution | Plan 03-01 → 03-02 → 03-03 (UI builds on previous) | 2026-01-14 |
| Format timestamps in Python route | Simpler than custom Jinja2 filters for students | 2026-01-15 |
| Navigation link in header | Global access to decks from any page, modern UX pattern | 2026-01-15 |

## Active Context

**User Profile:**
- Student learning Flask + Tailwind + SQLite + Anthropic API
- Prefers step-by-step explanations
- Wants to understand code as it's written

**Technical Constraints:**
- Local-first (no cloud deployment required)
- User needs to obtain Anthropic API key
- 10 flashcards per topic (default)

**Codebase State:**
- Flask project structure with src/ directory layout
- Core dependencies installed: Flask, python-dotenv, anthropic, pydantic
- .gitignore configured for Python/Flask
- SQLite database with decks and flashcards tables
- Database models with CRUD operations (Deck, Flashcard)
- Statistics tracking ready (studied_count, success_count, last_studied, streak)
- Configuration module with environment variable management (src/config.py)
- Flask app initializes database automatically on startup
- Environment template (.env.example) with API key instructions
- Comprehensive setup documentation (README.md)
- Anthropic API key configured in .env file
- Phase 2 research complete (02-RESEARCH.md with structured outputs architecture)
- Pydantic schemas for AI responses (FlashcardPair, FlashcardSet)
- FlashcardGenerator service with Claude Sonnet 4.5 integration
- Structured outputs guarantee schema compliance
- Exponential backoff retry logic with jitter and rate limit header support
- Database integration with save_to_database() and generate_and_save() methods
- Base HTML template with Tailwind CSS CDN (src/templates/base.html)
- Homepage template with flashcard generation form (src/templates/index.html)
- Blueprint pattern for routes (src/routes/main.py registered in app.py)
- Form configured to POST to /generate endpoint (will be created in 03-02)
- Git repo with 28+ commits (foundation + database + config + planning + AI service + templates + routes + generation + preview + editor + deck selection)
- Full UI stack working: homepage form → AI generation → card preview → modal editor
- Deck selection page showing all decks with card counts
- My Decks navigation link in header visible on all pages
- Preview page with "Start Studying" button linking to study mode

## Next Steps

1. **Plan 04-01 Complete ✅** - Deck Selection Page functional
2. **Next Plan:** 04-02 - Study Mode Interface
   - Interactive study session with one card at a time
   - Show question → user thinks → reveal answer → self-grade
   - Track statistics (studied_count, success_count, last_studied, streak)
   - Session end summary with performance stats
3. **Recommended command:** `/gsd:execute-plan .planning/phases/04-study-mode-ui/04-02-PLAN.md` to implement study mode

---

*State initialized: 2026-01-14*
*Last updated: 2026-01-14*
