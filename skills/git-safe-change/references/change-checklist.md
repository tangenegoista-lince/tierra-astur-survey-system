# Change Checklist

## Before
- Do I understand what is being changed?
- What is the risk level?
- Is backup warranted?
- Is the repo already dirty?
- What validation will prove success?

## During
- Am I keeping the diff as small as possible?
- Am I avoiding unrelated cleanup?
- Am I preserving behavior outside the intended scope?

## After
- Did I run validation that matches the change?
- Does the diff match the intent?
- Am I staging only the intended files?
- Is the commit message descriptive?
