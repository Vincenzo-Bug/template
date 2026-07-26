# Architecture Map

Keep this file current enough that a new Codex session can understand the codebase
without rediscovering every file.

The purpose of this map is to protect deep modules with simple interfaces.

## Current modules

| Module | Responsibility | Public interface | Hidden complexity | Dependencies | Tests | Risk level |
| --- | --- | --- | --- | --- | --- | --- |
| `app.api.routes.health` | Expose liveness and readiness endpoints. | `GET /health`, `GET /ready` | Timeout handling, safe dependency failure reporting. | Settings, database health adapter. | Health route tests. | Medium |
| `app.schemas.health` | Define safe response contracts for health endpoints. | `HealthResponse`, `DependencyStatus`, `ReadinessResponse` | Pydantic validation and forbidden extra fields. | Pydantic. | Schema and route tests. | Low |
| `app.core.config` | Load and validate typed settings. | Settings object. | Environment parsing, production safety checks, redaction. | Pydantic settings. | Settings tests. | High |
| `app.core.logging` | Configure structured logging. | Logger factory/configuration functions. | Redaction, JSON formatting, correlation IDs. | Python logging. | Logging tests. | Medium |
| `app.db` | Database engine/session/migrations support. | Database adapter/session functions. | SQLAlchemy setup, connection lifecycle, Alembic. | PostgreSQL, SQLAlchemy, Alembic. | Database tests. | High |

## Interface design rules

- Public interfaces should be small, stable, and easy to test.
- Internal implementation may be complex if the interface hides that complexity well.
- Avoid modules that only forward calls without hiding meaningful complexity.
- If adding behavior requires touching many modules, reconsider the boundary.
- If tests need too many mocks, reconsider the boundary.

## Update triggers

Update this file when:

- a new module is added;
- a module responsibility changes;
- a public interface changes;
- a dependency direction changes;
- tests move to a new boundary;
- Codex struggled to locate the correct place for a change.
