---
name: clean-architecture-plan
description: Create or update task plans using Thai main-task summaries and English AI task files in coded plans folders, separating Web, Backend, and Database delivery.
---

# Clean Architecture Task Planning

Use for planning work, breaking a feature into tasks, or maintaining an existing task plan. Planning does not authorize implementation, commits, deployments, or database mutations.

## Inspect before planning

Read the repository instructions and inspect the affected source, package boundaries, existing architecture, and sibling feature patterns. Base the design and implementation approach on those patterns. Record concrete source paths in task files; label unknowns instead of inventing architecture. Load the relevant installed architecture skill when its layer needs design detail.

## Main-task boundaries

Give each main task a unique task code and a concise Thai name. Preserve existing codes; if none exist, choose a feature prefix plus sequential numbers, such as `ATT01`. Use `plans/<task-code>-<main-task-name>/`, for example `plans/ATT01-หน้าแสดงผลการเข้างาน/`.

Never combine these delivery areas into one main task:

| Area | Planning scope |
| --- | --- |
| Frontend | Web (`apps/web`); shared UI changes supporting Web follow repository ownership. |
| Backend | API, generated client/contracts, infrastructure, domains, and application use cases where applicable. |
| Database | Domains and database schema, relations, migrations, and data integrity. |

`domains` overlaps Backend and Database and must be considered explicitly. Assign each domain change to one owning main task, explain its responsibility, and link dependent main tasks to it. Keep domain business contracts separate from database mechanics; overlapping packages do not permit duplicate implementation tasks. A Web task consumes the generated client; client generation belongs to the Backend task. Express cross-area dependencies with relative links rather than merging main tasks. Create only areas affected by the request.

## Route dependencies by affected layer

Plan business contracts and workflows with `clean-architecture-core`, concrete storage/adapters with `clean-architecture-persistence`, HTTP contracts and generated clients with `clean-architecture-api`, and Web/UI with `clean-architecture-frontend`. Use `clean-architecture-foundation` when workspace/package setup changes and `clean-architecture-validator` for final audits. Use installed skills when available; inspect existing source patterns when they are not installed.

Order dependencies inward to outward: domain contracts before dependent persistence/API work, generated client contracts before consuming Web work. Do not create tasks for unaffected layers. Keep this as a plan; implementation remains a separate user-authorized action.

## Output templates

Copy and adapt [the Thai README template](assets/main-task.README.md) and [the English task template](assets/task.md). Replace template tokens in generated plans and omit sections that do not apply.

```text
plans/ATT01-หน้าแสดงผลการเข้างาน/
├── README.md
└── tasks/
    ├── ATT01-01-display-attendance.md
    └── ATT01-02-filter-attendance.md
```

- `README.md` is a short Thai summary for the user to read and copy into Trello. Describe the main outcome, scope, dependencies, and completion criteria briefly.
- Its checklist contains only direct child task codes/titles and relative links to `tasks/`; do not put implementation details there.
- Task files are English instructions for AI. Give each a stable code such as `ATT01-01`, a small dependency-complete scope, the existing pattern/source references, implementation steps, acceptance criteria, and relevant verification.
- If a child task needs further subtasks, define and link them from that child's file only. Store extra files under `tasks/` with codes such as `ATT01-01-01`. Do not add grandchildren or their details to the main README.
- Order tasks by dependencies. Keep each task small enough to execute and verify independently once its prerequisites are complete.

## Maintaining progress

Keep direct-child checklist status in the README aligned with completion of that child. A child with subtasks is complete only when its required work and verification are complete. Track grandchild progress inside its parent file; update the main README only when the direct child's status changes.

Record completed work, actual verification, remaining work, and blockers in the English task file so another AI can resume. Distinguish planned checks, static checks, and exercised runtime behavior. Do not mark unverified acceptance criteria complete.

## Implementation constraints to carry into tasks

- Follow existing architecture and package ownership; search for reusable helpers first.
- In every layer, import utils/lib/helpers from the concrete file or explicit package subpath, never a barrel or a package root that re-exports them.
- Keep standalone helper functions out of Application/use-case files and files defining classes. Put them in the owning package's utils/helper/lib files; class methods remain in their classes.
- For Web, avoid `useEffect` for derived/form/server state. Use React Hook Form and `Controller` for editable form/input state in forms and query/mutation-driven components; React Query owns server data and request status. Do not copy query data or pending/error state into form state.
