---
name: clean-architecture-core
description: Design modular, tenant-aware Domain contracts and Application workflows with shared constants, configurable policies, repository ports, validation, and transactional invariants.
---

# Clean Architecture Core

Use for `packages/domains` and `packages/applications`. First inspect the target repository's module structure, exports, constants, security context, repository ports, and shared helpers. Adapt examples to its package scope; `@<project>` is a placeholder.

## Design the module first

1. Identify its business capability, aggregate boundaries, tenant owner, lifecycle, and collaborators. A table is a persistence detail, not automatically a new business module.
2. Define stable constants and the system catalog changes for every new module/table. Read [domain patterns](references/domain-patterns.md), including the mandatory constants checklist.
3. Define schemas, entities, scoped ports, and operation-specific use-case contexts. Keep Domain independent of Application, database, HTTP, and UI.
4. Implement use cases against injected ports. Read [application patterns](references/usecase-patterns.md) for helper reuse, authorization, transactions, and concurrency.
5. For tenant-owned data or configurable behavior, read [tenant and policy design](references/tenant-policy-design.md). Global catalogs and tenant configuration must remain distinct.
6. For a new module or substantial refactor, read [the source analysis](references/source-analysis.md) to distinguish observed patterns from improvements required by this skill.

## Module structure and flexibility

Preserve established public imports while organizing related behavior into modules:
`constants/<module>.ts`, `schema/<module>`, `entities/<module>`,
`repositories/<module>`, `applications/<module>`, and
`use-cases/<module>`. Small modules may retain one file per category.
Split a growing module by aggregate or workflow, not by arbitrary line counts.
Update package exports, barrels, and entity-generation discovery when moving files.

Keep invariants explicit and vary genuine policy through typed configuration or injected strategies. Tenant IDs, role names, and customer-specific branches must not control business behavior. Do not introduce a generic rules engine or plugin registry until an actual extension point requires one.

## Mandatory constants for each module/table addition

Create or extend the owning module's `constants/<module>.ts` and export it through `constants/index.ts`. Define its stable resource codes, lifecycle values, policy modes, and shared limits where they exist. Use constants in schemas and use cases instead of repeating strings.

For every added table, record its business owner and permission mapping in the change: an internal child/join/history table may inherit its aggregate's permission; do not invent CRUD permissions or a feature for every table. SQL table names and ORM objects stay in persistence.

When a capability adds system features/actions, synchronize `FEATURE_CODES`,
`SYSTEM_FEATURES`, `PERMISSION_ACTIONS`, `SYSTEM_PERMISSIONS`, and explicit
default-role grants as applicable. Database seed snapshots must be updated through
versioned migrations; never automatically grant new actions to every role.

## Reuse and verification

Search `domains/src/lib`, `applications/src/lib`, decorators, and module-local helpers before writing a new abstraction. Share pure business calculations in Domain, application orchestration helpers in Application, and DB mechanics in persistence. Keep shared functions typed, cohesive, and explicit about scope and dependencies.

Validate with the repository's type-check/lint commands. For runtime changes, select checks for tenant A/B separation, constants/catalog integrity, policy behavior, rollback, and concurrent updates as relevant. Report static checks separately from real API/database verification. Do not apply migrations merely to inspect a design.
