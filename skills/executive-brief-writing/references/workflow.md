# Adaptive executive brief workflow

This reference describes the full workflow. Ordinary reports use compact-workflow.md; a full graph is conditional, not the default.

## Configure once

Record the selected reader purpose first. Then record the executive audience, authority, decision or alignment context, requested action, scope, length, deadline, circulation and disclosure constraints, and requested artifacts in `planning/brief.md`. Keep exact user directions and material decisions in `control/decisions.md`. `project.json` stores executable settings:

- `mode`: investigate, decide, explain, or argue.
- `depth`: targeted, standard, or extended. This changes search breadth and documentation effort, never truthfulness.
- `structure`: preserve or flexible. Record protected headings and required coverage in the brief.
- `approval_policy`: adaptive, gated, or preapproved. Adaptive is the default.
- `formats`: any requested subset of md, pdf, docx.

Infer supplied preferences; do not ask the user to fill out a configuration form. An executive audience does not make every assignment a recommendation, and a commercially commissioned brief is not automatically an open investigation.

## Dependencies and entry points

Use `brief + reader stakes → compare framings → selected message → evidence design ↔ research/analysis → support graph + narrative beats → compile → stitch → semantic revision → cold-reader test → proofread → production`. A material comprehension failure sends work back to the earliest affected stage, followed by a new test. Evidence-dependent prose follows stable analysis; opening orientation and final requested action follow the body. Work on independent questions or production setup while other inputs are pending.

Start a new brief at intake. For a revision, start at the earliest affected dependency. For proofreading, inspect the existing argument and sources only as needed to detect meaning-changing errors. Do not restart research or restructure an approved document merely to conform to this workflow.

For a new sustained brief, first write a compact reader-stakes card in `planning/brief.md`. Use it with the emerging evidence to compare two or three materially different truthful framings of a supportable answer. Compare only messages the evidence can support; record an evidence-rejected premise separately from the framing choice. Choose the framing that best moves this reader toward the supported answer; record the alternatives and reason in `control/decisions.md`. A fixed commission or small revision may need no framing search; record a material constraint or change of direction, not a ritual list of alternatives. Reconsider the choice if decisive evidence or a cold-reader test changes it.

Define `planning/message.json` before decomposing the argument: record the executive's starting state, desired end state, the selected communicative thesis, the tension that makes attention worthwhile, and the proof direction. Use `top_down` by default so the answer, consequence, or requested action leads; use `bottom_up` only when revealing the conclusion early would mislead; use `re_earning` when the first page should orient and the body should prove the message before returning to action.

`planning/research.md` records questions, evidence needed, countertests, scope, and stopping decisions. `planning/architecture.md` gives reviewers a concise narrative map, including what belongs in the main path, appendix, or archive and where the reader needs emphasis or a pause; it must agree with, but does not replace, the executable graph. In `planning/architecture.json`, parent and dependency edges describe support while `sequence` describes the executive reading path. Each beat has one rhetorical role, one new contribution, a reader outcome, and a handoff to what follows. `planning/concepts.json` owns definitions and first-use placement. Keep the internal support graph deep enough for rigor while the visible brief remains shallow and scannable.

Use the deterministic helper before orchestration or release:

```bash
python3 <skill-directory>/scripts/tree_workflow.py validate <project-directory>
python3 <skill-directory>/scripts/tree_workflow.py ready <project-directory> --phase research
python3 <skill-directory>/scripts/tree_workflow.py ready <project-directory> --phase draft
python3 <skill-directory>/scripts/tree_workflow.py ready <project-directory> --phase review
python3 <skill-directory>/scripts/tree_workflow.py disclose <project-directory>
```

The root agent updates node statuses only after inspecting the corresponding artifact and evidence. A support parent cannot advance beyond a child. For version 3, `disclose` emits narrative `sequence` with each beat's support ancestors, neighbors, established context, and last-mention distance; older versions retain parent-first disclosure. Release requires every node to be validated.

## Human review

Adaptive policy carries forward supplied decisions and continues authorized work. Ask when a missing or changed material choice requires the owner's judgment. Gated policy uses only the gates the user requested: record `gate_id`, `status` (pending/approved/waived), and the decision record path in `project.json`. Preapproved policy records the scope of advance authorization in the brief. Never infer external distribution authorization from any policy.

At a checkpoint present a compact decision card: recommendation, material change, key uncertainty, and exact choice. Link to the evidence and audit detail. Do not make the owner approve administrative artifacts or reapprove unchanged decisions. Requested downstream-dependent gates remain pending until answered; progress on independent work meanwhile.

## Changes and state

`control/state.json` records stage, work status, next action, and affected artifacts; it is a resume aid, not proof of release readiness. Work status and human gate status are separate.

On changed data, assumptions, citations, concepts, or instructions, locate the earliest affected input and run `tree_workflow.py invalidate <project> <node-id>...`, adding `--concept-id <id>` or `--claim-id <id>` when appropriate. A changed message or proof direction requires reconsidering the narrative sequence and beat contracts even when the evidence is stable. Recompile the affected scope, restitch its joins, then reconcile the opening answer, requested action, exhibits, exports, and reviews. The supplied scripts conservatively invalidate release reviews when tracked content changes.

Do not update a stale review's digest to make it pass. Do not reinterpret historical approvals to cover a new time basis, conclusion, or disclosure. Copyedits that preserve meaning can be reviewed quickly, but exported files must still reflect the current source.

When a cold reader misreads the message, action, or material uncertainty, compare the unprompted reading with `planning/message.json` and the reader-stakes card. Reopen message selection for a wrong target, evidence for an unsupported inference, architecture or concept introduction for a missing link, and prose for a local ambiguity. Record the issue and affected nodes; rebuild and retest the changed artifact rather than treating all failures as copyedits.
