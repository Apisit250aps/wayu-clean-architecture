# Repository ownership, queries, and transactions

These are the collection's repository rules. Apply them to new and changed workflows; report existing violations without claiming an entire repository has already migrated. Examples illustrate contracts, not verified implementations in a consuming project.

## One explicit owner for each table

Record the owning repository for every table, view, and persisted source before refactoring. An aggregate repository may own internal child/history/join tables that have no separate repository owner. A table does not automatically need its own class, permission, or module. Once another repository owns it, access belongs there, even inside the same module or database.

A repository must not call, instantiate, inject, inherit behavior from, or delegate through another repository. Reusing a generic base for operations on the caller's own table is allowed; hidden access to another owner's tables is not.

This boundary includes direct SQL and indirect access through JOINs, subqueries, CTEs, ORM relational queries, raw SQL, views, database functions, triggers invoked by repository operations, mappers, callbacks, providers, and generic helpers. A helper rename or conversion from SQL to a query builder does not remove the dependency. Do not create a cross-owner read repository, view, or stored function as an escape hatch. Trace existing database-side behavior and preserve integrity constraints; changing a trigger is a separate schema/data change that needs its own review.

Cross-owner read projections, summaries, locks, and audit writes have no automatic exception. SQL joins between tables owned by the same repository remain possible. Foreign-key declarations and integrity constraints express relationships; they do not authorize a repository to load or modify the referenced owner's records.

## Application Services compose owners

Use a named Application Service for a workflow that needs multiple repositories. Inject the relevant Domain interfaces as required constructor dependencies; keep ORM objects, database connections, and raw queries out of that service. A controller continues to invoke a use case, which can use the service.

| Existing pattern                                                        | Replacement                                                                                        |
| ----------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------- |
| Period repository reads/locks sites and requirements                    | Service calls the site and requirement owners, then the period owner in the established lock order |
| Request repository joins member, user, site, or another owner's history | Owners return scoped source batches; Service assembles the read result                             |
| Mapper loads policy/rule revisions while mapping a row                  | Service obtains the revisions from their owners; mapper receives values and stays pure             |
| Base repository or helper inserts into the audit owner's table          | Service coordinates the mutation and audit owner's batch append in one transaction                 |

Audit removal is not a solution: retain actor/context, before/after values, redaction/encryption, and atomic rollback. Reuse source values or narrowly typed mutation results already needed by the workflow; do not expose raw storage rows just to pass audit data between layers.

An interface/port is a contract, not an extra runtime layer. Prefer explicit constructor parameters for a few dependencies. A cohesive narrow dependency object is acceptable when it adds clarity; do not duplicate the same dependencies in parameters and a `Ports` bag or accept an entire container. Missing required ports must fail wiring rather than silently bypass guards or create a fallback adapter inside a use case or repository. Optional execution inputs remain distinct from optional dependencies.

## Batch work without query loops

- Provide semantic, tenant-scoped owner ports such as `findByIds`, `exists`, `count`, and operation-specific batch writes. Preserve active/deleted and ownership predicates inside persistence as well as Application authorization.
- Do not query per item through `for`, `map`, `forEach`, recursion, or `Promise.all` when a batch operator can perform the work. Moving the callback or replacing it with Lodash does not fix N+1.
- Pure mapping, ID indexing, and payload preparation are different from a loop that performs I/O. Preserve validation; use an existing batch predicate/constraint for checks when possible. Explain necessary Domain iteration or bounded query chunks before implementing them, including why batching cannot replace them and how work is bounded.
- Prefer Drizzle/query-builder operations. Use parameterized `sql` fragments where the installed builder needs an expression, for example JSON input rows, ordinality, or an aggregate. Full raw SQL needs a concrete builder limitation; it still cannot cross ownership.
- A fixed number of owner batch queries is preferable to one statement that crosses owners. Avoid `Promise.all` for page/count when the owner can return both in one statement; concurrency alone does not reduce query count.
- Empty batches should avoid unnecessary queries. Document whether duplicate IDs are rejected/deduplicated, which duplicate value wins, how missing/deleted IDs behave, and whether output follows input order. Do not silently change those semantics during optimization.

For reorders, use one owner update when possible and make duplicate handling deterministic. For replacements, delete and batch insert must share the caller's transaction; insertion or audit failure must restore the old data and audit state.

## Pagination preserves the complete result

Choose page plus total, cursor/keyset, offset without total, or pagination after Domain derivation based on the existing contract; do not replace them all with one API for convenience.

For page/count on an owner's data:

- Use identical tenant, filter, and soft-delete predicates; count has no page limit/offset. Prefer a single statement when supported.
- Return the true total even for an empty page beyond the final offset. A window count alone has no row from which to read a total in that case; a count-driven LEFT JOIN/CTE can preserve the metadata row.
- Preserve stable ordering, including an ID tie-breaker, in the page and any outer query.
- Preserve native column decoders for Date, numeric, and custom/encrypted values. Do not JSON-round-trip result rows to simplify types. Use unique SQL aliases and preserve nullable relation semantics where relevant.

Services can enrich an authorized page through owner batch lookups when related values do not affect filtering, ordering, or totals. When a filter/order depends on another owner, coordinate its scoped owner operations before pagination and verify complete-dataset semantics. Do not filter only the returned page, fetch every tenant row without a bound, or reintroduce a cross-owner JOIN to keep a one-query target. If the current contract cannot meet these constraints with bounded owner operations, report the concrete conflict and resolve the contract/design explicitly rather than adding a hidden exception.

## Transaction participation and locks

Inspect the actual UnitOfWork adapter before promising atomicity. The Application workflow owns the transaction covering participating owner calls, mutations, history, and audit. A repository may use the existing transaction helper for its own atomic multi-step writes; it must not orchestrate other owners.

Where the project uses ambient transactions:

- Query through the connection resolver/getter for the current async scope. Retain the root database as the identity passed to the transaction helper; do not mechanically replace every `this.database` with `this.db`.
- All participating repositories and UnitOfWork must share the same root database object. The same connection URL on different objects is not sufficient.
- Do not mutate a singleton repository's connection to install a transaction. An ordinary `database.transaction()` may not register ambient scope; verify the project's helper rather than mixing mechanisms blindly.
- Check the adapter's actual outer isolation, nested savepoints, conflict translation, and retry policy. An interface alone proves none of them. Await all transactional work and keep external provider calls outside long DB transactions.

`FOR UPDATE` protects a workflow only while its transaction stays open. Require a transaction for a nonempty lock request, then keep subsequent writes inside that same scope. An empty-input no-op may follow the existing contract. Validate the tenant and expected locked-row set; a missing row is not locked.

Services preserve one shared lock order across workflows, and owner batch methods sort their own locks consistently. For example, site locks precede periods ordered by site/start/ID, and member locks can precede quota locks ordered by tenant/member/year/type/ID. These are project-specific protocols to inspect, not a universal replacement for the existing order. A member lock can coordinate creation of a quota row that does not yet exist; do not mistake a missing quota for a successful quota lock.

Preserve latest-head/revision semantics, reopened states, half-open date ranges, gap-period behavior, and historical time-zone/policy calculations. Do not recalculate Domain date windows in SQL merely to remove iteration.

## Source facts and verification

Persist necessary source facts, explicit decisions, integrity/concurrency keys, and indispensable history. Derive reproducible totals, counts, balances, durations, percentages, and statuses. Before removing a derived field, retain the inputs, units, time boundaries, and historical policy needed to reproduce it; never invent missing history. A historical snapshot is justified by mutable source facts that cannot reproduce the original record, not by a calculation that remains reproducible. Measured performance exceptions require an explicit separately documented decision.

Trace schema/view/function/trigger ownership, repository methods and helpers, Domain ports, Service/use-case callers, composition roots, exports, mocks, tests, and affected docs. Update them together. Add Thai JSDoc for actual contracts and every condition using [the condition guide](../../clean-architecture-docs/references/jsdoc.md#conditions).

Verify relevant behavior: cross-tenant IDs, batch statement counts, empty/out-of-range pages, filters/order, native decoding/nulls, duplicate/missing IDs, whole-batch rollback, audit rollback, real lock contention, and latest finalized/reopened heads. Type-check and unit tests do not prove database isolation. Query-count reductions do not prove speed without timings/plans; keep benchmark, SQL integration, HTTP, browser, and device/provider evidence distinct.

Report unresolved ownership paths and skipped/failed checks. A clean constructor, no `Promise.all`, or passing tests does not prove that indirect ownership access has been removed. Run the repository formatter and inspect both the content and file scope of the final diff before reporting completion.
