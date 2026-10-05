# Compact writing workflow

Use this for ordinary internal R&D papers and executive briefs. The truth and review standards are shared with the full workflow; the planning representation is smaller.

## Initialize and plan

Short or low-risk briefs may use the direct path described in SKILL.md. This managed path is appropriate when evidence registers, builds and automatic freshness checks are useful.

Run `scripts/init_report_project.py <project> --title "Title" --formats md` with the requested mode and formats. The default is `--workflow compact`. Python helper callers may pass `workflow="compact"`; the legacy function default remains full for compatibility.

In `planning/brief.md`, record the reader, purpose, prior knowledge, attention, scope, requested deliverables, stakes and consequential decisions. In `planning/plan.md`, record the supported message, what the reader should understand or decide, an ordered outline and any dependencies or uncertainties that affect drafting. Use prose or a short table. Do not make a record per paragraph or register ordinary vocabulary. Draft one canonical `report.md`.

Keep the shared source, claim and passage-link registers as the evidence ledger. Use number/calculation records when values or transformations matter, and figure records when an exhibit is present. Empty conditional registers are valid. Record material claims and their qualifications, not every sentence. A compact record does not relax source verification or permit unsupported synthesis.

## Draft and verify

Follow the selected audience/mode and shared research, prose and exhibit references. Preserve technical mechanism for technical readers and decision-changing consequences for executives. Keep material qualifications in the reading path. If a worker is useful, supply only the relevant brief, plan section and evidence; keep canonical policy, joins and the manuscript with the lead.

Run the same preflight, build, actual evidence/editorial/fresh-reader reviews and release validator as a full project. Store substantive review notes under `qa/` and bind them with `record_review.py` only after performing the check. A validator pass establishes structural controls and freshness, not truth or comprehension.

## Revise

On changed sources or requirements, inspect the changed evidence and affected claims, update their support and qualifications, and revise the dependent body, opening, conclusion, tables and exhibits. Record the reason and any remaining uncertainty in the brief or plan. Rebuild; prior bound reviews become stale. Repeat the affected semantic/editorial checks and obtain a fresh reader for the final artifact. Never copy an old review digest onto new content.

## When to use the full representation

Choose `--workflow full` for substantial parallel authorship, complex dependencies that need repeated impact queries, or maintained publications where executable scheduling earns its upkeep. Full projects use the architecture, message, concept and control records described in workflow.md and contracts.md. One technical report, several formats or a single revision is not sufficient reason by itself. Existing full projects retain their contract; create a separate compact project only when conversion is authorized and its evidence/review lineage can be preserved.
