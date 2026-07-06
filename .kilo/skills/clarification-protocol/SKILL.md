---
name: clarification-protocol
description: >
  When and how to use `AskUserQuestion`. Rule: **never guess on substance, never ask about trivia.**

---

## Ask When

- Two documents contradict
- A referenced entity / page / endpoint is undefined
- Mode B description doesn't map to any document
- Validator returns an error you can't resolve
- Phase priority is genuinely conflicted
- A new feature's boundary is unclear
- Archive reactivation needed

## Don't Ask When

- The answer is in the documents — read them
- It's an implementation choice — that's the coding system's problem
- It's stylistic with an obvious default

## Format

- One question per topic; batch only closely related yes/nos
- 2–4 mutually exclusive options
- Short labels (mobile-friendly)
- Cite the source

## Good

```
"PRD §4.5 lists 'social login' as MVP, but SDD has no auth_social module. Which is correct?"
options:
  - "MVP — plan SDD work for it"
  - "Post-MVP — move to Phase 3"
  - "Drop entirely"
```

## Bad

```
"How should I plan auth?"   # too vague
options:
  - "However you think"
  - "Use best practices"
```

## Batch Limit

Max 3 questions in one call. If you have more, ask the 3 most blocking; loop.

## After Asking

Don't re-ask. Treat the answer as authoritative for this session. Note in `changelog.md` under "Decisions" so future runs don't re-litigate.
