# Behavioral verification

Use this reference for consequential contracts, persistence, recovery, compatibility, or external-effect changes. Do not turn it into a required checklist for every edit.

## Establish an oracle independent of implementation structure

Start with authoritative requirements, consumers, persisted formats, and operating expectations. Reconcile conflicts with the main agent. Baseline comparison establishes parity only for the compared behavior; it can preserve an inherited defect.

For each material requirement, select the input or state distinctions that could change its outcome. Include malformed input and failure handoffs where the boundary permits them. Check both what must happen and effects that must not happen.

| Requirement | Relevant distinction | Observable outcome | Forbidden effect | Useful check |
| --- | --- | --- | --- | --- |
| Export a completed checkpoint | Fresh / interrupted / completed | Exported state corresponds to selected checkpoint | Exporting fresh state as a completed result | Exercise resume-to-export through the production seam; inspect state identity |
| Reject invalid batch records | Valid record / missing field / wrong shape | Invalid records produce the specified rejection | Paid call for an invalid record; loss of valid batch items | Mixed batch through public API with boundary call capture |
| Recover durable results | Recorded result / publication gap / changed request | Correct result reused or recomputed according to identity policy | Duplicate external effect for a reusable result | Restart from persisted state and inspect published results and boundary calls |

These are examples, not universal policies. Missing-checkpoint behavior, batch failure handling, and reuse identity depend on the actual contract.

## Exercise the seam that could fail

Use real orchestration and internal state transitions with a bounded substitute at an expensive or unavailable external boundary. Inspect persisted outputs, resource identity, or meaningful return values. Call-count assertions can supplement these observations but seldom establish them alone.

Choose fault injection where it can expose a real defect: interrupted publication, an adapter exception, serialization failure, or cleanup after partial work. A check is more convincing when a plausible faulty implementation would fail it. Use a small temporary mutation only when additional confidence justifies the work; do not build a mutation system for ordinary changes.

Do not replace the production execution seam with a test-only pipeline and then claim the production wiring passed. Test fixtures must carry the state whose loss or corruption matters.

## Independent verification when useful

Give a worker the user-visible contract, relevant inputs/callers, settled interfaces, current checks, allowed files, and budget. It may inspect implementation but should derive expected outcomes from the contract. Do not supply a suspected defect or intended patch when the purpose is independent discovery.

The worker returns checks, observed outcomes, ambiguities, and limitations. The main agent resolves policy, runs integrated checks, and reviews whether the selected partitions cover the consequential behavior. Independence offers another perspective; shared models and source material can still produce correlated omissions.

## Properties and operation sequences when they add coverage

Use a property when a stable invariant spans many inputs: normalization is idempotent, a rejected batch preserves caller state, or an alternate input representation has the same specified result. Derive the expected result independently of the implementation. Keep explicit regression examples for known failures; generated inputs do not repair a mistaken oracle.

Use stateful sequences when earlier operations affect correctness, such as import followed by rollback, restart after publication, or cancellation during cleanup. Compare observable state against a small test-side model after consequential transitions. Include the important transition deliberately, record a reproducible seed or trace, and report limits such as absent shrinking. Generation is optional: a focused sequence or example can expose the same defect with less machinery.

For checkpoint-to-export work, [the executable example](../assets/checkpoint-export/test_workflow.py) checks persisted state and resource ownership. Run it with its sibling `workflow.py`; it uses a CPU stand-in and does not establish real trainer or GPU behavior. Load it only when that handoff is relevant.

## Limits

Static checks support type and API consistency. Boundary substitutes support orchestration and local policy. Real bounded canaries support actual runtime integration. None automatically proves the others.

Report evidence at its actual scope. A CPU stand-in cannot prove PEFT restoration, quantized export fidelity, GPU memory release, or provider behavior. Do not add unrelated broad suites after the relevant risks have been checked.
