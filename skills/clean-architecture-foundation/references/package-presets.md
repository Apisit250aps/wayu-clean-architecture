# Package setup

Copy the nearest compatible package's configuration and change only its ownership-specific fields. Match the workspace package manager, module/output strategy, shared TypeScript/ESLint configs, and lockfile versions; do not paste version pins from an example.

## Shared setup

1. Set the package name/scope and required dependencies. Add only libraries used by the package; shared tooling stays in the existing dev/config packages.
2. Extend the matching base or React TypeScript config. Preserve strictness and the workspace's source/build resolution conditions.
3. Expose deliberate public paths with `exports`; use `imports` only for package-local aliases. Keep utils/lib/helpers available through concrete subpaths, not barrels.
4. Follow existing build/dev/check-types/lint scripts. Add generators only when this package owns an actual generation step.
5. Extend existing boundary rules using [the package matrix](architecture-overview.md#package-matrix). Test a prohibited import and a permitted one; remove probes afterward.

## Package-specific choices

| Package | Public surface and setup |
| --- | --- |
| `domains` | Constants, schemas, entities, repository/service ports, use-case contracts, and pure helpers. Preserve existing contract folders and entity-generator discovery. Zod/uuid/date-fns only where needed; no blanket CRUD base for every aggregate. |
| `database` | Schema/relations, connection/transaction mechanics, migrations, and owned repositories if that is the established placement. Domain dependency is allowed; expose only required entry points. |
| `applications` | Use cases, Application Services, and concrete helper/error subpaths. Internal dependency is Domain; no ORM/HTTP types. |
| `infrastructures` | Adapters and external SDKs. Isolate composition files if they wire Application implementations; do not permit those imports in every adapter. |
| `client` | Spec, OpenAPI and generated SDK output; use [API generation guidance](../../clean-architecture-api/references/typespec-patterns.md). |
| `ui` | Styles, components, generic hooks/fields, concrete utilities. Match the existing React peer/dependency convention and React TS preset; no business dependencies. |

## Exports

Example mapping for concrete helper files, adapted to the workspace's source/build convention:

```json
{
  "exports": {
    "./lib/*": "./src/lib/*.ts"
  },
  "imports": {
    "#lib/*": "./src/lib/*.ts"
  }
}
```

Export-map patterns are path substitutions, not file-discovery globs. Verify representative nested imports with the actual compiler/runtime resolution. Preserve existing public paths when moving files and update generators, consumers, tests, and docs together.

## Checks

Run package type/lint/build checks that apply, verify public imports from a consumer, and regenerate affected artifacts. A manifest alone does not prove the package can be consumed. Do not add unrelated packages or a new build pipeline to complete one package change.
