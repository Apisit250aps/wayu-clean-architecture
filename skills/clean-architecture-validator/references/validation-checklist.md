# Architecture verification checklist

Read the current core, frontend, and persistence entrypoints for ownership rules. Audit the actual target repository; examples are not proof of compliance.

## Domain and constants

- New modules/tables create or extend an owning constants module and export it.
- Each table maps to a business aggregate and permission policy; internal tables need not have independent CRUD permissions.
- Status/mode values are reused in schemas and use cases. Constants do not depend cyclically on schemas.
- Feature/action catalogs contain no duplicates; default grants reference known actions and remain explicit.
- Changed catalog snapshots have versioned migration handoffs without overwriting tenant-specific grants.
- Domain stays independent of DB/HTTP/UI; public contracts use narrow typed ports.
- Create/update schemas distinguish client-writable inputs from tenant/actor/audit/revision fields.
- Append-only history contracts expose only legal operations.
- Module splits preserve exports and generator discovery.

## Application and tenant policy

- Use cases accept injected domain ports and trusted execution context.
- Async parsing uses the existing helper or safeParseAsync, and business logic consumes parsed output.
- Resource operations check stored ownership; creates/lists validate destination tenant scope.
- Child IDs, membership, roles, sites, and templates satisfy the expected tenant relationships.
- Permission, feature entitlement, assignment, and lifecycle checks are distinct and use shared policy helpers.
- No customer/role-name hardcoding or mutable singleton tenant state.
- Missing required dependencies cannot silently skip an invariant.
- Shared pure functions receive explicit time/policy inputs where needed.
- Errors use the existing application hierarchy without leaking database internals.

## Repository ownership and query checks

Apply [the ownership rules](../../clean-architecture-persistence/references/repository-boundaries.md), including cross-owner summaries, audit, and locks.

- Every table/view has one explicit repository owner; aggregate-owned child/history tables have no competing owner.
- No repository calls/constructs/injects another repository, inherits its owner-specific behavior, or uses callbacks/providers as a substitute dependency.
- Inspect each accessed table and trace JOINs, subqueries, CTEs, ORM relations, raw SQL, views/functions/triggers, mappers, and shared/inherited helpers. No cross-owner read-model or audit exception; preserve integrity constraints when reviewing database-side behavior.
- Application Services compose required owner ports with no ORM/SQL or broad service container. A few explicit constructor dependencies are preferred over redundant port bags or fallback adapters.
- Owner batch operations replace per-item query loops, including `Promise.all`/Lodash wrappers. Pure mapping is distinct; necessary Domain iteration/chunks have an explained bound.
- Page/count predicates, stable order/ID tie-breaker, total beyond the last page, native decoders, and null relations remain correct. Related-field filtering/order is resolved before pagination through owners, not just on returned items.
- Reorders specify duplicate/missing/deleted/empty behavior; replacements and audit fail/rollback as one unit.
- Actual adapter tests establish ambient root-object identity, transactional locks through the final write, scoped expected row sets, consistent lock order, and latest finalized/reopened heads. No missing-row lock assumption or blind replacement of `this.database`/`this.db`.
- Retained source facts/history reproduce derived reads; snapshots do not justify reproducible caches or fabricated historical inputs.
- Ports, callers, Service wiring, exports, mocks, tests, and docs change together. File scope and formatted content are reviewed; no claim of global migration while violations remain.

## Condition JSDoc checks

Use [the full condition guide](../../clean-architecture-docs/references/jsdoc.md#conditions). Within the requested scope/diff, inventory conditions rather than searching only for `if`.

- Every new/changed branch, guard, `switch/case/default`, ternary/render expression, logical/nullish/default/optional expression, loop/recursion/callback predicate, refinement/assertion, result/error discriminant, and SQL/ORM condition has adjacent Thai JSDoc.
- Comments explain the checked source fact, reason, and true/false or selected/fallback/continuing outcomes. Compound predicates explain every part and short-circuit behavior where relevant.
- Null/undefined/falsy behavior, time units/boundaries, tenant scope, actual errors, side effects, and guarantees agree with source and callers. No invented policy or concurrency claim.
- A method-level overview or generic comment does not substitute for its individual conditions. Expression/JSX/SQL placement preserves syntax, evaluation order, and output; no behavior changes just to attach comments.

## Persistence and concurrency

- Reuse schema/query/row-mapping helpers where semantics match.
- Tenant predicates apply to lookup, update, delete, batch, and list operations.
- Uniqueness/idempotency requirements have database enforcement where needed.
- Revision guards have an atomic update predicate or appropriate lock/isolation implementation.
- Unit-of-work participation and rollback are verified at the real adapter boundary.
- Read-model projections do not expose internal columns through casts.
- Investigate N+1 lookups, unbounded lists, and repeated full scans; measure before claiming improvement.
- Infrastructure composition code may wire applications to adapters; core never imports that composition.
- Migrations are reviewed independently of whether they have been applied.

## API and generated client

- Controllers live at the actual server boundary, such as apps/api, and call use cases.
- Authentication produces trusted security context; request fields cannot overwrite it.
- Shared validators, response/error mappers, pagination, and generated DTOs are reused.
- Public DTOs expose only intended fields and preserve scope/revision requirements.
- Generated files are regenerated, not hand-edited; entity aliases and DTO transforms remain consistent.
- Real response envelopes, errors, nulls, dates, and attachments are checked when their contracts change.

## Frontend and UI

- Reuse packages/ui primitives and shared fields/tables/overlays before adding markup.
- Generic RHF Controller-backed fields and TanStack Table compositions are allowed in UI; business data fetching and tenant policy are not.
- Web routes render feature views; hooks own client calls and query invalidation.
- Query keys include the applicable tenant/filter scope.
- Avoid effects for mirrored/derived/form state; use RHF and Query lifecycle APIs.
- Follow the requested component rule forbidding try/catch/finally and handle request errors in hooks/callbacks.
- Pure utilities and typed payload adapters replace repeated inline transformations.
- Browser components do not import DB or backend compositions.

## Evidence and reporting

Run appropriate type/lint checks and record warnings as well as exit codes. For runtime changes choose focused cases: two tenants, inactive members, disabled features, invalid transitions, duplicate writes, concurrent revisions, and partial-write rollback. A static pass does not establish database isolation or browser behavior. For documentation-only changes validate links, metadata, and consistency instead of executing unrelated application tests.

## Helper and state ownership checks

- Utils/lib/helper imports resolve to concrete files or explicit subpaths in every layer; no barrel/root re-export imports.
- Application/use-case files and class files contain no standalone helper declarations; helpers live in the owning package utils/helper/lib files. Class methods and necessary inline callbacks are allowed.
- Editable fields in form/query/mutation-driven Web components use RHF/Controller; React Query retains server/request/cache state. Avoid useEffect for form or derived state synchronization.
