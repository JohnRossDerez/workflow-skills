#!/usr/bin/env python3
"""Isolated regression checks for record integrity, rendering, and review freshness."""

from __future__ import annotations

import json
from pathlib import Path
import shutil
import struct
import subprocess
import tempfile
import unittest
import zipfile
import zlib

from build_report import build
from init_report_project import initialize
from record_review import record_review
from report_common import MODES, read_json, write_json
from tree_workflow import dependent_record_ids, disclosure_rows, invalidate, ready_nodes
from validate_report_project import validate


@unittest.skipUnless(shutil.which("pandoc"), "Pandoc required")
class ReportWorkflowTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="report_skill_test_")
        self.project = Path(self.temp.name)
        initialize(self.project, "investigate", "Observation note", ["md"],
                   workflow=getattr(self, "workflow", "full"))
        (self.project / "sources/observations.txt").write_text("Observed sample: 40 systems.\n", encoding="utf-8")
        write_json(self.project / "evidence/sources.json", [{
            "id": "S01", "title": "Observations", "reference": "Internal research. Observations. 2026.",
            "url_or_path": "https://example.org/observations", "retrieved_date": "2026-09-08",
            "source_type": "internal_dataset", "origin_id": "O01", "limitations": "Sample only.",
            "archive_path": "sources/observations.txt",
        }])
        write_json(self.project / "evidence/claims.json", [{
            "id": "C01", "text": "40 observed systems", "type": "internal_observation",
            "status": "qualified", "importance": "high", "emitted": True,
            "report_excerpt": "In this sample, {{number:N01}} systems were observed.",
            "required_qualification": "In this sample",
        }])
        write_json(self.project / "evidence/links.json", [{
            "id": "E01", "claim_id": "C01", "source_id": "S01", "locator": "line 1",
            "excerpt": "Observed sample: 40 systems.", "relation": "direct",
            "verification": "verified", "reviewer": "test fixture", "assessment": "Fixture literal agrees.",
        }])
        write_json(self.project / "evidence/numbers.json", [{
            "id": "N01", "value": "40", "display_value": "40", "decimal_places": 0,
            "unit": "systems", "time_basis": "sample snapshot", "source_id": "S01",
        }])
        (self.project / "report.md").write_text(
            "# Findings\n\nIn this sample, {{number:N01}} systems were observed. [@S01, p. 1]\n\n"
            "Citation syntax example: `[@NOT_A_CITATION]`.\n", encoding="utf-8",
        )
        if getattr(self, "workflow", "full") == "full":
            tree = read_json(self.project / "planning/architecture.json")
            tree["nodes"][0].update(
                answer="The observed sample contains 40 systems.",
                new_information="The sample contains 40 observed systems.",
                claim_ids=["C01"],
                status="validated",
            )
            write_json(self.project / "planning/architecture.json", tree)
            message = read_json(self.project / "planning/message.json")
            message.update(
                status="defined", reader_start="The reader does not know the observed count.",
                reader_end="The reader knows the observed count and its sample limitation.",
                communicative_thesis="The observed sample contains 40 systems.",
                central_tension="The observation is useful but does not establish a forecast.",
            )
            write_json(self.project / "planning/message.json", message)

    def tearDown(self):
        self.temp.cleanup()

    def change(self, relative, edit):
        path = self.project / relative
        value = read_json(path)
        edit(value)
        write_json(path, value)

    def review(self, kind="evidence", method="self", status="pass", authorization=""):
        relative = f"qa/{kind.replace(':', '-')}.md"
        (self.project / relative).write_text(
            "Synthetic regression-test attestation; not a real report review.\n", encoding="utf-8",
        )
        return record_review(self.project, kind=kind, reviewer="test fixture", method=method,
                             notes_file=relative, status=status, authorization=authorization)

    def complete_md(self):
        build(self.project)
        self.review("evidence")
        self.review("editorial")
        self.review("cold_reader", method="independent")

    def assert_error(self, phrase, release=False):
        errors, _ = validate(self.project, release)
        self.assertTrue(any(phrase in error for error in errors), errors)

    def test_all_modes_and_idempotent_initialization(self):
        original = (self.project / "report.md").read_bytes()
        for mode in MODES:
            initialize(self.project, mode, "Different title", ["docx"])
        self.assertEqual((self.project / "report.md").read_bytes(), original)
        self.assertEqual(read_json(self.project / "project.json")["formats"], ["md"])
        for mode in MODES:
            self.change("project.json", lambda config: config.update(mode=mode))
            self.change("planning/architecture.json", lambda tree: tree.update(purpose=mode))
            self.assertEqual(validate(self.project)[0], [])

    def test_tree_ready_nodes_follow_bottom_up_order(self):
        tree = {
            "nodes": [
                {"id": "ROOT", "parent_id": None, "status": "supported", "dependencies": []},
                {"id": "LEAF", "parent_id": "ROOT", "status": "supported", "dependencies": []},
            ]
        }
        self.assertEqual([node["id"] for node in ready_nodes(tree, "draft")], ["LEAF"])
        tree["nodes"][1]["status"] = "drafted"
        self.assertEqual([node["id"] for node in ready_nodes(tree, "draft")], ["ROOT"])

    def test_combined_containment_and_dependency_cycle_fails(self):
        def add_child_cycle(tree):
            tree["nodes"].append({
                "id": "CHILD", "parent_id": "N0", "kind": "leaf", "title": "Child",
                "question": "What supports the parent?", "answer": "", "reader_outcome": "Support is visible.",
                "acceptance_criteria": "The dependency order is valid.", "claim_ids": [], "basis_claim_ids": [],
                "dependencies": ["N0"], "requires_concept_ids": [], "introduces_concept_ids": [],
                "budget_words": 50, "status": "planned", "draft_path": "drafts/CHILD.md", "sequence": 1,
            })

        self.change("planning/architecture.json", add_child_cycle)
        self.assert_error("compile cycle")

    def test_tree_invalidation_reaches_dependents_and_ancestors(self):
        tree = {
            "nodes": [
                {"id": "ROOT", "parent_id": None, "status": "validated", "dependencies": []},
                {"id": "A", "parent_id": "ROOT", "status": "validated", "dependencies": []},
                {"id": "B", "parent_id": "ROOT", "status": "validated", "dependencies": ["A"]},
            ]
        }
        self.assertEqual(invalidate(tree, {"A"}), {"ROOT", "A", "B"})
        self.assertTrue(all(node["status"] == "planned" for node in tree["nodes"]))

    def test_graph_invalidation_accepts_concept_and_claim_changes(self):
        tree = {
            "nodes": [
                {"id": "ROOT", "parent_id": None, "status": "validated", "dependencies": [],
                 "requires_concept_ids": [], "introduces_concept_ids": [], "claim_ids": [], "basis_claim_ids": ["C01"]},
                {"id": "A", "parent_id": "ROOT", "status": "validated", "dependencies": [],
                 "requires_concept_ids": ["K01"], "introduces_concept_ids": [], "claim_ids": ["C01"], "basis_claim_ids": []},
            ]
        }
        self.assertEqual(invalidate(tree, set(), changed_concepts={"K01"}), {"ROOT", "A"})
        for node in tree["nodes"]:
            node["status"] = "validated"
        self.assertEqual(invalidate(tree, set(), changed_claims={"C01"}), {"ROOT", "A"})
        records = [
            {"id": "C01", "derived_from": []},
            {"id": "C02", "derived_from": ["C01"]},
            {"id": "C03", "derived_from": ["C02"]},
        ]
        self.assertEqual(dependent_record_ids(records, {"C01"}, ("derived_from",)), {"C01", "C02", "C03"})

    def test_progressive_disclosure_is_parent_first_with_ancestor_context(self):
        def node(node_id, parent_id, sequence):
            return {
                "id": node_id, "parent_id": parent_id, "sequence": sequence,
                "kind": "root" if parent_id is None else "leaf", "title": node_id,
                "question": f"Question {node_id}", "answer": f"Synthesis {node_id}",
                "draft_path": f"drafts/{node_id}.md",
            }
        tree = {
            "root_id": "ROOT",
            "nodes": [node("B", "ROOT", 3), node("A1", "A", 2), node("ROOT", None, 0), node("A", "ROOT", 1)],
        }
        rows = disclosure_rows(tree)
        self.assertEqual([row["id"] for row in rows], ["ROOT", "A", "A1", "B"])
        self.assertEqual([item["id"] for item in rows[2]["ancestor_path"]], ["ROOT", "A"])

    def test_v3_disclosure_uses_narrative_order_and_local_distance(self):
        def node(node_id, parent_id, sequence, introduced=None, required=None, claims=None):
            return {
                "id": node_id, "parent_id": parent_id, "sequence": sequence,
                "kind": "root" if parent_id is None else "leaf", "title": node_id,
                "question": f"Question {node_id}", "answer": f"Synthesis {node_id}",
                "draft_path": f"drafts/{node_id}.md", "reader_outcome": f"Outcome {node_id}",
                "acceptance_criteria": f"Accept {node_id}", "rhetorical_role": "demonstrate",
                "new_information": f"New {node_id}", "handoff": f"Next {node_id}", "visual_role": "none",
                "claim_ids": claims or [], "basis_claim_ids": [], "dependencies": [],
                "requires_concept_ids": required or [], "introduces_concept_ids": introduced or [],
                "budget_words": 50, "status": "supported",
            }

        tree = {
            "schema_version": 3, "root_id": "ROOT",
            "nodes": [
                node("ROOT", None, 2),
                node("A", "ROOT", 0, introduced=["K01"], claims=["C01"]),
                node("B", "ROOT", 1, required=["K01"], claims=["C01"]),
            ],
        }
        concepts = [{
            "id": "K01", "canonical_name": "Known term", "definition": "A test term.",
            "aliases": [], "assumed_known": False, "prerequisite_ids": [], "introduced_at": "A",
        }]
        message = {"proof_direction": "re_earning", "communicative_thesis": "Message"}
        rows = disclosure_rows(tree, concepts=concepts, message=message)
        self.assertEqual([row["id"] for row in rows], ["A", "B", "ROOT"])
        self.assertEqual(rows[1]["previous_beat"]["id"], "A")
        self.assertEqual(rows[1]["next_beat"]["id"], "ROOT")
        self.assertEqual(rows[1]["last_mentions"]["concepts"]["K01"]["beats_back"], 1)
        selected = disclosure_rows(tree, start_id="B", concepts=concepts, message=message)
        self.assertEqual([item["id"] for item in selected[0]["ancestor_path"]], ["ROOT"])
        self.assertEqual(selected[0]["previous_beat"]["id"], "A")

    def test_concept_must_be_introduced_before_use(self):
        self.change("planning/concepts.json", lambda rows: rows.append({
            "id": "K01", "canonical_name": "Recovery horizon", "definition": "The evaluation interval.",
            "aliases": [], "assumed_known": False, "prerequisite_ids": [], "introduced_at": "LATE",
        }))

        def add_late_node(tree):
            tree["nodes"][0]["requires_concept_ids"] = ["K01"]
            tree["nodes"].append({
                "id": "LATE", "parent_id": "N0", "kind": "leaf", "title": "Late definition",
                "question": "What is the horizon?", "answer": "", "reader_outcome": "The reader knows the horizon.",
                "acceptance_criteria": "The term is defined.", "claim_ids": [], "basis_claim_ids": [],
                "dependencies": [], "requires_concept_ids": [], "introduces_concept_ids": ["K01"],
                "budget_words": 50, "status": "planned", "draft_path": "drafts/LATE.md", "sequence": 1,
            })

        self.change("planning/architecture.json", add_late_node)
        self.assert_error("requires K01 before its introduction")

    def test_release_requires_descendant_basis_for_synthesis(self):
        def add_child(tree):
            tree["nodes"].append({
                "id": "LEAF", "parent_id": "N0", "kind": "leaf", "title": "Evidence",
                "question": "What was observed?", "answer": "Forty systems were observed.",
                "reader_outcome": "The reader knows the observation.",
                "acceptance_criteria": "The observation is supported.", "claim_ids": ["C01"],
                "basis_claim_ids": [], "dependencies": [], "requires_concept_ids": [],
                "introduces_concept_ids": [], "budget_words": 50, "status": "validated",
                "draft_path": "report.md", "sequence": 1,
            })
            tree["nodes"][0]["claim_ids"] = []
            tree["nodes"][0]["basis_claim_ids"] = []

        self.change("planning/architecture.json", add_child)
        self.assert_error("synthesis has no descendant claim basis", True)

    def test_release_requires_validated_architecture(self):
        self.change("planning/architecture.json", lambda tree: tree["nodes"][0].update(status="planned"))
        self.assert_error("release requires validated status", True)

    def test_release_requires_defined_message_contract(self):
        self.change("planning/message.json", lambda message: message.update(status="planned"))
        self.assert_error("communication contract remains planned", True)

    def test_orchestration_policy_rejects_excess_concurrency(self):
        self.change("control/orchestration.json", lambda policy: policy.update(max_concurrent_subagents=4))
        self.assert_error("max_concurrent_subagents", False)

    def test_default_agent_profiles_use_explicit_gpt6_sol_or_luna(self):
        policy = read_json(self.project / "control/orchestration.json")
        self.assertIn("cold_reader", policy["roles"])
        profiles = list(policy["roles"].values()) + [
            policy["compatibility_worker"], policy["single_model_fallback"]
        ]
        for profile in profiles:
            self.assertIn(profile["model"], {"gpt-6-sol", "gpt-6-luna"})
            self.assertIn(profile["reasoning_effort"], {"low", "medium", "high", "xhigh", "max"})

    def test_orchestration_rejects_astra(self):
        self.change("control/orchestration.json", lambda policy: policy["roles"]["root"].update(model="gpt-6-astra"))
        self.assert_error("Astra models are prohibited", False)

    def test_cold_reader_agent_run_is_allowed_but_astra_is_not(self):
        self.change("control/agent-runs.json", lambda rows: rows.append({
            "role": "cold_reader", "model": "gpt-6-sol", "reasoning_effort": "medium",
            "status": "completed", "node_ids": [], "artifacts": ["qa/cold-reader.md"],
        }))
        self.assertEqual(validate(self.project)[0], [])
        self.change("control/agent-runs.json", lambda rows: rows[0].update(model="gpt-6-astra"))
        self.assert_error("Astra models are prohibited")

    def test_release_requires_actual_review_records(self):
        build(self.project)
        self.assert_error("missing review: evidence", True)
        self.review("evidence")
        self.review("editorial")
        self.assert_error("missing review: cold_reader", True)
        self.review("cold_reader", method="independent")
        self.assertEqual(validate(self.project, True)[0], [])

    def test_reader_review_is_optional_for_legacy_project(self):
        self.change("project.json", lambda config: config.pop("reader_test_required"))
        build(self.project)
        self.review("evidence")
        self.review("editorial")
        self.assertEqual(validate(self.project, True)[0], [])

    def test_reader_requirement_must_be_boolean(self):
        self.change("project.json", lambda config: config.update(reader_test_required="false"))
        self.assert_error("reader_test_required must be a boolean")

    def test_cold_reader_pass_requires_independence(self):
        build(self.project)
        with self.assertRaisesRegex(ValueError, "independent fresh reader"):
            self.review("cold_reader", method="self")
        self.review("cold_reader", method="independent")
        self.change("qa/reviews.json", lambda rows: rows[-1].update(method="self"))
        self.review("evidence")
        self.review("editorial")
        self.assert_error("cold_reader: pass requires an independent fresh reader", True)

    def test_cold_reader_review_cannot_be_waived(self):
        build(self.project)
        with self.assertRaisesRegex(ValueError, "only artifact-check limitations can be waived"):
            self.review("cold_reader", method="unavailable", status="waived", authorization="Skip reader test")

    def test_number_and_reference_rendering_uses_parsed_citations(self):
        build(self.project)
        text = (self.project / "output/report.md").read_text()
        self.assertIn("40 systems", text)
        self.assertNotIn("{{number:", text)
        self.assertIn("https://example.org/observations", text)
        self.assertIn("NOT_A_CITATION", text)
        self.assertEqual(read_json(self.project / "output/build.json")["citations"], ["S01"])

    def test_markdown_tables_and_reference_anchors_are_portable(self):
        path = self.project / "report.md"
        path.write_text(path.read_text() + "\n| Plan | Cost |\n|---|---:|\n| A | 12000 |\n")
        build(self.project)
        text = (self.project / "output/report.md").read_text()
        self.assertRegex(text, r"\|\s*Plan\s*\|\s*Cost\s*\|")
        self.assertNotIn("::: {", text)
        self.assertIn('id="ref-S01"', text)

    def test_unknown_source_link_fails(self):
        self.change("evidence/links.json", lambda rows: rows[0].update(source_id="MISSING"))
        self.assert_error("unknown source")

    def test_external_fact_needs_adjacent_supporting_citation(self):
        self.change("evidence/claims.json", lambda rows: rows[0].update(type="external_observation"))
        self.assertEqual(validate(self.project)[0], [])
        path = self.project / "report.md"
        path.write_text(path.read_text().replace("[@S01, p. 1]", ""))
        self.assert_error("lacks an adjacent supporting citation")

    def test_untracked_styling_asset_fails(self):
        (self.project / "header.tex").write_text("% untracked header")
        self.change("project.json", lambda config: config.update(pdf_header="header.tex"))
        self.assert_error("fingerprinted directory")

    def test_tampered_review_method_fails(self):
        self.complete_md()
        self.change("qa/reviews.json", lambda rows: rows[0].update(method="unavailable"))
        self.assert_error("unavailable check cannot pass", True)

    def test_failed_build_preserves_existing_artifacts(self):
        self.complete_md()
        original = (self.project / "output/report.md").read_bytes()
        self.change("project.json", lambda config: config.update(formats=["md", "pdf"], pdf_engine="nonexistent"))
        with self.assertRaisesRegex(ValueError, "unsupported pdf_engine"):
            build(self.project)
        self.assertEqual((self.project / "output/report.md").read_bytes(), original)

    def test_duplicate_claim_ids_fail(self):
        self.change("evidence/claims.json", lambda rows: rows.append(dict(rows[0])))
        self.assert_error("duplicate IDs")

    def test_claim_derivation_cycles_fail(self):
        def add_cycle(rows):
            rows[0]["derived_from"] = ["C02"]
            rows.append({
                "id": "C02", "text": "Derived interpretation", "type": "derived",
                "status": "supported", "importance": "low", "emitted": False,
                "derived_from": ["C01"], "qualified_by": [], "contradicted_by": [],
            })

        self.change("evidence/claims.json", add_cycle)
        self.assert_error("derivation cycle")

    def test_missing_qualification_fails(self):
        self.change("evidence/claims.json", lambda rows: rows[0].update(required_qualification="Hypothetical only"))
        self.assert_error("qualification missing")

    def test_wrong_rate_rounding_fails(self):
        self.change("evidence/numbers.json", lambda rows: rows[0].update(value="96.77", display_value="96", unit="percent"))
        self.assert_error("rounding tolerance")

    def test_nonfinite_number_fails(self):
        self.change("evidence/numbers.json", lambda rows: rows[0].update(value="NaN"))
        self.assert_error("finite")

    def test_unused_rejected_claim_is_allowed(self):
        self.change("evidence/claims.json", lambda rows: rows.append({
            "id": "C02", "text": "Rejected draft idea", "type": "interpretation",
            "status": "rejected", "importance": "high", "emitted": False,
        }))
        self.complete_md()
        self.assertEqual(validate(self.project, True)[0], [])

    def test_emitted_rejected_claim_fails_release(self):
        self.change("evidence/claims.json", lambda rows: rows[0].update(status="rejected"))
        self.assert_error("emitted claim is rejected", True)

    def test_context_source_does_not_support_claim(self):
        self.change("evidence/links.json", lambda rows: rows[0].update(relation="context"))
        self.assert_error("no verified supporting evidence", True)

    def test_undisposed_contradiction_fails(self):
        self.change("evidence/links.json", lambda rows: rows.append(dict(rows[0], id="E02", relation="contradicts")))
        self.assert_error("has no disposition", True)

    def test_changed_content_invalidates_build_and_reviews(self):
        self.complete_md()
        (self.project / "sources/observations.txt").write_text("Observed sample: 41 systems.\n")
        self.assert_error("build is stale", True)
        self.assert_error("stale evidence review", True)
        self.assert_error("stale cold_reader review", True)

    def test_changed_artifact_fails(self):
        self.complete_md()
        (self.project / "output/report.md").write_text("Replaced output")
        self.assert_error("artifact changed after build", True)

    def test_changed_notes_fail(self):
        self.complete_md()
        (self.project / "qa/evidence.md").write_text("Different review")
        self.assert_error("review notes changed", True)

    def test_failed_latest_review_supersedes_pass(self):
        self.complete_md()
        self.review("evidence", status="fail")
        self.assert_error("evidence review has not passed", True)

    def test_failed_latest_cold_reader_review_blocks_release(self):
        self.complete_md()
        self.review("cold_reader", method="independent", status="fail")
        self.assert_error("cold_reader review has not passed", True)

    def test_missing_archive_requires_explanation(self):
        self.change("evidence/sources.json", lambda rows: rows[0].pop("archive_path"))
        self.assert_error("archive file or reason", True)

    def test_project_path_escape_fails(self):
        self.change("evidence/sources.json", lambda rows: rows[0].update(archive_path="../outside.txt"))
        self.assert_error("path escapes project")

    def test_malformed_records_fail_closed(self):
        (self.project / "evidence/claims.json").write_text("not JSON")
        self.assert_error("cannot validate")

    def test_open_material_issue_blocks_release(self):
        write_json(self.project / "qa/issues.json", [{"id": "I01", "description": "Incorrect conclusion", "severity": "material", "status": "open"}])
        self.assert_error("open material issue", True)

    def test_pending_explicit_gate_blocks_release(self):
        self.change("project.json", lambda config: config.update(approval_policy="gated", gates=[
            {"gate_id": "mandate", "status": "pending", "decision_file": "control/decisions.md"},
        ]))
        self.assert_error("human gate pending", True)

    @unittest.skipUnless(shutil.which("pdflatex"), "TeX required")
    def test_registered_figure_is_embedded_with_source_note(self):
        def chunk(kind, payload):
            return struct.pack(">I", len(payload)) + kind + payload + struct.pack(">I", zlib.crc32(kind + payload) & 0xffffffff)
        width, height = 160, 80
        pixels = b"".join(b"\x00" + b"".join(
            b"\x35\x65\xa5" if 15 < x < 95 and 20 < y < 65 else b"\xff\xff\xff"
            for x in range(width)) for y in range(height))
        png = b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)) + chunk(b"IDAT", zlib.compress(pixels)) + chunk(b"IEND", b"")
        (self.project / "figures/sample.png").write_bytes(png)
        write_json(self.project / "figures/register.json", [{
            "id": "F01", "path": "figures/sample.png", "data_path": "sources/observations.txt",
            "source_note": "Source: supplied sample observations.", "units": "systems", "time_basis": "snapshot",
        }])
        path = self.project / "report.md"
        path.write_text(path.read_text() + "\n![Observed sample](figures/sample.png)\n")
        self.change("project.json", lambda config: config.update(formats=["md", "pdf", "docx"]))
        build(self.project)
        with zipfile.ZipFile(self.project / "output/report.docx") as archive:
            self.assertTrue(any(name.startswith("word/media/") for name in archive.namelist()))
            self.assertIn(b"Source: supplied sample observations.", archive.read("word/document.xml"))
        self.assertIn("Source: supplied sample observations.", (self.project / "output/report.md").read_text())

    @unittest.skipUnless(shutil.which("pdflatex"), "TeX required")
    def test_multi_format_build_and_visual_review_boundary(self):
        self.change("project.json", lambda config: config.update(formats=["md", "pdf", "docx"]))
        manifest = build(self.project)
        self.assertEqual(set(manifest["artifacts"]), {"output/report.md", "output/report.pdf", "output/report.docx"})
        with zipfile.ZipFile(self.project / "output/report.docx") as archive:
            self.assertIsNone(archive.testzip())
            self.assertIn(b"40", archive.read("word/document.xml"))
            self.assertIn(b"https://example.org/observations", archive.read("word/_rels/document.xml.rels"))
        if shutil.which("pdftotext"):
            text = subprocess.run(["pdftotext", str(self.project / "output/report.pdf"), "-"], text=True, capture_output=True, check=True).stdout
            self.assertIn("40 systems", text)
            self.assertIn("example.org/observations", text)
        with self.assertRaisesRegex(ValueError, "rendered inspection"):
            self.review("visual:docx", method="tool")
        self.review("evidence")
        self.review("editorial")
        self.review("cold_reader", method="independent")
        self.review("visual:pdf", method="rendered")
        self.review("cross_format", method="tool")
        self.review("visual:docx", method="unavailable", status="not_run")
        self.assert_error("visual:docx review has not passed", True)
        self.review("visual:docx", method="unavailable", status="waived", authorization="Synthetic fixture explicitly permits unrendered Word delivery.")
        errors, warnings = validate(self.project, True)
        self.assertEqual(errors, [])
        self.assertTrue(any("not verified" in warning for warning in warnings))


if __name__ == "__main__":
    unittest.main(verbosity=2)
