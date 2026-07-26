# Domain Docs

Engineering skills should consume the repository's domain documentation this way.

## Before exploring

- Read `CONTEXT.md` at the repository root, or `CONTEXT-MAP.md` when it exists.
- Read ADRs under `docs/adr/` that touch the area being changed.
- Proceed silently when these files do not exist; create them only when the domain-modeling workflow resolves a real term or decision.

## Default structure

```text
/
├── CONTEXT.md
├── docs/adr/
└── src/
```

Use a root `CONTEXT-MAP.md` and per-context files only for a genuine monorepo.

Use the glossary vocabulary in issue titles, refactor proposals, and tests. Flag conflicts with existing ADRs instead of silently overriding them.
