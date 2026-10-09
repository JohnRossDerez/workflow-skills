---
name: white-paper-writing
description: Research, write, revise, and produce internal technical white papers with traceable claims, methods, calculations, figures, references, and publication QA. Use for substantive documents meant for engineers, analysts, researchers, or technical reviewers; use executive-brief-writing for compressed communication to nontechnical decision-makers, and model-backtesting first when prediction evidence must be calculated.
---

# White-paper writing

Act as the technical document's research lead and editor. Match the commissioned outcome while keeping observations, calculations, assumptions, forecasts, internal assertions, and interpretation distinguishable. User instructions and existing authorizations govern scope; this skill adds no mandatory human gates by default.

This skill preserves the technical record needed for internal understanding, implementation, challenge, or
reuse. It is not an executive-summary generator. Choose the reader purpose first, then read
[profiles.md](references/profiles.md) to select the internal technical audience and appropriate depth.

## Choose the result

Infer one mode from the request and state it briefly. Read only its section in [modes.md](references/modes.md).

| Mode | Reader outcome | Acceptance question |
|---|---|---|
| `investigate` | Understand what the evidence supports | Are credible alternatives tested and unresolved questions visible? |
| `decide` | Choose an action | Are alternatives compared consistently, with decision-changing sensitivities? |
| `explain` | Understand a subject | Are the important concepts, mechanisms, examples, and boundaries intelligible? |
| `argue` | Assess a defensible technical position | Is the position supportable without overstating evidence or hiding material objections? |

After selecting the mode, choose the technical audience profile and record both in the brief. Keep revision scope, research depth, brand, deliverables, and approval policy separate from mode and audience. Preserve requested headings and conclusions as editorial constraints; flag unsupported factual propositions and offer supportable wording. Approval to use a statement does not establish its truth.

## Start or resume

Inspect the assignment, relevant inputs, current draft, prior decisions, and existing project state. Inventory large collections first and inspect material sources in depth. Ask only for missing choices that materially change the result; continue independent work while optional feedback is pending.

For an ordinary technical paper, use the compact workflow in [compact-workflow.md](references/compact-workflow.md). Keep a reader brief, a document plan and the evidence registers; maintain one canonical `report.md`. The initializer defaults to this workflow:

```bash
python3 <skill-directory>/scripts/init_report_project.py <project-directory> --title "Report title" --formats md
```

Choose formats actually requested. For a small edit, use the relevant checks directly without initializing a project. Use the full workflow when substantial parallel authorship, complex claim dependencies or repeated maintained-publication revisions justify executable scheduling and impact queries. Read [workflow.md](references/workflow.md) and [contracts.md](references/contracts.md), then initialize with `--workflow full`. Length, technical complexity and multiple output formats alone do not require a graph.

In either workflow, define what the technical reader should understand or decide and why the evidence supports that message before distributing prose. Record consequential framing choices, uncertainties and constraints. Compare alternative framings only when they change the communication; a settled commission needs no ritual alternatives. Keep evidence support separate from reading order, and perform a whole-document stitching pass after assembly.

Resume from the current brief, plan, evidence and unmet checks. In a full project, use the architecture graph and state records for scheduling and invalidation. Existing projects without a `workflow` setting retain their full-workflow contract; do not silently migrate them or invent prior approvals.

## Research and orchestration

Read [research.md](references/research.md) before substantive research or evidence review. Record material claims and passage-level evidence links before relying on them in the narrative. Record searched alternatives and exclusions in proportion to the assignment. Separate authorization, support strength, source independence, and predictive validity.

Read [orchestration.md](references/orchestration.md) for substantial parallel research, delegated drafting or a material independent review. Use native bounded workers when the task warrants them. Compact assignments receive the reader brief, relevant plan section, evidence and ownership boundaries; full projects can generate graph disclosure windows. The root owns the message, narrative sequence, joins, architecture, shared records, and canonical manuscript. Workers receive a local narrative window and own only assigned evidence or beat drafts. Do not install another agent runtime or require API keys.

## Draft and produce

Read [writing-and-figures.md](references/writing-and-figures.md) when drafting, restructuring, or making exhibits, and read [human-writing.md](references/human-writing.md) before drafting or surface revision. Apply a selected evidence-based voice profile without weakening technical precision. Develop evidence support and the reader's path separately in the document plan; full projects encode these as graph edges and `sequence`. Each beat must add information and hand attention forward; after assembly, perform a dedicated stitching pass that removes repeated setup and writes the cross-beat transitions. After stitching, perform the located prose-editing pass in the human-writing reference and retain representative diagnoses in the existing editorial notes; recheck any changed meaning against its evidence. For relationship visuals, begin with a Mermaid information sketch when useful, then render a quiet, information-rich document surface. Use source IDs for citations (`[@S01]`) and registered number tokens (`{{number:N01}}`).

When a validated backtest evidence bundle is supplied, treat its manifest, metric tables, and graph data as
calculation evidence. Do not recompute or silently reinterpret its cohort, target, baseline, price-band, or
coverage definitions. Preserve the useful legacy report rhythm—executive result, scope, overall model
performance, price-band and group behavior, distribution diagnostics, implications, conclusion—while
removing empty boilerplate and unsupported visual narration. Outlier/inlier sections are not part of the
standard backtest report.

Read [production-and-qa.md](references/production-and-qa.md) before building or delivering. For projects configured with `reader_test_required`, use a fresh reader to test comprehension after semantic revision and route failures to the smallest affected stage. Run preflight, build, review the resulting artifacts, record the reviews, then run release validation:

```bash
python3 <skill-directory>/scripts/validate_report_project.py <project-directory>
python3 <skill-directory>/scripts/build_report.py <project-directory>
python3 <skill-directory>/scripts/record_review.py <project-directory> --kind evidence --reviewer "reviewer identity" --method independent --notes-file qa/evidence-review.md --status pass
python3 <skill-directory>/scripts/validate_report_project.py <project-directory> --release
```

Record the other required reviews using the QA reference. Never record a review as passed before performing it. Review material claims against the original evidence's population, conditions, and support strength; review technical explanations for definitions or mechanisms the reader needs but the text omits. Locate findings in the claim, calculation, or passage and explain the correction. Scripts check structure, traceability, and freshness; they cannot establish semantic truth or visual quality. Report unavailable checks explicitly and deliver a review draft if release requirements remain unmet.

## Handoff

Deliver requested artifacts with the principal finding, material assumptions or limitations, intended internal audience, and actual verification status. Identify any review still pending. Wider internal circulation, publishing, or sending externally is a separate action governed by the user's authorization. For maintenance and behavioral regression checks, read [evaluation.md](references/evaluation.md).
