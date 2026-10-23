---
name: clean-architecture-persistence
description: Implement Drizzle database schemas, migrations, repository infrastructure, and external persistence adapters for Clean Architecture TypeScript projects.
---

# Clean Architecture Persistence

Use this skill when a feature needs storage or another concrete repository adapter. It covers `packages/database` and `packages/infrastructures`; it does not define business rules or HTTP contracts.

## Workflow

1. Start from the Domain entity and repository port; do not introduce a storage-driven domain model. Read [repository ownership, queries, and transactions](references/repository-boundaries.md) for repository changes and identify every table owner before editing.
2. Add Drizzle tables, relations, migrations, and shared repository mechanics in `packages/database`. Read [Drizzle patterns](references/drizzle-patterns.md).
3. Implement the domain port in `packages/infrastructures`, reusing the generic repository for standard CRUD and adding only real custom queries or adapters. Read [infrastructure patterns](references/infrastructure-patterns.md).
4. Keep Drizzle types and connection details at the persistence boundary; return domain-compatible values and validate migrations against the target database workflow.

## Boundary

Repository/storage adapters depend on domains and database, not application implementations or UI. An isolated composition root may import Application implementations to wire them to these adapters; never import that wiring into core or browser code.

A repository accesses only its own tables and never calls another repository, directly or indirectly. Cross-owner SQL/ORM JOINs, read projections, views/functions, helpers, locks, and audit writers are not exceptions. Application Services coordinate required owner ports and preserve transaction, ordering, filtering, and pagination semantics. A generic base may operate on the caller's own table but cannot write another owner's audit table. See [the ownership rules](references/repository-boundaries.md).

Prefer owner-scoped batch operations through Drizzle; parameterized SQL expressions do not permit crossing owners. Do not replace query loops with hidden helper queries or full raw SQL merely to remove `Promise.all`. Preserve source facts/history and verify actual query counts, rollback, and locks separately from performance claims.

When writing or changing conditions, add Thai JSDoc for every form using [the condition guide](../clean-architecture-docs/references/jsdoc.md#conditions).

## Module integration and quality

- For every new table, coordinate the owning module's constants, aggregate permission mapping, and any feature/action/seed changes with [core](../clean-architecture-core/SKILL.md). Internal tables may share an aggregate permission; SQL identifiers stay in persistence.
- Reuse schema helpers, row mappers, scoped query builders, and transaction infrastructure before introducing another repository abstraction. Return only intended domain/read-model fields; TypeScript casts do not remove database-only columns at runtime.
- Implement tenant predicates for reads and writes, scoped uniqueness, and atomic revision conditions where the domain contract requires them. An application uniqueness/revision check alone does not prevent races.
- Prefer bounded batch queries and projections to repeated row lookups. Validate an optimization with query counts/timings and execution plans where appropriate; do not infer speed from helper extraction or Promise.all.
- Keep a versioned migration snapshot of changed system catalogs and explicit grants. Preserve tenant customizations and distinguish migration generation from application to a target DB.

## Shared helper conventions

Import utils/lib/helpers from concrete files or package subpaths, never barrels. Keep standalone helpers outside Application/use-case and class files, in their owning package. See [Foundation helper conventions](../clean-architecture-foundation/SKILL.md#helper-files-and-imports) for the shared rule and exceptions.
