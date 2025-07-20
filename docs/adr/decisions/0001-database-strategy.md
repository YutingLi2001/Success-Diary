# ADR-0001: Database Strategy - SQLite to PostgreSQL

## Status

Accepted

## Context

The Success-Diary application requires a database strategy that supports both development velocity and production scalability. Key considerations include:

- **Development Phase**: Need for rapid prototyping and zero-setup complexity
- **Production Requirements**: Multi-user support, data integrity, and performance
- **Team Size**: Small development team requiring simple local setup
- **Deployment Timeline**: Production launch targeted for August 2025
- **Data Migration**: New application with no existing data to migrate

## Decision

Implement a dual-database strategy:
- **Development Environment**: SQLite for local development and testing
- **Production Environment**: PostgreSQL from day one of production deployment
- **No Migration Required**: Direct PostgreSQL deployment eliminates migration complexity

## Considered Options

1. **SQLite Only**: Simple but limited scalability for multi-user production
2. **PostgreSQL Only**: Production-ready but complex local development setup
3. **Dual Strategy (Selected)**: SQLite for development, PostgreSQL for production
4. **Migration Path**: Start with SQLite, migrate to PostgreSQL later

## Consequences

**Positive:**
- Zero local development setup complexity
- Production-ready database from launch
- No data migration complexity or risk
- Single codebase supports both environments via DATABASE_URL configuration
- Fast development iteration with SQLite
- Scalable production infrastructure with PostgreSQL

**Negative:**
- Slight differences between development and production environments
- Need to test with PostgreSQL before production deployment
- Database feature parity considerations between SQLite and PostgreSQL

**Neutral:**
- Standard practice for many web applications
- Well-supported by FastAPI and SQLModel

## Implementation Notes

**Technical Configuration:**
```python
# Database URL configuration
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "sqlite:///./db.sqlite3"  # Development default
)

# Production: "postgresql://user:pass@host:5432/dbname"
```

**Development Environment:**
- Use SQLite file: `db.sqlite3`
- Reset by deleting file and restarting server
- Fast schema iterations during development

**Production Environment:**
- AWS RDS PostgreSQL instance
- Proper connection pooling and performance tuning
- Automated backups and monitoring

**Timeline:**
- Development Phase: SQLite (Current - August 2025)
- Production Launch: PostgreSQL RDS (August 2025)

## References

- SQLModel documentation on database adapters
- FastAPI database configuration patterns
- AWS RDS PostgreSQL best practices
- Original analysis: `docs/requirements/remaining_requirements_analysis.md` (Section 10)