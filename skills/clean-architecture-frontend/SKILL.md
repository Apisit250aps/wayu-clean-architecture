---
name: clean-architecture-frontend
description: Build or refactor a Next.js feature UI using shared @repo/ui components, React Hook Form Controllers, React Query feature hooks, React Aria, and the generated API client.
metadata:
  tags: frontend
---

# Clean Architecture Frontend

Use this skill for work in `apps/web`, `packages/ui`, or `packages/client` in a Next.js Clean Architecture monorepo. Follow the repository's existing shared-component and feature-module patterns before adding new UI.

## Start with discovery

Before adding a component, search in this order:

1. `@repo/ui/components/*` for primitives and shadcn/React Aria controls.
2. `@repo/ui/form`, `@repo/ui/shared/*`, and `@repo/ui/hooks` for reusable controller-backed fields, tables, overlays, dashboards, and utilities.
3. `apps/web/src/shared/components`, `shared/utils`, and `shared/hooks` for application-wide composition.
4. The target feature's `components`, `hooks`, `utils`, and `views` for a local pattern.

Compose an existing component when it satisfies the need. Create a new shared component only when it is domain-independent and reused or clearly reusable; otherwise keep it in the owning feature. Use the installed `$shadcn` skill to search and inspect shadcn components before creating a new primitive. React Aria is already part of the UI stack; preserve its accessible component and locale conventions.

## Responsibilities and imports

```text
packages/client  generated HTTP types, services, React Query artifacts
       ↑
apps/web         routes, feature views/components, feature query/mutation hooks
       ↑
packages/ui      reusable primitives and shared UI behavior, including form fields
```

- **`packages/client`** owns TypeSpec-generated `*.gen.ts` output. Regenerate it after a contract change; never hand-edit generated files. Configure the client at the web composition root.
- **`packages/ui`** owns generic, domain-neutral UI. It may provide React Hook Form Controller-backed fields and other reusable interaction components. It must not import application modules, feature hooks, generated services, or domain-specific labels/rules.
- **`apps/web`** owns routes, page/view composition, authorization-aware feature behavior, and `modules/<feature>/{components,hooks,utils,views}`. Pages should stay thin and render a view or layout. Feature hooks call `@repo/client`; components do not make raw HTTP calls.

Read [frontend patterns](references/frontend-patterns.md) when implementing a feature, a reusable UI component, a form, or client data flow.

## State, forms, and server data

- Do not use `useEffect` to copy, initialize, synchronize, or derive component/form state. For forms, keep values in React Hook Form via `useForm`, `defaultValues`/`values`, `reset`, `watch`, and `Controller`.
- Every reusable form field that binds a React Hook Form value must use `Controller`; consume the field's value, change handler, disabled state, and validation state inside its render function.
- Resolve client data through feature `useQuery` hooks and writes through feature `useMutation` hooks. Define and reuse query-key factories from `shared/utils/query`; invalidate the narrow affected keys after success.
- Put shared transformations, error-message extraction, date/path/query-key helpers, and payload mappers in `shared/utils` or feature `utils`, not inline in views.

## React Compiler and interaction rules

- Component render must remain declarative. Do not use `try`, `catch`, or `finally` in components, views, form handlers, or contexts. Handle request failures in mutation/query callbacks and reusable error utilities.
- Use effects only for genuine external subscriptions or imperative browser integrations that cannot be expressed through React Hook Form, React Query, React Aria, props, or derived render state. Document that boundary when one is unavoidable.
- Keep async request orchestration in hooks. Components invoke `mutate`/`mutateAsync` and render pending, success, and error states; they do not implement transport control flow.

## Verify

Use domain constants or generated enum types for stable business values instead of local string catalogs. Keep mutable tenant policy in query data and scope relevant cache keys by tenant. Search shared UI, field adapters, error/payload mappers, and feature hooks before adding alternatives. Measure expensive renders or large-list behavior before introducing memoization or virtualization.

Run the affected workspace's type check and lint. When contracts change, regenerate the client before checking the web application. Do not claim browser behavior is verified unless the relevant route has been exercised.
