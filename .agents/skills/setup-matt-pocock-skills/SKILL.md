---
name: setup-matt-pocock-skills
description: Configure this repo for the engineering skills — set up its issue tracker, triage label vocabulary, and domain doc layout. Run once before first use of the other engineering skills.
disable-model-invocation: true
---
# Setup Matt Pocock's Skills

Scaffold the per-repo configuration that the engineering skills assume:

- **Issue tracker** — where issues live (GitHub by default; local Markdown is also supported)
- **Triage labels** — the strings used for the five canonical triage roles
- **Domain docs** — where `CONTEXT.md` and ADRs live, and the consumer rules for reading them

This is a prompt-driven skill, not a deterministic script. Explore, present what you found, confirm with the user, then write.

## Process

### 1. Explore

Look at the current repository. Read whatever exists; do not assume:

- `git remote -v` and `.git/config`
- root `AGENTS.md` and `CLAUDE.md`
- root `CONTEXT.md` and `CONTEXT-MAP.md`
- `docs/adr/` and `docs/agents/`
- `.scratch/`
- whether the `triage` skill is installed
- monorepo signals such as workspaces or populated package directories

### 2. Present findings and ask

Summarize what is present and missing. Then take these sections in order, one answer at a time:

**Issue tracker:** recommend GitHub when the remote points at GitHub, GitLab when it points at GitLab, or local Markdown under `.scratch/` when there is no remote. Record the choice in `docs/agents/issue-tracker.md`.

**Triage labels:** only ask this when the `triage` skill is installed. The defaults are `needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, and `wontfix`.

**Domain docs:** default to a single-context root `CONTEXT.md` plus `docs/adr/`; use a context map only for a genuine monorepo.

### 3. Confirm and edit

Show the user a draft of the `## Agent skills` block and the configuration files before writing them.

### 4. Write

If `CLAUDE.md` exists, edit it. Otherwise edit `AGENTS.md` if it exists. If neither exists, ask the user which one to create. Never create both. Add the `## Agent skills` block without overwriting surrounding user content, then write the selected configuration files under `docs/agents/` using the seed templates in this directory.

### 5. Done

Tell the user setup is complete and that `docs/agents/*.md` can be edited directly later. Re-run this skill only to switch trackers or restart setup.
