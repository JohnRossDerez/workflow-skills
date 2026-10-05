## Abstract

The `white-paper-writing` skill helps an agent explain R&D to engineers, analysts and technical reviewers. The author plans the reader's path, records the evidence behind material claims and produces requested formats from one manuscript. Ordinary papers use compact planning; a fuller dependency graph supports substantial coordination. Reviewers still have to judge whether the argument is true and understandable. [@S01; @S02]

A bounded comparison exercised the compact and prior workflows, then required authors to revise their papers after a real source correction. Both technical cases passed their final evidence and reader checks. One case per audience and condition cannot establish general effectiveness, graph superiority or cost savings. This paper describes that evidence and a subsequent prose-editing revision; the revision has not undergone the original comparative author trial. [@S03; @S06; @S11]

## From research notes to a reader's argument

An investigation's chronology rarely gives a new reader the best route through its findings. The reader needs to know what was done, how the result arose and where its interpretation stops. Even a well-cited paper can omit a premise or use a source that supplies background without supporting the conclusion. The skill therefore keeps evidence support and reading order separate: evidence records locate the basis of a claim, while the plan decides what the reader must understand before encountering it. [@S02]

The author chooses investigation, decision, explanation or argument, then adjusts depth to the audience. A builder may need implementation detail; a researcher may need to challenge the method. Here, the purpose is explanation for Python and AI engineers assessing whether the workflow suits their own R&D communication. [@S01; @S08]

## Proportionate planning and explicit support

A compact project starts with a reader brief, a document plan and one canonical `report.md`. The brief establishes purpose, audience, scope and constraints. In the plan, the author orders the supported argument; prose or a small table can do this without a node for every paragraph. [@S02]

The evidence ledger separates sources, claims and passage links. Sources identify provenance, limitations and archives. Claims distinguish observations from interpretations and record the wording emitted in the paper. Passage links locate support and describe how it bears on the claim. Numbers, calculations and figures receive records when used; empty conditional registers are allowed. Records focus on consequential assertions. [@S02; @S07]

For example, a source reporting selected test passes supports a claim about those tests. Production reliability requires further evidence. A ledger makes that distinction available for inspection, but its existence does not settle the inference. The reviewer must assess source fit, independence, counterevidence and qualification. [@S02; @S07]

A full workflow adds executable dependency and coordination records when parallel authorship or repeated impact queries justify maintaining them. Technical complexity, length and multiple export formats alone do not justify the graph. Existing projects without a workflow setting retain their full contract; initialization refuses an implicit switch. The lead owns the integrated message and shared evidence. Bounded workers can research or review without another agent runtime or a graph created solely for delegation. These rules do not establish context or cache savings. [@S01; @S02]

## Editing the argument and its sentences

After stitching the manuscript, the author performs a located prose-editing pass. The editor reads each affected paragraph in context, identifies a burden such as a delayed verb or several new concepts at once, and edits that passage for a stated reason. An observation may be direct; a mechanism may need more space; an inference retains its qualification. The skill keeps a consistent reader relationship rather than prescribing a tone change every sentence. [@S11]

Sentence length is a diagnostic clue. A long sentence can preserve a useful relationship between clauses; several short sentences can repeat setup without advancing the argument. The editor records representative before/after passages in existing editorial notes and rechecks changed meaning against the sources. A suitable available exemplar can inform rhythm or depth without supplying facts or copied wording. This is a practical editing mechanism whose benefit still needs testing across documents and readers. [@S11]

## Building and reviewing the delivered version

Python helpers and Pandoc build requested formats; PDF also requires a supported TeX engine. Preflight checks records and local paths. The build parses the canonical Markdown manuscript, substitutes registered number tokens and resolves registered citations into one document for the requested formats. Requested formats are staged before output replacement, so a failed format leaves prior outputs in place. This does not promise an atomic filesystem publication of all files. [@S04]

Fingerprints cover the manuscript, configuration and tracked planning, evidence and source artifacts. Review records bind notes to that content and to generated artifact hashes. Changed sources or output bytes prevent an old review from satisfying current release controls. Hashes detect stale controls; they cannot establish that a reviewer reasoned correctly. [@S04; @S09; @S10]

Evidence reviewers check consequential claims and their support. Editorial review checks the argument, development and language. A fresh reader receives only the audience, commission and reading artifact, then explains what they understood and where reading failed. PDF review inspects every rendered page. A structural validator supplements those judgments. A pass must describe an actual completed check. [@S07]

## What the prior evaluation established

The comparison contained {{number:N01}} initial author cases. The technical cases used full and compact workflows; the executive cases used direct and compact drafting. The two technical projects and the compact executive project were managed, while the direct brief used manual review. Each author used a source-check worker, then revised the same document after the correction. Revisions were not additional independent trials. The baseline executive author legitimately chose its direct route, so only the technical pair compared full with compact planning. [@S03]

The correction exposed an engineering extraction whose legacy API and command line stopped honoring changed live repository settings. An earlier favorable appraisal was superseded after reproduction; the frozen reference shared the defect, and original engineering grades remained unchanged. Authors had to revise their conclusions without treating supplemental checks as new trials or evidence of instruction-package superiority. Retaining the earlier no-defect implication would fail this revision task. [@S03]

Independent initial review found a provenance error in the compact technical paper: assigned writing instructions had been described as shared raw-input evidence. The author removed the dependent claim. Both executive drafts also required clarification. Some missing-link findings arose from evaluator copies losing package context and were withdrawn after inspecting the delivered locations. The record retains these dispositions so harness errors do not become author failures. [@S03]

| Technical case | Initial records | Revised records | Final review |
|:--|--:|--:|:--|
| Prior full workflow | {{number:N02}} | {{number:N03}} | Evidence and reader checks passed |
| Compact workflow | {{number:N04}} | {{number:N04}} | Evidence and reader checks passed |

Counts cover registered planning, evidence, control, research, analysis and draft files, excluding source archives, outputs, caches, QA notes and the figure register. Fewer records do not prove lower cost or better prose. All managed cases rejected stale controls after the tracked source changed, and all final documents passed independent evidence and fresh-reader checks. These were agent-based reviews and reader checks, not tests with intended human readers. [@S03; @S06]

Each writing helper suite separately passed {{number:N05}} structural and compatibility checks. Synthetic review fixtures did not test comprehension. The evaluation delivered Markdown, so it did not establish PDF or Word visual fidelity. The PDFs produced for this self-description receive separate checks and do not extend that experiment retrospectively. [@S05; @S03]

## When to use it and what to test next

Compact planning is a reasonable starting point for an internal R&D paper requiring inspectable support and revisions. Use the fuller representation when actual coordination or impact queries justify it; a small local edit can apply relevant checks directly. The author and reviewers remain responsible for the judgments those records expose. [@S01; @S02]

The comparison used one case per audience and condition, cooperative isolation and incomplete worker-inclusive usage and cache accounting. It cannot establish average communication quality or causal efficiency. To evaluate the prose revision, hold source facts and audience fixed, check retained claims and qualifications, then ask readers to locate clarity and continuity problems in concealed-label versions. Test unaided recovery of the message separately from preference. Agent-only judgments must be disclosed, and a single successful pair remains a local appraisal. [@S03; @S11]

### Source scope

The sources are local artifacts archived with this paper. Instructions and code establish design and implemented controls; evaluation records establish bounded observations. This self-description supplies no independent effectiveness estimate.
