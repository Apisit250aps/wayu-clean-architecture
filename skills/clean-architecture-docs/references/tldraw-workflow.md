# tldraw workflow documentation

Use this option for HMS-style, source-backed workflow canvases. Use Thai business prose by default and preserve exact code identifiers in technical notes. Mobile/Web handoff intake belongs to the separate handoff option. If the target repository has HMS workflow rules, read `docs/workflow/README.md`, `rules/business-flow.md`, and `rules/endpoint-flow.md` under `docs/workflow/` along with a complete example module before drawing.

## Output contract

For a new module or a full workflow request, create this exact set:

```text
docs/workflow/<module>/
├── 1.<module>-flow.tldr
├── 2.<module>-business.tldr
├── 3.<module>-endpoint.tldr
└── README.md
```

- **File format:** Each `.tldr` is a VS Code-compatible legacy tldraw JSON document with `tldrawFileFormatVersion: 1`, `schema`, and `records`. Preserve the schema and record conventions of an existing valid `.tldr` or use an exporter that writes this format. A `.tldraw` archive with a renamed extension, Markdown, Mermaid, or one canvas with three pages cannot satisfy this contract. Use another format only when the user explicitly requests it. If the tool cannot produce valid `.tldr`, state the limitation before delivery.
- **Separation:** Flow is the business lifecycle, Business is the detailed process by action, and Endpoint is the implementation view by entry point. Each has its own file, frames, and lane layout. Design Endpoint first, then Business, then Flow. Number the files in reading order.
- **Scoped update:** Edit a subset only when requested. Keep existing frame codes, numbered paths, and shape IDs. Reconcile affected pointers, source maps, and claims in the other files. Report any view that remains stale because of scope.
- **README:** Explain scope, states, roles, route inventory, cross-module handoffs, exceptions, examples, unresolved questions, and the source map. Index each file separately in `docs/workflow/README.md`.

## Trace the source

1. Resolve the requested source revision. If a Git revision is given, read the code at that revision. For updates, compare against the previous documented hash and check changes to contracts, shared rules, seed data, and callers as well as the owning module.
2. Inventory entry points with trigger, actor, exact method/path or function, permission and tenant scope, request and response schema, and source location. Trace guards and branches through writes, transaction boundaries, audit, and post-commit effects.
3. Check every branch that rejects, skips, returns early, or writes different data. Compare paths that reach the same state by different triggers. For example, if a late accept and a timer both mark an offer expired, check whether both schedule a replacement and record points. If a write precedes an error, check whether it commits. Distinguish intended behavior, behavior derived from code, and runtime evidence.
4. Put the branch and short commit hash on P0, P1, E1, or the first applicable frame of each view. Record the same evidence in the module README and workflow index. Identify any worktree changes used as evidence. Refresh the stamp only for the scope actually verified.

## Flow and Business

| View     | Frame and lane layout                                                                                                                                                       | Block placement                                                                                                                                                                            |
| -------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Flow     | P0 shows the main lifecycle. P0b, when needed, has separate starts for independent actions. Order the horizontal lanes by actor or system handoff.                          | Connect business milestones in sequence. Put the action and its result after `→` in the same block. Use a dashed blue milestone for a drill-down to Business.                              |
| Business | P1 onward. One frame per process or related set of triggers. Give each actor its own horizontal lane and each trigger its own start. Split a frame after 10 numbered steps. | Place detailed actions and decisions in the owning actor's lane. Put the Endpoint pointer immediately before the green completion oval. Give rejection and no-effect paths gray end ovals. |

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

E1–E5 have exactly two horizontal lanes. The upper lane contains the caller's start and, for HTTP, the request. The lower lane contains inputs, logic, and output. Each route gets a distinct path and its own caller row, even if routes share schemas or services. E6 uses one module lane. Database access stays in the step blocks.

```text
HTTP caller lane    start oval → request rectangle
                                       ↓
HTTP module lane                    input → numbered step → decision → green data
                                                                ↓
                                                          gray rejection

E5 caller lane      start oval
                        ↓
E5 module lane       arguments → logic → green data or outcome oval

E6 module lane      timer start → logic → outcome oval
```

Reserve one column as a gutter between the HTTP request and input. E5 has no HTTP request box. E6 has no request or input box.

| Box                   | Content                                                                                                                                                                                                                                                                                                                                             |
| --------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Start                 | Oval describing what the caller wants. Start path N with ID `shape:<frame>-box-s<N>` in a legacy canvas.                                                                                                                                                                                                                                            |
| Request               | `METHOD /path` with the actual route prefix, permission in brackets, and platform-only marker when applicable. Keep within three lines by default and wrap at a path boundary.                                                                                                                                                                      |
| Inputs                | Purple border. Group by `path`, `query`, and `body`. Show each field on its own line, indented two spaces below its group. Use typed sample values, such as `"10"` for a string and `10` for a number. Mark optional fields with `?`. Indicate when the call has no input. For internal calls, list arguments. Timers have no request or input box. |
| Step                  | Short sentence describing the operation. Append `อ่าน <table>` and `เขียน <table>` with actual mapped table names. Include an audit table when the step writes to it.                                                                                                                                                                               |
| Decision or rejection | Put the decision where it occurs. A unique constraint that fails on write belongs after the write attempt. Checks can share a decision when they have the same result. Explain the rejection in plain language and put exact statuses or codes in the README if needed.                                                                             |
| Result                | Green data box. Start with `จาก <table>` when data comes from tables. Show important fields as `name: value` lines, with no JSON braces. Mark list rows with `รายการ แถวละ:` and show `null` for a null result. Use an outcome oval for internal calls or timers that only produce an effect.                                                       |

Use sentences in steps, decisions, and rejection boxes. Keep ORM methods and pseudo-code in source references. For UUID fields, use a subline such as `↳ task (task E1)` for the owning table and view, or mark the view as unavailable. Add a blue relationship note in E1 and a gray note per frame for the actual response envelope and request/response schema names. Prefer seed values or fictional examples.

## Same action across all three files

Use this example to distinguish the levels. The names and values are illustrative. Always replace them with verified behavior from the target module.

| View                | Readable path                                                                                                                                                                                                                                       |
| ------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Flow P0             | ผู้ดูแลเริ่มตั้งค่า → `1. สร้างตัวเลือก → ใช้เลือกได้` with `ดูต่อ 2.config-option-business P1` in the dashed block.                                                                                                                                |
| Business P1         | ผู้ดูแลส่งชื่อและรหัส → ระบบถาม `รหัสซ้ำในหมวดไหม` → `ซ้ำ` ends at `สร้างไม่ได้`. On `ไม่ซ้ำ`, save, pass through the two-line `ดูต่อ 3.config-option-endpoint` / `E2 สาย 1` block, then end at `ตัวเลือกพร้อมใช้`.                                 |
| Endpoint E2, path 1 | Caller lane `อยากสร้างตัวเลือก` → `POST /v1/config-options [config_option:create]`. Module lane starts with purple `body` and field lines, then a duplicate decision, a step ending with `เขียน config_option, audit_log`, and green response data. |

## Layout and annotation

A lane is a horizontal band for an actor or system. A path is one trigger-to-outcome chain that can cross multiple lanes. `สาย 2` means path 2 within a frame and points to `s2`, regardless of which actor lane owns its blocks.

Use these tldraw `geo` styles for the HMS blocks:

| Block                  | Shape       | Stroke and fill                                    |
| ---------------------- | ----------- | -------------------------------------------------- |
| Start                  | `ellipse`   | Black, no fill                                     |
| Action or HTTP request | `rectangle` | Black, no fill                                     |
| Decision               | `diamond`   | Orange, no fill                                    |
| Flow drill-down        | `rectangle` | Dashed blue, no fill                               |
| Business pointer       | `rectangle` | Dashed light blue, solid fill                      |
| Endpoint input         | `rectangle` | Violet, no fill                                    |
| Endpoint data          | `rectangle` | Green, solid fill                                  |
| End                    | `ellipse`   | Green for success, gray for rejection or no effect |

- Use an even grid with one box centered in each cell. HMS uses roughly 420 × 220 for Business cells and 520-wide Endpoint columns as starting dimensions. Reserve space for full input lists and expand cells when labels need room. Keep Business text near three lines, Endpoint step prose near four plus data access lines, and green data boxes near six.
- Draw the main path left to right in the top row of the main lane. Branch below it. Use gutters for connectors and keep them clear of boxes and labels. As a default, each side of a box permits one inbound and one outbound connector. Split decisions with more than three exits. Aim for zero crossings and at most two bends per connector, with room for loops. Document an unavoidable crossing.
- Label every decision exit. Label a cross-lane edge when the payload is unclear. Keep labels short and wrap text at word boundaries.
- Place notes below lanes and the legend at the right of each frame. Use blue for source facts, green for examples, yellow for assumptions, red for open questions, and gray for code names. Match notes to boxes using numbered markers inside the lane. Give open questions stable IDs such as `Q-TK5`; retire the ID when resolved and update the affected decisions and README.
- Preserve the existing editor format. For legacy JSON `.tldr`, preserve the schema and compatible records, and use arrow bindings for both ends of meaningful connections. For open canvases use the available editor tooling. If a canvas is generated, prefer editing its source and regenerating. If a direct edit is necessary, report it so maintainers can reconcile the generator input.

## Check and deliver

- Run `python3 <skill-dir>/scripts/check-tldraw-workflow.py docs/workflow/<module>`. Resolve any failures in the output contract, legacy record structure, frame separation, bindings, or pointers. The check reports frame-only pointers, including existing E6 examples. Add the correct path numbers when updating those pointers. Use a compatible editor to validate the actual canvas and its layout.
- Compare request boxes with the controller inventory by method and path, including multiplicity. Recheck field types and optionality, permissions, response schema, table names, state changes, and commit boundaries at the documented revision.
- Keep a source map with frame, stable box ID, and file plus function. Each mapped box needs a source and each entry must reference an existing box. Group IDs only when they share the same source. Reconcile the diagrams, route inventory, questions, source map, and revision across the module set. In the workflow index, list each file with its frame names and revision.
- Open affected frames in a compatible editor when available. Check clipped text, overlapping labels or boxes, connectors crossing boxes or each other, lane or frame overflow, and legibility of branches. Report static checks and visual checks separately.
