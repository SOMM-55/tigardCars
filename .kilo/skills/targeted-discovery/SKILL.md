---
name: targeted-discovery
description: >
  Used by `incremental-planner`. Narrow the file set efficiently before reading.

---

## Two-Pass Discovery

### Pass 1 — Glob to inventory

```
Glob .nitro/steering/*/
```

Cheap. Learns project's documentation layout (not all 11 directories may exist).

### Pass 2 — Grep to locate

Run grep with Tier 1 keywords across `.nitro/steering/` (excluding `.nitro/steering/plans/`):

```
Grep "social login" .nitro/steering/
```

Collect unique file paths from results — your candidate file set.

If Tier 1 returned <3 hits, expand to Tier 2.

## File Set Triage

| Signal | Score |
|---|---|
| Named in user's description | 10 — must read |
| Contains Tier 1 keyword | 5 — should read |
| Contains Tier 2 only | 3 — read if layer affected |
| Contains Tier 3 only | 1 — skip unless layer narrow |

Read in score order until all affected layers are covered.

## Affected Layer Determination

A layer is "affected" if at least one file scores ≥3. Skip unaffected layers entirely.

Examples:
- Social login: likely prd, sdd, sdd_client, possibly ui_patterns — usually NOT design_tokens or layout
- New entity: sdd (data model), maybe sdd_client — usually NOT UI system
- Layout redesign: layout, ui_foundations, possibly all sdd_client pages — NOT sdd backend

## Within-File Reading

- User named section ("§4.5") → `Read` with line ranges to that section
- Grep hit specific lines → `Read` ±50 lines first; expand if needed
- Small documents (<200 lines) → reading whole is fine

## Token Budget

Rough Mode B budget: ~20k tokens of reading.

10 files × ~2k tokens average = 20k. Exceeding → narrow further or escalate.

## Skip the Existing Plan

The orchestrator gave you `outputs-index` and the existing-plan summary. Don't waste reads on `.nitro/steering/plans/tasks/*.yaml`. The archive is also off-limits unless a specific archived contract reference forces a targeted read.

## Record Files Consulted

Return the exact file list for `changelog.md`:

```json
{
  "files_consulted": [
    {"path": ".nitro/steering/prd/auth.md", "sections_read": ["§4.5"]},
    {"path": ".nitro/steering/sdd/auth.md", "sections_read": ["whole file"]}
  ]
}
```
