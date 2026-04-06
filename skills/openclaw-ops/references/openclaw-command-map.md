# OpenClaw Command Map

Use documented commands only.

## General diagnosis

- `openclaw status` — quick diagnosis of channels and sessions
- `openclaw status --all` — broader diagnostic snapshot
- `openclaw status --deep` — runs live probes for supported channels
- `openclaw status --usage` — usage-oriented view when relevant

## Gateway

- `openclaw gateway status`
- `openclaw gateway start`
- `openclaw gateway stop`
- `openclaw gateway restart`
- `openclaw gateway health --url ...` when probing a specific gateway endpoint

## Skills

- `openclaw skills search "..."`
- `openclaw skills install <slug>`
- `openclaw skills update <slug>`
- `openclaw skills update --all`
- `openclaw skills list`
- `openclaw skills list --eligible`
- `openclaw skills info <name>`
- `openclaw skills check`

## Logs and troubleshooting

- `openclaw logs --follow` for live debugging when appropriate
- `openclaw help` if command surface is unclear

## Operational reminders

- Prefer direct status checks before guessing.
- If docs exist locally, read them before prescribing.
- Keep service lifecycle operations on the canonical gateway subcommands.
