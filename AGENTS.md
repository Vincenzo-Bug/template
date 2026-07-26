# AI Agent Instructions

These instructions apply to Codex and other AI coding agents working in this repository.
They are based on the software-fundamentals workflow captured in the keynote transcript
`It Ain't Broke: Why Software Fundamentals Matter More Than Ever` by Matt Pocock.

The core thesis is simple: code is not cheap. Bad code is expensive because it makes
future AI-assisted changes harder, less reliable, and slower to verify. Treat the AI as
a tactical implementer. The human remains responsible for product direction, system
design, and acceptance.

## Non-negotiable workflow

1. Do not jump directly from a vague specification to code.
2. First reach a shared design concept with the user.
3. Ask clarifying questions until requirements, constraints, terminology, and tradeoffs
   are understood well enough to implement safely.
4. Maintain a shared language for the project in `docs/ai/ubiquitous-language.md`.
5. Make small, deliberate changes. The rate of feedback is the speed limit.
6. Prefer test-driven development for new behavior: failing test, passing code,
   refactor, then verification.
7. Design deep modules with simple interfaces. Avoid many shallow modules with complex
   dependency paths.
8. Test at stable interfaces and delegate internal implementation details only after
   the boundary is clear.
9. Invest in system design every day. Do not only solve the immediate ticket.
10. Never leave the repository in a state where formatting, linting, type checking,
    tests, or security checks fail without documenting why.

## Before implementation

Create or update these project assets when starting a new project from the template:

- `docs/ai/project-charter.md`: product goal, users, non-goals, constraints.
- `docs/ai/ubiquitous-language.md`: shared domain vocabulary.
- `docs/ai/architecture-map.md`: current modules, boundaries, and interfaces.
- `docs/ai/task-plan.md`: implementation plan and feedback loop.

For any non-trivial feature, first run the "grill me" process:

> Interview the user relentlessly about every aspect of this plan until you reach a
> shared understanding. Walk down each branch of the design tree, resolving dependent
> decisions one by one. Only produce an implementation plan after the design concept is
> shared.

## During implementation

- Keep diffs small and coherent.
- Change one concern at a time.
- Preserve existing public interfaces unless the plan explicitly changes them.
- Name modules, classes, functions, tests, and docs using the ubiquitous language.
- Avoid speculative abstractions, hidden global state, and duplicated domain concepts.
- Prefer explicit types, explicit boundaries, and explicit error handling.
- When touching a module, check whether its interface is becoming simpler or more
  complex. Simpler public interfaces are usually better.
- If the agent needs to explore the codebase for too long, pause and update the
  architecture map so the next change is easier.

## Verification

Before claiming the work is complete, run the relevant checks:

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

If a check is not relevant or cannot run in the current environment, say exactly why.

## Review standard

A change is not done just because it works once. It is done when:

- the behavior is specified in tests or documentation;
- the relevant feedback loops pass;
- the module boundary remains understandable;
- the shared language is still consistent;
- future AI agents can understand where to make the next change.
