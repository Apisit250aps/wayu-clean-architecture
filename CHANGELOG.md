# Changelog

## v1.0.0

This release consolidates the skill collection and updates its Core and Frontend guidance from an evolved TypeScript monorepo. The major version reflects breaking skill names and architecture guidance; it does not certify the runtime behavior of projects using the skills.

### Breaking changes and migration

The collection now contains seven skills:

| Previous skills | Replacement |
| --- | --- |
| setup + monorepo + format | clean-architecture-foundation |
| domain + application | clean-architecture-core |
| database-drizzle + infrastructure | clean-architecture-persistence |
| presentation + typespec | clean-architecture-api |

The previous names all had the `clean-architecture-` prefix. Update explicit invocations, installation selections, and local references to the replacement names. Review and remove obsolete installed copies after installing the replacements. Feature, Frontend, and Validator retain their existing names.

### Core

- Design around business modules and cohesive workflows, with tenant-scoped ports and typed policy configuration.
- Require owning constants and aggregate permission mapping for each new module/table, with coordinated feature/action catalogs and explicit default grants.
- Reuse validation, permission, existence, uniqueness, concurrency, and module-local helpers.
- Distinguish trusted tenant context, persisted ownership, tenant configuration, and global catalogs.
- Clarify unit-of-work propagation, atomic revision updates, rollback, and database uniqueness requirements.
- Replace older generic CRUD templates with focused design references and source analysis.

### Frontend

- Cover apps/web, packages/ui, and the generated packages/client contract.
- Search shared components before creating new UI; allow domain-neutral RHF fields, tables, and overlays in packages/ui.
- Use React Hook Form Controllers for form fields, feature React Query hooks for server state, and shared functions for mapping and derivation.
- Avoid effects for form/derived state synchronization and follow the project rule against component try/catch/finally.
- Preserve React Aria accessibility conventions and generated-client boundaries.

### Cross-layer quality

- Keep the Feature skill focused on orchestration.
- Align Foundation, Persistence, API, and Validator with module constants, tenant scope, helper reuse, and measurable performance.
- Update the audit checklist to accept shared UI compositions and discover the actual API boundary.
- Move skill tags into supported metadata.

### Validation

- All seven skills passed the skill-creator validator.
- Local Markdown references were checked for missing targets.
- Git whitespace checks passed.
- This is a skill/documentation release; application runtime tests were not run for these changes.

### Install

```sh
npx skills add Apisit250aps/wayu-clean-architecture#v1.0.0
```

For a machine-wide installation, add `-g`.
