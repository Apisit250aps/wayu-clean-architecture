# Domain design: modules, constants, schemas, and ports

## Ownership and layout

The reference project groups schema/entity/repository files by capability and groups use-case contracts in `src/applications/<module>/`. Preserve these imports when extending it. A large module can introduce `schema/form/{template,plan,submission}.ts` with a compatibility barrel, provided package export resolution and the entity-to-TypeSpec generator are updated together.

Domain owns business values, source facts, state transitions, pure calculations, entity shapes, repository contracts, security-context types, and `IUnitOfWork`. Domain does not query databases or instantiate adapters.

## Constants are part of module delivery

For every new module or table:

- Create or update `src/constants/<module>.ts` and its public export.
- Identify resource codes and actual finite values (status, action, mode, limits). Reuse an existing aggregate's constants for its internal tables; record that mapping explicitly.
- Add system permission actions and feature metadata only where the business capability requires them; update the central catalogs and explicit seed grants together.
- Reuse the same values in Zod enums, application checks, DB enum definitions, and API contracts where supported. Keep the dependency direction inward.
- Do not put mutable tenant settings, translated UI labels, SQL names, credentials, or arbitrary invented defaults in domain constants.

Example for a new inspection capability:

```ts
/** Stable business vocabulary; child tables share the inspection capability. */
export const INSPECTION_RESOURCES = {
  PLAN: 'inspection_plan',
  ANSWER: 'inspection_answer',
} as const;

export const INSPECTION_STATUS_VALUES = ['DRAFT', 'ACTIVE', 'CLOSED'] as const;
export type InspectionStatus = (typeof INSPECTION_STATUS_VALUES)[number];

export const INSPECTION_LATE_POLICY_VALUES = ['ALLOW', 'DENY'] as const;
export type InspectionLatePolicy =
  (typeof INSPECTION_LATE_POLICY_VALUES)[number];
```

Constants are leaf modules: avoid importing schema runtime values back into a constants module consumed by that schema. Derive union types from constants and use `satisfies` to check catalog shapes without widening literal values. A built-in catalog union need not close a runtime extension point: the reference project's `PermissionAction = string` supports dynamic action records while `SystemPermissionAction` enumerates built-ins. Validate dynamic action syntax and ownership at its registration boundary.

## Schema-first contracts

Reuse the project's `BaseEntity`, `AppendOnlyBaseEntity`, and typed field helpers after inspecting their semantics. Do not copy older helper implementations with `any` into a new module.

Keep a reusable object shape and derive operation-specific create/update schemas before attaching operation-specific object refinements. If extending a refined Zod schema, use the installed version's supported API, such as `safeExtend`; do not assume all shape transformations preserve every invariant. See [Zod's schema APIs](https://zod.dev/api).

Separate client-writable fields from server-owned tenant IDs, actor IDs, revisions, and audit timestamps. An entity schema is not automatically a safe create/update command. Derive allowed fields deliberately, then combine validated input with trusted scope inside the application layer. Distinguish omitted values from explicit nulls. When transforms exist, distinguish `z.input` from `z.output`.

Entities in this project are data classes implementing inferred schema shapes. Keep calculations in named pure functions rather than adding persistence or transport behavior to entities. Persist source facts and indispensable history; derive reproducible counts, totals, or display statuses unless a documented snapshot requirement needs stored values.

## Purpose-specific ports

Use narrow interfaces named for business operations. Reuse the existing base repository when its CRUD semantics fit; history or append-only resources should expose only legal operations, not inherit destructive updates/deletes by convenience.

Tenant-owned ports need tenant scope in their lookup/list/update operations, or an explicit documented ownership check before their result is used. Example contract, to be implemented in persistence rather than assumed to exist:

```ts
export interface IInspectionRepository {
  findByIdAndOrganization(
    id: string,
    organizationId: string,
  ): Promise<Inspection | null>;
  updateIfRevisionMatches(input: {
    id: string;
    organizationId: string;
    expectedRevision: number;
    status: InspectionStatus;
  }): Promise<Inspection | null>;
}
```

Here `null` on conditional update denotes no matching scoped row/revision; the application maps it according to its established conflict policy. The implementation must enforce the condition atomically.

Use bounded list filters, paging, and batch lookup ports when the workflow needs them. Keep Drizzle predicates, SQL types, connection objects, and query builders out of these contracts.
