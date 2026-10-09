# Verification

Run the writing helper suites from the repository root. They use Python's standard library and Pandoc; rendered PDF builds also need a supported TeX engine.

```bash
python3 skills/white-paper-writing/scripts/test_report_workflow.py
python3 skills/white-paper-writing/scripts/test_compact_workflow.py
python3 skills/white-paper-writing/scripts/test_review_recording.py
python3 skills/executive-brief-writing/scripts/test_report_workflow.py
python3 skills/executive-brief-writing/scripts/test_compact_workflow.py
python3 skills/executive-brief-writing/scripts/test_review_recording.py
```

The review-recording suites use only the standard library. They exercise the actual recorder with a synthetic persisted build fixture: separate notes stay bound after journal appends, and journal path aliases are rejected without mutation. They do not establish rendering or semantic review quality. Without Pandoc, the full-workflow suites skip their tests and the compact suites run only initialization checks; report executed and skipped counts separately.

The examples are managed compact projects. To check their records and current-artifact freshness:

```bash
python3 skills/white-paper-writing/scripts/validate_report_project.py \
  examples/white-paper --release
python3 skills/executive-brief-writing/scripts/validate_report_project.py \
  examples/executive-brief --release
```

These checks do not independently reperform the recorded source review or reader test. To revise a project, update its evidence and affected manuscript, rebuild, perform actual reviews and record the new results. Updating fingerprints alone is insufficient.

The refactoring inventory helper is read-only:

```bash
python3 skills/repository-refactoring/scripts/inventory_repository.py \
  /path/to/repository --format markdown
```

It reports candidate entry points and coarse absolute-import relationships. Relative imports, dynamic imports and runtime behavior still require inspection.

## Initial publication-copy checks

Both writing helper suites passed 48 full-workflow and 16 compact-workflow checks each in this copied repository: 128 checks in total. Both managed PDF examples passed release validation. The four skill metadata checks passed and skill file hashes matched the reviewed candidates. Navigation links were checked separately from verbatim evidence archives, whose original relative links retain their source context. The package-extraction example passed eight checks at each of its baseline, reference legacy and reference canonical entry points; its incomplete candidate failed as expected. These checks establish the distributed examples and helper behavior, without extending the earlier author experiment.

## Researched sample PDF refresh — 2026-10-09

Both self-description PDFs were rebuilt with the current helpers, Pandoc 3.12.1 and MiKTeX pdfTeX. The technical sample has two main pages and one reference page; the executive sample has one main page and one reference page. The executive scope covers any topic requiring researched evidence. Targeted web research added Digital.gov writing and paraphrase-testing guidance, Anthropic AI workflow guidance (technical sample) and Gao et al.'s 2023 ALCE research. These explain design rationale and concrete failure audits; they do not validate the complete skills or estimate current-model failure rates. Selective extracts, precise locators, source-family limits and search/stopping notes accompany the manuscripts.

Each sample received an independent original-source review (gpt-6-sol/high), a fresh agent reader (gpt-6-sol/medium), a separate editorial self-review and inspection of every rendered page. Evidence review prompted disclosure of initial trial defects, design-framed editing language and a narrower historical boundary. The notes preserve those findings and their corrections. Readers recovered the message and found the audits actionable; they retained minor questions about workflow thresholds and pass criteria. The final white-paper cleanup removed only a redundant citation after its reader test, with no prose change. No comparative author trial or intended-human-reader test was performed.

Actual PDF citation destinations all resolve. Both release validators passed with zero errors or warnings. Sample headers defer hyperlink setup, label bibliography items and separate the references heading from its list. Example text uses LF through `.gitattributes` so byte-based content and review fingerprints survive Windows and Unix checkouts. The build manifests and actual review records accompany the PDFs; these checks apply to the displayed samples, not general writing quality.

A follow-up AI engineering correction replaced the technical paper's generic NASA analogy with Anthropic's bounded-workflow and evaluator-criteria guidance. The technical paper received a new independent source check, a new fresh reader, editorial review and inspection of all three final pages; the executive artifact was unchanged. The removed analogy remains only as superseded evidence history.
