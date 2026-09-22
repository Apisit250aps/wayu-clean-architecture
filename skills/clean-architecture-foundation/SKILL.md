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

## Growing a modular workspace

Inspect current manifests, aliases, shared configs, constants, and helper libraries before scaffolding copies. Include domain constants and module-level exports in presets for new capabilities. Preserve public import paths when splitting large modules and verify entity/client generators still discover the moved files.

Shared libraries follow ownership, not a blanket ban on composition: domain-neutral RHF fields, tables, and overlays belong in UI; tenant/business orchestration belongs in Web or Application. The current core/frontend skills govern new work if an older starter example is more restrictive. A composition root may wire Application implementations to infrastructure adapters; keep that wiring isolated from the inner core and browser bundles.
