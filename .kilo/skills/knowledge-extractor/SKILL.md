---
name: knowledge-extractor
version: "6.0"
description: >
  Stage 1 of the gap-analyzer pipeline. Reads all raw source documents from
  the steering directory (EXCEPT UI_FOUNDATIONS) and produces a fully normalized,
  typed, multi-dimensional modular Knowledge Index in index/*.json.
  v6 adds 7 new extraction dimensions (A1–A7): quantitative values, temporal/SLA
  specs, field schema details, currency/format units, predicate normalization,
  domain events, and enumeration completeness. Preserves the existing
  reasoning_chain and 6-dimension confidence scoring from v5.
  Feeds directly into Stage 1.5 (extraction-auditor) and Stage 2
  (traceability-mapper). Never reads its own output files.
---

# Knowledge Extractor v6

## Mission

Extract every semantically meaningful concept from all source documents and
produce a normalized, machine-traversable Knowledge Index that downstream
stages can use for contradiction detection, traceability analysis, and
semantic gap auditing — with zero loss of information and maximum
quantitative precision.

---

## Input

All files inside `steering/` **EXCEPT** `UI_FOUNDATIONS`:

```
steering/
├── brd/          (Business Requirements Documents)
├── prd/          (Product Requirements Documents)
├── user_flow_map/ (User Flow Maps)
├── IA/           (Information Architecture)
├── layout/       (Layout specifications)
├── layout-builder/ (Layout builder specs)
├── sdd/          (System Design Documents)
├── sdd_client/   (Client-side SDD)
├── orr-audit/    (Operational Readiness Review)
├── architecture-grounding/
├── integration-discovery/
└── integration-resolver/
```

**Do NOT read:** `UI_FOUNDATIONS` (processed separately by the UI pipeline).

---

## Processing Order (Priority)

Process documents in this order to front-load the most semantically dense
material and catch contradictions early:

1. BRD (authoritative business rules, roles, constraints)
2. PRD (product requirements, functional specs)
3. SDD / SDD_CLIENT (technical contracts, API schemas, data models)
4. USER_FLOW_MAP (flow graphs, actor sequences)
5. IA (navigation structure, screen hierarchy)
6. LAYOUT / LAYOUT-BUILDER (UI screen specs)
7. ORR-AUDIT / ARCHITECTURE-GROUNDING (operational/architectural constraints)
8. INTEGRATION-DISCOVERY / INTEGRATION-RESOLVER (external system contracts)

Use **intermediate summaries** after every 2 documents to prevent context
overflow. Never skip a document. 100% accuracy is mandatory.

---

## Extraction Schema (v6)

### Core Concept Types (preserved from v5)

| Index File | Concept Type | Description |
|---|---|---|
| `entities.json` | Entity | Domain objects with identity and lifecycle |
| `roles.json` | Role | Human or system actors |
| `requirements.json` | Requirement | Functional/non-functional requirements |
| `business_rules.json` | BusinessRule | Constraints, validations, policies |
| `states.json` | State | Entity lifecycle states and transitions |
| `actions.json` | Action | Operations performed by roles on entities |
| `permissions.json` | Permission | Access control grants/restrictions |
| `flow_graphs.json` | FlowGraph | Structured flow sequences with nodes/edges |

---

## NEW: v6/v7 Extraction Dimensions (A1–A9)

These fields are added to relevant concept records. They are **additive** —
they do not replace or alter existing fields.

---

### A1 — Quantitative Values (`quantities[]`)

Extract every numeric claim tied to a business concept.

**Structure per item:**
```json
{
  "value": 500,
  "unit": "million",
  "operator": "<=",
  "concept": "contract_amount_ceiling",
  "concept_id": "BR-0012",
  "source_ref": { "doc": "brd", "path": "brd/overview.md", "section": "§3.1" },
  "raw_text": "Contract amount must not exceed 500M"
}
```

**Operators:** `=`, `!=`, `<`, `<=`, `>`, `>=`, `between`, `not_between`

**Capture ALL numeric claims including:**
- Retry limits, attempt counts, thresholds
- Amount ceilings/floors, percentage rules
- Count constraints (min/max items, quorum counts)
- Rate limits, concurrency limits
- Timeout durations (also captured in A2)

**Attach to:** `business_rules.json`, `requirements.json`, or `entities.json`
depending on context. Every record that contains a numeric claim MUST have
a `quantities[]` array (empty array if none).

---

### A2 — Temporal / SLA Values (`temporal_specs[]`)

Extract every duration, deadline, SLA, or time-based constraint and
**normalize to seconds**.

**Structure per item:**
```json
{
  "normalized_seconds": 86400,
  "raw_text": "24 hours",
  "unit_type": "duration|deadline|sla|recurrence|window",
  "concept": "payment_processing_timeout",
  "concept_id": "RQ-0015",
  "source_ref": { "doc": "prd", "path": "prd/payments.md", "section": "§2.3" },
  "business_day_adjusted": false,
  "note": "If unit_type is 'business_day', set business_day_adjusted=true and normalize assuming 8h/day"
}
```

**Normalization table:**

| Raw unit | Seconds |
|---|---|
| second / sec / s | 1 |
| minute / min / m | 60 |
| hour / hr / h | 3600 |
| day (calendar) | 86400 |
| business day | 28800 (8h) |
| week | 604800 |
| month (30d) | 2592000 |
| year (365d) | 31536000 |

**Business day flag:** If source says "business day / working day / business hour",
set `business_day_adjusted: true` and document the assumed hours/day (default 8).

**Capture ALL temporal claims including:**
- Session timeouts, token expiry, retry windows
- SLA response times, processing deadlines
- Approval expiry windows, lock durations
- Archival periods, retention windows

---

### A3 — Field Schema Details (`field_schema[]`)

For every data field/attribute of every entity, extract full type metadata.

**Structure per field:**
```json
{
  "entity_id": "E-0001",
  "entity_name": "Contract",
  "field_name": "amount",
  "type": "decimal",
  "format": "currency",
  "nullable": false,
  "required": true,
  "min": 0,
  "max": 500000000,
  "length": null,
  "precision": 2,
  "scale": 2,
  "enum_values": null,
  "default": null,
  "is_enum": false,
  "source_ref": { "doc": "prd", "path": "prd/contracts.md", "section": "§3.1" }
}
```

**Field metadata to extract (null if not specified):**

| Property | Description |
|---|---|
| `type` | string, integer, decimal, boolean, date, datetime, uuid, enum, array, object |
| `format` | currency, email, phone, url, iso8601, etc. |
| `nullable` | Can this field be null? (true/false/null if unspecified) |
| `required` | Is this field mandatory? |
| `min` | Minimum value (numeric) or minimum length (string) |
| `max` | Maximum value or maximum length |
| `length` | Exact length constraint |
| `precision` | Decimal precision |
| `scale` | Decimal scale |
| `enum_values` | List of valid values if type=enum |
| `default` | Default value if unspecified |
| `is_enum` | Boolean flag — drives A7 enumeration completeness check |

**Attach to:** Write to `entities.json[*].field_schema[]` and mirror to
`index/field_schemas.json` for cross-entity schema comparison in Stage 3.

---

### A4 — Currency / Format / Locale Units (`format_specs[]`)

Extract every claim about formatting conventions, currencies, date formats,
and locales to enable Stage 3's FMTC detector.

**Structure per item:**
```json
{
  "spec_type": "currency|date_format|locale|number_format|timezone",
  "value": "BRL",
  "context": "Contract amount field",
  "concept_id": "E-0001",
  "source_ref": { "doc": "prd", "path": "prd/contracts.md", "section": "§3.1" }
}
```

**Write to:** `index/format_specs.json`

**Capture:**
- Currency codes (USD, EUR, BRL, etc.)
- Date format strings (DD/MM/YYYY, ISO 8601, etc.)
- Locale codes (en-US, pt-BR, etc.)
- Number separators (comma vs period)
- Timezone specifications

---

### A5 — Predicate Normalization (`structured_predicate`)

Convert every conditional rule, constraint, or guard clause to a normalized
logical form that Stage 4's SMT-lite analyzer can process.

**Normalized form:**
```json
{
  "structured_predicate": {
    "conditions": [
      {
        "variable": "contract.amount",
        "operator": ">",
        "value": 1000000,
        "unit": "currency_BRL",
        "logical_connector": "AND"
      },
      {
        "variable": "user.role",
        "operator": "=",
        "value": "Manager",
        "logical_connector": null
      }
    ],
    "result": "requires_dual_approval",
    "result_type": "action|state_transition|permission|restriction",
    "confidence": 0.92,
    "raw_text": "Contracts above 1M BRL require dual approval from a Manager"
  }
}
```

**Operators:** `=`, `!=`, `<`, `<=`, `>`, `>=`, `IN`, `NOT IN`, `CONTAINS`,
`IS_NULL`, `IS_NOT_NULL`, `MATCHES_REGEX`

**Logical connectors:** `AND`, `OR`, `NOT`, `XOR`, `IMPLIES`

**Predicate extraction rules:**
1. Every `business_rules.json` record MUST have a `structured_predicate` (even
   if `conditions: []` and confidence is low).
2. If a condition cannot be parsed with confidence ≥ 0.5, set
   `parse_confidence: "low"` and keep `raw_text` — do not fabricate a predicate.
3. Compound rules (if A then B; if C then D) must be split into multiple
   predicate records, one per outcome.

---

### A6 — Domain Events (`events[]`)

Extract every domain event mentioned in the source documents.

**Structure per event:**
```json
{
  "id": "EV-0001",
  "name": "ContractApproved",
  "direction": "produced|consumed|both",
  "producer_action": "AC-0001",
  "consumer_actions": ["AC-0045", "AC-0046"],
  "payload_fields": ["contract_id", "approved_by", "timestamp"],
  "trigger_condition": "contract.status transitions to APPROVED",
  "source_refs": [
    { "doc": "brd", "path": "brd/overview.md", "section": "§4.1" },
    { "doc": "sdd", "path": "sdd/events.yaml", "section": "ContractApproved" }
  ]
}
```

**Capture ALL event mentions including:**
- Explicit event definitions (event buses, message queues, webhooks)
- Implicit events (state transitions that trigger downstream effects)
- Domain events in flow diagrams
- Integration events in SDD / integration-discovery docs

**Write to:** `index/events.json`

**Critical for Stage 2:** B4-GRAPH-ORPHAN-EVENT requires this data.

---

### A7 — Enumeration Completeness (`enum_registry[]`)

For every field or concept with `is_enum: true` (from A3), extract the
**complete set of valid values** and flag coverage gaps.

**Structure per enum:**
```json
{
  "enum_id": "ENUM-0001",
  "concept_name": "contract_status",
  "entity_id": "E-0001",
  "declared_values": ["DRAFT", "PENDING_REVIEW", "APPROVED", "REJECTED", "CANCELLED"],
  "values_with_transitions": ["DRAFT", "PENDING_REVIEW", "APPROVED", "REJECTED"],
  "values_without_handler": ["CANCELLED"],
  "values_in_flow_not_in_enum": [],
  "values_in_enum_not_in_flow": ["CANCELLED"],
  "coverage_complete": false,
  "coverage_note": "CANCELLED state defined in enum but no flow path leads to or from it",
  "source_refs": [
    { "doc": "prd", "path": "prd/contracts.md", "section": "§3.2" },
    { "doc": "sdd", "path": "sdd/contracts.yaml", "section": "ContractStatus" }
  ]
}
```

**Completeness checks:**
1. Every enum value must appear in at least one state transition (`states.json`).
2. Every state in `states.json` must correspond to a declared enum value.
3. Values referenced in flow steps but absent from the enum → flag as
   `values_in_flow_not_in_enum` (likely an undeclared state).
4. Values in enum but with no inbound or outbound transition → flag as
   `values_without_handler` (orphan state).

**Write to:** `index/enum_registry.json`

---

### A8 — Aggregation Constraints (`aggregations[]`)

Extract every declared total, quota, limit, or aggregate value that is
composed of named sub-component values, enabling Stage 3's C6-AIC
aggregation inconsistency detector.

**Structure per item:**
```json
{
  "aggregation_id": "AGG-0001",
  "concept": "total_contract_value_ceiling",
  "concept_id": "BR-0030",
  "declared_total": {
    "value": 10000000,
    "unit": "currency_BRL",
    "operator": "<=",
    "raw_text": "Total contract portfolio must not exceed 10M BRL"
  },
  "sub_components": [
    {
      "name": "direct_contracts_ceiling",
      "value": 6000000,
      "unit": "currency_BRL",
      "operator": "<=",
      "source_ref": { "doc": "prd", "path": "prd/contracts.md", "section": "§3.1" }
    },
    {
      "name": "indirect_contracts_ceiling",
      "value": 5000000,
      "unit": "currency_BRL",
      "operator": "<=",
      "source_ref": { "doc": "prd", "path": "prd/contracts.md", "section": "§3.2" }
    }
  ],
  "computed_sum": 11000000,
  "delta_from_total": 1000000,
  "consistent": false,
  "note": "Sub-component ceilings (6M + 5M = 11M) exceed declared total ceiling of 10M",
  "source_ref": { "doc": "brd", "path": "brd/overview.md", "section": "§4.0" }
}
```

**Aggregation patterns to capture:**
- **Budget/limit ceilings:** total portfolio cap and per-category sub-limits
- **SLA decomposition:** parent SLA response time and per-step sub-SLAs
- **Quota allocations:** total capacity and per-role/per-region quotas
- **Count constraints:** max total items and max per-type items (e.g., "max 10 active contracts, max 3 high-value")
- **Financial aggregates:** total transaction volume and per-channel breakdowns

**Algorithm:**
1. For every numeric claim with a scope indicator ("total", "overall", "portfolio",
   "combined"), search for sub-component claims in the same or related documents.
2. Use `alias_index` to resolve sub-component names to the same aggregation context.
3. Compute `computed_sum` of sub-component values (using `normalized_seconds` for
   temporal aggregations, same-unit numeric addition for quantities).
4. Compare `computed_sum` against `declared_total.value`.
5. Set `consistent = true` only if `computed_sum` matches declared total within
   a configurable tolerance (default: ±5% for estimates, ±0 for exact constraints).

**Attach to:** `business_rules.json[*].aggregations[]` or
`requirements.json[*].aggregations[]` depending on source. Empty array if no
aggregation claims found.

---

### A9 — Responsibility Mapping (`responsibilities[]`)

Extract every explicit or implicit assignment of responsibility or
accountability from a role to an action, enabling Stage 4's D6-RGC
responsibility gap detector and Stage 2's B7-GRAPH-RGAP.

**Structure per item:**
```json
{
  "responsibility_id": "RESP-0001",
  "action_id": "AC-0012",
  "action_name": "ApproveContract",
  "role_id": "RL-0001",
  "role_name": "Manager",
  "accountability": "responsible|accountable|consulted|informed",
  "explicit": true,
  "source_ref": { "doc": "prd", "path": "prd/contracts.md", "section": "§4.2" }
}
```

**Accountability levels (RACI model):**
| Level | Meaning | Detect When |
|-------|---------|-------------|
| `responsible` | Performs the action | Action has `actor = role` in `actions.json`, or flow step assigns actor |
| `accountable` | Owns the outcome | Explicit "X is accountable for Y" statement |
| `consulted` | Must be consulted before action | "X must approve Y", "X reviews Y" |
| `informed` | Must be notified after action | "X is notified when Y happens" |

**Infer implicit responsibilities:**
1. If an action has `actor` in `actions.json` → the actor is `responsible`.
2. If a flow step assigns a role to a node → that role is `responsible` for
   the action linked to that node.
3. If a permission record grants a role access to an action → that role is
   at minimum `informed` (may be `responsible` if `actor` aligns).
4. If "X is accountable for Y" language appears → set `accountable` level.

**Write to:** `index/responsibilities.json`

---

## Preserved from v5: Confidence Scoring (6 Dimensions)

Every extracted concept retains the 6-dimension confidence score:

```json
{
  "confidence": {
    "syntactic": 0.95,
    "semantic": 0.88,
    "cross_doc": 0.72,
    "completeness": 0.80,
    "ambiguity": 0.65,
    "overall": 0.80
  }
}
```

| Dimension | Description |
|---|---|
| `syntactic` | How clearly the concept is stated in text |
| `semantic` | How unambiguously the concept's meaning can be inferred |
| `cross_doc` | Whether the concept is consistent across multiple documents |
| `completeness` | Whether all expected attributes of the concept are present |
| `ambiguity` | Inverse of how many plausible interpretations exist |
| `overall` | Weighted average (syntactic×0.2 + semantic×0.25 + cross_doc×0.2 + completeness×0.15 + ambiguity×0.2) |

---

## Preserved from v5: Reasoning Chains

Every extracted concept record includes a `reasoning_chain[]`:

```json
"reasoning_chain": [
  {
    "step": 1,
    "evidence": "Text: 'Contract amount must not exceed 500M' found in brd/overview.md §3.1",
    "inference": "Identifies a numeric constraint on the Contract entity's amount field"
  },
  {
    "step": 2,
    "evidence": "Unit 'M' with context 'amount' → monetary value in millions",
    "inference": "Resolves to value=500, unit=million, operator=<="
  },
  {
    "step": 3,
    "conclusion": "Created quantities[0] entry with value=500, unit=million, operator=<=, concept=contract_amount_ceiling"
  }
]
```

---

## Output Files

```
index/
├── entities.json          (+ field_schema[], quantities[], temporal_specs[])
├── roles.json
├── requirements.json      (+ quantities[], temporal_specs[], structured_predicate, aggregations[])
├── business_rules.json    (+ structured_predicate, quantities[], temporal_specs[], aggregations[])
├── states.json
├── actions.json           (+ events produced/consumed, responsible_roles[])
├── permissions.json
├── flow_graphs.json
├── traceability_index.json
├── field_schemas.json     [NEW v6 — cross-entity schema index]
├── format_specs.json      [NEW v6 — A4]
├── events.json            [NEW v6 — A6]
├── enum_registry.json     [NEW v6 — A7]
└── responsibilities.json  [NEW v7 — A9]
```

### `traceability_index.json` structure

```json
{
  "version": "6.0",
  "alias_index": {
    "Customer": ["Client", "End User", "Buyer"],
    "Contract": ["Agreement", "Deal"]
  },
  "inferred_concepts": [
    {
      "id": "IC-0001",
      "name": "ComplianceOfficer",
      "kind": "role",
      "inferred_from": "user_flow_map/contracts.md Step 4",
      "confidence": 0.75,
      "note": "Referenced but never defined in BRD or PRD"
    }
  ],
  "placeholder_refs": [],
  "coverage": {}
}
```

---

## Rules

- Read **ALL** files in `steering/` except `UI_FOUNDATIONS`. Never skip.
- Process by priority order (BRD → PRD → SDD → UFM → IA → Layout → ORR → Integration).
- Use intermediate summaries every 2 documents to prevent context overflow.
- Every `business_rules.json` record MUST have `structured_predicate` (A5).
- Every entity MUST have `field_schema[]` (A3) — empty array if no field info.
- Every temporal claim MUST have `temporal_specs[]` (A2) normalized to seconds.
- Every numeric claim MUST have `quantities[]` (A1).
- Every enum/status field MUST be registered in `enum_registry.json` (A7).
- Every aggregation claim (totals + sub-components) MUST be captured in `aggregations[]` (A8).
- Every responsibility/accountability assignment MUST be recorded in `responsibilities.json` (A9).
- Preserve ALL v5 fields: `reasoning_chain`, 6-dimension confidence, `alias_index`, `inferred_concepts`, `negative_knowledge`.
- Do not delete, overwrite, or downgrade any existing concept already in the index — only extend.
- Fully domain-agnostic: no assumptions about the business domain.
- Target extraction coverage: **≥ 95%** of all semantically meaningful claims.
- Target execution time: **< 30 seconds** per document.
