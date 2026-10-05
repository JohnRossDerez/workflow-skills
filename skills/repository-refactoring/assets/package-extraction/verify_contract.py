"""Run the same public outcome checks against an implementation directory."""

import argparse
import importlib
import sys
import unittest
from pathlib import Path


VALID = {"account_id": "account-7", "amount_cents": 2500}
implementation = None


class DispatchContractTests(unittest.TestCase):
    def test_provider_request_and_receipt_identity(self):
        requests = []
        receipt = {"receipt_id": "r-1"}

        def provider(request):
            requests.append(request)
            return receipt

        result = implementation.dispatch({**VALID, "extra": "ignored"}, provider)
        self.assertIs(result, receipt)
        self.assertEqual(requests, [VALID])

    def test_invalid_records_have_no_provider_effect(self):
        requests = []
        invalid = [None, [], False, {}, {**VALID, "amount_cents": True},
                   {**VALID, "amount_cents": -1}, {**VALID, "account_id": 7}]
        for record in invalid:
            with self.subTest(record=record):
                with self.assertRaises(ValueError):
                    implementation.dispatch(record, requests.append)
        self.assertEqual(requests, [])

    def test_default_retry_reaches_second_attempt(self):
        calls = []

        def provider(request):
            calls.append(request)
            if len(calls) == 1:
                raise TimeoutError("transient")
            return "receipt"

        self.assertEqual(implementation.dispatch(VALID, provider), "receipt")
        self.assertEqual(calls, [VALID, VALID])

    def test_explicit_attempts_govern_execution_and_exhaustion_propagates(self):
        for attempts in (1, 3):
            calls = []
            failure = TimeoutError("unavailable")

            def provider(request):
                calls.append(request)
                raise failure

            with self.subTest(attempts=attempts):
                with self.assertRaises(TimeoutError) as caught:
                    implementation.dispatch(VALID, provider, attempts=attempts)
                self.assertIs(caught.exception, failure)
                self.assertEqual(calls, [VALID] * attempts)

    def test_invalid_attempts_rejected_before_effect(self):
        calls = []
        for attempts in (0, -1, True, 1.5):
            with self.subTest(attempts=attempts):
                with self.assertRaises(ValueError):
                    implementation.dispatch(VALID, calls.append, attempts=attempts)
        self.assertEqual(calls, [])

    def test_provider_failure_is_not_retried_or_converted(self):
        calls = []
        failure = RuntimeError("provider failure")

        def provider(request):
            calls.append(request)
            raise failure

        with self.assertRaises(RuntimeError) as caught:
            implementation.dispatch(VALID, provider)
        self.assertIs(caught.exception, failure)
        self.assertEqual(calls, [VALID])

    def test_mixed_batch_preserves_receipt_order_and_rejection_positions(self):
        other = {"account_id": "account-8", "amount_cents": 1500}
        calls = []

        def provider(request):
            calls.append(request)
            return request["account_id"]

        result = implementation.dispatch_batch([VALID, None, other, {}], provider)
        self.assertEqual(result, {"receipts": ["account-7", "account-8"], "rejected": [1, 3]})
        self.assertEqual(calls, [VALID, other])

    def test_provider_value_error_is_not_a_record_rejection(self):
        failure = ValueError("provider rejected account")

        def provider(request):
            raise failure

        with self.assertRaises(ValueError) as caught:
            implementation.dispatch_batch([VALID], provider)
        self.assertIs(caught.exception, failure)


def main():
    global implementation
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    parser.add_argument("--module", default="legacy_dispatch")
    args = parser.parse_args()
    sys.path.insert(0, str(args.directory.resolve()))
    implementation = importlib.import_module(args.module)
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(DispatchContractTests)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
