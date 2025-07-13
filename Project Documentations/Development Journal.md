## 2025-06-09 – Dev Log #1: Project Foundation

### Progress
- Created core project documents:
  - `Project Vision`: defined users, value, and philosophy
  - `MVP Scope`: feature priorities using MoSCoW
  - `Success Metrics & Timeline`: 10-week Gantt chart
  - `Tech Stack Decision`: finalized core technologies

### Insight
- Good planning clarified MVP boundaries and reduced ambiguity.

### Next Steps
- Finalize tech stack
- Scaffold initial project structure

## 2025-06-10 – Dev Log #2: Project Setup

### Progress
- Set up Python virtual environment and installed FastAPI, SQLModel, Uvicorn
- Initialized Node environment with Tailwind CSS, PostCSS, Autoprefixer
- Verified HTMX + Tailwind rendering at `http://127.0.0.1:8000`
- Added `.gitignore` and committed clean project skeleton

### Learnings
- HTMX simplifies dynamic interfaces without full SPA overhead
- Frontend build artifacts should remain isolated from Python logic

### Questions
- What is the long-term role of the virtual environment?
- How should the folder structure be organized?

### Next Steps
- Define `Entry` model in `models.py`
- Integrate Alembic and create initial migration
- Build `POST /api/entry` endpoint with HTMX form
- Add `requirements.txt` and NPM scripts
- Improve folder layout and module separation

### Reflection
- Development felt too passive; aim for deeper understanding moving forward

## 2025-07-12 (11pm) to 2025-07-13 (1am) – Dev Log #3: Claude Code Integration & UX Refinement

### Progress
- Switched coding partner from ChatGPT to Claude Code 
- Fixed runtime bugs (missing `date`, template path errors, missing dependencies)
- Completed 11-field `Entry` form with optional fields and form validation
- Updated schema to support nullable fields with SQLModel
- Removed non-English text and standardized language for international use

### UX Refinement
- Made fields 2 and 3 optional in each section to reduce user pressure
- Added visual indicators for required vs optional fields
- Reworded field labels for softer, more approachable tone

### Technical Learnings
- Google Chrome actually has a terminal for debugging in F12

### Current Status
- Refined UX and complete documentation

### Next Steps
- ==Re-plan all existing projects – including timeline, scope, and priorities==
- More testing and improvement on existing UI and functionalities
- Introducing User authentication

### Reflection
Today marks a major shift in my development workflow — I've started using Claude Code as my primary coding partner instead of ChatGPT. The experience is remarkably powerful. I believe this could be a turning point.

It's prompted me to reassess my role as a human developer. Rather than focusing solely on improving traditional programming skills, I now feel a stronger urge to master how to collaborate effectively with AI agents.

## 2025-07-13 (continued) – Database Schema Learning

### Key Learning: Database Schema Changes
**Problem Encountered**: After making fields 2 & 3 optional in each category (success, gratitude, anxiety), the application crashed on form submission.

**Root Cause**: SQLite database schema mismatch - existing `db.sqlite3` still expected all fields to be required, but updated `models.py` defined them as optional (`Optional[str] = None`).

**Solution Applied**: 
1. Stop application (Ctrl+C)
2. Delete database file: `del db.sqlite3` 
3. Restart application - database recreated with new schema

**Critical Insight**: In SQLModel/SQLAlchemy, changing field nullability requires database recreation in development. The existing database structure conflicts with model changes.

### Documentation Created
- **New file**: `Project Documentations/Developer Manual.md`
- **Purpose**: Centralized troubleshooting guide and development procedures
- **Key sections**: Quick start, database management, schema change procedures

### Developer Workflow Established
- Always activate venv first: `venv\Scripts\activate`
- For schema changes: Delete `db.sqlite3` and restart
- Document learnings in Development Journal
- Use Developer Manual for procedures and troubleshooting

**Next Priority**: Test current application state and plan next features.

## 2025-07-13 (9:30am-11:00am) – Dev Log #4: Authentication System & Production-Ready Scripts

### Session Overview
**Duration**: 1.5 hours intensive development session
**Focus**: Complete authentication implementation + professional automation scripts
**Breakthrough**: Successfully debugged complex authentication setup and created production-quality tooling

### Major Achievements

#### 🔐 **Complete Authentication System**
- **FastAPI-Users integration**: Full email registration with verification flow
- **Mailtrap configuration**: Email testing environment successfully configured  
- **Mixed database architecture**: Solved complex async/sync session handling (async for users, sync for entries)
- **Beautiful UI**: Tailwind CSS login/register templates with proper form handling
- **Debugging marathon**: Resolved 6+ complex import/session/configuration errors

#### 🛠️ **Production-Quality Automation Scripts**
- **Complete script suite**: `dev-start.bat`, `quick-start.bat`, `reset-db.bat`, `install-deps.bat`
- **Professional Windows batch practices**: setlocal/endlocal, proper error codes, environment isolation
- **Smart error detection**: Database file locking detection, dependency checking, directory validation
- **User-friendly design**: Flexible input parsing (y/yes/n/no), clear error messages, confirmation prompts
- **Organized structure**: Dedicated `scripts/` folder with comprehensive README documentation

#### 🔧 **Problem-Solving Highlights** 
- **Database session compatibility**: Solved FastAPI-Users async session requirements vs SQLModel sync sessions
- **Batch file debugging**: Identified and fixed Windows case-sensitivity and logic flow issues
- **Dependency management**: Resolved missing aiosqlite causing authentication startup failures
- **Script reliability**: Implemented robust file existence checking and error handling

### Technical Architecture Decisions
- **User model**: Pure SQLAlchemy with FastAPI-Users base class (avoids SQLModel conflicts)
- **Entry model**: SQLModel for familiar syntax and easier development
- **Database sessions**: Dual session approach - async for auth, sync for business logic
- **Email testing**: Mailtrap for development, easily switchable to production SMTP

### Development Workflow Improvements
- **Automated setup**: Single command (`dev-start.bat`) handles entire development environment
- **Database management**: Safe reset procedures with confirmation and error detection
- **Documentation**: Comprehensive guides in Developer Manual and script README files
- **Error resilience**: Scripts handle common failure scenarios gracefully

### Next Session Goals
- **End-to-end authentication testing**: Complete registration → verification → login flow
- **User-specific data**: Ensure diary entries properly tied to authenticated users
- **Production readiness**: Additional OAuth providers (Google, GitHub)