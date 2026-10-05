# Choose tests and justify guards

Use this guidance when selecting a test boundary, reviewing weak tests, or deciding whether a guard belongs in Python code. Start from the changed contract and a specific wrong outcome the check must detect. Do not add tests or defenses merely because a construct is present.

## Choose the boundary that exposes the defect

| What must be established | Action |
| --- | --- |
| A deterministic domain rule | Call the real function with domain inputs and assert independently derived results. Include a boundary case when it distinguishes the required rule from a plausible incorrect one. |
| Components pass the right values or state | Exercise the actual caller and collaborators together. Observe the returned or persisted result; do not mock the handoff being checked. |
| A required or prohibited external interaction | Replace the external boundary and assert the contractual arguments, ordering, or absence of calls. Do not assert incidental internal call sequences. |
| An invariant across many inputs | Use property-based testing when a justified property and useful generators cover cases that examples would miss. Pair round-trip properties with known values if matching encode/decode bugs could cancel out. |
| Behavior after interruption or failure | Inject the specific failure at the affected boundary and inspect the resulting state, preserved artifact, or released resource. |

Prefer real deterministic collaborators. Substitute network, hardware, or other expensive/volatile boundaries when needed. A substitute verifies local wiring and policy, not the vendor's semantics. Where a fake's behavior is itself disputed, use the real boundary or state the unresolved limitation.

Use TDD when a failing example helps settle the contract or guide implementation. It does not require one test per method or mocks for every dependency. Choose integration breadth according to the handoff under examination, not a universal test ratio.

## Repair weak assertions

Derive expectations from requirements or independently justified examples. Do not copy the production algorithm into the expected value. Select a scenario that distinguishes a plausible defective implementation, not merely a convenient input/output pair.

### Python example: successful export can still contain the wrong state

Contract: exporting an already-completed checkpoint must publish its saved state and release the acquired model. Skipping training must not skip restoration. This example uses the repository's [runnable CPU workflow](../assets/checkpoint-export/workflow.py); its model stands in for an external ML runtime.

```python
import json

from workflow import Model, run_export


def test_completed_checkpoint_exports_saved_state(tmp_path):
    checkpoint = tmp_path / "checkpoint.json"
    output = tmp_path / "export.json"
    checkpoint.write_text(json.dumps({"weight": 41, "step": 10}))
    model = Model()  # Fresh state differs from the completed checkpoint.

    run_export(checkpoint, output, target_step=10, acquire=lambda: model)

    # Weak on its own: fresh model state can also produce an output file.
    assert output.exists()

    # Stronger: inspect what the consumer receives after real orchestration.
    assert json.loads(output.read_text()) == {"weight": 41, "step": 10}
    assert model.closed
```

The supplied `broken_completed_export` writes a valid file and closes the model, but exports fresh state when training is skipped. The artifact-content assertion rejects that implementation. The test keeps checkpoint loading, restoration, orchestration, and publication connected instead of mocking those handoffs or asserting that `restore()` was called. Reading the expected values from the input checkpoint is legitimate here: state preservation is the specified relationship, and the output takes a separate execution path. This establishes the stand-in workflow's behavior, not a real ML library's restoration semantics.

Inspect suspicious tests for these specific failures:

- The test exercises only its own setup, or replaces the production function with a mock. Exercise the real behavior instead.
- The expected result repeats the production algorithm. Use an independently established value or model.
- An exact outcome is known, but the assertion checks only truthiness, positivity, or non-nullness. Assert the required outcome.
- An exception is required, but the assertion runs only if one occurs. Use `pytest.raises` or the repository's equivalent so absence of the exception fails.
- The test accepts both success and failure when the scenario requires one. Assert the required branch and its effects.
- A behavior-preserving refactor breaks internal call assertions. Retain only interactions that belong to the public contract.

A mock returning a configured value can establish forwarding if forwarding is the requirement. It cannot establish the mocked calculation. A test that encodes a mistaken requirement is an oracle error even when it can catch regressions; verify the requirement before labelling every implementation-derived example a tautology.

If assertion sensitivity is uncertain, name one plausible faulty implementation and determine whether the test would reject it. Run a focused temporary mutation only when that question warrants execution. Use [behavioral-verification.md](behavioral-verification.md) for stateful handoffs; do not introduce a mutation campaign by default.

## Place guards where the contract requires them

Validate uncertain external inputs with explicit runtime checks. Once converted into the internal representation, use its contract. Revalidate only where another trust boundary, persisted state, or mutation can invalidate earlier knowledge; Python annotations alone do not validate runtime values.

Before adding a guard or catch, identify the reachable condition and the required response. If `load_customer` promises `Customer` or an exception, remove an invented `if customer is None: return []` fallback. If absence is legitimate, represent it in the contract and handle it deliberately.

Catch specific operational failures when the code has a defined response. A timeout retry needs bounded attempts and idempotency considerations. Broad catches can implement cleanup with re-raising or a defined failed-job/batch policy; do not turn unexpected exceptions into plausible success results.

Use assertions for internal invariants. Use explicit checks when enforcement must remain active in production because Python optimization can remove assertions. Test a guard's rejection or recovery when that behavior is part of the changed contract; do not manufacture impossible inputs just to cover defensive branches.

## Sources behind the choices

These instructions combine state-oriented and interaction-oriented testing rather than enforcing one school. [Fowler compares classical and mockist TDD](https://martinfowler.com/articles/mocksArentStubs.html); [Dodds argues for integration emphasis](https://kentcdodds.com/blog/write-tests); [QuickCheck](https://www.cs.tufts.edu/~nr/cs257/archive/john-hughes/quick.pdf) and [Hypothesis](https://hypothesis.readthedocs.io/en/latest/) support property-based testing; [SQLite](https://www.sqlite.org/testing.html) illustrates failure-oriented checks; [Design by Contract](https://www.eiffel.org/doc/solutions/Design_by_Contract_and_Assertions) motivates assigned obligations. These sources inform the decisions above; they do not mandate a suite shape.
