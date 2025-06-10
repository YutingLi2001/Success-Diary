**2025-06-09 Development Journal**

**Progress (Project Initiation)**

* Finalized and committed the core project documents:

  1. **Project Vision** – Defined target users, value proposition, and product philosophy.
  2. **MVP Scope** – Outlined Must/Should/Could/Won’t features using MoSCoW.
* Established the success metrics and 10-week Gantt timeline in **Success Metrics & Timeline**.
* Recorded tech-stack decisions in **Tech Stack Decision** document.

**Progress (Understanding of the Project)**

* Gained clarity on the product’s north star: a lightweight, data-driven daily journal with motivational feedback loops.
* Solidified the boundary between MVP essentials and future enhancements.
* Learned that good planning is just as important as good executing


**Next To-Dos**

1. Decide on tech stack choice.

---

**2025-06-10 Development Journal**

**Progress (Project Setup)**

* Created Python virtual environment and installed FastAPI, SQLModel, Uvicorn, and related packages.
* Initialized Node environment, installed Tailwind CSS, PostCSS, and Autoprefixer; configured local build with `npx tailwindcss init -p`.
* Verified HTMX + Tailwind integration by running `uvicorn app.main:app --reload` and `npm run dev:css`, successfully rendering the first UI at `http://127.0.0.1:8000`.
* Added a comprehensive `.gitignore` to exclude `.venv/`, `node_modules/`, and `db.sqlite3`; committed project skeleton and docs.

**Progress (Understanding of Development)**

* Learned how HTMX simplifies dynamic page updates without a full SPA framework.
* Understood the importance of isolating front-end build artifacts from the Python environment.

**Questions**

* What are we using this virtual environement for?
* How should I organize the folder structure? 

**Next To-Dos**

1. Define the `Entry` data model in `models.py` with all required fields.
2. Integrate Alembic for database migrations and generate the initial migration script.
3. Implement the `POST /api/entry` endpoint and hook it up via HTMX for in-page updates.
4. Create `requirements.txt` and add npm scripts (`dev:css`, `build:css`) to `package.json`.

**Personal Reflection**

> Today’s development feels like copy & pasting from ChatGPT, I need to think harder and learn more.
