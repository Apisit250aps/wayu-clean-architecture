# Contract design in Markdown

Use in design tasks before implementation scheduling. Inspect the consuming repository's entity/schema/base-port/error/TypeSpec/client conventions first. The fragments below illustrate the detail required, not a new universal package layout or production implementation. Adapt names and reuse existing types. Prose and tables explain purpose; **fenced code blocks specify the actual planned contract**. Use `typescript`, `typespec`, `http`, `json`, `yaml` or `mermaid` as appropriate.

## Inventory and ownership

For every affected table, identify its entity/table model, persisted facts, owner repository and internal children. Separate derived read DTOs from stored entities. Name concrete target paths/exports and a producer task; consumers link to that definition rather than fork it. New request/approval requirements may require revising an earlier ERD: plan that change explicitly and never claim tables already exist.

Every repository contract lists scoped method signatures, inputs/results/nulls, batches, pagination, locks, idempotency and CAS/transaction preconditions. Internal child/event tables can share an aggregate owner. Choose ownership so required derivations can be computed without another owner's SQL; Application Services batch-enrich across owners and cannot filter an already paginated page incorrectly.

An illustrative schema-derived table model:

```typescript
// Proposed Domain contract; fields reflect inspected source/design.
export const itemSchema = z.object({
  id: z.uuid(),
  organizationId: z.uuid(),
  name: z.string().trim().min(1),
  revision: z.number().int().positive(), // concurrency token, not workflow status
});
export type ItemRecord = z.infer<typeof itemSchema>;
export type RenameItemInput = {
  id: string;
  expectedRevision: number;
  data: { name: string };
};
```

Use the project's entity class/type convention, not an invented ORM model. Reference the existing Zod import/version. For real contracts include all necessary source fields and distinguish server-written identity/audit fields from client input. New/changed declarations and conditions receive the consuming repository's Thai JSDoc requirements.

## Repository, use-case and service contracts

Reuse existing BaseRepository/Repository and scoped-props conventions; narrow illegal generic CRUD on append-only owners. Do not copy this example instead of inspecting those bases.

```typescript
export type ItemScope = { organizationId: string };
export interface IItemRepository {
  findById(props: ItemScope & { id: string }): Promise<ItemRecord | null>;
  rename(props: ItemScope & RenameItemInput): Promise<ItemRecord>;
  // rename uses an atomic revision predicate; stale revision is a typed conflict.
  // No Member, Permission, Audit or another owner's tables are accessed here.
}

// Use the repository's existing BaseUseCase and trusted security context.
export type IRenameItemUseCase = BaseUseCase<
  SecurityContext & ItemScope & { data: RenameItemInput },
  ItemRecord
>;
export interface IItemService {
  rename(
    context: SecurityContext & ItemScope,
    input: RenameItemInput,
  ): Promise<ItemRecord>;
}
export type ItemServiceDependencies = {
  items: IItemRepository;
  access: IItemAccessService;
  audit: IAuditRepository;
  unitOfWork: IUnitOfWork;
};
```

Existing base/context/audit/UoW types above are illustrative imported contracts, not declarations to recreate. Show actual required constructor collaborators or a narrow interface when parallel consumers need it; do not add redundant dependency bags/services for every method. The implementation task must state the service sequence: parse input → current identity/scope/permission check → UnitOfWork → owner lock/CAS → mutation → Audit owner's append → commit. Verify the real project's transaction/lock order instead of applying this illustrative order blindly. Audit and mutation roll back together. Repository-to-repository orchestration is forbidden.

For each use case specify: purpose, typed input/result, permission/feature checks, applicable transitions, typed failure codes and required Service method. Pure Domain rule signatures specify facts in/out without repositories; service signatures specify I/O coordination. Never invent successful method bodies to unblock codegen.

## Permission contracts are required

Design permissions with the contracts, not after handlers/UI are built. Name resource/action constants and explicitly map existing or new catalog entries. Include organization/Site/stored-resource scope, current identity/assignment/feature checks, sensitive contacts/evidence/file reads, and any no-self-review or assigned-reviewer rule. Reuse existing shared access capabilities; role names are not authorization.

```typescript
// Proposed names: confirm against the project's actual action catalog.
export const ITEM_ACTIONS = {
  READ: "item:read",
  UPDATE: "item:update",
} as const;

export interface IItemAccessService {
  require(
    context: SecurityContext & ItemScope,
    action: (typeof ITEM_ACTIONS)[keyof typeof ITEM_ACTIONS],
  ): Promise<void>;
}
```

Pair the code block with a traceability matrix: endpoint → use case → required action → scope/field restrictions → Access Service. Explicit default role grants and feature scope are business decisions: inspect existing defaults, ask when missing, and do not grant all new actions to everyone. Identify the owner task for constants/exports, versioned catalog/seed migration and tenant-custom-grant preservation. Permission checks apply to stored ownership, not just IDs supplied by the client. Plan accepted/denied examples (wrong tenant/Site, inactive member, revoked permission, restricted fields, invalid reviewer) and resulting typed errors.

## API contracts and generated-client handoff

For **every** planned endpoint write method/path/operationId, input/query/path fields, response/error/envelope shapes, pagination/order, authorization, owning use case/service and generation owner. Request fields cannot override trusted tenant/actor/permissions. Fix nullability, decimal precision/string encoding, date transformations, revision/idempotency, batch limits and retry semantics before SDK readiness.

```typespec
namespace ProjectName;
model Item is Domain.Entity.ItemRecord;
model RenameItemRequest {
  name: Item.name;
  expectedRevision: int32;
}
@route("/organizations/{organizationId}/items")
interface ItemServices {
  @patch @route("/{itemId}")
  renameItem(
    @path organizationId: string,
    @path itemId: string,
    @body body: RenameItemRequest,
  ): ApiOkResponse<Item> | ApiUnauthorizedResponse | ApiForbiddenResponse
     | ApiBadRequestResponse | ApiNotFoundResponse | ApiConflictResponse;
}
```

Use the consuming spec's real namespace, imports, response models and DTO derivation utilities. Do not send `id` twice in body and path. State controller mapping: path itemId → Domain input id, body name → data.name, expectedRevision → CAS, authenticated context → trusted identity. Response helpers and error mappings follow the real repository rather than the example.

```http
PATCH /api/organizations/{organizationId}/items/{itemId}
Content-Type: application/json

{"name":"Radio","expectedRevision":2}
```

```json
{
  "success": true,
  "message": "Updated",
  "data": {
    "id": "01900000-0000-7000-8000-000000000001",
    "organizationId": "01900000-0000-7000-8000-000000000002",
    "name": "Radio",
    "revision": 3
  }
}
```

Examples are proposed response contracts, not exercised HTTP. Enumerate invalid input, unauthenticated, forbidden, scoped missing and stale-revision responses using existing typed errors. A table can map each operation to its contract block/service/permission; do not replace all endpoints with one vague “CRUD” row.

Plan Domain codegen → TypeSpec/OpenAPI → main-app generated SDK independently of concrete Backend adapters/handlers. Record exact exports/generation commands from the repository. Web consumes that SDK immediately with real request hooks; no mock fetch is needed to write the code. Backend absence still blocks successful runtime data tests. Contract-ready, SDK-ready, HTTP-ready and browser-integrated are distinct evidence gates.
