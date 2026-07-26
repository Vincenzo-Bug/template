# Python Service Template

A security-conscious foundation for a Python 3.13, FastAPI, PostgreSQL, and
Redis service. It is intentionally domain-neutral: product behavior, schemas,
routes, integrations, and authorization policy belong to the project created
from this template.

## Included

- FastAPI application factory with correlation IDs and safe error responses
- typed, startup-validated settings with secret redaction
- structured logging, OpenTelemetry hooks, liveness, and readiness endpoints
- async SQLAlchemy, Alembic, PostgreSQL, and Redis development services
- Docker image that runs as an unprivileged user with a read-only filesystem
- locked dependencies, tests, linting, type checking, vulnerability scanning,
  documentation validation, and GitHub Actions

## Create a project

Use GitHub's **Use this template** action, then replace the starter metadata:

1. Rename the distribution and CLI in `pyproject.toml`.
2. Rename the `app` package if desired and update its imports/tooling config.
3. Set a project-specific environment prefix instead of `SERVICE_`.
4. Replace service/database/container identifiers in Compose and the Dockerfile.
5. Write the product charter, threat model, API contract, and migrations.
6. Retain or strengthen the default capability deny set before adding automation
   or AI tooling.

## Local development

```bash
uv sync --all-extras --locked
docker compose up -d postgres redis
cp .env.example .env
uv run alembic upgrade head
uv run pytest
uv run service-api
```

The API listens on `http://127.0.0.1:8000`. Use `/health` for liveness and
`/ready` for database readiness. To run the fully containerized stack:

```bash
docker compose up --build
```

## Configuration

Settings use the `SERVICE_` prefix. `.env.example` contains safe development
values only. Production configuration must use managed secrets and explicit CORS
origins; production startup rejects debug mode, wildcard CORS, and the template
development database credentials.

Integration tests require `SERVICE_TEST_DATABASE_URL`; they are skipped when it
is not configured.

## Verification

```bash
uv lock --check
uv run black --check .
uv run ruff check .
uv run mypy app tests
uv run pytest
uv run bandit -c pyproject.toml -r app
uv run pip-audit
```

The reusable agent skills are under `.agents/skills/`. They are copied into the
template as personal workflow aids and are independent of the runtime service.
For a new project, run `/setup-matt-pocock-skills` once before using `to-spec`,
`to-tickets`, or other engineering skills; it creates project-specific tracker
and domain configuration after inspecting that project's remote and conventions.
