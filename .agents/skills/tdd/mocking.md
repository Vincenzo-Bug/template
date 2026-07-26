# When to Mock

Mock at **system boundaries** only:

- External APIs
- Databases (sometimes — prefer a test database)
- Time and randomness
- File system (sometimes)

Do not mock:

- Your own classes/modules
- Internal collaborators
- Anything you control

## Designing for Mockability

At system boundaries, design interfaces that are easy to mock:

1. Use dependency injection: pass external dependencies in rather than creating them internally.
2. Prefer SDK-style interfaces over generic fetchers. Create specific functions for each external operation instead of one generic function with conditional logic.

This keeps each mock focused, makes exercised operations visible, and preserves type safety at the boundary.
