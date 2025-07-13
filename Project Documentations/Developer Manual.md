# Developer Manual – SuccessDiary

## Table of Contents
1. [Quick Start](#quick-start)
2. [Development Workflow](#development-workflow)
3. [Database Management](#database-management)
4. [Troubleshooting](#troubleshooting)
5. [Common Issues & Solutions](#common-issues--solutions)

---

## Quick Start

### 🚀 **Automated Scripts (Recommended)**

**Full Development Setup:**
```bash
# Double-click or run in Command Prompt:
scripts\dev-start.bat
```
*This script: activates venv → installs dependencies → resets database → starts server*

**Quick Start (No DB Reset):**
```bash
scripts\quick-start.bat
```
*This script: activates venv → starts server*

**Other Useful Scripts:**
```bash
scripts\reset-db.bat        # Reset database only
scripts\install-deps.bat    # Install/update dependencies only
```

**📁 Note:** All automation scripts are located in the `scripts/` folder to keep the project root clean.

### 📋 **Manual Commands (Alternative)**

**Initial Setup:**
```bash
# Navigate to project
cd "C:\Users\Yuting\Projects\success-diary"

# Activate virtual environment
venv\Scripts\activate

# Install/update dependencies (if needed)
pip install -r requirements.txt

# Start development server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Daily Development:**
```bash
# 1. Activate environment
venv\Scripts\activate

# 2. Start server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 3. Open browser
# Visit: http://localhost:8000
```

---

## Development Workflow

### 🎯 **Recommended Daily Workflow**
1. **Start development**: Run `scripts\dev-start.bat` (full setup) or `scripts\quick-start.bat` (quick start)
2. **Make code changes**: Edit files as needed
3. **Test changes**: Server auto-reloads on file changes
4. **Database schema changes**: If you modify `models.py`, run `scripts\reset-db.bat` then restart server

### 🔧 **Manual Workflow (Alternative)**
1. **Always activate virtual environment first**: `venv\Scripts\activate`
2. **Test changes locally**: Start server and verify functionality
3. **Check for database schema changes**: If you modify `models.py`, see [Database Management](#database-management)

### ✅ **Before Committing**
- [ ] Test application starts without errors
- [ ] Verify all features work as expected
- [ ] Check database compatibility (if schema changed)

---

## Database Management

### Database Location
- **File**: `db.sqlite3` (in project root)
- **Auto-created**: On first application startup
- **Models**: Defined in `app/models.py`

### Schema Changes (IMPORTANT!)

**When you modify `app/models.py` (database schema):**

1. **Stop the application** (Ctrl+C)
2. **Delete the database file**: `del db.sqlite3` (Windows) or `rm db.sqlite3` (Mac/Linux)
3. **Restart the application**: `uvicorn app.main:app --reload --host 0.0.0.0 --port 8000`
4. **Database will be recreated** with the new schema

**⚠️ WARNING**: Deleting `db.sqlite3` will lose all existing data!

### Schema Change Example
```python
# Before - in app/models.py
class Entry(SQLModel, table=True):
    success_1: str
    success_2: str  # Required field

# After - making field optional
class Entry(SQLModel, table=True):
    success_1: str
    success_2: Optional[str] = None  # Now optional

# Action needed: Run scripts\reset-db.bat and restart server
```

## Automation Scripts

### 📁 **Available Scripts** (Located in `scripts/` folder)
- **`scripts\dev-start.bat`**: Complete development setup (recommended for daily use)
- **`scripts\quick-start.bat`**: Quick server start (when no DB changes)
- **`scripts\reset-db.bat`**: Reset database only (with smart error handling)
- **`scripts\install-deps.bat`**: Install/update dependencies only

### 🛠️ **Script Features**
- **Error checking**: Verifies project directory and virtual environment
- **Dependency management**: Auto-installs/updates requirements
- **Database handling**: Safe database reset with confirmation
- **Smart error detection**: Detects if database is locked by running server
- **Flexible input**: Accepts y/yes/n/no in any case combination
- **Clear output**: Shows progress and helpful information
- **Robust operation**: Handles common errors gracefully
- **Professional design**: Environment isolation and proper error codes

---

## Troubleshooting

### Application Won't Start

**Error**: `ImportError` or missing modules
```bash
# Quick solution: Run scripts\install-deps.bat
# Or manual: pip install -r requirements.txt
```

**Error**: Port already in use
```bash
# Kill existing process then restart
# Or change port: uvicorn app.main:app --reload --host 0.0.0.0 --port 8001
```

### Database Issues

**Error**: Database schema mismatch
```bash
# Quick solution: Run scripts\reset-db.bat then scripts\quick-start.bat
# Or manual: del db.sqlite3 then restart application
```

**Error**: Application crashes after form submission
- **Likely cause**: Schema mismatch between models and database
- **Quick solution**: Run `scripts\reset-db.bat` and restart server
- **Manual solution**: Delete `db.sqlite3` and restart application

### Frontend Issues

**Error**: CSS not loading/updating
```bash
# Solution: Rebuild CSS
npm run build  # (when build script is added)
```

---

## Common Issues & Solutions

### Issue 1: Database Schema Changes Breaking Application

**Problem**: After making fields optional in `models.py`, application crashes on form submission

**Root Cause**: Existing database schema doesn't match updated model definitions

**Solution**: 
1. Stop application (Ctrl+C)
2. Delete database: `del db.sqlite3`
3. Restart application: Database recreated with new schema

**Prevention**: Always test schema changes in development before deploying

### Issue 2: Virtual Environment Not Activated

**Problem**: `ModuleNotFoundError` when starting application

**Symptoms**: 
- Missing FastAPI, uvicorn, or other dependencies
- Python can't find project modules

**Solution**: Always activate virtual environment first
```bash
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux
```

### Issue 3: Template Not Found Errors

**Problem**: Application can't find HTML templates

**Root Cause**: Template directory path mismatch

**Current Setup**: Templates are in `/templates/` (project root), not `/app/templates/`

**Fix**: Verify `main.py` template configuration:
```python
templates = Jinja2Templates(directory=Path(__file__).parent.parent / "templates")
```

---

## Development Notes

### Project Structure Understanding
- **Backend**: `app/` directory (FastAPI application)
- **Frontend**: `templates/` directory (HTML templates)
- **Styling**: Tailwind CSS via PostCSS
- **Database**: SQLite file `db.sqlite3`

### Key Files
- `app/main.py`: FastAPI application and routes
- `app/models.py`: Database models (SQLModel)
- `app/database.py`: Database configuration
- `templates/index.html`: Main application template
- `requirements.txt`: Python dependencies
- `package.json`: Node.js dependencies for CSS processing

### Development Philosophy
- **Human-centered design**: Optional fields reduce user pressure
- **Structured flexibility**: Users define what they track
- **Data integrity**: All records exportable for long-term use

---

## Maintenance Commands

```bash
# View current dependencies
pip list

# Update specific package
pip install --upgrade package_name

# Freeze current environment
pip freeze > requirements.txt

# Database inspection (if needed)
sqlite3 db.sqlite3
.tables
.schema entries
.quit
```

---

*Last updated: 2025-07-13*
*For questions or issues, refer to Development Journal.md or create new log entries*