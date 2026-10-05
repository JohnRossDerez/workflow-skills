# Maintaining and evaluating the skill

Exercise both workflow branches. Compare compact and full records on the same commission and sources, then supply a consequential source correction. Check factual fidelity, unaided comprehension, stale-review rejection and dependent revision. Record actual file/context/rework measures; counts alone do not establish quality or cost.

Run the bundled deterministic regression checks after changing the helpers:

```bash
python3 -B <skill-directory>/scripts/test_report_workflow.py
```

The tests create isolated temporary projects. They check observable failures such as unknown evidence IDs, lost qualifications, incorrect rounding, stale content/reviews, edited artifacts, missing visual inspection, and consistent multi-format builds. They do not replace behavioral testing of research or writing.

For a substantial instruction change, use an independent Codex worker when available and authorized. Give it the skill, a realistic request, and raw inputs in a temporary workspace; do not tell it the desired answer or suspected failure. The author can continue helper verification while the worker exercises the workflow. Inspect the actual artifacts and fix only demonstrated defects.

Useful behavioral cases:

| Request | Observable acceptance criteria |
|---|---|
| Investigate a plausible but false thesis | Tests a competing explanation and reports the supported answer without preserving the false premise. |
| Recommend between three options with uncertain demand | Includes baseline, common comparison criteria, and sensitivity that can reverse the choice. |
| Explain a technical system to an internal builder | Defines necessary concepts, boundaries, interfaces, and failure modes; labels hypothetical examples; avoids inventing a recommendation. |
| Explain a system containing unfamiliar metrics and acronyms | Introduces each prerequisite before substantive use, retains canonical terminology, and gives only the context this audience needs. |
| Turn accurate node drafts into a coherent technical paper | Leads with each point, develops rather than restates it, uses domain-native language and purposeful sentence variation, preserves qualifications, and adds no invented experience or decorative detail. |
| Assemble independently drafted beats into one paper | Preserves each beat's unique contribution, removes repeated setup and mini-conclusions, and writes joins that create one continuous argument. |
| Test an apparently clear paper with a fresh technical reader | The reader reconstructs the message, decisive support, implication, and uncertainty without seeing the writer's contract; a material misreading yields a located issue and a targeted retest on the changed artifact. |
| Explain the same supported result top-down and by re-earning it | Both preserve the evidence, but their beat order, transitions, and attention curve visibly follow the declared proof direction. |
| Present a detailed system with a relationship diagram | Uses a low-noise diagram with an obvious reading path while retaining technical depth in prose, labels, and appendices rather than duplicating it. |
| Compile an executive summary from a stable technical body | Every material summary claim traces to descendant claims or declared derivation; no new evidence, concept, or dropped qualification appears only in the summary. |
| Match a supplied author sample | Preserves recurring choices in formality, vocabulary, and cadence without copying distinctive passages, stereotyping dialect, or reproducing errors that obstruct meaning. |
| Defend a methodology for an assurance review | Preserves assumptions, calculation paths, sensitivity, limitations, and open issues rather than replacing the mechanism with a compliance conclusion. |
| Strengthen a commissioned position while preserving headings | Retains the requested hierarchy and useful case; narrows unsupported premises and includes material qualifications. |
| Revise one challenged finding in an otherwise stable long report | Recompiles the affected subtree and ancestor synthesis, preserves unrelated branches, and repeats proofreading where the reading surface changed. |
| Two publications repeat one vendor estimate | Records the common origin and does not count them as independent corroboration. |
| Revise a monthly assumption to annual | Updates dependent calculations, wording, figures, and exports; rejects earlier QA as stale. |
| Finish a report without an available Word renderer | Distinguishes structural checks from visual inspection; reports the unfinished check honestly. |
| An authoritative citation is irrelevant to the attached claim | Flags the support mismatch despite publisher prestige and a valid URL. |

Score outcome fidelity, unprompted message recall, support reconstruction, implication and uncertainty recovery, attention loss, accidental inference, supported material claims, coverage, citation accuracy, numerical consistency, preserved constraints, paragraph development, voice fit, stylistic repetition, material defects found, user correction burden, and resource use. Compare against the same cases and inputs before and after changes, using at least one technical white paper and one executive brief for a communication-workflow change. Keep reviewer context limited to the final artifact and intended audience/commission; calibrate judgment-based grading with the report owner's assessment. Do not use an AI detector or a single readability statistic as a writing-quality grader.

Method references: [GAO data reliability](https://www.gao.gov/products/gao-20-283g), [CEBMa rapid evidence assessments](https://cebma.org/resources/guidelines-reas-and-cats/), and [research-agent evaluation](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents). These motivate appraisal and evaluation practices; they are not automatic evidence sources for individual reports.

## Prose revisions

For a bounded prose comparison, hold the source facts and audience commission fixed. Check retained claims and qualifications as gates. Conceal version labels from readers, vary presentation order, and request located examples of clarity, specificity, continuity and reading burden rather than detector scores or preferred sentence-length statistics. Test unaided recovery of the message, mechanism, limits and any action separately from preference. Disclose whether reviewers are agents or intended human readers; distinguish a revision of one document from an independent author trial. Preserve failures and actual overhead when recorded. A local successful pair does not establish general effectiveness or cache savings.
