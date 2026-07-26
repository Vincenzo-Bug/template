# Architecture

`app/main.py` composes the FastAPI application. The `core` package owns cross
cutting concerns such as configuration, logging, errors, and security policy.
The `domain` package remains framework-independent. Infrastructure implements
database, cache, observability, and future external adapters.

The default operational contract is deliberately small:

- `GET /health` confirms the process is live without dependency I/O.
- `GET /ready` confirms required dependencies are reachable without exposing
  internal failure details.

Use Alembic migrations for all persistent-schema changes. Keep route handlers
thin, validate input at boundaries, and make product-specific dependencies
replaceable in tests.
