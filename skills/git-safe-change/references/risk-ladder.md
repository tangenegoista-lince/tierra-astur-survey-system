# Risk Ladder

Use this to classify the change before editing.

## Low risk

Examples:
- wording changes
- documentation cleanup
- isolated template updates
- local notes with no runtime effect

Default posture:
- proceed carefully
- keep diff narrow
- basic validation is enough

## Medium risk

Examples:
- non-critical scripts
- bounded config changes
- logic edits with limited blast radius
- changes to a skill that matters but is easy to recover

Default posture:
- inspect current state first
- make minimal edits
- run targeted validation
- commit carefully

## High risk

Examples:
- critical OpenClaw config
- services or startup/runtime scripts
- important operational skills
- changes that could break working flows
- changes that are difficult to reverse from memory

Default posture:
- strongly consider pre-change backup
- make the smallest viable change
- validate explicitly
- document what changed

## Simple rule

If failure would cost significant time, break current operations, or make recovery uncertain, treat it as high risk.
