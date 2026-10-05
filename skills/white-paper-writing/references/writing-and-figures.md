# Writing and exhibits

For compact projects, record message, reader movement, outline and consequential dependencies in planning/plan.md. References below to message.json, nodes, sequence or disclosure describe the full-workflow representation; use the corresponding plan section without creating a graph. Evidence and figure requirements remain shared.

## Message and proof direction

Write the `planning/message.json` contract before outlining prose. The communicative thesis is the sentence the reader should retain; the analytical synthesis is what the evidence supports. Keep them aligned without treating them as the same artifact. Define the reader's starting state, intended end state, and the tension that makes movement between them necessary.

Choose how the body earns the message. `top_down` moves from thesis through reasons and mechanisms to evidence. `bottom_up` lets observations and mechanisms accumulate into the conclusion. `re_earning` orients with the communicative thesis, develops the body bottom-up, and returns to the thesis with fuller meaning. The direction governs the whole document; do not let individual agents silently reset it.

## Narrative beats

The support graph and reading order are different views. Parent and dependency edges explain why the message is true; `sequence` stages how the reader encounters it. Give every beat one rhetorical role, one genuinely new contribution, a reader outcome, and a handoff that creates the reason to continue. Use `orient`, `define`, `demonstrate`, `complicate`, `compare`, `resolve`, `transition`, and `conclude` deliberately rather than turning every beat into another assertion-plus-list. In `planning/architecture.md`, mark which valid material is essential to the main path, supporting, optional, or archival; plan emphasis and scan order before layout QA. Existing beat outcomes, new information, visual roles, and budgets carry the local execution.

Move from given information to new information. Before first substantive use, introduce any concept, entity, acronym, metric, variable, framework, product, or mechanism the target reader cannot reasonably be expected to know. Give the identity, function, and context needed at that point; do not rely on a later section to make an earlier sentence intelligible. Keep canonical terminology stable unless a distinction is intentional and explained.

Treat recurrence as purposeful. Briefly remind only when distance makes recall uncertain; otherwise reinterpret an earlier fact, use it in a new decision, or leave it established. Do not give every section its own miniature introduction and conclusion. The manuscript should feel like one continuous act of reasoning, not a collection of complete agent responses.

## Compile the manuscript

Compile in distinct layers:

1. **Form the message:** define the thesis, tension, reader movement, and proof direction.
2. **Build support:** decompose and validate evidence, claims, concepts, and calculations in whatever analytical direction the work requires.
3. **Stage beats:** order rhetorical contributions for the chosen proof direction. Use `tree_workflow.py disclose` to inspect each beat's support ancestors, narrative neighbors, established context, and last-mention distance.
4. **Draft locally:** write each beat as developed prose that adds its assigned information and hands attention forward. Keep claims, qualifications, citations, and registered values together.
5. **Stitch globally:** delete repeated setup and mini-conclusions, write the joins, alternate abstraction with concrete detail, and control pace. Then write the opening, conclusion, and title against the stable body.

Do not expose every beat as a heading or force uniform depth. Prefer developed prose over enumerative lists when ideas depend on one another. Lead with substance, link evidence to inference explicitly, and keep qualification close to the claim. A paragraph should change the reader's understanding, not merely inventory facts.

## Technical disclosure

Preserve definitions, system or data boundaries, methods, inputs, transformations, baselines, assumptions,
uncertainty, robustness checks, failure modes, implementation constraints, and unresolved questions when they
matter to the selected purpose. Make artifacts and interfaces locatable enough for the intended internal
reader to reproduce, challenge, or extend the work. Compress repetition and non-decisive history, not the
technical detail required to understand how the answer was produced.

Use appendices for supporting depth that would interrupt the main reasoning, but do not exile a decisive
qualification or mechanism from the body. An executive summary may orient the reader; it must be compiled
from the stable technical body and cannot substitute for it.

## Claims in the manuscript

Use citations such as `[@S01]` or `[@S01, p. 12; @S02]`. Source IDs must match the source register. Keep a verified `report_excerpt` for every emitted material claim and include any `required_qualification` in the same paragraph. After revisions, update the excerpt only after rechecking the meaning and evidence.

This exact-excerpt check verifies declared coverage; the evidence reviewer must still detect unregistered claims and overbroad statements elsewhere. Examples and interpretations should be identified appropriately rather than burdened with irrelevant citations.

## Figures

Add a figure only when it clarifies a material relationship better than prose or a small table. Record its question, input table, transformation, output file, units, period, and source note in `figures/register.json`. Produce the exhibit from stable analysis outputs. Preserve native vector output for print when appropriate and a raster companion for Word.

For processes, systems, dependencies, and decision paths, sketch the information structure in Mermaid first when the tool is available. Keep the editable Mermaid source, then render a publication asset. Minimalist means low visual noise, restrained color, strong grouping, and a single obvious reading path—not sparse information. Let the diagram map relationships while prose explains mechanism, evidence, and consequence; do not duplicate the same content in both.

Use honest axes, consistent units, readable labels at final size, and explicit distinction between observations and modeled paths. Connecting modeled monthly values is acceptable when labeled; connecting sparse observations must not imply unobserved continuity. Explain uncertainty and source limitations at the level relevant to the reader.

Use the project's requested brand, not a hardcoded business identity. Typography, palette, logo, language, and disclosure preferences belong in project assets and the brief. Reuse `assets/report_chart_style.py` as an optional neutral starting point.

Treat the document as a performative interface: its layout should help the reader orient, inspect, compare, and return to the argument. Use a quiet surface with rich depth—clear typographic hierarchy, shallow visible headings, generous space at conceptual turns, consistent exhibit grammar, compact callouts only for genuine orientation, and appendices for inspectable depth. Visual emphasis must follow the attention plan rather than decorate the page.

## Revision order

Revise the semantic graph before polishing its surface:

1. Message pass: test the communicative thesis, tension, reader transformation, and chosen proof direction against the supported answer.
2. Support pass: test whether each leaf is supported and whether the graph establishes every synthesis. Resolve contradictions, gaps, and weak derivation.
3. Narrative pass: read in `sequence`, checking that every beat adds something, follows from what precedes it, and creates a useful handoff. Remove unnecessary recurrence and repair the attention curve.
4. Recompile: after changing a node, concept, or claim, redraft the smallest affected scope and restitch its neighboring beats. Do not rewrite stable, unrelated passages merely for uniformity.
5. Surface edit: once meaning and movement are stable, apply [human-writing.md](human-writing.md) to edit paragraphs and sentences for development, continuity, voice, diction, rhythm, and audience fit.

Treat changes to causality, quantifiers, attribution, numbers, units, or uncertainty as analytical edits that reopen the affected subtree. Do not let a copyedit silently strengthen a claim. Keep the canonical source authoritative and regenerate exports after accepted edits.

## Proofreading

Proofreading is a freeze-stage check, not another recursive rewrite. First run whole-document consistency checks for names, terminology, abbreviations, symbols, equations, code identifiers, dates, units, registered numbers, citations, cross-references, captions, table columns, and heading levels. Then read the manuscript linearly in reader order for grammar, spelling, punctuation, missing words, local ambiguity, and transition defects. Finally inspect each rendered format page by page for breaks, clipping, equations, code, tables, figures, notes, links, and references.

Correct surface defects directly. If proofreading reveals a factual, evidentiary, structural, or meaning-changing problem, stop treating it as a copyedit, reopen the affected subtree, recompile it, and repeat the relevant proof and review scope.
