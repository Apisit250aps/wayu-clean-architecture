---
name: clean-architecture-monorepo
description: Guidelines and blueprints for Turborepo Monorepo Clean Architecture (packages/domains -> packages/database -> packages/applications -> packages/infrastructures -> apps/web with Hono and Drizzle ORM).
---

# Turborepo Monorepo Clean Architecture Skill 🏛️

Use this skill when developing, scaffolding, or maintaining a **Turborepo Monorepo** using Clean Architecture principles.

---

## 📐 Monorepo Dependency Flow

The workspace is organized into discrete packages where dependencies strictly point inward:

```
[apps/web (Next.js + Hono API + UI)]
    │
    ▼
[packages/infrastructures] ──▶ Concrete Repositories, Auth, External APIs
    │
    ▼
[packages/applications]    ──▶ Use Cases / Interactors, lib/error.ts
    │
    ▼
[packages/database]        ──▶ Drizzle ORM Schema, DB Connection, Generic Repository
    │
    ▼
[packages/domains]         ──▶ (Innermost) Entities, Zod Schemas, Repository Interfaces, Contexts
```

---

## 📦 Package Responsibilities

### 1. `packages/domains` (Innermost Core)
- **Role**: Pure business rules, data models, Zod validation schemas, and abstract contracts.
- **Rules**: Zero dependencies on internal packages (`database`, `applications`, `infrastructures`, `apps`).
- **Contains**:
  - `src/lib/entity.ts`: Zod Entity builder (`BaseEntity`, `StringField`, `EmailField`, `UUIDField`, etc.)
  - `src/schema/`: Zod schemas (`userSchema`, `createUserSchema`, `updateUserSchema`)
  - `src/entities/`: Entity classes implementing inferred schema types (`User implements UserEntity`)
  - `src/repositories/`: Repository interfaces extending `BaseRepository<Entity, CreatePayload, UpdatePayload>`
  - `src/applications/`: Context types (`ICreateUserContext`) and Use Case interfaces (`BaseUseCase<Context, Output>`)

### 2. `packages/database` (Data Access Core)
- **Role**: Drizzle ORM schemas, database migrations, connection pool, and base repository abstraction.
- **Rules**: Can depend on `domains` for types. Must NOT depend on `applications`, `infrastructures`, or `apps`.
- **Contains**:
  - `src/schema/`: Drizzle table schemas (`pgTable`, `relations`)
  - `src/repository.ts`: Abstract `Repository<T, C, U> extends BaseRepository<T, C, U>` implementing generic CRUD operations
  - `src/lib/utils.ts`: Drizzle helpers (`primaryKeyUuid7`, `updatedAtTimestamp`, `createdAtTimestamp`)

### 3. `packages/applications` (Application Business Rules)
- **Role**: Implements business workflows and Use Cases.
- **Rules**: Depends on `domains`. Cannot depend on `infrastructures` or `database` directly. Must use Constructor Dependency Injection.
- **Contains**:
  - `src/use-cases/`: Use case classes implementing domain use case contracts (`CreateUserUseCase implements ICreateUserUseCase`)
  - `src/lib/error.ts`: Standardized error classes (`ValidationError`, `NotFoundError`, `DuplicateError`, `AppError`) and `ApiResponse<T>`

### 4. `packages/infrastructures` (Adapters & External Drivers)
- **Role**: Concrete implementations of interfaces defined in `domains`.
- **Rules**: Depends on `domains`, `database`, and `applications`.
- **Contains**:
  - `src/repositories/`: Concrete repositories extending `database/Repository` and implementing domain repository interfaces (`UserRepository extends Repository<User, CreateUser, UpdateUser> implements IUserRepository`)
  - `src/lib/password.ts`: Argon2 password hashing and verification
  - `src/auth/`: Better Auth integration

### 5. `apps/web` (Presentation & Composition Root)
- **Role**: UI, Next.js Pages/App router, Hono API routes, and DI Container.
- **Rules**:
  - **Shared DI (`src/shared/`)**: Wire singletons for repositories (`shared/repositories`) and use cases (`shared/applications`).
  - **Controllers (`src/api/controllers/`)**: Extend base `Controller` and use `this.validator({ body, query, params })`.
  - **Ponytail Principle**: Group related endpoints by domain module rather than over-fragmenting into tiny files.
  - **Global Error Handler**: Use `onApiError` to map `AppError` to HTTP status codes.

---

## 🔗 Subpath Imports (`imports` & `exports` Mapping)

In modern Turborepo setups, each package defines **Subpath Imports (`#...`)** for internal imports and **Subpath Exports** for cross-package imports, avoiding messy relative paths (`../../`):

### 1. `packages/domains/package.json`
```json
{
  "name": "@shop/domains",
  "exports": {
    ".": "./src/index.ts",
    "./schema/*": "./src/schema/*.ts",
    "./entities": "./src/entities/index.ts",
    "./repositories/*": "./src/repositories/*.repo.ts",
    "./applications/*": "./src/applications/*.usecase.ts"
  },
  "imports": {
    "#lib/*": "./src/lib/*.ts",
    "#schema/*": "./src/schema/*.ts",
    "#entities/*": "./src/entities/*.ts",
    "#repositories/*": "./src/repositories/*.repo.ts",
    "#applications/*": "./src/applications/*.usecase.ts"
  }
}
```

### 2. `packages/applications/package.json`
```json
{
  "name": "@shop/applications",
  "exports": {
    ".": "./src/index.ts",
    "./use-cases/*": "./src/use-cases/*.usecase.ts",
    "./lib/*": "./src/lib/*.ts"
  },
  "imports": {
    "#lib/*": "./src/lib/*.ts",
    "#use-cases/*": "./src/use-cases/*.usecase.ts"
  }
}
```

### 3. `packages/database/package.json`
```json
{
  "name": "@shop/database",
  "exports": {
    "./db": "./src/db.ts",
    "./schema": "./src/schema/index.ts",
    "./repository": "./src/repository.ts"
  },
  "imports": {
    "#lib/*": "./src/lib/*.ts",
    "#schema/*": "./src/schema/*.ts"
  }
}
```

### 4. `packages/infrastructures/package.json`
```json
{
  "name": "@shop/infrastructures",
  "exports": {
    ".": "./src/index.ts",
    "./repositories/*": "./src/repositories/*.repo.ts",
    "./lib/*": "./src/lib/*.ts"
  },
  "imports": {
    "#lib/*": "./src/lib/*.ts",
    "#repositories/*": "./src/repositories/*.repo.ts"
  }
}
```

### 5. `packages/ui/package.json`
```json
{
  "name": "@shop/ui",
  "exports": {
    "./globals.css": "./src/styles/globals.css",
    "./components/*": "./src/components/*.tsx",
    "./lib/*": "./src/lib/*.ts",
    "./hooks/*": "./src/hooks/*.ts"
  },
  "imports": {
    "#components/*": "./src/components/*.tsx",
    "#lib/*": "./src/lib/*.ts",
    "#hooks/*": "./src/hooks/*.ts"
  }
}
```

### 6. `apps/web/package.json`
```json
{
  "name": "web",
  "imports": {
    "#api/*": "./src/api/*.ts",
    "#shared/*": "./src/shared/*.ts",
    "#components/*": "./src/components/*.tsx"
  }
}
```

---

## 🛡️ Strict Zero-Tolerance Rules

1. ❌ **No Type-Checking Bypasses**: Never use `// @ts-ignore`, `// @ts-expect-error`, or `// @ts-nocheck`.
2. ❌ **No Linting Bypasses**: Never use `// eslint-disable` or `/* eslint-disable */`.
3. ❌ **No `any`**: Always write explicit types or use `unknown` with narrowing.
4. 🛡️ **Enforce with Dependency Cruiser**: Verify boundary integrity with `.dependency-cruiser.cjs`.

---

## 📚 Further Reference

See [starter-libraries.md](../clean-architecture-setup/references/starter-libraries.md) for full copy-paste ready code implementations of all utilities.
