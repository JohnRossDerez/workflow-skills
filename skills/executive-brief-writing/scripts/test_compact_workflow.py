#!/usr/bin/env python3
"""Compact boundary checks; review records are synthetic test attestations only."""

from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

from build_report import build
from init_report_project import initialize
from report_common import RECORDS, read_json, write_json
import test_report_workflow as full_regression
from validate_report_project import validate


class InitializationTests(unittest.TestCase):
    def test_compact_scaffold_and_cli_default(self):
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory) / "project"
            subprocess.run([sys.executable, str(Path(__file__).with_name("init_report_project.py")),
                            str(project), "--title", "Compact", "--formats", "md"], check=True,
                           capture_output=True, text=True)
            self.assertEqual(read_json(project / "project.json")["workflow"], "compact")
            expected = {"project.json", "report.md", "planning/brief.md", "planning/plan.md",
                        "qa/issues.json", "qa/reviews.json", *RECORDS.values()}
            self.assertEqual({p.relative_to(project).as_posix() for p in project.rglob("*") if p.is_file()}, expected)
            self.assertFalse((project / "drafts").exists())
            self.assertFalse((project / "control").exists())
            before = self.snapshot(project)
            initialize(project, "decide", "Preserve", ["docx"], workflow="compact")
            self.assertEqual(before, self.snapshot(project))

    @staticmethod
    def snapshot(project):
        return {str(p.relative_to(project)): p.read_bytes() if p.is_file() else None
                for p in project.rglob("*")}

    def test_cross_workflow_reinitialization_never_mutates(self):
        for original, requested in (("compact", "full"), ("full", "compact")):
            with self.subTest(original=original), tempfile.TemporaryDirectory() as directory:
                project = Path(directory)
                initialize(project, "explain", "Existing", ["md"], workflow=original)
                before = self.snapshot(project)
                with self.assertRaisesRegex(ValueError, "workflow differs"):
                    initialize(project, "decide", "Changed", ["docx"], workflow=requested)
                self.assertEqual(before, self.snapshot(project))

    def test_absent_workflow_is_legacy_full_and_preserved(self):
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            initialize(project, "explain", "Legacy", ["md"])
            config = read_json(project / "project.json")
            config.pop("workflow")
            write_json(project / "project.json", config)
            before = self.snapshot(project)
            with self.assertRaisesRegex(ValueError, "workflow differs"):
                initialize(project, "explain", "Legacy", ["md"], workflow="compact")
            self.assertEqual(before, self.snapshot(project))
            initialize(project, "explain", "Legacy", ["md"])
            self.assertEqual(before, self.snapshot(project))

    def test_invalid_workflow_rejected_before_creation_or_repair(self):
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory) / "new"
            with self.assertRaisesRegex(ValueError, "workflow must"):
                initialize(project, "explain", "Invalid", ["md"], workflow="unknown")
            self.assertFalse(project.exists())
            initialize(project, "explain", "Invalid", ["md"], workflow="compact")
            config = read_json(project / "project.json")
            config["workflow"] = "unknown"
            write_json(project / "project.json", config)
            before = self.snapshot(project)
            with self.assertRaisesRegex(ValueError, "existing workflow"):
                initialize(project, "explain", "Invalid", ["md"], workflow="compact")
            self.assertEqual(before, self.snapshot(project))


@unittest.skipUnless(shutil.which("pandoc"), "Pandoc required")
class CompactWorkflowTests(unittest.TestCase):
    workflow = "compact"
    tearDown = full_regression.ReportWorkflowTests.tearDown
    change = full_regression.ReportWorkflowTests.change
    review = full_regression.ReportWorkflowTests.review
    complete_md = full_regression.ReportWorkflowTests.complete_md
    assert_error = full_regression.ReportWorkflowTests.assert_error

    def setUp(self):
        full_regression.ReportWorkflowTests.setUp(self)
        (self.project / "planning/brief.md").write_text(
            "The internal reader needs the observed sample count, with Markdown delivery and no forecast.\n")
        (self.project / "planning/plan.md").write_text(
            "Reader outcome: understand the observed count and sample limits. Thesis: the sample contains 40 systems.\n\n"
            "1. Present the observation.\n2. Explain its sample limitation.\n\n"
            "The observation depends on the retained source and verified evidence link; representativeness is unknown.\n")

    def test_compact_real_markdown_release(self):
        self.assertEqual(validate(self.project)[0], [])
        self.complete_md()
        errors, warnings = validate(self.project, True)
        self.assertEqual(errors, [])
        self.assertEqual(warnings, [])
        self.assertIn("40 systems", (self.project / "output/report.md").read_text())
        self.assertEqual(set(read_json(self.project / "output/build.json")["artifacts"]), {"output/report.md"})

    def test_source_change_after_bound_reviews_rejects_build_and_all_reviews(self):
        self.complete_md()
        (self.project / "sources/observations.txt").write_text("Observed sample: 41 systems.\n")
        self.assert_error("build is stale", True)
        for kind in ("evidence", "editorial", "cold_reader"):
            self.assert_error(f"stale {kind} review: content changed", True)
        build(self.project)
        for kind in ("evidence", "editorial", "cold_reader"):
            self.assert_error(f"stale {kind} review: content changed", True)

    def test_changed_planning_input_invalidates_release(self):
        self.complete_md()
        with (self.project / "planning/plan.md").open("a") as handle:
            handle.write("\nNew limit: observation period is unknown.\n")
        self.assert_error("build is stale", True)
        self.assert_error("stale cold_reader review", True)

    def test_changed_artifact_and_review_notes_rejected(self):
        self.complete_md()
        (self.project / "output/report.md").write_text("Tampered artifact")
        self.assert_error("artifact changed after build", True)
        (self.project / "qa/evidence.md").write_text("Tampered synthetic attestation")
        self.assert_error("review notes changed", True)

    def test_changed_review_artifact_binding_rejected(self):
        self.complete_md()
        self.change("qa/reviews.json", lambda rows: rows[0].update(artifacts={}))
        self.assert_error("stale evidence review: artifacts changed", True)

    def test_compact_requires_independent_cold_reader(self):
        build(self.project)
        self.review("evidence")
        self.review("editorial")
        self.assert_error("missing review: cold_reader", True)
        with self.assertRaisesRegex(ValueError, "independent fresh reader"):
            self.review("cold_reader", method="self")
        self.review("cold_reader", method="independent")
        self.assertEqual(validate(self.project, True)[0], [])

    def test_qualified_claim_cannot_lose_qualification(self):
        self.change("evidence/claims.json", lambda rows: rows[0].update(
            report_excerpt="{{number:N01}} systems were observed."))
        path = self.project / "report.md"
        path.write_text(path.read_text().replace("In this sample, ", ""))
        self.assert_error("qualification missing from claim paragraph")

    def test_unknown_evidence_source_rejected(self):
        self.change("evidence/links.json", lambda rows: rows[0].update(source_id="UNKNOWN"))
        self.assert_error("evidence link E01: unknown source")

    def test_missing_compact_plan_rejected(self):
        (self.project / "planning/plan.md").unlink()
        self.assert_error("missing file: planning/plan.md")

    def test_compact_brief_and_plan_need_prose_without_fixed_headings(self):
        for relative in ("planning/brief.md", "planning/plan.md"):
            with self.subTest(relative=relative):
                path = self.project / relative
                original = path.read_text()
                for empty in ("", "# Only a heading\n\n<!-- guidance -->\n", "   \n---\n"):
                    path.write_text(empty)
                    self.assert_error(f"{relative}: substantive nonempty text required")
                path.write_text(original)
        self.assertEqual(validate(self.project)[0], [])

    def test_invalid_workflow_config_rejected(self):
        self.change("project.json", lambda config: config.update(workflow="unknown"))
        self.assert_error("invalid workflow")

    def test_full_graph_validation_remains_active_for_legacy_default(self):
        self.change("project.json", lambda config: config.pop("workflow"))
        self.assert_error("missing file: planning/architecture.json")


if __name__ == "__main__":
    unittest.main(verbosity=2)
