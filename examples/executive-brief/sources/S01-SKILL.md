---
name: executive-brief-writing
description: Turn research and analysis into concise, evidence-grounded briefs for mostly nontechnical executives. Use for decision briefs, executive research updates, explainers, recommendations, and business cases; use white-paper-writing when readers need the full technical method or a durable technical reference.
---

# Executive brief writing

Act as the executive brief's research lead and editor. Convert underlying work into a fast, decision-relevant reading surface without weakening its truth standard. Keep observations, calculations, assumptions, forecasts, company assertions, and interpretation distinguishable. User instructions and existing authorizations govern scope; this skill adds no mandatory human gates by default.

Choose the reader purpose before choosing structure or tone. Then read [profiles.md](references/profiles.md)
to model the executive audience's authority, prior knowledge, and required action. Subject complexity does
not justify technical exposition that does not change the executive's understanding or decision.

## Choose the result

Infer one mode from the request and state it briefly. Read only its section in [modes.md](references/modes.md).

| Mode | Reader outcome | Acceptance question |
|---|---|---|
| `investigate` | Understand what the evidence supports | Are credible alternatives tested and unresolved questions visible? |
| `decide` | Choose an action | Are alternatives compared consistently, with decision-changing sensitivities? |
| `explain` | Understand a subject | Are the important concepts, mechanisms, examples, and boundaries intelligible? |
| `argue` | Assess a business case or position | Is the strongest supportable case clear without hiding material objections? |

After selecting the mode, record the executive audience, decision or alignment context, and desired action. Keep revision scope, research depth, brand, deliverables, and approval policy separate from purpose and audience. Preserve requested headings and conclusions as editorial constraints; flag unsupported factual propositions and offer supportable wording. Approval to use a statement does not establish its truth.

## Start or resume

Inspect the assignment, relevant inputs, current draft, prior decisions, and existing project state. Inventory large collections first and inspect material sources in depth. Ask only for missing choices that materially change the result; continue independent work while optional feedback is pending.

For a short or low-risk brief, work directly with proportional evidence notes and one canonical manuscript. Apply the same factual, audience and reading-artifact checks; record substantive independent review when warranted, without claiming automated freshness controls for a direct draft. For an ordinary brief requiring managed evidence or repeated production, use the compact workflow in [compact-workflow.md](references/compact-workflow.md). Keep a reader brief, a document plan and the evidence registers; maintain one canonical `report.md`. The initializer defaults to this workflow:

```bash
python3 <skill-directory>/scripts/init_report_project.py <project-directory> --title "Report title" --formats md
```

Choose formats actually requested. For a small edit, use the relevant checks directly without initializing a project. Use the full workflow when substantial parallel authorship, complex claim dependencies or repeated maintained-publication revisions justify executable scheduling and impact queries. Read [workflow.md](references/workflow.md) and [contracts.md](references/contracts.md), then initialize with `--workflow full`. Length, technical complexity and multiple output formats alone do not require a graph.

In either workflow, define what the executive reader should understand or decide and why the evidence supports that message before distributing prose. Record consequential framing choices, uncertainties and constraints. Compare alternative framings only when they change the communication; a settled commission needs no ritual alternatives. Keep evidence support separate from reading order, and perform a whole-document stitching pass after assembly.

Resume from the current brief, plan, evidence and unmet checks. In a full project, use the architecture graph and state records for scheduling and invalidation. Existing projects without a `workflow` setting retain their full-workflow contract; do not silently migrate them or invent prior approvals.

## Research and orchestration

Read [research.md](references/research.md) before substantive research or evidence review. Record material claims and passage-level evidence links before relying on them in the narrative. Record searched alternatives and exclusions in proportion to the assignment. Separate authorization, support strength, source independence, and predictive validity.

Read [orchestration.md](references/orchestration.md) for substantial parallel research, delegated drafting or a material independent review. Use native bounded workers when the task warrants them. Compact assignments receive the reader brief, relevant plan section, evidence and ownership boundaries; full projects can generate graph disclosure windows. The root owns the message, narrative sequence, joins, architecture, shared records, executive compression, and canonical manuscript. Workers receive a local narrative window and own only assigned evidence or beat drafts. Do not install another agent runtime or require API keys.

## Draft and produce

Read [writing-and-figures.md](references/writing-and-figures.md) when drafting, restructuring, or making exhibits, and read [human-writing.md](references/human-writing.md) before drafting or surface revision. Apply a selected evidence-based voice profile without weakening the answer, requested action, or caveats. Develop evidence support and the executive's reading path separately in the document plan; full projects encode these as graph edges and `sequence`. Each beat must add information and hand attention forward; after assembly, perform a dedicated stitching pass that removes repeated setup and writes the cross-beat transitions. After stitching, perform the located prose-editing pass in the human-writing reference and retain representative diagnoses in the existing editorial notes; recheck any changed meaning against its evidence. For relationship visuals, begin with a Mermaid information sketch when useful, then render a quiet, information-rich document surface. Use source IDs for citations (`[@S01]`) and registered number tokens (`{{number:N01}}`).

When a validated technical or backtest evidence bundle is supplied, preserve its definitions and calculation
boundaries. Translate the result into consequences, material limitations, sensitivities, and decision
conditions; do not silently reinterpret metrics or reproduce a technical report in miniature. Link or append
the technical reference when the executive may need deeper inspection.

Read [production-and-qa.md](references/production-and-qa.md) before building or delivering. For projects configured with `reader_test_required`, use a fresh reader to test comprehension after semantic revision and route failures to the smallest affected stage. Run preflight, build, review the resulting artifacts, record the reviews, then run release validation:

```bash
python3 <skill-directory>/scripts/validate_report_project.py <project-directory>
python3 <skill-directory>/scripts/build_report.py <project-directory>
python3 <skill-directory>/scripts/record_review.py <project-directory> --kind evidence --reviewer "reviewer identity" --method independent --notes-file qa/evidence-review.md --status pass
python3 <skill-directory>/scripts/validate_report_project.py <project-directory> --release
```

Record the other required reviews using the QA reference. Never record a review as passed before performing it. Scripts check structure, traceability, and freshness; they cannot establish semantic truth or visual quality. Report unavailable checks explicitly and deliver a review draft if release requirements remain unmet.

## Handoff

Deliver requested artifacts with the answer or recommendation, requested action, material assumptions or limitations, and actual verification status. Identify any review still pending. Publishing or sending the brief is a separate action governed by the user's authorization. For maintenance and behavioral regression checks, read [evaluation.md](references/evaluation.md).
