from collections.abc import Mapping


def _request(record):
    if not isinstance(record, Mapping):
        raise ValueError("invoice must be a mapping")
    account = record.get("account_id")
    amount = record.get("amount_cents")
    if not isinstance(account, str) or not account:
        raise ValueError("account_id must be nonempty")
    if type(amount) is not int or amount <= 0:
        raise ValueError("amount_cents must be positive")
    return {"account_id": account, "amount_cents": amount}


def dispatch(record, provider, *, attempts=2):
    if type(attempts) is not int or attempts < 1:
        raise ValueError("attempts must be a positive integer")
    request = _request(record)
    for attempt in range(attempts):
        try:
            return provider(request)
        except TimeoutError:
            if attempt == attempts - 1:
                raise


def dispatch_batch(records, provider, *, attempts=2):
    if type(attempts) is not int or attempts < 1:
        raise ValueError("attempts must be a positive integer")
    receipts, rejected = [], []
    for position, record in enumerate(records):
        # Validate separately so a provider's ValueError is not a record rejection.
        try:
            request = _request(record)
        except ValueError:
            rejected.append(position)
            continue
        receipts.append(dispatch(request, provider, attempts=attempts))
    return {"receipts": receipts, "rejected": rejected}
