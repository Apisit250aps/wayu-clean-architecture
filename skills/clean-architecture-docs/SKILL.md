---
name: clean-architecture-docs
description: Write source-backed Thai JSDoc for declarations and conditions, or Mobile/Web feature and API flow handoffs. Not for implementation task plans.
---

# Clean Architecture Docs

Document actual source and callers within the requested scope. Documentation work does not authorize behavior changes. Load only the requested mode.

| Request | Read and do |
| --- | --- |
| JSDoc/code comments | Read relevant declaration/tag sections of [the JSDoc guide](references/jsdoc.md) and [conditions](references/conditions.md) when conditions are in scope. Inspect callers; use Thai prose and unchanged identifiers unless requested otherwise. No Mobile/Web intake or diagrams. |
| Feature/flow handoff | [Handoff workflow](references/handoff-workflow.md), then adapt [the template](assets/handoff.md). Ask only missing platform/language/flow choices and wait before drafting dependent documents. |
| Both | Apply each mode to its own deliverable; handoff questions do not block independent JSDoc work. |

## Evidence and delivery

- Derive fields, rules, errors, side effects, and guarantees from source; label proposals/discrepancies instead of inventing behavior.
- Keep code signatures, logic, unrelated files, and generated output unchanged for documentation-only work.
- Check formatting, links, and applicable templates/diagram syntax. Report paths, actual checks, and unresolved gaps; static inspection does not prove runtime behavior.
- Do not run builds, live API calls, DB mutations, or application tests solely to write docs unless separately requested.
