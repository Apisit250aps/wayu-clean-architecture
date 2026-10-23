# Naming, formatting, and boundary enforcement

## Types and names

Use explicit types or `unknown` with narrowing; no `any`, `@ts-ignore`, `@ts-expect-error`, `@ts-nocheck`, or eslint-disable comments. Fix the contract instead of suppressing the failure.

Follow sibling module/file names and preserve public imports. Group by business capability and split by responsibility, not an arbitrary file length. Stable Domain values belong in owning constants; helpers use descriptive concrete files rather than a generic utility bucket.

## Formatting

Use the repository's formatter/configuration. For a new workspace with no convention, a compact baseline is:

```json
{
  "semi": true,
  "singleQuote": true,
  "trailingComma": "all",
  "printWidth": 80,
  "tabWidth": 2,
  "useTabs": false
}
```

Ignore dependencies, build/generated output as appropriate, coverage, logs, lockfiles, and agent caches. Add format/check scripts using the existing package runner; do not reformat unrelated files for a scoped change.

## Enforcing boundaries

Use existing ESLint/import tooling or dependency-cruiser if installed. Implement [the package matrix](architecture-overview.md#package-matrix), covering package roots, subpaths, aliases, and relative imports. For a single-package layout, map the same rules to its Domain/Application/infrastructure/presentation directories.

Keep composition exceptions limited to actual wiring files. Do not replace existing restrictions when adding a rule, or assume package-import checks detect cross-owner SQL/helpers. Verify one allowed and one forbidden import using the project's resolution settings, then remove probes.

## Helpers and comments

Follow [helper ownership/import rules](../SKILL.md#helper-files-and-imports). Add Thai JSDoc for declarations and every condition written/changed, explaining source facts, reason, and outcomes; use the relevant sections of [the JSDoc guide](../../clean-architecture-docs/references/jsdoc.md). Do not change logic to accommodate comments.
