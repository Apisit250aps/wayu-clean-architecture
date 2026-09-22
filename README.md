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
npx skills add Apisit250aps/wayu-clean-architecture --skill clean-architecture-foundation
```

### Install a specific Release / Version Tag 🏷️
```bash
# Install from a specific version/tag (e.g. v1.0.0)
npx skills add Apisit250aps/wayu-clean-architecture#v1.0.0

# Install a specific skill from a release version
npx skills add Apisit250aps/wayu-clean-architecture#v1.0.0 --skill clean-architecture-core
```

### Install globally (available in all projects)
```bash
npx skills add Apisit250aps/wayu-clean-architecture -g
```

---

## 🛠️ Available Skills

| Skill Name | Scope / Tag | Description | Key Focus |
| :--- | :--- | :--- | :--- |
| **`clean-architecture-feature`** | `🏷️ Both (Fullstack)` | 🚀 **Feature Orchestrator**: Routes an end-to-end feature through only its affected layers. | Core → Persistence → API → Frontend → audit. |
| **`clean-architecture-foundation`** | `🏷️ Both (Fullstack)` | Set up a workspace or package and its shared conventions. | Turborepo setup, package presets, Prettier, and dependency boundaries. |
| **`clean-architecture-core`** | `🏷️ Backend` | Define business language and application workflows. | Zod schemas, entities, ports, use cases, `safeParseAsync`, typed errors. |
| **`clean-architecture-persistence`** | `🏷️ Backend` | Implement concrete storage and repository adapters. | Drizzle schemas, migrations, relations, generic repositories, and infrastructure. |
| **`clean-architecture-api`** | `🏷️ Both (Fullstack)` | Deliver HTTP contracts and handlers. | TypeSpec, OpenAPI, generated client SDKs, controller validation, and error mapping. |
| **`clean-architecture-frontend`** | `🏷️ Frontend` | Frontend architecture: Separation of Design System (`packages/ui`) vs Combined Components (`apps/web`). | Primitives vs Compound UI, react-hook-form, TanStack Table, Client SDK. |
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
    ├── clean-architecture-foundation/
    │   ├── SKILL.md
    │   └── references/
    │       ├── architecture-overview.md
    │       ├── naming-and-style.md
    │       ├── package-presets.md
    │       └── starter-libraries.md
    ├── clean-architecture-core/
    │   ├── SKILL.md
    │   └── references/
    │       ├── domain-patterns.md
    │       └── usecase-patterns.md
    ├── clean-architecture-persistence/
    │   ├── SKILL.md
    │   └── references/
    │       ├── drizzle-patterns.md
    │       └── infrastructure-patterns.md
    ├── clean-architecture-api/
    │   ├── SKILL.md
    │   └── references/
    │       ├── presentation-patterns.md
    │       └── typespec-patterns.md
    ├── clean-architecture-frontend/
    │   └── SKILL.md
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
