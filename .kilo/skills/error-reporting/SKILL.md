---
name: error-reporting
description: >
  Used by `plan-validator`. Format errors usefully for the orchestrator.

---

## Error Object

```json
{
  "check": "D.Small",
  "task": "T-022",
  "issue": "estimated_hours=40 exceeds 24h limit",
  "remediation": "Split T-022 ('Implement billing module'). Consider per-endpoint or per-sub-feature split."
}
```

For plan-level issues: `tasks: ["T-018", "T-031", "T-042"]` instead of single `task`.

## Actionable Remediation

Bad: "Split this task"
Good: "Split T-022 ('Implement billing module'). One task per endpoint described in `sdd/billing.md`, or one task per sub-feature (subscription / invoicing / receipts)."

The orchestrator either acts on the remediation directly or escalates to the user via `AskUserQuestion`.

## Grouping Related Errors

If 12 tasks share the same issue, group them into one entry:

```json
{
  "check": "E.Coding-Agent Usability",
  "tasks": ["T-005", "T-007", "T-009", ...],
  "issue": "12 tasks have requirements_to_read entries without 'reason' field",
  "remediation": "Re-dispatch the affected analyzers with note: 'every requirements_to_read entry must include reason'."
}
```

## Severity Order

Sort worst-first:

1. Cycles
2. Phase-order violations
3. Orphan dependencies / undefined contracts
4. Oversized tasks
5. Missing required fields
6. Targetedness failures
7. Other INVEST violations

## Stats Block

Always include, even on failure:

```json
{
  "stats": {
    "total_tasks": 47,
    "errors": 14,
    "warnings": 23,
    "passing_rules": ["A.Structural", "B.Graph", "C.Phase"],
    "failing_rules": ["D.Small", "E.Targeted"]
  }
}
```
