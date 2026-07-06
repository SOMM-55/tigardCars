---
name: consistency-validator
version: "6.0"
description: >
  Stage 3 of the gap-analyzer pipeline. Reads all index/*.json files and the
  knowledge_graph.json produced by Stage 2. Performs direct value contradiction
  detection across all source documents. v5 capabilities preserved:
  STC (semantic type conflict), PC (permission conflict), IC (implicit conflict),
  BRM (missing business rule), VDG (version/phasing drift), OQ (open questions),
  CMS/CRG (concurrency/conflict strategy). v6 adds 5 new direct-value detectors
  (C1–C5): numeric value conflicts, temporal/unit conflicts, field schema
  conflicts, enum/value-set conflicts, and format/locale conflicts.
  Never reads raw source documents.
---

# Consistency Validator v6

## Mission

Find every place where two or more source documents make incompatible
factual claims about the same concept — value contradictions, type
mismatches, temporal inconsistencies, format conflicts, and missing rules.
In v6, the A1–A7 extraction data from Stage 1 provides the numerical and
structural precision needed to detect contradictions that were previously
invisible to purely semantic analysis.

---

## Input

```
index/entities.json
index/roles.json
index/requirements.json
index/business_rules.json
index/states.json
index/actions.json
index/permissions.json
index/traceability_index.json
index/flow_graphs.json
index/knowledge_graph.json       (from Stage 2)
index/field_schemas.json         [NEW v6 — from Stage 1 A3]
index/format_specs.json          [NEW v6 — from Stage 1 A4]
index/events.json                [NEW v6 — from Stage 1 A6]
index/enum_registry.json         [NEW v6 — from Stage 1 A7]
index/responsibilities.json      [NEW v7 — from Stage 1 A9]
index/extraction_quality_report.json
```

Never reads raw source documents.

---

## Preserved from v5: Existing Detectors

### STC — Semantic Type Conflict
Two documents assign incompatible types to the same concept
(e.g., BRD says Contract.status is a string, SDD says it's an integer enum).

### PC — Permission Conflict
Two documents grant conflicting access rights to the same role/action pair.

### IC — Implicit Conflict
Contradiction inferred from multi-hop reasoning across the knowledge graph
(not directly stated).

### BRM — Missing Business Rule
A situation that clearly requires a governing rule but none is defined
(e.g., what happens when payment fails? No rule exists).

### VDG — Version / Phasing Drift
The same concept is assigned to different product versions or phases across
documents (e.g., BRD says MVP, PRD says v2).

### OQ — Open Question
A `TBD`, `TODO`, or unresolved placeholder on a business-critical concept.

### CMS — Concurrency / Mutation Strategy Gap
Multiple actors can mutate the same entity concurrently with no locking or
conflict resolution strategy defined.

### CRG — Conflict Resolution Gap
Parallel flow branches converge at a join with no defined merge strategy.

---

## NEW in v6/v7: Direct Value Contradiction Detectors (C1–C9) ✨

These detectors use the quantitative extraction data from Stage 1 (A1–A9)
to find precise, numerical and structural contradictions that semantic
analysis cannot catch.

---

### C1 — NVC: Numeric Value Conflict

**Goal:** Detect cases where two or more documents assign different numeric
values to the same named concept.

**Algorithm:**

1. Build a `value_map` from `quantities[]` fields across all index files:
   ```
   key   = (concept_name, unit, operator)
   values = list of {value, source_ref, concept_id}
   ```
   Use `alias_index` to normalize concept names (so "amount ceiling" and
   "max_amount" are compared if they are aliases).

2. For each `key` with ≥ 2 entries:
   - If ALL values are equal → consistent (no finding).
   - If values differ → potential NVC.

3. NVC qualification:
   - **Direct NVC:** Same concept, same unit, same operator, different value
     (e.g., `max_retries = 3` in BRD, `max_retries = 5` in PRD).
   - **Operator NVC:** Same concept, same unit, conflicting operators
     (e.g., `amount <= 500M` in BRD, `amount <= 200M` in PRD — these define
     overlapping but different domains, making one stricter than intended).
   - **Asymmetric NVC:** Same concept, different units but same dimensionality
     after conversion (e.g., `500M BRL` vs `500,000,000 BRL`; or `3 attempts`
     vs `three` — numeric/textual mismatch).

4. Use `quantities[].unit` to detect unit-dimension mismatches:
   - `3 million` vs `3000000` → same (flag only if values differ after normalization).
   - `3 retries` vs `3 minutes` → dimensionality mismatch → escalate to C2.

**Severity:**
- BLOCKER: if the conflicting concept is in `business_rules.json` or
  `requirements.json` AND at least one source is BRD or PRD tier.
- MAJOR: any other numeric conflict.

**Output schema:**
```json
{
  "detector": "C1-NVC",
  "severity": "BLOCKER",
  "conflict_type": "direct_nvc",
  "concept": "contract_amount_ceiling",
  "values": [
    {
      "value": 500,
      "unit": "million",
      "operator": "<=",
      "source_ref": { "doc": "brd", "path": "brd/overview.md", "section": "§3.1" },
      "raw_text": "Contract amount must not exceed 500M"
    },
    {
      "value": 200,
      "unit": "million",
      "operator": "<=",
      "source_ref": { "doc": "prd", "path": "prd/contracts.md", "section": "§5.2" },
      "raw_text": "Contract amount ceiling is 200M"
    }
  ],
  "delta": {
    "absolute": 300,
    "unit": "million",
    "relative_pct": 60.0
  },
  "description": "BRD sets contract amount ceiling at 500M; PRD sets it at 200M. A 300M (60%) discrepancy between business definition and product specification.",
  "suggested_resolution": "Align by confirming the authoritative value in BRD §3.1. If 200M is the correct constraint, update BRD. If 500M is correct, update PRD.",
  "reasoning_chain": [...]
}
```

---

### C2 — TUC: Temporal / Unit Conflict

**Goal:** Detect temporal or unit conflicts after normalization — where two
documents describe the same duration or SLA with different values, or with
values that appear equivalent on the surface but differ after normalization.

**Algorithm:**

1. Build a `temporal_map` from `temporal_specs[]` across all index files:
   ```
   key   = concept_name (normalized via alias_index)
   values = list of {normalized_seconds, raw_text, source_ref, business_day_adjusted}
   ```

2. For each concept with ≥ 2 temporal entries:
   a. **Direct TUC:** `normalized_seconds` values differ.
      Example: `"24 hours"` (86400s) vs `"1 business day"` (28800s) for the
      same timeout — appear similar semantically but differ by 3× after
      normalization.
   b. **Business-day ambiguity TUC:** One source specifies calendar days,
      another specifies business days, for the same SLA. Flag even if
      `normalized_seconds` are equal (because different working-hour
      assumptions may apply).
   c. **Unit-dimension TUC:** Temporal value used where a non-temporal unit
      is expected (e.g., `3 days` for a count limit → dimension mismatch).

3. Suppress false positives:
   - If both sources use the same `raw_text` → consistent (no finding).
   - If one source says "up to X" and the other says "at least X" → NOT a
     TUC; record as a C1-NVC with operator conflict.

**Severity:**
- BLOCKER: SLA or payment timeout conflict.
- MAJOR: approval window, session expiry, retry interval conflict.
- MINOR: archival or retention period conflict.

**Output schema:**
```json
{
  "detector": "C2-TUC",
  "severity": "MAJOR",
  "concept": "payment_processing_timeout",
  "values": [
    {
      "normalized_seconds": 86400,
      "raw_text": "24 hours",
      "business_day_adjusted": false,
      "source_ref": { "doc": "prd", "path": "prd/payments.md", "section": "§2.3" }
    },
    {
      "normalized_seconds": 28800,
      "raw_text": "1 business day",
      "business_day_adjusted": true,
      "source_ref": { "doc": "sdd", "path": "sdd/payments.yaml", "section": "§timeout" }
    }
  ],
  "normalized_delta_seconds": 57600,
  "delta_description": "24 calendar hours vs 8 business hours — 3× difference after normalization",
  "description": "PRD specifies payment timeout as 24 calendar hours; SDD uses 1 business day (8h). After normalization, these differ by 57,600 seconds. The correct boundary must be specified unambiguously.",
  "suggested_resolution": "Decide: calendar hours or business hours? Update both PRD §2.3 and SDD timeout section to use the same unit and value.",
  "reasoning_chain": [...]
}
```

---

### C3 — FSC: Field Schema Conflict

**Goal:** Detect cases where the same entity field is defined with
incompatible type, format, nullability, or constraints across documents.

**Algorithm:**

1. Read `index/field_schemas.json`. Group entries by `(entity_name, field_name)`
   using `alias_index` for name normalization.

2. For each field group with ≥ 2 entries, compare:
   - `type`: must be identical (or compatible — `integer` vs `decimal` is a conflict; `string` vs `text` is compatible).
   - `format`: must be identical if specified in both.
   - `nullable`: if one says `false` and another says `true` → conflict.
   - `required`: same as nullable.
   - `min`/`max`: if both are specified, they must define the same range (stricter range in SDD is acceptable only if PRD is silent; conflicting ranges are a conflict).
   - `precision`/`scale`: must be identical for decimal fields.
   - `enum_values`: if type=enum, see C4.
   - `default`: conflicting defaults are MAJOR.
   - `length`: conflicting length constraints are MAJOR.

3. Conflict classification:
   - **Type FSC:** `type` mismatch (e.g., PRD says `string`, SDD says `integer`).
   - **Nullable FSC:** nullability mismatch (BRD implies required; SDD marks nullable).
   - **Range FSC:** conflicting min/max bounds.
   - **Format FSC:** format string mismatch (see also C5).

**Severity:**
- BLOCKER: type mismatch or nullable conflict on a required field.
- MAJOR: range conflict, format mismatch, precision mismatch.
- MINOR: default value conflict.

**Output schema:**
```json
{
  "detector": "C3-FSC",
  "severity": "BLOCKER",
  "conflict_type": "type_fsc",
  "entity": "Contract",
  "field": "amount",
  "conflict_entries": [
    {
      "type": "decimal",
      "nullable": false,
      "precision": 2,
      "source_ref": { "doc": "prd", "path": "prd/contracts.md", "section": "§3.1" }
    },
    {
      "type": "integer",
      "nullable": false,
      "precision": null,
      "source_ref": { "doc": "sdd", "path": "sdd/contracts.yaml", "section": "ContractSchema" }
    }
  ],
  "description": "Contract.amount is typed as 'decimal' with 2 decimal places in PRD, but as 'integer' in SDD schema. This would cause precision loss on amounts with decimal fractions.",
  "suggested_resolution": "Align SDD ContractSchema to use decimal/float with precision=2. Verify database schema supports decimal storage.",
  "reasoning_chain": [...]
}
```

---

### C4 — ENC: Enum / Value-Set Conflict

**Goal:** Detect cases where the allowed values for an enum or status field
differ between documents.

**Algorithm:**

1. Read `index/enum_registry.json`. Group enum entries by `concept_name`
   (normalized via `alias_index`).

2. For each enum with ≥ 2 entries, compare `declared_values` lists:
   - **Missing values:** Values in source A but absent from source B.
   - **Extra values:** Values in source B but absent from source A.
   - **Renamed values:** Values with high string similarity (≥ 0.80) but
     different exact names (e.g., `PENDING_REVIEW` vs `UNDER_REVIEW`).

3. Severity classification:
   - BLOCKER: A value present in a flow diagram or SDD state machine is
     absent from the PRD/BRD enum definition (undefined behavior).
   - MAJOR: Values differ between BRD and PRD (upstream conflict).
   - MINOR: Values differ between PRD and SDD/Layout (implementation drift).

4. Cross-reference with `states.json`: If a missing enum value corresponds
   to a state that has transitions defined, severity escalates to BLOCKER.

**Output schema:**
```json
{
  "detector": "C4-ENC",
  "severity": "BLOCKER",
  "concept": "contract_status",
  "entity": "Contract",
  "conflict_type": "missing_values",
  "source_a": {
    "declared_values": ["DRAFT", "PENDING_REVIEW", "APPROVED", "REJECTED", "CANCELLED", "EXPIRED"],
    "source_ref": { "doc": "prd", "path": "prd/contracts.md", "section": "§3.2" }
  },
  "source_b": {
    "declared_values": ["DRAFT", "IN_REVIEW", "APPROVED", "DECLINED"],
    "source_ref": { "doc": "sdd", "path": "sdd/contracts.yaml", "section": "ContractStatus" }
  },
  "missing_in_sdd": ["PENDING_REVIEW", "REJECTED", "CANCELLED", "EXPIRED"],
  "extra_in_sdd": ["IN_REVIEW", "DECLINED"],
  "renamed_suspects": [
    { "prd": "PENDING_REVIEW", "sdd": "IN_REVIEW", "similarity": 0.81 },
    { "prd": "REJECTED", "sdd": "DECLINED", "similarity": 0.74 }
  ],
  "description": "PRD defines 6 contract statuses; SDD schema defines only 4, with different names for 2 of them. CANCELLED and EXPIRED states are entirely absent from SDD — their handling is undefined at the API level.",
  "suggested_resolution": "Expand SDD ContractStatus enum to include all PRD-defined values. Determine if IN_REVIEW = PENDING_REVIEW and DECLINED = REJECTED — if so, standardize names across all documents.",
  "reasoning_chain": [...]
}
```

---

### C5 — FMTC: Format / Locale Conflict

**Goal:** Detect format and locale inconsistencies — where the same data
is expected in different formats across documents, leading to parsing errors
or display bugs.

**Algorithm:**

1. Read `index/format_specs.json`. Group entries by `(concept_id, spec_type)`.

2. For each group with ≥ 2 entries, compare `value`:
   - **Currency conflict:** BRD says USD, SDD says EUR for the same amount field.
   - **Date format conflict:** PRD uses ISO 8601 (`YYYY-MM-DD`), Layout uses
     localized format (`DD/MM/YYYY`).
   - **Locale conflict:** Inconsistent locale codes across documents.
   - **Number separator conflict:** Some docs use comma decimal separator,
     others use period.
   - **Timezone conflict:** One document specifies UTC, another specifies local
     timezone for the same timestamp field.

3. Cross-reference with C3 (FSC):
   - If C3 already caught a `format` mismatch on the same field, merge the
     findings (do not duplicate).
   - If C5 catches a locale conflict that C3 missed (because C3 only checks
     schema types), create a new C5 finding.

**Severity:**
- BLOCKER: Currency mismatch on a financial transaction field.
- MAJOR: Date format or timezone mismatch on a business-critical timestamp.
- MINOR: Number separator or locale code mismatch.

**Output schema:**
```json
{
  "detector": "C5-FMTC",
  "severity": "BLOCKER",
  "conflict_type": "currency_conflict",
  "concept_id": "E-0001",
  "concept": "Contract.amount",
  "conflict_entries": [
    {
      "spec_type": "currency",
      "value": "BRL",
      "source_ref": { "doc": "brd", "path": "brd/overview.md", "section": "§3.1" }
    },
    {
      "spec_type": "currency",
      "value": "USD",
      "source_ref": { "doc": "sdd", "path": "sdd/contracts.yaml", "section": "ContractSchema" }
    }
  ],
  "description": "BRD defines Contract.amount in BRL (Brazilian Real); SDD schema uses USD. This currency mismatch would cause critical financial errors in amount handling and reporting.",
  "suggested_resolution": "Standardize currency to BRL throughout all documents. Update SDD schema's currency annotation and verify API response serialization.",
  "reasoning_chain": [...]
}
```

---

### C6 — AIC: Aggregation Inconsistency

**Goal:** Detect cases where declared sub-component values do not sum to
their declared total — budget overruns, quota mismatches, or SLA decomposition
errors that are invisible when looking at individual constraints.

**Algorithm:**

1. Read `aggregations[]` from `business_rules.json` and `requirements.json`
   (extracted by Stage 1 A8).

2. For each aggregation record:
   a. Compute `actual_sum` = sum of `sub_components[].value` (normalizing
      units via `quantities[].unit` where necessary).
   b. Compare `actual_sum` against `declared_total.value`.
   c. If `|actual_sum - declared_total| > tolerance` → AIC finding.

3. Tolerance rules:
   - **Exact constraints** (operator `=` or `<=` with integer values):
     tolerance = 0 (any mismatch is a finding).
   - **Estimated totals** (operator `~`, `≈`, or natural language "about"):
     tolerance = ±5% of declared total.
   - **Range totals** (operator `<=` or `>=` with explicit sub-ranges):
     if sub-components define separate ranges, check that the combined
     range covers the declared total range.

4. SLA-specific check:
   - If `unit_type` is temporal (seconds), use `normalized_seconds` from
     `temporal_specs[]` for all sub-component values.
   - Example: parent SLA = 24h (86400s), sub-steps = 12h + 8h + 6h = 26h
     (93600s) → sub-components exceed parent SLA by 2h.

**Severity:**
- BLOCKER: Aggregation on a financial total, SLA commitment, or security
  quota where sub-components exceed the declared total.
- MAJOR: Aggregation on operational limits (e.g., concurrent session counts).
- MINOR: Aggregation on display or reporting thresholds.

**Output schema:**
```json
{
  "detector": "C6-AIC",
  "severity": "BLOCKER",
  "aggregation_id": "AGG-0001",
  "concept": "total_contract_value_ceiling",
  "declared_total": { "value": 10000000, "unit": "currency_BRL" },
  "sub_components": [
    { "name": "direct_contracts", "value": 6000000 },
    { "name": "indirect_contracts", "value": 5000000 }
  ],
  "computed_sum": 11000000,
  "delta": 1000000,
  "delta_pct": 10.0,
  "description": "Total contract portfolio ceiling is 10M BRL, but sub-component ceilings sum to 11M (direct: 6M + indirect: 5M). Sub-limits allow the portfolio to exceed its declared total by 10%.",
  "suggested_resolution": "Reduce one or both sub-limits so their sum ≤ 10M, or increase the portfolio ceiling to 11M.",
  "reasoning_chain": [...]
}
```

---

### C7 — RDC: Requirement Duplication Conflict

**Goal:** Detect the same requirement defined in two or more source documents
with different specifications, creating ambiguity about which version is
authoritative.

**Algorithm:**

1. Build a text fingerprint (TF-IDF weighted n-gram hash) for the
   `description` or `name` field of every record in `requirements.json`.

2. Group records with fingerprint similarity ≥ 0.75 (Jaccard similarity
   on shingled n-grams of length 3).

3. For each group with ≥ 2 records from different source documents:
   a. Compare `quantities[]`, `temporal_specs[]`, `structured_predicate.result`,
      and `field_schema[]` values.
   b. If any of these differ → RDC finding.
   c. If only the `description` text differs but all normalized values match
      → MINOR (cosmetic divergence, possible copy-paste).

4. Cross-document duplicate check:
   - Compare each PRD requirement against each BRD requirement for
     semantic overlap. A PRD requirement that rephrases a BRD requirement
     without changing any constraint is PASS (good traceability).
   - A PRD requirement that rephrases AND changes a constraint value without
     documenting the change → RDC (MAJOR or BLOCKER).

**Severity:**
- BLOCKER: Duplicate requirement with conflicting business rule outcome
  (e.g., "deny" vs "allow" for the same condition).
- MAJOR: Duplicate requirement with conflicting numeric constraints.
- MINOR: Duplicate requirement with cosmetic text differences only.

**Output schema:**
```json
{
  "detector": "C7-RDC",
  "severity": "MAJOR",
  "source_a": {
    "concept_id": "RQ-0012",
    "concept_name": "PaymentTimeout",
    "description": "Payment processing must complete within 24 hours",
    "source_ref": { "doc": "brd", "path": "brd/payments.md", "section": "§3.2" }
  },
  "source_b": {
    "concept_id": "RQ-0045",
    "concept_name": "PaymentProcessingSLA",
    "description": "All payments must be processed within 48 hours",
    "source_ref": { "doc": "prd", "path": "prd/payments.md", "section": "§5.1" }
  },
  "fingerprint_similarity": 0.82,
  "differing_fields": [
    { "field": "temporal_specs.normalized_seconds", "value_a": 86400, "value_b": 172800 }
  ],
  "description": "BRD RQ-0012 and PRD RQ-0045 describe the same payment processing timeout (82% text similarity) but with conflicting SLA values: 24h vs 48h. The authoritative timeout is ambiguous.",
  "suggested_resolution": "Reconcile to a single timeout value. If 24h is correct (BRD authority), update PRD RQ-0045. If 48h is correct, update BRD RQ-0012.",
  "reasoning_chain": [...]
}
```

---

### C8 — CRD: Constraint Relaxation Drift

**Goal:** Detect when the same business constraint is progressively tightened
or relaxed across the document chain (BRD → PRD → SDD → Client) without
documented rationale — a sign of requirement degradation.

**Algorithm:**

1. Chain all concept records across tiers using `traceability_index`:
   for a given concept (e.g., `contract_amount_ceiling`), collect its
   value from BRD, PRD, SDD, and SDD_CLIENT.

2. For each 2-tier transition (BRD→PRD, PRD→SDD, SDD→CLIENT):
   a. Extract the numeric value, operator, and unit from `quantities[]`
      or the temporal value from `temporal_specs[]`.
   b. Compute the delta (absolute and relative).
   c. If the delta changes the constraint's strictness:
      - **Relaxation:** constraint becomes looser (e.g., 500M → 1B allows
        higher amounts). Flag with `direction: relaxation`.
      - **Tightening:** constraint becomes stricter (e.g., 500M → 200M).
        May be intentional — flag only if no rationale is documented.
   d. Check for documented rationale: search the source document section
      for keywords indicating intentional change ("phase 2", "v2", "revised",
      "updated as of", "per stakeholder feedback").

3. Drift accumulation:
   - If a constraint changes across every tier transition (BRD≠PRD≠SDD≠CLIENT)
     with no rationale at any step → BLOCKER (requirement is undefined).
   - If the drift reverses direction (relax then tighten, or vice versa)
     → BLOCKER (contradictory drift pattern).

**Severity:**
- BLOCKER: Unjustified drift on a financial, security, or compliance constraint.
- MAJOR: Unjustified drift on an operational constraint.
- MINOR: Drift with partial rationale documented.

**Output schema:**
```json
{
  "detector": "C8-CRD",
  "severity": "MAJOR",
  "concept": "contract_amount_ceiling",
  "drift_chain": [
    { "tier": "BRD", "value": 500000000, "operator": "<=", "source_ref": { "doc": "brd", "path": "brd/overview.md", "section": "§3.1" } },
    { "tier": "PRD", "value": 200000000, "operator": "<=", "source_ref": { "doc": "prd", "path": "prd/contracts.md", "section": "§5.2" } },
    { "tier": "SDD", "value": 100000000, "operator": "<=", "source_ref": { "doc": "sdd", "path": "sdd/contracts.yaml", "section": "ContractSchema" } }
  ],
  "drift_type": "progressive_tightening",
  "total_delta_pct": -80.0,
  "rationale_documented": false,
  "description": "Contract amount ceiling progressively tightens from 500M (BRD) → 200M (PRD) → 100M (SDD), an 80% reduction with no documented rationale at any tier transition.",
  "suggested_resolution": "Either document the rationale for each tightening step (e.g., risk adjustment, regulatory requirement) or align all tiers to the authoritative BRD value of 500M.",
  "reasoning_chain": [...]
}
```

---

### C9 — DIC: Dataflow Inconsistency

**Goal:** Detect mismatches between data produced by one action and data
consumed by a downstream action — fields that are expected but never
produced, or produced in an incompatible format.

**Algorithm:**

1. Read `events.json` for all domain events and their `payload_fields`.

2. For each `produces` edge in `knowledge_graph.json` (action→event),
   collect the event's `payload_fields` from `events.json`.

3. For each `consumes` edge (action→event), collect the expected input
   fields of the consuming action:
   - From the action's `field_schema[]` in `actions.json` or `field_schemas.json`
     (inputs are fields with `direction: "input"`).
   - From the flow step parameters in `flow_graphs.json`.

4. For each produce→consume pair on the same event:
   a. **Missing field check:** fields consumed but not produced.
   b. **Type mismatch check:** same field name, different `type` or `format`
      between producer output and consumer input.
   c. **Extra field check:** fields produced but never consumed (advisory —
      may be intentional for future use).

5. Silent data loss check:
   - If a field is marked `nullable: false` (required) by the consumer but
     the producer may emit `null` for that field (producer schema has
     `nullable: true` or field is optional) → flag as potential runtime error.

**Severity:**
- BLOCKER: Missing required field or type mismatch between producer and consumer.
- MAJOR: Nullable/required mismatch on a business-critical data field.
- MINOR: Extra produced fields never consumed (advisory).

**Output schema:**
```json
{
  "detector": "C9-DIC",
  "severity": "BLOCKER",
  "event_id": "EV-0003",
  "event_name": "PaymentConfirmed",
  "producer": {
    "action_id": "AC-0015",
    "action_name": "ProcessPayment",
    "produced_fields": ["payment_id", "amount", "currency", "timestamp"]
  },
  "consumer": {
    "action_id": "AC-0020",
    "action_name": "GenerateInvoice",
    "consumed_fields": ["payment_id", "amount", "currency", "timestamp", "customer_id", "tax_amount"]
  },
  "missing_fields": [
    { "field": "customer_id", "consumer_type": "string", "consumer_required": true },
    { "field": "tax_amount", "consumer_type": "decimal", "consumer_required": false }
  ],
  "description": "ProcessPayment emits PaymentConfirmed with 4 fields, but GenerateInvoice consumer expects 6 fields including 'customer_id' (required) and 'tax_amount'. Payment data flows to invoice generation are incomplete.",
  "suggested_resolution": "Extend ProcessPayment to emit all fields required by GenerateInvoice, or split the invoice generation into a separate data-fetch step.",
  "reasoning_chain": [...]
}
```

---

## Deduplication and Merge Logic

Before emitting findings, apply the following deduplication pass:

1. **Same concept, same documents, same type:** If two detectors catch the
   same conflict (e.g., STC and C3-FSC both detect a type mismatch on the
   same field), merge into a single finding with the higher severity and
   both detector codes listed (e.g., `"detector": "STC+C3-FSC"`).

2. **Overlap with Stage 2 graph findings:** If a C1-NVC conflicts with a
   B5-GRAPH-EDGE-CONFLICT on the same concept, note the overlap — keep both
   findings but cross-reference them.

3. **Merge priority:** `C1 > C2 > C3 > C4 > C5 > C6 > C7 > C8 > C9 > STC > PC > IC` (more specific
   detectors take priority in the merged finding's `detector` field).

---

## Output

### File: `consistency_findings.json`

```json
{
  "stage": "3",
  "version": "7.0",
  "generated_at": "...",
  "summary": {
    "total_findings": 18,
    "blocker": 4,
    "major": 9,
    "minor": 5,
    "by_detector": {
      "C1-NVC": 2,
      "C2-TUC": 1,
      "C3-FSC": 3,
      "C4-ENC": 2,
      "C5-FMTC": 1,
      "C6-AIC": 1,
      "C7-RDC": 2,
      "C8-CRD": 1,
      "C9-DIC": 1,
      "STC": 2,
      "PC": 3,
      "IC": 1,
      "BRM": 2,
      "VDG": 1
    }
  },
  "findings": [
    {
      "id": "CON-001",
      "detector": "C1-NVC",
      "severity": "BLOCKER",
      "priority": 1,
      ...
    }
  ]
}
```

---

## Rules

- Read `index/*.json` only. Never read raw source documents.
- MUST run all v5 detectors: STC, PC, IC, BRM, VDG, OQ, CMS, CRG.
- MUST run all v6/v7 detectors: C1-NVC, C2-TUC, C3-FSC, C4-ENC, C5-FMTC, C6-AIC, C7-RDC, C8-CRD, C9-DIC.
- C1 MUST use normalized values from `quantities[]` — never compare raw text.
- C2 MUST use `normalized_seconds` — never compare raw duration strings.
- C3 MUST read from `field_schemas.json` — not from individual entity records.
- C4 MUST cross-reference enum values with `states.json` transitions.
- C5 MUST merge with C3 findings when format conflicts overlap with schema conflicts.
- C6 MUST use `aggregations[]` from A8 — compute sum of sub-components and compare to declared total.
- C7 MUST use TF-IDF n-gram fingerprinting for requirement similarity — never exact string match alone.
- C8 MUST chain the same concept across all available tiers (BRD→PRD→SDD→CLIENT) to detect drift.
- C9 MUST read `events.json` payload_fields and cross-reference produces/consumes edges in knowledge_graph.
- Deduplication pass is mandatory before output.
- Explanation chains are mandatory on every finding.
- Do not assign final priority scores — Stage 5 does global prioritization.
- Fully domain-agnostic.
- Target execution time: **< 15 seconds** for 50 concepts.
