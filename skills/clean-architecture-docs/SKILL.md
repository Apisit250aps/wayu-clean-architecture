---
name: clean-architecture-docs
description: Create source-backed feature or flow handoff docs for Mobile or Web teams, with interactive platform and language selection, decision flowcharts, and API sequence diagrams. Use for integration documentation rather than implementation task plans.
---

# Clean Architecture Docs

Create documents that let the receiving team understand user actions, API order, request value origins, and supported outcomes. Documentation does not authorize application changes.

## Interactive intake

Before drafting, ask for choices not already explicit in the conversation:

- Platform: Mobile, Web, or both.
- Document language: Thai, English, or another user-specified language for headings and explanatory prose. All diagram text stays in English regardless of this choice. Keep paths, identifiers, fields, and error codes unchanged.
- Scope: feature overview, individual flows, or both; ask which feature/flows if unspecified.

Use an available interactive question tool with selectable options and free text, in the user's language and within its question limit. If unavailable, ask concise numbered questions in chat. These choices are required: wait for answers before drafting dependent documents. A preselected option or elapsed time is not an answer. While waiting, inspect source without writing deliverables. Clarify ambiguous answers with a focused follow-up. Briefly summarize the selected scope and proceed without another approval round.

Infer output location from repository conventions; ask only if competing destinations materially affect the handoff.

## Inspect actual behavior

Read repository instructions and existing docs. Trace selected flows through mounted routes, handlers, API contracts (TypeSpec/OpenAPI or equivalent), use cases, domain policies, and relevant client consumers. Do not assume package paths or frameworks.

- Verify exact method/path, authentication, tenant/member context, permissions, encoding, required/optional fields, response envelopes, and actual errors.
- Trace dependencies: selected IDs, mutation/upload results, pagination, preview results, and subsequent refresh calls.
- Distinguish backend support from implemented client behavior. If the target client is absent, describe its integration contract and label proposed client behavior.
- Record contract/implementation discrepancies and missing facts. Never invent endpoints, fields, error codes, refresh-token flows, or business rules.
- Treat plans as proposals. Source inspection is static evidence; claim runtime verification only when actually performed.

## Write the handoff

Adapt [the handoff template](assets/handoff.md): headings and explanatory prose use the selected language; diagram labels, participants, messages, notes, and branch conditions use English. Preserve exact API identifiers and literal contract values, even when they contain another language. Replace tokens and remove inapplicable sections. Preserve useful existing docs and unrelated flows.

Separate each flow into readable sections in this order: overall flowchart → explanation of steps and decisions → API sequence diagram → explanation of API ordering and data dependencies → ordered API table and per-case contract examples. Do not place diagrams back-to-back or combine the journey and API sequence in one diagram. For large flows, split into named subflows and explain each before moving to the next diagram.

Follow existing paths. Otherwise use `docs/features/<feature>/README.md` for the feature entry point and `docs/flow/<mobile|web>/<feature>/<flow>.md` for separate flows. For both platforms, create separately linked Mobile and Web flows; share API reference material when useful. Create only files needed for the selected scope. Feature-only docs still need diagrams and API order for covered workflows.

For every covered flow, include:

1. Goal, actor, trigger, prerequisites, entry state, and final state.
2. Mermaid `flowchart` showing the overall journey and source-supported decisions, including relevant failure/recovery paths. A state diagram can supplement state-heavy features.
3. Mermaid `sequenceDiagram` showing client-facing API calls in order, exact methods/paths, responses, and supported `alt`, `opt`, `loop`, or `par` branches. Separate different actors where needed. Never parallelize calls that consume each other's results.
4. Numbered API table aligned with the sequence: trigger/condition, method/path, input and origin, response used next. Explicitly connect returned fields to subsequent request fields.
5. Per-endpoint, per-case request body and response examples with actual encoding and envelopes, illustrative values, and no real credentials/personal data. Cover every source-supported, integration-relevant case with distinct inputs, response shapes, business outcomes, or recovery actions (including alternative successes and errors). Give each case a heading, triggering condition, request, HTTP status, response, and explanation of what the client does next. Show required/optional fields, uploads, and null/missing values where relevant. Reuse an explicitly linked shared request for cases with identical input rather than repeating it. For bodyless requests, say there is no body and show relevant path/query/header inputs; for empty responses, show the status and say there is no response body. Do not invent JSON for multipart requests or unknown error envelopes. Mark unavailable examples as unresolved with source evidence.
6. Actual errors, business outcomes, and recovery actions. Distinguish HTTP success from business completion, pending approval, async publication, or device delivery when applicable. Label recommended client recovery separately from implemented behavior.
7. Concrete source links, verification status, and unresolved integration questions.

Keep the receiving team's perspective central. Mobile docs explain supported session/context propagation and device/upload prerequisites. Web docs explain supported navigation, submission, and refetch/cache behavior. Internal details belong only when they affect integration. Do not prescribe unverified offline support, retries, or frontend libraries.

## Check delivery

- Every covered flow has both diagrams in its actual file, with relevant alternative outcomes. Chat-only diagrams do not count.
- Tables, diagrams, and examples agree on paths, ordering, conditions, IDs, and outcomes.
- Diagram text is English, explanatory prose follows the selected language, and meaningful explanations separate diagram sections.
- Every integration-relevant case identified in source has a request/response example or an explicit unresolved gap; case headings, HTTP statuses, and next client actions agree with the outcome table.
- Recheck endpoints and fields against source. Check relative links and balanced Mermaid fences. Use an existing local Mermaid parser/renderer if available; otherwise report rendering as unverified.
- Follow repository formatting tools when available. Do not run builds, live API calls, database mutations, or application tests solely to write docs unless separately requested.
- Report created/updated paths, chosen platform/language, actual checks, and material gaps. Do not mark incomplete integration behavior as verified.
