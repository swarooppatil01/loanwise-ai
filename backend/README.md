# LoanWise AI Backend

FastAPI + PostgreSQL backend for the LoanWise AI technical project.

## Current scope

- FastAPI API
- PostgreSQL
- SQLAlchemy 2
- Alembic migrations
- JWT authentication
- Argon2 password hashing
- User profiles
- Demo loan products
- CORS
- Health endpoint

## Run locally

```bash
cd backend
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Start PostgreSQL from the repository root:

```bash
docker compose -f docker-compose.backend.yml up -d
```

Run migrations:

```bash
cd backend
alembic upgrade head
```

Seed demo products:

```bash
python -m scripts.seed_data
```

Start API:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Open:

- http://localhost:8000/
- http://localhost:8000/health
- http://localhost:8000/docs
