---
name: clean-architecture-persistence
description: Implement Drizzle database schemas, migrations, repository infrastructure, and external persistence adapters for Clean Architecture TypeScript projects.
---

# Clean Architecture Persistence

Use this skill when a feature needs storage or another concrete repository adapter. It covers `packages/database` and `packages/infrastructures`; it does not define business rules or HTTP contracts.

## Workflow

1. Start from the Domain entity and repository port; do not introduce a storage-driven domain model.
2. Add Drizzle tables, relations, migrations, and shared repository mechanics in `packages/database`. Read [Drizzle patterns](references/drizzle-patterns.md).
3. Implement the domain port in `packages/infrastructures`, reusing the generic repository for standard CRUD and adding only real custom queries or adapters. Read [infrastructure patterns](references/infrastructure-patterns.md).
4. Keep Drizzle types and connection details at the persistence boundary; return domain-compatible values and validate migrations against the target database workflow.

## Boundary

Infrastructure may depend on domains and database. It must not depend on application, presentation, or UI packages. Concrete adapters are composed outside the core.

