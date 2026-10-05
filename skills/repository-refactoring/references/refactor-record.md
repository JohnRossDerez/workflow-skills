# Compact refactor record

Adapt this record to the migration. Omit irrelevant sections, use prose where clearer, and keep one canonical mapping. Do not fill fields merely to make the document look complete.

## Comparison contract

- Baseline repository and revision; reason it is authoritative:
- Target repositories/packages and revisions or current workspace:
- Refactor kind: replacement, staged extraction, library, or narrower product:
- Required outcomes, deployed defaults, and important modes:
- Compatibility constraints and explicit exclusions:
- Concurrent owners and protected work:
- Consequential open decisions:

## Capability comparison

| Capability / trigger / mode | Baseline flow and dependencies | Target owner, flow, and dependencies | Disposition and intentional difference | Evidence or remaining gap |
| --- | --- | --- | --- | --- |
| Name a required outcome | Meaningful decisions and actual execution path | Corresponding target path, including handoffs | Explicit status and rationale | Revision, exercised command/API, observed result, limitations |

Each important row connects use case, behavior, and implementation. Expand only a complex row into a separate flow note. Include runtime configuration, schemas, prompts/models, storage, and downstream consumers where they affect that capability.

Dispositions are `preserved`, `replaced`, `deferred`, `retired`, and `concurrent-owned`. A proposed preserved row with no evidence remains a gap until checked. Deferred rows need an owner or completion condition. Retired rows need established authority. Concurrent-owned rows need a protected path/branch and integration expectation.

If no decision establishes a disposition, mark it pending and describe the gap. Missing implementation alone does not authorize `deferred` or `replaced`. Keep a proposal distinguishable from an established decision and its actual delivery evidence.

## Flow notes, when needed

```text
Capability and operating mode:
Baseline: input -> policy/decision -> transformation -> effect/state -> artifact/consumer
Target:   input -> policy/decision -> transformation -> effect/state -> artifact/consumer
Difference: preserved / authorized change / unresolved
Concrete paths and runtime dependencies:
Required invariant or compatibility boundary:
Evidence and limitation:
```

Keep this semantic. Incidental function calls and directory names are not separate behavioral stages.

## Execution and handoff evidence

| Outcome / risk | Check and input/state partition | Revision / input identity | Observed outcome | Limitation or next action |
| --- | --- | --- | --- | --- |

Observe the consumed result and important forbidden effects. Show that configuration reaches the target behavior and that artifacts reach the intended consumer. Label historical reuse, boundary substitutes, and real-runtime execution accurately.

## Ownership and operations, when affected

- Capability owner and public contract for each target:
- Dependency direction and justified shared dependencies:
- Compatibility adapter and eventual caller migration:
- Cutover/default selection and rollback:
- Backup/retention/cleanup action if authorized:
- Unresolved decisions and cross-slice contradictions:

Record delegated discoveries only if delegation is used. Preserve worker evidence, reconcile discrepancies, and keep canonical dispositions with the main agent. Use Git revisions for source snapshots rather than reproducing commit history here.

## Capability review view

For a material slice, point the reviewer to its existing row/flow note, baseline and target identities, relevant changed interfaces or diff, important modes/defaults, and execution evidence through the consumer. Include unresolved ownership or policy and cross-slice dependencies. Ask whether the reviewer can trace the outcome and distinguish an intended disposition from delivered behavior. This is a view of the canonical record, not another inventory to synchronize.

The [package-extraction example](../assets/package-extraction/CAPABILITY_COMPARISON.md) pairs a compact comparison with runnable checks. `verify_contract.py` applies the same public outcomes to `baseline`, the deliberately incomplete `candidate`, and `reference`; its `--module invoice_dispatch` option checks the canonical package. Read it only when that extraction/compatibility handoff is relevant. These synthetic results are not evidence for the repository being migrated.
