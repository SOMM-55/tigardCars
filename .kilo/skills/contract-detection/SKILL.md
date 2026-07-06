---
name: contract-detection
description: >
  Used by `sdd-analyzer` (and applicable for other analyzers when identifying blocking artifacts). What counts as a contract and must be `blocking: true`.

---

## Definition

A contract is any artifact whose **shape** is consumed by another task. Consumers cannot start until the contract is finalized.

## Always-Blocking Artifacts

- Database schemas and migrations
- OpenAPI / Swagger / Protobuf specs
- Shared types / Pydantic models
- Auth middleware (every protected endpoint depends on it)
- Event / webhook schemas
- Configuration schemas
- Public SDK interfaces

## Detection Test

Ask: "If task X is incomplete, does some other task fail to build or fail at runtime?"

- Yes → blocking
- No → not blocking

## Common Mistakes

- **Treating implementation as a contract.** The OpenAPI spec is the contract, not the endpoint implementation. The migration is blocking, not the entity-class.
- **Forgetting cross-task wiring.** After marking blocking, walk consumers and confirm `input_contracts` references resolve to your blocking task's `outputs`.
