# Conversation Memory

## Summary

Conversation context should not depend on a single chat surface. Important context must be written into workspace memory so it survives across Telegram, webchat, and future channels.

## Current decision

Use multiple files instead of one giant log or table:

- daily notes for chronological capture
- topic files for durable context by subject
- channel files for channel-specific notes
- `MEMORY.md` for long-term curated memory

## Why

- Prevent losing useful context when switching channels
- Keep topics encapsulated instead of mixing unrelated discussions
- Make retrieval easier when the needed context is about a specific project or issue

## Operating rule

When a conversation produces one of these, write it down in the relevant topic file:

- decision
- preference
- command worth reusing
- pending task
- important explanation or constraint

Record the event in the daily note the same day.

## Pending

- Apply this structure consistently in future conversations
- Add or split topic files as subjects become distinct enough to deserve their own file
