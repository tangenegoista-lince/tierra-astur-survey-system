---
name: git-safe-change
description: Make code or workspace changes carefully, with explicit risk assessment, minimal diffs, validation, and clean commits. Use when editing files in a repository or managed workspace, especially when the change could break working behavior, affect important skills/configuration, or requires disciplined before/after checks. Decide whether a pre-change backup is warranted, prefer the smallest effective change, validate the result, and close with a descriptive commit when edits are made.
---

# Git Safe Change

Make changes without being reckless.

This skill is for disciplined editing work where the change itself is not the whole job. The full job is:
- understand the scope
- assess risk
- make the smallest useful change
- validate what changed
- leave a clean commit trail

## Core workflow

1. **Understand the change surface**
   Identify:
   - what files are involved
   - whether they are config, code, skills, scripts, or docs
   - whether failure would be annoying, disruptive, or dangerous

2. **Assess risk before editing**
   Classify the change:
   - low risk: isolated docs or clearly local changes
   - medium risk: logic/config changes with limited blast radius
   - high risk: critical config, services, skills relied on operationally, or anything hard to recover quickly

3. **Decide if backup is needed**
   If the change is high risk or touches working operational state, strongly consider `pre-change-backup` before proceeding.
   Do not overuse backup for trivial edits.

4. **Inspect current repo state**
   Before editing, check the working tree so you do not trample unrelated changes.
   Use git status and keep awareness of what is already dirty.

5. **Prefer the smallest effective diff**
   - avoid unrelated cleanup unless it materially helps
   - avoid large rewrites when a precise edit will do
   - preserve surrounding behavior unless the task requires otherwise

6. **Validate after changing**
   Validation should match the change:
   - docs/template change → structural sanity check
   - skill change → package or validate the skill
   - config change → relevant status/health check
   - code/script change → targeted command or test if available

7. **Review the result before committing**
   Check:
   - does the diff match the intent?
   - is there collateral damage?
   - was validation actually run?

8. **Commit cleanly**
   If you changed files in the workspace, make a descriptive commit.
   The commit should describe the actual change, not just “update files”.

## Practical rules

### Do not stomp on unrelated work
If the repository is already dirty, stay narrowly scoped and avoid sweeping adds unless the user asked for them.

### Minimalism beats cleverness
Choose the smallest change that solves the problem.

### Validation is part of the change
A change without validation is only half done.

### Commit only what you mean
Review what is staged. Avoid accidentally bundling unrelated files.

### Explain risk honestly
If a change is risky, say so before proceeding.

## Common playbooks

### Skill edit
- inspect the skill structure
- make focused edits
- package/validate the skill
- commit only the intended skill files

### OpenClaw-related change
- assess whether backup is warranted
- make minimal config or skill edits
- run relevant OpenClaw validation/status checks
- commit clearly

### Document/report change
- keep the diff narrow
- check formatting or generated structure if relevant
- commit with a message tied to the document purpose

## What good looks like

A good Git Safe Change result should:
- reduce avoidable risk
- produce a small, understandable diff
- include some real validation
- leave a clean commit history

## References

- `references/risk-ladder.md` — how to think about low/medium/high change risk
- `references/change-checklist.md` — before/during/after checklist
- `templates/change-note.md` — compact record of change, validation, and risk
