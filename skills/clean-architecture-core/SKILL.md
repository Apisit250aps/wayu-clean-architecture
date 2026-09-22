---
name: clean-architecture-core
description: Implement Domain schemas, entities, ports, and Application use cases in a Clean Architecture TypeScript monorepo.
---

# Clean Architecture Core

Use this skill for business entities, Zod schemas, repository/use-case contracts, and concrete application use cases. Do not put persistence, HTTP, or UI behavior in these packages.

## Workflow

1. In `packages/domains`, define the schema, entity, repository port, and use-case context first. Read [domain patterns](references/domain-patterns.md).
2. In `packages/applications`, implement the use case only against domain contracts. Validate untrusted inputs with `await safeParseAsync`; translate failures into typed application errors. Read [use-case patterns](references/usecase-patterns.md).
3. Export intentional public types and verify that the core remains free of outward package imports.

## Boundary

The domain owns business language and ports. The application layer orchestrates those ports. Neither layer may query Drizzle, instantiate concrete repositories, return HTTP responses, or import interface packages.

