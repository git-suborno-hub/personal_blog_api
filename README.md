# Personal Blogging Platform API

## 📌 Project Overview

I am building a **backend-only RESTful API** for a personal blogging platform using Python and FastAPI. The main goal of this project is to learn backend development by building, focusing on clean API design, proper project structure, and real-world backend fundamentals rather than just CRUD shortcuts.

## 🎯 Project Goals

* Build a well-structured RESTful API that can power a personal blog
* Learn how backend systems are designed and organized
* Gradually move from dummy data to a real database-backed application
* Make the project portfolio-ready for junior backend roles

## 🛠️ Tech Stack (Planned)

* **Python** - Core programming language
* **FastAPI** - Modern web framework for APIs
* **PostgreSQL** - Relational database (upcoming)
* **SQLAlchemy** - SQL toolkit and ORM (upcoming)
* **Pydantic** - Data validation and settings management
* **Uvicorn** - ASGI server
* **Git & GitHub** - Version control and collaboration

## ✅ Completed Features

* FastAPI project initialized with a clean folder structure
* Virtual environment and dependency management set up
* Health check endpoint (`/health`) implemented
* Core Article entity defined using Pydantic schemas
* Articles API router created
* GET `/articles` endpoint implemented using dummy (in-memory) data
* Swagger/OpenAPI documentation enabled and verified

### Current Implementation Details

At this stage, the project intentionally avoids database integration to clearly understand:

* API routing
* Request/response flow
* Schema-based validation
* Separation of concerns in backend projects

## 🔄 Current Focus

* Replacing dummy data with a real database
* Designing the articles table
* Introducing SQLAlchemy step by step
* Implementing full CRUD operations properly

## 🚀 Final Vision

By the end of the project, the API will:

* Support full CRUD operations for blog articles
* Allow filtering and pagination
* Follow REST best practices
* Be structured in a way that reflects real backend engineering standards

## 📁 Project Structure

```
personal-blog-api/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── articles.py
│   │   └── health.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── article.py
│   └── models/
│       └── __init__.py
├── requirements.txt
├── .gitignore
└── README.md
```

## 🔧 Installation & Setup

```bash
# Clone the repository
git clone <repository-url>
cd personal-blog-api

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the application
uvicorn app.main:app --reload
```

## 📚 API Documentation

Once the server is running, you can access:

* **Interactive API Docs**: http://localhost:8000/docs
* **Alternative API Docs**: http://localhost:8000/redoc
* **OpenAPI Schema**: http://localhost:8000/openapi.json

## 🧪 Current Endpoints

### Health Check
```http
GET /health
```
Returns API health status.

### Get All Articles
```http
GET /articles
```
Returns a list of articles (currently using dummy data).

## 🎯 Learning Objectives

This project is being developed incrementally with strict daily goals and meaningful Git commits to simulate a real-world development workflow. The focus is on:

1. **Fundamentals First**: Understanding HTTP, routing, and request/response cycles
2. **Progressive Enhancement**: Starting simple and adding complexity gradually
3. **Clean Architecture**: Following separation of concerns and modular design
4. **Documentation**: Maintaining clear documentation and API specs
5. **Version Control**: Using Git effectively with meaningful commits

## 📈 Development Roadmap

### Phase 1: Foundation ✅
- [x] Project setup and structure
- [x] Basic FastAPI configuration
- [x] Health endpoint
- [x] Article schema definition
- [x] Dummy data implementation

### Phase 2: CRUD Operations (Current)
- [ ] Database integration (PostgreSQL + SQLAlchemy)
- [ ] Full CRUD endpoints for articles
- [ ] Input validation and error handling
- [ ] Request/response model refinement

### Phase 3: Advanced Features
- [ ] Authentication and authorization
- [ ] Pagination and filtering
- [ ] Search functionality
- [ ] Categories and tags
- [ ] Comments system

### Phase 4: Production Readiness
- [ ] Testing (unit, integration)
- [ ] Logging and monitoring
- [ ] Deployment configuration
- [ ] Performance optimization
- [ ] Security hardening

## 🤝 Contributing

This is a personal learning project, but suggestions and feedback are welcome! If you have ideas for improvement or find issues, please feel free to open an issue or submit a pull request.

## 📄 License

This project is open source and available for educational purposes.

---

**Note**: This project is actively under development as part of a backend learning journey. The structure and features may evolve as new concepts are learned and implemented.