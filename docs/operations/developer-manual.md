# Developer Manual – SuccessDiary

## Table of Contents
1. [Quick Start](#quick-start)
2. [Development Workflow](#development-workflow)
3. [Database Management](#database-management)
4. [Cross-Platform Setup](#cross-platform-setup)
5. [Troubleshooting](#troubleshooting)
6. [Common Issues & Solutions](#common-issues--solutions)

---

## Quick Start

### 🚀 **Automated Scripts (Recommended)**

**Windows - Full Development Setup:**
```bash
# Double-click or run in Command Prompt:
scripts\windows\dev-start.bat
```
*This script: activates venv → installs dependencies → resets database → starts server*

**Mac - Full Development Setup:**
```bash
# Run in Terminal:
./scripts/mac/dev-start.sh
```
*This script: activates venv → installs dependencies → resets database → starts server*

**Quick Start (No DB Reset):**
```bash
# Windows:
scripts\windows\quick-start.bat

# Mac:
./scripts/mac/quick-start.sh
```

**Other Useful Scripts:**
```bash
# Windows:
scripts\windows\reset-db.bat        # Reset database only
scripts\windows\install-deps.bat    # Install/update dependencies only

# Mac:
./scripts/mac/reset-db.sh           # Reset database only
./scripts/mac/install-deps.sh       # Install/update dependencies only
```

**📁 Note:** Scripts are organized by platform in `scripts/windows/` and `scripts/mac/` folders for cross-platform development.

---

## Development Workflow

### 🎯 **Recommended Daily Workflow**
1. **Planning Review**: Check `docs/requirements/` for current objectives
2. **Architecture Review**: Consult `docs/adr/` for technical decision context
3. **Start development**: Run platform-specific dev-start script (full setup) or quick-start script
4. **Make code changes**: Edit files as needed
5. **Test changes**: Server auto-reloads on file changes
6. **Database schema changes**: If you modify `models.py`, run reset-db script then restart server
7. **Document decisions**: Create ADRs for new architectural choices in `docs/adr/`

### 🔧 **Manual Workflow (Alternative)**
1. **Always activate virtual environment first**: Platform-specific activation command
2. **Test changes locally**: Start server and verify functionality
3. **Check for database schema changes**: If you modify `models.py`, see [Database Management](#database-management)

### ✅ **Before Committing**
- [ ] Test application starts without errors
- [ ] Verify all features work as expected
- [ ] Check database compatibility (if schema changed)
- [ ] Create ADRs for significant architectural decisions

### 📋 **Architecture Decision Records (ADRs)**

When making significant technical decisions, document them using the ADR system:

**ADR Creation Process:**
1. **Identify Decision**: Recognize when an architectural choice needs documentation
2. **Research Options**: Evaluate alternatives and their trade-offs
3. **Create ADR**: Use template in `docs/adr/template.md`
4. **Choose Category**: Place in appropriate folder:
   - `decisions/` - Core architectural decisions
   - `specifications/` - Technical implementation details
   - `business-decisions/` - Product/business strategy
5. **Update Index**: Add entry to `docs/adr/README.md`

**When to Create ADRs:**
- Database schema design decisions
- Authentication/authorization approaches
- Frontend framework or library choices
- API design patterns
- Performance optimization strategies
- Security implementation approaches
- Third-party service integrations

**ADR Benefits:**
- Future developers understand why decisions were made
- Prevents revisiting settled architectural questions
- Documents trade-offs and alternative approaches
- Maintains institutional knowledge as team evolves

---

## Database Management

### Database Location
- **File**: `db.sqlite3` (in project root)
- **Auto-created**: On first application startup
- **Models**: Defined in `app/models.py`

### Schema Changes (IMPORTANT!)

**When you modify `app/models.py` (database schema):**

1. **Stop the application** (Ctrl+C)
2. **Delete the database file**: 
   - Windows: `del db.sqlite3`
   - Mac/Linux: `rm db.sqlite3`
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

# Action needed: Run reset-db script and restart server
```

---

## Cross-Platform Setup

### 🖥️ **Mac Development Setup**

**Required Software Installation:**
```bash
# Install Homebrew (if not installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python 3.12+
brew install python@3.12

# Install Node.js (for Tailwind CSS)
brew install node

# Install Git (if not installed)
brew install git

# Install VS Code or preferred editor
brew install --cask visual-studio-code
```

**Project Setup on Mac:**
```bash
# Navigate to preferred directory
cd ~/Projects

# Clone the repository
git clone https://github.com/YutingLi2001/Success-Diary.git
cd Success-Diary

# Create virtual environment
python3 -m venv venv

# Activate virtual environment (Mac syntax)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install Node dependencies
npm install
```

### 🔄 **Cross-Platform Differences**

**File Paths:**
- **Windows**: `venv\Scripts\activate`
- **Mac**: `source venv/bin/activate`

**Script Extensions:**
- **Windows**: `.bat` files
- **Mac**: `.sh` files (with shebang)

**Command Differences:**
- **Windows**: `del filename`
- **Mac**: `rm filename`

---

## Troubleshooting

### Application Won't Start

**Error**: `ImportError` or missing modules
```bash
# Quick solution: Run install-deps script
# Windows: scripts\windows\install-deps.bat
# Mac: ./scripts/mac/install-deps.sh
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
# Quick solution: Run reset-db script then quick-start script
# Windows: scripts\windows\reset-db.bat then scripts\windows\quick-start.bat
# Mac: ./scripts/mac/reset-db.sh then ./scripts/mac/quick-start.sh
# Or manual: Delete db.sqlite3 then restart application
```

**Error**: Application crashes after form submission
- **Likely cause**: Schema mismatch between models and database
- **Quick solution**: Run platform-specific reset-db script and restart server
- **Manual solution**: Delete `db.sqlite3` and restart application

---

## Common Issues & Solutions

### Issue 1: Database Schema Changes Breaking Application

**Problem**: After making fields optional in `models.py`, application crashes on form submission

**Root Cause**: Existing database schema doesn't match updated model definitions

**Solution**: 
1. Stop application (Ctrl+C)
2. Delete database: `del db.sqlite3` (Windows) or `rm db.sqlite3` (Mac)
3. Restart application: Database recreated with new schema

**Prevention**: Always test schema changes in development before deploying

### Issue 2: Virtual Environment Not Activated

**Problem**: `ModuleNotFoundError` when starting application

**Symptoms**: 
- Missing FastAPI, uvicorn, or other dependencies
- Python can't find project modules

**Solution**: Always activate virtual environment first
```bash
# Windows:
venv\Scripts\activate

# Mac:
source venv/bin/activate
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

*Last updated: 2025-01-17*
*For questions or issues, refer to logs/development-journal.md or create new log entries*