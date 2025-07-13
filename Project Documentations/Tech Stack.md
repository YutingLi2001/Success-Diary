## Technology Stack – *SuccessDiary MVP*

The following stack is designed to support rapid development, clean UX, and scalable architecture for the **SuccessDiary** MVP. It leverages modern Python tooling with progressive enhancement techniques for a reactive yet server-driven UI experience.

| **Layer**          | **Tool / Framework**                                                   | **Notes**                                                                                         |
| ------------------ | ---------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------- |
| **Runtime**        | Python 3.12                                                            | Latest LTS version with full async/await support                                                  |
| **Web Framework**  | FastAPI 0.110.1                                                        | High-performance async web framework with type hints, Pydantic validation, and Swagger UI         |
| **Templating**     | Jinja2                                                                 | Server-side HTML rendering, integrated with FastAPI                                               |
| **Progressive UX** | HTMX                                                                   | Enables partial page updates with `hx-` attributes; no need for React or client-side routing      |
| **Styling**        | Tailwind CSS v3.4                                                      | Utility-first CSS framework; no custom CSS required                                               |
| **Authentication** | [FastAPI Users](https://github.com/fastapi-users/fastapi-users) 14.0.1 | Provides modular user management (JWT, registration, reset, OAuth-ready), native to FastAPI       |
| **Database & ORM** | SQLModel 0.0.24                                                        | Type-safe ORM from the FastAPI author; SQLite (dev) → PostgreSQL (prod) with Alembic support      |
| **Charting**       | Chart.js (CDN) + JSON API endpoint                                     | Lightweight visualizations using RESTful JSON fetches; avoids heavy frontend libraries            |
| **Hosting**        | Render (Free Web Service Tier)                                         | One-click deployment from GitHub; includes free PostgreSQL (0.1 GB); automatic HTTPS & sleep mode |
| **Async Server**   | Uvicorn 0.34.3                                                         | ASGI server for running FastAPI with high concurrency support                                     |

---

### Global Environment

* **Python:** 3.12
* **Node.js:** v20.19.2

### Python Virtual Environment (Pinned Versions)

* `fastapi==0.110.1`
* `uvicorn==0.34.3`
* `jinja2==3.1.3`
* `tailwindcss==3.4`
* `sqlmodel==0.0.24`
* `fastapi-users==14.0.1`

---

