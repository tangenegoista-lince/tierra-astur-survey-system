# Memory Index

## Purpose

Use this directory as structured, cross-channel memory.

- `daily/` stores chronological notes and raw events.
- `topics/` stores durable context grouped by subject or project.
- `channels/` stores channel-specific operational notes.

## Topics

- `topics/conversation-memory.md` — how cross-channel conversational context should be captured
- `topics/openclaw-memory-system.md` — structure and operating rules for memory files

## Channels

- `channels/telegram.md`
- `channels/webchat.md`

## Rules of thumb

- Write raw events to `daily/YYYY-MM-DD.md`.
- Write decisions, stable context, useful commands, and pending work to a topic file.
- Keep channel files focused on channel constraints or operational quirks, not full transcripts.
- Update `MEMORY.md` only for long-term, curated context worth carrying broadly.
