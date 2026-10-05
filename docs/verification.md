# Verification

Run the writing helper suites from the repository root. They use Python's standard library and Pandoc; rendered PDF builds also need a supported TeX engine.

```bash
python3 skills/white-paper-writing/scripts/test_report_workflow.py
python3 skills/white-paper-writing/scripts/test_compact_workflow.py
python3 skills/executive-brief-writing/scripts/test_report_workflow.py
python3 skills/executive-brief-writing/scripts/test_compact_workflow.py
```

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

## Publication-copy checks

Both writing helper suites passed 48 full-workflow and 16 compact-workflow checks each in this copied repository: 128 checks in total. Both managed PDF examples passed release validation. The four skill metadata checks passed and skill file hashes matched the reviewed candidates. Navigation links were checked separately from verbatim evidence archives, whose original relative links retain their source context. The package-extraction example passed eight checks at each of its baseline, reference legacy and reference canonical entry points; its incomplete candidate failed as expected. These checks establish the distributed examples and helper behavior, without extending the earlier author experiment.
