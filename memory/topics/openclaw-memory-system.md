# OpenClaw Memory System

## Summary

Structured memory layout for preserving useful context across channels.

## Layout

- `MEMORY.md` — long-term curated memory
- `memory/daily/YYYY-MM-DD.md` — daily chronological notes
- `memory/topics/*.md` — context grouped by project, issue, or subject
- `memory/channels/*.md` — per-channel operational notes
- `memory/index.md` — index and conventions

## Capture policy

### Daily notes

Use for:

- what happened today
- raw observations
- links between conversations and later decisions

### Topic notes

Use for:

- stable context
- decisions
- commands worth reusing
- next actions
- constraints

### Channel notes

Use for:

- channel-specific behavior
- technical limitations
- routing quirks

Do not use channel files as full conversation transcripts unless there is a clear operational need.

## Maintenance rule

If a topic grows large or mixes unrelated concerns, split it into more specific topic files and update `memory/index.md`.
