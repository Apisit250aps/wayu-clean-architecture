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

| Skill Name | Description | Key Focus |
| :--- | :--- | :--- |
| **`clean-architecture-monorepo`** | Specialized blueprints for Turborepo Monorepo (domains -> database -> applications -> infrastructures -> web). | Monorepo package boundaries, Hono Controller, Ponytail principle, Drizzle ORM. |
| **`clean-architecture-setup`** | Initialize or scaffold Clean Architecture projects across various tech stacks. | Folder structure, DI container wiring, Prettier/ESLint, boundary configuration. |
| **`clean-architecture-domain`** | Design and implement pure Domain Layer components. | Entities, Value Objects, Domain Events, Repository Interfaces, Business Invariants. |
| **`clean-architecture-application`** | Implement Application Layer Use Cases and Business Workflows. | Use Cases, Interactors, CQRS Commands/Queries, DTOs, Service Ports, Mappers. |
| **`clean-architecture-infrastructure`** | Implement Infrastructure Layer adapters and external integrations. | Database Repositories (Prisma, TypeORM, GORM, EF Core, etc.), External APIs, Message Brokers. |
| **`clean-architecture-presentation`** | Implement Presentation Layer handlers, controllers, and APIs. | REST Controllers, GraphQL Resolvers, gRPC Services, Request Validation, ViewModels. |
| **`clean-architecture-format`** | Enforce naming conventions, file organization, and architectural linting rules. | File suffixes (`.entity`, `.usecase`, etc.), dependency boundary rules, ESLint / Depcruise configs. |
| **`clean-architecture-validator`** | Audit and validate codebase against Clean Architecture rules. | Detect layer leaks, illegal inward-to-outward imports, bypassed use cases. |

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
    ├── clean-architecture-monorepo/
    │   └── SKILL.md
    ├── clean-architecture-setup/
    │   ├── SKILL.md
    │   └── references/
    │       ├── architecture-overview.md
    │       └── starter-libraries.md
    ├── clean-architecture-domain/
    │   ├── SKILL.md
    │   └── references/
    │       └── domain-patterns.md
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
