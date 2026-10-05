# Extraction capability comparison

## Scope and authority

The synthetic `baseline/legacy_dispatch.py` and `CONTRACT.md` define this exercise's baseline. These files have no repository commit identity; do not present them as a deployed historical revision. The target ownership is the standalone `invoice_dispatch` package, with `legacy_dispatch` retained as a compatibility surface.

The candidate is intentionally incomplete. The reference implements the contract at both entry points. There is no retirement or policy-change authorization in this exercise.

## Three-layer comparison in one table

| Use case / mode | Baseline behavior and path | Candidate target behavior and path | Corrected target owner/path | Disposition and evidence |
| --- | --- | --- | --- | --- |
| Single invoice dispatch | Validate shape/fields, send `account_id` and `amount_cents`, return provider receipt; `legacy_dispatch.dispatch` | Weaker validation and changed provider field names; legacy shim calls `invoice_dispatch.dispatch` | `invoice_dispatch.parse_invoice` and `send_invoice`, reached through either public surface | Candidate has a compatibility gap; corrected target preserves request and return behavior in contract checks |
| Default and explicit transient retry | Two default attempts; explicit count consumed; only `TimeoutError` retried | Policy dataclass exists but execution calls provider only once | `dispatch` validates attempts; `send_invoice` consumes the count | Candidate leaves policy disconnected from execution; corrected target exercises successful retry and exhaustion |
| Mixed-validity batch | Invalid records rejected by position, valid receipts kept in order; provider errors propagate | No target batch API or legacy re-export | `invoice_dispatch.dispatch_batch`, re-exported by `legacy_dispatch` | Candidate has an unmapped capability; corrected target checks mixed batch and provider error handoff |

Implementation structure alone misses these distinctions: the candidate package imports successfully, the old single-dispatch name exists, and its policy value looks correct. None establishes the provider contract, retry execution, or batch outcome.

## Verification

The eight contract checks pass against the baseline, the reference legacy surface, and the reference canonical package. The candidate fails the suite as expected. Cases cover request/receipt identity, malformed records and forbidden provider effects, default retry, explicit attempts/exhaustion, invalid retry configuration, non-transient errors, mixed batch results, and provider `ValueError` propagation.

The fixtures perform no real external calls. They establish the example's local contract and wiring, not a live invoice provider's semantics. The source mapping is an editorial interpretation supported by execution evidence; it is not automatically complete merely because it is a table.

## Cutover within the exercise

The reference is ready for this bounded compatibility example. The candidate is not ready to replace the baseline. Real cutover would additionally require the repository's pinned revision, actual callers, configuration/deployment contracts, and appropriate real-runtime evidence.
