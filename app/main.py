from datetime import date
from fastapi import FastAPI, Request, Depends, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from sqlmodel import Session
from pathlib import Path
from app.database import engine, init_db
from app.models import Entry
from fastapi.templating import Jinja2Templates

app = FastAPI()
app.mount("/static", StaticFiles(directory=Path(__file__).parent / "static"), name="static")
templates = Jinja2Templates(directory=Path(__file__).parent.parent / "templates")


@app.on_event("startup")
def on_startup() -> None:
    init_db()


def get_session() -> Session:
    with Session(engine) as session:
        yield session


@app.get("/", response_class=HTMLResponse)
def index(request: Request, db: Session = Depends(get_session)):
    entries = db.query(Entry).order_by(Entry.entry_date.desc()).all()
    return templates.TemplateResponse("index.html", {"request": request, "entries": entries})


@app.post("/add")
def add_entry(
    success_1: str = Form(...),
    success_2: str = Form(""),
    success_3: str = Form(""),
    gratitude_1: str = Form(...),
    gratitude_2: str = Form(""),
    gratitude_3: str = Form(""),
    anxiety_1: str = Form(...),
    anxiety_2: str = Form(""),
    anxiety_3: str = Form(""),
    score: int = Form(...),
    db: Session = Depends(get_session),
):
    entry = Entry(
        user_id="demo",
        entry_date=date.today(),
        success_1=success_1,
        success_2=success_2 if success_2.strip() else None,
        success_3=success_3 if success_3.strip() else None,
        gratitude_1=gratitude_1,
        gratitude_2=gratitude_2 if gratitude_2.strip() else None,
        gratitude_3=gratitude_3 if gratitude_3.strip() else None,
        anxiety_1=anxiety_1,
        anxiety_2=anxiety_2 if anxiety_2.strip() else None,
        anxiety_3=anxiety_3 if anxiety_3.strip() else None,
        score=score
    )
    db.add(entry)
    db.commit()
    return RedirectResponse("/", status_code=303)
