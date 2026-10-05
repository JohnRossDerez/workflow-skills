import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from workflow import Model, broken_completed_export, run_export


class CheckpointExportTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        self.checkpoint = self.root / "checkpoint.json"
        self.output = self.root / "export.json"

    def snapshot(self, weight, step):
        self.checkpoint.write_text(json.dumps({"weight": weight, "step": step}))

    def test_completed_checkpoint_exports_restored_state_and_releases_resource(self):
        self.snapshot(41, 10)
        model = Model()
        run_export(self.checkpoint, self.output, 10, lambda: model)
        self.assertEqual(json.loads(self.output.read_text()), {"weight": 41, "step": 10})
        self.assertTrue(model.closed)

    def test_interrupted_checkpoint_continues_from_restored_state(self):
        self.snapshot(41, 8)
        model = Model()
        run_export(self.checkpoint, self.output, 10, lambda: model)
        self.assertEqual(json.loads(self.output.read_text()), {"weight": 43, "step": 10})
        self.assertTrue(model.closed)

    def test_failed_training_preserves_previous_artifact_and_releases_resource(self):
        class FailingModel(Model):
            def train_to(self, target_step):
                raise RuntimeError("training interrupted")

        self.snapshot(41, 8)
        self.output.write_text("previous artifact")
        model = FailingModel()
        with self.assertRaisesRegex(RuntimeError, "training interrupted"):
            run_export(self.checkpoint, self.output, 10, lambda: model)
        self.assertEqual(self.output.read_text(), "previous artifact")
        self.assertTrue(model.closed)

    def test_failed_publication_preserves_previous_artifact_and_cleans_pending_file(self):
        self.snapshot(41, 10)
        self.output.write_text("previous artifact")
        model = Model()
        with patch.object(Path, "replace", side_effect=OSError("publication failed")):
            with self.assertRaisesRegex(OSError, "publication failed"):
                run_export(self.checkpoint, self.output, 10, lambda: model)
        self.assertEqual(self.output.read_text(), "previous artifact")
        self.assertFalse(self.output.with_name("export.json.pending").exists())
        self.assertTrue(model.closed)

    def test_malformed_checkpoint_is_rejected_before_acquisition(self):
        self.checkpoint.write_text("null")
        acquired = []
        with self.assertRaises(ValueError):
            run_export(self.checkpoint, self.output, 10, lambda: acquired.append(Model()))
        self.assertEqual(acquired, [])
        self.assertFalse(self.output.exists())

    def test_state_oracle_detects_the_skipped_training_bug(self):
        self.snapshot(41, 10)
        model = Model()
        broken_completed_export(self.checkpoint, self.output, 10, lambda: model)
        self.assertNotEqual(json.loads(self.output.read_text()), {"weight": 41, "step": 10})
        self.assertTrue(model.closed)


if __name__ == "__main__":
    unittest.main()
