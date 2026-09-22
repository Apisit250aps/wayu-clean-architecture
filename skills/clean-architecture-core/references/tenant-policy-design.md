# Tenant scope and configurable policy

## Three kinds of data

| Kind | Source and owner | Examples |
| --- | --- | --- |
| Stable business vocabulary | Domain constants, versioned with code | Resource/action codes, lifecycle modes |
| Global system catalog | Domain seed definitions plus versioned DB migrations | Built-in features, permissions, role defaults |
| Tenant configuration and facts | Tenant-scoped persisted records | Enabled features, custom roles/grants, schedules, review assignments |

Treat organization as the tenant in the reference project. Sites and members are children of that scope. Global records must be explicitly modeled as global; a missing tenant ID must not broaden a tenant query.

## Trusted request context

Build security attributes from the verified session or a trusted internal service principal. Request bodies must not set `permissions`, `user.isAdmin`, or `activeOrganizationId`. In the reference project `ISecurityContext` includes those values; its TypeScript shape alone does not make untrusted data safe.

For read/update/delete by ID, authorize against stored ownership. For creates, authorize the destination tenant and verify every referenced role/member/site/template belongs to the expected scope. Tenant reassignment is a distinct operation, not a generic update field. Background jobs and batch commands carry explicit tenant scope too. Partition any derived cache by tenant and relevant policy identity. This follows [OWASP's tenant-isolation guidance](https://cheatsheetseries.owasp.org/cheatsheets/Multi_Tenant_Security_Cheat_Sheet.html).

## Dynamic access, not role-name branching

For a tenant capability, evaluate the applicable checks separately: active actor/membership, organization feature entitlement, role feature assignment where the product uses it, action grant, resource ownership/assignment, and lifecycle policy. Share evaluation helpers without merging these distinct decisions into a vague `isAdminOrOwner` flag.

Use current persisted grants and active membership according to the session freshness policy. Role names, creator IDs, and contributor history are not permission grants. A new action must not automatically appear in every default role through `Object.values(PERMISSION_ACTIONS)`. Keep default grants explicit and define how catalog updates affect existing tenant customizations.

An explicitly trusted platform-admin policy may cross tenants; do not derive this from a role label or silently weaken tenant checks for missing scope. Preserve existing intentional platform behavior and verify it separately.

## Typed policy extension

Represent real variation with validated finite policy modes or discriminated configurations, such as recurring versus explicit schedules or ALLOW versus DENY late submission. Resolve an effective tenant policy once per operation, validate it, and pass it to pure functions or an injected strategy.

Use a strategy map only when several implementations genuinely vary by mode. Ensure all declared modes have a handler and unknown modes fail explicitly. Keep mutable tenant configuration in storage; never introduce tenant-specific code branches or executable policy strings.

Decide whether future operations use current configuration or a stored version. Historical reviews/submissions may need their original version or policy snapshot to remain reproducible. Store that version/decision when required; do not recalculate historical decisions using today's settings.
