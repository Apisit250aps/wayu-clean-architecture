---
name: clean-architecture-validator
description: Audit scoped code or changes for Clean Architecture boundaries, repository ownership, tenant safety, contracts, and verification gaps. Report findings without editing unless requested.
metadata:
  tags: both, fullstack, backend, frontend
---

# Clean Architecture Validator

Audit the requested scope; do not turn a local review into a whole-repository scan. Read repository instructions and trace affected callers, contracts, persistence, wiring, tests, and generated consumers. Review is read-only unless fixes are requested.

## Review process

1. Identify changed behavior, package/table owners, and affected consumers. Use [the architecture matrix](../clean-architecture-foundation/references/architecture-overview.md) when checking import direction.
2. Read only applicable sections of [the checklist](references/validation-checklist.md). It covers contracts/constants, authorization, owner composition, persistence/concurrency, API/client, UI/state, conditions, helpers, and time.
3. Trace violations through actual calls and data access. Repositories must neither depend on another repository nor access its tables through SQL/ORM/helpers/views/audit paths. For those checks, read [repository boundaries](../clean-architecture-persistence/references/repository-boundaries.md).
4. Run appropriate existing type/lint/targeted checks. Search results identify candidates, not proven bugs; inspect the behavior and distinguish baseline failures from introduced ones.

## Non-negotiable checks

- No inward-to-outward leaks, controller-to-repository bypass, browser backend wiring, `any`, TypeScript suppression, or lint-disable shortcuts.
- Command validation uses existing async parsing helpers or `safeParseAsync`; business logic consumes parsed output and preserves typed errors.
- Stored resource scope, permissions, lifecycle, required dependencies, and atomic write conditions enforce the actual workflow.
- Helpers use concrete imports and proper file ownership. RHF/Controller owns editable fields; React Query owns server state. New/changed conditions have source-faithful Thai JSDoc.

## Report

Order actionable findings by severity. For each, give file/line, trigger, observed evidence, user/data impact, and smallest complete remedy. Do not force a fixed finding count or report a grep match as a violation.

State scope, commands/results, unresolved paths, and skipped checks. Separate static/unit evidence from DB rollback/concurrency, HTTP, browser, and performance evidence. No findings in the inspected scope is not certification of the whole codebase. For documentation-only edits, check links/metadata/consistency instead of unrelated runtime suites.
