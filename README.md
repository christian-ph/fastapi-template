# Template Project - FastAPI + PostgreSQL

Python backend based on FastAPI with a layered architecture (adapters/domain/application/infrastructure), repository-based data access, and centralized configuration. It includes PostgreSQL integration, encryption for sensitive columns, colored logging, and Docker support. Python versioning, virtual environments, and dependencies are intended to be managed with `uv`.

## Project structure

- `app/main.py`: FastAPI entrypoint.
- `app/factory.py`: app creation, middleware, and routes.
- `app/adapters/api/v1/routers/`: HTTP routers (health, users).
- `app/domain/`: entities and repository ports.
- `app/application/`: DTOs and mappers.
- `app/infrastructure/`: config, logging, DB, repositories, security.
- `config/*.conf`: environment configuration (app and DB).
- `main.py`: simple "Hello world" example.
- `Dockerfile`, `docker-compose.yml`: containerization.

## Behavior and current capabilities

- FastAPI API with automatic docs:
  - Swagger: `/api/docs`
  - ReDoc: `/api/redoc`
  - OpenAPI: `/api/openapi.json`
- Base endpoints:
  - `GET /welcome` returns environment and DB info.
  - `GET /ping` returns `pong`.
  - `GET /api/v1/health` basic health check.
- User CRUD (async repository + SQLAlchemy) with Pydantic input/output schemas:
  - `POST /api/v1/users/test` DB write/read test.
  - `POST /api/v1/users` create user.
  - `GET /api/v1/users/{user_id}` read user.
  - `GET /api/v1/users/by-email/{email}` read by email.
  - `PUT /api/v1/users/{user_id}` update user.
  - `DELETE /api/v1/users/{user_id}` delete user.
- Async persistence with SQLAlchemy and PostgreSQL.
- Encryption for sensitive columns (email, name, password) using `pgp_sym_encrypt`.
- Password hashing with Argon2.
- Colored logging with `coloredlogs`.
- Configurable CORS.

## Tech stack

- Python 3.14+
- FastAPI
- Uvicorn
- SQLAlchemy 2.x
- PostgreSQL (psycopg3)
- Pydantic v2 + pydantic-settings
- Alembic (dependency included)
- Argon2 (argon2-cffi)
- Docker / Docker Compose

## Configuration

The app loads configuration from:

1) `.conf` files in `config/`
2) Environment variables in `.env` (higher priority)

Examples:

- `config/app.conf` (APP_NAME, DEBUG, CORS_ORIGINS)
- `config/connection.conf` (HOST, PORT, DB_NAME, DB_USER, DB_PASSWORD, DB_SCHEMA, etc.)

Key variables:

- `APP_NAME`
- `DEBUG`
- `CORS_ORIGINS` (comma-separated list)
- `SECRET_KEY` (encryption key)
- DB: `HOST`, `PORT`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_SCHEMA`

## Database requirements

- PostgreSQL with the `pgcrypto` extension enabled (required by `pgp_sym_encrypt`).
- The schema is created automatically if it does not exist.

## How to run

### 1) Local environment (uv)

```bash
uv python install 3.14
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Alternative (from `pyproject.toml`):

```bash
uv python install 3.14
uv venv
source .venv/bin/activate
uv sync
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### 2) Docker

```bash
docker build -t template-project .
docker run -p 8000:8000 --env-file .env template-project
```

### 3) Docker Compose

```bash
docker compose up --build
```

## Tests

The project uses `pytest` for unit testing, with a focus on isolation and mockability.

### Test Structure

- `tests/conftest.py`: contains shared fixtures and global mocks (e.g., DB session, repositories, and environment isolation).
- `tests/test_config.py`: unit tests for application configuration and parsing.
- `tests/test_user_routes.py`: unit tests for User CRUD API endpoints.

### Scalability and Mocking

To ensure tests are fast and reliable:
1. **Environment Isolation**: The `clean_env` fixture (applied automatically) prevents tests from reading real `.env` files.
2. **Dependency Mocking**: Database and repository dependencies are mocked using `pytest` fixtures, allowing tests to run without a PostgreSQL instance.
3. **Common Fixtures**: Use the `client`, `mock_db`, and `mock_user_repo` fixtures to facilitate testing new components.

### How to run tests

```bash
uv run pytest tests
```

To run tests with broad output:

```bash
uv run pytest tests -v
```

## Pre-commit hooks

Pre-commit is used to enforce formatting, linting, typing, and tests before commit.

### Install hooks

```bash
uv run pre-commit install
```

### Run all hooks

```bash
uv run pre-commit run --all-files
```

### Run a single hook

```bash
uv run pre-commit run ruff-lint
```

## Future Improvements

- Add extra validation and pagination for list endpoints.
- Add Alembic migrations and data seeds.
- Add authentication (JWT/OAuth2) and roles.
- Add observability (metrics, tracing).
