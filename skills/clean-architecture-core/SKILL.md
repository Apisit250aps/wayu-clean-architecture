---
name: clean-architecture-core
description: Define Domain contracts and implement use cases, pure business rules, and Application Services that coordinate repository ports.
---

# Clean Architecture Core

Use for Domain and Application changes. Inspect the affected module, callers, exports, and existing helpers. Read only references needed for that work.

## Responsibilities

| Component | Owns |
| --- | --- |
| Domain | Types/schemas, constants, entities, ports, lifecycle invariants, pure business calculations |
| Use case | Command/query entry, parsed input, trusted actor/tenant scope, workflow outcome |
| Application Service | Cohesive multi-repository orchestration through required Domain interfaces |
| Composition root | Construction/injection of concrete services and adapters; stays outside core |

## Workflow

1. Establish capability, aggregate/table owners, actor, lifecycle, and business decisions. Reuse agreed ERD/flows; tables alone do not define behavior.
2. Define the smallest usable contract slice: inputs/results, errors, scoped repository/service ports, constants, and exports. Read [Domain patterns](references/domain-patterns.md).
3. Implement pure rules in Domain and orchestration in Application. Use cases/services can use typed test doubles while concrete adapters are built. Read [Application patterns](references/usecase-patterns.md).
4. For tenant-owned or configurable behavior, read [tenant policy](references/tenant-policy-design.md). Authorize stored resource ownership; request fields cannot override trusted scope.
5. Update callers, wiring, exports, catalogs, and tests affected by the contracts. The [historical source analysis](references/source-analysis.md) is optional context, not current implementation proof.

## Rules

- A repository never depends on or calls another repository, nor accesses another owner's tables. Application Services compose required owner ports without ORM/SQL. Read [repository boundaries](../clean-architecture-persistence/references/repository-boundaries.md) for multi-owner, batching, pagination, audit, or transaction work.
- Each new module/table has an owning constants/permission mapping; internal tables may inherit their aggregate's policy. Update affected feature/action/default-grant catalogs and versioned seed migrations; never grant new actions to all roles implicitly.
- Validate command input with the existing `parseSchemaOrThrow` or `safeParseAsync` and use the parsed result. Keep typed errors, atomic revision checks, and required dependencies; no fallback adapters or duplicated dependency bags.
- Import helpers through concrete subpaths and keep standalone helpers outside use-case/class files. Use explicit types, no suppressions, and Thai JSDoc for [every changed condition](../clean-architecture-docs/references/conditions.md).
- Pure calculations receive time inputs. A use case samples `new Date()` once; use direct date-fns imports, no clock port/shared time wrapper/Temporal. Read [time handling](../clean-architecture-foundation/references/time-handling.md) for date changes.

## Verify

Run affected type/lint checks and focused rule/workflow tests. Test relevant tenant, permission, lifecycle, and failure paths; real adapter tests are needed to claim rollback/concurrency. Keep isolated implementation and integration completion separate.
