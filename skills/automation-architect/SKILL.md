---
name: automation-architect
description: Decide how to structure an automation and where it should live. Use when the user wants to automate a business or internal process and the key question is whether it belongs in OpenClaw, n8n, Make, a script, or a hybrid design. Use also when comparing orchestration options, mapping responsibilities between tools, or designing robust automation with clear triggers, ownership, retries, observability, approvals, and failure handling.
---

# Automation Architect

Design automations as systems, not just flows.

This skill exists for the layer above individual tools. The goal is to decide:
- what should be automated
- what should not
- which platform should own each part
- how the pieces should interact cleanly

## Core workflow

1. **Start from the process**
   Clarify:
   - trigger
   - owner
   - inputs
   - outputs
   - side effects
   - failure cost
   - required timing
   - human approval points

2. **Decide the job shape**
   Ask what the automation really is:
   - event-driven integration
   - scheduled maintenance/checking
   - document/file pipeline
   - approval workflow
   - messaging/notification flow
   - AI-assisted analysis
   - operational control loop

3. **Choose the right execution layer**
   Use these tendencies:
   - **OpenClaw** for agentic work, conversational continuity, reminders, cron, session-aware tasks, research, synthesis, and tool-mediated operations
   - **n8n** for robust multi-step workflows, webhooks, APIs, branching logic, self-hosted control, retries, and system orchestration
   - **Make** for fast SaaS automation, highly visual cross-app business scenarios, approvals, messaging, and lightweight business ops
   - **Script/code** for narrow deterministic jobs that do not need a visual workflow tool

4. **Prefer separation of concerns**
   A good hybrid often looks like:
   - SaaS event intake in Make or n8n
   - deterministic transformation in code/script
   - agentic interpretation or communication in OpenClaw
   - status, notes, or reminders routed back through the right surface

5. **Design for operations, not just happy path**
   Define:
   - idempotency
   - retries
   - partial failure behavior
   - observability/logging
   - ownership/maintainer
   - credentials/dependencies

6. **Produce an architecture-level output**
   The result should not just say “use X”. It should explain:
   - why
   - what lives where
   - what interfaces connect the pieces
   - what the next implementation step is

## Decision heuristics

### Use OpenClaw when
- conversational context matters
- the system should message or remind a human naturally
- the task is research, synthesis, interpretation, or judgment-heavy
- cron/session tools are enough and exact external integration complexity is modest
- the workflow benefits from memory, session continuity, or agent tooling

### Use n8n when
- the process is integration-heavy
- reliability and branching matter
- webhooks/APIs/datastores are central
- self-hosted control and explicit workflow logic matter
- retries, logging, and operational robustness are important

### Use Make when
- the process is primarily SaaS-to-SaaS business automation
- speed of building matters
- visual readability for business operators matters
- modules/routers/filters are a good fit
- the logic is substantial but not too infrastructure-heavy

### Use a script when
- the task is narrow, deterministic, and local
- a full workflow tool would be overkill
- the operation is better expressed as code than as boxes and arrows

## Hybrid architecture patterns

### Pattern 1: Event → workflow engine → OpenClaw
Use when an external event should trigger a human-quality message, synthesis, or decision support.

### Pattern 2: OpenClaw → workflow engine
Use when a human asks for something conversationally, but the heavy lifting belongs in n8n/Make.

### Pattern 3: workflow engine + script
Use when orchestration is visual but one step needs deterministic transformation or validation.

### Pattern 4: OpenClaw + cron + memory
Use when the workflow is lightweight, timing-based, and conversational rather than integration-heavy.

## Anti-patterns

- forcing everything into one tool
- using an agent where deterministic code is enough
- using Make/n8n for judgment-heavy conversational work they are bad at
- putting opaque business logic into routers/filters without documentation
- skipping ownership, retries, or failure planning

## Good outputs from this skill

- tool-selection recommendation
- automation architecture note
- hybrid workflow design
- phased build plan
- decision brief on OpenClaw vs n8n vs Make vs script

## References

- `references/tool-selection-matrix.md` — how to choose the right execution layer
- `references/hybrid-patterns.md` — common split-responsibility architectures
- `templates/automation-architecture-note.md` — default output for applied recommendations
