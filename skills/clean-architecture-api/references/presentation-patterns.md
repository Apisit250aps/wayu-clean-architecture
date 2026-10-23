# HTTP presentation

Inspect the actual server entry and framework; paths such as `apps/api` are examples. Reuse current controllers, request validation, security middleware, response utilities, and composition. Do not introduce a new base-controller framework for one handler.

## Handler flow

1. Resolve authenticated actor/security context through trusted middleware.
2. Parse the declared path/query/body input with existing validators; preserve async refinements/transforms. Treat JSON, multipart, bodyless requests, and empty responses according to the actual contract.
3. Invoke the use case with parsed business input and separately trusted context. Never spread request data over actor, permission, admin, or tenant fields.
4. Map the typed result/error into the spec's status/envelope. Use cases return business results, not HTTP `Request`/`Response` objects.

Controllers never access repositories/DB. Obtain use cases from the isolated composition root. Group routes/controllers by module; split only when responsibility requires it. A Web server boundary does not make server composition safe to import into client modules.

## Mapping and errors

- Reuse pagination parsing/defaults and validate bounds; do not force every query into page/limit or add undeclared take/skip fields.
- Preserve optional/null fields, dates, uploads, and revision/idempotency inputs. Transport validation complements use-case validation and resource authorization.
- Translate known typed errors centrally; preserve their intended status/code without exposing unknown internal messages, SQL details, credentials, or stack traces.
- Keep standalone transport helpers outside controller class files and import concrete paths.

## Verify

Trace mounted method/path → middleware → handler → use case → response mapping. Compare against generated contracts and representative success/failure cases. Static inspection does not prove middleware mounting, encoding, or runtime status mapping; exercise those paths when required by the change.
