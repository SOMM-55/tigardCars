---
name: extraction-auditor
version: "1.0"
description: >
  Stage 1.5 of the gap-analyzer pipeline — NEW in v6. Runs immediately after
  Stage 1 (knowledge-extractor) and before Stage 2 (traceability-mapper).
  Measures the quality, completeness, and reliability of the extracted
  Knowledge Index. Detects coverage gaps (E1), weak source references (E2),
  semantic placeholders (E3), over/under-merge in alias resolution (E4), and
  semantically empty fragments (E5). Outputs a quality report that gates
  downstream stages: if coverage falls below 80%, emits a WARNING that
  Stage 2–5 results may be incomplete. Never reads raw source documents —
  operates exclusively on index/*.json.
---

# Extraction Auditor v1.0

## Mission

Act as a quality gatekeeper between extraction (Stage 1) and analysis
(Stages 2–5). Measure how much of the source document content was
successfully captured in the Knowledge Index, identify systematic extraction
failures, and produce a quality certification that downstream stages can
use to calibrate their confidence.

---

## Input

```
index/
├── entities.json
├── roles.json
├── requirements.json
├── business_rules.json
├── states.json
├── actions.json
├── permissions.json
├── flow_graphs.json
├── traceability_index.json   (includes inferred_concepts, alias_index)
├── field_schemas.json
├── format_specs.json
├── events.json
└── enum_registry.json
```

**Never reads raw source documents.** Operates purely on the Knowledge Index.

---

## Quality Metrics (E1–E5)

---

### E1 — Extraction Coverage Rate

**Goal:** Measure what percentage of raw source text was successfully mapped
to at least one concept record.

**Algorithm:**

1. Count total `source_ref` entries across ALL index files
   (`total_source_refs`).
2. Count unique `(doc, path, section)` triples that appear as `source_ref`
   in at least one concept record (`covered_sections`).
3. Estimate total expected sections from each document by dividing document
   word count by an average section density (default: 1 section per 150 words,
   configurable). Store as `expected_sections`.
4. Compute:
   ```
   extraction_coverage = covered_sections / expected_sections
   ```
5. Per-document coverage:
   ```
   doc_coverage[doc] = covered_sections_in_doc / expected_sections_in_doc
   ```

**Output:**
```json
{
  "metric": "E1",
  "total_source_refs": 312,
  "covered_sections": 87,
  "expected_sections": 104,
  "extraction_coverage": 0.836,
  "per_document": {
    "brd/overview.md": { "covered": 14, "expected": 16, "coverage": 0.875 },
    "prd/contracts.md": { "covered": 22, "expected": 28, "coverage": 0.786 }
  },
  "status": "WARNING",
  "threshold": 0.80,
  "note": "prd/contracts.md coverage below 80% — re-extraction recommended for §§ 5–7"
}
```

**Thresholds:**
- `≥ 0.90` → ✅ PASS
- `0.80–0.89` → ⚠️ WARNING (proceed with caution)
- `< 0.80` → ❌ FAIL (downstream results unreliable — halt or re-extract)

---

### E2 — Weak Source Reference Detection

**Goal:** Identify concepts whose `source_ref` is too vague to be actionable
(single-word section, no section at all, or generic placeholder section names).

**Weak reference patterns:**
- `section: null` or `section: ""`
- `section` is a single word without a `§` marker (e.g., `"Overview"`, `"General"`)
- `section` matches any of: `"Introduction"`, `"Summary"`, `"Background"`,
  `"Overview"`, `"General"`, `"Miscellaneous"`, `"Notes"`, `"Other"`
- `source_ref` array is empty (`[]`)
- `path` is null or empty

**Algorithm:**

For every concept record in all index files, check all `source_refs[]` entries.
If ALL source_refs for a concept are weak → flag the concept as `weak_sourced`.

```json
{
  "metric": "E2",
  "weak_sourced_concepts": [
    {
      "concept_id": "BR-0023",
      "concept_name": "PaymentRetryPolicy",
      "source_refs": [
        { "doc": "prd", "path": "prd/payments.md", "section": "Overview" }
      ],
      "weakness_reason": "section is a generic placeholder ('Overview')",
      "recommendation": "Re-extract with specific section reference (e.g., §2.3)"
    }
  ],
  "weak_count": 4,
  "total_concepts": 87,
  "weak_rate": 0.046,
  "status": "WARNING"
}
```

**Thresholds:**
- `weak_rate < 0.05` → ✅ PASS
- `0.05–0.10` → ⚠️ WARNING
- `> 0.10` → ❌ FAIL

---

### E3 — Semantic Placeholder Detection

**Goal:** Identify concepts that were extracted but carry no real semantic
content — hollow records that exist structurally but convey no meaning.

**Placeholder indicators:**

| Field | Hollow value |
|---|---|
| `name` | Single word (≤ 1 word) without a domain noun |
| `description` | null, empty, `"TBD"`, `"TODO"`, `"Placeholder"`, `"N/A"` |
| `structured_predicate.conditions` | Empty array `[]` with `confidence < 0.4` |
| `quantities[]` | Non-empty but all entries have `value: null` |
| `field_schema[]` | Non-empty but all fields have `type: null` and `nullable: null` |
| `reasoning_chain` | Length ≤ 1 with no `evidence` or `conclusion` |

**Algorithm:**

Score each concept on a hollowness scale (0 = fully substantive, 1 = fully hollow).
Flag concepts with `hollowness_score ≥ 0.6` as placeholders.

```json
{
  "metric": "E3",
  "hollow_concepts": [
    {
      "concept_id": "AC-0041",
      "concept_name": "Process",
      "hollowness_score": 0.80,
      "hollow_indicators": [
        "name is a generic single word",
        "description is null",
        "reasoning_chain has only 1 step with no evidence"
      ],
      "recommendation": "Either enrich with specific semantic content from source or remove as spurious extraction"
    }
  ],
  "hollow_count": 3,
  "total_concepts": 87,
  "hollow_rate": 0.034,
  "status": "PASS"
}
```

**Thresholds:**
- `hollow_rate < 0.03` → ✅ PASS
- `0.03–0.08` → ⚠️ WARNING
- `> 0.08` → ❌ FAIL

---

### E4 — Alias Merge Quality (Over-Merge / Under-Merge Rate)

**Goal:** Detect problematic alias merges in `traceability_index.alias_index`
where semantically distinct concepts were merged (over-merge) or synonymous
concepts were left separate (under-merge).

**Algorithm:**

**Over-merge detection:**
For each alias group `{canonical: X, aliases: [A, B, C]}`:
1. Check if any alias appears in a `forbids`, `blocks`, or `depends_on` edge
   alongside the canonical. If A forbids X, they cannot be the same concept.
2. Check if the canonical and any alias appear in the same relationship with
   different values (e.g., `Contract.amount_ceiling` in BRD = 500M, but
   `Agreement.amount_ceiling` in PRD = 200M → these are NOT the same concept).
3. Check cross-tier role definitions: if `Customer (BRD)` has permissions
   different from `Client (PRD)`, they may be distinct roles, not aliases.

**Under-merge detection:**
1. Scan all concept names for string similarity ≥ 0.85 (Levenshtein) that
   are NOT currently in the same alias group.
2. Scan for semantic co-reference patterns: concepts that appear together in
   the same sentence with linking verbs ("X is also called Y", "X, also known
   as Y", "X (or Y)").
3. Scan for prefix/suffix variants: `ContractApproval` vs `ApproveContract`
   vs `ContractApprovalProcess` — these likely refer to the same concept.

```json
{
  "metric": "E4",
  "over_merge_suspects": [
    {
      "canonical": "Contract",
      "suspect_alias": "Agreement",
      "reason": "Agreement.amount_ceiling (PRD §5.2) = 200M ≠ Contract.amount_ceiling (BRD §3.1) = 500M — semantically distinct values suggest distinct concepts",
      "recommendation": "HUMAN REVIEW — split 'Agreement' into separate concept if amount ceilings intentionally differ"
    }
  ],
  "under_merge_suspects": [
    {
      "concept_a": "ContractApproval",
      "concept_b": "ApproveContract",
      "similarity_score": 0.91,
      "co_reference_evidence": "prd/contracts.md §4: 'ApproveContract action initiates the ContractApproval process'",
      "recommendation": "HUMAN REVIEW — consider merging under canonical 'ContractApproval'"
    }
  ],
  "over_merge_count": 1,
  "under_merge_count": 2,
  "status": "WARNING",
  "note": "All merge quality findings require HUMAN REVIEW — do not auto-merge or auto-split"
}
```

**Important:** E4 findings are **advisory only**. No automatic changes are
made to `alias_index`. All E4 outputs are flagged for human review.

---

### E5 — Semantic Fragment Detection

**Goal:** Identify text fragments in source documents that generated no
semantic concept in the Knowledge Index — content that was parsed but
produced zero extraction output.

**Algorithm:**

1. During Stage 1 extraction, every processed text fragment is given an
   internal `fragment_id` and classified as either `mapped` (produced at
   least one concept record) or `unmapped` (parsed but produced nothing).
2. Stage 1.5 reads `index/.extraction_audit.json` (an internal Stage 1
   artifact written only for this purpose, never exposed in the final report).
3. Analyze unmapped fragments:
   - **Type A — Structural noise:** Page headers, footers, table borders,
     navigation elements → acceptable, do not flag.
   - **Type B — Transitional prose:** Connecting sentences with no substantive
     content ("This section describes...") → acceptable.
   - **Type C — Meaningful but missed:** Sentences containing business nouns,
     numeric claims, role names, or constraint verbs that produced no concept
     → FLAG as `missed_extraction`.

```json
{
  "metric": "E5",
  "total_fragments_processed": 1240,
  "mapped_fragments": 1087,
  "unmapped_structural": 98,
  "unmapped_transitional": 41,
  "unmapped_meaningful": 14,
  "missed_extraction_rate": 0.011,
  "missed_extractions": [
    {
      "fragment_id": "frag-0312",
      "source": { "doc": "prd", "path": "prd/payments.md", "section": "§4.1" },
      "raw_text": "Payment reversals must be initiated within 72 hours of the original transaction.",
      "missed_concepts": ["payment_reversal_window (temporal_spec)", "PaymentReversal (action or requirement)"],
      "recommendation": "Add temporal_spec: 72h (259200s) for payment reversal window; consider adding PaymentReversal to actions.json"
    }
  ],
  "status": "WARNING",
  "threshold_fail": 0.05,
  "threshold_warn": 0.02
}
```

**Thresholds:**
- `missed_extraction_rate < 0.02` → ✅ PASS
- `0.02–0.05` → ⚠️ WARNING
- `> 0.05` → ❌ FAIL

---

## Output

### File: `index/extraction_quality_report.json`

```json
{
  "stage": "1.5",
  "version": "1.0",
  "generated_at": "2024-01-15T10:05:00Z",
  "overall_status": "WARNING",
  "gate_pass": true,
  "metrics": {
    "E1": { "status": "WARNING", "extraction_coverage": 0.836 },
    "E2": { "status": "PASS",    "weak_rate": 0.046 },
    "E3": { "status": "PASS",    "hollow_rate": 0.034 },
    "E4": { "status": "WARNING", "over_merge_count": 1, "under_merge_count": 2 },
    "E5": { "status": "WARNING", "missed_extraction_rate": 0.011 }
  },
  "gate_logic": {
    "hard_fail": false,
    "hard_fail_reason": null,
    "soft_warn": true,
    "soft_warn_reasons": ["E1 coverage below 90%", "E4 merge suspects require human review", "E5 missed extractions detected"]
  },
  "downstream_confidence_modifier": 0.88,
  "recommendations": [
    "Re-extract prd/contracts.md §§5–7 (low E1 coverage)",
    "Human review of 3 alias merge suspects (E4)",
    "Add 14 missed fragments manually or trigger re-extraction (E5)"
  ],
  "detail": {
    "E1": { ... },
    "E2": { ... },
    "E3": { ... },
    "E4": { ... },
    "E5": { ... }
  }
}
```

### Gate Logic

| Condition | Action |
|---|---|
| Any metric = ❌ FAIL | Set `gate_pass: false`. Emit BLOCKER to gap_report. Downstream stages run with degraded confidence. |
| Any metric = ⚠️ WARNING | Set `gate_pass: true` with `soft_warn: true`. Downstream stages run normally but apply `downstream_confidence_modifier`. |
| All metrics = ✅ PASS | Set `gate_pass: true`. Full confidence. |

**The extraction-auditor NEVER blocks the pipeline.** Even on FAIL, downstream
stages execute — the FAIL is surfaced as a finding in the final report, not
as a pipeline halt.

---

## Rules

- Read `index/*.json` only. Never read raw source documents.
- Read `index/.extraction_audit.json` (Stage 1 internal artifact) for E5.
- Never expose `.extraction_audit.json` or any internal path in the final report.
- All E4 findings are advisory — never auto-modify `alias_index`.
- `downstream_confidence_modifier` must be applied to all confidence scores
  in Stages 2–5 when `soft_warn: true` or `gate_pass: false`.
- Write exactly one output file: `index/extraction_quality_report.json`.
- Fully domain-agnostic.
- Target execution time: **< 5 seconds**.
