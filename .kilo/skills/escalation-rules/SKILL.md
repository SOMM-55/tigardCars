---
name: escalation-rules
description: >
  Used by `incremental-planner`. When Mode B isn't appropriate, escalate to Mode A.

---

## Escalate When

### 1. Scope too broad

Candidate file set exceeds 15 files after narrowing.

### 2. Layers too widespread

Files surface across >3 of the 11 documentation directories.

### 3. Foundational rewrites

- "Switched from REST to GraphQL"
- "Redesigned the entire auth model"
- "Changed data model to event-sourced"

Foundation work touches everything downstream. Mode A is safer.

### 4. Too many existing modifications

Would need to modify >10 existing tasks.

### 5. Very small existing plan

Plan has <15 tasks total. Just rebuild — Mode A is cheap for small plans.

### 6. User explicitly asks for fresh plan

Overrides heuristics.

## Output

```json
{
  "escalate_to_mode_a": true,
  "reason": "Affected files span 5 layers (prd, sdd, sdd_client, ui_patterns, design_tokens) — substantial enough to warrant full re-plan",
  "discovered_so_far": {
    "files_consulted": [...],
    "preliminary_findings": "..."
  }
}
```

The orchestrator confirms with the user before switching modes — never silent.

## Don't Escalate When

- Large but well-contained (one feature, multiple layers) — Mode B handles
- Many tasks in one layer (e.g., 8 new UI components) — Mode B handles
- Can't quickly tell — read a few files first, then decide

Escalation is for cases where Mode B would mishandle, not where it's merely working hard.

## Hybrid

If part of the delta is clean and part is too big, return both:

```json
{
  "new_tasks": [...],
  "modifications_to_existing": [...],
  "escalation_recommendation": {
    "should_escalate": true,
    "reason": "Beyond the social-login delta, the auth-flow rewrite in §4.6 affects T-018, T-019, T-031 in ways needing full re-analysis",
    "affected_existing_task_ids": ["T-018", "T-019", "T-031"]
  }
}
```

Orchestrator surfaces to user — apply the clean delta now, do Mode A for the rest later.
