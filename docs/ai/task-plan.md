# Task Plan

Use this file for the current implementation plan. Keep it short and update it as the
work changes.

## Goal

What are we trying to change?

## Shared understanding

What decisions have already been made with the user?

## Assumptions

What is assumed but not yet proven?

## Implementation steps

1. 
2. 
3. 

## Feedback loop

Focused checks:

```bash
# Add the smallest useful checks here.
```

Full checks:

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

## Design notes

What module boundaries or interfaces are affected?

## Risks

What could break or become harder to change?

## Completion notes

What changed, what passed, and what remains?
