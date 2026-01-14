# Codebase Structure

**Analysis Date:** 2026-01-14

## Directory Layout

```
Expanza_Gary_Test/
├── main.py              # Empty entry point (0 bytes)
├── test.py              # Test file (1 line: print statement)
├── .claude/             # Claude Code configuration
│   └── settings.local.json
├── .planning/           # GSD planning directory
│   └── codebase/        # Codebase analysis documents
├── .venv/               # Python virtual environment
└── .git/                # Git repository (no commits yet)
```

## Directory Purposes

**Project Root:**
- Purpose: Contains minimal Python source files
- Contains: `main.py` (empty), `test.py` (print statement)
- Key files: Currently minimal placeholder files
- Subdirectories: .claude/, .planning/, .venv/, .git/

**.claude/**
- Purpose: Claude Code CLI configuration
- Contains: Local settings and permissions
- Key files: `settings.local.json` (configured for GSD workflow)
- Subdirectories: None

**.planning/**
- Purpose: GSD (Get Shit Done) planning directory
- Contains: Codebase analysis documents
- Key files: None yet (codebase/ directory empty before this mapping)
- Subdirectories: codebase/ (for stack, architecture, etc.)

**.venv/**
- Purpose: Python virtual environment
- Contains: Python 3.12.0 environment, pip 25.3
- Key files: `pyvenv.cfg`, Python binaries
- Subdirectories: bin/, lib/, include/

**.git/**
- Purpose: Git version control
- Contains: Repository metadata (no commits yet)
- Key files: Git configuration
- Subdirectories: Standard git structure

## Key File Locations

**Entry Points:**
- `main.py` - Intended primary entry point (currently empty)
- `test.py` - Test/utility file (single print statement)

**Configuration:**
- `.claude/settings.local.json` - Claude Code permissions and settings
- `.venv/pyvenv.cfg` - Python virtual environment configuration

**Core Logic:**
- Not applicable - No application logic implemented yet

**Testing:**
- `test.py` - Not a proper test file (just contains print statement)

**Documentation:**
- Not detected - No README, CONTRIBUTING, or documentation files

## Naming Conventions

**Files:**
- snake_case: `main.py`, `test.py`
- No other patterns established due to minimal codebase

**Directories:**
- Dot-prefixed for hidden/config: `.claude`, `.planning`, `.venv`, `.git`
- No application directories yet

**Special Patterns:**
- Virtual environment excluded from version control (should be in .gitignore)
- Planning directory follows GSD conventions

## Where to Add New Code

**New Feature:**
- Primary code: Create proper directory structure (e.g., `src/` or `app/`)
- Tests: Create `tests/` directory with proper test framework
- Config: Add `pyproject.toml` or `setup.cfg`

**New Module:**
- Implementation: Establish package structure first
- Types: Add type hints to modules
- Tests: Co-locate or separate in `tests/`

**New CLI Command:**
- Not applicable yet - No CLI framework established

**Utilities:**
- Create `utils/` or `lib/` directory when needed

## Special Directories

**.venv/**
- Purpose: Python virtual environment
- Source: Created via `python -m venv .venv`
- Committed: No - should be in .gitignore (currently not present)

**.planning/**
- Purpose: GSD workflow planning and context
- Source: Created by GSD commands
- Committed: Yes - contains project planning documents

**.claude/**
- Purpose: Claude Code CLI settings
- Source: Created by Claude Code
- Committed: Optional - contains local permissions

---

*Structure analysis: 2026-01-14*
*Update when directory structure changes*
