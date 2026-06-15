# AWS Cost Guardian

AWS cost monitoring tool with automatic ingestion, threshold alerts, and a REST API. Built with FastAPI, PostgreSQL and Docker Compose.

## Stack

- **FastAPI** — REST API backend
- **PostgreSQL** — persistent cost data storage
- **SQLAlchemy + Alembic** — ORM and database migrations
- **Boto3** — AWS Cost Explorer integration
- **APScheduler** — automatic ingestion every 6 hours
- **Docker Compose** — reproducible local environment

## Project structure

```
app/
  api/v1/       # versioned API routes
  core/         # config and scheduler
  db/           # database engine and session
  models/       # SQLAlchemy ORM models
  services/     # AWS Cost Explorer logic
alembic/        # database migrations
tests/          # unit and integration tests
Dockerfile
docker-compose.yml
```

## Getting started

1. Copy `.env.example` to `.env` and fill in your values:
   ```
   AWS_ACCESS_KEY_ID=your_key
   AWS_SECRET_ACCESS_KEY=your_secret
   AWS_REGION=us-east-1
   AWS_COST_ALERT_THRESHOLD=100.0
   ```
2. Build and start:
   ```bash
   docker compose up --build
   ```
3. Apply database migrations:
   ```bash
   docker compose run --rm web alembic upgrade head
   ```
4. API available at `http://localhost:8000`
5. Interactive docs at `http://localhost:8000/docs`

## API endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/v1/health` | Health check including DB connectivity |
| `POST` | `/api/v1/costs/ingest` | Fetch costs from AWS and store in DB |
| `GET` | `/api/v1/costs` | List cost records (filters: `service`, `start`, `end`) |
| `GET` | `/api/v1/costs/summary` | Monthly cost summary with threshold alert |

## Notes

- `.env` is git-ignored — never commit credentials
- The scheduler runs `ingest` automatically every 6 hours
- `POST /costs/ingest` is idempotent — safe to call multiple times
