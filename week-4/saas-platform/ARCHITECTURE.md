# Architecture & Engineering Lifecycle

## System design
```text
React SPA ──HTTPS──> FastAPI REST API ──> SQLAlchemy ──> PostgreSQL
   │                       │
   └──── WebSocket ────────┤
                           ├── Prometheus /metrics
                           └── Swagger / OpenAPI
```

## Security
- Passwords are never stored in plaintext; bcrypt hashes are persisted.
- JWTs expire after two hours.
- Protected resources require Bearer authentication.
- Pydantic validates request payloads.
- Secrets are supplied through environment variables.
- Production should use HTTPS, a managed PostgreSQL database, restrictive CORS, secret rotation, and a reverse proxy/WAF.

## Reliability
- `/health` checks process availability.
- `/ready` exercises the database dependency.
- Prometheus metrics expose request/latency/error telemetry.
- Docker provides reproducible local environments.
- GitHub Actions runs tests, compilation checks, and a container build.

## Delivery lifecycle
**Discover → Design → Implement → Test → Containerize → CI → Deploy → Observe → Iterate**

## API contract
FastAPI generates the canonical OpenAPI document automatically. Swagger UI is available at `/docs` and ReDoc at `/redoc`.
