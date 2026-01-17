from fastapi import FastAPI, Request
from db_config import engine, Base
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
from routers import users, notes, search, auth, download
import time
from alembic.config import Config
from alembic import command
from utils.logger import setup_logger

logger = setup_logger("main")

load_dotenv()

origins = []

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Smriti API", description="Smriti API")

def run_migrations():
    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")

@app.on_event("startup")
def startup_event():
    logger.info("Application starting up...")
    run_migrations()
    logger.info("Database migrations completed.")

@app.middleware("http")
async def log_requests(request: Request, call_next):
    if request.url.path in ["/favicon.ico", "/apple-touch-icon.png", "/apple-touch-icon-precomposed.png"]:
        return await call_next(request)

    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    logger.info(
        f"Method: {request.method} Path: {request.url.path} "
        f"Status: {response.status_code} Duration: {process_time:.4f}s"
    )
    return response

app.include_router(users.router, prefix='/users', tags=['users'])
app.include_router(notes.router, prefix='/notes', tags=['notes'])
app.include_router(search.router, prefix='/search', tags=['search'])
app.include_router(auth.router, prefix='/auth', tags=['auth'])
app.include_router(download.router, prefix='/download', tags=['download'])

if os.getenv("FRONTEND_URL"):
    frontend_url = os.getenv("FRONTEND_URL")
    origins.append(frontend_url)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/')
def check_health():
    logger.info("Health check endpoint called")
    return {'health': 'ok'}
