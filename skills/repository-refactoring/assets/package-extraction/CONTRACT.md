# Invoice dispatch extraction

Extract the deployed invoice dispatch capability from `legacy_dispatch` into `invoice_dispatch` while preserving existing callers. The baseline in `baseline/` is authoritative for this exercise. Existing imports of `legacy_dispatch.dispatch` and `legacy_dispatch.dispatch_batch` must remain usable in the target. The extracted package must not import the legacy module.

For a valid invoice, dispatch sends exactly `{"account_id": <nonempty string>, "amount_cents": <positive integer>}` to the supplied provider callable and returns its receipt unchanged. Booleans are not amounts. Extra input fields are ignored. Invalid records, including non-mapping values, raise `ValueError` before calling the provider.

By default, dispatch permits two total attempts on `TimeoutError`. Explicit `attempts` values are positive integers and govern the actual execution path. Other provider exceptions propagate without retry or conversion. Exhausted timeouts propagate.

Batch dispatch preserves input order within its receipt and rejection lists. Invalid records become rejection entries containing their zero-based input position, while valid records continue. Provider errors propagate, as they do for single dispatch. Existing callers pass the provider positionally and may pass `attempts` by keyword.

The package extraction changes ownership and structure; there is no authorization to drop batch handling, alter provider request fields, change the deployed default, or reinterpret provider failures.

The directories `candidate/` and `reference/` are an illustrative review exercise and its corrected implementation. They are examples, not a blinded benchmark. Use the candidate with the contract and baseline for independent discovery; inspect the reference after the review.
