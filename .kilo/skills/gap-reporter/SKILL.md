---
name: gap-reporter
version: "6.0"
description: >
  Stage 5 (final) of the gap-analyzer pipeline. Consumes all findings files
  from Stages 2–4 plus the full Knowledge Index. Executes a Global Consistency
  Pass over the entire knowledge graph, then produces a single stakeholder-ready
  gap_report.md as a Decision Dashboard. v6 COMPLETE OUTPUT REDESIGN:
  the report is reduced to exactly 3 sections — Executive Summary, Master Gap
  Table, and Traceability Coverage. Conflict cards, propagation trees, debug
  sections, and appendixes are fully removed. Internal JSON filenames, knowledge
  graphs, and system artifacts are strictly forbidden from appearing anywhere in
  the report. Every Fix Target maps to an editable source document only.
---

# Gap Reporter v6

## Mission

Produce a single `gap_report.md` that functions as an actionable Decision
Dashboard for stakeholders. Every finding is reduced to its essential signal:
what is wrong, where to fix it, and how urgent it is. No prose explanations.
No internal artifacts. No clutter.

---

## Hard Boundaries (Absolute — No Exceptions)

**NEVER reference** any of the following in the final report:
- `index/*.json` filenames (entities.json, knowledge_graph.json, etc.)
- `contradiction_graph.json`, `fragments/`, `.tmp/` paths
- `manifest.json`, `traceability_index.json`, or any pipeline artifact
- Any detector-internal stage variable or computation artifact
- Stage 1.5 metric names (E1, E2, E3, E4, E5) — these are internal

**ALWAYS map** every finding to a permitted source document:
```
BRD → PRD → USER_FLOW → MERMAID → IA → LAYOUT → LAYOUT-BUILDER →
UI FOUNDATIONS → SDD → ORR-AUDIT → ARCHITECTURE-GROUNDING →
SDD_CLIENT → INTEGRATION-DISCOVERY → INTEGRATION-RESOLVER
```

**Fix Target column** must contain ONLY one value from the permitted list above.
**Conflict Between column** must contain ONLY pairs from the permitted list.

---

## Input

```
traceability_findings.json        (Stage 2)
graph_health_findings.json        (Stage 2)
consistency_findings.json         (Stage 3)
semantic_findings.json            (Stage 4)
index/knowledge_graph.json
index/traceability_index.json
index/extraction_quality_report.json
```

---

## Step 0 — Global Consistency Pass

Before generating the report, execute a full-project reasoning pass over
the knowledge graph to find contradictions that no local detector caught.

### Global Pass Operations

**1. Merge Duplicate Findings**
If the same contradiction was caught by multiple detectors
(e.g., a numeric conflict caught by both C1-NVC and STC), merge into a single
row in the Master Gap Table with the highest severity.
Note the merge with `[merged: C1-NVC + STC]` in the Type column.

**2. Discover Hidden Contradictions**
BFS traversal of `knowledge_graph.json` at depth up to 6:
- A `forbids` edge at depth 1 contradicting a `performs` edge at depth 4+.
- Entity lifecycle contradiction spanning 3+ chain hops.
- Implicit ordering constraint from `depends_on` chains contradicting a flow sequence.

Label new findings with detector `"GLOBAL"` and map to the nearest
permitted source document.

**3. Detect Semantic Drift**
Compare each concept across the full chain
(BRD → PRD → UFM → IA → Layout → SDD → Client).
Flag any concept with ≥ 2 core semantic changes without documented rationale.

**4. Recompute Priorities**
A finding at BRD/PRD tier that affects ≥ 3 downstream artifacts is escalated
to BLOCKER even if originally scored as MAJOR.

---

## Step 1 — Source Document Mapping

Before writing the report, remap ALL internal source_refs to permitted documents.

### Mapping Rules

| Internal `source_refs.doc` | Report Fix Target |
|---|---|
| `"brd"` | `BRD` |
| `"prd"` | `PRD` |
| `"user_flow_map"` | `USER_FLOW` |
| `"mermaid"` | `MERMAID` |
| `"IA"` | `IA` |
| `"layout"` | `LAYOUT` |
| `"layout-builder"` | `LAYOUT-BUILDER` |
| `"ui_foundations"` | `UI FOUNDATIONS` |
| `"sdd"` | `SDD` |
| `"orr-audit"` | `ORR-AUDIT` |
| `"architecture-grounding"` | `ARCHITECTURE-GROUNDING` |
| `"sdd_client"` | `SDD_CLIENT` |
| `"integration-discovery"` | `INTEGRATION-DISCOVERY` |
| `"integration-resolver"` | `INTEGRATION-RESOLVER` |
| `"permissions"` (index) | Map via traceability_index to originating BRD or PRD |
| `"entities"` (index) | Map via traceability_index to originating PRD or BRD |
| Any `index/*.json` | Resolve to original source doc via traceability_index |

**If a finding has no mappable source document:**
Use the nearest logical tier based on detector type:
- Graph health findings (B-series) → map to the tier where the node was first defined.
- Global findings → map to the lowest-tier document involved in the contradiction.

---

## Step 2 — Priority Computation

Assign final priority to every finding:

| Priority | Label | Criteria |
|---|---|---|
| P1 | BLOCKER | Severity = BLOCKER OR (MAJOR AND ≥ 3 downstream artifacts affected) |
| P2 | MAJOR | Severity = MAJOR (any count of downstream) |
| P3 | MINOR | Severity = MINOR |

**Escalation rule:** Two or more MINOR findings on the same concept in the
same tier → escalate both to P2.

**De-escalation rule:** A B6-ALIAS-SUSPECT finding is always P3 (advisory).
An E4 or E5 finding surfaced as a gap is always P3.

---

## Step 3 — Generate Report (3 Sections Only)

The final report has **exactly 3 sections**. No other sections are permitted.

---

### SECTION 1: Executive Summary

```markdown
# Gap Analysis Report — [Project Name]
_Generated: [timestamp]_

---

## Section 1: Executive Summary

**Verdict:** NO-GO ⛔ / GO-WITH-WARNINGS ⚠️ / GO ✅

| Severity | Count |
|----------|-------|
| 🔴 BLOCKER | N |
| 🟡 MAJOR | N |
| ⚪ MINOR | N |
| **Total** | **N** |

**Verdict logic:**
- **NO-GO:** ≥ 1 BLOCKER finding.
- **GO-WITH-WARNINGS:** 0 BLOCKERs AND ≥ 1 MAJOR finding.
- **GO:** 0 BLOCKERs AND 0 MAJOR findings.

**Top 5 Issues Requiring Immediate Action:**

1. [1-sentence description] — Fix in: [Fix Target] — Impact: [N downstream artifacts]
2. [1-sentence description] — Fix in: [Fix Target] — Impact: [N downstream artifacts]
3. [1-sentence description] — Fix in: [Fix Target] — Impact: [N downstream artifacts]
4. [1-sentence description] — Fix in: [Fix Target] — Impact: [N downstream artifacts]
5. [1-sentence description] — Fix in: [Fix Target] — Impact: [N downstream artifacts]
```

**Rules for Section 1:**
- Verdict is a single word: `NO-GO`, `GO-WITH-WARNINGS`, or `GO`.
- Top issues list: exactly 5 items (or fewer if total findings < 5).
- Each issue: max 1 sentence. No explanations.
- No tables other than the count table.
- No references to internal files or detector codes.

---

### SECTION 2: Master Gap Table

This is the core of the report. Every finding is a row. Rows are independent
and scannable. No prose. No cards. No trees.

```markdown
## Section 2: Master Gap Table

| ID | Priority | Type | Description | Conflict Between | Fix Target | Impact | Confidence |
|----|----------|------|-------------|-----------------|------------|--------|------------|
| G-001 | 🔴 P1 | Value Conflict | Contract amount ceiling is 500M in BRD but 200M in PRD — a 300M discrepancy on a financial constraint. | BRD vs PRD | PRD | High (4 downstream) | 0.99 |
| G-002 | 🔴 P1 | Logic Conflict | ApproveContract action is granted to Advisor role in PRD but explicitly forbidden by BRD. | BRD vs PRD | PRD | High (3 downstream) | 0.95 |
| G-003 | 🔴 P1 | Dead Rule | InvoiceAmountValidation rule can never fire — condition requires amount > 10000 AND amount < 5000 simultaneously. | - | PRD | Medium (2 downstream) | 0.98 |
| G-004 | 🟡 P2 | Chain Break | ContractApproval requirement has no User Flow step — approval behavior is unspecified in the flow. | - | USER_FLOW | Medium (2 downstream) | 0.88 |
| G-005 | 🟡 P2 | Dead-End State | PAYMENT_FAILED state has 3 inbound transitions but no exit path and is not marked terminal. | - | PRD | High (3 downstream) | 0.92 |
| G-006 | 🟡 P2 | Orphan Event | ContractExpired event is produced but no consumer is defined — downstream effects are unhandled. | - | PRD | Medium (2 downstream) | 0.87 |
| G-007 | 🟡 P2 | Coverage Gap | Contract approval decision table has no rule for role=Analyst — results in undefined behavior. | - | BRD | High (4 downstream) | 0.90 |
| G-008 | 🟡 P2 | Schema Conflict | Contract.amount typed as decimal (PRD) but integer (SDD) — would cause precision loss on fractional amounts. | PRD vs SDD | SDD | Medium (2 downstream) | 0.95 |
| G-009 | 🟡 P2 | Enum Conflict | contract_status has 6 values in PRD but only 4 in SDD — CANCELLED and EXPIRED states are unhandled at API level. | PRD vs SDD | SDD | High (3 downstream) | 0.93 |
| G-010 | ⚪ P3 | Alias Suspect | "Customer" (BRD) and "Client" (PRD) may refer to the same role — requires human review to confirm or separate. | - | PRD | Low (advisory) | 0.82 |
```

#### Column Definitions

| Column | Rules |
|---|---|
| **ID** | Sequential: G-001, G-002, ... |
| **Priority** | 🔴 P1 (BLOCKER), 🟡 P2 (MAJOR), ⚪ P3 (MINOR) |
| **Type** | Human-readable category — see Type Vocabulary below |
| **Description** | 1–2 clear sentences. No internal filenames. No detector codes. |
| **Conflict Between** | Only if two permitted documents truly conflict (e.g., `BRD vs PRD`). Otherwise `-`. |
| **Fix Target** | EXACTLY ONE permitted document name. Never a JSON file. |
| **Impact** | `High (N downstream)` / `Medium (N downstream)` / `Low (advisory)` |
| **Confidence** | 0.00–1.00 from detector. Apply Stage 1.5 modifier if applicable. |

#### Type Vocabulary

Use ONLY these human-readable type names in the Type column:

| Internal Detector | Report Type Label |
|---|---|
| C1-NVC | Value Conflict |
| C2-TUC | Time Conflict |
| C3-FSC | Schema Conflict |
| C4-ENC | Enum Conflict |
| C5-FMTC | Format Conflict |
| C6-AIC | Aggregation Conflict |
| C7-RDC | Duplicate Requirement |
| C8-CRD | Constraint Drift |
| C9-DIC | Dataflow Conflict |
| D1-PLC | Logic Conflict |
| D2-DRC | Dead Rule |
| D3-CGC | Coverage Gap |
| D4-ORC | Rule Overlap |
| D5-SUC | Subsumed Rule |
| D6-RGC | Responsibility Gap |
| D7-SLC | SLA Gap |
| D8-NSC | Missing Negative Case |
| D9-PCC | Precondition Break |
| B1-GRAPH-CYCLE | Dependency Cycle |
| B2-GRAPH-DEADEND | Dead-End State |
| B3-GRAPH-UNREACHABLE | Unreachable Node |
| B4-GRAPH-ORPHAN-EVENT | Orphan Event |
| B5-GRAPH-EDGE-CONFLICT | Edge Conflict |
| B6-ALIAS-SUSPECT | Alias Suspect |
| B7-GRAPH-RGAP | Orphan Action |
| B8-GRAPH-DFLOW | Data Flow Mismatch |
| TRC-1 | Chain Break |
| TRC-2 | Orphan Artifact |
| TRC-MULTIHOP | Multi-Hop Conflict |
| STC | Type Mismatch |
| PC | Permission Conflict |
| IC | Implicit Conflict |
| BRM | Missing Rule |
| VDG | Version Drift |
| OQ | Open Question |
| CMS | Concurrency Gap |
| CRG | Conflict Strategy Gap |
| MDC | Missing Concept |
| MSC | Missing Screen |
| MPC | Missing Permission |
| MPH | Missing Phase |
| MFC | Flow Break |
| GLOBAL | Cross-Doc Conflict |

**NEVER write a detector code (e.g., C1-NVC, D3-CGC) in the table.**
Always write the human-readable label.

#### Master Gap Table Ordering

1. Sort by Priority (P1 first, then P2, then P3).
2. Within same priority, sort by Impact descending (High → Medium → Low).
3. Within same impact, sort by Confidence descending.

---

### SECTION 3: Traceability Coverage

A summary of how completely the source document chain is covered.

```markdown
## Section 3: Traceability Coverage

| Tier | Coverage | Weighted Score | Status |
|------|----------|---------------|--------|
| BRD | 100% | 1.00 | ✅ Fully covered |
| PRD | 100% | 0.95 | ✅ Fully covered |
| USER_FLOW | 79% | 0.67 | ⚠️ Partially covered |
| IA | 64% | 0.88 | ⚠️ Partially covered |
| LAYOUT | 50% | 0.55 | ❌ Insufficient coverage |
| SDD | 33% | 0.40 | ❌ Insufficient coverage |
| SDD_CLIENT | 0% | 0.00 | ❌ Not covered |
```

**Status thresholds:**
- ✅ Fully covered: weighted score ≥ 0.90
- ⚠️ Partially covered: 0.50 ≤ weighted score < 0.90
- ❌ Insufficient: weighted score < 0.50

**Rules for Section 3:**
- Exactly 7 rows (one per tier in the permitted chain).
- Omit SDD_CLIENT row only if no SDD_CLIENT documents exist.
- No additional columns, prose, or explanatory notes.

---

## Step 4 — Final Validation Before Write

Before writing `gap_report.md`, run these checks:

1. **Internal filename check:** Search the entire draft for any occurrence of
   `.json`, `/index/`, `knowledge_graph`, `contradiction_graph`, `fragments/`,
   `manifest`, `traceability_index`. If found → remove and remap.

2. **Fix Target validation:** Every value in the Fix Target column must be
   exactly one of the 14 permitted document names. No file paths. No section
   references. No detector codes.

3. **Conflict Between validation:** Every value must be `X vs Y` where both
   X and Y are permitted document names, or `-`.

4. **Type label validation:** Every Type value must be from the Type Vocabulary
   table. No detector codes (C1-NVC, D3-CGC, etc.) allowed.

5. **Description validation:** Descriptions must not contain:
   - JSON filenames or paths
   - Detector codes (C1-NVC, etc.)
   - Internal stage variables
   - Any path starting with `index/`, `.nitro/`, or `steering/`

6. **Section count check:** Report must have EXACTLY 3 sections.
   No Appendix. No Debug section. No Conflict Cards. No Propagation Trees.

If any check fails → fix the violation before writing.

---

## Step 5 — Output

Write exactly one file: `gap_report.md`

```markdown
# Gap Analysis Report — [Project Name]
_Generated: [timestamp] | Pipeline: gap-analyzer v6 | Mode: production_

---

## Section 1: Executive Summary
[... content ...]

---

## Section 2: Master Gap Table
[... table ...]

---

## Section 3: Traceability Coverage
[... table ...]
```

**Format rules:**
- Markdown only. No HTML. No embedded JSON. No code blocks in production mode.
- Tables use standard GFM pipe syntax.
- No bold emphasis inside table cells (except Priority emojis).
- No headers within sections (no `###` inside a section).
- Maximum report length: **200 lines** (excluding the table). The Master Gap
  Table can be longer.

---

## Rules

- **NEVER reference** internal index files, JSON structures, knowledge graphs,
  fragment files, manifest.json, or detector codes in the production report.
- Output is **exactly 3 sections** and nothing else. No exceptions.
- Every Fix Target must point to one of the 14 permitted document names.
- Every Description must be 1–2 sentences. No technical jargon from the pipeline.
- Type column uses only the human-readable Type Vocabulary labels.
- Global Consistency Pass is mandatory — run before generating the table.
- Deduplication is mandatory — merged findings appear as a single row.
- B6-ALIAS-SUSPECT findings are always P3 and always include `(advisory)` in Impact.
- The Verdict is computed strictly: any BLOCKER → NO-GO.
- Target execution time: **< 25 seconds** for 60 findings with Global Pass.
- Fully domain-agnostic.
