---
name: research-ops
description: Research deeply and produce a structured, source-backed document. Use when the user asks for investigation in depth, competitive or technology scanning, GitHub/repo research, market or tooling analysis, pattern extraction, trend mapping, or a serious report with sources, conclusions, and recommendations. Prefer official docs and accredited software sources first, then curated community sources. Distinguish clearly between strong evidence, weak signals, and speculation.
---

# Research Ops

Run disciplined research and leave behind a useful deliverable.

The goal is not just to answer. The goal is to:
- define the question clearly
- gather evidence from the best available sources
- separate signal from noise
- synthesize findings honestly
- produce a document that is reusable later

## Core workflow

1. **Clarify the research object**
   - Identify exactly what must be learned.
   - Determine whether the user wants:
     - a quick answer
     - a deep report
     - a comparison
     - strategic recommendations
     - an applied plan for Lince/OpenClaw

2. **Choose the evidence stack**
   Use sources in this order when possible:
   - official documentation
   - official repositories
   - accredited vendor/software sources
   - respected engineering blogs or technical writeups
   - curated community collections
   - general community discussion only as weak signal

3. **Collect before concluding**
   - Do not overfit to the first source.
   - Check at least 2–3 meaningful sources for important claims when possible.
   - If one source is unofficial but interesting, label it clearly.

4. **Classify sources explicitly**
   Use these categories in the report when relevant:
   - Official
   - Accredited / vendor / primary technical source
   - Curated community source
   - Secondary or weak-signal source

5. **Extract patterns, not just facts**
   Look for:
   - repeated use cases
   - recurring workflow types
   - architecture patterns
   - emerging standards
   - operational tradeoffs
   - what appears mature vs hype-driven

6. **Write a reusable output**
   For serious research, produce a document in the workspace.
   Use `templates/research-report.md` unless there is a better fit.

7. **End with judgment**
   Do not stop at listing links.
   State:
   - what looks solid
   - what looks noisy or overhyped
   - what is actionable for the user's context
   - what should be done next

## Strong research habits

- Prefer primary evidence over commentary.
- Quote product positioning carefully; do not treat marketing as proof.
- Separate:
  - direct evidence
  - inference
  - speculation
- If access is blocked or incomplete, say so plainly.
- If a source looks viral but unofficial, keep it in the analysis as market signal, not as verified truth.

## Deliverable rules

When the task is substantial, create a document in the workspace that includes:
- title
- date
- scope
- methodology
- findings
- source classification
- conclusions
- recommendations

For applied strategy work, also include:
- what to copy
- what to adapt
- what to ignore
- what to build first

## Use local context when relevant

Before broad web research, check whether local notes or prior reports already contain useful context.
If the topic is connected to prior user work, use memory and local files where appropriate.

## Output quality bar

A good Research Ops result should:
- be traceable
- be honest about uncertainty
- save the user time later
- produce a document they can reuse or extend

## References

- `references/source-quality-rubric.md` — how to rank sources and claims
- `references/research-playbook.md` — practical sequence for deep investigation
- `templates/research-report.md` — default report structure
- `templates/applied-recommendation.md` — structure for “what to copy/adapt/build” outputs
