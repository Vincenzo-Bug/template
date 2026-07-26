# Ubiquitous Language

Use this file to keep humans, Codex, documentation, tests, and source code aligned.

A term should mean the same thing everywhere. If the domain changes, update this file
before renaming or adding code.

## Terms

| Term | Meaning | Example | Code locations | Do not call it | Open questions |
| --- | --- | --- | --- | --- | --- |
| Service | The deployable application created from this template. | API service, worker service. | `app/`, `Dockerfile`, `docker-compose.yml` | app thing, backend thing | What is the real service name? |
| Dependency | External infrastructure the service needs to be ready. | PostgreSQL, Redis. | `app/api/routes/health.py`, `app/schemas/health.py` | integration, provider | Which dependencies are required in production? |
| Liveness | Whether the process is running. It must not require external infrastructure. | `GET /health` | `app/api/routes/health.py` | healthiness | None. |
| Readiness | Whether required dependencies are available enough to receive traffic. | `GET /ready` | `app/api/routes/health.py` | health, alive | Which dependencies should block readiness? |
| Settings | Typed configuration loaded at startup. | `SERVICE_DATABASE_URL` | `app/core/config.py` | config blob | What prefix replaces `SERVICE_`? |
| Module boundary | The public interface that hides internal complexity. | Database adapter interface. | Architecture map | folder, layer | Which modules are deep enough? |
| Feedback loop | A check that tells the agent whether a change is correct. | Pytest, mypy, ruff. | CI, README, AGENTS.md | validation step | Which checks are required for this project? |

## Naming rules

- Use the terms above in prompts, code, tests, migrations, API routes, docs, and issues.
- Add new terms before introducing new domain concepts.
- Do not create synonyms unless they are intentionally different concepts.
- If a term becomes ambiguous, split it into two clearer terms.
- If Codex invents a new name, compare it with this table before accepting it.

## How to update this file

1. Add the proposed term.
2. Define it in one sentence.
3. Add one concrete example.
4. Point to code or docs where it appears.
5. List forbidden synonyms.
6. Record any unresolved naming question.
