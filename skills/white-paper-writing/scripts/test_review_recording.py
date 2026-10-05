"""Review-recording boundary checks; fixtures are not real build/review attestations."""

from pathlib import Path
import tempfile
import unittest

from init_report_project import initialize
from record_review import record_review
from report_common import content_digest, read_json, sha256, write_json


class ReviewRecordingTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.project = Path(self.temporary.name)
        initialize(self.project, "explain", "Synthetic review fixture", ["md"], workflow="compact")
        artifact = self.project / "output/report.md"
        artifact.write_text("Synthetic artifact, not a rendered publication.\n", encoding="utf-8")
        # The persisted build is the input boundary of record_review, not a
        # substitute implementation of its review/history handoff.
        write_json(self.project / "output/build.json", {
            "content_digest": content_digest(self.project),
            "artifacts": {"output/report.md": sha256(artifact)},
        })

    def record(self, notes_file):
        return record_review(self.project, kind="evidence", reviewer="test fixture",
                             method="self", notes_file=notes_file, status="pass")

    def test_separate_notes_remain_bound_after_history_append(self):
        notes = self.project / "qa/evidence.md"
        notes.write_text("Synthetic test notes, not an actual evidence review.\n", encoding="utf-8")
        self.record("qa/evidence.md")
        self.record("qa/evidence.md")
        history = read_json(self.project / "qa/reviews.json")
        self.assertEqual(len(history), 2)
        self.assertTrue(all(row["notes_sha256"] == sha256(notes) for row in history))

    def test_history_alias_rejected_without_appending(self):
        history = self.project / "qa/reviews.json"
        before = history.read_bytes()
        for alias in ("qa/reviews.json", "./qa/reviews.json", "qa/../qa/reviews.json"):
            with self.subTest(alias=alias):
                with self.assertRaisesRegex(ValueError, "separate review notes"):
                    self.record(alias)
                self.assertEqual(history.read_bytes(), before)


if __name__ == "__main__":
    unittest.main(verbosity=2)
