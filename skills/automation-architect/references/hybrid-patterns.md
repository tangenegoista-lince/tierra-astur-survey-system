# Hybrid Patterns

## 1. Intake in n8n or Make, judgment in OpenClaw

Use when a workflow starts from an external trigger but needs interpretation, prioritization, summarization, or human-style communication.

## 2. OpenClaw as front door, workflow engine as back office

Use when the human asks conversationally for work that ultimately needs integrations, records, or multi-step execution elsewhere.

## 3. Workflow engine plus helper scripts

Use when the flow is mostly orchestration, but one or two steps need deterministic code.

## 4. OpenClaw-native light automation

Use when timing and human context matter more than heavy integrations:
- reminders
- heartbeat-like checks
- periodic summaries
- follow-ups

## 5. Split operational owner from communication owner

A useful pattern is:
- n8n/Make owns execution state
- OpenClaw owns messaging, explanation, reminders, and user-facing summaries
