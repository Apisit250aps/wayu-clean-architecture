# Drizzle schemas and migrations

Inspect the installed Drizzle version, sibling schema/relations, migration history, and connection setup. Reuse their APIs rather than copying a version-specific scaffold. For query/adapter changes, read [ownership and transactions](repository-boundaries.md).

## Schema decisions

- Record each table's business/repository owner and aggregate permission mapping. Reuse owning Domain constants; SQL names/ORM objects stay in persistence.
- Reuse UUIDv7 primary-key and audit timestamp helpers. Keep timestamps, timezone handling, precision, nullability, defaults, and native decoders consistent with the Domain contract.
- Define tenant-aware relationships, uniqueness, checks, and revision/idempotency constraints from actual invariants. A foreign key expresses integrity; it does not permit the referencing repository to read the other owner's records.
- Preserve source facts and indispensable history; derive reproducible values. Define numeric units/precision explicitly rather than assuming all numbers are integers or serializing rows through JSON.
- Add required foreign-key/query indexes and schema exports. Inspect existing composite indexes before adding duplicates; index choices need query evidence.
- Register relations in the existing relation entry point using the installed API. Relation declarations do not authorize cross-owner relational queries.

## Connections and helpers

Keep credentials in the existing environment/config boundary. Fail clearly when required configuration is absent; avoid logging secrets. Reuse the root connection and actual transaction resolver instead of creating another pool in a repository.

Audit timestamps and column defaults are allowed clock reads; business-time queries receive required time inputs. For dates/zones, read [time handling](../../clean-architecture-foundation/references/time-handling.md).

## Reuse the existing base repository

Inspect the base's typed columns/mappers, tenant predicates, transaction resolver, and side effects. Reuse it only for the caller's owned tables. Do not scaffold another generic CRUD base, silently cast rows into entities, or inherit audit writes into another owner's table. Concrete adapters still implement narrow Domain ports; see [adapter patterns](infrastructure-patterns.md).

## Migration delivery

Generate through the repository's established Drizzle scripts. Inspect SQL and snapshot together for destructive changes, defaults/backfills, constraints, indexes, and data compatibility. Applied migrations are immutable; changes use a new migration. Synchronize changed system-catalog seed snapshots without overwriting tenant grants.

Generation/review does not imply applying the migration. Use the authorized target/environment and existing safeguards when application is part of the task. Verify relevant changes against an isolated database; report generated, applied, and verified states separately.
