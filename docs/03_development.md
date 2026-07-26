# Development

Install with `uv sync --all-extras --locked`, copy `.env.example` to `.env`,
then use Docker Compose for PostgreSQL and Redis. The `migrate` Compose service
runs Alembic before the API starts.

Run formatting, lint, type checks, tests, dependency audit, and strict MkDocs
build before publishing changes. CI runs these checks and also verifies the
container stack and health endpoints.
