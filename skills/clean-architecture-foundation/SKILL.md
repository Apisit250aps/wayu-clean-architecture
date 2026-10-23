---
name: clean-architecture-foundation
description: Set up or extend Clean Architecture workspaces, packages, shared tooling, and dependency boundaries. Use layer skills for feature implementation.
---

# Clean Architecture Foundation

Inspect repository instructions, manifests, exports, aliases, and shared tooling before changing them. Read only the reference sections needed for the requested setup.

## Choose the work

| Work | Read |
| --- | --- |
| Workspace layout or import boundaries | [Architecture overview](references/architecture-overview.md) |
| Package manifests, exports, TypeScript or lint setup | [Package presets](references/package-presets.md) |
| Naming, formatting or enforcement | [Naming and style](references/naming-and-style.md) |
| Shared library scaffolding | [Starter library decisions](references/starter-libraries.md); reuse existing code first |
| Date/time handling or its lint rules | [Time handling](references/time-handling.md) |
| Example of multi-layer wiring | [Product walkthrough](references/end-to-end-example.md), only when useful |

## Boundaries

- Domain has no internal package dependencies. Applications depend on Domain; persistence adapters depend on Domain and database mechanics. Only an isolated composition root wires concrete adapters to Application implementations.
- A repository owns its tables and has no repository dependency, direct or indirect. Application Services coordinate multiple owners. For ownership/enforcement changes, read [repository boundaries](../clean-architecture-persistence/references/repository-boundaries.md); import lint alone cannot prove compliance.
- Preserve public imports and generator discovery when splitting modules. New capabilities include their owning constants and exports.
- Shared UI may compose generic RHF fields/tables/overlays; business orchestration belongs in Web/Application. Keep backend wiring out of browser bundles.

## Helper files and imports

Import utils/lib/helpers from concrete files or explicit package subpaths, never barrels/root re-exports. Keep standalone helpers outside Application/use-case and class files, in their owning package. Constructors, class methods, and necessary inline callbacks remain allowed.

## Code and verification

Use explicit types or narrowed `unknown`; no `any`, TypeScript suppression, or lint-disable comments. Every new/changed condition needs Thai JSDoc explaining its fact, reason, and outcomes; use the [condition guide](../clean-architecture-docs/references/conditions.md) for placement/coverage.

Dates use native `Date` and direct date-fns imports; no Temporal, shared date wrapper, or clock port. Use cases sample `now` once, repositories receive it, and Web/UI owns display formatting. Read the time reference when that behavior changes.

Run affected type/lint/export checks using repository commands; test changed enforcement with a temporary violating import and remove the probe. Report actual checks and remaining gaps.
