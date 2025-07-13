## 2025-06-09 – Dev Log #1: Project Foundation

### Progress
- Created core project documents:
  - `Project Vision`: defined users, value, and philosophy
  - `MVP Scope`: feature priorities using MoSCoW
  - `Success Metrics & Timeline`: 10-week Gantt chart
  - `Tech Stack Decision`: finalized core technologies

### Insight
- Good planning clarified MVP boundaries and reduced ambiguity.

### Next Steps
- Finalize tech stack
- Scaffold initial project structure

## 2025-06-10 – Dev Log #2: Project Setup

### Progress
- Set up Python virtual environment and installed FastAPI, SQLModel, Uvicorn
- Initialized Node environment with Tailwind CSS, PostCSS, Autoprefixer
- Verified HTMX + Tailwind rendering at `http://127.0.0.1:8000`
- Added `.gitignore` and committed clean project skeleton

### Learnings
- HTMX simplifies dynamic interfaces without full SPA overhead
- Frontend build artifacts should remain isolated from Python logic

### Questions
- What is the long-term role of the virtual environment?
- How should the folder structure be organized?

### Next Steps
- Define `Entry` model in `models.py`
- Integrate Alembic and create initial migration
- Build `POST /api/entry` endpoint with HTMX form
- Add `requirements.txt` and NPM scripts
- Improve folder layout and module separation

### Reflection
- Development felt too passive; aim for deeper understanding moving forward

## 2025-07-13 – Dev Log #3: Claude Code Integration & UX Refinement

### Progress
- Switched coding partner from ChatGPT to Claude Code 
- Fixed runtime bugs (missing `date`, template path errors, missing dependencies)
- Completed 11-field `Entry` form with optional fields and form validation
- Updated schema to support nullable fields with SQLModel
- Removed non-English text and standardized language for international use

### UX Refinement
- Made fields 2 and 3 optional in each section to reduce user pressure
- Added visual indicators for required vs optional fields
- Reworded field labels for softer, more approachable tone

### Technical Learnings
- Google Chrome actually has a terminal for debugging in F12

### Current Status
- Refined UX and complete documentation

### Next Steps
- ==Re-plan all existing projects – including timeline, scope, and priorities==
- More testing and improvement on existing UI and functionalities
- Introducing User authentication

### Reflection
Today marks a major shift in my development workflow — I've started using Claude Code as my primary coding partner instead of ChatGPT. The experience is remarkably powerful. I believe this could be a turning point.

It's prompted me to reassess my role as a human developer. Rather than focusing solely on improving traditional programming skills, I now feel a stronger urge to master how to collaborate effectively with AI agents.