---
name: clean-architecture-api
description: Define TypeSpec API contracts and implement HTTP presentation handlers, OpenAPI output, and generated TypeScript client SDKs for Clean Architecture projects.
---

# Clean Architecture API

Use this skill when changing an HTTP-facing feature: its TypeSpec contract, generated client, controller/route, request validation, or response mapping. Do not use it for visual UI composition alone.

## Contract-to-handler flow

1. Model externally visible request and response DTOs in TypeSpec, deriving them from domain aliases rather than duplicating field lists. Read [TypeSpec patterns](references/typespec-patterns.md).
2. Generate and inspect OpenAPI plus the TypeScript client after contract changes; do not hand-edit generated output.
3. Implement presentation handlers that validate transport input, invoke application use cases, and map typed errors to transport responses. Read [presentation patterns](references/presentation-patterns.md).
4. Keep controllers free of direct repository or database access.

## Shared boundaries

Search existing request validators, response/error mappers, pagination helpers, and generated DTOs before adding a parallel implementation. Group routes by business module and share transport plumbing while leaving authorization and lifecycle policy in core.

Build actor/security context from authenticated middleware. Never spread request data over trusted permissions, admin status, or active tenant fields. Propagate tenant scope and revision/idempotency inputs required by the use-case contract. Expose only client-writable fields, even when the entity model has more properties.

Use core constants for stable statuses/actions and preserve generated contracts through regeneration. Check representative payloads, response envelopes, error codes, pagination, and nullable/date conversions at the boundary; a shared helper must not hide a contract mismatch.
