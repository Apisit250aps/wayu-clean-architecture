# Changelog

## v3.0.1

Complete the v3.0.0 guidance bundle by publishing the pending time-handling changes that were omitted from that release. Repository ownership and condition JSDoc rules remain in effect.

- Include the shared time reference and route Foundation, Core, Persistence, Frontend, and Validator to it.
- Use native `Date`, direct `date-fns`/`@date-fns/tz` imports, and explicit zone-free date/time strings; remove shared date wrappers, Temporal, and clock ports from the prescribed architecture.
- Sample `now` once per use-case execution and pass required time inputs/computed cutoffs into Domain calculations and repositories. Preserve audit/default timestamp exceptions and document synchronized-host-clock requirements.
- Require parameterized SQL time zones, central Web/UI display presets, second-host-zone tests, and non-default-zone SQL verification.
- Align Validator's allowed pure Domain dependencies with date-fns, clarify that construction from an explicit Date input is not a clock read, and avoid one-hour assumptions for DST transitions.
- Preserve existing working trees when comparing tests with a baseline.

### Validation

- All eight skills passed skill-creator validation; YAML metadata, concrete local Markdown links/anchors, code fences, formatting, and Git whitespace checks passed.
- Documentation/skill changes only; application runtime tests and interactive end-to-end skill execution were not run.

### Install

```sh
npx skills add Apisit250aps/wayu-clean-architecture#v3.0.1 --skill '*' --agent codex --yes
npx skills add Apisit250aps/wayu-clean-architecture#v3.0.1 --skill '*' --agent codex --global --yes
```

## v3.0.0

Breaking architecture guidance: enforce repository ownership through both direct and indirect data access. All eight skill names remain unchanged.

- Assign explicit table owners; aggregate-owned child/history tables do not require separate repositories by default.
- Prohibit repository-to-repository calls and cross-owner SQL/ORM queries, read projections, views/functions, helper/mapper paths, locks, and audit writes. Trace database-side behavior without weakening integrity constraints.
- Move multi-owner reads, locks, mutations, and audit orchestration to Application Services using narrow required ports and a shared UnitOfWork; reject redundant dependency bags and fallback adapters.
- Add scoped batch-query, duplicate/empty-input, atomic replacement, pagination/empty-total, decoder/nullability, ambient transaction identity, and ordered-lock guidance.
- Preserve source facts and historical inputs; distinguish query counts, timings/plans, static checks, and real rollback/concurrency evidence.
- Require Thai JSDoc for every condition written or changed: if/else, guards, switch/case/default, ternary/rendering, logical/nullish/default/optional expressions, loop/callback predicates, validation/assertions, error/result branches, and SQL/ORM predicates. Explain facts, reasons, outcomes, and actual contracts without changing logic just to comment it.
- Route the rules through Foundation, Core, Persistence, API, Frontend, Docs, and Validator; expand ownership and condition audit checklists.

### Migration

Reinstall the selected skills and migrate existing cross-owner workflows explicitly. Installing the release does not refactor applications or install automated enforcement. Cross-owner read models and audit helpers are not compatibility exceptions. Preserve public response shapes, filtering before pagination, tenant guards, audit rollback, and lock ordering during migration.

### Validation

- All eight skills passed skill-creator validation.
- YAML metadata, concrete local Markdown links/anchors, code fences, formatting, and Git whitespace checks passed.
- Skill/documentation changes only; application runtime tests and interactive end-to-end skill execution were not run.

### Install

```sh
npx skills add Apisit250aps/wayu-clean-architecture#v3.0.0 --skill '*' --agent codex --yes
npx skills add Apisit250aps/wayu-clean-architecture#v3.0.0 --skill '*' --agent codex --global --yes
```

## v2.3.0

Extend `clean-architecture-docs` with Thai JSDoc guidance alongside existing feature and flow handoffs.

- Add a Thai JSDoc reference covering responsibilities, inputs, outputs, business rules, errors, and examples for classes, use cases, repositories, functions, types, and constants.
- Route code documentation requests directly to the JSDoc workflow without Mobile/Web intake or handoff diagrams.
- Require comments to match actual source and callers, including nullable results, side effects, tenant scope, and transaction guarantees when relevant.
- Update skill discovery metadata and README examples while preserving the handoff workflow.

### Validation

- All eight skills passed skill-creator validation.
- YAML metadata, local Markdown links, code fences, and Git whitespace checks passed.
- Documentation/skill changes only; application runtime tests and interactive end-to-end skill execution were not run.

### Install

```sh
npx skills add Apisit250aps/wayu-clean-architecture#v2.3.0
```

## v2.2.0

Improve `clean-architecture-docs` handoffs with clearer diagrams and case-specific API examples.

- Keep diagram labels, participants, messages, notes, and branch conditions in English while headings and explanatory prose follow the selected language.
- Separate flowcharts, flow explanations, sequence diagrams, and API ordering explanations into readable sections.
- Require request bodies, HTTP statuses, response examples, and next client actions for each source-supported integration case.
- Handle shared requests, bodyless requests, multipart uploads, empty responses, and unknown contract shapes explicitly.
- Align the handoff template, delivery checks, and README with these requirements.

### Validation

- All eight skills passed skill-creator validation.
- YAML metadata and Git whitespace checks passed.
- Skill/documentation changes only; interactive end-to-end execution was not performed.

### Install

```sh
npx skills add Apisit250aps/wayu-clean-architecture#v2.2.0
```

## v2.1.0

The collection now contains eight skills. Existing skill names and working instructions remain compatible.

- Add `clean-architecture-docs` for source-backed feature and flow handoff documentation for Mobile and Web teams.
- Ask interactively for platform, document language, and feature/flow scope before drafting.
- Include decision flowcharts, API sequence diagrams, ordered calls with value dependencies, contract examples, and supported recovery paths in each documented flow.
- Add a reusable handoff Markdown template and distinguish source inspection, proposed behavior, and runtime verification.
- Add consistent `agents/openai.yaml` UI metadata to all eight skills, including display names, short descriptions, and skill-specific default prompts.
- Update the skill catalog and repository structure in README.

### Validation

- All eight skills passed skill-creator validation and YAML metadata checks.
- Git whitespace checks passed.
- Skill/documentation changes only; application runtime tests and interactive end-to-end skill execution were not run.

### Install

```sh
npx skills add Apisit250aps/wayu-clean-architecture#v2.1.0
```

## v2.0.0

Breaking release: remove `clean-architecture-feature`. Use `clean-architecture-plan` for task planning, affected layer skills for implementation, and `clean-architecture-validator` for cross-layer delivery review. Reinstall and remove obsolete Feature skill copies; update explicit invocations. The collection contains seven skills.

- Move dependency routing into Plan and cross-layer delivery checks into Validator.
- Preserve the illustrative end-to-end walkthrough under Foundation; remove the redundant Feature generation guide.
- Centralize detailed helper conventions in Foundation with concise layer reminders and links.
- Add `clean-architecture-plan` with Thai main-task and English AI-task templates, coded folders, parent-only nested checklists, and separate Web/Backend/Database task ownership.
- Require concrete-file utils/lib/helper imports across layers and separate standalone helpers from Application/use-case and class files.
- Clarify RHF/Controller editable input ownership in form/query/mutation components while keeping server state in React Query.
- Align skill routing, audit checks, and starter examples with these rules.

### Validation

- All seven skills passed skill-creator validation.
- Local Markdown links and Git whitespace checks passed.
- Documentation/skill changes only; application runtime tests were not run.

## v1.0.0

This release consolidates the skill collection and updates its Core and Frontend guidance from an evolved TypeScript monorepo. The major version reflects breaking skill names and architecture guidance; it does not certify the runtime behavior of projects using the skills.

### Breaking changes and migration

The collection now contains seven skills:

| Previous skills                   | Replacement                    |
| --------------------------------- | ------------------------------ |
| setup + monorepo + format         | clean-architecture-foundation  |
| domain + application              | clean-architecture-core        |
| database-drizzle + infrastructure | clean-architecture-persistence |
| presentation + typespec           | clean-architecture-api         |

The previous names all had the `clean-architecture-` prefix. Update explicit invocations, installation selections, and local references to the replacement names. Review and remove obsolete installed copies after installing the replacements. Feature, Frontend, and Validator retain their existing names.

### Core

- Design around business modules and cohesive workflows, with tenant-scoped ports and typed policy configuration.
- Require owning constants and aggregate permission mapping for each new module/table, with coordinated feature/action catalogs and explicit default grants.
- Reuse validation, permission, existence, uniqueness, concurrency, and module-local helpers.
- Distinguish trusted tenant context, persisted ownership, tenant configuration, and global catalogs.
- Clarify unit-of-work propagation, atomic revision updates, rollback, and database uniqueness requirements.
- Replace older generic CRUD templates with focused design references and source analysis.

### Frontend

- Cover apps/web, packages/ui, and the generated packages/client contract.
- Search shared components before creating new UI; allow domain-neutral RHF fields, tables, and overlays in packages/ui.
- Use React Hook Form Controllers for form fields, feature React Query hooks for server state, and shared functions for mapping and derivation.
- Avoid effects for form/derived state synchronization and follow the project rule against component try/catch/finally.
- Preserve React Aria accessibility conventions and generated-client boundaries.

### Cross-layer quality

- Keep the Feature skill focused on orchestration.
- Align Foundation, Persistence, API, and Validator with module constants, tenant scope, helper reuse, and measurable performance.
- Update the audit checklist to accept shared UI compositions and discover the actual API boundary.
- Move skill tags into supported metadata.

### Validation

- All seven skills passed the skill-creator validator.
- Local Markdown references were checked for missing targets.
- Git whitespace checks passed.
- This is a skill/documentation release; application runtime tests were not run for these changes.

### Install

```sh
npx skills add Apisit250aps/wayu-clean-architecture#v1.0.0
```

For a machine-wide installation, add `-g`.
