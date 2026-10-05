# Writing and exhibits

For compact projects, record message, reader movement, outline and consequential dependencies in planning/plan.md. References below to message.json, nodes, sequence or disclosure describe the full-workflow representation; use the corresponding plan section without creating a graph. Evidence and figure requirements remain shared.

## Message and proof direction

Write the `planning/message.json` contract before outlining prose. The communicative thesis is the sentence the executive should retain; the analytical synthesis is what the evidence supports. Keep them aligned without treating them as the same artifact. Define the executive's starting state, intended end state, and the tension that makes attention or action necessary.

Choose how the brief earns the message. `top_down` moves from answer or requested action through decisive reasons to evidence and is the default. `bottom_up` lets observations and mechanism accumulate into the conclusion when early compression would mislead. `re_earning` orients on the first page, proves the message through the body, and returns to action with fuller meaning. The direction governs the whole brief; do not let individual agents silently reset it.

## Narrative beats

The support graph and reading order are different views. Parent and dependency edges explain why the message is true; `sequence` stages how the executive encounters it. Give every beat one rhetorical role, one genuinely new contribution, a reader outcome, and a handoff that creates the reason to continue. Use the roles deliberately rather than turning every beat into another assertion-plus-list. In `planning/architecture.md`, mark which valid material is essential to the main path, supporting, optional, or archival; plan emphasis and scan order before layout QA. Existing beat outcomes, new information, visual roles, and budgets carry the local execution.

Move from given information to new information. Before first substantive use, introduce any concept, entity, acronym, metric, variable, framework, product, or mechanism the target reader cannot reasonably be expected to know. Give the identity, function, and decision context needed at that point; do not rely on a later section to make an earlier sentence intelligible. Keep canonical terminology stable unless a distinction is intentional and explained.

Treat recurrence as purposeful. Briefly remind only when distance makes recall uncertain; otherwise reinterpret an earlier fact, use it in a decision, or leave it established. Do not give every section its own miniature introduction and conclusion. The brief should feel like one continuous act of judgment, not a collection of complete agent responses.

## Compile the manuscript

Compile in distinct layers:

1. **Form the message:** define the thesis, tension, reader movement, proof direction, and requested action when one exists.
2. **Build support:** validate evidence, claims, concepts, alternatives, and consequences without prematurely compressing them.
3. **Stage beats:** order rhetorical contributions for the chosen direction. Use `tree_workflow.py disclose` to inspect support ancestors, narrative neighbors, established context, and last-mention distance.
4. **Draft locally:** write each beat as developed prose that adds its assigned information and hands attention forward. Translate technical measures into consequences without changing meaning.
5. **Stitch globally:** delete repeated setup and mini-conclusions, write the joins, control pace, and then make the opening answer, requested action, conclusion, and title agree with the stable body.

Do not expose every beat as a heading or reproduce the research process in miniature. Prefer developed prose over enumerative lists when ideas depend on one another. Use a shallow visible structure, concrete subjects and verbs, compact analytical passages, and exhibits that answer one executive question. A paragraph should change the reader's understanding or decision state, not merely inventory facts.

## Executive reading surface

The opening screen or page should make the answer or decision state, why it matters, and requested action
recoverable without reading the appendix. For a decision, identify the owner, recommendation, alternatives
including no action, decisive reasons, horizon, material risks, and conditions that could reverse the choice.
For an investigation or explainer, state the current answer, consequence, uncertainty, and next information
or action. Do not invent a call to action when the selected purpose does not require one.

Move non-decision-relevant method, derivations, metric inventories, and specialist diagnostics to a compact
appendix or linked technical source. Do not hide a decisive qualification, counterargument, mechanism, or
risk there. The brief may be shorter than its evidence trail; it may not be more certain.

## Claims in the manuscript

Use citations such as `[@S01]` or `[@S01, p. 12; @S02]`. Source IDs must match the source register. Keep a verified `report_excerpt` for every emitted material claim and include any `required_qualification` in the same paragraph. After revisions, update the excerpt only after rechecking the meaning and evidence.

This exact-excerpt check verifies declared coverage; the evidence reviewer must still detect unregistered claims and overbroad statements elsewhere. Examples and interpretations should be identified appropriately rather than burdened with irrelevant citations.

## Figures

Add a figure only when it clarifies a material relationship better than prose or a small table. Record its question, input table, transformation, output file, units, period, and source note in `figures/register.json`. Produce the exhibit from stable analysis outputs. Preserve native vector output for print when appropriate and a raster companion for Word.

For processes, systems, dependencies, and decision paths, sketch the information structure in Mermaid first when the tool is available. Keep the editable Mermaid source, then render a publication asset. Minimalist means low visual noise, restrained color, strong grouping, and a single obvious reading path—not sparse information. Let the diagram map relationships while prose explains consequence and choice; do not duplicate the same content in both.

Use honest axes, consistent units, readable labels at final size, and explicit distinction between observations and modeled paths. Give each exhibit one executive question and a takeaway that the displayed evidence actually supports. Prefer a small comparison table or decision-relevant chart over a dashboard. Explain uncertainty and source limitations at the level needed to avoid a wrong decision.

Use the project's requested brand, not a hardcoded business identity. Typography, palette, logo, language, and disclosure preferences belong in project assets and the brief. Reuse `assets/report_chart_style.py` as an optional neutral starting point.

Treat the brief as a performative interface: its layout should help the executive orient, compare, decide, and return to the evidence. Use a quiet surface with rich depth—clear typographic hierarchy, shallow headings, generous space at conceptual turns, consistent exhibit grammar, compact callouts only for genuine orientation, and appendices or links for inspectable depth. Visual emphasis must follow the attention plan rather than decorate the page.

## Revision order

Revise the semantic graph before polishing its surface:

1. Message pass: test the communicative thesis, tension, executive transformation, requested action, and proof direction against the supported answer.
2. Support pass: test whether the graph establishes every synthesis and decision condition. Resolve contradictions, gaps, and weak derivation.
3. Narrative pass: read in `sequence`, checking that every beat adds something, follows from what precedes it, and creates a useful handoff. Remove unnecessary recurrence and repair the attention curve.
4. Recompile: after changing a node, concept, or claim, redraft the smallest affected scope and restitch its neighboring beats. Do not rewrite stable, unrelated passages merely for uniformity.
5. Surface edit: once meaning and movement are stable, apply [human-writing.md](human-writing.md) to edit paragraphs and sentences for development, continuity, voice, diction, rhythm, and audience fit.

Treat changes to causality, quantifiers, attribution, numbers, units, or uncertainty as analytical edits that reopen the affected subtree. Do not let a copyedit silently strengthen a claim. Keep the canonical source authoritative and regenerate exports after accepted edits.

## Proofreading

Proofreading is a freeze-stage check, not another recursive rewrite. First run whole-document consistency checks for the recommendation or answer, requested action, owners, alternative names, terminology, abbreviations, dates, units, registered numbers, citations, captions, and headings. Then read linearly in executive order for plain language, skimmability, unexplained jargon, grammar, spelling, punctuation, missing words, ambiguity, and transition defects. Finally inspect each rendered format page by page, with special attention to first-page sufficiency, hierarchy, whitespace, tables, figures, notes, links, and references.

Correct surface defects directly. If proofreading reveals a factual, evidentiary, structural, or meaning-changing problem, stop treating it as a copyedit, reopen the affected subtree, recompile it, and repeat the relevant proof and review scope.
