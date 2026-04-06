---
name: openclaw-ops
description: Operate, diagnose, and improve OpenClaw environments safely. Use when the task involves OpenClaw behavior, CLI commands, gateway status, pairing, channels, sessions, nodes, skills, scheduling, diagnostics, configuration, upgrades, troubleshooting, or changes to an OpenClaw deployment. Consult local OpenClaw docs first, prefer direct status/health checks before guessing, and distinguish clearly between read-only diagnosis, safe internal changes, and actions that require user approval.
---

# OpenClaw Ops

Work on OpenClaw with operational discipline.

The job is to:
- check local docs first
- diagnose before prescribing
- use first-class OpenClaw commands where possible
- keep changes minimal and reversible
- document what changed
- commit workspace edits when the task modifies files

## Core workflow

1. **Start from local docs**
   Before making claims about OpenClaw behavior, commands, config, or architecture, consult local docs in `/home/openclaw/.npm-global/lib/node_modules/openclaw/docs`.

2. **Probe the real system**
   Prefer live checks over assumptions. Common first moves:
   - `openclaw status`
   - `openclaw status --all`
   - `openclaw status --deep` when channel probing matters
   - `openclaw gateway status`
   - `openclaw skills list`
   - `openclaw skills check`
   - targeted `openclaw gateway ...` commands when the issue is clearly gateway-related

3. **Classify the task**
   Decide whether the work is mainly:
   - diagnosis
   - configuration review
   - skill work
   - channel/pairing/node connectivity
   - scheduling / cron / heartbeat design
   - upgrade or maintenance
   - risky change requiring backup or approval

4. **Choose the safest path**
   - Read-only diagnosis first
   - Then minimal internal changes
   - Ask before destructive or externally impactful actions
   - If the change could break the system, strongly consider using `pre-change-backup`

5. **Use OpenClaw-native surfaces**
   Prefer first-class tools and documented CLI flows over ad-hoc shell hacks.
   Examples:
   - reminders/schedules → cron
   - session routing → sessions tools
   - ACP harness intent → sessions_spawn runtime=acp
   - health/status → `openclaw status` / gateway status

6. **Close the loop**
   If files were edited:
   - summarize what changed
   - note validation performed
   - commit the changes

## Practical rules

### Docs-first rule
If OpenClaw docs exist locally for the topic, consult them before giving operational advice.

### Status-before-theory rule
For troubleshooting, run a real status/health command before speculating.

### Use canonical commands only
Do not invent OpenClaw CLI commands. If uncertain, use `openclaw help` or the relevant docs page.

### Gateway rule
For gateway service lifecycle, use the documented commands:
- `openclaw gateway status`
- `openclaw gateway start`
- `openclaw gateway stop`
- `openclaw gateway restart`

### Change safety rule
Ask before destructive operations. Prefer reversible edits and backups for critical changes.

### Skill install rule
For skill discovery and installation, prefer `openclaw skills ...` when the task is about marketplace/local skill management.

## Common task playbooks

### Diagnose OpenClaw generally
- Read the relevant local docs page if the issue is scoped
- Run `openclaw status`
- Escalate to `openclaw status --all` or `--deep` if needed
- Interpret the output in plain language
- Recommend next actions based on evidence, not guesses

### Troubleshoot gateway
- Read gateway docs if needed
- Run `openclaw gateway status`
- If needed, check whether the problem is service-only, RPC, bind/auth, or exposure-related
- Keep auth/bind advice aligned with documented safety guardrails

### Work on skills
- Check local visible skills and health with:
  - `openclaw skills list`
  - `openclaw skills check`
- For marketplace tasks, use `openclaw skills search/install/update`
- For authoring/editing skills in the workspace, keep structure lean and package when appropriate

### Plan scheduled behavior
- Prefer cron for exact reminders and scheduled isolated work
- Prefer heartbeat batching for lightweight periodic checks that can drift
- Keep reminder text readable as a reminder when it fires

### OpenClaw config or upgrade changes
- Read docs first
- Assess risk
- If the change is critical, recommend or perform backup workflow if appropriate
- Make the smallest viable change
- Validate after the change

## What good OpenClaw Ops looks like

A good result should:
- rely on local docs and real status
- avoid made-up commands
- separate diagnosis from action
- preserve safety and reversibility
- leave the workspace cleaner and more documented than before

## References

- `references/openclaw-command-map.md` — common commands and when to use them
- `references/diagnostic-flow.md` — triage sequence for common OpenClaw issues
- `templates/ops-note.md` — compact note for documenting changes, findings, and validation
