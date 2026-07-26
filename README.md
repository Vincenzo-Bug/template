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
- AI-agent guidance for Codex-style project starts, shared language, architecture
  boundaries, TDD, and verification loops

## Create a project

Use GitHub's **Use this template** action, then replace the starter metadata:

1. Rename the distribution and CLI in `pyproject.toml`.
2. Rename the `app` package if desired and update its imports/tooling config.
3. Set a project-specific environment prefix instead of `SERVICE_`.
4. Replace service/database/container identifiers in Compose and the Dockerfile.
5. Write the product charter, threat model, API contract, and migrations.
6. Retain or strengthen the default capability deny set before adding automation
   or AI tooling.
7. Ask Codex to read `AGENTS.md` and `docs/ai/project-start-checklist.md` before
   implementing product behavior.

## AI-assisted workflow

This template includes software-fundamentals rules for Codex and other AI coding
agents:

- `AGENTS.md` contains the root instructions agents should follow first.
- `docs/ai/software-fundamentals.md` explains the principles behind the workflow.
- `docs/ai/project-start-checklist.md` gives Codex a repeatable startup process.
- `docs/ai/project-charter.md` captures the product goal, users, constraints, and
  acceptance criteria.
- `docs/ai/ubiquitous-language.md` keeps humans, code, tests, docs, and AI prompts
  aligned on terminology.
- `docs/ai/architecture-map.md` tracks module boundaries and public interfaces.

The intended pattern is: shared understanding first, shared language second, small
verified implementation third. Do not ask an agent to generate large amounts of code
from a vague specification and repeatedly rerun it until it works.

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
uv run mkdocs build --strict
```

See the [documentation](docs/00_overview.md) for architecture, security, and
adaptation guidance.
