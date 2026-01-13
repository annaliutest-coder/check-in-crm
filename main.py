from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from app.db import connect_db, disconnect_db
from app.routes import router as api_router
from app.scheduler_routes import router as scheduler_router
from app.scheduler import start_scheduler, shutdown_scheduler, restore_pending_tasks


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handle startup and shutdown events."""
    await connect_db()
    start_scheduler()
    await restore_pending_tasks()
    yield
    shutdown_scheduler()
    await disconnect_db()


app = FastAPI(
    title="Check-In CRM",
    description="Fast Event Check-In System for collecting emails",
    version="1.0.0",
    lifespan=lifespan
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates
templates = Jinja2Templates(directory="templates")

# Include API routes
app.include_router(api_router, prefix="/api")
app.include_router(scheduler_router, prefix="/api")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """Render the main kiosk page."""
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    """Render the dashboard page."""
    return templates.TemplateResponse("dashboard.html", {"request": request})


@app.get("/scheduler", response_class=HTMLResponse)
async def scheduler_page(request: Request):
    """Render the scheduler management page."""
    return templates.TemplateResponse("scheduler.html", {"request": request})
