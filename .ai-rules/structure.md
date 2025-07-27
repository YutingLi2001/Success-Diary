---
title: Project Structure
description: "Defines the project's file organization, naming conventions, and architectural patterns."
inclusion: always
---

# Project Structure - Success-Diary

## Directory Organization

### Root Level Structure
```
Success-Diary/
├── app/                    # Main FastAPI application
├── templates/              # Jinja2 HTML templates  
├── docs/                   # Comprehensive documentation
├── scripts/                # Development automation
├── data/                   # Data storage and backups
├── config/                 # Configuration files
├── tests/                  # Test files (unit, integration)
├── tools/                  # Development utilities
├── src/                    # Alternative source structure (legacy)
├── .ai-rules/              # AI agent guidance files
├── db.sqlite3              # SQLite database (auto-created)
├── requirements.txt        # Python dependencies
├── package.json            # Node.js dependencies
└── tailwind.config.js      # Frontend build configuration
```

## Core Application Structure (`app/`)

### Backend Organization
```
app/
├── main.py                 # FastAPI app, routes, and endpoint definitions
├── auth.py                 # Authentication logic (FastAPI-Users integration)
├── models.py               # Database models (User, Entry, UserFeedback)
├── database.py             # Database configuration and session management
├── errors.py               # Centralized error handling system
├── validation.py           # Server-side form validation logic
├── timezone_utils.py       # Timezone handling utilities
└── __init__.py             # Package initialization
```

### Frontend Assets (`app/static/`)
```
app/static/
├── css/
│   ├── input.css           # Tailwind CSS source file
│   ├── output.css          # Compiled Tailwind CSS (generated)
│   └── progressive-ui.css  # Dynamic UI behavior styles
└── js/
    ├── entry-titles.js     # Entry title generation logic
    ├── error-handlers.js   # Client-side error handling
    ├── progressive-ui.js   # Dynamic field display
    ├── unsaved-changes-warning.js  # Data loss prevention
    └── validation-engine.js # Client-side form validation
```

## Template Architecture (`templates/`)

### Template Organization
```
templates/
├── auth/                   # Authentication pages
│   ├── login.html
│   ├── register.html
│   ├── verify.html
│   ├── forgot-password.html
│   └── reset-password.html
├── components/             # Reusable UI components
├── errors/                 # Error handling templates
│   ├── inline.html         # Inline error messages
│   ├── modal.html          # Modal error dialogs
│   ├── toast.html          # Toast notifications
│   └── error-handlers.js   # Error JavaScript logic
├── partials/               # Template partials
│   └── entry_card.html     # Entry display card component
├── shared/                 # Shared template components
│   ├── entry_content.html  # Entry content display
│   └── entry_form.html     # Entry form fields
├── test/                   # Test templates
│   └── errors.html         # Error testing page
├── dashboard.html          # Main entry creation page
├── entries.html            # Entry history/listing page
├── edit_entry.html         # Entry editing page
├── entry_detail.html       # Individual entry view
├── analytics.html          # Future analytics page
├── archive.html            # Archived entries view
├── settings.html           # User settings page
├── settings_simple.html    # Simplified settings
└── index.html              # Landing/home page
```

### Template Naming Conventions
- **Pages**: `page_name.html` (e.g., `dashboard.html`, `entries.html`)
- **Components**: Located in `components/` directory for reusable elements
- **Partials**: Located in `partials/` for template fragments
- **Shared**: Located in `shared/` for common form/content elements
- **Auth**: All authentication templates in `auth/` subdirectory
- **Errors**: All error handling templates in `errors/` subdirectory

## Documentation Structure (`docs/`)

### Documentation Organization
```
docs/
├── adr/                    # Architecture Decision Records
│   ├── analysis/           # Requirement analysis archives
│   ├── business-decisions/ # Business and product decisions
│   ├── decisions/          # Technical architecture decisions
│   ├── specifications/     # Technical specifications
│   └── template.md         # ADR template for new decisions
├── logs/                   # Development tracking
│   └── development-journal.md
├── planning/               # Project planning documents
│   ├── roadmap.md
│   ├── todo.md
│   └── Notes.txt
├── refactoring/            # Code improvement documentation
│   ├── technical-debt-analysis.md
│   ├── refactoring-roadmap.md
│   └── quick-wins-implementation-guide.md
└── requirements/           # Project requirements
    ├── product-requirements.md
    └── architecture.md
```

## Development Tools Structure

### Automation Scripts (`scripts/`)
```
scripts/
├── mac/                    # macOS/Linux automation
│   ├── dev-setup.command   # Full development environment setup
│   ├── server-start.command # FastAPI server only
│   ├── email-start.command # Mailpit email server
│   └── utilities/          # Helper scripts
│       ├── install-deps.command
│       ├── reset-db.command
│       └── kill-server.command
└── windows/                # Windows automation
    ├── dev-setup.bat       # Full development environment setup
    ├── server-start.bat    # FastAPI server only
    ├── email-start.bat     # Mailpit email server
    └── utilities/          # Helper scripts
        ├── install-deps.bat
        ├── reset-db.bat
        └── kill-server.bat
```

### Test Structure (`tests/`)
```
tests/
├── unit/                   # Unit tests (planned)
└── integration/            # Integration tests (planned)
```

## File Naming Conventions

### Python Files
- **Snake case**: `file_name.py` (e.g., `timezone_utils.py`, `main.py`)
- **Descriptive names**: Files clearly indicate their purpose
- **Single responsibility**: Each file focuses on a specific domain

### HTML Templates
- **Lowercase with hyphens**: `page-name.html` for multi-word pages
- **Underscore for partials**: `partial_name.html` for template fragments
- **Directory grouping**: Related templates grouped in subdirectories

### JavaScript Files
- **Kebab case**: `feature-name.js` (e.g., `progressive-ui.js`, `entry-titles.js`)
- **Descriptive naming**: File names clearly indicate functionality
- **Modular approach**: One concern per file

### CSS Files
- **Lowercase with hyphens**: `style-name.css`
- **Purpose-based naming**: Files named for their role (input, output, progressive-ui)

## Database Organization

### Database Files
- **Development**: `db.sqlite3` in project root (auto-created)
- **Backups**: `data/backups/` for database snapshots
- **Test Data**: `data/test/` for testing scenarios
- **Development Data**: `data/dev/` for development-specific data

### Model Organization (`app/models.py`)
- **User Models**: User, UserRead, UserCreate, UserUpdate
- **Entry Models**: Entry, EntryRead, EntryUpdate, ArchiveRequest
- **Feedback Models**: UserFeedback, UserFeedbackCreate
- **Clear separation**: Read/Create/Update models for API boundaries

## Configuration Management

### Environment Configuration
- **.env**: Environment variables (not in repository)
- **config/**: Configuration files and templates
- **Default values**: Sensible defaults in code for development

### Build Configuration
- **package.json**: Node.js dependencies and build scripts
- **tailwind.config.js**: Tailwind CSS customization
- **postcss.config.js**: PostCSS processing pipeline

## Legacy Structure Note

### Duplicate Structure (`src/`)
The `src/` directory contains an alternative/duplicate application structure that appears to be from an earlier architectural iteration. This includes:
- `src/app/` with core, api, and services subdirectories
- `src/static/` with additional frontend assets

This structure should be evaluated for consolidation during refactoring efforts.

## Development Workflow Patterns

### File Creation Rules
1. **Prefer editing existing files** over creating new ones
2. **Use established directory structure** for new files
3. **Follow naming conventions** consistently
4. **Group related functionality** in appropriate directories

### Template Development
1. **Shared components** go in `templates/shared/`
2. **Reusable UI elements** go in `templates/components/`
3. **Page-specific templates** in root `templates/`
4. **Feature-specific subdirectories** for complex features

### Static Asset Management
1. **CSS compilation** from `input.css` to `output.css`
2. **JavaScript modules** for specific functionality
3. **Progressive enhancement** approach for dynamic features
4. **Build scripts** for production optimization