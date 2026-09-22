---
name: clean-architecture-validator
description: Audit and validate codebases against Clean Architecture monorepo rules — detects layer boundary leaks, bypassed use cases, illegal any/@ts-ignore, missing safeParseAsync, unhandled typed errors, and improper cross-package imports.
metadata:
  tags: both, fullstack, backend, frontend
---

# Clean Architecture Validator & Auditor Skill 🛡️

Use this skill when reviewing, auditing, or diagnosing codebases for compliance with **Clean Architecture Monorepo rules**.

---

## 🎯 Primary Responsibilities

When asked to *"Audit codebase"*, *"Check Clean Architecture rules"*, or *"Find layer leaks"*, this skill scans the workspace for:

1. **Layer Import Leaks**: Inward packages importing outward packages (`domains` importing `database`/`applications`/`infrastructures`, or `applications` importing `infrastructures`/`database`).
2. **Bypassed Use Cases**: Presentation controllers or routes importing repositories or querying databases directly instead of invoking Use Cases.
3. **Zero-Tolerance Violations**:
   - Usage of `any` types (must use `unknown` with narrowing).
   - Usage of `// @ts-ignore`, `// @ts-expect-error`, or `// @ts-nocheck`.
   - Usage of `/* eslint-disable */` or `// eslint-disable`.
4. **Validation Flaws**: Using synchronous `.parse()` inside use cases instead of `await schema.safeParseAsync()`.
5. **Untyped Generic Errors**: Throwing raw `new Error()` instead of typed application errors (`NotFoundError`, `ValidationError`, `DuplicateError`, `UnauthorizedError`, `ForbiddenError`).
6. **Persistence Leaks into Domain**: Importing Drizzle ORM, table schemas, or DB connection inside `packages/domains`.
7. **Frontend Boundary Leaks**: `packages/ui` importing business-specific hooks, generated services, or backend packages. Domain-neutral RHF fields, tables, and overlays are permitted.
8. **Missing Module Constants**: New modules/tables without owning constants, explicit aggregate permission mapping, or affected feature/action/default-grant catalog updates.
9. **Tenant and Workflow Gaps**: Caller-controlled security attributes, unscoped resource access, cross-tenant references, optional dependencies that skip invariants, and revision checks without atomic persistence enforcement.
10. **Duplicated or Inefficient Patterns**: Copied parsing/guards/mappers, oversized shared helper interfaces, N+1 queries, unbounded lists, and unsupported performance claims.

---

## 🔍 Layer Audit Matrix

| Package / Layer | Permitted Imports | Prohibited Imports | Architectural Violations |
| :--- | :--- | :--- | :--- |
| **`packages/domains`** | Pure language types, `zod`, `uuid` (`uuidv7`). | `@<project>/database`, `@<project>/applications`, `@<project>/infrastructures`, `@<project>/ui`, `@<project>/client`, ORMs, HTTP libs. | Any external dependency other than Zod/UUID; ORM schemas inside domain. |
| **`packages/database`** | `@<project>/domains`, `drizzle-orm`, `pg`, `uuid`. | `@<project>/applications`, `@<project>/infrastructures`, `@<project>/ui`, `@<project>/client`. | Business logic in DB schemas; directly implementing use cases. |
| **`packages/applications`** | `@<project>/domains` (schemas, entities, interfaces). | `@<project>/database`, `@<project>/infrastructures`, `@<project>/ui`, `@<project>/client`, HTTP types (`Request`/`Response`). | Direct database queries; using `.parse()` instead of `safeParseAsync`; throwing untyped raw `Error`. |
| **`packages/infrastructures`**| Domain/database and adapter dependencies; isolated composition roots may import application implementations. | UI or browser dependencies inside repositories; concrete adapters imported by core. | Duplicated CRUD mechanics; missing scoped/atomic write semantics; transaction connection not propagated. |
| **`packages/client`** | `@typespec/*`, `@hey-api/*`, `Domain.Entity.*`. | Direct usage of `Domain.Entity.<Model>` in services (must alias in `spec/models/`). | Rewriting request DTO properties manually instead of using `OmitProperties`/`OptionalProperties`. |
| **`packages/ui`** | React, styling/accessibility libraries, RHF Controllers, generic table/overlay behavior. | Backend packages, generated services, business-specific module hooks. | Tenant policy, permission decisions, or app data fetching inside generic UI. |
| **`apps/web`** | UI, generated client, pure domain contracts/constants, explicit auth integration boundaries. | DB connections or backend compositions in browser modules. | Raw transport duplicated in views; form state mirrored with effects. |

---

## 🚀 How to Conduct an Architectural Audit

When running an audit, follow these 4 steps:

### 1. Run Automated Lints & Boundaries
```bash
npm run check-types   # 1. TypeScript compilation check
npm run lint          # 2. ESLint no-restricted-imports check
```

### 2. Search for Zero-Tolerance Violations
Search for illegal bypasses across all packages:
- `rg -n '@ts-ignore|eslint-disable|: any' packages/*/src apps/*/src`

### 3. Check Application Use Cases
- Verify command input uses `await schema.safeParseAsync(context.data)` or the shared `parseSchemaOrThrow`; inspect helper behavior rather than requiring copied validation code.
- Verify errors use `ValidationError`, `NotFoundError`, `DuplicateError`, etc.
- Verify repositories are injected via constructor interface (`I<Module>Repository`).

### 4. Check Presentation Controllers (discover `apps/api` or the existing server entry)
- Verify controllers use the established composition root to obtain Use Cases.
- Verify no controller injects or calls a Repository directly.
- Verify endpoints follow the **Ponytail Principle** (grouped by domain module, not over-fragmented into single-method files).

Audit is read-only unless changes were requested. Report source path, failing scenario, evidence, impact, and proposed remediation. Distinguish existing conventions from required improvements; use the current core/frontend guidance where older examples disagree.

---

## 📋 Audit Report Output Template

When reporting audit findings to the user, format the output as follows:

```markdown
# 🛡️ Clean Architecture Audit Report

## Summary
- **Total Violations**: X
- **Critical (Layer Leaks / Direct DB bypass)**: X
- **Code Quality (any / @ts-ignore / synchronous parse)**: X

## 🚩 Detected Violations

### 1. [CRITICAL] Illegal Layer Import
- **File**: `packages/applications/src/use-cases/order.usecase.ts:4`
- **Violation**: Importing `db` from `@<project>/database/db` directly inside Use Case.
- **Remedy**: Inject `IOrderRepository` via constructor and call repository method instead.

### 2. [WARNING] Synchronous .parse() Used
- **File**: `packages/applications/src/use-cases/user.usecase.ts:18`
- **Violation**: `createUserSchema.parse(context.data)` throws unhandled ZodError.
- **Remedy**: Replace with `const parsed = await createUserSchema.safeParseAsync(context.data)` and throw `ValidationError`.

### 3. [QUALITY] Zero-Tolerance `any` Usage
- **File**: `packages/infrastructures/src/repositories/product.repo.ts:25`
- **Violation**: Parameter typed as `any`.
- **Remedy**: Use explicit entity type or `unknown` with type narrowing.
```

---

## 📚 Further Reference

- [validation-checklist.md](references/validation-checklist.md): Comprehensive checklist and red flags for Clean Architecture monorepos.
