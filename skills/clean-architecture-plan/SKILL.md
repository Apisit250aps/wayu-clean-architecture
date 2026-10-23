---
name: clean-architecture-plan
description: Plan Domain contracts first, then parallel implementation and Web mockups with explicit dependencies and integration tasks; Thai summaries and English AI tasks.
---

# Clean Architecture Task Planning

Planning does not authorize implementation, commits, deployment, or database mutations. Inspect affected source, existing plans, and agreed ERD/flows; record unknown decisions instead of inventing behavior. Read only references for affected work.

## Delivery boundaries

Keep separate main tasks for affected areas only:

| Area | Scope |
| --- | --- |
| Web | `apps/web` and supporting shared UI |
| Backend | API/spec/client, use cases, Application Services, infrastructure, Domain contracts |
| Database | Schema, relations, migrations, integrity, and assigned Domain contracts |

Assign each Domain change one owner. Link consumers to the exact child task/artifact they need, not completion of its whole main task. Preserve package ownership and avoid duplicate tasks for overlapping packages.

## Dependencies

1. Reuse or plan a usable Domain contract slice: types, ports, inputs/results, errors, business rules, and exports derived from ERD plus actor/lifecycle flows.
2. Once those inputs are ready, plan independent repository, use-case/Application Service, pure Domain rule, API spec/client, and Web mockup work. For multiple tracks, read [parallel delivery](references/parallel-delivery.md) for readiness, ownership, and integration criteria.
3. Distinguish **start prerequisites** from **integration prerequisites**. Mockups use Domain-informed fixtures; real HTTP integration uses the main application's spec-generated client.
4. Add explicit tasks to connect real collaborators and verify end-to-end behavior. Isolated/mock completion does not complete integration. Task numbering is not an execution barrier.

Route design detail only as needed: Core for contracts/rules/orchestration, Persistence for owned storage/adapters, API for transport/client, Frontend for UI, Foundation for workspace changes, Validator for requested cross-layer review. Asynchronous plans do not automatically spawn agents or add background workers.

## Files and progress

- Use `plans/<CODE>-<ชื่อ main task>/README.md` and `tasks/<CODE>-01-<slug>.md`; preserve existing codes or choose a feature prefix plus sequence.
- Adapt [Thai README](assets/main-task.README.md) and [English task](assets/task.md) templates; replace tokens and omit irrelevant sections.
- README is a concise Trello summary with direct-child checklist links only. Grandchildren use codes such as `CODE-01-01` and are linked/tracked inside their parent task.
- Tasks name concrete source patterns, contracts, file owners, parallel peers, steps, acceptance criteria, and relevant checks. Record contract changes and affected consumers.
- A task is complete only when its scope/subtasks and required checks are complete. Synchronize direct-child status with README; record actual evidence, remaining integration, and blockers so another worker can resume.

## Carry into implementation tasks

Preserve architecture rules: repositories have no repository dependencies; Application Services compose owner ports; helpers use concrete imports and live outside use-case/class files. Web editable state uses RHF/Controller, server state uses React Query, and neither is mirrored with effects. Link the relevant layer rules instead of copying their full checklists into every task.
