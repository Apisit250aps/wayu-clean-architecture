# Repository and external adapters

Concrete adapters implement Domain ports. Preserve established package placement and reuse typed mechanics. Read [repository boundaries](repository-boundaries.md) for repository changes; schema and migration work uses [Drizzle patterns](drizzle-patterns.md).

## Repository construction

Inject the existing database/transaction infrastructure and non-repository adapter dependencies actually needed. Never inject, instantiate, call, or obtain another repository through a helper, callback, container, base class, or service. A composition root creates repositories separately and injects their Domain ports into Application Services.

A repository may own aggregate child/history tables. All queries and side effects, including inherited helpers, stay within that ownership. Foreign keys to other owners remain valid integrity constraints, not read/write access permissions.

## Method implementation

1. Implement the port's scoped operation, including active/deleted, duplicate/missing-ID, ordering, and empty-batch semantics.
2. Query through the project's current transaction resolver. Keep the root connection identity used by UnitOfWork; do not replace it mechanically or mutate singleton connection fields.
3. Use typed columns and explicit result mapping where shapes differ. Preserve native Date/numeric/custom decoders and nullability; casts do not validate or remove fields.
4. Enforce unique/revision conditions atomically where required, and translate known storage conflicts using established typed errors.
5. Batch reads/writes instead of query-per-item loops. Coordinate cross-owner filters, locks, and audit through Application Services, preserving pagination semantics.

Trust-boundary validation remains required; do not add redundant parsing of every typed ORM result as a substitute for explicit mapping and integrity guards. Validate untrusted external/JSON payloads according to their actual contract.

## External adapters

Reuse existing authentication, password hashing, storage, and provider clients. Expose only required Domain ports; keep SDK types, credentials, and provider-specific errors in the adapter. Preserve failure semantics, redaction, and idempotency where the workflow needs them. Do not build an alternate credential system or a generic adapter framework for one operation.

Keep provider calls outside long DB transactions. Application decides any required compensation or durable delivery; a database rollback does not undo a remote operation.

## Wiring and verification

Update composition, exports, callers, mocks, and tests when a port changes. Required dependencies must fail wiring instead of selecting fallback adapters or skipping guards. Share the actual UnitOfWork database identity among participating repositories. Test real transaction/lock behavior before claiming it; isolated fake tests prove orchestration only.
