---
name: to-tickets
description: Break a plan, spec, or the current conversation into a set of tracer-bullet tickets, each declaring its blocking edges, published to the configured tracker — edges as text in one file per ticket locally, or native blocking links on a real tracker.
disable-model-invocation: true
---
# To Tickets

Break the work into **tickets** — tracer-bullet vertical slices, each declaring the tickets that **block** it.

The issue tracker and triage label vocabulary should have been provided to you — run `/setup-matt-pocock-skills` if not.

## Process

### 1. Gather context

Work from the conversation context. If the user passes a spec path, issue number, or URL, fetch it and read its full body and comments.

### 2. Explore the codebase (optional)

Explore the current codebase when needed. Use the project's domain glossary vocabulary and respect ADRs. Look for prefactoring opportunities that make the implementation easier.

### 3. Draft vertical slices

Each slice cuts a narrow but complete path through every relevant layer. A completed slice is demoable or verifiable on its own and fits in a single fresh context window. Give each ticket its blocking edges.

Wide refactors are the exception: use expand–contract sequencing so CI stays green while callers migrate.

### 4. Quiz the user

Present the proposed breakdown as a numbered list. For each ticket, show:

- **Title**: short descriptive name
- **Blocked by**: tickets that must complete first
- **What it delivers**: the end-to-end behaviour

Ask whether the granularity and blocking edges are correct, then iterate until the user approves.

### 5. Publish the tickets

For local files, write one file per ticket under `.scratch/<feature-slug>/issues/<NN>-<slug>.md`, numbered in dependency order. For a real issue tracker, publish one issue per ticket in dependency order and apply the `ready-for-agent` label unless instructed otherwise.

Do not close or modify a parent issue. Work the frontier: any ticket whose blockers are complete.

Each local ticket uses this shape:

```markdown
# <NN> — <Ticket title>

**What to build:** the end-to-end behaviour from the user's perspective.

**Blocked by:** the tickets that gate it, or "None — can start immediately".

**Status:** ready-for-agent

- [ ] Acceptance criterion 1
- [ ] Acceptance criterion 2
```
