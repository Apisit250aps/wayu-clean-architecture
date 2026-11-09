# tldraw workflow documentation

Use this option for source-backed workflow canvases. Follow the target repository’s workflow rules, language, paths, and format. The defaults below derive from the HMS module workflow pattern. Use Thai business prose by default and preserve exact code identifiers in technical notes. Mobile/Web handoff intake and English Mermaid labels belong to the separate handoff option.

## Choose scope

- **Full module set** is the default for a new module. Use one directory per module under `docs/workflow/`. Design Endpoint lanes first, then Business and Flow. File numbers indicate reading order.
- **Scoped update** starts from an existing set. Keep frame codes, lane numbers, and shape IDs. Update the requested views and reconcile affected pointers, source maps, and claims across the set. If a scope limit leaves another view stale, report which view and why. When local rules require the complete set to change together, apply those rules within the authorized scope.

| File                       | Reader and purpose                                                                                                                                                                                           |
| -------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `1.<module>-flow.tldr`     | P0 gives the lifecycle for all readers. Show who acts, the main business choices, and the resulting state, notification, or points. Put separate mid-lifecycle triggers in a supplemental frame such as P0b. |
| `2.<module>-business.tldr` | P1 onward gives business readers the detailed decisions and outcomes, grouped by action. Limit each frame to 10 numbered steps by default. P0 has no step limit.                                             |
| `3.<module>-endpoint.tldr` | Shows developers how each request, internal entry point, or timer runs and what data it returns or changes.                                                                                                  |
| `README.md`                | Explains scope, states, roles, route inventory, cross-module handoffs, exceptions, examples, unresolved questions, and the source map.                                                                       |

## Trace the source

1. Resolve the requested source revision. If a Git revision is given, read the code at that revision. For updates, compare against the previous documented hash and check changes to contracts, shared rules, seed data, and callers as well as the owning module.
2. Inventory entry points with trigger, actor, exact method/path or function, permission and tenant scope, request and response schema, and source location. Trace guards and branches through writes, transaction boundaries, audit, and post-commit effects.
3. Check every branch that rejects, skips, returns early, or writes different data. Compare paths that reach the same state by different triggers. For example, if a late accept and a timer both mark an offer expired, check whether both schedule a replacement and record points. If a write precedes an error, check whether it commits. Distinguish intended behavior, behavior derived from code, and runtime evidence.
4. Put the branch and short commit hash on P0, P1, E1, or the first applicable frame of each view. Record the same evidence in the module README and workflow index. Identify any worktree changes used as evidence. Refresh the stamp only for the scope actually verified.

## Flow and Business

- Keep Flow and Business boxes in plain language. Put table names, enums, and other identifiers in a gray code note per frame. Flow shows business outcomes. Business expands rules that affect those outcomes. Technical exceptions invisible to business readers can stay in Endpoint and the README.
- Give each trigger its own start. An edge means the next step follows from that trigger or outcome. An edit performed later, an independent timer, and an external call start their own paths. Separate actions with different rules, such as deactivate and delete.
- Give each decision one question and label every exit. Split compound checks when their failures lead to different outcomes. Draw a loop when each item can follow a different branch. Label the return edge with the next item. Summarize uniform bulk work in one box.
- Show each distinct result, including no change and failed save. Use green ovals for normal completion and gray ovals for rejection or no effect. Use an orange diamond for a decision and a numbered rectangle with a verb and object for a step. In P0, state the outcome in the box after `→` where useful.
- Draw the actors and the module in swimlanes. Show external modules in dashed lanes with the triggering message or handoff. Link to their own documentation for their decisions and writes.
- Use a dashed blue box ending with `ดูต่อ 2.<module>-business P6` for a child flow. Every Business frame must be referenced from Flow.
- Put a blue pointer before each Business path’s normal end. Use two lines, `ดูต่อ 3.<module>-endpoint` and the destination, such as `E2d สาย 2` or `E1 สาย 5, 6`. Include the lane number for single-lane frames too. Use text pointers for the legacy HMS format and keep canvas URL fields empty.

## Endpoint

Group frames by operation. Omit unused groups and retain their numbers. Split large POST groups with stable suffixes.

| Frame      | Entry point                                           |
| ---------- | ----------------------------------------------------- |
| E1         | GET                                                   |
| E2, E2b, … | POST, including actions                               |
| E3         | PUT or PATCH                                          |
| E4         | DELETE                                                |
| E5         | Direct calls by another module, one path per function |
| E6         | Timers owned by this module                           |

E1–E5 have a caller lane above the owning module’s lane. Each route occupies a separate row in the caller lane. E6 uses the module lane only. Describe data access within the module lane.

| Box                   | Content                                                                                                                                                                                                                                                                 |
| --------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Start                 | Oval describing what the caller wants. Start path N with ID `shape:<frame>-box-s<N>` in a legacy canvas.                                                                                                                                                                |
| Request               | `METHOD /path` with the actual route prefix, permission in brackets, and platform-only marker when applicable. Keep within three lines by default and wrap at a path boundary.                                                                                          |
| Inputs                | Purple border. Group by `path`, `query`, and `body`. Show every accepted field, example type, and optional `?`. Indicate when the call has no input. For internal calls, list arguments. Timers have no request or input box.                                           |
| Step                  | Short sentence describing the operation. Append `อ่าน <table>` and `เขียน <table>` with actual mapped table names. Include an audit table when the step writes to it.                                                                                                   |
| Decision or rejection | Put the decision where it occurs. A unique constraint that fails on write belongs after the write attempt. Checks can share a decision when they have the same result. Explain the rejection in plain language and put exact statuses or codes in the README if needed. |
| Result                | Green data box. Start with `จาก <table>` when data comes from tables. Show important fields with typed illustrative values, list or null shape where applicable. Use an outcome oval for internal calls or timers that only produce an effect.                          |

Use sentences in steps, decisions, and rejection boxes. Keep ORM methods and pseudo-code in source references. For UUID fields, use a subline such as `↳ task (task E1)` for the owning table and view, or mark the view as unavailable. Add a blue relationship note in E1 and a gray note per frame for the actual response envelope and request/response schema names. Prefer seed values or fictional examples.

## Layout and annotation

- Use an even grid with one box centered in each cell. HMS uses roughly 420 × 220 for Business cells and 520-wide Endpoint columns as starting dimensions. Reserve space for full input lists and expand cells when labels need room. Keep Business text near three lines, Endpoint step prose near four plus data access lines, and green data boxes near six.
- Draw the main path left to right in the top row of the main lane. Branch below it. Use gutters for connectors and keep them clear of boxes and labels. As a default, each side of a box permits one inbound and one outbound connector. Split decisions with more than three exits. Aim for zero crossings and at most two bends per connector, with room for loops. Document an unavoidable crossing.
- Label every decision exit. Label a cross-lane edge when the payload is unclear. Keep labels short and wrap text at word boundaries.
- Place notes below lanes and the legend at the right of each frame. Use blue for source facts, green for examples, yellow for assumptions, red for open questions, and gray for code names. Match notes to boxes using numbered markers inside the lane. Give open questions stable IDs such as `Q-TK5`; retire the ID when resolved and update the affected decisions and README.
- Preserve the existing editor format. For legacy JSON `.tldr`, preserve the schema and compatible records, and use arrow bindings for both ends of meaningful connections. Use `.tldraw` where the target repository uses it. For open canvases use the available editor tooling. If a canvas is generated, prefer editing its source and regenerating. If a direct edit is necessary, report it so maintainers can reconcile the generator input.

## Check and deliver

- Parse each affected canvas in its expected format. Check shape IDs, frame parentage, and arrow binding targets. Verify that all `ดูต่อ` references resolve to the intended frame and lane.
- Compare request boxes with the controller inventory by method and path, including multiplicity. Recheck field types and optionality, permissions, response schema, table names, state changes, and commit boundaries at the documented revision.
- Keep a source map with frame, stable box ID, and file plus function. Each mapped box needs a source and each entry must reference an existing box. Group IDs only when they share the same source. Reconcile the diagrams, route inventory, questions, source map, and revision across the module set. In the workflow index, list each file with its frame names and revision.
- Open affected frames in a compatible editor when available. Check clipped text, overlapping labels or boxes, connectors crossing boxes or each other, lane or frame overflow, and legibility of branches. Report static checks and visual checks separately.
