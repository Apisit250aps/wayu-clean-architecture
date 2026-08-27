# Wayu Clean Architecture - AI Agent Skills Collection 🏛️

A modular collection of **AI Agent Skills** designed for building robust, scalable applications using **Clean Architecture** principles.

Compatible with **`npx skills add`**, Claude Code, Cursor, GitHub Copilot, Antigravity, and any Agent Skills-compliant AI tool.

---

## 📦 How to Install Skills

You can install all skills or select specific skills into your project using the **Skills CLI**:

### Install to your project
```bash
# Interactive selection (choose from all available skills)
npx skills add Apisit250aps/wayu-clean-architecture

# Or using full GitHub URL
npx skills add https://github.com/Apisit250aps/wayu-clean-architecture
```

### Install a specific skill
```bash
npx skills add Apisit250aps/wayu-clean-architecture --skill clean-architecture-setup
```

### Install a specific Release / Version Tag 🏷️
```bash
# Install from a specific version/tag (e.g. v1.0.0)
npx skills add Apisit250aps/wayu-clean-architecture#v1.0.0

# Install a specific skill from a release version
npx skills add Apisit250aps/wayu-clean-architecture#v1.0.0 --skill clean-architecture-monorepo
```

### Install globally (available in all projects)
```bash
npx skills add Apisit250aps/wayu-clean-architecture -g
```

---

## 🛠️ Available Skills

| Skill Name | Scope / Tag | Description | Key Focus |
| :--- | :--- | :--- | :--- |
| **`clean-architecture-feature`** | `🏷️ Both (Fullstack)` | 🚀 **Master Orchestrator**: End-to-end generator creating complete features/modules across ALL layers. | 7-step pipeline (Domain -> Database -> Application -> Infrastructure -> Presentation -> Verify). |
| **`clean-architecture-monorepo`** | `🏷️ Both (Fullstack)` | 📦 **Package Initializer**: Scaffold new packages (`domains`, `database`, `applications`, `infrastructures`, etc.). | Generates `package.json` with `#imports`, `tsconfig.json`, `eslint.config.mjs` layer boundaries. |
| **`clean-architecture-setup`** | `🏷️ Both (Fullstack)` | Initialize or scaffold Clean Architecture projects across various tech stacks. | Folder structure, DI container wiring, Prettier/ESLint, boundary configuration. |
| **`clean-architecture-domain`** | `🏷️ Both (Shared)` | Design and implement pure Domain Layer components. | Schema-First Zod (`BaseEntity`), pure data Entities, Repository interfaces, Use Case contracts. |
| **`clean-architecture-database-drizzle`** | `🏷️ Backend` | Scaffold, configure, and implement the Database Layer using Drizzle ORM. | Drizzle table schemas, UUIDv7 helpers, `defineRelationsPart`, Drizzle client, base `Repository<T,C,U>`. |
| **`clean-architecture-application`**| `🏷️ Backend` | Implement Application Layer Use Cases and Business Workflows. | Use Case implementations, `safeParseAsync` validation, typed error hierarchy (`lib/error.ts`). |
| **`clean-architecture-infrastructure`** | `🏷️ Backend` | Implement Infrastructure Layer adapters and external integrations. | Drizzle generic `Repository<T,C,U>` base (`super(db, table)`), custom queries, Argon2 auth. |
| **`clean-architecture-presentation`**| `🏷️ Both (Shared)` | Implement Presentation Layer handlers, controllers, and APIs. | Hono REST Controllers, Ponytail grouping, input validation, structured API responses. |
| **`clean-architecture-typespec`** | `🏷️ Both (Fullstack)` | Design TypeSpec (`.tsp`) API specs & generate TypeScript Axios/React Query Client SDKs. | Model Aliasing (`Domain.Entity`), `OmitProperties`/`OptionalProperties` DTO transforms, Hey-API. |
| **`clean-architecture-frontend`** | `🏷️ Frontend` | Frontend architecture: Separation of Design System (`packages/ui`) vs Combined Components (`apps/web`). | Primitives vs Compound UI, react-hook-form, TanStack Table, Client SDK. |
| **`clean-architecture-format`** | `🏷️ Both (Fullstack)` | Enforce naming conventions, file organization, and architectural linting rules. | File suffixes (`.entity`, `.usecase`, etc.), dependency boundary rules, ESLint / Depcruise configs. |
| **`clean-architecture-validator`** | `🏷️ Both (Fullstack)` | 🛡️ **AI Auditor**: Audit codebase for Clean Architecture violations. | Detect layer leaks, illegal `any`/`@ts-ignore`, bypassed use cases, synchronous `.parse()`. |

---

## 📐 Clean Architecture Dependency Rule

```
┌────────────────────────────────────────────────────────┐
│  Presentation / Web / UI Layer                         │
│  (Controllers, Routes, Middlewares, Presenters)        │
│    │                                                   │
│    ▼                                                   │
│  Application Layer                                     │
│  (Use Cases, Interactors, CQRS, DTOs, Ports)           │
│    │                                                   │
│    ▼                                                   │
│  Domain Layer (Pure Business Logic)                    │
│  (Entities, Value Objects, Domain Events, Repos Interfaces)
│    ▲                                                   │
│    │ (Inverted via Interfaces/Ports)                   │
│  Infrastructure Layer                                  │
│  (Database, ORM, External APIs, Caching, Adapters)     │
└────────────────────────────────────────────────────────┘
```

> **The Golden Rule**: Source code dependencies must only point **inward** toward the Domain.
> - **Domain** depends on **nothing** (no frameworks, no ORMs).
> - **Application** depends only on **Domain**.
> - **Infrastructure** & **Presentation** depend on **Application** and **Domain**.

---

## 📂 Repository Structure

```text
wayu-clean-architecture/
├── README.md
└── skills/
    ├── clean-architecture-feature/
    │   ├── SKILL.md
    │   └── references/
    │       ├── feature-generation-guide.md
    │       └── end-to-end-example.md
    ├── clean-architecture-monorepo/
    │   ├── SKILL.md
    │   └── references/
    │       └── package-presets.md
    ├── clean-architecture-setup/
    │   ├── SKILL.md
    │   └── references/
    │       ├── architecture-overview.md
    │       └── starter-libraries.md
    ├── clean-architecture-domain/
    │   ├── SKILL.md
    │   └── references/
    │       └── domain-patterns.md
    ├── clean-architecture-database-drizzle/
    │   ├── SKILL.md
    │   └── references/
    │       └── drizzle-patterns.md
    ├── clean-architecture-application/
    │   ├── SKILL.md
    │   └── references/
    │       └── usecase-patterns.md
    ├── clean-architecture-infrastructure/
    │   ├── SKILL.md
    │   └── references/
    │       └── infrastructure-patterns.md
    ├── clean-architecture-presentation/
    │   ├── SKILL.md
    │   └── references/
    │       └── presentation-patterns.md
    ├── clean-architecture-typespec/
    │   ├── SKILL.md
    │   └── references/
    │       └── typespec-patterns.md
    ├── clean-architecture-frontend/
    │   └── SKILL.md
    ├── clean-architecture-format/
    │   ├── SKILL.md
    │   └── references/
    │       └── naming-and-style.md
    └── clean-architecture-validator/
        ├── SKILL.md
        └── references/
            └── validation-checklist.md
```

---

## 🚀 How AI Agents Use These Skills

1. **Progressive Loading**: AI agents initially read only the frontmatter `name` and `description`.
2. **Context Activation**: When you ask your agent to *"Create a new Use Case for user registration"* or *"Review my repository for layer leaks"*, the agent automatically loads the corresponding `SKILL.md` and referenced guidelines.
3. **Execution**: The agent strictly follows the design patterns, code templates, and constraints defined in each skill.

---

## 📄 License
MIT License. Created by [Apisit250aps](https://github.com/Apisit250aps).
