---
name: improve-codebase-architecture
description: Scan a codebase for deepening opportunities, present them as a visual HTML report, then grill through whichever one you pick.
disable-model-invocation: true
---
# Improve Codebase Architecture

Surface architectural friction and propose **deepening opportunities** — refactors that turn shallow modules into deeper ones. The aim is testability and AI-navigability.

This command is informed by the project's domain model and built on a shared design vocabulary: **module**, **interface**, **depth**, **deep**, **shallow**, **seam**, **adapter**, **leverage**, and **locality**. Run `/codebase-design` for the architecture vocabulary and principles.

## Process

### 1. Explore

Scope before you scan. Focus on recently changed hot spots unless the user names a direction. Read `CONTEXT.md` and relevant ADRs first, then explore organically:

- Where does understanding one concept require bouncing between many small modules?
- Where are modules shallow — interface nearly as complex as implementation?
- Where do tightly coupled modules leak across their seams?
- Which parts are untested or hard to test through their interface?

Apply the deletion test: would deleting the suspected module concentrate complexity, or merely move it?

### 2. Present candidates as an HTML report

Write a self-contained HTML file to the OS temp directory. Use `<tmpdir>/architecture-review-<timestamp>.html`, open it for the user, and report the absolute path. Use Tailwind and Mermaid from CDNs for diagrams. Each candidate needs files, problem, solution, benefits, before/after visualisation, and recommendation strength (`Strong`, `Worth exploring`, or `Speculative`). End with a top recommendation.

Do not propose interfaces yet. Ask: "Which of these would you like to explore?"

### 3. Grilling loop

Once the user picks a candidate, run `/grilling` to walk the decision tree: constraints, dependencies, the deepened module, its seam, and surviving tests. Use `/domain-modeling` as durable terms crystallize, and offer an ADR when a rejected alternative needs recording.
