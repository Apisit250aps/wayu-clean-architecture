---
name: clean-architecture-plan
description: Plan detailed Domain, permission and API contracts in Markdown code blocks, generate the client before backend implementation, and map dependencies; sequential by default, parallel only after user choice. Thai summaries and English tasks.
---

# Clean Architecture Task Planning

Planning does not authorize implementation, commits, deployment, or database mutations. Inspect affected source, existing plans and agreed flows/storage design. Record unknown decisions instead of inventing behavior. Read only references for affected work.

## Execution preference

Ask whether the user wants sequential or parallel delivery before selecting a parallel schedule, unless the user already specified the mode for this plan. Recommend **sequential (default)**. While an answer is pending, continue source inspection and contract design; an unanswered question never authorizes parallel work. Record the mode and its basis in the plan. A later change to parallel requires an explicit user choice.

Every main task and child task includes a **parallel map** showing real dependencies, readiness gates, potential independent work and shared-file constraints. A map shows capability, not permission: in sequential mode label parallel lanes as potential only and give one concrete ordered schedule. Neither a map nor selecting parallel delivery authorizes spawning agents, opening chats or executing tasks.

Read [delivery modes and maps](references/parallel-delivery.md) when constructing the schedule, including a sequential plan.

## Design contracts before implementation

Read [contract design](references/contract-design.md) and write concrete Markdown fenced code blocks with language tags. Tables explain responsibilities and traceability; they do not replace contract signatures. Reuse established repository types/paths/patterns rather than impose illustrative code verbatim.

The design must name:

- Entity/table models, persisted source facts, derived read models, input/output schemas and public exports.
- Every repository owner and its scoped methods, inputs/results, batches, transaction/lock and concurrency semantics. A table does not require its own repository.
- Each use case's input/result/errors, authorization and purpose.
- Application Services, their required owner ports and the transaction/workflow each coordinates; pure Domain rules separately.
- Permission actions, organization/Site/resource scope, current identity/feature checks, sensitive-field/file access, explicit default grants and the catalog/seed owner. Map every use case and endpoint to these rules.
- API method/path/operation ID, request/query/response/error contracts and permission, plus its use case/service. Specify dates, decimals, nullability, envelopes, pagination, CAS and idempotency where relevant.

Unresolved product or permission decisions block only dependent contract slices. Assign a design task to close them before generating those contracts; do not invent approval workflows or grants. A design inventory is not implemented code.

## Delivery boundaries and readiness

| Area     | Scope                                                                                 |
| -------- | ------------------------------------------------------------------------------------- |
| Web      | `apps/web` and supporting shared UI                                                   |
| Backend  | Domain contracts, API/spec/client, use cases, Application Services and infrastructure |
| Database | Schema, relations, migrations, integrity and assigned Domain changes                  |

Assign each contract/shared file one writer. Link consumers to the exact producing child task and artifact readiness, not completion of its whole main task. Separate start prerequisites from integration prerequisites.

The preferred delivery order is **Domain + permission + transport contracts → TypeSpec/OpenAPI → generated main-app client → Web using that client**, with concrete Backend implementation scheduled separately. Spec/client generation must not depend on implemented repositories, handlers or a running backend. Web can type-check hooks/forms/views and construct real requests once the SDK is ready; successful data flows require real HTTP. Do not add mock fetch, a second SDK or fake-success production handlers to hide missing Backend. Domain fixtures/mockups are a separate path only when the user requests them.

After contracts are ready, repository adapters, Application orchestration and spec/client may be technically independent. Schedule them concurrently only in the selected parallel mode; otherwise retain those dependencies and select an ordered schedule. Plan explicit real-collaborator integration and database/HTTP/browser verification. Contract-ready, SDK-ready, HTTP-ready and integrated completion are distinct milestones.

## Files and progress

- Use `plans/<CODE>-<ชื่อ main task>/README.md` and `tasks/<CODE>-01-<slug>.md`; preserve existing codes or choose a feature prefix plus sequence.
- Adapt [Thai README](assets/main-task.README.md) and [English task](assets/task.md); replace tokens and omit irrelevant sections.
- README is a concise Thai Trello summary with direct-child checklist links only. Grandchildren use codes such as `CODE-01-01` and are linked/tracked inside their parent task.
- Each task records owned/consumed code-block contracts (or links to their owning design task), source patterns, permissions, file owners, mode, local parallel map, steps and checks. Keep one authoritative contract definition and link consumers to it.
- A task is complete only when its scope/subtasks and required checks are complete. Record actual evidence, remaining integration and contract changes affecting consumers. Never infer successful runtime behavior from generation or static checks.

## Architecture carried into tasks

Repositories access only their owned tables, with no repository dependencies or indirect cross-owner SQL/views/helpers/audit exceptions. Application Services compose required owner ports and preserve one UnitOfWork/lock protocol. Define aggregate ownership so derived reads and filtering before pagination remain possible without crossing owners. Helpers use concrete imports and live outside use-case/class files. Web editable state uses RHF/Controller; React Query owns server state. Follow the consuming repository's structure, error/base contracts, codegen and Thai JSDoc rules; link affected layer guidance instead of duplicating a full checklist.
