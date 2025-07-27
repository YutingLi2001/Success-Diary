---
title: Technology Stack
description: "Defines the project's technical architecture, dependencies, and development practices."
inclusion: always
---

# Technology Stack - Success-Diary

## Architecture Overview
Full-stack web application with FastAPI backend, Jinja2 templating, and SQLite/PostgreSQL database. Designed for single-user development transitioning to multi-user production deployment.

## Backend Stack

### Core Framework
- **FastAPI 0.110.1**: Main web framework for API endpoints and route handling
- **Uvicorn 0.34.3**: ASGI server for running FastAPI application
- **SQLModel 0.0.24**: Database ORM combining SQLAlchemy and Pydantic
- **Python 3.8+**: Primary programming language

### Authentication & Security
- **FastAPI-Users 14.0.1**: Modular user management system with JWT authentication
- **Passlib[bcrypt] 1.7.4**: Password hashing with bcrypt
- **Email Verification**: 6-digit codes with 10-minute expiration
- **Session Management**: JWT-based with secure cookies

### Database
- **Development**: SQLite (db.sqlite3) for rapid prototyping and single-user testing
- **Production**: PostgreSQL RDS for scalability and multi-user support
- **Database Strategy**: Mixed async (authentication) and sync (business logic) sessions
- **File Location**: `db.sqlite3` in project root (auto-created)

### Email System
- **Development**: Mailpit for local email testing (http://localhost:8025)
- **Production**: SMTP service for email verification
- **FastAPI-Mail 1.4.1**: Email sending functionality

### Additional Backend Dependencies
- **Python-multipart**: Form data handling
- **Python-dotenv 1.0.0**: Environment variable management
- **Aiosqlite 0.20.0**: Async SQLite driver
- **HTTPX-OAuth 0.14.0**: OAuth provider integration (future)
- **PyTZ 2023.3**: Timezone handling utilities

## Frontend Stack

### Templating & Styling
- **Jinja2 3.1.3**: Server-side HTML templating
- **Tailwind CSS 3.4**: Utility-first CSS framework
- **PostCSS**: CSS processing with autoprefixer
- **HTMX**: Dynamic interactions without complex JavaScript

### JavaScript Architecture
- **Modular Structure**: Individual JS files for specific functionality
  - `entry-titles.js`: Entry title generation and management
  - `error-handlers.js`: Client-side error handling
  - `progressive-ui.js`: Dynamic field display logic
  - `unsaved-changes-warning.js`: Data loss prevention
  - `validation-engine.js`: Client-side form validation

### CSS Organization
- **Input CSS**: `app/static/css/input.css` (source file)
- **Output CSS**: `app/static/css/output.css` (compiled Tailwind)
- **Progressive UI**: `app/static/css/progressive-ui.css` (dynamic behavior)

## Development Tools

### Build System
- **Node.js/NPM**: Frontend build tooling
- **Tailwind Build**: `npm run build-css` (development), `npm run build-css-prod` (production)
- **PostCSS Config**: Autoprefixer and Tailwind processing

### Development Scripts
- **Windows**: Batch files in `scripts/windows/`
  - `dev-setup.bat`: Full development environment setup
  - `server-start.bat`: FastAPI server only
  - `email-start.bat`: Mailpit email server
- **Mac/Linux**: Shell scripts in `scripts/mac/`
  - `dev-setup.command`: Full development environment
  - `server-start.command`: FastAPI server only
  - `email-start.command`: Mailpit email server

### Database Management
- **Schema Changes**: Delete `db.sqlite3` and restart server (development)
- **Reset Scripts**: Platform-specific database reset utilities
- **Models Location**: `app/models.py` (SQLModel definitions)

## Deployment Architecture

### Development Environment
- **Local Server**: http://localhost:8000 (FastAPI)
- **Email Testing**: http://localhost:8025 (Mailpit)
- **Database**: SQLite file storage
- **Static Files**: Served by FastAPI StaticFiles

### Production Target
- **Platform**: AWS EC2/ECS with PostgreSQL RDS
- **Domain**: Custom domain with Route 53 and SSL via CloudFront
- **Database Migration**: SQLite → PostgreSQL transition documented
- **Timeline**: Production launch target August 17, 2025

## Code Quality & Testing

### Validation & Linting
- **Server Validation**: `app/validation.py` with comprehensive field validation
- **Client Validation**: JavaScript validation engine with real-time feedback
- **Type Checking**: MyPy for static type analysis
- **Linting**: Flake8 for code style enforcement

### Error Handling System
- **Centralized Error Handling**: `app/errors.py` with custom exception classes
- **Error Types**: Authentication, Validation, Network, HTTP, General exceptions
- **Template System**: Dedicated error templates (inline, modal, toast)
- **Recovery Guidance**: Contextual error messages with retry functionality

### Testing Structure
- **Unit Tests**: `tests/unit/` (planned)
- **Integration Tests**: `tests/integration/` (planned)
- **Test Command**: `pytest` (when implemented)

## Key Configuration Files
- **requirements.txt**: Python dependencies
- **package.json**: Node.js dependencies and build scripts
- **tailwind.config.js**: Tailwind CSS configuration
- **postcss.config.js**: PostCSS processing configuration
- **.env**: Environment variables (not in repository)

## Development Commands

### Quick Start
```bash
# Windows
scripts\windows\dev-setup.bat

# Mac/Linux  
./scripts/mac/dev-setup.command
```

### Manual Setup
```bash
# Virtual environment
python -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows

# Dependencies
pip install -r requirements.txt
npm install

# Servers
mailpit &                 # Email server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### CSS Compilation
```bash
npm run build-css        # Development (watch mode)
npm run build-css-prod   # Production (minified)
```