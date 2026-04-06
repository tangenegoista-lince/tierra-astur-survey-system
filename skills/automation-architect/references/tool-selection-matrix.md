# Tool Selection Matrix

Use this matrix to decide where an automation should live.

## OpenClaw

Best for:
- reminders and cron-driven check-ins
- conversational workflows
- research and synthesis
- session-aware tasks
- human-facing messages with context
- agentic tool use and judgment-heavy steps

Weaknesses:
- not the best primary layer for complex external system orchestration by itself
- not ideal as the sole owner of large integration graphs

## n8n

Best for:
- webhook/API orchestration
- branching logic
- retries and workflow robustness
- self-hosted internal process control
- system-to-system integrations

Weaknesses:
- can become hard to maintain if business process is still fuzzy
- conversational/human-quality interpretation is not its main strength

## Make

Best for:
- quick SaaS automation
- visual business workflows
- approvals, notifications, CRM/forms/docs routing
- easy-to-modify business scenarios

Weaknesses:
- very complex logic can become visually messy
- deep infrastructure or engineering-heavy flows may fit better elsewhere

## Script / custom code

Best for:
- deterministic local tasks
- transformation, validation, extraction
- narrow repeatable operations

Weaknesses:
- poor visibility if used as the entire workflow layer
- may require another orchestrator around it

## Default rule

Choose the simplest architecture that preserves:
- reliability
- clarity
- maintainability
- ownership
