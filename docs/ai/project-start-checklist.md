# Project Start Checklist for Codex

Use this checklist whenever a new software project is created from this template.

## 1. Establish the design concept

Do not start with implementation. First create shared understanding.

Ask the user:

- What problem are we solving?
- Who is the primary user?
- What is explicitly out of scope?
- What are the core user flows?
- What data is sensitive?
- What must be secure from day one?
- What can be simple in version 1?
- What integrations are required?
- What should fail closed?
- What would make the first version successful?

Output:

- `docs/ai/project-charter.md`
- `docs/ai/task-plan.md`

## 2. Build the ubiquitous language

Create `docs/ai/ubiquitous-language.md` before naming important code concepts.

For each term, capture:

- term;
- meaning;
- example;
- where it appears in code;
- forbidden synonyms;
- open questions.

Use these terms in code, tests, migrations, routes, configuration, and docs.

## 3. Draw the first architecture map

Create `docs/ai/architecture-map.md` before major implementation.

Capture:

- module name;
- responsibility;
- public interface;
- hidden complexity;
- dependencies;
- tests that protect it;
- risk level.

Prefer deep modules with simple interfaces.

## 4. Choose the first feedback loop

Before coding, identify which checks prove the change works.

Use the smallest useful loop first:

```bash
uv run pytest tests/path/to/test_file.py
uv run mypy app tests
uv run ruff check app tests
```

Then run the full loop before completion:

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

## 5. Implement in small steps

For each change:

1. Write or update a test.
2. Run the focused test and confirm it fails for the expected reason.
3. Implement the smallest useful change.
4. Run the focused test again.
5. Refactor the design if the interface became worse.
6. Update docs when terminology, architecture, or behavior changed.
7. Run the broader verification loop.

## 6. Review the design before finishing

Ask:

- Did this change make the codebase easier to change?
- Did it create a shallow module or unnecessary wrapper?
- Did it duplicate a domain concept?
- Did it introduce a new term without adding it to the ubiquitous language?
- Did it weaken an interface?
- Did it add hidden coupling?
- Can a new Codex session understand where the next change belongs?

## 7. Completion response format

When the agent finishes, report:

- what changed;
- what files changed;
- what checks passed;
- what checks were not run and why;
- what design risk remains;
- what the next useful step is.
