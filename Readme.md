# Notes App

What i have done till now - 

1. Created a FastAPI application for a notes management system.
2. connected to the database using sqlalchemy.
3. created a database table for notes.
4. just implmented CRUD operations for notes.

added alembic for database migrations.
commands include - alembic init alembic, alembic upgrade head


Build Command: pip install -r requirements.txt
Start Command: uvicorn main:app --host 0.0.0.0 --port 10000

(Note: Migrations run automatically on startup) 