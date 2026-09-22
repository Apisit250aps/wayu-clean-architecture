# Application workflows and shared functions

## Module organization

Use `src/use-cases/<module>/` for related workflow implementations and a public `index.ts`. A cohesive CRUD group can remain in one file; complex assignments, publishing, reviewing, scheduling, or attachment workflows deserve separate named files. Module-local helpers stay next to their callers until another module needs the same semantics.

Constructors accept domain ports, including `IUnitOfWork` when needed. Keep request actor/tenant values in execution context or local variables, never mutable fields on a singleton use case. Require dependencies that enforce invariants; an optional repository must not silently disable authorization or relationship checks.

## Execute a command

1. Validate the trusted actor and required action with the existing authorization mechanism.
2. For resource operations, resolve the stored resource and its actual organization. Authorize that scope before exposing data or performing related writes. For create/list operations, validate the requested organization against the actor's permitted scope.
3. Parse command input with `parseSchemaOrThrow` or `safeParseAsync`; use the parsed result, not the original body.
4. Load related resources through scoped ports and check ownership, active membership, policy, and lifecycle conditions.
5. Perform the atomic write set inside the existing unit of work; map conflicts using typed application errors.
6. Return domain/read-model output. HTTP response wrapping belongs to presentation.

The project's decorator can pass its already authorized resource to `execute(context, resource)`. Reuse it rather than loading the same row again, while still enforcing atomic write predicates when concurrency matters.

## Search and reuse these existing helpers

| Helper | Responsibility | Limitation to preserve |
| --- | --- | --- |
| `parseSchemaOrThrow` | Async Zod parsing and typed validation errors | Do not duplicate the parse/error block in each new use case |
| `requireEntityExists` | Map absent lookup results to NotFoundError | Finder must respect authorization/scope |
| `requireUniqueField` | Friendly create/update duplicate check | A database uniqueness constraint still resolves races |
| `PermissionGuard` / `RequirePermission` | Action and resource-scope authorization | A permission string alone does not prove tenant ownership |
| `requireRevisionMatch` | Consistent optimistic revision validation | An in-memory comparison is not atomic concurrency control |
| `form-access`, `form-guards`, `form-reorder` | Module-specific shared workflow rules | Promote only genuinely shared semantics to application lib |
| `attendance-time`, domain `lib/leave` | Date and duration calculations | Make time zone, calendar rules, and clock input explicit |

Use named pure functions for deterministic calculations and named orchestration helpers for work requiring ports. Avoid generic `utils.ts` buckets, boolean option matrices, hidden dependency registries, and helpers that accept an entire service container. Prefer typed result unions and explicit error factories where callers have different failure semantics.

Application code may use `try/catch` for meaningful typed error translation or transaction coordination. The frontend restriction on component `try/catch/finally` does not apply to backend use cases. Do not wrap every exception just to rethrow its message.

## Transactions and concurrency

The observed `IUnitOfWork` signature is:

```ts
export interface IUnitOfWork {
  transaction<T>(work: () => Promise<T>): Promise<T>;
}
```

Its adapter must ensure every participating repository uses the same transaction connection. Nested calls, rollback, and transaction propagation require integration evidence; the interface alone does not establish these behaviors.

Group aggregate writes, target changes, history records, and ordering changes that must succeed together. Keep external HTTP/storage operations outside long DB transactions where feasible; define compensation or durable event delivery only when the actual workflow needs it.

Revision checking followed by an unconditional update can race, even inside a transaction. Ask persistence for an atomic compare-and-update using resource ID, tenant, and expected revision, or use an appropriate lock/isolation strategy. Use database unique constraints for duplicate-sensitive writes, and translate their conflicts at the adapter boundary. [PostgreSQL isolation behavior](https://www.postgresql.org/docs/current/transaction-iso.html) explains why plain reads do not serialize concurrent writers.

## Performance with evidence

- Prefer scoped batch/read-model ports over `findById` inside a result loop.
- `Promise.all` reduces waiting for independent calls but does not reduce N+1 query count; bound concurrency for large inputs.
- Avoid fetching all tenant rows just to count or test existence; add narrow `exists`/`count` ports where needed.
- Select required read fields; use Maps/Sets for repeated joins or membership tests.
- Inject or pass a clock for time-sensitive calculations and use a single operation timestamp.
- Measure query counts, row volumes, and timings before claiming a performance improvement. SQL/index/EXPLAIN work belongs to persistence.

## Verification by behavior

For a changed workflow, cover relevant cases: missing/inactive actor, another tenant's IDs, stale membership, disabled feature, missing action, invalid transition, revision conflict, duplicate creation, and rollback of partial writes. Include catalog integrity checks for duplicate actions, unknown feature mappings, and unknown default grants. Keep test and runtime verification proportional to the change; documentation edits need structural checks rather than application execution.
