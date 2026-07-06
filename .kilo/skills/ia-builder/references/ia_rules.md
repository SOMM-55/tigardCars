# IA Rules & Heuristics

Detailed rules and heuristics the agent must apply when building any IA.

---

## Structural Rules

### Rule 1 — Task-Oriented Architecture
IA must be shaped by user tasks, not database tables or backend service boundaries.

❌ Wrong: `Tables > Users > Transactions`
✅ Right: `Learning > Payments > Support`

### Rule 2 — Mandatory Role Separation
Every role must have:
- Its own IA section
- Its own navigation items
- Explicit permission boundaries

Implementation: document each role separately in `02_roles_and_access.md`.

### Rule 3 — Content Before Screens
Correct thinking order:
1. Define entities and objects first
2. Define relationships between them
3. Design pages last

❌ Common mistake: starting with wireframes or page layouts.

### Rule 4 — One Source of Truth
Every entity has exactly one primary home in the IA.

Example: `Exam Result` cannot be a primary entity in Learning, Payments, AND Dashboard simultaneously. Pick one primary location; the others are references.

### Rule 5 — Maximum Depth (4 Levels)
```
Level 1: Platform
Level 2: Zone        (Student / Instructor / Public)
Level 3: Section     (Courses / Payments / Settings)  ← usually stop here
Level 4: Sub-section (Active Courses / Completed)     ← absolute maximum
Level 5+: ❌ Forbidden
```

If depth beyond 4 is needed → redesign the hierarchy. Do not just add levels.

### Rule 6 — No Ambiguous Labels
❌ Forbidden: "Other", "Misc", "General", "Various", "Stuff"
✅ Required: a precise, descriptive label

If something does not fit any group → either the grouping is wrong, or a new entity/section must be defined.

### Rule 7 — Consistent Taxonomy
One concept = one term, used identically throughout the entire system.

```
If you chose "Course" → use "Course" everywhere
Never: "Course" in one place, "Class" somewhere else
```

Maintain a Glossary in `00_ia_overview.md`.

### Rule 8 — Progressive Disclosure
- Level 1: most important sections
- Level 2: frequently used sub-sections
- Level 3–4: advanced or rarely used features

### Rule 9 — Predictability
A user should be able to guess:
- Where a feature lives
- What happens after clicking a link

Test: without seeing the UI, can a user locate "Change Password"?

### Rule 10 — Navigation ≠ IA
The navigation menu is only one component of the IA. The full IA also includes:
- Hierarchy
- Taxonomy
- Entity relationships
- Discoverability paths
- Permission model

---

## Decision Heuristics

### How many items in the top nav?
- Minimum: 3
- Ideal: 5
- Maximum: 7
- If more needed → group items or move to secondary nav

### When to ask a clarifying question?
Ask when:
- The user flow shows two conflicting paths with no clear primary
- The number or names of roles are unclear
- The public/private boundary is not defined
- Naming in the user flow is inconsistent or contradictory

Do NOT ask when:
- The answer can be inferred from the user flow
- Enough context exists to make a reasonable decision
- The question is about aesthetics, not structure

### When to create an additional output file?
- More than 5 roles → each role gets its own file under `roles/`
- Complex entity relationships → extend `03_entity_map.md` with diagrams
- Complex navigation rules → add `04b_navigation_rules.md`

---

## Pre-delivery Validation Checklist

Run this checklist before declaring the IA complete:

### Structure
- [ ] Every screen in the user flow has a corresponding entry in the sitemap
- [ ] Every entry in the sitemap is reachable from the user flow (or justified)
- [ ] No section exceeds 4 levels of depth
- [ ] No ambiguous or placeholder labels exist

### Roles
- [ ] Every role from the user flow is defined in the IA
- [ ] Every role has a clear primary path
- [ ] Permission boundaries are explicit for each role

### Entities
- [ ] Every entity has exactly one primary home
- [ ] Relationships between entities are documented
- [ ] Ownership is defined for each entity

### Consistency
- [ ] Taxonomy is identical across all output files
- [ ] All IDs are unique and follow the naming convention
- [ ] All files conform to the templates in `output_templates.md`

---

## Common Mistakes

| Mistake | Symptom | Fix |
|---------|---------|-----|
| Backend-driven IA | Labels like "Users Table", "TransactionService" | Rewrite based on user tasks |
| Navigation-only IA | Only a menu was designed | Add entity map and permissions |
| Deep nesting | More than 4 levels | Redesign the hierarchy |
| Duplicate primary entities | Same concept primary in multiple sections | Define one Source of Truth |
| Screen-first design | Started with wireframes | Go back to entity definition |
| Mixed role permissions | Role access blended or ambiguous | Build explicit access matrix |
| Inconsistent terminology | "Course" and "Class" used interchangeably | Enforce taxonomy, update glossary |