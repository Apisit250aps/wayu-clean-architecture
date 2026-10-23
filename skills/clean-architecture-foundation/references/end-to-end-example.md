# Product workflow example

Illustrative plan for a tenant-owned Product capability; names/operations below are proposed contracts, not verified project APIs. Use only the parts required by the real feature.

## Contracts first

Domain defines Product's source facts, allowed inputs/results/errors, stable status/action constants, tenant context, and narrow Product/Category/Audit ports. Decide which aggregate owns each table. Define pure product rules from agreed business behavior; do not infer currency units, stock accounting, or deletion policy from field names.

## Separate implementations

| Track | Work from those contracts |
| --- | --- |
| Persistence | ProductRepository touches only its owned tables. CategoryRepository and AuditRepository implement their own ports. Schema constraints enforce scoped uniqueness/revisions where required. |
| Application | CreateProductUseCase validates input/actor scope and delegates cohesive multi-owner work to ProductCreationService. The service loads the category through its owner, applies Domain rules, writes Product, and appends audit. |
| API | Define transport DTOs from Domain aliases with server-owned fields excluded, generate the client, and map handler input/results/errors around the use case. |
| Web | Build a form/list mockup from typed fixtures. Later connect feature hooks using generated HTTP types and explicit view mappings. |

Application work uses typed test doubles while repositories are unfinished. Contract signatures alone do not prove authorization, uniqueness, rollback, or HTTP compatibility.

## Composition and atomicity

```text
Server composition root
  ├─ shared database/UnitOfWork
  ├─ ProductRepository
  ├─ CategoryRepository
  ├─ AuditRepository
  └─ ProductCreationService(owner ports, UnitOfWork as needed)
       └─ injected into CreateProductUseCase
            └─ invoked by HTTP handler
```

The workflow establishes the transaction covering required reads/locks and product/audit writes. All participating repositories must join the same transaction; preserve established lock order and atomic constraints. Services use ports, never raw queries; repositories never call each other. Keep composition out of browser code.

## Verify the join points

- Domain rules: valid/invalid inputs and transitions.
- Use case/service: scope, missing/inactive category, required dependencies, typed failures.
- Isolated DB: scoped uniqueness/revisions, atomic product/audit rollback, relevant locks.
- API/client: generated shapes, errors, dates/nulls, and actual HTTP mapping.
- Web: form/permission/loading/error/success states and removal/isolation of mock wiring.

See [parallel planning](../../clean-architecture-plan/references/parallel-delivery.md) for start versus integration prerequisites and [repository boundaries](../../clean-architecture-persistence/references/repository-boundaries.md) for concrete ownership/transaction requirements.
