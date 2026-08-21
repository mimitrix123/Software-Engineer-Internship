# Week 4 — Production SaaS Platform

A production-oriented full-stack SaaS reference application demonstrating the complete software engineering lifecycle: design, implementation, testing, containerization, CI/CD, observability, API documentation, and cloud deployment.

## Architecture
- **Frontend:** React + Vite
- **Backend:** FastAPI + SQLAlchemy
- **Database:** PostgreSQL in production; SQLite supported locally
- **Authentication:** JWT access tokens + bcrypt password hashing
- **Real-time:** WebSocket notifications
- **API docs:** OpenAPI / Swagger UI / ReDoc
- **Observability:** Prometheus metrics + Grafana dashboard
- **Containers:** Docker + Docker Compose
- **CI/CD:** GitHub Actions
- **Deployment:** Render configuration included

## Features
- User registration/login
- JWT-protected REST API
- SaaS project CRUD
- Real-time project events over WebSockets
- Request validation and error handling
- Health/readiness endpoints
- Structured application logging
- Prometheus metrics at `/metrics`
- Automated tests

## Run locally
```bash
docker compose up --build
```

- Frontend: `http://localhost:5173`
- API: `http://localhost:8000`
- Swagger: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
- Metrics: `http://localhost:8000/metrics`
- Grafana: `http://localhost:3000`

Without Docker:
```bash
cd backend
python -m venv .venv
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Test
```bash
cd backend
pytest -q
```

## Lifecycle
1. Requirements and architecture
2. Domain/API design
3. Implementation
4. Automated testing
5. Containerization
6. CI/CD validation
7. Cloud deployment configuration
8. Monitoring and health checks
9. Documentation and release readiness

## Production notes
Set a strong `SECRET_KEY` and a managed PostgreSQL `DATABASE_URL` in the cloud environment. The included Render blueprint is a deployment starting point; actual cloud deployment requires connecting the repository to a hosting account.
