| Layer          | Tool                                                      | Notes                                                        |
| -------------- | --------------------------------------------------------- | ------------------------------------------------------------ |
| Runtime        | Python 3.12                                               | Latest LTS; async support                                    |
| Web framework  | FastAPI                                                   | Type hints, Pydantic validation, automatic Swagger docs      |
| Templating     | Jinja2                                                    | Render HTML from the server                                  |
| Progressive UX | HTMX                                                      | `hx-` attributes give partial page updates without React     |
| Styling        | Tailwind CSS                                              | Utility classes, no custom CSS churn                         |
| Auth           | Flask-Login-guard (very light) **or** JWT via OAuthlib    | Works with email/password; can add Google later              |
| DB / ORM       | SQLModel (by FastAPI author) → SQLite dev / Postgres prod | Single model file, type-hinted, easy migrations with Alembic |
| Charts         | Chart.js CDN + JSON endpoint                              | One `fetch()` per graph; no heavy state libraries            |
| Hosting        | Render (free web service)                                 | One-click deploy from GitHub; includes free Postgres 0.1 GB  |


Node.js v20.19.2
Tailwind v3.4