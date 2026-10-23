# Contract readiness and parallel delivery

Use for plans with multiple implementation tracks or mockups before API readiness.

## Domain contracts before parallel implementation

Plan the smallest coherent contract slice first, owned by a single task. Reuse existing contracts when sufficient. Its readiness criteria are:

- Public types/schemas, constants, entities/value objects, and the exports consumers need are defined and type-check.
- Repository and service ports, use-case inputs/results, typed errors, and relevant actor/tenant context are explicit in the repository's existing contract locations.
- Business rules and lifecycle transitions have agreed inputs, outcomes, and representative accepted/rejected examples. Record relevant transaction, concurrency, pagination, and batch-operation semantics in the ports; concrete SQL and adapters come later.
- Exact source paths and a revision (commit when available, otherwise an identified artifact snapshot) are recorded for consumers. Open decisions affecting this slice are resolved or explicitly block those consumers.

Contract readiness does not require repository implementations, completed rule bodies, use cases, HTTP handlers, or migrations applied to a database. It is a task milestone, not a requirement to commit or publish. Avoid placeholder production implementations that silently return fake success.

Once this milestone is ready, separate the affected tracks:

| Track | Required to start | Independent work and later integration |
| --- | --- | --- |
| Persistence/repositories | Owned Domain ports and approved storage design for the affected slice | Implement schema/migrations and owned-table adapters. A repository task waits for the schema artifacts it actually imports, not all Database work. Verify DB constraints/transactions with a real isolated database before claiming them. |
| Use cases/Application Services | Use-case and collaborator port contracts plus agreed business behavior | Implement orchestration against injected ports and typed test doubles; do not wait for concrete repositories or external adapters. Integrate real collaborators later. |
| Domain rules / pure Domain services | Agreed rule inputs, outputs, errors, and examples | Implement pure rules in Domain. Multi-owner/I/O orchestration belongs to the Application track above, not a duplicate task here. Define any service interface needed by parallel consumers in the contract task; assign each rule implementation once. |
| API spec/client | Domain contracts and agreed transport decisions | Define TypeSpec DTOs and generate the main application's client independently of concrete repositories/use cases. Handlers and runtime composition must later be checked against real implementations. |
| Web mockup | Domain contracts and agreed screen/flow behavior | Build views, forms, and interaction states with typed fixtures; do not wait for API spec, generated client, or a running backend. Schedule API integration separately. |

Keep actual dependencies: if a consumer imports an unfinished rule/service, use the established injection seam and a test double for isolated checks, or declare that implementation as its prerequisite. Do not describe a branch as independently buildable when its imports are missing. Do not invent extra service abstractions just to split work.

## Mockup and integration boundaries

Domain types describe business data and behavior; HTTP DTOs remain owned by the main application's spec/generated client. Do not make Domain import generated HTTP types or treat a Domain entity as a wire response. Mockup fixtures can use safe public Domain types/type imports where package boundaries allow, or a minimal feature-local view model derived from them. Keep backend runtime modules and internal fields out of browser bundles; do not create a second API spec/client for the mockup.

Use existing fixture/mock facilities or component props, with fixture data and simulated states outside production request paths. State which interactions are simulated, including relevant loading, empty, error, validation, permission, and success states. UI checks do not prove server authorization or persistence.

Plan explicit integration tasks with their own prerequisites: real repository/service composition for Application; handlers with use cases and generated HTTP contracts; Web hooks/mappers with the main application's generated client; then relevant end-to-end flow verification against the real backend. When HTTP DTOs differ from mock view data (dates, nullability, pagination, errors), adapt at the existing feature boundary and check the mapping. Remove or isolate mock wiring so production uses real requests. Each delivery area owns its integration task and links collaborators rather than combining areas into one main task.

## Asynchronous task handoff

- Separate **start prerequisites** (exact contracts/artifacts needed to implement and verify in isolation) from **integration prerequisites** (real collaborators needed to verify the connected behavior). Each dependency names its producer task and readiness evidence; task numbering is not an execution barrier.
- Record owned source files/exports and parallel-safe sibling tasks. Assign shared contracts, migrations, catalogs, and composition files one writer or a sequenced handoff; overlapping files are not automatically safe to edit concurrently.
- After a contract change, its owner records the changed shape/semantics and affected consumer tasks. Update those plans, fixtures, and required generation/checks before claiming affected work still integrates; block only consumers of the changed contract.
- Keep isolated implementation completion distinct from integration completion. A mockup or port-based task can finish its own acceptance criteria while linked integration tasks remain open; the feature is complete only when its required integration and verification tasks are complete.
