from dataclasses import dataclass


@dataclass(frozen=True)
class DispatchPolicy:
    attempts: int = 2


def dispatch(record, provider, *, attempts=2):
    policy = DispatchPolicy(attempts)
    account = record.get("account_id")
    amount = record.get("amount_cents")
    if not account or not amount:
        raise ValueError("invalid invoice")
    request = {"customer": account, "total": amount}
    return provider(request)
