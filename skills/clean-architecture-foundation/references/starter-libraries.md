# Shared library decisions

Read only the row relevant to the requested scaffolding. Search the target repository first; use the existing helper with matching semantics. This is a selection guide, not a second framework to install.

| Need | Reuse or establish | Owning guidance |
| --- | --- | --- |
| Entity/schema helpers | Typed Zod shapes; preserve defaults, transforms, omitted/null values, and operation-specific refinements. Avoid broad casts or a generic field-builder API without a demonstrated need. | [Domain patterns](../../clean-architecture-core/references/domain-patterns.md#schema-first-contracts) |
| Base contracts | Narrow business ports and use-case contracts. An append-only aggregate must not inherit update/delete simply because a CRUD base exists. | [Domain ports](../../clean-architecture-core/references/domain-patterns.md#purpose-specific-ports) |
| Validation/errors | Existing async parsing and typed error helpers; transport envelopes/status mapping belong at the API boundary. Never leak unknown internal error messages to clients. | [Application patterns](../../clean-architecture-core/references/usecase-patterns.md), [presentation](../../clean-architecture-api/references/presentation-patterns.md) |
| Repository mechanics | Existing typed owner-scoped base, mapping and transaction resolver. No `any`, disabled lint, unscoped generic `findAll`, or cast-only row conversion. | [Adapter patterns](../../clean-architecture-persistence/references/infrastructure-patterns.md) |
| UUID/timestamps | Existing UUIDv7 and audit timestamp helpers; preserve schema defaults and migration semantics. | [Drizzle patterns](../../clean-architecture-persistence/references/drizzle-patterns.md) |
| Password/provider adapters | Existing auth/provider integration and Domain port; no parallel credential system. | [External adapters](../../clean-architecture-persistence/references/infrastructure-patterns.md#external-adapters) |
| Formatting | Existing Prettier config/scripts and ignores. | [Naming and style](naming-and-style.md) |
| Domain → TypeSpec generation | Existing generator/configuration and its supported type mappings. | [Generation contract](#generation-contract) |
| HTTP SDK setup | Existing spec → OpenAPI → client pipeline. | [TypeSpec patterns](../../clean-architecture-api/references/typespec-patterns.md) |

## Generation contract

When changing or creating an entity-to-TypeSpec generator:

- Inspect actual entity/schema exports and the API package's expected namespace/output path; do not assume every declaration is public API.
- Preserve optional versus nullable, arrays/unions/enums, dates, and declared numeric semantics. TypeScript `number` alone does not justify mapping every field to `int32`.
- Preserve inherited fields deliberately. Do not inject every base field when only one is present or silently drop fields such as historical deletion metadata.
- Fail visibly on unsupported shapes instead of emitting plausible but wrong contracts. Keep generation deterministic and changes reviewable.
- Use existing parsing/compiler tooling where available. Add a new generator only when the requested workflow requires it; test representative supported and unsupported shapes, then compile the emitted spec and generated consumers.

Generated files remain owned by their pipeline. A scaffold example is not evidence that the output compiles or matches a consuming project's runtime.
