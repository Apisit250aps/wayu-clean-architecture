---
name: clean-architecture-feature
description: Orchestrate an end-to-end Clean Architecture feature across the required layers without duplicating layer-specific implementation guidance.
metadata:
  tags: both, fullstack, backend, frontend
---

# Clean Architecture Feature Orchestrator

Use this skill for a feature that crosses two or more layers. It coordinates work; the selected layer skills remain the source of implementation detail.

## Route the feature

1. Start with `$clean-architecture-core` to define the business model and use cases.
2. If it persists data or integrates an adapter, use `$clean-architecture-persistence`.
3. If it exposes or changes an HTTP contract, use `$clean-architecture-api`.
4. If it changes screens, forms, or shared UI/application composition, use `$clean-architecture-frontend`.
5. Use `$clean-architecture-validator` to audit the completed change. Use `$clean-architecture-foundation` only when the workspace/package configuration itself must change.

Work inward to outward and do not create a layer merely because this checklist names it. Read [the end-to-end example](references/end-to-end-example.md) for a full module only when a comparable example is useful; read [the feature guide](references/feature-generation-guide.md) for the delivery checklist.

## Delivery checks across layers

- Before creating another helper or component, search the owning layer's shared code and the sibling module's implementation. Reuse semantics, not just similar syntax.
- Every new module/table includes its domain constants and aggregate permission mapping; update feature/action/default-grant catalogs and seed migrations when affected.
- Carry trusted tenant ownership, lifecycle policy, and concurrency requirements from core into repository predicates, API contracts, and frontend query keys.
- Verify actual behavior for the affected boundaries. Report static findings, runtime verification, and performance measurements separately. Refactoring into shared functions does not itself establish faster execution.
