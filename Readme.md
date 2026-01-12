# Smriti API - Notes Management System

Smriti API is a robust and efficient backend service designed for managing personal notes. Built with modern web technologies, it provides a secure and scalable foundation for any frontend notes application.

## Features

### User Management
- **Registration**: Secure user sign-up with email and username uniqueness checks.
- **Authentication**: JWT-based login system for secure session management.
  - **Refresh Tokens**: Implemented secure, rotating refresh tokens using HttpOnly cookies to maintain long-lived sessions safely.
- **Profile Management**: Update user profile details (username, email).
- **Account Control**: Full account deletion capability, cascading to all user data.

### Note Management
- **CRUD Operations**: Complete Create, Read, Update, and Delete functionality for notes.
- **Organization**: Archive and Unarchive notes to keep your workspace organised.
- **Search**: Full-text search capability to instantly find notes by title or content using ILIKE operator.
- **Data Integrity**: All notes are securely linked to the authenticated user.

## Tech Stack

- **Framework**: [FastAPI](https://fastapi.tiangolo.com/) - High performance, easy to learn, fast to code, ready for production.
- **Database ORM**: [SQLAlchemy](https://www.sqlalchemy.org/) - The Python SQL Toolkit and Object Relational Mapper.
- **Database**: PostgreSQL (via `psycopg2-binary`).
- **Migrations**: [Alembic](https://alembic.sqlalchemy.org/) - Lightweight database migration tool for usage with SQLAlchemy.
- **Authentication**: JWT (JSON Web Tokens) with `python-jose` (or `pyjwt`) and `passlib` for password hashing.

## Installation & Setup

Follow these steps to get the project running on your local machine.

### Prerequisites
- Python 3.9 or higher
- PostgreSQL database

### 1. Clone the Repository
```bash
git clone <repository-url>
cd notesApp-backend
```

### 2. Create and Activate Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Configuration
Create a `.env` file in the root directory. You can use `.env.example` as a template.
```env
DATABASE_URL=postgresql://user:password@localhost/dbname
SECRET_KEY=your_secret_key
ALGORITHM=HS256
```

### 5. Database Migrations
Initialize the database tables using Alembic.
```bash
alembic upgrade head
```

## Running the Application

Start the server using Uvicorn:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

The API will be available at `http://localhost:8000`.

## API Documentation

FastAPI automatically generates interactive API documentation. Once the app is running, visit:

- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs) - Interactive exploration and testing of API endpoints.
- **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc) - Alternative documentation view.

## Contributing

Contributions, issues, and feature requests are welcome!

## License

This project is licensed under the MIT License.

