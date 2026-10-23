---
name: clean-architecture-foundation
description: Set up or extend a Clean Architecture Turborepo workspace, including package scaffolding, naming, formatting, and dependency-boundary enforcement.
---

# Clean Architecture Foundation

Use this skill when creating a workspace, adding a package, or changing shared TypeScript, formatting, import, or boundary configuration. Do not use it for a feature implementation inside an established layer; use that layer's skill instead.

## Choose the smallest mode

- **Workspace setup:** establish the root layout, shared tooling, and dependency direction. Read [architecture overview](references/architecture-overview.md) first; read [starter libraries](references/starter-libraries.md) only when installing those implementations.
- **Package setup:** add or repair one package's manifest, exports/imports, TypeScript config, ESLint rules, and starter layout. Read [package presets](references/package-presets.md).
- **Conventions:** change names, Prettier, or boundary enforcement. Read [naming and style](references/naming-and-style.md).

## Invariants

Keep dependencies inward: domains has no internal dependency; database and applications depend on domains; infrastructures depends on domains and database; interface packages may depend on the layers they compose. Configure the restriction where it is enforceable, and verify with the workspace's type-check and lint commands.

Repository ownership is stricter than package import direction: each repository accesses only its owned tables, with no direct or indirect dependency on another owner. Application Services compose owner ports; SQL JOINs, read models, helper queries, locks, and audit do not bypass this rule. Use [the ownership reference](../clean-architecture-persistence/references/repository-boundaries.md) when designing boundaries or enforcement, including schema/view/function/helper paths and caller wiring. Import lint alone cannot prove ownership.

## Conditions and JSDoc

When writing or changing JavaScript/TypeScript, document every condition with Thai JSDoc, not only declarations or complex branches. Cover guards, if/else, switch, ternary, logical/nullish/optional expressions, loop/callback predicates, schema validation, and query conditions. Follow [the condition guide](../clean-architecture-docs/references/jsdoc.md#conditions); preserve logic and explain the checked fact, reason, and outcomes rather than restating the operator.

## Growing a modular workspace

Inspect current manifests, aliases, shared configs, constants, and helper libraries before scaffolding copies. Include domain constants and module-level exports in presets for new capabilities. Preserve public import paths when splitting large modules and verify entity/client generators still discover the moved files.

Shared libraries follow ownership, not a blanket ban on composition: domain-neutral RHF fields, tables, and overlays belong in UI; tenant/business orchestration belongs in Web or Application. The current core/frontend skills govern new work if an older starter example is more restrictive. A composition root may wire Application implementations to infrastructure adapters; keep that wiring isolated from the inner core and browser bundles.

## Helper files and imports

In every layer, import utils, lib, and helper symbols directly from their concrete file or explicit package subpath. Never import them through an `index.ts` barrel, an aggregate re-export, or a package root that re-exports them. Package export maps may expose concrete subpaths; unrelated domain/entity/constants barrels remain governed by the existing architecture.

Keep standalone function declarations and helper arrow functions out of Application/use-case files and any file defining a class. Extract them into cohesive utils/helper/lib files owned by the same package and import them directly. Class constructors and methods remain in their class; this rule does not prohibit method bodies or necessary inline callbacks.

For an illustrative multi-layer wiring example, read [the Product walkthrough](references/end-to-end-example.md) only when useful. Apply the current layer skills over older example patterns.
