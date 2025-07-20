# Architecture Decision Records (ADRs)

This directory contains Architecture Decision Records and related technical documentation for the Success-Diary project.

## Directory Structure

```
docs/adr/
├── README.md                    # This file
├── template.md                  # ADR template
├── decisions/                   # Core architectural decisions
├── specifications/              # Technical implementation details
├── business-decisions/          # Product and business strategy
└── analysis/                    # Ongoing research and analysis
```

## About ADRs

An Architecture Decision Record (ADR) captures a single architectural decision and its rationale. Each ADR describes the forces that influence a decision, the decision itself, and the consequences of that decision.

## Content Types

### Core ADRs (`decisions/`)
Architectural choices affecting system design, scalability, and maintainability.

### Technical Specifications (`specifications/`)
Implementation details, configuration standards, and technical constraints.

### Business Decisions (`business-decisions/`)
Product strategy, pricing, and user experience philosophy.

### Analysis (`analysis/`)
Ongoing research, unresolved questions, and comparative analysis.

## ADR Index

### Architectural Decisions

| Number | Title | Status | Date |
|--------|-------|--------|------|
| 0001 | [Database Strategy: SQLite to PostgreSQL](./decisions/0001-database-strategy.md) | Accepted | 2025-01-17 |
| 0002 | [Authentication: Email Verification System](./decisions/0002-authentication-email-verification.md) | Accepted | 2025-01-17 |
| 0003 | [Frontend: Mobile Responsive Breakpoints](./decisions/0003-frontend-responsive-breakpoints.md) | Accepted | 2025-01-17 |
| 0004 | [UI/UX: Entry Title Auto-Generation](./decisions/0004-entry-title-auto-generation.md) | Accepted | 2025-01-17 |
| 0005 | [Data: User Timezone Handling Strategy](./decisions/0005-timezone-handling-strategy.md) | Accepted | 2025-01-17 |
| 0006 | [History View Sorting Strategy](./decisions/0006-history-view-sorting.md) | Accepted | 2025-01-17 |
| 0007 | [Analytics Architecture with Chart.js](./decisions/0007-analytics-architecture.md) | Accepted | 2025-01-17 |
| 0008 | [Data Export Strategy - CSV First](./decisions/0008-data-export-strategy.md) | Accepted | 2025-01-17 |
| 0009 | [OAuth Provider Priority Strategy](./decisions/0009-oauth-provider-priority.md) | Accepted | 2025-01-17 |
| 0010 | [User Feedback Collection Strategy](./decisions/0010-feedback-collection-strategy.md) | Accepted | 2025-01-17 |
| 0011 | [Browser Compatibility Baseline](./decisions/0011-browser-compatibility-baseline.md) | Accepted | 2025-01-17 |
| 0012 | [Entry Archive System](./decisions/0012-entry-archive-system.md) | Accepted | 2025-01-17 |

### Technical Specifications

| Document | Description |
|----------|-------------|
| [Character Limits](./specifications/character-limits-spec.md) | Entry character limits and UI feedback |
| [Error Handling](./specifications/error-handling-spec.md) | HTMX-native error handling patterns |
| [Performance Standards](./specifications/performance-standards-spec.md) | MVP performance approach and monitoring |

### Business Decisions

| Number | Title | Status | Date |
|--------|-------|--------|------|
| 0001 | [Pricing Model Strategy](./business-decisions/0001-pricing-model-strategy.md) | Accepted | 2025-01-17 |

## Creating New Documentation

### New ADR (decisions/)
1. Copy `template.md` to `decisions/XXXX-short-title.md`
2. Update the ADR index table above
3. Fill in all sections of the template
4. Submit for review and update status accordingly

### New Specification (specifications/)
1. Create `specifications/feature-name-spec.md`
2. Include overview, requirements, implementation, and testing
3. Add entry to Technical Specifications table

### New Business Decision (business-decisions/)
1. Create `business-decisions/XXXX-decision-name.md`
2. Follow business decision template format
3. Add entry to Business Decisions table

## ADR Lifecycle

- **Proposed**: Under discussion, not yet agreed upon
- **Accepted**: Agreed upon and ready for implementation
- **Deprecated**: No longer relevant but kept for historical context
- **Superseded**: Replaced by a newer ADR (reference the replacement)

## Guidelines

- **One decision per ADR**: Keep architectural decisions focused
- **Concise content**: 1-2 pages maximum for readability
- **Future-focused**: Write for developers who will maintain the code
- **Status updates**: Keep status current as decisions evolve
- **Cross-references**: Link related ADRs and specifications
- **Implementation details**: Include concrete technical guidance