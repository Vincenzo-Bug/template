---
name: tdd
description: Test-driven development. Use when the user wants to build features or fix bugs test-first, mentions "red-green-refactor", or wants integration tests.
---
# Test-Driven Development

TDD is the red → green loop. Consult this skill before and during every cycle.

When exploring the codebase, read `CONTEXT.md` if it exists and respect ADRs.

## What a good test is

Tests verify behavior through public interfaces, not implementation details. A good test reads like a specification, survives refactors, and describes what the caller observes.

See [tests.md](tests.md) for examples and [mocking.md](mocking.md) for mocking guidelines.

## Seams — where tests go

A **seam** is the public boundary tested without reaching inside. Tests live at seams, never against internals. Agree the seams before writing tests and test the highest useful seam.

## Anti-patterns

- **Implementation-coupled** — mocking internal collaborators, testing private methods, or verifying through a side channel.
- **Tautological** — recomputing the expected value using the same implementation logic.
- **Horizontal slicing** — writing all tests first and all implementation second.

## Rules of the loop

- **Red before green.** Write the failing test first, then only enough code to pass it.
- **One slice at a time.** One seam, one test, one minimal implementation per cycle.
- **Refactoring is not part of the loop.** Do it during review after the behavior is green.
