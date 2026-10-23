---
name: clean-architecture-api
description: Define TypeSpec HTTP contracts, generate OpenAPI/client output, and implement handlers that invoke application use cases.
---

# Clean Architecture API

Use for HTTP contracts, generated clients, validation, handlers, and response mapping. Inspect the actual server entry, spec/generator configuration, use-case contracts, and existing transport helpers. Read only the relevant reference.

## Contract and handler work

- **Spec/client:** follow [TypeSpec patterns](references/typespec-patterns.md). Reuse Domain aliases, expose only client-writable fields, and regenerate output; never hand-edit generated files. Spec/client work can proceed before backend implementations when contracts are ready.
- **Handlers:** follow [presentation patterns](references/presentation-patterns.md). Validate transport input, invoke a use case, and map its result/errors. Controllers never call repositories or databases.

## Boundaries

- Build actor/tenant context from authenticated middleware; request data cannot override permissions, admin status, or trusted scope.
- Keep business authorization/lifecycle rules in core. Preserve tenant, revision/idempotency, pagination, nullability, and date semantics across DTO mappings.
- The main application's spec/generated client owns HTTP types. Domain contracts and Web mock view models are not automatically wire DTOs.
- Reuse validators, error/response mappers, and pagination helpers. Import helpers directly and keep standalone helpers outside class files.
- Use explicit types without suppressions and Thai JSDoc for [every changed condition](../clean-architecture-docs/references/conditions.md).

## Verify

Run generation and affected type/lint checks. Check representative requests/responses, encoding, envelopes, errors, dates/nulls, and client mappings. Distinguish contract/static checks from exercised HTTP behavior; integrate handlers with real use cases separately when implementations are still pending.
