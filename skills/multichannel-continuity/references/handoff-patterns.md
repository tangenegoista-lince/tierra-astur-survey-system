# Handoff Patterns

Use this file for examples and decision patterns when continuing a conversation across channels.

## Core principle

A good handoff recreates the **working state** of the conversation, not the entire transcript.

Capture only:

- objective
- current status
- decisions made
- constraints
- next action

## Good recovery examples

### Example 1: explicit channel handoff

User in webchat:

> Sigue aquí lo de Telegram sobre la skill.

Good behavior:

- inspect recent Telegram-linked sessions
- pick the most recent relevant thread
- recover the current skill topic
- continue with the next concrete step

Good reply:

> Sí, sigo desde lo de Telegram: querías una skill de continuidad multicanal en modo semiautomático. Ya puedo montarla aquí.

## Example 2: implicit handoff

User says:

> Como te dije por WhatsApp, quiero que esto quede como un único canal.

Good behavior:

- treat this as a strong signal
- inspect recent WhatsApp-related sessions
- recover the latest active topic
- continue without asking the user to restate everything

## Example 3: ambiguous handoff

User says:

> Continúa desde el otro chat.

If there are two plausible recent sessions, ask one short question.

Good reply:

> Tengo dos hilos recientes que cuadran: WhatsApp sobre configuración y Telegram sobre automatizaciones. ¿Cuál continúo?

## Selection heuristics

Prefer sessions that satisfy most of these:

1. newest relevant activity
2. matching named channel from the user message
3. overlapping topic keywords
4. similar unresolved next step
5. same human / same ongoing project

## Summarization template

When reconstructing context internally, compress to something like:

- User goal:
- Current state:
- Constraints/preferences:
- Next step:

Keep it short.

## What not to do

- Do not merge multiple candidate chats just to be helpful.
- Do not quote long histories unless asked.
- Do not expose unrelated personal details found in another session.
- Do not act as if continuity is certain when it is only a guess.
