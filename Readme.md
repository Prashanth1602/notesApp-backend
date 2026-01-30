# Smriti API — Notes Management Backend

Smriti is a backend system focused on secure data persistence, authentication, and note lifecycle management.  
The project explores how personal user data can be stored, queried, exported, and deleted safely in a multi-user API.

The frontend exists only to exercise and validate backend workflows.

---

## Core Focus Areas

### Authentication & Session Design
- JWT-based authentication with short-lived access tokens
- Long-lived refresh tokens stored as HttpOnly cookies
- Token revocation via database-backed refresh tokens
- Immediate access denial for deleted or deactivated users

This design limits the blast radius of token compromise while keeping sessions usable.

---

### Note Lifecycle Management
- Full CRUD operations scoped strictly to the authenticated user
- Archive and unarchive flows to support long-term data organization
- Cascade deletion of all user-owned data on account removal
- Export of all user notes as a single HTML file

---

### Search & Data Integrity
- Full-text search using PostgreSQL `TSVECTOR`
- `websearch_to_tsquery` support (quotes, negation, OR)
- Strong ownership guarantees enforced at the database and API layers
- Indexed queries to keep search and reads efficient

---

### Observability & Operational Awareness
- Structured logging for requests, errors, and system events
- Rotating log files for production-style log management
- Centralized error handling to avoid leaking internal details

---

## Tech Stack

- **Framework**: FastAPI
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy
- **Migrations**: Alembic
- **Authentication**: JWT (HS256), Passlib (bcrypt)
- **Logging**: Python logging with RotatingFileHandler

---

