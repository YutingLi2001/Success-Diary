# Project Structure Guide

## Overview
SuccessDiary follows professional software development best practices for project organization. This structure promotes maintainability, scalability, and clear separation of concerns.

## Directory Structure

```
Success-Diary/
├── 📁 src/                          # Source code (application logic)
│   ├── 📁 app/                      # Python application package
│   │   ├── __init__.py
│   │   ├── main.py                  # FastAPI entry point & routes
│   │   ├── 📁 core/                 # Core application logic
│   │   │   ├── __init__.py
│   │   │   ├── auth.py              # Authentication & user management
│   │   │   ├── database.py          # Database configuration & session
│   │   │   └── models.py            # SQLModel data models
│   │   ├── 📁 api/                  # API routes (future organization)
│   │   │   └── __init__.py
│   │   └── 📁 services/             # Business logic services (future)
│   │       └── __init__.py
│   └── 📁 static/                   # Static web assets
│       ├── 📁 css/
│       │   └── input.css            # Tailwind CSS input file
│       ├── 📁 js/                   # JavaScript files (future)
│       └── 📁 images/               # Image assets (future)
├── 📁 templates/                    # Jinja2 HTML templates
│   ├── 📁 auth/                     # Authentication templates
│   │   ├── login.html
│   │   ├── register.html
│   │   └── verify.html
│   ├── 📁 components/               # Reusable template components
│   ├── dashboard.html               # Main dashboard
│   ├── entries.html                 # Entries listing
│   ├── settings.html                # Settings page
│   └── *.html                       # Other template files
├── 📁 data/                         # Data storage (environment-separated)
│   ├── 📁 dev/
│   │   └── db.sqlite3               # Development database
│   ├── 📁 test/                     # Test data (future)
│   └── 📁 backups/                  # Database backups (future)
├── 📁 scripts/                      # Automation scripts
│   ├── 📁 dev/                      # Development scripts
│   │   ├── 📁 mac/                  # macOS development scripts
│   │   ├── 📁 windows/              # Windows development scripts
│   │   └── README.md                # Script documentation
│   └── 📁 deploy/                   # Deployment scripts (future)
├── 📁 tests/                        # Test files (future)
│   ├── 📁 unit/                     # Unit tests
│   └── 📁 integration/              # Integration tests
├── 📁 docs/                         # All project documentation
│   ├── 📁 requirements/             # Requirements & specifications
│   │   ├── product-overview.md
│   │   ├── core-functionality-overview.md
│   │   ├── development-requirements.md
│   │   └── project-scope.md
│   ├── 📁 adr/                      # Architecture Decision Records
│   │   ├── 📁 decisions/            # Core architectural decisions
│   │   ├── 📁 specifications/       # Technical implementation details
│   │   ├── 📁 business-decisions/   # Product/business strategy
│   │   ├── 📁 analysis/             # Research and analysis
│   │   ├── README.md                # ADR index and guidelines
│   │   └── template.md              # ADR template
│   ├── 📁 operations/               # Operational guides
│   │   └── developer-manual.md
│   ├── 📁 logs/                     # Development logs
│   │   ├── development-journal.md
│   │   └── development-notes.md
│   ├── project-timeline.md          # Project timeline & milestones
│   └── PROJECT_STRUCTURE.md         # This file
├── 📁 config/                       # Configuration files
│   └── .env.example                 # Environment variable template
├── 📁 tools/                        # Development tools (future)
│   ├── 📁 build/                    # Build utilities
│   └── 📁 deployment/               # Deployment utilities
├── 📁 .venv/                        # Python virtual environment
├── 📁 node_modules/                 # Node.js dependencies (auto-generated)
├── .env                             # Environment variables (gitignored)
├── .gitignore                       # Git ignore rules
├── README.md                        # Project overview & setup
├── CLAUDE.md                        # AI assistant instructions
├── requirements.txt                 # Python dependencies
├── package.json                     # Node.js dependencies & scripts
├── tailwind.config.js               # Tailwind CSS configuration
└── postcss.config.js                # PostCSS configuration
```

## Design Principles

### 1. Separation of Concerns
- **`src/`**: All application source code
- **`templates/`**: Frontend presentation layer
- **`data/`**: All data files, organized by environment
- **`docs/`**: All documentation in one place
- **`config/`**: Configuration files isolated

### 2. Environment Isolation
- **`data/dev/`**: Development data
- **`data/test/`**: Test data (future)
- **`data/prod/`**: Production data (future)
- **`config/`**: Environment-specific configurations

### 3. Scalability
- **`src/app/core/`**: Core business logic that rarely changes
- **`src/app/api/`**: API routes can be split by feature areas
- **`src/app/services/`**: Business services can grow independently
- **`tests/`**: Organized by test type for easy maintenance

### 4. Professional Standards
- **Clear naming**: Self-documenting directory names
- **Predictable locations**: Standard locations for common files
- **Import organization**: Clean import paths with logical hierarchy

## Key File Purposes

### Source Code (`src/`)
- **`main.py`**: FastAPI application entry point, route definitions
- **`core/auth.py`**: User authentication, JWT handling, OAuth
- **`core/database.py`**: Database connection, session management
- **`core/models.py`**: SQLModel data models and schemas

### Templates (`templates/`)
- **`auth/`**: Authentication-related templates
- **`components/`**: Reusable template parts for DRY principle
- **Individual pages**: Feature-specific HTML templates

### Data (`data/`)
- **`dev/`**: Development environment data (SQLite database)
- **`test/`**: Test fixtures and test database (future)
- **`backups/`**: Automated database backups (future)

### Scripts (`scripts/`)
- **`dev/`**: Development workflow automation
- **`deploy/`**: Production deployment automation (future)

### Documentation (`docs/`)
- **`requirements/`**: What to build (specifications)
- **`operations/`**: How to build and maintain (procedures)
- **`logs/`**: Development history and insights

## Migration Benefits

### Before (Old Structure)
❌ Mixed concerns at root level  
❌ Templates in two locations  
❌ Database at root level  
❌ Unclear file organization  
❌ No environment separation  

### After (New Structure)
✅ Clear separation of concerns  
✅ Single source of truth for templates  
✅ Environment-specific data storage  
✅ Professional project organization  
✅ Scalable architecture  

## Development Workflow

### Daily Development
1. Navigate to project root: `cd Success-Diary`
2. Activate environment: `source .venv/bin/activate` (Mac) or `.venv\Scripts\activate` (Windows)
3. Run development server: `uvicorn src.app.main:app --reload`
4. Access application: http://localhost:8000

### Adding New Features
1. **Models**: Add to `src/app/core/models.py`
2. **Database**: Update `src/app/core/database.py` if needed
3. **Authentication**: Extend `src/app/core/auth.py` for user features
4. **Routes**: Add to `src/app/main.py` or new files in `src/app/api/`
5. **Templates**: Create in appropriate `templates/` subdirectory
6. **Tests**: Add to `tests/unit/` or `tests/integration/`

### Configuration Management
- Copy `config/.env.example` to `.env` for local development
- Update environment variables in `.env` as needed
- Never commit `.env` file to version control

## Import Patterns

### Within Application
```python
# Core modules
from src.app.core.models import Entry, User
from src.app.core.database import get_session
from src.app.core.auth import current_active_user

# Future API modules
from src.app.api.entries import router as entries_router
from src.app.services.email import send_verification_email
```

### Path Configuration
- **Static files**: `src/static/` directory
- **Templates**: `templates/` directory
- **Database**: `data/dev/db.sqlite3` for development

## Future Expansion

### When to Create New Directories
- **`src/app/api/entries.py`**: When entry routes become complex
- **`src/app/services/`**: For business logic like email, analytics
- **`tests/`**: When adding automated testing
- **`tools/`**: For build scripts, deployment automation

### Scaling Considerations
- Split large modules by feature area
- Use dependency injection for services
- Maintain clear import hierarchies
- Keep configuration centralized

This structure provides a solid foundation for professional software development while remaining simple enough for a solo developer to navigate and maintain.