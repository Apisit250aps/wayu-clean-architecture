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
# Install from a specific version/tag (e.g. v3.1.0)
npx skills add Apisit250aps/wayu-clean-architecture#v3.1.0

# Install a specific skill from a release version
npx skills add Apisit250aps/wayu-clean-architecture#v3.1.0 --skill clean-architecture-core
```

### Install globally (available in all projects)

```bash
npx skills add Apisit250aps/wayu-clean-architecture -g
```

### Upgrading from v0.5.0

Version 1.0.0 consolidates 12 skills into 7. Update explicit skill invocations and local references using this mapping, then reinstall the selected skills. Review and remove obsolete local copies so agents do not load conflicting instructions.

| Previous skills                                                                        | Replacement                      |
| :------------------------------------------------------------------------------------- | :------------------------------- |
| `clean-architecture-setup`, `clean-architecture-monorepo`, `clean-architecture-format` | `clean-architecture-foundation`  |
| `clean-architecture-domain`, `clean-architecture-application`                          | `clean-architecture-core`        |
| `clean-architecture-database-drizzle`, `clean-architecture-infrastructure`             | `clean-architecture-persistence` |
| `clean-architecture-presentation`, `clean-architecture-typespec`                       | `clean-architecture-api`         |

In v1.0.0, `clean-architecture-feature`, `clean-architecture-frontend`, and `clean-architecture-validator` retained their names. For v2.0.0, also apply the migration below. See [release notes](CHANGELOG.md) for behavioral changes.

---

## Upgrading from v1.0.0

Version 2.0.0 replaces `clean-architecture-feature` with `clean-architecture-plan` for task planning. Implementation uses the affected Core, Persistence, API, and Frontend skills directly; cross-layer delivery review belongs to Validator. Update explicit invocations and remove obsolete installed Feature copies after reinstalling. The collection still has seven skills.

Utils/lib/helpers now require concrete-file imports. Extract standalone helpers from Application/use-case and class files into their owning package; constructors, class methods, and necessary inline callbacks remain allowed. Use RHF/Controller for editable inputs in form/query/mutation-driven Web components, with React Query retaining server state.

## Upgrading from v2.x

Version 3.0.0 keeps all eight skill names but makes repository ownership stricter. A repository accesses only its owned tables and cannot call another repository or reach another owner through SQL/ORM JOINs, read projections, views/functions, helpers, locks, or audit writers. Application Services compose required owner ports and preserve batching, transaction/lock order, and filtering before pagination. Internal child/history tables may stay with their aggregate owner; do not create a repository per table without a separate ownership need.

Read [repository ownership, queries, and transactions](skills/clean-architecture-persistence/references/repository-boundaries.md) before migrating existing code. A query-builder rewrite alone does not remove a hidden dependency, and fewer queries do not prove a speed improvement. Skills provide guidance and audit criteria; installation does not refactor a project, add lint rules automatically, or certify its compliance.

Thai JSDoc now covers every condition written or changed, including guards, branches, shorthand/default expressions, callback/schema predicates, and SQL/ORM conditions. Explain the checked fact, why it matters, and each outcome using [the condition guide](skills/clean-architecture-docs/references/conditions.md). Existing untouched code is audited only within the requested scope.

Install all eight skills from the release in each scope you use:

```bash
# Global Codex skills
npx skills add Apisit250aps/wayu-clean-architecture#v3.1.0 --skill '*' --agent codex --global --yes

# Project Codex skills: run from the project's root
npx skills add Apisit250aps/wayu-clean-architecture#v3.1.0 --skill '*' --agent codex --yes
```

Review local skill customizations before updating; do not delete unrelated skills or legacy entries solely as part of this release.

## Time handling

Version 3.0.1 includes the time-handling guidance omitted from the v3.0.0 publication. Use native `Date` values with direct package imports from `date-fns`/`@date-fns/tz`; no Temporal, shared `lib/time` wrapper, or clock port. A use case reads `now` once and passes required `now`/`asOf`/`timeZone` values and computed cutoffs into Domain logic and owner repositories. Audit stamps and column defaults retain their documented exception.

Web/UI display formatting uses central presets; calendar math and SQL conversions preserve explicit zone semantics. Read [time handling](skills/clean-architecture-foundation/references/time-handling.md) for conversion, DST, lint, and verification requirements. This patch completes the intended guidance bundle; existing projects still need an explicit implementation migration.

## 🛠️ Available Skills

| Skill Name                           | Scope / Tag           | Description                                                                                        | Key Focus                                                                                             |
| :----------------------------------- | :-------------------- | :------------------------------------------------------------------------------------------------- | :---------------------------------------------------------------------------------------------------- |
| **`clean-architecture-plan`**        | `🏷️ Planning`         | Plan Domain contracts first, then asynchronous implementation.                                     | Thai summaries, English tasks, parallel tracks, contract ownership, and integration gates.           |
| **`clean-architecture-docs`**        | `🏷️ Documentation`    | Write Thai JSDoc or create feature and flow docs for Mobile or Web teams.                          | Source-backed declaration/condition JSDoc, interactive handoff intake, and API diagrams.              |
| **`clean-architecture-foundation`**  | `🏷️ Both (Fullstack)` | Set up a workspace or package and its shared conventions.                                          | Turborepo setup, package presets, Prettier, and dependency boundaries.                                |
| **`clean-architecture-core`**        | `🏷️ Backend`          | Design modular Domain and Application workflows for configurable tenant systems.                   | Module constants/catalogs, scoped ports, shared validation/policies, unit of work, and concurrency.   |
| **`clean-architecture-persistence`** | `🏷️ Backend`          | Implement concrete storage and repository adapters.                                                | Owner-scoped Drizzle repositories, batch queries, pagination, transactions/locks, and infrastructure. |
| **`clean-architecture-api`**         | `🏷️ Both (Fullstack)` | Deliver HTTP contracts and handlers.                                                               | TypeSpec, OpenAPI, generated client SDKs, controller validation, and error mapping.                   |
| **`clean-architecture-frontend`**    | `🏷️ Frontend`         | Build feature-oriented Next.js UI with reusable `@repo/ui` components and generated API contracts. | React Hook Form Controllers, React Query hooks, React Aria, shadcn, and TypeSpec client boundaries.   |
| **`clean-architecture-validator`**   | `🏷️ Both (Fullstack)` | 🛡️ **AI Auditor**: Audit codebase for Clean Architecture violations.                               | Detect layer/ownership leaks, undocumented conditions, unsafe types, and workflow/validation gaps.    |

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
>
> - **Domain** depends on **nothing** (no frameworks, no ORMs).
> - **Application** depends only on **Domain**.
> - **Infrastructure** & **Presentation** depend on **Application** and **Domain**.

---

## 📂 Repository Structure

```text
wayu-clean-architecture/
├── README.md
└── skills/
    ├── clean-architecture-docs/
    │   ├── SKILL.md
    │   ├── agents/openai.yaml
    │   ├── assets/handoff.md
    │   └── references/
    │       ├── jsdoc.md
    │       ├── conditions.md
    │       └── handoff-workflow.md
    ├── clean-architecture-plan/
    │   ├── SKILL.md
    │   ├── agents/openai.yaml
    │   ├── references/parallel-delivery.md
    │   └── assets/
    │       ├── main-task.README.md
    │       └── task.md
    ├── clean-architecture-foundation/
    │   ├── SKILL.md
    │   ├── agents/openai.yaml
    │   └── references/
    │       ├── end-to-end-example.md
    │       ├── architecture-overview.md
    │       ├── naming-and-style.md
    │       ├── package-presets.md
    │       ├── starter-libraries.md
    │       └── time-handling.md
    ├── clean-architecture-core/
    │   ├── SKILL.md
    │   ├── agents/openai.yaml
    │   └── references/
    │       ├── domain-patterns.md
    │       ├── usecase-patterns.md
    │       ├── tenant-policy-design.md
    │       └── source-analysis.md
    ├── clean-architecture-persistence/
    │   ├── SKILL.md
    │   ├── agents/openai.yaml
    │   └── references/
    │       ├── drizzle-patterns.md
    │       ├── infrastructure-patterns.md
    │       └── repository-boundaries.md
    ├── clean-architecture-api/
    │   ├── SKILL.md
    │   ├── agents/openai.yaml
    │   └── references/
    │       ├── presentation-patterns.md
    │       └── typespec-patterns.md
    ├── clean-architecture-frontend/
    │   ├── SKILL.md
    │   ├── agents/openai.yaml
    │   └── references/
    │       └── frontend-patterns.md
    └── clean-architecture-validator/
        ├── SKILL.md
        ├── agents/openai.yaml
        └── references/
            └── validation-checklist.md
```

---

## Task planning

Use `$clean-architecture-plan` to create `plans/<task-code>-<ชื่อ main task>/README.md` with a short Thai Trello summary and linked direct-child checklist. English AI instructions live in `tasks/`; deeper subtasks are linked only from their parent task. Web, Backend (API/client/infra/domains/application), and Database (domains/database) have separate main tasks, with explicit ownership for shared domain changes. Templates are included in the skill assets.

Start from the agreed ERD and business flows, then define a usable Domain contract slice: types, ports, use-case inputs/results, errors, and business rules. Once those contracts are ready, repositories, use cases/Application Services, business-rule implementations, API spec/client work, and Web mockups can proceed in parallel according to their actual inputs. Every task distinguishes start prerequisites from integration prerequisites and records file ownership plus a contract baseline. A child contract task can unblock consumers before its main task is complete.

Web mockups use Domain-informed typed fixtures or view models without waiting for HTTP contracts. Real API integration still uses the main application's spec-generated client types. Separate integration tasks connect real collaborators and verify behavior; a completed mockup or isolated use-case test does not mean the integrated feature is complete.

Across implementation skills, utils/lib/helpers use concrete-file imports and standalone helpers live outside use-case/class files. Web editable form/input state uses RHF/Controller; React Query owns server state.

## 🚀 How AI Agents Use These Skills

Each skill includes `SKILL.md` for its working instructions and `agents/openai.yaml` for Codex UI metadata (`display_name`, `short_description`, and `default_prompt`). Supporting references and assets remain specific to each skill.

Load the relevant skill entrypoint, then only reference sections needed for the current task. Links are conditional reading routes, not instructions to load the entire collection. Entry points retain essential boundaries; detailed ownership/transaction rules, condition JSDoc, handoff requirements, and parallel planning each have a focused reference. Existing repository code and installed tooling determine implementation details; examples are illustrative, not drop-in libraries.

The skills share some relative references. Install the collection together when using those shared rules; a copied standalone folder may have missing links. If a required reference is unavailable, report that gap rather than silently inventing its rules. Shorter entrypoints reduce text loaded initially; actual token use still depends on selected references and repository inspection.

Use `$clean-architecture-docs` for feature handoff documentation. It asks interactively for Mobile, Web, or both; document language; and feature/flow scope before drafting. Diagrams use English; headings and explanatory prose use the selected language. Each flow separates its flowchart, step/decision explanation, sequence diagram, and API ordering explanation into readable sections. API examples show request bodies, HTTP statuses, responses, and next client actions for each source-supported integration case. Existing docs conventions take precedence; fallback paths are `docs/features/` and `docs/flow/mobile/` or `docs/flow/web/`.

For code documentation, the same skill uses [the Thai JSDoc guide](skills/clean-architecture-docs/references/jsdoc.md) to explain responsibilities, inputs, outputs, business rules, and errors from actual source. Its [condition rules](skills/clean-architecture-docs/references/conditions.md) cover every condition written or changed, not only method declarations or `if` statements. JSDoc requests do not require platform selection or handoff diagrams.

Example: `ใช้ $clean-architecture-docs เพิ่ม JSDoc ภาษาไทยให้ UseCase และ Repository ของ feature ผู้ใช้ โดยอธิบายเงื่อนไข ผลลัพธ์ และข้อผิดพลาดตามโค้ดจริง`

Example: `ใช้ $clean-architecture-docs สร้างเอกสารส่งต่อ feature การลา แล้วถาม platform และภาษาก่อน`

1. **Progressive Loading**: AI agents initially read only the frontmatter `name` and `description`.
2. **Context Activation**: When you ask your agent to _"Create a new Use Case for user registration"_ or _"Review my repository for layer leaks"_, the agent automatically loads the corresponding `SKILL.md` and referenced guidelines.
3. **Execution**: The agent strictly follows the design patterns, code templates, and constraints defined in each skill.

---

## 📄 License

MIT License. Created by [Apisit250aps](https://github.com/Apisit250aps).
