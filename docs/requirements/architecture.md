# Technical Architecture

## Technology Stack

The following stack is designed to support rapid development, clean UX, and scalable architecture for the SuccessDiary MVP. It leverages modern Python tooling with progressive enhancement techniques for a reactive yet server-driven UI experience.

| **Layer** | **Tool / Framework** | **Version** | **Notes** |
|-----------|---------------------|-------------|-----------|
| **Runtime** | Python | 3.12+ | Latest LTS version with full async/await support |
| **Web Framework** | FastAPI | 0.110.1 | High-performance async web framework with type hints, Pydantic validation, and Swagger UI |
| **Templating** | Jinja2 | 3.1.3 | Server-side HTML rendering, integrated with FastAPI |
| **Progressive UX** | HTMX | Latest | Enables partial page updates with `hx-` attributes; no need for React or client-side routing |
| **Styling** | Tailwind CSS | v3.4 | Utility-first CSS framework; no custom CSS required |
| **Authentication** | FastAPI Users | 14.0.1 | Provides modular user management (JWT, registration, reset, OAuth-ready), native to FastAPI |
| **Database & ORM** | SQLModel | 0.0.24 | Type-safe ORM from the FastAPI author; SQLite (dev) → PostgreSQL (prod) with Alembic support |
| **Charting** | Chart.js (CDN) | Latest | Lightweight visualizations using RESTful JSON fetches; avoids heavy frontend libraries |
| **Async Server** | Uvicorn | 0.34.3 | ASGI server for running FastAPI with high concurrency support |

## Development Environment Architecture

### Local Development Stack
- **Python Environment**: Virtual environment with pinned dependencies
- **Database**: SQLite for rapid prototyping and single-developer workflow
- **Email Testing**: Mailpit for local email testing (http://localhost:8025)
- **Static Assets**: Served via FastAPI static files middleware
- **Build Tools**: PostCSS and Autoprefixer for CSS processing
- **Development Scripts**: Automated batch files for Windows/Mac cross-platform setup

### Cross-Platform Development Setup
- **Windows**: Batch files in `scripts/windows/` for automated setup
- **Mac/Linux**: Shell scripts in `scripts/mac/` for automated setup
- **Node.js Environment**: v20.19.2 for Tailwind CSS compilation
- **Package Management**: pip for Python, npm for Node.js dependencies

## Database Architecture

### Development Database (SQLite)
- **File**: `db.sqlite3` (auto-created on first run)
- **Models**: 
  - `User` (SQLAlchemy + FastAPI-Users base class)
  - `Entry` (SQLModel for familiar syntax)
- **Session Management**: Mixed async/sync approach
  - Async sessions for FastAPI-Users authentication
  - Sync sessions for business logic (Entry operations)

### Production Database (PostgreSQL)
- **Platform**: AWS RDS PostgreSQL
- **Migration Strategy**: SQLite to PostgreSQL migration scripts
- **Data Integrity**: Comprehensive testing of production data flows
- **Backup**: Automated database backups and disaster recovery procedures

### Schema Management
- **Development**: Delete `db.sqlite3` and restart for schema changes
- **Production**: Alembic migrations for safe schema evolution
- **Data Types**: Full type safety with SQLModel/Pydantic integration

## Authentication Architecture

### FastAPI-Users Integration
- **User Model**: Pure SQLAlchemy with FastAPI-Users base class (avoids SQLModel conflicts)
- **Email Verification**: 6-digit codes with 10-minute expiration
- **Session Management**: JWT-based authentication with secure cookies
- **Password Security**: Bcrypt hashing with salt rounds

### Development Authentication
- **Email Service**: Mailpit (localhost:1025) for development email testing
- **SMTP Configuration**: Local SMTP server with web interface
- **Verification Flow**: Complete registration → verification → login testing

### Production Authentication
- **Email Service**: Production SMTP (SendGrid/AWS SES)
- **SSL/HTTPS**: Complete SSL certificate setup and HTTPS enforcement
- **Security Headers**: Proper security headers for production deployment

## Infrastructure Progression

### Phase 1: Local Development (Current)
- **Platform**: Local development with FastAPI + SQLite
- **Email**: Mailpit for testing email verification flows
- **Static Assets**: Served via FastAPI static files
- **Domain**: localhost:8000 for application, localhost:8025 for email testing

### Phase 2: Production Deployment
- **Platform**: AWS Cloud Infrastructure
  - **Compute**: EC2/ECS for application hosting
  - **Database**: PostgreSQL RDS for production scalability
  - **Domain**: Route 53 with SSL certificate via CloudFront
  - **Email**: Production SMTP service (replace Mailpit)
- **Migration Timeline**: After MVP 1.0 validation

### Phase 3: Scaling Considerations (Future)
- **Load Balancing**: Application load balancer for multiple instances
- **Database Scaling**: Read replicas and connection pooling
- **CDN**: CloudFront for static asset delivery
- **Monitoring**: Application monitoring and error tracking

## Security Architecture

### Development Security
- **Local Environment**: Isolated development environment with no external data transmission
- **Email Testing**: Local email server with no external SMTP dependencies
- **Data Isolation**: All user data securely isolated per account during development

### Production Security
- **Authentication**: Email verification required for all new accounts
- **Data Isolation**: All user data securely isolated per account
- **Privacy**: No data mining or advertising - user entries remain private
- **Export Capability**: Users maintain full ownership and export capability of their data
- **HTTPS Enforcement**: All traffic encrypted with SSL certificates

### Data Protection
- **Password Storage**: Bcrypt hashing with proper salt rounds
- **Session Security**: Secure JWT tokens with appropriate expiration
- **Input Validation**: Comprehensive input validation with Pydantic models
- **SQL Injection Prevention**: SQLModel/SQLAlchemy ORM prevents SQL injection

## Performance Architecture

### Development Performance
- **Auto-reload**: Uvicorn hot reload for rapid development iteration
- **Static Assets**: Direct serving for development simplicity
- **Database**: SQLite for minimal setup overhead

### Production Performance
- **Application Server**: Uvicorn with multiple workers for high concurrency
- **Database Optimization**: PostgreSQL with proper indexing and query optimization
- **Static Assets**: CDN delivery for faster asset loading
- **Caching Strategy**: Application-level caching for frequently accessed data

## Quality Requirements

### Browser Compatibility
- **Primary**: Modern browsers supporting ES6+ and CSS Grid
- **Responsive**: Mobile-first design with Tailwind CSS
- **Progressive Enhancement**: Core functionality works without JavaScript

### Performance Standards
- **Page Load**: < 3 seconds on standard connections
- **Error Rate**: < 1% production error rate (uncaught exceptions per 1,000 requests)
- **Uptime**: 99.9% availability target for production deployment
- **Mobile Performance**: Optimized for mobile networks and devices

### Code Quality
- **Type Safety**: Full Python type annotation with SQLModel
- **Validation**: Pydantic models for comprehensive data validation
- **Documentation**: Automatic API documentation via FastAPI Swagger UI
- **Testing**: Unit and integration testing framework (to be implemented)

---

*This document defines the technical architecture and infrastructure strategy. For feature requirements, see `core-functionality-overview.md`. For user requirements, see `product-requirements.md`. For development timeline, see `roadmap.md`.*