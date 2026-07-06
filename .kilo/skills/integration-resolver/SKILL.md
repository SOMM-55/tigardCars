---
name: integration-resolver
description: >
  Use this skill when running the Integration Resolution phase — after integration-discovery-agent
  has completed and the Architecture Manifest (discovery.md) exists.

  Trigger when the user says: "resolve integrations", "fetch integration docs",
  "continue integration", "run resolver", or "next integration batch".

  This skill reads the Architecture Manifest, processes one batch of unresolved
  Components, fetches documentation from Memoria MCP (Internal Ecosystem) or
  Context7 MCP (External Solution), normalizes it into structured Integration
  Knowledge, saves one file per Component, and updates the Manifest's status.

  Can be run multiple times — each run resumes from where the last stopped.
  Requires integration-discovery-agent to have completed first.
---

# Integration Resolver Skill

This skill handles documentation retrieval and normalization for the
Integration phase. It reads state from the Architecture Manifest and saves
structured Integration Knowledge per Component.

---

## What This Skill Does

1. Reads the Architecture Manifest (discovery.md) — the only input needed
2. Identifies the next batch of `ready` Components
3. Calls Memoria MCP for `Internal Ecosystem` Components
4. Calls Context7 MCP for `External Solution` Components
5. Generates Integration Knowledge directly from the Manifest for `Project Core` Components (no MCP call)
6. Normalizes retrieved documentation into structured Integration Knowledge
7. Saves Integration Knowledge to `.nitro/steering/integration/{name}.md`
8. Updates the Architecture Manifest's status after each Component

## What This Skill Does NOT Do

- Read project documentation (BRD, PRD, SDD, etc.)
- Re-run Component discovery or re-decide a Component's Source Strategy
- Save raw, unstructured MCP output as the final file
- Make architecture decisions
- Generate the final consolidated project documentation (a separate, later step)

## Resume Behavior

Every session is stateless from the agent's perspective. State lives in the
Architecture Manifest. The agent reads it, finds pending items, and
continues. No memory of previous sessions is needed or used. The agent must
never create duplicate files or duplicate Manifest rows when resuming.

## Reference Files

- `references/batch-strategy.md` — batch size rules and context management
- `references/file-format.md` — per-Component Integration Knowledge file format
- `references/mcp-strategy.md` — how to query Memoria and Context7 effectively, and how to handle `Project Core` Components
