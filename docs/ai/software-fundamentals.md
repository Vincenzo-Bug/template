# Software Fundamentals for AI-Assisted Projects

This document converts the keynote transcript into reusable project rules for AI coding
agents. The goal is not to prevent AI from writing code. The goal is to make the
codebase easier for humans and agents to understand, verify, and change.

## Thesis

Software fundamentals matter more with AI, not less. A good codebase lets AI move fast
because the system is understandable and the feedback loops are strong. A bad codebase
makes AI output worse over time because each change increases complexity.

Do not assume that generated code is cheap. Generated code still creates maintenance
cost, design cost, review cost, security cost, and future-change cost.

## Failure mode 1: the AI did not build what was intended

Cause: the human and the AI did not share a design concept.

Rule:

- Before implementation, establish a shared understanding.
- Ask questions until the product goal, constraints, user flows, edge cases, and
  tradeoffs are clear.
- Do not treat the first written spec as complete.
- Convert the conversation into a product requirements document, issue list, or task
  plan only after the important decisions are resolved.

Reusable prompt:

```text
Interview me relentlessly about every aspect of this plan until we reach a shared
understanding. Walk down each branch of the design tree, resolving dependencies between
decisions one by one. Do not produce an implementation plan until the design concept is
clear.
```

## Failure mode 2: the AI is too verbose or uses the wrong concepts

Cause: the project lacks a shared language.

Rule:

- Maintain a ubiquitous language document.
- Use the same terms in requirements, code, tests, docs, database names, route names,
  and prompts.
- When the AI introduces a new term, check whether it matches the domain language.
- If two names mean the same thing, choose one.
- If one name means two different things, split it.

Project file:

- `docs/ai/ubiquitous-language.md`

## Failure mode 3: the code compiles but does not work

Cause: feedback loops are too weak or too slow.

Rule:

- The rate of feedback is the speed limit.
- Make small changes and verify them immediately.
- Use static types, automated tests, linting, formatting, and runtime checks.
- Give the agent access to the right feedback loop for the layer being changed.
- Do not allow the agent to write a large implementation before checking it.

For this Python template, the feedback loop is:

```bash
uv run black --check .
uv run ruff check .
uv run mypy app tests
uv run pytest
uv run bandit -c pyproject.toml -r app
uv run pip-audit
uv run mkdocs build --strict
```

## Failure mode 4: tests are hard to write

Cause: the codebase is not testable.

Rule:

- Prefer test-driven development for new behavior.
- Write the failing test first.
- Implement the smallest change that passes the test.
- Refactor after the behavior is protected.
- Test through stable interfaces rather than unstable internals.

Testing questions the agent must answer before writing tests:

- What behavior matters?
- What is the smallest useful unit to test?
- What should be mocked, and what should remain real?
- What would make this test flaky?
- Which public interface should the test use?

## Failure mode 5: the codebase becomes shallow and scattered

Cause: the agent creates many tiny modules with complex dependency paths.

Rule:

- Prefer deep modules: substantial behavior hidden behind simple interfaces.
- Avoid shallow modules: tiny wrappers with complicated interfaces.
- Design the public interface carefully.
- Let implementation details live behind the interface.
- When the agent struggles to find where to change code, improve the architecture map.

Good module design asks:

- What complexity can this module hide?
- What public interface should callers use?
- What should be impossible to access from outside?
- How can the interface make tests simple?

## Failure mode 6: the human cannot keep up

Cause: the system requires too much context in working memory.

Rule:

- Use module boundaries as cognitive boundaries.
- Review interfaces more carefully than internals for low-risk modules.
- For high-risk areas such as payments, auth, privacy, safety, or migrations, review
  both interface and implementation.
- Keep `docs/ai/architecture-map.md` current enough that a new agent can orient itself
  without rediscovering the entire codebase.

## Strategic role of the human

AI can be the tactical programmer. The human must remain the strategist.

The human is responsible for:

- product direction;
- design tradeoffs;
- domain language;
- architecture boundaries;
- risk tolerance;
- final acceptance.

The agent is responsible for:

- asking when the design concept is unclear;
- implementing small verified changes;
- preserving the ubiquitous language;
- strengthening feedback loops;
- leaving the codebase easier to change than before.
