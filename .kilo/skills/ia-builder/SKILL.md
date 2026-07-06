---
name: ia-builder
description: >
  Build Information Architecture (IA) from User Flow Maps. Use this skill whenever
  the user wants to create, generate, design, or update an IA document from their
  user flow maps. Triggers include: "build IA", "create information architecture",
  "design IA from user flow", "start IA", "generate IA", or any request to convert
  or transform user flows into an IA structure. Also triggers when the user wants
  to edit or extend an existing IA. This skill handles the full workflow: reading
  user flow maps → asking clarifying questions → generating structured IA output
  files.
---

# IA Builder Skill

This skill guides the agent to build a complete, professional Information Architecture (IA) from a User Flow Map.

> **Note on file reading:** The agent's session-memory rules govern WHEN files are read (once per conversation, on the first relevant turn). This skill defines WHAT to read and HOW to process it. Never re-read a file already in your context.

---

## 1. Execution Sequence

```
Step 1 → Read user flow maps (first turn only)
Step 2 → Read existing IA (first turn only, if in edit mode)
Step 3 → Extract & analyze
Step 4 → Ask clarifying questions (only if real ambiguity remains)
Step 5 → Generate IA output files
Step 6 → Validate against checklist
Step 7 → Hand off
```

Step 1 and Step 2 happen at most ONCE per conversation. If those files were already read earlier in this conversation, skip directly to Step 3.

---

## 2. Step 1 — Read User Flow Maps (first turn only)

Fixed path:
```
.nitro/steering/user_flow_map/*.md
```

**Action (first turn only):**
```bash
ls .nitro/steering/user_flow_map/
```
Then read all `.md` files found.

**If the path does not exist or is empty:** ask the user once for the correct path, then stop and wait.

**If you have already read these files earlier in this conversation:** skip this step entirely.

---

## 3. Step 2 — Read Existing IA (edit mode, first turn only)

If the user wants to edit or extend an existing IA AND it is the first turn:

```bash
ls .nitro/steering/IA/
```

Read all existing `.md` files there.

**Skip entirely if:**
- This is a fresh build (no existing IA)
- You have already read the existing IA earlier in this conversation

---

## 4. Step 3 — Extract & Analyze

From the user flow content (already in your context), extract:

- **Entities / Objects** — User, Course, Payment, Exam, Ticket, etc.
- **Roles** — Student, Instructor, Admin, Support, etc.
- **Screens & Pages** — every view mentioned
- **Entry Points** — where each role enters the system
- **Primary vs Secondary Flows** — main paths vs alternative/error paths
- **Ambiguities** — anything unclear; these become questions in Step 4

---

## 5. Step 4 — Ask Clarifying Questions

Use the `ask_user_input` / `question` tool. Never ask in plain prose.

**Limits:**
- Maximum 3 questions per round
- Only ask if real structural ambiguity remains
- If the user flow already answers it → don't ask
- Never ask about aesthetics, colors, or styling

**Priority order:**
1. Roles & Boundaries — which roles exist, public vs private access
2. Scope — which features must appear in the IA
3. Structure preferences — depth limit, device target, language
4. Naming — preferred terminology / glossary

---

## 6. Step 5 — Generate IA Output Files

**Output path:**
```
.nitro/steering/IA/
```

**Files to produce (always all six, unless explicitly told the project is small):**

```
.nitro/steering/IA/
├── 00_ia_overview.md          # Principles and architectural decisions
├── 01_sitemap.md              # Page structure and hierarchy
├── 02_roles_and_access.md     # Roles and permission boundaries
├── 03_entity_map.md           # Entity relationships and ownership
├── 04_navigation_model.md     # Navigation model per role
└── 05_access_matrix.md        # Full feature access matrix
```

For exact format → use the templates in `references/output_templates.md`.

---

## 7. Step 6 — Validate

Run the validation checklist in `references/ia_rules.md`.
If any item fails → fix it before continuing to Step 7.

---

## 8. Step 7 — Hand Off

When all output files exist and validation passes:
1. List the files created or updated.
2. Output exactly the handoff line defined in the agent rules.
3. Stop.

---

## 9. Golden IA Rules

| Rule | Description |
|------|-------------|
| Task-Oriented | IA is shaped by user tasks, not backend/DB structure |
| Role Separation | Each role has its own IA, navigation, permission boundary |
| Max 3–4 Level Depth | Nesting beyond 4 levels is forbidden |
| No Ambiguous Labels | No "Other", "Misc", "General", "Various" |
| Consistent Taxonomy | One term, one meaning, system-wide |
| One Source of Truth | Each entity has exactly one primary home |
| Content First | Define entities before designing pages |
| Progressive Disclosure | Not everything belongs at Level 1 |

---

## 10. Forbidden Actions

❌ Building IA without reading the user flow first
❌ Re-reading files already loaded in this conversation
❌ Asking more than 3 questions per round
❌ Editing IA without first reading existing IA files (on the first turn of an edit session)
❌ Modeling IA after database tables or backend structure
❌ Treating the nav menu as the complete IA
❌ Nesting beyond 4 levels
❌ Ambiguous category labels
❌ Continuing the conversation after the handoff line

---

## 11. Reference Files

- `references/output_templates.md` — exact format for every output file
- `references/ia_rules.md` — rules, heuristics, and validation checklist