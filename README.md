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
# Install from a specific version/tag (e.g. v2.0.0)
npx skills add Apisit250aps/wayu-clean-architecture#v2.0.0

# Install a specific skill from a release version
npx skills add Apisit250aps/wayu-clean-architecture#v2.0.0 --skill clean-architecture-core
```

### Install globally (available in all projects)
```bash
npx skills add Apisit250aps/wayu-clean-architecture -g
```

### Upgrading from v0.5.0

Version 1.0.0 consolidates 12 skills into 7. Update explicit skill invocations and local references using this mapping, then reinstall the selected skills. Review and remove obsolete local copies so agents do not load conflicting instructions.

| Previous skills | Replacement |
| :--- | :--- |
| `clean-architecture-setup`, `clean-architecture-monorepo`, `clean-architecture-format` | `clean-architecture-foundation` |
| `clean-architecture-domain`, `clean-architecture-application` | `clean-architecture-core` |
| `clean-architecture-database-drizzle`, `clean-architecture-infrastructure` | `clean-architecture-persistence` |
| `clean-architecture-presentation`, `clean-architecture-typespec` | `clean-architecture-api` |

In v1.0.0, `clean-architecture-feature`, `clean-architecture-frontend`, and `clean-architecture-validator` retained their names. For v2.0.0, also apply the migration below. See [release notes](CHANGELOG.md) for behavioral changes.

---

## Upgrading from v1.0.0

Version 2.0.0 replaces `clean-architecture-feature` with `clean-architecture-plan` for task planning. Implementation uses the affected Core, Persistence, API, and Frontend skills directly; cross-layer delivery review belongs to Validator. Update explicit invocations and remove obsolete installed Feature copies after reinstalling. The collection still has seven skills.

Utils/lib/helpers now require concrete-file imports. Extract standalone helpers from Application/use-case and class files into their owning package; constructors, class methods, and necessary inline callbacks remain allowed. Use RHF/Controller for editable inputs in form/query/mutation-driven Web components, with React Query retaining server state.

## 🛠️ Available Skills

| Skill Name | Scope / Tag | Description | Key Focus |
| :--- | :--- | :--- | :--- |
| **`clean-architecture-plan`** | `🏷️ Planning` | Create coded, layer-separated task plans. | Thai Trello README, English AI tasks, linked checklists, and reusable templates. |
| **`clean-architecture-foundation`** | `🏷️ Both (Fullstack)` | Set up a workspace or package and its shared conventions. | Turborepo setup, package presets, Prettier, and dependency boundaries. |
| **`clean-architecture-core`** | `🏷️ Backend` | Design modular Domain and Application workflows for configurable tenant systems. | Module constants/catalogs, scoped ports, shared validation/policies, unit of work, and concurrency. |
| **`clean-architecture-persistence`** | `🏷️ Backend` | Implement concrete storage and repository adapters. | Drizzle schemas, migrations, relations, generic repositories, and infrastructure. |
| **`clean-architecture-api`** | `🏷️ Both (Fullstack)` | Deliver HTTP contracts and handlers. | TypeSpec, OpenAPI, generated client SDKs, controller validation, and error mapping. |
| **`clean-architecture-frontend`** | `🏷️ Frontend` | Build feature-oriented Next.js UI with reusable `@repo/ui` components and generated API contracts. | React Hook Form Controllers, React Query hooks, React Aria, shadcn, and TypeSpec client boundaries. |
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
    ├── clean-architecture-plan/
    │   ├── SKILL.md
    │   └── assets/
    │       ├── main-task.README.md
    │       └── task.md
    ├── clean-architecture-foundation/
    │   ├── SKILL.md
    │   └── references/
    │       ├── end-to-end-example.md
    │       ├── architecture-overview.md
    │       ├── naming-and-style.md
    │       ├── package-presets.md
    │       └── starter-libraries.md
    ├── clean-architecture-core/
    │   ├── SKILL.md
    │   └── references/
    │       ├── domain-patterns.md
    │       ├── usecase-patterns.md
    │       ├── tenant-policy-design.md
    │       └── source-analysis.md
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
    │   ├── SKILL.md
    │   └── references/
    │       └── frontend-patterns.md
    └── clean-architecture-validator/
        ├── SKILL.md
        └── references/
            └── validation-checklist.md
```

---

## Task planning

Use `$clean-architecture-plan` to create `plans/<task-code>-<ชื่อ main task>/README.md` with a short Thai Trello summary and linked direct-child checklist. English AI instructions live in `tasks/`; deeper subtasks are linked only from their parent task. Web, Backend (API/client/infra/domains/application), and Database (domains/database) have separate main tasks, with explicit ownership for shared domain changes. Templates are included in the skill assets.

Across implementation skills, utils/lib/helpers use concrete-file imports and standalone helpers live outside use-case/class files. Web editable form/input state uses RHF/Controller; React Query owns server state.

## 🚀 How AI Agents Use These Skills

1. **Progressive Loading**: AI agents initially read only the frontmatter `name` and `description`.
2. **Context Activation**: When you ask your agent to *"Create a new Use Case for user registration"* or *"Review my repository for layer leaks"*, the agent automatically loads the corresponding `SKILL.md` and referenced guidelines.
3. **Execution**: The agent strictly follows the design patterns, code templates, and constraints defined in each skill.

---

## 📄 License
MIT License. Created by [Apisit250aps](https://github.com/Apisit250aps).
