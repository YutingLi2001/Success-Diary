# Development Requirements

## Technology Stack

The following stack is designed to support rapid development, clean UX, and scalable architecture for the SuccessDiary MVP. It leverages modern Python tooling with progressive enhancement techniques for a reactive yet server-driven UI experience.

| **Layer** | **Tool / Framework** | **Notes** |
|-----------|---------------------|-----------|
| **Runtime** | Python 3.12 | Latest LTS version with full async/await support |
| **Web Framework** | FastAPI 0.110.1 | High-performance async web framework with type hints, Pydantic validation, and Swagger UI |
| **Templating** | Jinja2 | Server-side HTML rendering, integrated with FastAPI |
| **Progressive UX** | HTMX | Enables partial page updates with `hx-` attributes; no need for React or client-side routing |
| **Styling** | Tailwind CSS v3.4 | Utility-first CSS framework; no custom CSS required |
| **Authentication** | [FastAPI Users](https://github.com/fastapi-users/fastapi-users) 14.0.1 | Provides modular user management (JWT, registration, reset, OAuth-ready), native to FastAPI |
| **Database & ORM** | SQLModel 0.0.24 | Type-safe ORM from the FastAPI author; SQLite (dev) → PostgreSQL (prod) with Alembic support |
| **Charting** | Chart.js (CDN) + JSON API endpoint | Lightweight visualizations using RESTful JSON fetches; avoids heavy frontend libraries |
| **Async Server** | Uvicorn 0.34.3 | ASGI server for running FastAPI with high concurrency support |

## Development Environment

### Global Environment
- **Python:** 3.12
- **Node.js:** v20.19.2

### Python Virtual Environment (Pinned Versions)
- `fastapi==0.110.1`
- `uvicorn==0.34.3`
- `jinja2==3.1.3`
- `tailwindcss==3.4`
- `sqlmodel==0.0.24`
- `fastapi-users==14.0.1`
- `aiosqlite` (for async database operations)

### Development Tools
- **Email Testing**: Mailpit for local email testing (http://localhost:8025)
- **Database**: SQLite for development, PostgreSQL for production
- **Build Tools**: PostCSS, Autoprefixer for CSS processing
- **Development Scripts**: Automated batch files for Windows development

## Deployment Requirements

### MVP Deployment (Current)
- **Platform**: Local development with FastAPI + SQLite
- **Email**: Mailpit for testing
- **Static Assets**: Served via FastAPI static files

### Production Deployment (Post-Calgary)
- **Platform**: AWS Cloud Infrastructure
  - **Compute**: EC2/ECS for application hosting
  - **Database**: PostgreSQL RDS for production scalability
  - **Domain**: Route 53 with SSL certificate via CloudFront
  - **Email**: Production SMTP service (replace Mailpit)
- **Migration Timeline**: After initial MVP validation (post-August 17, 2025)

## Quality Requirements

### Testing Standards
- **Error Rate**: < 1% production error rate (uncaught exceptions per 1,000 requests)
- **Performance**: Responsive UI optimized for both desktop and mobile
- **Data Integrity**: Auto-save functionality to prevent data loss
- **Validation**: Frontend and backend form validation with friendly error messages

### Security Requirements
- **Authentication**: Email verification required for all new accounts
- **Data Isolation**: All user data securely isolated per account
- **Privacy**: No data mining or advertising - user entries remain private
- **Export**: Users maintain full ownership and export capability of their data

### Browser Compatibility
- **Primary**: Modern browsers supporting ES6+ and CSS Grid
- **Responsive**: Mobile-first design with Tailwind CSS
- **Progressive Enhancement**: Core functionality works without JavaScript

## Development Workflow

### Database Management
- **Schema Changes**: Delete `db.sqlite3` and restart for development
- **Migrations**: Alembic for production database migrations
- **Backup**: Regular export functionality for user data protection

### Code Quality
- **Type Hints**: Full Python type annotation with SQLModel
- **Validation**: Pydantic models for data validation
- **Documentation**: Automatic API documentation via FastAPI Swagger UI

### Development Scripts
- **Setup**: Automated dependency installation and environment configuration
- **Testing**: Local email server integration with authentication flow
- **Database**: Safe reset procedures with confirmation prompts