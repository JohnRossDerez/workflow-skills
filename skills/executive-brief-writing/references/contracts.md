# Project records and contracts

These graph/control contracts apply to full projects. Compact projects use the shared evidence, build and QA contracts, with brief.md and plan.md replacing mandatory graph/message/control records; see compact-workflow.md.

The supplied helpers use UTF-8 JSON, Markdown, Python 3.10+, and Pandoc. JSON avoids an additional YAML/CSV parsing dependency. Records are editable artifacts owned by the lead, not an autonomous database or another agent runtime. IDs are unique within a register and match `[A-Za-z][A-Za-z0-9_-]*`.

## Project and manuscript

`project.json` contains `schema_version: 1`, `mode`, `title`, `author`, `lang`, `depth`, `structure`, `approval_policy`, `gates`, and `formats`. New full projects set `reader_test_required: true`, which makes a fresh-reader comprehension review a release requirement; an absent field preserves older projects' release contract. It is a boolean, independent of the human approval policy. Short, low-risk work can use the lightweight path without a project. Optional `pdf_engine` is pdflatex/xelatex/lualatex; `pdf_header` and `reference_doc` name project-relative assets for PDF and Word styling. Store styling assets under `assets/` so they are fingerprinted. The brief holds human-readable scope and acceptance decisions. Use ISO full dates when known; omit unknown dates rather than inventing a day.

`planning/architecture.json` is the executable writing architecture graph. Version 3 retains the version-2 support fields and adds `rhetorical_role` (`orient`, `define`, `demonstrate`, `complicate`, `compare`, `resolve`, `transition`, or `conclude`), `new_information`, `handoff`, and `visual_role` (`none`, `map`, `mechanism`, `comparison`, `evidence`, or `decision`). Parent links form the support tree; dependencies, concepts, and claims form the support DAG; unique `sequence` values independently define the narrative reading order. This separation allows top-down, bottom-up, or re-earning arguments without confusing evidentiary support with presentation. At release every node is validated, every evidentiary leaf names a claim, and every substantive synthesis names descendant claims as its basis. Versions 1 and 2 remain readable under their original parent-first ordering but do not receive the communication-layer guarantees.

`planning/message.json` is required by architecture version 3. It records `schema_version: 1`, `status` (`planned` or `defined`), `reader_start`, `reader_end`, `communicative_thesis`, `central_tension`, and `proof_direction` (`top_down`, `bottom_up`, or `re_earning`). The communicative thesis is the sentence the reader should retain; it is not a substitute for the evidence-bound analytical synthesis. A release requires a defined message contract.

`planning/brief.md` holds the compact reader-stakes card: attention available, prior belief or investment, what earns trust, likely resistance or misreading, authority and feasible action, and the retention target. The existing message fields carry the selected thesis and reader movement; do not copy the whole card into `message.json` or add node fields for it. Give prose workers the card with their bounded disclosure window. `control/decisions.md` records materially different candidate framings, the selection reason, and later changes of direction; rejected framings do not enter node disclosure.

`planning/concepts.json` is the canonical registry for nontrivial concepts, acronyms, symbols, metrics, and frameworks that are unfamiliar to the audience, used unusually, essential, or easily confused. Each entry has `id`, `canonical_name`, `definition`, `aliases`, `assumed_known`, `prerequisite_ids`, and `introduced_at` (a node ID or null). Do not register ordinary vocabulary. An unfamiliar concept must have one introduction node; prerequisites and uses must appear no later than the nodes that depend on them. The scripts validate identity and order, while the semantic reviewer judges whether the definition is sufficient for the reader.

`control/orchestration.json` stores dated preferred model and concurrency policy. `control/agent-runs.json` records actual delegated role, model, effort, node IDs, artifacts, and completion or limitation. Model availability may change; these records document execution but never establish semantic quality.

`planning/voice.md` stores the optional project voice profile and its provenance, confidence, version, tone modulation, and runtime card. `Status: unset` means no voice should be inferred or applied. A populated profile is a fingerprinted writing input, not evidence for factual claims and not permission to impersonate a person deceptively.

`report.md` is the canonical executive brief; the generic filename preserves helper compatibility. Do not maintain a separate editable manuscript per format. Cite with `[@S01]` and use `{{number:N01}}` for registered values, writing units and currency symbols explicitly in the surrounding sentence. Avoid metadata blocks in the manuscript; project metadata is canonical. Use project-relative image paths under `figures/`, preferably PNG for a shared PDF/Word build. Preserve vector companions for print use. Manuscript citations use source IDs directly.

## Evidence registers

Each file below is a JSON array. Empty arrays are valid during research. Readiness depends on the emitted report, not on supporting every abandoned idea.

`evidence/sources.json`:

```json
[
  {
    "id": "S01",
    "title": "Equipment observations",
    "reference": "Research team. Equipment observations. 2026.",
    "url_or_path": "sources/observations.csv",
    "published_date": "2026-08-01",
    "retrieved_date": "2026-09-08",
    "source_type": "internal_dataset",
    "origin_id": "ORIGIN01",
    "limitations": "Observed sample; not a forecast.",
    "archive_path": "sources/observations.csv"
  }
]
```

For external sources use their actual URL, publisher/author/date in `reference`, and a local `archive_path`. When retention is unavailable, replace the archive path with `archive_exception` explaining why. `origin_id` groups items sharing an underlying dataset, estimate, press release, or other evidentiary origin. Do not use a generic value such as `web` for an archive or a locator. Public references should be complete, consistent, and useful without internal file access; internal-only references must be recognizable as such.

`evidence/claims.json`:

```json
[
  {
    "id": "C01",
    "text": "The observed sample contains 40 systems.",
    "type": "internal_observation",
    "status": "supported",
    "importance": "high",
    "emitted": true,
    "report_excerpt": "The observed sample contains {{number:N01}} systems.",
    "required_qualification": "observed sample",
    "derived_from": [],
    "qualified_by": [],
    "contradicted_by": []
  }
]
```

Types: external_observation, internal_observation, company_claim, derived, assumption, projection, interpretation. Statuses: proposed, supported, qualified, unsupported, rejected, superseded. Importance: high, medium, low. `derived_from`, `qualified_by`, and `contradicted_by` are claim-ID lists; derivation must remain acyclic. An emitted claim must be supported or qualified for release. `report_excerpt` must match one paragraph after number substitution. `required_qualification` must occur in that paragraph. A reviewer checks both that the qualifier applies and that a declared derivation actually warrants its synthesis.

Add `calculation_id` for calculated claims. Company claims also require `publication_authorization` (approved/pending/public) and `attribution` matching the report; retain authorization scope in the decision record. This authorizes use, not empirical certification. A qualified claim always needs an explicit qualification. Do not mark a false proposition supported merely because a source establishes that someone said it; write the attributed proposition as the claim.

`evidence/links.json`:

```json
[
  {
    "id": "E01", "claim_id": "C01", "source_id": "S01",
    "locator": "Summary row, system_count column",
    "excerpt": "system_count: 40",
    "relation": "direct", "verification": "verified",
    "reviewer": "analyst identity",
    "assessment": "The field counts the observed systems, not transactions."
  }
]
```

Relations: direct, partial, context, contradicts. Verification: pending, verified, failed. Verified links require a named reviewer and an assessment of support. Contradictory links for emitted claims require a `disposition` explaining their effect. A locator can be a PDF page/table, section and paragraph, spreadsheet cells, or dataset selection; preserve enough detail to repeat retrieval. Excerpts should be short, exact, and proportionate to the evidence needed.

`evidence/calculations.json`: each object requires `id`, `description`, `formula`, `inputs` (paths), `outputs` (paths), `code_path`, `units`, `time_basis`, and `assumptions`. All file paths must resolve inside the project. Preserve actual code and data, not a prose-only description of a result. Formula text is documentation and is never evaluated by the helpers. Calculation existence is checked automatically; correctness and reproducibility are reviewed separately.

`evidence/numbers.json`:

```json
[
  {
    "id": "N01", "value": "40", "display_value": "40",
    "decimal_places": 0, "unit": "systems", "time_basis": "2026-08 snapshot",
    "source_id": "S01"
  }
]
```

Use numeric strings, optionally with grouping commas in `display_value`. Include `source_id`, `calculation_id`, or both. Store percentages in percent units when printing percentages, rather than displaying a fraction as a percentage. The validator checks finite values and declared rounding precision; it does not infer economic relationships or reconstruct calculations.

`figures/register.json`: each object requires `id`, `path`, `data_path`, `source_note`, `units`, and `time_basis`. Preserve analysis linkage in a `calculation_id` or a descriptive field as applicable. Register only analytical figures used by this project; put logos in styling assets. The build inserts each figure's source note after its containing document block. Captions should identify measure, scope, and period without duplicating that note.

## QA and version contracts

`qa/issues.json` is an array of issues with `id`, `description`, `severity` (blocker/material/minor), and `status` (open/resolved/accepted). Accepted issues require `disposition`; a blocker cannot be accepted in place of resolution. Explain resolved issues and link their evidence in review notes.

`qa/reviews.json` is append-only review history written by `record_review.py`. Each review contains a kind, status, reviewer, method, date, notes file and its hash, current content digest, and exact artifact hashes. The last entry per kind is authoritative. Prior entries remain historical, not current passes.

`cold_reader` is a review kind for projects with `reader_test_required: true`; older projects can opt in by setting that field to true. A pass requires an independent fresh reader who sees only the reader-facing artifact and the commission/audience. The review notes preserve the reader's unprompted reconstruction and the editor's comparison with the private message contract. A failed or missing required review blocks release; content or artifact edits make it stale. It cannot be waived as an artifact-check limitation.

`output/build.json` records input hashes, content digest, toolchain hashes, Pandoc version, requested artifacts, citation inventory, and build warnings. `output/document.json` is the expanded Pandoc document used for all formats; it is a debugging artifact, not a second manuscript.

Content fingerprints include `project.json`, `report.md`, `control/decisions.md`, and files under planning/evidence/research/analysis/drafts/figures/assets/sources. Hidden files and Python caches are excluded. Output and QA are checked separately to avoid recursive hashes. Keep authoritative inputs in the tracked locations and copy external dependencies locally. State and agent-run updates alone do not invalidate the report.

## Migrating an older report

The revised skill is self-contained and does not depend on GPU_REPORT. Leave historical projects and approvals intact. When asked to migrate one, create a sibling project, convert its authoritative source into `report.md`, and copy required sources, analysis, and assets. Convert an older outline deliberately; do not mark nodes validated merely because prose exists. A version-1 or version-2 JSON architecture may remain as-is. To adopt version 3, add `planning/message.json`, rhetorical beat fields, and a narrative `sequence` independent of support parentage. Map legacy source IDs directly, add missing evidence locators through actual inspection, mark unverified links pending, and record the origin and approved constraints.

Do not copy old QA passes into the new reviews register. Rebuild and verify the migrated artifacts. The initializer deliberately refuses an unconverted LaTeX workspace to avoid quietly treating scaffolding as migration.
