# Success-Diary Project

## Project Overview
A web application for tracking daily successes and achievements.

## Tech Stack
- Backend: Python (FastAPI/Flask)
- Frontend: HTML templates with Tailwind CSS
- Database: SQLite (db.sqlite3)
- Styling: Tailwind CSS with PostCSS

## Development Commands

### Setup
- Create virtual environment: `python -m venv venv`
- Activate virtual environment: `venv\Scripts\activate` (Windows) or `source venv/bin/activate` (Mac/Linux)
- Install Python dependencies: `pip install -r requirements.txt`
- Install Node dependencies: `npm install`

### Running the Application
- Start development server: `uvicorn app.main:app --reload --host 0.0.0.0 --port 8000`
- Build CSS (if needed): `npm run build` (when you add npm scripts)

### Database
- Database file: `db.sqlite3` (auto-created on first run)
- Models are in: `app/models.py`

### Testing & Quality
- Run tests: `pytest` (when tests are added)
- Lint: `flake8 app/`
- Type check: `mypy app/`

## Project Structure
- `app/` - Python application code
- `templates/` - HTML templates
- `static/css/` - CSS files
- `Project Documentations/` - Project documentation and planning
- `db.sqlite3` - SQLite database

## Current Status
✅ **Working MVP Completed (as of 2025-07-13)**
- Full 11-field daily entry form (3 successes, 3 gratitudes, 3 worries, 1 rating)
- Human-centered UX with optional fields (only first field required in each category)
- Beautiful emoji bullet display (✨🙏💭) for entries
- SQLite database with proper nullable field support
- Responsive Tailwind CSS styling
- Form validation and error handling

## Key Features Implemented
- **Daily Entry Form**: Complete with encouraging placeholders and visual cues
- **Entry Display**: Clean emoji-based bullet format for readability
- **Optional Fields**: Fields 2 & 3 in each category are optional to reduce user pressure
- **Database**: Auto-created SQLite with Entry model supporting null values

## Important Implementation Details
- **Database Reset**: If you change the schema, delete `db.sqlite3` to recreate with new structure
- **Template Location**: Templates are in project root `/templates/`, not `/app/templates/`
- **Form Handling**: Uses standard HTML forms (not HTMX) for simplicity
- **Field Requirements**: success_1, gratitude_1, anxiety_1, and score are required; others optional

## Next Priority Features
1. User authentication system (FastAPI Users)
2. Duplicate entry prevention (one entry per day per user)
3. Daily highlight feature (show random past positive entry)
4. Data export functionality (JSON/CSV)
5. Edit/delete functionality for historical entries

## Notes
- Project uses human-centered design principles
- All text is in English for international contributors
- Focus on encouraging reflection rather than demanding perfection