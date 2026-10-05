from collections.abc import Mapping
from dataclasses import dataclass


@dataclass(frozen=True)
class Invoice:
    account_id: str
    amount_cents: int


def parse_invoice(record) -> Invoice:
    if not isinstance(record, Mapping):
        raise ValueError("invoice must be a mapping")
    account = record.get("account_id")
    amount = record.get("amount_cents")
    if not isinstance(account, str) or not account:
        raise ValueError("account_id must be nonempty")
    if type(amount) is not int or amount <= 0:
        raise ValueError("amount_cents must be positive")
    return Invoice(account, amount)


def validate_attempts(attempts):
    if type(attempts) is not int or attempts < 1:
        raise ValueError("attempts must be a positive integer")


def send_invoice(invoice: Invoice, provider, attempts):
    request = {"account_id": invoice.account_id, "amount_cents": invoice.amount_cents}
    for attempt in range(attempts):
        try:
            return provider(request)
        except TimeoutError:
            if attempt == attempts - 1:
                raise


def dispatch(record, provider, *, attempts=2):
    validate_attempts(attempts)
    return send_invoice(parse_invoice(record), provider, attempts)


def dispatch_batch(records, provider, *, attempts=2):
    validate_attempts(attempts)
    receipts, rejected = [], []
    for position, record in enumerate(records):
        try:
            invoice = parse_invoice(record)
        except ValueError:
            rejected.append(position)
            continue
        receipts.append(send_invoice(invoice, provider, attempts))
    return {"receipts": receipts, "rejected": rejected}
