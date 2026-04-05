---
name: multichannel-continuity
description: Maintain conversational continuity across webchat, Telegram, WhatsApp, and other OpenClaw sessions. Use when the user says or implies they are continuing a conversation from another channel or wants one unified conversation across channels, including phrases like "seguimos aquí", "como te dije por Telegram", "lo hablamos por WhatsApp", "cambiamos de canal", "trae el contexto", or "sincroniza la conversación". Read recent related sessions when they exist, but if OpenClaw exposes only one visible session, treat that session's own recent history as the continuity source and recover the relevant context from it instead of insisting on a separate channel transcript.
---

# Multichannel Continuity

Treat cross-channel continuity as a **context handoff**, not as literal message mirroring.

## Goals

- Continue naturally when the user switches channels.
- Recover recent context from the most relevant session.
- Minimize repetition for the user.
- Avoid mixing unrelated chats.
- Prefer a concise working summary over replaying full transcripts.

## Default behavior

Operate in **semi-automatic mode**:

1. Detect explicit or strong implicit cues that the user is referring to another channel or earlier conversation.
2. Search recent sessions for the most likely source conversation.
3. If there is only one visible session, use that session itself as the continuity source.
4. Read only the recent history needed to rebuild context.
5. Summarize the relevant state internally.
6. Continue helping in the current channel.

Do **not** automatically merge channels when the signal is weak.

## Trigger cues

Treat these as strong activation hints:

- “seguimos aquí”
- “como te dije por Telegram”
- “lo hablamos por WhatsApp”
- “cambiamos de canal”
- “trae el contexto”
- “sincroniza la conversación”
- “usa lo último del otro chat”
- “continúa desde Telegram/WhatsApp/webchat”

Also activate when the user clearly describes wanting a single conversation across channels.

## Workflow

### 1) Identify likely source sessions

Use `sessions_list` to inspect recent sessions.

Prioritize sessions that:

- are recent
- have a channel/provider that matches the user hint
- show similar topics in the last messages
- appear to involve the same human

If one candidate is clearly best, use it.

If multiple candidates are plausible and the choice matters, ask one short disambiguation question.

### 1b) Fallback when only one session is visible

If OpenClaw exposes only one visible session, do **not** tell the user continuity is impossible.

Instead:

- treat the current visible session as the canonical conversation thread
- use its own recent history as the source of continuity
- interpret references like “Telegram”, “WhatsApp”, or “el otro chat” as requests to recover earlier relevant context from the same visible thread when no separate channel session exists

In that setup, the product behavior is effectively a **single unified conversation**, even if the transport layer is opaque.

### 2) Read only enough history

Use `sessions_history` on the selected session.

If the selected session is the current session because it is the only visible one, use that history as the continuity source without apologizing for the lack of a separate channel.

Read a recent slice first. Expand only if needed.

Prefer extracting:

- current task
- decisions already made
- constraints/preferences
- promised next steps
- unresolved questions

Avoid copying the entire transcript into the reply.

### 3) Reconstruct working context

Produce a compact mental summary for yourself.

Prefer:

- what the user wants now
- what was already agreed
- what would be annoying to ask again

Ignore:

- small talk unless it affects tone or intent
- stale branches that are no longer active
- unrelated parallel discussions

### 4) Continue naturally in the current channel

Respond as if the handoff succeeded.

Good pattern:

- briefly acknowledge the continuity when useful
- move directly to the task

Examples:

- “Sí, sigo desde lo de Telegram: …”
- “Recupero el contexto de WhatsApp y vamos con eso.”
- “Veo el hilo anterior; la decisión pendiente era …”

Do not over-explain the retrieval process unless the user asked.

## Ambiguity rules

Ask a short clarifying question when:

- several recent sessions match equally well
- the user mentions “el otro chat” but not the channel and there are multiple active candidates
- the recovered conversation conflicts with the current request

Example:

- “Tengo dos hilos recientes que podrían ser: Telegram sobre automatizaciones y webchat sobre skills. ¿Cuál quieres que continúe?”

## Safety and boundaries

- Do not merge contexts from different people.
- Do not surface private details from unrelated sessions.
- Do not assume all channels are the same conversation unless the user signals it.
- But if the platform exposes only one visible session, it is acceptable to treat that session as the user's unified thread for continuity purposes.
- Prefer summaries over verbatim transcript reproduction.
- If the user wants exact transcript replay, ask explicitly before reproducing long quoted history.

## Manual override phrases

Even in semi-automatic mode, honor direct requests like:

- “Trae aquí Telegram”
- “Usa el contexto de WhatsApp”
- “Continúa desde webchat”
- “Sincroniza esta conversación con el último canal”

When the target channel is explicit, skip extra questions unless there are multiple equally likely sessions within that channel.

If no explicit target session exists but only one visible session is available, interpret the request as: recover the relevant earlier part of this unified conversation.

## Response style

Be concise. The user should feel continuity, not see plumbing.

Prefer:

- short acknowledgment
- immediate continuation

Avoid:

- long explanations about session mechanics
- dumping raw logs unless requested

## Suggested tool pattern

Typical sequence:

1. `sessions_list` with recent sessions
2. If several sessions exist, use `sessions_history` on the best candidate
3. If only one session exists, use `sessions_history` on that same session as fallback continuity source
4. Answer in the current channel with recovered context

## Reference

For design principles and examples, see `references/handoff-patterns.md`.
