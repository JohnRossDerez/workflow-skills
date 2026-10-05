# Production and release QA

Compact and full projects share the evidence, artifact and review-freshness checks below. For compact documents, editorial passes use the plan instead of graph/message records. A changed claim reopens its affected prose, synthesis and reviews; full projects can use graph invalidation. New projects in both workflows require a fresh reader.

## Build prerequisites and behavior

Helpers need Python 3.10+ and Pandoc; PDF also needs the selected TeX engine. Word generation uses Pandoc's default document or a project-owned `reference_doc`. PDF styling can use a project-owned `pdf_header`. English PDFs use TeX's default English support; other languages may require the relevant TeX language packages and fonts. No API key, model SDK, or separate orchestration service is required.

Preflight checks records and paths. Unsupported or unverified emitted claims are warnings during drafting and errors at release. A build is allowed for review before evidence is complete, but it is not a release pass. All requested formats must build before output replacement. Run analysis scripts separately before the build; the helper does not execute source-provided code automatically.

The build parses Markdown with Pandoc, substitutes registered numbers, resolves citation nodes against the source register, and creates a numbered bibliography with source URLs and retrieval dates. It emits all formats from this single parsed document. Markdown delivery uses GitHub-flavored Markdown with pipe tables and HTML reference anchors, rather than Pandoc-only fenced divs. This compact citation style works with the older Pandoc available here without an extra citeproc executable. Markdown retains relative figure paths: include each referenced asset at the corresponding path in the delivery bundle, or rewrite the link to a verified location before handoff. A Markdown file with broken local figures is not a complete artifact. Arbitrary CSL styles and journal-specific formats require an explicitly configured alternative build and equivalent audits; they are not advertised as built-in features.

## Required review passes

1. `evidence`: check material-claim coverage, original passages, source fit, attribution, counterevidence, assumptions, formulas, units, temporal bases, and consequential rounding. Confirm that the selected mode's acceptance questions are answered. Reproduce decisive numerical results and verify that figures match their data. Source counts alone do not establish completion.
2. `editorial`: perform and document distinct message, support, narrative, and surface passes. Check that the communicative thesis matches the supported answer; the selected proof direction produces the intended reader movement; every beat adds information and hands attention forward; concepts arrive before use; support reconstructs each synthesis; and the stitching pass removes repeated setup, duplicated detail, and local mini-conclusions. Include representative located prose diagnoses, edits and their reader-relevant reasons in these same notes; for a clean small draft, record what was inspected rather than manufacturing edits. Then apply the human-writing standard and proofread in narrative order for paragraph development, voice, concrete diction, rhythm, transitions, terminology, grammar, spelling, names, symbols, equations, code identifiers, dates, units, headings, captions, cross-references, and bibliography consistency. Protect attribution, causal language, uncertainty, and registered numbers; meaning-changing findings reopen graph revision.
3. `cold_reader` when `reader_test_required` is true: after semantic revision, give an independent fresh reader the intended audience and commission plus one actual reader-facing build artifact. Do not give the reader `planning/message.json`, the support graph, earlier drafts, or the author's diagnosis. Ask neutrally what the main message is, what supports it, what action or implication follows, what uncertainty remains, what they inferred accidentally, and where attention or understanding failed. Preserve the unprompted answers in `qa/cold-reader.md`; then the editor compares them with the private message, stakes card, and evidence. Record located material failures in `qa/issues.json`, assign the smallest revision scope, rebuild, and retest. A pass means the test revealed no unresolved material misunderstanding; it does not certify factual truth. The review must be independent, cannot be waived, and is bound to the current content and artifacts.
4. `visual:pdf` and/or `visual:docx`: inspect every page of each requested rendered format. Check clipping, aspect ratios, readable figures and source notes, page breaks, orphan headings, tables, headers, footers, links, and reference formatting. Also check that emphasis follows the attention plan, whitespace marks conceptual turns, diagrams have one obvious reading path, and detail remains accessible without making the surface noisy. Record page-specific notes and the renderer used. For DOCX use an available office renderer; XML/text extraction is not a visual inspection.
5. `cross_format` when multiple formats are requested: compare wording, section ordering, figures, citations, and numbers after extraction. Shared generation reduces divergence but does not prove that a writer preserved every element. Account for harmless layout differences and document any unsupported elements.

Write each pass's substantive notes under `qa/`, including scope, findings and dispositions, limitations, and verdict. For visual reviews, list all pages checked. A separate reviewer is useful for material evidence; record `method: self` when one session performed a separate pass itself. Do not claim independence from adopting another role name.

## Record actual checks

After the final build and actual review, bind each result to that version:

```bash
python3 <skill-directory>/scripts/record_review.py <project> --kind evidence --reviewer "analyst" --method independent --notes-file qa/evidence-review.md --status pass
python3 <skill-directory>/scripts/record_review.py <project> --kind editorial --reviewer "editor" --method self --notes-file qa/editorial-review.md --status pass
python3 <skill-directory>/scripts/record_review.py <project> --kind cold_reader --reviewer "fresh reader identity" --method independent --notes-file qa/cold-reader.md --status pass
python3 <skill-directory>/scripts/record_review.py <project> --kind visual:pdf --reviewer "editor" --method rendered --notes-file qa/pdf-review.md --status pass
python3 <skill-directory>/scripts/record_review.py <project> --kind visual:docx --reviewer "editor" --method rendered --notes-file qa/docx-review.md --status pass
python3 <skill-directory>/scripts/record_review.py <project> --kind cross_format --reviewer "editor" --method tool --notes-file qa/format-comparison.md --status pass
python3 <skill-directory>/scripts/validate_report_project.py <project> --release
```

Use only required kinds for the requested formats and project reader-test setting; older projects can opt in by setting `reader_test_required: true`. A correction changes tracked content and invalidates prior records; rebuild, check the changed scope and retained findings, and record a new review. Even an identical-content rebuild can change binary artifacts, so reviews must cover the actual files handed off.

For an unavailable renderer, record `not_run` with `method unavailable`, explain the limitation, and deliver a review draft when appropriate. If the user already authorizes delivery with that artifact-check limitation, record `waived` with `--authorization` describing the actual direction. A waiver is reported as a limitation, never a performed check. This is not a new approval gate: do not ask again when the session already supplies authorization. Evidence, editorial, and configured cold-reader review are core validity checks; a work-in-progress artifact can be handed off explicitly as such when they are incomplete.

## What automated checks establish

The validator checks register shape and ID integrity, resolvable paths, declared emitted claims, required qualification presence, evidence-link status, numeric display tolerance, citation keys, figure registration, outstanding issues, pending configured gates, build fingerprints, review fingerprints, notes integrity, and the configured cold-reader review's freshness and independence. It reports all known errors and fails closed on unreadable/malformed records.

It does not prove search completeness, semantic entailment, whether every factual sentence was registered, computation correctness, source independence, truthful reviewer attestations, or visual quality. Those remain explicit review duties. Release results should say "controls passed" and identify any limitations rather than claiming the report is factually certified.
