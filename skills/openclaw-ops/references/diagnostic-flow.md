# Diagnostic Flow

## 1. Identify the surface

Ask internally:
- Is this about channels?
- gateway?
- sessions?
- skills?
- pairing/node connectivity?
- config?
- upgrade/maintenance?

## 2. Check docs before assumptions

Read the relevant local docs page when the issue is command or architecture specific.

## 3. Run the smallest useful probe

Start with:
- `openclaw status`

Escalate only if needed:
- `openclaw status --all`
- `openclaw status --deep`
- `openclaw gateway status`
- `openclaw skills check`

## 4. Explain the evidence plainly

Good explanation format:
- what was checked
- what the system reported
- what that likely means
- what the next step is

## 5. Change only after diagnosis

If you need to modify files or config:
- assess risk
- prefer minimal edits
- validate after the change
- commit workspace edits

## 6. Escalate responsibly

Ask before:
- destructive operations
- risky config rewrites
- external actions
- anything that would materially change exposure or credentials
