---
name: repository-refactoring
description: Plan, execute, or review repository splits, package extraction, and substantial architecture migrations by comparing baseline and target capabilities, behavior, ownership, and dependencies. Use when a local code cleanup is insufficient to establish migration parity.
---

# Repository refactoring

Preserve required outcomes while changing structure. Cleaner modules and passing local tests do not establish migration completeness. Keep the audit proportional to the capabilities and boundaries being changed.

## Fix the comparison contract

Establish the authoritative baseline repository/revision, target, refactor kind, in-scope outcomes, operating modes, compatibility obligations, and protected concurrent work. Inspect Git status and relevant worktrees before editing.

A deployed default and an experimental variant remain distinct capabilities until an explicit decision merges or retires them. Distinguish pinned baseline behavior from target additions sourced from later or external work. Untracked reconstructions and generated analysis are evidence with limitations, not automatically authoritative baselines.

Do not infer retirement from deletion or a cleaner replacement. Settle consequential policy and ownership centrally; progress on independent discovery while unresolved decisions remain visible.

## Compare three perspectives

| Perspective | Baseline-to-target question |
| --- | --- |
| Use cases | Does each required outcome and important mode have an owner and explicit disposition? |
| Behavioral flows | Are ordering, defaults, precedence, fallbacks, retries, state transitions, and artifact handoffs preserved or intentionally changed? |
| Implementation dependencies | Which entry points, modules, configuration, schemas, models/prompts, storage, and external systems implement each flow? |

Start with the required capability and its entry point, identify the responsible packages/modules and contracts, then descend into the functions and runtime dependencies needed to explain the migration. Trace important capabilities vertically through all three perspectives; these are views of the same behavior, not separate phases or required agents. Split flows by adapter, asset, or mode when algorithms or ownership differ. An import graph misses semantic and runtime relationships; similar filenames do not prove equivalent behavior.

For a bounded extraction, one capability table with compact flow notes may suffice. For multiple capabilities or repositories, use [refactor-record.md](references/refactor-record.md) as the working record. Keep one authoritative mapping; diagrams can be views of it. Do not create a node for every function or duplicate Git history.

For a large unfamiliar Python repository, `scripts/inventory_repository.py <root> --format markdown` can provide a read-only starting inventory. It identifies candidate entry points and coarse absolute-import relationships; it is not a complete dependency graph and does not resolve relative/dynamic imports or prove parity.

## Make dispositions and gaps explicit

Give each discovered in-scope baseline capability a disposition: **preserved**, **replaced**, **deferred**, **retired**, or **concurrent-owned**. Record evidence or remaining gaps. Name the replacement and compatibility decision, deferral owner/condition, retirement authority, or protected concurrent path as applicable.

A missing target implementation is an unresolved gap, not evidence of an authorized deferral or replacement. Keep its disposition pending until the responsible decision is established. Distinguish the intended disposition from delivered implementation and verification status.

Inspect unexplained baseline capabilities before excluding them. Existing behavior can conflict with an authoritative contract; preserve compatibility where required and record deliberate defect corrections explicitly. A parity test alone can preserve a bug.

## Design and migrate in vertical slices

Partition by cohesive capability and meaningful ownership. Keep public contracts narrow and dependency direction visible. Avoid technical dumping grounds and shared packages that erase ownership. Use functions, domain values, composition, and owned-resource classes as appropriate; this workflow requires no particular programming paradigm or companion skill.

Complete one outcome through its policies, adapters, artifacts, and consumers before widening adjacent abstractions. Use compatibility adapters where they avoid forcing an unnecessary caller migration. Verify configuration consumption and the target's real entry point, including cross-package handoffs. Keep cutover and rollback consistent with the existing operating contract.

Protect dirty or concurrent work. Use an isolated checkout/worktree when appropriate and reconcile at declared boundaries. Do not copy half-finished sibling implementations or silently simplify away active special cases.

## Use context and delegation selectively

The main agent owns scope, baseline authority, product policy, target design, capability dispositions, cross-layer reconciliation, and integration. It may delegate independent use-case discovery, flow comparison, dependency inventory, implementation slices, or verification. The three audit perspectives do not require three separate agents.

Give workers the shared comparison contract plus relevant source evidence, a bounded capability slice, permitted paths, and a stopping condition. Discovery workers propose findings and dispositions; they do not redefine scope or edit the canonical audit. Implementation workers need clear interfaces and ownership. Reconcile contradictions centrally and verify joins across slices.

Keep exploratory logs outside the root's routine context. A worker return should identify its capability/outcome, changed paths, observed checks, evidence locations and revision, open decisions or contradictions, and limitations. The root inspects decisive evidence before settling a disposition or accepting a handoff; neither a summary nor a valid record establishes parity.

Use machine-readable graphs when repeated impact queries, cross-session resumption, or bounded disclosures warrant them. Use Git revisions as source identity. Add freshness checks for concrete stale-evidence risks rather than requiring a general task/evidence harness. See [ir-and-git.md](references/ir-and-git.md) when choosing the representation.

## Verify and finish

Run required repository checks. For each claimed preserved or replaced capability, identify a specific behavior the migration could break, the input/state that exposes it, the affected target entry point, and the observation its consumer must receive. Reuse checks that establish that behavior; add checks for uncovered migration failures rather than for every moved function. For example, after extracting configuration handling, change the operator's live configuration and observe whether the target behavior consumes it; successful imports do not establish that contract. Distinguish static validation, historical-result reuse, component checks, simulated wiring, and actual target execution. None is interchangeable evidence.

Review one coherent capability with its baseline-to-target contract, important modes, changed interfaces or diff, disposition, and consumer checks together. Reuse the canonical comparison rather than maintaining a separate review graph. Choose reading order for the capability and its dependencies; inspect shared policy and cross-slice joins explicitly. See [refactor-record.md](references/refactor-record.md) for a compact review view and a runnable extraction example.

If storage cleanup is in scope, follow the authorized backup/retention and removal policy and verify the intended target. Cleanup does not establish capability retirement.

Before declaring completion, reconcile outcomes, behavior, and dependencies; give important baseline capabilities explicit dispositions; verify critical handoffs; and align operating/cutover instructions with the delivered target. Report deferred, concurrent-owned, and unverified items directly. Structural completeness is insufficient when an outcome remains unwired.
