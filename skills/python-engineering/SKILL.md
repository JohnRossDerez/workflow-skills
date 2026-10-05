---
name: python-engineering
description: Design, implement, review, and locally refactor Python with expressive types, visible effects, lightweight composition, and verification of observable behavior. Use for Python services, agents, pipelines, integrations, and code-quality work; repository-scale migrations need a capability audit as well.
---

# Python engineering

Make the intended behavior and common execution path easy to follow. Prefer correctness, data integrity, truthful contracts, and low indirection over paradigm purity. Preserve the user's scope and established repository conventions.

## Understand the change

Inspect the current diff, relevant callers, configuration, public contracts, and existing checks. Identify the outcomes that must hold, including failure behavior and persisted formats. Treat existing tests and implementation as evidence, not the sole authority: they can share the same defect.

Resolve consequential choices about defaults, compatibility, state, and lifecycle before distributing implementation. Infer routine choices from context; ask only when a missing decision materially affects the result. Keep repository-specific commands and conventions in repository documentation or `AGENTS.md`.

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

Make types carry meaning without elaborate generic machinery. Validate uncertain values at their boundary, then use the established internal contract. Frozen dataclasses help express stable values but do not make nested mutable contents immutable. Use assertions for programmer invariants, not external-input validation.

Separate deterministic computations from I/O where it clarifies data flow. Pass boundary results into computations explicitly. Keep mutation local and resource ownership visible; respect numerical and ML libraries' performance and lifecycle requirements. Do not split cohesive code into tiny functions merely to make it look functional.

Compose dependencies at a visible entry point. Introduce interfaces, factories, or higher-order functions for demonstrated variation or a meaningful boundary. One concrete dependency does not automatically need an abstraction. Prefer explicit loops and ordinary Python over point-free pipelines, universal currying, or bespoke effect frameworks.

## Preserve behavior through effects and failure

Keep files, databases, HTTP, model calls, clocks, randomness, and process state visible at boundaries. Read configuration once at the appropriate scope and show where the selected policy is consumed.

Translate vendor errors where domain meaning is known, preserving the cause. Retry known transient failures with bounded attempts and attention to idempotency. Make fallback policy explicit. Avoid converting unexpected failure into a plausible default or a success-shaped result.

Trace important state and artifacts through the real execution path: which resource is loaded, which instance is used, which state is exported, and who releases it. Similar filenames, skipped calls, and successful subprocesses do not establish artifact correctness. For consequential lifecycle or persistence work, read [state-and-resources.md](references/state-and-resources.md).

## Verify the outcome

Select checks for the changed contract and risk. Verify representative valid and invalid inputs, important state transitions, failure handoffs, and observable outputs. Mock volatile external boundaries rather than the internal handoff being tested.

For consequential changes, use [behavioral-verification.md](references/behavioral-verification.md) to identify relevant input/state partitions and checks. A small table or prose note is enough; ordinary edits need no contract file or task graph.

Use configured static, focused behavioral, integration, smoke, or performance checks where they resolve an affected risk. Avoid adding tests that merely restate fields, mirror branches, or assert language/library behavior. A simulated boundary can establish wiring but cannot establish real vendor or hardware semantics; state that limit when it matters.

## Keep global judgment with the main agent

The main agent owns policy, architecture, integration, and the final assessment. Delegate independent test creation, pure functions, or boilerplate when the work has a clear contract and enough substance to justify handoff. An independent verification worker is useful when it can challenge consequential assumptions; it is not a default requirement.

Give a worker the relevant requirements, settled interfaces, source context, permitted paths, and a stopping condition. Include a narrow IR slice if one exists. Let it surface ambiguity; reconcile it centrally. Retain stable global context with the main agent rather than repeatedly sending the full repository. Do not assume higher cache hit rates mean lower total cost.

Keep exploratory detail with the worker. Its return should identify the outcome delivered, changed paths, checks and observed results, retrievable evidence, unresolved decisions or conflicts, and limitations. A short note suffices. Open decisive evidence before accepting a consequential conclusion; a compressed summary can omit the same handoff as the implementation.

For repository splits or migrations across capabilities, add a baseline-to-target audit of outcomes, behavior, and implementation dependencies. Use a repository-refactoring workflow if available; this skill remains usable independently.

## Finish and review

Check that the real entry point consumes the change, relevant outcomes have evidence, and unrelated work is preserved. Report actual checks and material unverified behavior. Review findings should identify a concrete scenario, location, consequence, and practical correction; preference alone is not a blocker.

For consequential design work, assess whether a reader can explain the common path, domain values and units, policy location, resource ownership, and failure precedence. A bounded follow-up change can reveal duplicated policy or difficult integration. Do not equate fewer lines, additional abstractions, or a functional style with maintainability; preserve behavior while improving the contract a reader must reconstruct.
