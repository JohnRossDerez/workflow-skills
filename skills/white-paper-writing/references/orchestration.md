# Graph orchestration and model policy

For compact projects, skip tree_workflow.py readiness/disclosure and send a bounded reader brief, plan section and evidence slice directly. Keep global message, joins and authoritative evidence with the lead. Record actual worker identity and evidence when delegation is used; do not initialize a graph merely to delegate. The graph-specific procedures below apply to full projects.

Use the session's native delegation capability; tool names vary by host. Do not emulate delegation by launching nested Codex processes or install an agent framework. `planning/architecture.json` and `scripts/tree_workflow.py` determine what work is ready; the model decides content within those boundaries.

## Default models

`control/orchestration.json` records the prescribed defaults:

| Role | Default | Effort | Responsibility |
|---|---|---:|---|
| root architect/editor | `gpt-6-sol` | high | purpose, tree, synthesis, conflict resolution, canonical manuscript |
| researcher | `gpt-6-sol` | medium | bounded research and evidence packages |
| leaf writer | `gpt-6-sol` | high | supported node drafts under `drafts/` |
| semantic reviewer | `gpt-6-sol` | high | evidence, parent-child sufficiency, counterargument, meaning |
| cold reader | `gpt-6-sol` | medium | unprimed comprehension and attention test |
| proofreader | `gpt-6-luna` | medium | consistency and surface defects after semantic freeze |

Use `gpt-6-luna` at medium effort as the compatibility worker when the preferred role model is unavailable. If the host cannot assign different models within one run, use `gpt-6-sol` at high effort for all roles. Record the actual model and effort in `control/agent-runs.json`. Do not silently replace a user-selected model. Models with `astra` in the model ID are prohibited for this workflow even if the host offers them.

The defaults reflect the 2026-09-24 policy snapshot. Recheck official model guidance before changing them: Sol handles research, writing, and judgment; Luna handles focused mechanical review. Model choice never relaxes evidence or acceptance criteria.

## When delegation is required

Delegate when the validated graph exposes at least three independent ready leaves, when research divides into substantial independent questions, or when a consequential conclusion needs an independent semantic review. Use no more than three concurrent subagents by default. Prefer one agent when the work is small, sequential, or would make agents contend over the same mutable artifact.

Run `tree_workflow.py ready` for the relevant phase before spawning. Assign complete ready nodes, not arbitrary page ranges or source counts. Parallel workers must not edit `report.md`, `planning/architecture.json`, shared evidence registers, or another worker's files. The root reconciles their outputs and advances statuses.

## Narrative context across agents

Before assigning a node, run `tree_workflow.py disclose <project> --node <node-id>`. Its version-3 output includes the selected document message and proof direction, support ancestors, prior and next narrative beats, established concepts and claims, and the distance to relevant prior mentions. Give the worker this bounded window and the compact reader-stakes card from `planning/brief.md`, with the node's outcome, unique new information, handoff, claims, and concept records. Keep rejected message candidates in the decision record, outside routine node disclosure. The worker should develop its contribution, not restart the document, enumerate its contract, or repeat established detail merely to sound complete.

For prose work, also give the worker the selected `planning/voice.md` version, its compact runtime card, and the tone delta for this audience and node. At most two short calibration excerpts should accompany the card. Researchers do not need voice context unless they are drafting reader-facing prose. The root performs a whole-document voice pass after assembly because locally consistent leaves can still produce global drift.

A worker returns the beat's prose first, followed by its evidence and limitation manifest. A worker may delegate independent support work only after passing the same message, proof direction, and local narrative window forward. The root assembles beats in narrative sequence and validates separately that the support graph reconstructs each synthesis. Agent hierarchy never substitutes for that sufficiency check.

## Roles and ownership

The root acts as narrative director and owns the brief, message contract, proof direction, architecture graph, transitions, concept and evidence records, synthesis, decisions, and canonical manuscript. Evidence researchers investigate distinct questions or calculations and report newly required concepts or competing definitions. Leaf writers draft only assigned beats. A semantic reviewer checks consequential claims, reader movement, concept continuity, and whether support establishes the message. A proofreader works only after semantic freeze.

These are roles, not a requirement to create one agent per node. Reuse a worker for several independent nodes when its bounded context remains coherent. Keep the final narrative under one root. If a separate reviewer is unavailable, record a separate self-review pass rather than claiming independence.

## Worker contract

Give each worker:

```text
Question and intended reader outcome:
Reader-stakes card (attention, belief, trust, resistance, authority, retention):
Communicative thesis, central tension, and proof direction:
Architecture node ID, status, dependencies, and acceptance contract:
Root-to-node disclosure path (ancestor questions and syntheses):
Previous beat, next beat, established context, and last-mention distance:
Rhetorical role, unique new information, handoff, and visual role:
Claim IDs and scope boundaries:
Required concepts, assigned introductions, canonical terms, and synthesis basis:
Voice profile path/version and applicable tone delta:
Input files and content version:
Preferred model and reasoning effort:
Source classes and relevant constraints:
Output path or structured response:
Required evidence: source ID, locator, excerpt, support relation, limitations:
Countertest or plausible competing explanation:
Time/tool budget and stopping condition:
Files owned by this worker:
```

Workers return the requested beat without prefacing it with a summary of their assignment. Append a compact manifest of evidence links, calculations, counterevidence, unresolved gaps, concepts introduced and used, claims expressed or derived, qualifications preserved, and any requested canonical-term change. Return artifacts plus a concise completion or limitation note; do not rely on conversational memory for evidence. Store research under `research/` or `analysis/` and prose under its declared `draft_path`; only the root reconciles shared records, graph status, transitions, and `report.md`. Reject findings that have no retrievable underlying source.

## Assembly and stitching

After merging beats, the root performs a dedicated stitching pass before semantic review. Remove repeated setup, duplicated evidence, and local mini-conclusions; write the transitions that explain why the next beat follows; restore forward pull; and reintroduce an earlier detail only to reinterpret it, make a decision with it, or close a deliberate long-range thread. Preserve analytical meaning while varying pace and the level of abstraction. Leaf workers do not own cross-document joins.

## Coordination

Partition by independent questions, not by arbitrary source counts. Reuse a source inventory to avoid repeated retrieval; preserve distinct original sources behind syndicated reporting. The lead reconciles disagreements by definitions, scope, dates, measurement, and provenance rather than majority vote.

Do not ask workers to draft leaves before evidence and node contracts are supported. Retry a failed tool or missing source with a relevant alternative; stop at the task's budget and return a gap when further work cannot change the result. When an assumption changes, invalidate the affected nodes before issuing revised contracts.

## Reviewer independence

Give the reviewer the commission, message contract, current manuscript, architecture graph, concepts, original evidence, and acceptance criteria. Ask first whether the chosen proof direction creates the intended reader movement without repetition or missing joins, then whether claims, qualifications, and definitions support that movement. Do not prime it with the author's desired verdict. A reviewer must return located issues with severity, evidence, and proposed disposition. The lead resolves them and requests targeted rechecks. Reviewer disagreement alone is not a veto; unresolved material factual defects are release blockers.

## Cold-reader independence

The cold reader has a different task from the semantic reviewer. Give a fresh human or agent only the intended audience and commission plus the reader-facing artifact; withhold the selected thesis, architecture, evidence register, earlier drafts, and review history. Ask for unprompted comprehension and attention failures, not a verdict on whether the writer followed the plan. The root compares that reading with private contracts, diagnoses the smallest affected stage, and records issues. For an agent, use the `cold_reader` model and effort in the policy and log the actual run with that role. Never use an Astra model.
