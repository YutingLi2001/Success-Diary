# Success-Diary Project

## Project Overview
A privacy-focused web application for tracking daily successes and achievements through structured emotional reflection. Designed for personal growth enthusiasts aged 20-35 who want to build positive mental health habits.

## Current Development Status
**Phase: MVP 1.0 Development** (Core Features)

### ✅ Completed Features
- User authentication system with email verification (FastAPI-Users + Mailpit)
- Daily entry form (11 fields: successes, gratitude, anxiety, overall rating, free-form journal)
- Basic entry viewing and history display
- Cross-platform development automation scripts (Windows/Mac)
- Comprehensive project planning and requirements documentation

### ⏳ Remaining MVP 1.0 Features
- Entry editing functionality for historical entries
- Entry titles with custom/auto-generated options
- Dynamic UI with progressive field display
- Enhanced form validation and error handling
- Mobile responsive design optimization

### 📋 Future Phases
- **V2.0**: Health tracking modules (diet, exercise, sleep, productivity)
- **V3.0+**: Advanced analytics, custom fields, data export, API access, OAuth integration
- **Production**: AWS deployment with PostgreSQL

## Tech Stack
- **Backend**: FastAPI 0.110.1 with SQLModel ORM
- **Frontend**: Jinja2 templates with Tailwind CSS v3.4
- **Database**: SQLite (development) → PostgreSQL (production)
- **Authentication**: FastAPI-Users 14.0.1 with email verification
- **Email**: Mailpit (development) → Production SMTP (deployment)
- **Enhancement**: HTMX for dynamic interactions
- **Deployment**: AWS EC2/ECS + RDS (planned)

## Development Commands

### 🚀 Quick Start (Automated - Recommended)

**Windows:**
```cmd
scripts\windows\dev-start-with-email.bat    # Full setup with email server
scripts\windows\quick-start.bat             # FastAPI only
scripts\windows\reset-db.bat                # Database reset only
scripts\windows\install-deps.bat            # Dependencies only
```

**Mac/Linux:**
```bash
./scripts/mac/dev-start-with-email.sh       # Full setup with email server
./scripts/mac/quick-start.sh                # FastAPI only
./scripts/mac/reset-db.sh                   # Database reset only
./scripts/mac/install-deps.sh               # Dependencies only
```

**Servers:**
- **Application**: http://localhost:8000
- **Email Testing**: http://localhost:8025 (Mailpit interface)

### 📋 Manual Setup (Alternative)

**Initial Setup:**
```bash
# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate                        # Windows
source venv/bin/activate                     # Mac/Linux

# Install dependencies
pip install -r requirements.txt
npm install

# Start email server (separate terminal)
mailpit

# Start development server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Database Management
- **File**: `db.sqlite3` (auto-created)
- **Models**: `app/models.py`
- **Schema Changes**: Delete `db.sqlite3` and restart server
- **Reset**: Use platform-specific reset scripts

### Testing & Quality
- **Lint**: `flake8 app/`
- **Type Check**: `mypy app/`
- **Tests**: `pytest` (when implemented)

## AI Collaboration Workflow

### Prompt System
This project uses a template-driven approach for efficient Claude Code collaboration:

**Available Prompts:**
- `prompts/update-development-journal.md` - For concise dev log entries

**Usage:**
```
"Read the prompt in prompts/update-development-journal.md and update the journal for today's 2-hour OAuth integration session where we completed Google provider setup."
```

### Development Methodology
**"Planning Then Go" Approach:**
- Comprehensive upfront planning before implementation
- Detailed requirements documentation drives development
- Reduces rework by ~80% through thorough AI collaboration planning
- Template-driven workflows for consistent outcomes

## Project Structure

```
Success-Diary/
├── app/                         # FastAPI application
│   ├── main.py                 # Routes and endpoints
│   ├── auth.py                 # Authentication logic
│   ├── models.py               # Database models (User, Entry)
│   └── database.py             # Database configuration
├── templates/                   # Jinja2 HTML templates
│   ├── dashboard.html          # Main entry form
│   ├── entries.html            # History display
│   ├── analytics.html          # Future analytics
│   ├── settings.html           # User preferences
│   └── auth/                   # Authentication pages
├── scripts/                     # Development automation
│   ├── mac/                    # macOS/Linux scripts
│   └── windows/                # Windows batch files
├── docs/                        # Comprehensive documentation
│   ├── logs/                   # Development tracking
│   │   ├── development-journal.md
│   │   └── development-notes.md
│   ├── operations/             # Development procedures
│   │   └── developer-manual.md
│   ├── requirements/           # Project specifications
│   │   ├── core-functionality-overview.md
│   │   ├── development-requirements.md
│   │   ├── product-overview.md
│   │   └── project-scope.md
│   └── project-timeline.md
├── prompts/                     # AI collaboration templates
│   └── update-development-journal.md
├── config/                      # Configuration files
├── data/                        # Data storage and backups
├── src/                         # Alternative source structure
├── tests/                       # Test files (future)
├── tools/                       # Development utilities
├── venv/                        # Python virtual environment
├── db.sqlite3                   # SQLite database (auto-created)
├── requirements.txt             # Python dependencies
├── package.json                 # Node.js dependencies
└── .env                         # Environment variables
```

## Key Documentation

### 📋 Requirements & Planning
- **Product Overview**: `docs/requirements/product-overview.md`
- **Feature Roadmap**: `docs/requirements/core-functionality-overview.md`
- **Development Requirements**: `docs/requirements/development-requirements.md`
- **Timeline & Scope**: `docs/requirements/project-scope.md`

### 🏗️ Architecture Decisions
- **Architecture Decision Records**: `docs/adr/README.md`
- **Technical Decision History**: Immutable record of key architectural choices
- **Implementation Rationale**: Context and consequences of technical decisions

### 🛠️ Development Operations
- **Developer Manual**: `docs/operations/developer-manual.md`
- **Setup Guides**: Cross-platform installation and troubleshooting
- **Database Procedures**: Schema management and migration guides

### 📈 Progress Tracking
- **Development Journal**: `docs/logs/development-journal.md`
- **Development Notes**: `docs/logs/development-notes.md`
- **Project Timeline**: `docs/project-timeline.md`

## Development Workflow

### 🎯 Daily Development Process
1. **Planning Review**: Check `docs/requirements/` for current objectives
2. **Architecture Review**: Consult `docs/adr/` for technical decision context
3. **Start Environment**: Run platform-specific dev-start script
4. **Track Progress**: Use prompt templates for consistent documentation
5. **Schema Changes**: Reset database if modifying `app/models.py`
6. **Update Logs**: Document sessions using `prompts/update-development-journal.md`

### 🔄 "Planning Then Go" Methodology
1. **Requirements Phase**: Comprehensive planning before implementation
2. **Specification Documentation**: Detailed requirements capture in `docs/requirements/`
3. **Architecture Decision Records**: Document key technical choices in `docs/adr/`
4. **Template-Driven Execution**: Use prompt system for consistent AI collaboration
5. **Progress Tracking**: Regular journal updates with concise, human-focused content

## Technical Implementation

### Authentication Architecture
- **FastAPI-Users**: Modular user management system
- **Email Verification**: 6-digit codes with 10-minute expiration
- **Session Management**: JWT-based with secure cookies
- **Database**: Mixed async (auth) and sync (business logic) sessions

### Database Strategy
- **Development**: SQLite for rapid prototyping and single-user testing
- **Production**: PostgreSQL RDS for scalability and multi-user support
- **Migration**: Documented transition plan for post-Calgary deployment

### UI/UX Philosophy
- **Human-Centered Design**: Optional fields reduce user pressure
- **Structured Flexibility**: Users define what they track while maintaining consistency
- **Encouraging Experience**: Supportive language and visual cues guide reflection

## Production Deployment Plan

### Production Deployment Phase
- **Platform**: AWS EC2/ECS with PostgreSQL RDS
- **Domain**: Custom domain with Route 53 and SSL via CloudFront
- **Timeline**: Production launch target August 17, 2025

### Success Metrics
- **Active Users**: >10 users creating ≥1 entry by 4 weeks post-launch
- **User Retention**: >30 days average entries per user within first 45 days
- **System Stability**: <1% error rate in production
- **Self-Adoption**: ≥50 consecutive days of founder usage

## Important Notes

### For Claude Code Users
- **All scripts must be run from project root directory**
- **Database schema changes require database reset (delete `db.sqlite3`)**
- **Use prompt templates for consistent AI collaboration workflows**
- **Refer to comprehensive documentation in `docs/` for detailed guidance**

### Development Priorities
1. **MVP 1.0**: Complete core features (editing, titles, dynamic UI, validation, mobile)
2. **Production Deployment**: AWS infrastructure and database migration
3. **Future Versions**: Health tracking (V2.0), advanced features (V3.0+)

---

**📚 For detailed information, see the comprehensive documentation in the `docs/` folder.**
**🤖 For AI collaboration, use templates in the `prompts/` folder.**
**⚡ For quick development setup, use automated scripts in the `scripts/` folder.**