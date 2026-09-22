# Frontend Patterns

This reference reflects a feature-oriented Next.js App Router frontend with `@repo/ui`, React Hook Form, React Query, React Aria, and a generated TypeSpec client.

## File placement

```text
apps/web/src/
  app/.../page.tsx                 route entry: render the owning view
  modules/<feature>/
    views/                         screen-level composition
    components/                    feature-specific presentation
    hooks/<feature>-queries.ts     generated-client reads + query keys
    hooks/<feature>-mutations.ts   generated-client writes + invalidation
    utils/                         feature-only mapping and derivation
  shared/
    components/                    cross-feature app composition
    hooks/                         providers and browser integration
    utils/                         query keys, errors, dates, paths, URLs

packages/ui/src/
  components/                      shadcn / React Aria primitives
  shared/form/                     Controller-backed generic fields
  shared/table|button|dashboard/   reusable generic compositions
  hooks/                           generic interaction and overlay hooks

packages/client/src/api/*.gen.ts   generated: never edit directly
```

## Reuse decision

Search `@repo/ui` before creating markup or a field. Prefer a primitive for a simple control, an existing `@repo/ui/form` field for standard RHF binding, and `apps/web/src/shared/components/form` for a cross-feature control that requires app data.

Keep a component in `modules/<feature>` when its wording, permission logic, API type, or query behavior belongs to one business capability. Promote it to `packages/ui` only after removing all business knowledge and accepting generic props.

## Controlled form pattern

The form owns values and validation. A shared field accepts `control` and `name`; it must not mirror the field value in local state or synchronize it with an effect.

```tsx
const methods = useForm<FormValues>({
  resolver: zodResolver(schema),
  defaultValues,
  values: loadedValues,
});

<form onSubmit={methods.handleSubmit(onSubmit)}>
  <InputField name="name" label="Name" control={methods.control} required />
</form>
```

```tsx
<Controller
  control={control}
  name={name}
  render={({ field, fieldState }) => (
    <Field data-invalid={fieldState.invalid} data-disabled={field.disabled}>
      <FieldLabel htmlFor={id}>{label}</FieldLabel>
      <Input {...field} id={id} aria-invalid={fieldState.invalid} />
      <FieldError errors={fieldState.error ? [fieldState.error] : undefined} />
    </Field>
  )}
/>
```

Use React Aria controls and the repository's `Field` primitives for accessible labels, descriptions, disabled state, and validation state. Dialog, Sheet, and Alert Dialog content must have an accessible title, visually hidden if necessary. `I18nProvider` and `RouterProvider` remain at the client provider boundary.

## Generated client and React Query

Web providers configure the generated client once, including the relative API base URL and error mode. A feature query consumes a generated service and its abort `signal`; it has a stable query key from `shared/utils/query`.

```tsx
export function useOrganizationQuery(organizationId: string) {
  return useQuery({
    queryKey: organizationKeys.detail(organizationId),
    enabled: Boolean(organizationId),
    queryFn: async ({ signal }) => {
      const response = await organizationServicesGetOrganization({
        path: { id: organizationId },
        signal,
      });
      if (response.data) return response.data.data;
      throw new Error('Organization response contains no data');
    },
  });
}
```

Mutations own transport calls, toast/error mapping, and targeted invalidation. Keep component handlers declarative: validate with `handleSubmit`, call `mutate`, and navigate or render feedback through callbacks. Do not use component-level `try`/`catch`/`finally` for mutation flow.

## State rules

Derive render values from props, form watches, query results, and query status. Store only true user interaction state locally. Do not use `useEffect` to copy a prop/query/form value into `useState`, to initialize a form, or to invalidate/refetch data after a mutation. Prefer React Hook Form's `values`/`reset`, React Query mutation callbacks, event handlers, and derived values.

An effect is reserved for an external subscription or imperative browser API with a real lifecycle. Keep it small and ensure cleanup belongs to that external resource.

## shadcn workflow

Before adding a primitive, inspect existing `packages/ui/src/components`. If absent, use `$shadcn` to search a named registry, read the selected component documentation, then add and review it with the workspace package runner. Do not overwrite an existing component without an explicit user request. Preserve the workspace import aliases and React Aria/base component APIs.
