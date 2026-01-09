from fastapi import FastAPI
from db_config import engine, Base
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
from routers import users, notes

load_dotenv()

origins = []

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Notes API", description="Notes API")

from alembic.config import Config
from alembic import command

def run_migrations():
    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")

@app.on_event("startup")
def startup_event():
    run_migrations()

app.include_router(users.router, prefix='/users', tags=['users'])
app.include_router(notes.router, prefix='/notes', tags=['notes'])

if os.getenv("FRONTEND_URL"):
    origins.append(os.getenv("FRONTEND_URL"))

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/')
def check_health():
    return {'health': 'ok'}
