---
name: python-engineering
description: Design, implement, review, and locally refactor Python with expressive types, visible effects, lightweight composition, and verification of observable behavior. Use for Python services, agents, pipelines, integrations, and code-quality work; repository-scale migrations need a capability audit as well.
---

# Python engineering

Make the intended behavior and common execution path easy to follow. Prefer correctness, data integrity, truthful contracts, and low indirection over paradigm purity. Preserve the user's scope and established repository conventions.

## Understand the change

For new code, establish the requested behavior, inputs, outputs, failure semantics, and integration point before choosing constructs. For existing code, inspect the current diff, relevant callers, configuration, public contracts, and existing checks. Identify the outcomes that must hold, including failure behavior and persisted formats. Treat existing tests and implementation as evidence, not the sole authority: they can share the same defect.

Resolve consequential choices about defaults, compatibility, state, and lifecycle before distributing implementation. Infer routine choices from context; ask only when a missing decision materially affects the result. Keep repository-specific commands and conventions in repository documentation or `AGENTS.md`.

For an unfamiliar or multi-module problem, reason from higher abstractions to lower ones. First establish the affected capability and its public entry point. Then identify the responsible packages/modules, their contracts, ownership, and dependencies. Descend into the relevant classes/functions and finally the algorithms, representations, or statements needed to explain or change the behavior. Follow the abstraction units the repository actually uses; functions and modules do not require an intervening class layer. Use a concrete question at each level to select the next code to inspect rather than reading every file or designing the whole repository upfront. A well-located local defect can start at its known location, with enough caller context to establish the contract.

Trace the selected behavior through domain rules, configuration, state, external adapters, and consumed output. Bound implementation tasks around cohesive responsibilities with explicit inputs, outputs, failure behavior, and ownership. Keep shared policy and cross-module decisions together; include relevant callers and contracts when narrowing context. After a local fix or component check, move back up through its callers and module contract to verify the actual entry-point behavior and cross-module handoffs. Complete one behavior before widening the change. A compact flow note is enough unless the repository needs a richer map.

## Choose constructs for the actual responsibility

| Responsibility | Useful starting point |
| --- | --- |
| Stateless transformation | Named function |
| Related stateless operations | Module |
| Stable domain information | Type alias, enum, dataclass, or an existing validated schema |
| Mutually exclusive states | A discriminated union or another explicit representation |
| Replaceable policy | Named callable; callable protocol if its contract needs a name |
| External capability with real variation | Small consumer-owned protocol |
| Identity, evolving state, or owned resource | Class, often with a context manager |
| Short orchestration | Straight-line procedural code |

Make types carry meaning without elaborate generic machinery. Validate uncertain values at their boundary, then preserve the established type through internal calls and containers. Avoid discarding known domain information into `Any`, `object`, or unstructured dictionaries only to recover it with casts, dynamic attribute access, or repeated validation. Keep dynamic representations where the boundary or requirement needs them; `typing.cast` does not validate runtime input. Frozen dataclasses help express stable values but do not make nested mutable contents immutable. Use assertions for programmer invariants, not external-input validation.

Separate deterministic computations from I/O where it clarifies data flow. Pass boundary results into computations explicitly. Keep mutation local and resource ownership visible. Build growing collections with comprehensions or mutation of fresh, locally owned accumulators rather than repeated full copies; retain copies when snapshots or independent ownership are required. Respect numerical and ML libraries' performance and lifecycle requirements. Do not split cohesive code into tiny functions merely to make it look functional.

Evaluate functions, modules, and classes by the knowledge they remove from callers. Keep each changeable implementation decision with the code that owns it. Extract helpers when they create a meaningful abstraction; avoid fragmentation that forces readers to reconstruct one operation across many locations. If configured complexity tooling flags changed code, inspect its decisions: remove redundant checks or duplicated policy where behavior permits, and separate responsibilities only when each resulting unit owns a meaningful contract. Do not extract helpers solely to lower a complexity score. A short signature is insufficient if callers must understand hidden sequencing, configuration interactions, or internal representations.

Prefer the simplest interface that serves current needs without depending unnecessarily on particular callers. Keep caller-specific adaptation outside reusable mechanisms, while preserving meaningful domain operations. Add generality when it reduces present complexity. Keep effects, ownership, failure behavior, and consequential policy explicit in the contract while hiding implementation mechanics. Make bounded design improvements when the current change exposes a workaround; avoid speculative infrastructure or unrelated cleanup.

Compose dependencies at a visible entry point. Introduce interfaces, factories, or higher-order functions for demonstrated variation or a meaningful boundary. One concrete dependency does not automatically need an abstraction. Prefer explicit loops and ordinary Python over point-free pipelines, universal currying, or bespoke effect frameworks.

Use abstraction boundaries to reduce the facts needed for each local change. In Python, a computation can consume validated domain values, an adapter can translate a vendor API, and orchestration can select policy and own resource lifecycle. Each boundary should hide a distinct decision and expose the contract needed by its caller. Avoid forwarding layers that only rename the same operation, universal context objects, or splitting by execution order when steps share an invariant. Preserve useful existing boundaries; do not impose this arrangement on every script or create layers merely to divide work among agents. Check the joins as well as the components.

## Preserve behavior through effects and failure

Keep files, databases, HTTP, model calls, clocks, randomness, and process state visible at boundaries. Read configuration once at the appropriate scope and show where the selected policy is consumed.

Translate vendor errors where domain meaning is known, preserving the cause. Retry known transient failures with bounded attempts and attention to idempotency. Make fallback policy explicit. Avoid converting unexpected failure into a plausible default or a success-shaped result.

Distinguish uncertain boundary input, an internal invariant violation, and an expected operational failure. Add guards for reachable states and an intentional rejection or recovery policy; trust an established internal contract unless a separate trust boundary or mutable state justifies rechecking it. Type annotations alone do not validate runtime input. Avoid speculative null/type checks and exception catches, or defaults that disguise broken assumptions. Broad catches can belong at cleanup or process/job boundaries when they preserve failure and apply a defined policy. Assertions may express internal invariants, but checks required in production must remain active under Python optimization.

Trace important state and artifacts through the real execution path: which resource is loaded, which instance is used, which state is exported, and who releases it. Similar filenames, skipped calls, and successful subprocesses do not establish artifact correctness. For collection-building examples or consequential lifecycle/persistence work, read [state-and-resources.md](references/state-and-resources.md).

## Verify the outcome

Run the repository's required checks. For additional verification, name a plausible defect in the new or changed behavior, the input or state that exposes it, the execution path to exercise, and the expected observation. Use an existing check when it covers that defect. Do not add a test, harness, or review stage solely to appear thorough. Prefer real deterministic collaborators within the behavior being exercised; replace expensive or volatile boundaries as needed. Assert interactions when the interaction itself is contractual, such as a prohibited paid call or a required idempotency key. Do not replace the internal handoff whose correctness the test claims to establish.

For consequential changes, use [behavioral-verification.md](references/behavioral-verification.md) to identify relevant input/state partitions and checks. A small table or prose note is enough; ordinary edits need no contract file or task graph.

Run checks after the final relevant edit and report their actual results. Justify changes to acceptance expectations, exclusions, or check configuration from the contract; do not weaken them merely to obtain a pass. Add repository enforcement only for a specific rule whose violations can be detected reliably within the requested scope.

Use configured static, focused behavioral, integration, smoke, or performance checks where they resolve an affected risk. Derive expected outcomes from requirements, domain examples, or an independently justified model. Avoid tests that merely restate fields, reproduce production logic to calculate expectations, assert a mock's configured result without exercising a meaningful contract, or verify language/library behavior. Test cases may follow branches when those branches represent required behavior; branch coverage alone does not establish correctness.

Ask which plausible defect each new test would detect and whether a behavior-preserving refactor would break it unnecessarily. For consequential or suspicious assertions, a focused temporary mutation or fault injection can verify that the test fails for the intended reason. Do not require mutation runs or new tests for every edit. A simulated boundary can establish wiring but cannot establish real vendor or hardware semantics; state that limit when it matters. When selecting test boundaries, repairing weak assertions, or justifying guards, read [testing-design.md](references/testing-design.md).

## Keep global judgment with the main agent

The main agent owns policy, architecture, integration, and the final assessment. Delegate independent test creation, pure functions, or boilerplate when the work has a clear contract and enough substance to justify handoff. An independent verification worker is useful when it can challenge consequential assumptions; it is not a default requirement.

Give a worker the relevant requirements, settled interfaces, source context, permitted paths, and a stopping condition. Include a narrow IR slice if one exists. Let it surface ambiguity; reconcile it centrally. Retain stable global context with the main agent rather than repeatedly sending the full repository. Do not assume higher cache hit rates mean lower total cost.

Keep exploratory detail with the worker. Its return should identify the outcome delivered, changed paths, checks and observed results, retrievable evidence, unresolved decisions or conflicts, and limitations. A short note suffices. Open decisive evidence before accepting a consequential conclusion; a compressed summary can omit the same handoff as the implementation.

For repository splits or migrations across capabilities, add a baseline-to-target audit of outcomes, behavior, and implementation dependencies. Use a repository-refactoring workflow if available; this skill remains usable independently.

## Finish and review

Check that the real entry point consumes the change, relevant outcomes have evidence, and unrelated work is preserved. Report actual checks and material unverified behavior. Review findings should identify a concrete scenario, location, consequence, and practical correction; preference alone is not a blocker.

Assess design against the requested behavior: identify duplicated decisions, implementation knowledge required by callers, or ownership and failure semantics the code leaves ambiguous. Locate the dependency and explain what change or failure it obstructs. Do not equate fewer lines, additional abstractions, or a functional style with maintainability; preserve behavior while improving the contract a reader must reconstruct.
