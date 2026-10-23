---
name: clean-architecture-persistence
description: Implement Drizzle schemas, migrations, owner-scoped repositories, and external persistence adapters from Domain ports.
---

# Clean Architecture Persistence

Inspect Domain ports, table owners, existing schema/helpers, and the actual transaction adapter. Preserve the repository's package placement; storage code may live in database or infrastructures, while composition stays outside core. Read only references needed for the change.

## Workflow

1. For repository/query changes, read [ownership and transactions](references/repository-boundaries.md).
2. For tables, relations, indexes, or migrations, read [Drizzle patterns](references/drizzle-patterns.md). Use the installed ORM version and existing typed helpers.
3. For concrete ports, row mapping, external adapters, or DI, read [adapter patterns](references/infrastructure-patterns.md).
4. Update affected ports, callers, wiring, exports, fixtures, and migration/catalog handoffs together.

## Boundaries

- A repository must not inject, construct, call, or indirectly use another repository. It accesses only its owned tables, including aggregate-owned children/history.
- Cross-owner JOINs, subqueries, views/functions/triggers, helpers, read projections, locks, and audit writes are not exceptions. Application Services coordinate owner ports; a generic base operates only on the caller's own tables.
- Keep ORM/query/connection types inside persistence. Return deliberately mapped Domain-compatible values; casts do not remove internal columns.
- Preserve tenant predicates, atomic revision/uniqueness constraints, native decoders, batch semantics, and shared transaction participation. Do not replace them with Application-only checks.
- Store source facts, decisions, integrity keys, and necessary history; derive reproducible values. Preserve historical inputs before removing derived fields.
- Import helpers directly; keep standalone helpers outside class files. Use explicit types without suppressions and Thai JSDoc for [changed conditions](../clean-architecture-docs/references/conditions.md).
- Repositories receive required `now`/`asOf` and computed cutoffs; they do not read the clock. Audit stamps and column defaults are exceptions. For time/zone changes, read [time handling](../clean-architecture-foundation/references/time-handling.md).

## Verify

Review generated migration SQL/snapshots; keep applied migrations immutable. Applying a migration is distinct from generating/reviewing it. Run affected type/lint checks and relevant isolated DB tests for tenant scope, batching, filtering/pagination, decoding, rollback, and locks. Report executed versus skipped checks; query count alone does not prove speed.
