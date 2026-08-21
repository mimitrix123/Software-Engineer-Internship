# Week 3 — Blog Platform API

A complete FastAPI blog platform API with JWT authentication, post CRUD, comments, likes, pagination, search, rate limiting, validation, and automatic Swagger/OpenAPI documentation.

## Features
- JWT access-token authentication
- User registration and login
- Authenticated post CRUD
- Comments and comment deletion by owner
- Like/unlike posts
- Pagination and title/content search
- Per-IP rate limiting middleware
- Pydantic input validation
- SQLite database via SQLAlchemy
- Automatic Swagger UI at `/docs` and ReDoc at `/redoc`
- Unit/API tests with pytest
- Render deployment configuration

## Local setup
```bash
cd week-3/blog-platform-api
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000/docs`.

## Tests
```bash
pytest -q
```

## Deployment
The included `render.yaml` can be used to deploy the API on Render's free web service tier when available for the account/region. Set `SECRET_KEY` in the service environment.

## Authentication
Register or login, copy the JWT from the response, then use Swagger's **Authorize** button with `Bearer <token>`.

## API overview
- `POST /auth/register`
- `POST /auth/login`
- `GET /posts`
- `POST /posts`
- `GET /posts/{post_id}`
- `PUT /posts/{post_id}`
- `DELETE /posts/{post_id}`
- `POST /posts/{post_id}/like`
- `DELETE /posts/{post_id}/like`
- `GET /posts/{post_id}/comments`
- `POST /posts/{post_id}/comments`
- `DELETE /comments/{comment_id}`
- `GET /health`
