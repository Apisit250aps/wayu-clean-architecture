---
name: clean-architecture-frontend
description: Build Next.js feature UIs or Domain-informed mockups with shared UI, RHF/Controller, React Query, and the main application's generated API client.
metadata:
  tags: frontend
---

# Clean Architecture Frontend

Inspect the target feature and shared components before editing. Search UI primitives → shared UI fields/tables/overlays → app shared components/hooks → feature code. Reuse the closest suitable component; use the installed shadcn skill when a new primitive is needed.

## Ownership

- `packages/ui`: generic, domain-neutral components and Controller-backed fields; no business hooks, generated services, or backend imports.
- `apps/web`: thin routes and feature `views/components/hooks/utils`; hooks own client calls, errors, query keys, and invalidation.
- `packages/client`: generated HTTP types/services. Configure once at the Web composition root and regenerate after spec changes; never hand-edit output.

## Choose the work

- **Mockup:** agreed Domain contracts and screen flows are enough to start. Use typed fixtures/props or existing mocks, safe public type imports or a small feature view model. Keep simulated wiring out of production requests. Real integration uses the main application's spec-generated client, with a separate mapping/integration task; do not create a second spec/client.
- **Feature, form, or client integration:** read the relevant sections of [frontend patterns](references/frontend-patterns.md), including accessibility and data flow.
- **Dates/time zones:** use the central UI formatter and `DATE_FORMATS` presets; no feature-local display formatters/options. Read [time handling](../clean-architecture-foundation/references/time-handling.md).

## State and interaction

- RHF/Controller owns editable fields in form/query/mutation components. React Query owns server data, request status, and cache. Do not mirror either through `useEffect` or local state.
- Use form defaults/values/reset, query/mutation callbacks, and render derivation. Effects are for genuine external subscriptions/imperative browser APIs with cleanup.
- Components invoke mutations and render state; no `try/catch/finally` in components, views, form handlers, or contexts. Request orchestration and error handling stay in hooks/utilities.
- Keep business constants stable, mutable tenant policy in query data, and query keys scoped by tenant/filters. Map payloads in feature/shared utils.
- Import helpers directly; keep standalone helpers outside class files. Use explicit types without suppressions and Thai JSDoc for [changed conditions](../clean-architecture-docs/references/conditions.md), including rendering expressions.

## Verify

Run affected type/lint checks; regenerate changed HTTP contracts first. Exercise relevant form, loading/error/empty, permission, and success states. Report mock/static/browser/API evidence separately. Measure before adding memoization/virtualization; do not claim browser behavior without exercising it.
