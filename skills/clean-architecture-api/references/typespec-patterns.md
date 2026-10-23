# TypeSpec and generated clients

Use the main application's existing spec → OpenAPI → TypeScript client pipeline. Inspect its installed compiler/plugins, configuration, scripts, entity generator, and public exports; do not introduce a second pipeline or paste unrelated version pins.

## Model ownership

- Domain describes business values and ports. Transport DTOs belong in spec models and expose only intended client-visible/writable fields.
- Reuse existing `Domain.Entity.*` generation and define named aliases in `spec/models/`; services reference those aliases rather than repeating entity field lists.
- Derive create/update DTOs with the existing transforms (for example `OmitProperties`/`OptionalProperties`) only after excluding server-owned tenant, actor, audit, and revision fields as required by the operation. Entity shape alone does not define a safe command.
- Preserve required/optional/null distinctions, unions/enums, numeric units, and date serialization. Domain Date values and generated wire values may differ.

Illustrative model derivation, only if these are the real fields and policies:

```typespec
model Product is Domain.Entity.Product;
model CreateProduct is OmitProperties<Product, "id" | "createdAt" | "updatedAt">;
model UpdateProduct is OptionalProperties<CreateProduct>;
```

## Operations and responses

Match existing namespaces, route/tag conventions, authentication metadata, parameter locations, and response models. Define exact methods/paths, statuses, envelopes, supported errors, pagination, and file encoding. Reuse common responses; do not invent an envelope or JSON body for a bodyless/multipart operation.

Contract generation can proceed from agreed Domain and transport decisions without a running backend. Real handlers must later be checked against that contract. Mockup types do not replace these HTTP types.

## Generation and exports

1. Run the existing Domain/entity generator if its inputs changed.
2. Compile TypeSpec into the configured OpenAPI output.
3. Generate the TypeScript SDK/query artifacts with configured plugins.
4. Inspect changes and type-check affected handlers/client/Web consumers; never hand-edit generated files.

Preserve public exports and generator discovery when moving models. Choose date transformation, transport client, and React Query plugins according to the existing pipeline; do not assume installed versions support an example configuration.

## Web consumption

Configure the SDK at the Web composition root. Feature hooks consume generated services/types, pass cancellation signals where supported, and own scoped query keys, error mapping, and invalidation. Components invoke those hooks. Adapt DTOs to mock/view models at the existing feature boundary, checking dates, nulls, errors, and pagination.

See [frontend data flow](../../clean-architecture-frontend/references/frontend-patterns.md#generated-client-and-react-query) only when changing the consumer. Generation/type-check success is separate from actual HTTP/browser verification.
