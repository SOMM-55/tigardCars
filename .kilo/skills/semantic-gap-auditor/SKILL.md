---
name: semantic-gap-auditor
version: "6.0"
description: >
  Stage 4 of the gap-analyzer pipeline. Reads all index/*.json files plus
  both findings files from Stages 2 and 3. Detects semantic and logic-level
  gaps that are invisible to traceability and direct-value analysis.
  v5 capabilities preserved: MDC (missing domain concepts), MSC (missing
  screen), MPC (missing permission check), MPH (missing phase), MFC (missing
  flow continuation). v6 adds a Decision Table / SMT-lite analyzer (D1–D5)
  that operates on the normalized predicate logic extracted by Stage 1 A5.
  This is the highest-ROI stage for finding hidden bugs.
  Never reads raw source documents.
---

# Semantic Gap Auditor v6

## Mission

Find logical errors and semantic gaps that survive all previous stages —
contradictions hidden in conditional logic, unreachable conditions, coverage
holes in decision tables, ambiguous rule priority, and subsumed rules.
In v6, the A5 predicate normalization from Stage 1 provides the structured
logical form needed to run SMT-lite analysis without a full constraint solver.

---

## Input

```
index/entities.json
index/roles.json
index/requirements.json
index/business_rules.json       (with structured_predicate from A5)
index/states.json
index/actions.json
index/permissions.json
index/traceability_index.json
index/flow_graphs.json
index/knowledge_graph.json
index/events.json
index/enum_registry.json
index/field_schemas.json
index/format_specs.json
traceability_findings.json       (Stage 2 output)
graph_health_findings.json       (Stage 2 output)
consistency_findings.json        (Stage 3 output)
index/responsibilities.json           [NEW v7 — from Stage 1 A9]
index/extraction_quality_report.json
```

Never reads raw source documents.

---

## Preserved from v5: Semantic Detectors

### MDC — Missing Domain Concept
A role, screen, action, or entity referenced in a flow/permission without
being defined anywhere in the source documents.

### MSC — Missing Screen
A flow step references a UI screen that does not exist in the IA or Layout.

### MPC — Missing Permission Check
An action is performed in a flow by an actor, but no corresponding permission
is defined in `permissions.json`.

### MPH — Missing Phase Assignment
A requirement or entity is defined but assigned to no MVP/phase/sprint.

### MFC — Missing Flow Continuation
A flow step has no `next_step` and is not marked as a terminal node.

---

## NEW in v6: Decision Table / SMT-lite Analyzer (D1–D5) ✨

These detectors operate on `structured_predicate` records from Stage 1 A5.
They implement a lightweight Satisfiability Modulo Theories (SMT) approach:
rather than using a full constraint solver, they apply domain-specific rules
and symbolic reasoning to detect the five most common predicate logic errors.

**Priority:** D-series detectors run FIRST (highest ROI). They catch hidden
bugs that no other stage can find.

---

### D1 — PLC: Predicate Logic Conflict (Same Condition → Different Results)

**Goal:** Detect rules where two or more conditions are logically equivalent
(or overlapping) but produce different results — a classic logic contradiction.

**Algorithm:**

1. Load all `structured_predicate` records from `business_rules.json` and
   `requirements.json`.

2. Build condition fingerprints: for each predicate, sort conditions by
   `{variable, operator, value}` and hash to a canonical form.

3. Group predicates by condition fingerprint. For each group with ≥ 2 records:
   a. Compare `result` values.
   b. If results differ → PLC (same condition, different outcome).
   c. If results are same but `result_type` differs → MAJOR (ambiguous
      enforcement mechanism).

4. Partial overlap detection:
   - If predicate A's condition set is a subset of predicate B's condition set
     AND their results differ → this is D5-SUC (handled there).
   - If predicates share ≥ 50% of conditions but have different non-overlapping
     conditions → both may fire on the same input → D4-ORC (handled there).

5. Condition normalization before comparison:
   - `role = "Manager"` ≡ `role IN ["Manager"]`
   - `amount > 100 AND amount > 50` → simplify to `amount > 100`
   - `amount > 500000 AND amount <= 1000000` → `amount BETWEEN (500000, 1000000]`

**Severity:**
- BLOCKER: The conflicting rules govern a financial, security, or approval
  decision (result_type = permission, state_transition, or payment).
- MAJOR: Other result types.

**Output schema:**
```json
{
  "detector": "D1-PLC",
  "severity": "BLOCKER",
  "conflict_type": "same_condition_different_result",
  "rule_a": {
    "concept_id": "BR-0012",
    "concept_name": "ContractApprovalRule",
    "conditions": [
      { "variable": "contract.amount", "operator": ">", "value": 1000000 },
      { "variable": "user.role", "operator": "=", "value": "Manager" }
    ],
    "result": "auto_approved",
    "source_ref": { "doc": "brd", "path": "brd/overview.md", "section": "§5.1" }
  },
  "rule_b": {
    "concept_id": "RQ-0034",
    "concept_name": "HighValueApprovalRequirement",
    "conditions": [
      { "variable": "contract.amount", "operator": ">", "value": 1000000 },
      { "variable": "user.role", "operator": "=", "value": "Manager" }
    ],
    "result": "requires_dual_approval",
    "source_ref": { "doc": "prd", "path": "prd/contracts.md", "section": "§6.2" }
  },
  "condition_fingerprint": "contract.amount>1000000 AND user.role=Manager",
  "result_conflict": {
    "rule_a_result": "auto_approved",
    "rule_b_result": "requires_dual_approval"
  },
  "description": "BRD BR-0012 and PRD RQ-0034 have identical conditions (amount > 1M by Manager) but produce opposite results: BRD says auto-approve, PRD requires dual approval. A system implementing both rules is non-deterministic.",
  "suggested_resolution": "Determine authoritative source (BRD or PRD). If high-value contracts require dual approval, remove auto-approve from BRD §5.1.",
  "reasoning_chain": [...]
}
```

---

### D2 — DRC: Dead Rule / Unreachable Condition

**Goal:** Detect conditions that can never be simultaneously true — rules
that can never fire, creating dead code in business logic.

**Algorithm:**

1. For each `structured_predicate`, check for internal contradictions:
   - **Numeric contradiction:** `x > 10 AND x < 5` — no value of x satisfies both.
   - **Enum contradiction:** `status = APPROVED AND status = REJECTED` — mutually exclusive.
   - **Role contradiction:** `role = Manager AND role = Advisor` — single-role system.
   - **Temporal contradiction:** `date > 2025-01-01 AND date < 2024-01-01`.

2. For each condition `c_i` in a predicate, check against all other conditions
   `c_j` in the same predicate:
   - If `c_i` specifies `x > A` and `c_j` specifies `x < B` where `A >= B` →
     dead condition (no values satisfy both).
   - If `c_i` specifies `x IN [set_A]` and `c_j` specifies `x NOT IN [set_B]`
     where `set_A ⊆ set_B` → all values in set_A are excluded → dead rule.
   - If `c_i` and `c_j` use the same variable with `=` to different values →
     dead rule (a variable cannot equal two different values simultaneously).

3. Cross-rule dead conditions:
   After checking within-predicate contradictions, check pairs of predicates
   that are supposed to be applied together (linked by `AND` connectors or
   sequential in a flow):
   - If rule A fires only when `status = PENDING` and rule B (which must fire
     before A) transitions status to `APPROVED` (never `PENDING`) → A is
     unreachable in this flow path.

**Severity:**
- BLOCKER: Dead rule on a security or financial decision.
- MAJOR: Dead rule on an approval or state transition.
- MINOR: Dead rule on a UI display or notification.

**Output schema:**
```json
{
  "detector": "D2-DRC",
  "severity": "MAJOR",
  "rule_id": "BR-0019",
  "rule_name": "InvoiceAmountValidation",
  "dead_condition": {
    "condition_a": { "variable": "invoice.amount", "operator": ">", "value": 10000 },
    "condition_b": { "variable": "invoice.amount", "operator": "<", "value": 5000 },
    "contradiction_type": "numeric_range_impossible",
    "explanation": "amount > 10000 AND amount < 5000 — no value satisfies both constraints"
  },
  "full_predicate": {
    "conditions": [
      { "variable": "invoice.amount", "operator": ">", "value": 10000 },
      { "variable": "invoice.amount", "operator": "<", "value": 5000 },
      { "variable": "invoice.status", "operator": "=", "value": "PENDING" }
    ],
    "result": "block_invoice"
  },
  "source_ref": { "doc": "prd", "path": "prd/invoices.md", "section": "§4.3" },
  "description": "Rule BR-0019 can never fire because it requires invoice.amount > 10000 AND invoice.amount < 5000 simultaneously. This rule is dead code — the block_invoice action is unreachable via this rule.",
  "suggested_resolution": "Fix the numeric range. If the intent is to block invoices between 5000 and 10000, use: amount >= 5000 AND amount <= 10000. If the intent is different, clarify the rule.",
  "reasoning_chain": [...]
}
```

---

### D3 — CGC: Coverage Gap in Decision Table

**Goal:** Detect cases where a set of rules does NOT completely cover all
possible input combinations — leaving unhandled cases that default to
undefined behavior.

**Algorithm:**

1. Identify decision tables: groups of rules that share the same variable set
   and govern the same outcome type (same `result_type` and same `concept`).

2. For each decision table (group of related predicates):
   a. Extract all unique variables referenced across the group.
   b. For each variable, extract its domain:
      - Numeric: determine range from `min`/`max` in `field_schemas.json`.
      - Enum: get `declared_values` from `enum_registry.json`.
      - Boolean: domain = {true, false}.
   c. Compute the Cartesian product of all variable domains.
   d. For each point in the product space, check which rules (if any) cover it.
   e. Points covered by NO rule → coverage gap.

3. Gap reporting:
   - Identify the specific input combination(s) not covered.
   - Assess impact: what happens when an uncovered input is received?
     (undefined behavior, system error, or silent failure)

4. Optimization:
   - For large variable domains (numeric ranges), use interval arithmetic
     rather than enumerating all points.
   - Represent gaps as intervals or enum value sets, not individual points.

**Severity:**
- BLOCKER: Coverage gap in a payment processing, approval, or authentication decision.
- MAJOR: Coverage gap in any other business-critical decision.
- MINOR: Coverage gap in a display or notification rule.

**Output schema:**
```json
{
  "detector": "D3-CGC",
  "severity": "BLOCKER",
  "decision_table": "ContractApprovalMatrix",
  "variables": [
    { "name": "contract.amount", "type": "decimal", "domain": "[0, ∞)" },
    { "name": "user.role", "type": "enum", "domain": ["Manager", "Advisor", "Analyst"] }
  ],
  "defined_rules": [
    {
      "rule_id": "BR-0012",
      "covers": { "contract.amount": "(1000000, ∞)", "user.role": ["Manager"] }
    },
    {
      "rule_id": "BR-0013",
      "covers": { "contract.amount": "[0, 1000000]", "user.role": ["Manager", "Advisor"] }
    }
  ],
  "coverage_gaps": [
    {
      "uncovered_region": { "contract.amount": "any", "user.role": ["Analyst"] },
      "description": "No rule covers what happens when an Analyst attempts to act on a contract of any amount.",
      "impact": "Undefined behavior — system may default to deny or allow depending on implementation"
    }
  ],
  "description": "The contract approval decision table has no rule for role=Analyst. For any contract amount, an Analyst's request results in undefined behavior.",
  "suggested_resolution": "Add an explicit rule for role=Analyst (either deny all, or define their approval scope). Do not rely on implicit defaults.",
  "reasoning_chain": [...]
}
```

---

### D4 — ORC: Overlapping Rules with Ambiguous Priority

**Goal:** Detect cases where two or more rules can fire simultaneously for
the same input, and the priority or expected result is ambiguous.

**Algorithm:**

1. For each pair of rules (R_i, R_j) in the same decision table:
   a. Check if their condition sets have a non-empty intersection
      (can both be satisfied by the same input?).
   b. If intersection is non-empty → potential overlap.
   c. Check if their `result` values are identical → acceptable overlap
      (redundant but not contradictory); log as MINOR if coverage is helpful.
   d. If results differ → D4 finding (ambiguous priority).

2. Intersection computation:
   - Numeric: intervals overlap if max(lower bounds) < min(upper bounds).
   - Enum: `set_A ∩ set_B ≠ ∅`.
   - Boolean: both conditions on same variable with same value.
   - Mixed: compute per-variable intersection, then check if all variable
     intersections are non-empty simultaneously.

3. Priority resolution check:
   - If rules are in a document that specifies explicit priority ordering
     (e.g., "Rule 1 takes precedence over Rule 2") → downgrade to MINOR.
   - If no priority is specified → MAJOR or BLOCKER based on result type.

4. Distinguish from D1-PLC:
   - D1: conditions are IDENTICAL (exact same input point).
   - D4: conditions OVERLAP (same input satisfies both, but conditions are
     not identical — one may be a subset of the other).

**Severity:**
- BLOCKER: Overlap with different financial or security results and no
  defined priority.
- MAJOR: Overlap with different operational results (approval, access).
- MINOR: Overlap with identical results (redundant but harmless).

**Output schema:**
```json
{
  "detector": "D4-ORC",
  "severity": "MAJOR",
  "overlap_type": "partial_condition_overlap",
  "rule_a": {
    "concept_id": "BR-0020",
    "concept_name": "SeniorManagerApproval",
    "conditions": [
      { "variable": "contract.amount", "operator": ">", "value": 500000 },
      { "variable": "user.seniority", "operator": ">=", "value": 5 }
    ],
    "result": "single_approval_sufficient"
  },
  "rule_b": {
    "concept_id": "BR-0021",
    "concept_name": "HighValueDualApproval",
    "conditions": [
      { "variable": "contract.amount", "operator": ">", "value": 750000 }
    ],
    "result": "requires_dual_approval"
  },
  "overlap_region": {
    "contract.amount": "(750000, ∞)",
    "user.seniority": "[5, ∞)"
  },
  "ambiguity": "For contracts > 750000 submitted by a senior manager (seniority ≥ 5), both rules fire: BR-0020 says single approval is sufficient, BR-0021 requires dual approval.",
  "priority_defined": false,
  "description": "Rules BR-0020 and BR-0021 overlap for amount > 750000 AND seniority ≥ 5, producing conflicting approval requirements with no defined priority.",
  "suggested_resolution": "Add a priority clause: 'If both BR-0020 and BR-0021 apply, BR-0021 takes precedence.' Or refine BR-0020 to exclude amounts > 750000.",
  "reasoning_chain": [...]
}
```

---

### D5 — SUC: Subsumed Rule Conflict

**Goal:** Detect cases where one rule's conditions are fully contained within
another rule's conditions (subsumption), but their results conflict — making
the more specific rule's intent impossible to achieve.

**Algorithm:**

1. For each pair of rules (R_i, R_j) in the same decision table:
   a. Check if condition set of R_i is a **proper subset** of condition set of R_j:
      - Every condition in R_i is satisfied whenever R_j's conditions are satisfied.
      - But R_j has additional conditions that R_i does not.
      - → R_j is a specialization of R_i.
   b. If R_j's result conflicts with R_i's result → D5-SUC.
      (R_j tries to create an exception to R_i, but R_i also fires for all
      inputs that satisfy R_j — the exception is swallowed by the general rule.)

2. Subsumption check:
   - Condition A subsumes condition B if every value satisfying B also
     satisfies A (A is the more general condition).
   - Example: `amount > 0` subsumes `amount > 1000000` (every value > 1M
     is also > 0, but not vice versa).
   - For enum: `role IN ["Manager", "Advisor"]` subsumes `role = "Manager"`.

3. Conflict check:
   - If R_i (general) says `result: allow` and R_j (specific, subsumed) says
     `result: deny`, and no priority rule resolves which takes precedence →
     D5-SUC finding.
   - If priority is explicitly defined (specific overrides general) → no
     finding (this is the classic override pattern, which is valid).

**Severity:**
- BLOCKER: Subsumed rule that was clearly intended to create a security or
  financial exception (deny subsumed by allow, or stricter threshold subsumed
  by looser threshold).
- MAJOR: Subsumed rule that affects operational outcomes.
- MINOR: Subsumed rule with advisory results.

**Output schema:**
```json
{
  "detector": "D5-SUC",
  "severity": "BLOCKER",
  "subsumption_type": "specific_subsumed_by_general",
  "general_rule": {
    "concept_id": "BR-0005",
    "concept_name": "AdvisorPermissions",
    "conditions": [
      { "variable": "user.role", "operator": "=", "value": "Advisor" }
    ],
    "result": "can_create_contracts",
    "source_ref": { "doc": "prd", "path": "prd/contracts.md", "section": "§4.1" }
  },
  "specific_rule": {
    "concept_id": "BR-0022",
    "concept_name": "AdvisorContractValueLimit",
    "conditions": [
      { "variable": "user.role", "operator": "=", "value": "Advisor" },
      { "variable": "contract.amount", "operator": ">", "value": 1000000 }
    ],
    "result": "cannot_create_contracts",
    "source_ref": { "doc": "brd", "path": "brd/overview.md", "section": "§6.3" }
  },
  "subsumption_path": "BR-0022 conditions ⊂ BR-0005 conditions: BR-0005 fires for ALL Advisors, including those with amount > 1M. BR-0022's deny result is overridden by BR-0005's allow.",
  "priority_defined": false,
  "description": "BR-0022 intends to prevent Advisors from creating contracts over 1M, but BR-0005 grants all Advisors contract creation rights without an amount limit. BR-0022 is subsumed and its restriction can never take effect without explicit rule priority.",
  "suggested_resolution": "Add a priority clause: 'BR-0022 takes precedence over BR-0005 when amount > 1M.' Or add an amount condition to BR-0005: can_create_contracts when amount <= 1M.",
  "reasoning_chain": [...]
}
```

---

### D6 — RGC: Responsibility Gap

**Goal:** Detect actions that are required by the system but have no
performing role assigned — an action exists in flows or requirements but
nobody is responsible for executing it.

**Algorithm:**

1. Collect all actions from `actions.json` and flow steps from
   `flow_graphs.json`.

2. For each action, check for a `performs` edge in `knowledge_graph.json`
   connecting any role to this action.

3. If no `performs` edge exists:
   a. Check `responsibilities.json` (A9) for any `responsible` or
      `accountable` assignment for this action.
   b. Check `permissions.json` for any role that has a grant for this action.
   c. If all three checks fail → RGC finding.

4. Flow-level check:
   - For each flow step, check if the step assigns an actor (`actor` field).
   - If the step has no actor and no default actor is defined for the flow
     → RGC finding for the flow step.

5. Implicit resolution check:
   - If an action's parent flow has an owner → owner is implicitly
     responsible for all unassigned steps in the flow (no finding).
   - If no parent flow owner and no explicit actor → RGC.

**Severity:**
- BLOCKER: Action on a security, payment, or compliance-critical path
  with no assigned role.
- MAJOR: Operational action with no assigned role.
- MINOR: Informational action (notification, logging) with no assigned role.

**Output schema:**
```json
{
  "detector": "D6-RGC",
  "severity": "MAJOR",
  "action_id": "AC-0023",
  "action_name": "ArchiveExpiredContracts",
  "flow_context": "Contract lifecycle management flow",
  "source_ref": { "doc": "prd", "path": "prd/contracts.md", "section": "§7.2" },
  "description": "Action 'ArchiveExpiredContracts' is defined in PRD §7.2 and appears in the contract lifecycle flow, but no role is assigned to perform this action. Expired contracts will never be archived.",
  "suggested_resolution": "Add a responsible role (e.g., System, Admin) to the ArchiveExpiredContracts action in PRD or assign an actor in the flow graph.",
  "reasoning_chain": [...]
}
```

---

### D7 — SLC: SLA Composition Gap

**Goal:** Detect cases where a composite SLA (end-to-end) is not satisfiable
by the sum of its sub-SLAs — for example, a 24h end-to-end SLA where the
combined sub-step SLAs total 30h.

**Algorithm:**

1. Collect all `temporal_specs[]` records (A2) that have an aggregation
   relationship (linked via `aggregations[]` from A8).

2. For each SLA with sub-SLA components:
   a. Sum `normalized_seconds` of all sub-SLA components.
   b. Compare to parent SLA's `normalized_seconds`.
   c. If sub-SLA sum > parent SLA → SLC finding (parent SLA is impossible).

3. Chain SLA check (multi-tier):
   - If component A has SLA of 10h, and A is decomposed into A1 (6h) + A2 (6h)
     = 12h, both A1+A2 exceed A AND A1+A2 > parent SLA → compound gap.
   - Flag the deepest decomposition level where the gap first appears.

4. Business-day vs calendar-day:
   - If parent SLA is in calendar days and sub-SLAs are in business days
     (or vice versa), normalize both to seconds before comparing.
   - Flag unit mismatch separately (also captured by C2-TUC).

**Severity:**
- BLOCKER: Parent SLA is a contractual or regulatory commitment that
  sub-SLAs cannot satisfy.
- MAJOR: Operational SLA where sub-SLA excess is < 50% of parent.
- MINOR: Internal SLA with advisory implications.

**Output schema:**
```json
{
  "detector": "D7-SLC",
  "severity": "BLOCKER",
  "parent_sla": {
    "concept": "end_to_end_contract_approval_sla",
    "normalized_seconds": 86400,
    "raw_text": "Contract approval must complete within 24 hours"
  },
  "sub_slas": [
    { "step": "SubmitContract", "normalized_seconds": 36000, "raw_text": "10 hours" },
    { "step": "ManagerReview", "normalized_seconds": 43200, "raw_text": "12 hours" },
    { "step": "FinalApproval", "normalized_seconds": 14400, "raw_text": "4 hours" }
  ],
  "combined_sub_sla_seconds": 93600,
  "excess_seconds": 7200,
  "excess_pct": 8.3,
  "description": "End-to-end contract approval SLA is 24h (86400s), but sub-step SLAs sum to 26h (93600s). The parent SLA is impossible to meet by 2 hours even if all steps execute perfectly sequentially.",
  "suggested_resolution": "Reduce sub-step SLAs (e.g., ManagerReview from 12h to 10h), or increase parent SLA to 26h, or document parallel execution assumption.",
  "reasoning_chain": [...]
}
```

---

### D8 — NSC: Negative Space Gap

**Goal:** Detect conditional rules that specify what happens when a condition
is TRUE but are silent about what happens when it is FALSE — missing negative
cases that create undefined behavior.

**Algorithm:**

1. For each `structured_predicate` in `business_rules.json` with at least
   one condition:
   a. Extract the condition set: `{variable, operator, value}` pairs.
   b. For each condition, compute the negation:
      - `x > 5` → negated: `x <= 5`
      - `x = "APPROVED"` → negated: `x != "APPROVED"`
      - `x IN [A, B]` → negated: `x NOT IN [A, B]`

2. Check if any rule in the same decision table covers the negated condition.
   - If no rule covers the negated case for ANY condition → NSC finding.
   - If some conditions have negative coverage but others don't → report
     the specific uncovered negations.

3. Default behavior check:
   - If the document set has an explicit "deny by default" or "allow by
     default" policy → no finding for that direction.
   - Example: "All actions are denied unless explicitly permitted" → deny
     is the default, so missing negative cases for permission rules are
     acceptable (the default handles them).

4. Implicit negation detection:
   - Some rules imply their negation through context (e.g., a rule that
     says "Managers can approve" implicitly means "non-Managers cannot
     approve" only if there's a deny-by-default policy).
   - Without a default policy, the negative case is a gap.

**Severity:**
- BLOCKER: Missing negative case on a security, access control, or payment rule.
- MAJOR: Missing negative case on an approval or state transition rule.
- MINOR: Missing negative case on a display or notification rule.

**Output schema:**
```json
{
  "detector": "D8-NSC",
  "severity": "MAJOR",
  "rule_id": "BR-0012",
  "rule_name": "ContractApprovalRule",
  "positive_condition": { "variable": "user.role", "operator": "=", "value": "Manager" },
  "result": "can_approve_contracts",
  "negated_condition": { "variable": "user.role", "operator": "!=", "value": "Manager" },
  "negation_uncovered": true,
  "default_policy": "none_defined",
  "description": "Rule BR-0012 specifies that Managers can approve contracts, but no rule defines what happens when the user is NOT a Manager. Without a deny-by-default policy, non-Manager behavior is undefined.",
  "suggested_resolution": "Add an explicit rule: 'If user.role != Manager → cannot_approve_contracts', or document a default-deny policy for all approval actions.",
  "reasoning_chain": [...]
}
```

---

### D9 — PCC: Precondition Chain Break

**Goal:** Detect actions whose preconditions cannot be satisfied by any
predecessor action in the flow graph — the action requires a condition
that no prior step establishes.

**Algorithm:**

1. For each flow graph in `flow_graphs.json`:
   a. Build the directed path from `start_node` through each sequence.
   b. For each node (action), collect its preconditions:
      - From `structured_predicate.conditions` of any rule governing this action.
      - From `states.json` if the action requires a specific entity state.
   c. Walk the predecessor chain backward from each action.

2. For each precondition, verify it is satisfiable:
   - **State precondition:** action requires `status = APPROVED`. Walk
     predecessors — does any predecessor transition entity to APPROVED?
   - **Data precondition:** action requires `amount > 0`. Walk predecessors
     — does any predecessor set or validate the amount?
   - **Role precondition:** action requires `Manager` role. Walk
     predecessors — does any predecessor verify the user is a Manager?

3. If a precondition cannot be satisfied by any direct predecessor:
   - Check 2+ hops back (the precondition may be established earlier in
     the flow).
   - If still unsatisfiable → PCC finding.

4. Conditional flow paths:
   - If the flow has parallel branches, check each branch independently.
   - A precondition may be satisfiable via one branch but not another
     → flag the specific branch with the broken chain.

**Severity:**
- BLOCKER: Precondition required for a payment, security, or compliance action.
- MAJOR: Precondition required for an approval or state transition.
- MINOR: Informational precondition.

**Output schema:**
```json
{
  "detector": "D9-PCC",
  "severity": "MAJOR",
  "action_id": "AC-0018",
  "action_name": "DisbursePayment",
  "flow_id": "FLOW-0003",
  "flow_name": "PaymentDisbursement",
  "precondition": {
    "type": "state_precondition",
    "description": "Contract.status must be APPROVED before payment can be disbursed"
  },
  "predecessor_actions": ["AC-0015 (ValidateContract)", "AC-0016 (CalculateAmount)"],
  "chain_break": "Neither ValidateContract nor CalculateAmount transitions Contract to APPROVED status. APPROVED is only reached via AC-0017 (ApproveContract), which is not a predecessor of DisbursePayment in this flow.",
  "description": "DisbursePayment requires Contract.status = APPROVED, but its predecessors (ValidateContract, CalculateAmount) do not establish this state. The APPROVED state is set by ApproveContract, which is not in DisbursePayment's predecessor chain.",
  "suggested_resolution": "Add ApproveContract as a predecessor of DisbursePayment, or remove the state precondition from DisbursePayment if it is not required.",
  "reasoning_chain": [...]
}
```

---

## Predicate Analysis Execution Order

Run in this order (each informs the next):

```
1.  D2-DRC  → prune dead rules before analyzing overlaps
2.  D1-PLC  → find exact condition conflicts
3.  D5-SUC  → find subsumption conflicts (uses results from D1)
4.  D4-ORC  → find overlapping rules (uses results from D2 and D5)
5.  D3-CGC  → find coverage gaps (uses alive rules after D2 pruning)
6.  D6-RGC  → find responsibility gaps (uses alive actions only)
7.  D7-SLC  → find SLA composition gaps (uses aggregations and temporal_specs)
8.  D8-NSC  → find negative space gaps (uses alive rules from D2 pruning)
9.  D9-PCC  → find precondition chain breaks (uses flow_graphs)
```

---

## Output

### File: `semantic_findings.json`

```json
{
  "stage": "4",
  "version": "7.0",
  "generated_at": "...",
  "predicate_analysis": {
    "total_predicates_analyzed": 42,
    "dead_rules": 1,
    "logic_conflicts": 2,
    "coverage_gaps": 3,
    "overlapping_rules": 2,
    "subsumed_rules": 1,
    "responsibility_gaps": 1,
    "sla_composition_gaps": 1,
    "negative_space_gaps": 2,
    "precondition_breaks": 1
  },
  "summary": {
    "total_findings": 26,
    "blocker": 6,
    "major": 13,
    "minor": 7,
    "by_detector": {
      "D1-PLC": 2,
      "D2-DRC": 1,
      "D3-CGC": 2,
      "D4-ORC": 1,
      "D5-SUC": 1,
      "D6-RGC": 1,
      "D7-SLC": 1,
      "D8-NSC": 2,
      "D9-PCC": 1,
      "MDC": 4,
      "MSC": 3,
      "MPC": 3,
      "MPH": 3,
      "MFC": 2
    }
  },
  "findings": [...]
}
```

---

## Rules

- Run D-series detectors FIRST (highest ROI — execute before MDC/MSC/MPC).
- Run D-detectors in order: D2 → D1 → D5 → D4 → D3 → D6 → D7 → D8 → D9.
- D1–D9 MUST operate on normalized `structured_predicate` from `business_rules.json`.
- D2 dead-rule pruning result MUST be passed to D3 (do not include dead rules in coverage analysis).
- D3 MUST use variable domains from `field_schemas.json` and `enum_registry.json`.
- D4 MUST distinguish between redundant overlaps (same result, MINOR) and
  ambiguous overlaps (different result, MAJOR/BLOCKER).
- D5 MUST check for explicit priority declarations before flagging.
- D6 MUST cross-reference `responsibilities.json`, `permissions.json`, and knowledge graph `performs` edges.
- D7 MUST use `aggregations[]` (A8) and `temporal_specs[]` (A2) for SLA composition analysis.
- D8 MUST check for a document-level default policy before flagging missing negations.
- D9 MUST traverse 2+ hops backward in flow graphs for precondition verification.
- Preserve ALL v5 detectors: MDC, MSC, MPC, MPH, MFC.
- Cross-reference with Stage 2 and Stage 3 findings (avoid duplicates).
- Explanation chains are mandatory on every finding.
- Fully domain-agnostic.
- Target execution time: **< 20 seconds** for 50 predicates.
