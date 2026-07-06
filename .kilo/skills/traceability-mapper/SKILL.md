---
name: traceability-mapper
version: "6.0"
description: >
  Stage 2 of the gap-analyzer pipeline. Reads only the modular Knowledge Index
  (index/*.json), including flow_graphs.json and the new v6 files
  (events.json, enum_registry.json, format_specs.json).
  v5 capabilities preserved: typed knowledge graph with 21 edge labels,
  weighted traceability, multi-hop traversal (depth 5), explanation chains.
  v6 adds Graph Health Analysis (B1–B6): cycle detection, dead-end states,
  unreachable nodes, orphan events, edge conflicts, and alias suspect reporting.
  Also traces each flow step to its parent requirement, flags orphan steps,
  and extends concept_chain_map to include flow graph coverage.
  Always runs. Never reads raw source documents.
---

# Traceability Mapper v6

## Input

```
index/entities.json
index/roles.json
index/requirements.json
index/business_rules.json
index/states.json
index/actions.json
index/permissions.json
index/traceability_index.json     (includes inferred_concepts from Stage 1)
index/flow_graphs.json
index/events.json                 [NEW v6]
index/enum_registry.json          [NEW v6]
index/format_specs.json           [NEW v6]
index/extraction_quality_report.json  [NEW v6 — from Stage 1.5]
```

All reads from `index/*.json` only. Never reads raw documents.

---

## Step 0 — Quality Gate Check

Read `extraction_quality_report.json`:
- If `gate_pass: false` → apply `downstream_confidence_modifier` to all
  confidence scores and prepend a WARNING to all findings.
- If `soft_warn: true` → multiply all confidence values by
  `downstream_confidence_modifier` before emitting findings.
- If all metrics PASS → proceed with full confidence.

---

## Step 1 — Cross-Artifact Mapping

For every concept across all typed index files (entities, roles, requirements,
business_rules, states, actions, permissions, flow steps, events,
external_systems), build `chain_positions`: which of
`brd, prd, user_flow_map, IA, layout, sdd, sdd_client` have ≥ 1
non-placeholder `source_ref`.

### Flow Step Chain Positions

For each node in `flow_graphs.json`, determine chain positions by:
1. `node_links.requirement_id` → requirement's `lifecycle` in `requirements.json`.
2. `node_links.action_id` → action's `source_refs` in `actions.json`.
3. `node_links.ia_node_id` → if non-null, add `IA` chain position.
4. Flow's own `source` path → always adds `user_flow_map`.

---

## Step 2 — Knowledge Graph Construction

Build `index/knowledge_graph.json`. This graph is the canonical semantic
model that downstream stages traverse for multi-hop reasoning and impact analysis.

### Node Types

Every concept in the 8 index files + flow graph nodes + IA nodes + layout
screens + API endpoints + events + external systems becomes a graph node:

```json
{
  "id": "E-0001",
  "type": "entity|role|requirement|business_rule|state|action|permission|flow_step|ia_node|layout_screen|api_endpoint|event|external_system|data_model",
  "name": "Contract",
  "source_tier": "prd",
  "criticality": "core"
}
```

| Node Type | Description | Source |
|---|---|---|
| `event` | Domain event (PaymentConfirmed, ContractApproved) | BRD, PRD, flow_graphs, SDD, events.json |
| `external_system` | Third-party integration | BRD, SDD, flow_graphs |
| `data_model` | Persistence model, database schema | SDD, sdd_client |

### Edge Types (23 labels)

| Edge Label | From → To | Construction Rule |
|---|---|---|
| `performs` | role → action | `actions.json[*].actor` matches `roles.json[*].name` |
| `owns` | role → entity | `permissions.json[*].actor` has `exclusive:true` |
| `transitions_to` | state → state | `states.json[*].transitions[*].{from,to}` |
| `requires` | requirement → action | requirement implies action via flow node_links |
| `forbids` | requirement/rule → action/role | `negative_knowledge.forbidden_actors/actions` |
| `references` | any → any | `references[].item` resolved via alias_index |
| `implements` | action → requirement | `node_links.requirement_id` in flow_graphs |
| `displays` | layout_screen → action/entity | layout components |
| `invokes` | action → api_endpoint | matched via alias |
| `guards` | business_rule → transition | `structured_predicate.guard` present |
| `escalates_to` | flow_step → flow_step | `flow_graphs[*].escalations[*]` |
| `compensates` | flow_step → flow_step | `flow_graphs[*].compensation_paths[*]` |
| `sub_process` | flow_step → flow | `flow_graphs[*].subprocesses[*]` |
| `creates` | action → entity | `action_type: create` |
| `updates` | action → entity | `action_type: update` |
| `deletes` | action → entity | `action_type: delete` |
| `depends_on` | any → any | explicit dependency statement |
| `blocks` | any → any | "X prevents Y" |
| `derives_from` | entity → entity | derived attribute |
| `authorizes` | permission → action | grants permission |
| `consumes` | action → event | action subscribes to event |
| `produces` | action → event | action emits event |
| `responsible_for` | role → action | `responsibilities.json[*]` with `accountability: responsible|accountable` |
| `dataflows_to` | action → action | A `produces` event E and B `consumes` event E → A `dataflows_to` B |

### Edge Schema

```json
{
  "from": "RL-0001",
  "to": "AC-0001",
  "label": "performs",
  "confidence": 0.95,
  "basis": "explicit|inferred",
  "source_refs": [
    { "doc": "prd", "path": "prd/contracts.md", "section": "§4.2" }
  ]
}
```

---

## Step 3 — Coverage Analysis (Weighted Traceability)

### Weighted Coverage Formula

```
expected_at_P(C) = number of downstream entities/screens/steps/endpoints
                   that should reference C based on knowledge graph

actual_at_P(C)   = confirmed links in knowledge_graph.json from C to tier P

coverage_score(C, P) = actual_at_P(C) / expected_at_P(C)
```

### Coverage Output

Write into `traceability_index.json.coverage`:

```json
{
  "chain_depth_available": "layout",
  "coverage_by_position": {
    "brd":           { "count": 14, "pct": 100, "weighted_avg": 1.00 },
    "prd":           { "count": 14, "pct": 100, "weighted_avg": 0.95 },
    "user_flow_map": { "count": 11, "pct": 79,  "weighted_avg": 0.67 },
    "IA":            { "count": 9,  "pct": 64,  "weighted_avg": 0.88 },
    "layout":        { "count": 7,  "pct": 50,  "weighted_avg": 0.55 }
  }
}
```

---

## Step 4 — Standard Traceability Findings

### TRC-1 — Chain Break

**Trigger:** Position N populated; position N+1 empty OR
`coverage_score(C, N+1) < 0.5`.

**Severity:** MAJOR; BLOCKER if `criticality: core`.

### TRC-2 — Orphan Artifact

**Trigger:** An action whose earliest position is `layout` or `sdd` with no
link to any requirement.

**Severity:** MAJOR.

---

## Step 5 — Flow Step Traceability

### Step 5.1 — Requirement Linking

Check `node_links.requirement_id`:
- Non-null → link confirmed.
- Null → attempt auto-link (keyword overlap ≥ 2 significant words; confidence ≥ 0.6).
- No match → orphan flow step.

### Step 5.2 — TRC-FLOW, TRC-FLOW-ACTOR, TRC-FLOW-SCREEN

Same as v5. All findings include explanation chains.

### Step 5.3 — Multi-Hop Traceability

BFS traversal up to depth 5. Detect contradictions requiring 3+ artifact hops.

---

## Step 6 — NEW: Graph Health Analysis (B1–B6) ✨

These analyzers run AFTER the knowledge graph is fully built in Step 2.
They examine the graph's structural integrity — not content correctness
(that is Stage 3's job) but structural pathology.

---

### B1 — GRAPH-CYCLE: Logical Cycle / Deadlock Detection

**Goal:** Find circular dependency chains where A depends on B which depends
on A (or longer chains), creating logical deadlocks or infinite loops.

**Algorithm:**
1. Extract all `depends_on`, `requires`, `guards`, and `blocks` edges from
   the knowledge graph.
2. Build a directed dependency subgraph from these edges only.
3. Run Tarjan's SCC (Strongly Connected Components) algorithm.
4. Any SCC with more than 1 node is a cycle.
5. Classify by cycle type:
   - **Dependency cycle:** A `depends_on` B `depends_on` A (deadlock risk)
   - **Guard cycle:** Rule R1 `guards` Transition T1, which is only reachable
     after Rule R1 is satisfied (contradictory guard)
   - **Approval cycle:** Role A can only approve after Role B approves, and
     Role B can only approve after Role A approves

**Output schema:**
```json
{
  "detector": "B1-GRAPH-CYCLE",
  "severity": "BLOCKER",
  "cycle_type": "dependency_cycle",
  "cycle_nodes": ["AC-0012 (SubmitPayment)", "AC-0015 (ValidatePayment)", "AC-0012"],
  "cycle_edges": [
    { "from": "AC-0012", "to": "AC-0015", "label": "depends_on" },
    { "from": "AC-0015", "to": "AC-0012", "label": "requires" }
  ],
  "description": "SubmitPayment depends on ValidatePayment, which requires SubmitPayment — circular dependency, neither can proceed.",
  "source_refs": [
    { "doc": "prd", "path": "prd/payments.md", "section": "§3.2" },
    { "doc": "sdd", "path": "sdd/payments.yaml", "section": "§5" }
  ],
  "suggested_resolution": "Break cycle by making ValidatePayment a precondition (not a dependency) of SubmitPayment.",
  "reasoning_chain": [...]
}
```

---

### B2 — GRAPH-DEADEND: Dead-End State Detection

**Goal:** Identify states that have inbound transitions but no outbound
transitions, and are NOT marked as terminal states.

**Algorithm:**
1. For every node of type `state` in `knowledge_graph.json`:
   - Count outbound `transitions_to` edges → `outbound_count`.
   - Count inbound `transitions_to` edges → `inbound_count`.
2. Flag states where `outbound_count = 0` AND `inbound_count > 0` AND
   the state is NOT in `states.json[*].is_terminal = true`.
3. Also flag states where ALL outbound transitions lead back to the same
   state (self-loop without escape → effective dead-end).

**Dead-end vs Terminal distinction:**
- Terminal state: explicitly marked `is_terminal: true` in `states.json`
  (e.g., `COMPLETED`, `ARCHIVED`). These are PASS — by design.
- Dead-end state: not marked terminal but has no exit. These are BLOCKER.
- Ambiguous terminal: `is_terminal` is null and no outbound transitions →
  flag as MAJOR (may be intentional but undocumented).

```json
{
  "detector": "B2-GRAPH-DEADEND",
  "severity": "BLOCKER",
  "state_id": "ST-0007",
  "state_name": "PAYMENT_FAILED",
  "inbound_count": 3,
  "outbound_count": 0,
  "is_terminal": false,
  "description": "PAYMENT_FAILED state is reachable from 3 transitions but has no exit path and is not marked as a terminal state. Entities entering this state are permanently stuck.",
  "source_refs": [
    { "doc": "prd", "path": "prd/payments.md", "section": "§3.5" }
  ],
  "suggested_resolution": "Either add a retry/recovery transition from PAYMENT_FAILED, or mark it as is_terminal=true with documented rationale.",
  "reasoning_chain": [...]
}
```

---

### B3 — GRAPH-UNREACHABLE: Unreachable Node Detection

**Goal:** Identify states or screens that have no inbound path from any
root node (initial states, entry points, or BRD-level concepts).

**Algorithm:**
1. Identify root nodes: states marked `is_initial: true`, IA nodes marked
   `is_root: true`, flow graphs' `start_node`, and all BRD-tier concepts.
2. Run BFS from ALL root nodes simultaneously, following ALL edge types
   (except `forbids`, `blocks`, and `compensates` which represent
   preventive/alternative paths, not normal flow).
3. Mark all reached nodes as `reachable`.
4. Flag all nodes NOT marked `reachable` as `unreachable`.
5. Suppress false positives:
   - Nodes referenced only by `compensates` or `escalates_to` edges are
     reachable via exception paths — mark as `reachable_via_exception`.
   - Nodes in `inferred_concepts` (not from explicit source) → downgrade
     severity to MINOR.

```json
{
  "detector": "B3-GRAPH-UNREACHABLE",
  "severity": "MAJOR",
  "node_id": "SCR-0042",
  "node_type": "layout_screen",
  "node_name": "Bulk Contract Approval Screen",
  "reachable_via_exception": false,
  "description": "Layout screen 'Bulk Contract Approval Screen' has no inbound path from any root node. It is defined in the Layout document but never linked from any IA node or flow step.",
  "source_refs": [
    { "doc": "layout", "path": "layout/contracts-bulk.md", "section": "§1" }
  ],
  "suggested_resolution": "Add this screen to the IA document under the Contracts section, or remove it from the Layout if it is out of scope.",
  "reasoning_chain": [...]
}
```

---

### B4 — GRAPH-ORPHAN-EVENT: Orphan Event Detection

**Goal:** Identify domain events that are produced but never consumed
(dangling producer) or consumed but never produced (phantom consumer).

**Algorithm:**

Read `index/events.json`. For each event:

1. **Produced but not consumed (orphan producer):**
   - Event has at least one `producer_action` in `events.json`.
   - Event has no `consumer_actions` in `events.json`.
   - Event has no `consumes` edge pointing to it in `knowledge_graph.json`.
   - → Flag as `orphan_producer`.

2. **Consumed but not produced (phantom consumer):**
   - Event appears in at least one action's `consumed_events[]` in `actions.json`.
   - Event has no `produces` edge pointing to it in `knowledge_graph.json`.
   - Event has no `producer_action` in `events.json`.
   - → Flag as `phantom_consumer`.

3. **Declared but not referenced (dead event):**
   - Event is in `events.json` but appears in no `produces` or `consumes`
     edge in `knowledge_graph.json`.
   - → Flag as `dead_event` (MINOR).

```json
{
  "detector": "B4-GRAPH-ORPHAN-EVENT",
  "severity": "MAJOR",
  "orphan_type": "orphan_producer",
  "event_id": "EV-0008",
  "event_name": "ContractExpired",
  "producer_action": "AC-0031 (ExpireContract)",
  "consumer_actions": [],
  "description": "Event 'ContractExpired' is emitted by ExpireContract action but no consumer is defined. Downstream effects of contract expiry (notifications, archival triggers) are unhandled.",
  "source_refs": [
    { "doc": "brd", "path": "brd/overview.md", "section": "§5.3" }
  ],
  "suggested_resolution": "Define a consumer action for ContractExpired in PRD (e.g., NotifyContractOwner, ArchiveContract) or document why no consumer is needed.",
  "reasoning_chain": [...]
}
```

---

### B5 — GRAPH-EDGE-CONFLICT: Conflicting Edge Detection

**Goal:** Identify nodes with logically incompatible outbound edges — where
two or more edges from the same source create a structural contradiction.

**Conflict patterns:**

| Pattern | Description | Severity |
|---|---|---|
| `creates` + `deletes` | Same action creates and deletes the same entity | BLOCKER |
| `performs` + `forbids` | Same role performs and is forbidden from the same action | BLOCKER |
| `transitions_to` duplicate | Two transitions from the same state on the same trigger to different target states | BLOCKER |
| `requires` + `blocks` | A requires B, but A also blocks B | BLOCKER |
| `authorizes` + `forbids` | Permission authorizes and a rule forbids the same action for same actor | BLOCKER |
| `depends_on` (mutual) | A depends_on B AND B depends_on A (caught by B1 also, but record here too) | BLOCKER |
| `produces` (duplicate) | Same action produces the same event twice from different sources | MAJOR |
| `owns` (shared) | Two roles both have `owns` edge to the same entity with `exclusive:true` | MAJOR |

**Algorithm:**
For every source node in `knowledge_graph.json`, group outbound edges by target.
Check each target group for conflicting label pairs from the table above.

```json
{
  "detector": "B5-GRAPH-EDGE-CONFLICT",
  "severity": "BLOCKER",
  "conflict_pattern": "performs + forbids",
  "source_node": { "id": "RL-0003", "name": "Advisor" },
  "target_node": { "id": "AC-0001", "name": "ApproveContract" },
  "conflicting_edges": [
    { "label": "performs", "basis": "explicit", "source_refs": [{ "doc": "prd", "path": "prd/contracts.md", "section": "§4.2" }] },
    { "label": "forbids", "basis": "explicit", "source_refs": [{ "doc": "brd", "path": "brd/overview.md", "section": "§6.2" }] }
  ],
  "description": "Role 'Advisor' simultaneously has a 'performs' edge (from PRD) and a 'forbids' edge (from BRD) to action 'ApproveContract'. These edges are logically incompatible.",
  "suggested_resolution": "Determine authoritative source: if BRD prohibition is correct, remove Advisor from PRD §4.2. If PRD grant is correct, update BRD §6.2.",
  "reasoning_chain": [...]
}
```

---

### B6 — ALIAS-SUSPECT: Unmerged Synonym Reporting

**Goal:** Identify concept pairs that are likely synonyms but are NOT
currently merged in `alias_index`. Report for human review only —
never auto-merge.

**Algorithm:**
1. For each pair of concepts (C1, C2) not in the same alias group:
   a. Compute normalized name similarity (Levenshtein distance ÷ max length).
   b. Check for co-reference in source_refs (same document, same section).
   c. Check for semantic role equivalence (same edges, same source_tier,
      same field_schema structure).
   d. Compute composite suspicion score:
      ```
      suspicion = 0.35 × name_similarity +
                  0.35 × co_reference_score +
                  0.30 × structural_equivalence
      ```
2. Flag pairs with `suspicion ≥ 0.75` as `alias_suspect`.
3. Distinguish:
   - **High confidence synonym** (suspicion ≥ 0.90): very likely the same concept
   - **Probable synonym** (0.75–0.89): likely, but needs review
   - **Possible synonym** (0.60–0.74): worth noting — logged but NOT flagged

**Important:** B6 findings are **ADVISORY ONLY**. Never modify `alias_index`.
Always marked `requires_human_review: true`. Severity is always MINOR.

```json
{
  "detector": "B6-ALIAS-SUSPECT",
  "severity": "MINOR",
  "requires_human_review": true,
  "concept_a": { "id": "RL-0001", "name": "Customer", "source_tier": "brd" },
  "concept_b": { "id": "RL-0007", "name": "Client", "source_tier": "prd" },
  "suspicion_score": 0.82,
  "evidence": {
    "name_similarity": 0.45,
    "co_reference": "Both appear in prd/contracts.md §1.1: 'The Customer (also referred to as Client in this document)'",
    "structural_equivalence": "Both have identical permission sets and same source_tier chain positions"
  },
  "recommendation": "HUMAN REVIEW — if Customer = Client, merge under canonical 'Customer' in alias_index. If they are distinct, add clarifying note to PRD §1.1.",
  "reasoning_chain": [...]
}
```

---

### B7 — GRAPH-RGAP: Responsibility Gap Detection

**Goal:** Identify actions in the knowledge graph that have no performing
role — orphan actions that exist in requirements or flows but cannot be
executed because no actor is assigned.

**Algorithm:**

1. For every node of type `action` in `knowledge_graph.json`:
   a. Count outbound `produces` edges and inbound `consumes` edges (event
      participation ≠ actor assignment).
   b. Count inbound `performs` edges (actual actor assignment).
   c. If `performs` count = 0 → potential orphan action.

2. Cross-reference with `index/responsibilities.json` (from A9):
   - If a responsibility record exists for this action with
     `accountability: responsible` or `accountable` → not orphaned.
   - If only `consulted` or `informed` exists → still orphaned (no one
     is responsible for execution).

3. Cross-reference with `permissions.json`:
   - If any role has a grant for this action → the action has a
     performer (flagged as B6-ALIAS possible name mismatch instead).

4. Distinct from D6-RGC: B7 operates on the graph structure (nodes and edge
   counts), while D6-RGC operates on source documents (textual analysis).
   Both may find the same orphan — Stage 5 merges duplicates.

**Severity:**
- BLOCKER: Action on a critical path (payment, security, approval) with no performer.
- MAJOR: Any other orphan action.

**Output schema:**
```json
{
  "detector": "B7-GRAPH-RGAP",
  "severity": "MAJOR",
  "orphan_action_id": "AC-0030",
  "orphan_action_name": "SendExpiryNotifications",
  "inbound_performs_edges": 0,
  "inbound_responsibility_records": 0,
  "event_participation": {
    "produces_events": ["EV-0012 (ContractExpiryWarning)"],
    "consumes_events": []
  },
  "description": "Action 'SendExpiryNotifications' emits ContractExpiryWarning event but has zero performs edges and zero responsibility records. No role is assigned to execute this action.",
  "suggested_resolution": "Assign a performing role (e.g., System) to SendExpiryNotifications via responsibilities.json or permissions.json.",
  "reasoning_chain": [...]
}
```

---

### B8 — GRAPH-DFLOW: Data Flow Mismatch Detection

**Goal:** Detect data flow inconsistencies in the knowledge graph where
the fields produced by an action do not match the fields consumed by a
downstream action connected via events — data producers and consumers are
linked but incompatible.

**Algorithm:**

1. Traverse `produces` and `consumes` edges in `knowledge_graph.json`:
   For each action A that `produces` event E, and action B that `consumes`
   event E, add a derived `dataflows_to` edge A → B.

2. For each `dataflows_to` path, check field compatibility:
   a. Read `events.json` for event E's `payload_fields`.
   b. Read the producer action's output fields from `field_schemas.json`
      (fields with `direction: "output"`).
   c. Read the consumer action's input fields from `field_schemas.json`
      (fields with `direction: "input"`).
   d. Compare produced fields vs consumed fields:
      - **Missing output fields:** Consumed by B but not produced by A.
      - **Type mismatch:** Same field name, different type/format.
      - **Optional-to-required mismatch:** Produced as nullable, consumed
        as required (runtime risk).

3. Flow-level check:
   - For each flow graph in `flow_graphs.json`, trace data flow through
     sequential nodes. If node N produces field X and node N+1 consumes
     field X, verify type compatibility.
   - If no event-based link exists between consecutive nodes → advisory
     (data may be passed via shared state, not events).

**Severity:**
- BLOCKER: Missing required field or type mismatch on a payment or
  compliance-critical data path.
- MAJOR: Missing optional field or nullable/required mismatch.
- MINOR: Data flow exists without event link (advisory — may indicate
  undocumented coupling).

**Output schema:**
```json
{
  "detector": "B8-GRAPH-DFLOW",
  "severity": "MAJOR",
  "source_action": { "id": "AC-0015", "name": "ProcessPayment" },
  "target_action": { "id": "AC-0020", "name": "GenerateInvoice" },
  "event": { "id": "EV-0003", "name": "PaymentConfirmed" },
  "field_mismatches": [
    {
      "field": "customer_id",
      "produced": null,
      "consumed": { "type": "string", "required": true }
    },
    {
      "field": "amount",
      "produced": { "type": "decimal", "nullable": false },
      "consumed": { "type": "decimal", "nullable": false }
    }
  ],
  "description": "Data flow from ProcessPayment to GenerateInvoice via PaymentConfirmed event is missing field 'customer_id' (required by consumer, not produced by producer). Amount field is compatible.",
  "suggested_resolution": "Emit customer_id as part of PaymentConfirmed payload, or have GenerateInvoice fetch customer_id from a shared data store.",
  "reasoning_chain": [...]
}
```

---

## Step 7 — Multi-Hop Traceability

BFS traversal at depth up to 5. Same as v5.

Detect `forbids` edges at depth 1 contradicting `performs` edges at depth 4+.
Detect entity lifecycle contradictions across 3+ chain hops.
Detect implicit ordering constraints from `depends_on` chains that contradict flow sequences.

---

## Step 8 — Explanation Chains

Every finding (TRC-1, TRC-2, TRC-FLOW, TRC-FLOW-ACTOR, TRC-FLOW-SCREEN,
TRC-MULTIHOP, B1–B8) MUST include a `reasoning_chain[]`.

---

## Output

```
traceability_findings.json        (TRC-* findings)
graph_health_findings.json        [NEW v6/v7 — B1–B8 findings]
index/knowledge_graph.json        (updated)
traceability_index.json.coverage  (updated)
```

### `graph_health_findings.json`

```json
{
  "stage": "2",
  "analyzer_version": "6.0",
  "generated_at": "...",
  "summary": {
    "B1_cycle_count": 0,
    "B2_deadend_count": 1,
    "B3_unreachable_count": 2,
    "B4_orphan_event_count": 1,
    "B5_edge_conflict_count": 1,
    "B6_alias_suspect_count": 3,
    "B7_responsibility_gap_count": 1,
    "B8_dataflow_mismatch_count": 1
  },
  "findings": [...]
}
```

---

## Rules

- Read `index/*.json` only (including new v6/v7 files).
- Always write: `traceability_findings.json`, `graph_health_findings.json`,
  updated `traceability_index.json.coverage`, and `index/knowledge_graph.json`.
- B6 findings MUST be `requires_human_review: true`. Never auto-merge.
- B1–B5 findings are structural contradictions — severity BLOCKER or MAJOR.
- B2 dead-end detection must distinguish terminal states from dead-ends.
- B3 unreachable detection must allow exception-path reachability.
- B4 must cross-reference both `events.json` and `knowledge_graph.json` edges.
- B7 must cross-reference `responsibilities.json` and knowledge graph `performs` edges for orphan detection.
- B8 must traverse `produces`→`consumes` paths and check field compatibility via `field_schemas.json` and `events.json`.
- Multi-hop traversal depth: up to 5 hops.
- Explanation chains are mandatory on every finding.
- Include ALL edge types: all 23 labels must be recognized.
- Include ALL node types: entity, role, requirement, business_rule, state,
  action, permission, flow_step, ia_node, layout_screen, api_endpoint, event,
  external_system, data_model.
- Fully domain-agnostic.
- Target execution time: **< 10 seconds**.
