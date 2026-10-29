# {{TASK_CODE}} — {{English task title}}

## Outcome and scope

{{Concrete outcome and owning delivery area/packages. State design/contract-only versus implementation.}}

## Contracts and dependencies

- Start prerequisites: {{Exact producer tasks, artifact paths/revisions and readiness evidence; or None.}}
- Contract baseline: {{Authoritative design-task links, actual source patterns and unresolved gates.}}
- Integration prerequisites: {{Real collaborators needed for connected behavior; or None.}}
- Integration follow-up: {{Owning integration task, or Included here.}}

## Contract code blocks

{{Write concrete fenced code blocks for the slice this task defines. Link the authoritative producer blocks for consumed contracts; do not duplicate or invent irrelevant contracts. Design tasks inventory entities/table models, scoped repository signatures, use-case inputs/results/errors, Service collaborators and responsibilities, permission actions/scope/default-grant ownership, and API operations with request/response/errors. Tables supplement signatures.}}

```typescript
// {{Actual planned/consumed entity, input/result, port or capability signatures.}}
// {{Use the inspected repository's base/context/error conventions and concrete export paths.}}
```

{{For API tasks add typespec/http/json blocks for each operation or coherent group, with an operation-to-use-case/service/permission map. For other tasks link those owning blocks. Do not present a proposed interface as implemented code.}}

## Permissions and scope

{{Exact actions required by each affected operation; organization/Site/stored-resource scope, current actor/feature checks, restricted fields/files, reviewer rules and deny cases. Link the owning constants/default-grants/seed task. Use Not applicable with a reason only for a task that genuinely introduces/consumes no protected capability.}}

## Ownership and execution mode

- Owns: {{Files/exports; shared contracts, codegen, migrations, catalogs and composition have one writer.}}
- Execution mode: {{sequential (default), or parallel explicitly chosen by the user; record choice/basis.}}
- Selected schedule: {{The task's position in an ordered schedule, or approved parallel wave/start gate.}}
- Potential independent peers: {{Task links and exact readiness/file constraints; capability only when mode is sequential, or None.}}
- Shared-file handoff: {{Single writer and serialization constraints, or None.}}

## Parallel map

{{Small local dependency graph with real producer/current/consumer task codes; include independent peers only where justified. Link the authoritative main-task graph. Even in sequential mode show technical opportunities as potential, not approved concurrent execution. Replace every token/node label.}}

```mermaid
flowchart LR
    P[{{PRODUCER_CODE}}: {{ready artifact}}] --> T[{{TASK_CODE}}: {{deliverable}}]
    T --> C[{{CONSUMER_CODE}}: {{consumer readiness}}]
```

{{If there is no producer or consumer, remove that node/edge. State no parallel peers for a leaf instead of inventing work. Record any real integration gate separately from contract/SDK readiness.}}

## Existing architecture and approach

- {{Concrete inspected source paths and patterns to follow; scoped owner/layer/transaction rules.}}
- {{Domain-change owner and consumers; required Service ports and multi-owner workflow.}}
- {{For Web, actual generated-client symbols/types and SDK producer. No mock fetch/fixture-success fallback unless an explicit separate mockup was requested.}}

## Implementation

- [ ] {{Concrete step.}}
- [ ] {{Concrete step.}}

## Acceptance criteria

- [ ] {{Observable deliverable and permission/boundary guarantees.}}
- [ ] {{Contract/codegen/static or real integration evidence required by this task; exclude later tasks' claims.}}

## Verification

- [ ] {{Repository command or meaningful behavior check; separate permission, DB, HTTP and browser evidence.}}

## Subtasks

{{Omit unless needed. Link grandchildren here only with TASK_CODE-01 codes and task-relative paths.}}

## Progress and handoff

- Status: {{Not started / In progress / Blocked / Complete}}
- Readiness: {{Missing start artifacts or Ready; distinguish contract/SDK/HTTP/integration readiness.}}
- Completed: {{Actual work or None.}}
- Verification evidence: {{Checks actually run; state runtime limits.}}
- Contract changes: {{Changed code blocks/exports/permissions and affected consumer tasks, or None.}}
- Remaining/blockers: {{Next action, unresolved decisions and required user input, or None.}}
