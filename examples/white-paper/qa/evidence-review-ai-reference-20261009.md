# Independent AI-reference evidence review — white paper

- Reviewer: independent agent, gpt-6-sol, high reasoning; 2026-10-09.
- Reviewed canonical `report.md` SHA-256: `AE85C39D6993BF95C27EEF1BF8BA9B496D63A952A4821BF87D0A936E3FE2BA91`.
- Scope: the new **Bounded AI tasks** paragraph, its C16/C17 claims and E16/E17 links, S16 metadata and saved extract, the [original Anthropic article](https://www.anthropic.com/engineering/building-effective-agents), and surrounding manuscript for misleading implications. The other historical and external claims were not re-reviewed; their earlier independent baseline is `qa/evidence-review-researched-20261009.md` (final citation-only check bound to manuscript SHA-256 `3EA34CD58987654DA0762A12D0C6FE8CE172D4ACEB4CF78CBD8DF9A495D950E6`). This is a targeted semantic evidence check, not a PDF review or new efficacy experiment.

## Verdict

**Pass for the reviewed manuscript hash, with a minor excerpt-precision suggestion.** The paragraph uses Anthropic's article as practitioner design guidance and explicitly says it does not prove this writing skill works. The separation of evidence checking, prose editing, and reader testing is plainly introduced as this project's application of the article, not a practice Anthropic tested on this skill.

## Source fit

- **C16 / E16:** The original article's “When (and when not) to use agents” section recommends the simplest workable solution and increasing complexity only as needed. Its “Workflow: Evaluator-optimizer” section says this pattern fits clear evaluation criteria and measurable value from iterative refinement. These passages support the manuscript's compressed description of simple workflows and clear evaluator criteria. E16's saved excerpt covers only the simplicity part; its locator does point to the evaluator section. Adding an excerpt for that second part would make the ledger easier to audit, but the underlying claim is supported.
- **C17 / E17:** The article describes decomposition into fixed subtasks, parallel review of distinct aspects, and evaluator feedback as patterns whose fit depends on the task. Its “Combining and customizing” section calls for added complexity only when measured outcomes justify it. Separating this paper's evidence, prose, and reader checks into bounded tasks is a reasonable, explicitly labeled application. E17 correctly records partial support: Anthropic does not prescribe these exact three writing roles or demonstrate their effect here. The manuscript's “only when it improves the result” is design advice, not a reported measured improvement.
- **S16 / caveat:** The original is dated 2024-12-19 and now warns that much of the tooling landscape it described has changed. S16 correctly classifies it as vendor practitioner guidance and limits its use to workflow principles. The manuscript makes no claim about current Anthropic tools, model performance, or controlled efficacy.

The surrounding abstract and demonstration section keep external guidance separate from local outcomes. The latter still discloses the initial defects, agent-only final reviews, small comparison, and PDF boundary. I found no new misleading inference or missing counterevidence introduced by the AI-reference paragraph.

## Review limits

I inspected the live original page and saved S16 extract, but did not repeat the historical author cases, independently measure this workflow's quality, or reopen the unchanged source graph. This verdict applies only to the manuscript hash above and the targeted records as inspected.
