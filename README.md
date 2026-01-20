# Personal Blog API

A simple, clean, and modern RESTful API for a personal blog built with **FastAPI**, **SQLAlchemy**, and **SQLite**.  
Perfect for learning backend development, API design, and FastAPI best practices.

## Features (Implemented So Far)

- FastAPI application setup with automatic interactive docs (Swagger UI)
- SQLite database integration using SQLAlchemy ORM
- Health check endpoint (`/health`)
- Welcome message at root (`/`)
- Article model with fields: `id`, `title`, `content`, `tags`, `created_at`, `updated_at`, `is_published`
- Pydantic schemas for request/response separation:
  - `ArticleCreate` (for POST requests)
  - `ArticleResponse` (for GET responses)

## Tech Stack

- **Python** 3.10+
- **FastAPI** — modern, fast web framework
- **Uvicorn** — ASGI server
- **SQLAlchemy** — ORM for database
- **Pydantic** — data validation & serialization
- **SQLite** — lightweight local database (for development)

## Project Structure
personal_blog_api/
├── app/
│   ├── init.py
│   ├── main.py               # FastAPI app instance, root & health endpoints
│   ├── database.py           # DB engine, session, Base, get_db dependency
│   ├── models.py             # SQLAlchemy Article model
│   ├── schemas.py            # Pydantic models: ArticleCreate, ArticleResponse
│   └── routers/              # (empty for now — endpoints coming soon)
├── tests/                    # (empty for now)
├── venv/                     # Virtual environment
├── .gitignore
├── requirements.txt
├── README.md
└── blog.db                   # SQLite database file


