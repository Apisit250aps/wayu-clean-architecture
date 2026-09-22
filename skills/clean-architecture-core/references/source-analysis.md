# Reference project analysis

Inspected `security-project` under `Workspaces/Chilltalk` on 2026-09-22. Paths below are relative to that reference repository. These observations guide the skill; they do not claim every existing workflow already meets the new rules.

## Domain

- `src/constants/features.ts`: FEATURE_CODES and SYSTEM_FEATURES define built-in capability metadata.
- `src/constants/system-permissions.ts`: PERMISSION_ACTIONS and SYSTEM_PERMISSIONS connect actions to modules and feature codes.
- `src/constants/roles.ts`: SYSTEM_DEFAULT_ROLES and explicit SYSTEM_DEFAULT_ROLE_PERMISSIONS separate catalog defaults from tenant assignments.
- `src/constants/permissions.ts`: ISecurityContext, WithSecurityContext, and isTenantConfigurablePermission distinguish platform restrictions from tenant-manageable actions.
- `src/schema/form.ts`: many lifecycle/field/policy values still live inline with schemas. New modules should place these in their owning constants file; migrate existing public exports deliberately.
- `src/applications/<module>/*` defines contexts/contracts; `src/repositories/*` defines ports. Root `src/index.ts` owns BaseUseCase, BaseRepository, and IUnitOfWork.

## Application

- `src/lib/validation.ts`, `guards.ts`, and `concurrency.ts` already provide parseSchemaOrThrow, existence/uniqueness helpers, and requireRevisionMatch.
- `src/decorators/permission.decorator.ts` resolves a resource, verifies its stored organization, and passes that same resource into the method. `src/lib/guard.ts` uses a trusted actor/session context.
- `src/use-cases/organization/site.usecase.ts` demonstrates scoped uniqueness and stored-tenant checks; it still repeats literal permission actions and inline parsing.
- `src/use-cases/form/form-access.ts` reuses active membership, assignment, occurrence, and late-policy checks.
- `src/use-cases/form/form-plan.usecase.ts` injects IUnitOfWork and multiple ports for an aggregate workflow. It also illustrates growing constructor/workflow complexity and repeated membership logic.
- `src/use-cases/feature/role-feature.usecase.ts` models feature entitlement and role assignment as data. Its methods require individual scope review; its existence is not evidence that all tenant checks are complete.
- `src/repositories/form.repo.ts` in Domain includes batch ports such as findByAssignmentIds and findByAnswerIds; use these patterns for list workflows instead of repeated row lookups.

## Improvements encoded by this revision

Require constants for new module/table work; reuse typed helpers rather than copied templates; organize large capabilities by cohesive workflows; keep trusted tenant ownership separate from request input; distinguish application revision checks from atomic database writes; share pure calculations and narrow ports before introducing generic frameworks.

The prior core templates contained `any` field helpers and unscoped user CRUD examples. They have been replaced with the module/port guidance. No runtime implementation, database migration, or behavior change in the reference project is part of this skill update.
