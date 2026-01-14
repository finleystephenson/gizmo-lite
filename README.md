# AI Flashcard Generator

An intelligent flashcard application that uses AI to generate study materials from any topic. Perfect for students who want to learn efficiently using spaced repetition and AI-powered content generation.

## Features

- **AI-Powered Generation**: Create flashcards automatically from any topic using Claude AI
- **Study Mode**: Practice with flashcards and track your progress
- **Spaced Repetition**: Smart algorithm helps you focus on cards you need to review
- **Statistics Tracking**: Monitor your study streaks and success rates
- **Deck Management**: Organize flashcards by topic
- **Export/Import**: Share decks with others in JSON format

## Requirements

- Python 3.12 or higher
- Anthropic API key (for AI features)

## Setup Instructions

Follow these steps to get the application running on your computer:

### 1. Clone or Download the Project

If you haven't already, get the project files on your computer.

### 2. Create a Virtual Environment

A virtual environment keeps this project's dependencies separate from other Python projects.

```bash
# Create virtual environment
python3 -m venv .venv

# Activate virtual environment
# On macOS/Linux:
source .venv/bin/activate

# On Windows:
.venv\Scripts\activate
```

**Tip**: You should see `(.venv)` at the start of your terminal prompt when activated.

### 3. Install Dependencies

Install all required Python packages:

```bash
pip install -r requirements.txt
```

This installs:
- Flask (web framework)
- python-dotenv (environment variable management)
- anthropic (Claude AI API client)

### 4. Set Up Environment Variables

Environment variables store sensitive information like API keys.

```bash
# Copy the template file
cp .env.example .env
```

Then edit the `.env` file and add your Anthropic API key (see next step).

### 5. Get Your Anthropic API Key

To use the AI flashcard generation feature, you need an API key:

1. Go to [https://console.anthropic.com/settings/keys](https://console.anthropic.com/settings/keys)
2. Sign up or log in to your Anthropic account
3. Click "Create Key" to generate a new API key
4. Copy the key
5. Open the `.env` file in your project
6. Replace `your_api_key_here` with your actual API key

**Important**: Never share your API key or commit the `.env` file to git!

### 6. Run the Application

Start the Flask development server:

```bash
# Make sure your virtual environment is activated first!
python3 src/app.py
```

You should see:
```
 * Running on http://127.0.0.1:5000
```

### 7. Open in Browser

Visit [http://localhost:5000](http://localhost:5000) in your web browser.

## Project Structure

```
ai-flashcard-generator/
├── src/
│   ├── app.py              # Flask application entry point
│   ├── config.py           # Configuration and environment variables
│   ├── models/
│   │   ├── database.py     # Database connection and initialization
│   │   ├── deck.py         # Deck model (CRUD operations)
│   │   └── flashcard.py    # Flashcard model (CRUD operations)
│   └── routes/
│       └── __init__.py     # API routes (to be implemented)
├── .env                    # Environment variables (DO NOT COMMIT)
├── .env.example            # Environment variable template
├── flashcards.db           # SQLite database (created automatically)
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## Development Guide

### Database

The application uses SQLite, a lightweight database that stores data in a single file (`flashcards.db`). The database is automatically created when you first run the app.

**Tables**:
- `decks`: Stores flashcard decks (topic-based organization)
- `flashcards`: Stores individual flashcards with questions, answers, and study statistics

### Making Changes

When you make changes to the code:
1. Save your file
2. Flask auto-reloads in debug mode (you don't need to restart the server)
3. Refresh your browser to see changes

### Common Issues

**"ModuleNotFoundError"**: Make sure your virtual environment is activated:
```bash
source .venv/bin/activate  # macOS/Linux
```

**"Permission denied" on database**: The app needs write access to create `flashcards.db` in the project directory.

**Port 5000 already in use**: Another application is using port 5000. Stop it, or change the port in `app.py`:
```python
app.run(debug=True, port=5001)
```

## Learning Resources

- **Flask Documentation**: [https://flask.palletsprojects.com/](https://flask.palletsprojects.com/)
- **Tailwind CSS**: [https://tailwindcss.com/docs](https://tailwindcss.com/docs)
- **SQLite**: [https://www.sqlite.org/docs.html](https://www.sqlite.org/docs.html)
- **Anthropic API**: [https://docs.anthropic.com/](https://docs.anthropic.com/)

## Next Steps

This is a learning project! Here's what you can do:

1. **Explore the code**: Open files in `src/` and read the comments
2. **Experiment**: Try modifying the homepage message in `src/app.py`
3. **Learn the database**: Run Python commands to query the database
4. **Stay tuned**: More features coming in upcoming phases!

## License

This is a personal learning project. Feel free to modify and experiment!
