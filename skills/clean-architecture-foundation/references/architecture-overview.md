# Architecture and ownership

These are this collection's package conventions. Adapt package names/locations to the target repository; keep dependency direction and business ownership explicit.

## Package matrix

| Package/layer | Responsibility and allowed dependencies | Forbidden |
| --- | --- | --- |
| Domain | Contracts, constants, entities, pure rules; pure libraries such as Zod, uuid, date-fns | Internal outer packages, DB/HTTP/UI/framework I/O, current-time reads in business rules |
| Application | Use cases and Application Services; Domain interfaces and pure helpers | Concrete adapters, ORM/SQL, HTTP request/response types, UI |
| Database | Schemas, migrations, DB mechanics, owned adapters where established; Domain + database libraries | Application implementations, UI/client, infrastructure composition |
| Infrastructure | Concrete adapters; Domain/database/external SDKs | UI/browser code; adapter imports back into core |
| Composition root | Wires concrete adapters and Application implementations, isolated at the server boundary | Import into Domain, use cases, or browser bundles |
| API/presentation | Auth/context, transport validation, use-case invocation, HTTP mapping | Direct repository/DB operations inside handlers |
| Generated client | Main application TypeSpec/OpenAPI types and SDK output | Hand-edited generated output or backend runtime dependencies |
| Shared UI | Generic accessible components, RHF fields/tables/overlays | Business hooks/policy, generated services, backend modules |
| Web | Routes/features/hooks; UI, generated client, safe public Domain types/constants | Database connections and server composition in browser modules |

## Runtime calls and source dependencies

```text
Controller → Use case → Application Service → Repository A
                                           → Repository B
                        ↘ Pure Domain rules

Composition root creates the implementations and injects them.
Application imports Domain ports, not concrete repositories.
Repository A does not depend on or call Repository B.
```

A single-owner use case need not add a pass-through service. A named Application Service owns a cohesive workflow requiring multiple owners. Pure rules compute from supplied facts and do not fetch repositories. See [Application patterns](../../clean-architecture-core/references/usecase-patterns.md#service-composition-and-dependencies).

Table ownership is separate from package placement. An aggregate repository may own multiple child/history tables and JOIN its own tables. Cross-owner reads/writes, including hidden helper/view/audit paths, go through Application orchestration and each owner's port. See [repository boundaries](../../clean-architecture-persistence/references/repository-boundaries.md).

## Enforcement

Use existing lint/import tooling to enforce the matrix, including aliases, package roots, and subpaths. Restrict any composition exception to its actual files. Import checks do not prove table ownership, tenant isolation, transaction propagation, or runtime behavior; inspect and test those separately.
