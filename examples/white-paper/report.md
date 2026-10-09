## Abstract

The `white-paper-writing` skill turns technical research into an explanation that engineers can inspect: a clear reader path, claims tied to source passages, and reviews of the delivered document. Its strongest rationale is practical: separate understanding, evidence support and version freshness so one cannot stand in for another. External guidance supports these design choices; it does not establish the skill's overall effectiveness. [@S01; @S07]

## What the workflow adds

Ordinary papers use a reader brief, a short plan and one manuscript. The author records consequential claims and the passages supporting them; numbers and figures get records when needed. A full dependency graph is reserved for substantial coordination. Technical difficulty or document length alone does not justify it. [@S01; @S02]

For example, a test log can support “this case passed these checks.” It cannot by itself support “the system is reliable in production.” The reviewer checks that inference; a valid citation or completed register cannot settle it. A separate editing pass targets located reading problems and checks that the claim's scope is preserved. [@S07; @S11]

## Why these choices may help

**Reader fit.** Digital.gov recommends matching the audience's knowledge and organizing the answer up front. Its paraphrase-testing guidance asks readers to explain meaning in their own words, without being corrected during the test. This gives the workflow a concrete clarity check: can a reader recover the conclusion and its limits unaided? An agent reader is a preliminary check, not evidence of human comprehension. [@S12; @S13]

**Bounded AI tasks.** Anthropic's agent-engineering guidance recommends simple workflows and clear criteria for evaluator feedback. Applied here, separate evidence checking, prose editing and reader testing into bounded tasks; add orchestration only when it improves the result. This is practitioner guidance, not controlled evidence that this skill works. [@S16]

**Separate quality questions.** Gao and colleagues' ALCE research evaluates fluency, factual correctness and citation quality separately and found incomplete support in its 2023 benchmark. That distinction motivates checking both whether a cited passage supports a claim and whether important assertions have support. It supplies no failure-rate estimate for current models or this skill. [@S15]

\newpage

## What reviewers should audit

These checks turn the rationale into review work; they are proposed applications of the references and the skill's review contract. [@S07; @S13; @S15]

| Failure case | Concrete audit |
|:--|:--|
| A real citation supports a weaker claim | Open the original passage; compare population, conditions and causal strength with the paper's wording. |
| Compression changes the conclusion | Compare the abstract with the supporting section: retain any assumption or exception that changes the result. |
| A reviewer repeats the author's framing | Give a fresh reader only the document and audience; ask for the conclusion, limits and implication before showing the plan. |
| Correct evidence belongs to an old version | Check which source changed, revisit dependent claims and inspect the exact PDF being released. |

Managed builds bind review records to tracked content and artifact hashes. This detects stale reviews, not sound reasoning. Evidence inspection, reader checks and rendered-page review remain separate jobs. [@S07]

## What has actually been demonstrated

A local comparison covered {{number:N01}} initial author cases across technical and executive writing. Three of the four initial drafts needed corrections to evidence attribution or scope. After a source correction and revisions, final agent evidence reviewers and fresh agent readers passed the documents. One case per audience and condition cannot establish average quality, savings or human-reader benefit. The comparison delivered Markdown and does not establish PDF layout quality. This PDF is a separate demonstration. [@S03]

Start compact when a paper needs inspectable support and revisions. Add coordination machinery only when maintaining dependencies earns its effort. Judge the result by supported claims and unaided reader understanding, rather than the amount of workflow paperwork. [@S01; @S02]

\newpage
