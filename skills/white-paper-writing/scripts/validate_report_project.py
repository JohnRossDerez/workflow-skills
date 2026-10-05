#!/usr/bin/env python3
"""Check report records and release freshness; semantic and visual review remain explicit."""

from __future__ import annotations

import argparse
from datetime import date
from decimal import Decimal, InvalidOperation
from pathlib import Path
import re
import subprocess

from report_common import (
    FORMATS, MODES, RECORDS, TRACKED_DIRS, citation_ids, content_digest,
    image_paths, load_records, local_path, pandoc_ast, read_json,
    rendered_numbers, required_reviews, sha256,
)
from tree_workflow import validate_architecture, validate_orchestration


def validate(project: Path, release: bool = False) -> tuple[list[str], list[str]]:
    project = project.resolve()
    errors, warnings = [], []

    def readiness(message):
        (errors if release else warnings).append(message)

    def require(condition, message):
        if not condition:
            errors.append(message)

    def file_exists(relative, label, tracked=False):
        try:
            path = local_path(project, relative)
            if tracked and Path(relative).parts[0] not in TRACKED_DIRS:
                raise ValueError(f"input must live in a fingerprinted directory: {relative}")
            if not path.is_file():
                raise ValueError(f"missing file: {relative}")
            return path
        except (ValueError, TypeError) as exc:
            errors.append(f"{label}: {exc}")
            return None

    def nonempty(row, fields, label):
        for field in fields:
            require(isinstance(row.get(field), str) and bool(row[field].strip()), f"{label}: missing text field {field}")

    try:
        config = read_json(project / "project.json")
        if not isinstance(config, dict):
            raise ValueError("project.json must be an object")
        workflow = config.get("workflow", "full")
        require(workflow in {"compact", "full"}, "invalid workflow; choose compact or full")
        require(config.get("schema_version") == 1, "unsupported schema_version; migrate explicitly")
        require(isinstance(config.get("reader_test_required", False), bool), "reader_test_required must be a boolean")
        require(config.get("mode") in MODES, "invalid mode")
        require(config.get("depth") in {"targeted", "standard", "extended"}, "invalid depth")
        require(config.get("structure") in {"preserve", "flexible"}, "invalid structure")
        require(config.get("approval_policy") in {"adaptive", "gated", "preapproved"}, "invalid approval_policy")
        nonempty(config, ["title"], "project")
        for field in ("pdf_header", "reference_doc"):
            if config.get(field):
                file_exists(config[field], field, tracked=True)
        formats = config.get("formats")
        if not isinstance(formats, list) or not formats or any(fmt not in FORMATS for fmt in formats):
            raise ValueError("formats must be a nonempty list drawn from md,pdf,docx")
        require(len(set(formats)) == len(formats), "duplicate requested formats")
        gates = config.get("gates", [])
        if not isinstance(gates, list):
            raise ValueError("gates must be a list")
        for gate in gates:
            nonempty(gate, ["gate_id", "status", "decision_file"], "gate")
            require(gate.get("status") in {"pending", "approved", "waived"}, "invalid gate status")
            file_exists(gate.get("decision_file"), "gate decision")
            if gate.get("status") == "pending":
                readiness(f"human gate pending: {gate.get('gate_id')}")
        if config.get("approval_policy") == "gated" and not gates:
            readiness("gated policy has no configured gates")
        required_files = ("report.md", "planning/brief.md", "planning/plan.md") if workflow == "compact" else (
            "report.md", "planning/brief.md", "planning/research.md", "planning/architecture.json",
            "control/decisions.md", "control/state.json", "control/orchestration.json", "control/agent-runs.json",
        )
        for relative in required_files:
            path = file_exists(relative, "workspace")
            if workflow == "compact" and path and relative in {"planning/brief.md", "planning/plan.md"}:
                prose = re.sub(r"<!--.*?-->", "", path.read_text(encoding="utf-8"), flags=re.S)
                prose = re.sub(r"^\s*#{1,6}\s+.*$", "", prose, flags=re.M)
                require(bool(re.search(r"\w", prose)), f"{relative}: substantive nonempty text required")
        records = load_records(project)
        indexes = {}
        for name, rows in records.items():
            if not isinstance(rows, list) or any(not isinstance(row, dict) for row in rows):
                raise ValueError(f"{RECORDS[name]} must be a list of objects")
            ids = [row.get("id") for row in rows]
            if any(not isinstance(key, str) or not re.fullmatch(r"[A-Za-z][A-Za-z0-9_-]*", key) for key in ids):
                raise ValueError(f"{name}: invalid or missing ID")
            require(len(set(ids)) == len(ids), f"{name}: duplicate IDs")
            indexes[name] = {row["id"]: row for row in rows}

        if workflow != "compact":
            tree_errors, tree_warnings = validate_architecture(
                project, release=release, claim_ids=set(indexes["claims"]),
                claim_records=indexes["claims"], purpose=config["mode"],
            )
            errors.extend(tree_errors)
            warnings.extend(tree_warnings)
            errors.extend(validate_orchestration(project))

        for source in records["sources"]:
            label = f"source {source['id']}"
            nonempty(source, ["title", "reference", "url_or_path", "source_type", "origin_id", "limitations"], label)
            for field in ("published_date", "retrieved_date"):
                value = source.get(field)
                if value:
                    try:
                        date.fromisoformat(value)
                    except (ValueError, TypeError):
                        errors.append(f"{label}: {field} must be an ISO date or empty")
            url = source.get("url_or_path", "")
            if url.startswith(("http://", "https://")):
                require(bool(source.get("retrieved_date")), f"{label}: missing retrieval date")
            elif url:
                file_exists(url, label, tracked=True)
            if source.get("archive_path"):
                file_exists(source["archive_path"], label, tracked=True)
            elif not source.get("archive_exception"):
                readiness(f"{label}: archive file or reason for unavailable retention required")

        for calc in records["calculations"]:
            label = f"calculation {calc['id']}"
            nonempty(calc, ["description", "formula", "units", "time_basis", "assumptions"], label)
            for field in ("inputs", "outputs"):
                values = calc.get(field)
                require(isinstance(values, list) and bool(values), f"{label}: nonempty {field} required")
                if isinstance(values, list):
                    for value in values:
                        file_exists(value, label, tracked=True)
            file_exists(calc.get("code_path"), label, tracked=True)

        for number in records["numbers"]:
            label = f"number {number['id']}"
            nonempty(number, ["unit", "time_basis"], label)
            try:
                raw = Decimal(str(number["value"]))
                display = Decimal(str(number["display_value"]).replace(",", ""))
                precision = number["decimal_places"]
                if isinstance(precision, bool) or not isinstance(precision, int) or not 0 <= precision <= 12:
                    raise ValueError("decimal_places must be an integer from 0 to 12")
                if not raw.is_finite() or not display.is_finite():
                    raise ValueError("values must be finite")
                tolerance = Decimal(5).scaleb(-precision - 1)
                require(abs(raw - display) <= tolerance, f"{label}: display differs from value beyond rounding tolerance")
                require(display == display.quantize(Decimal(1).scaleb(-precision)), f"{label}: display has more precision than declared")
            except (KeyError, ValueError, InvalidOperation) as exc:
                errors.append(f"{label}: invalid numeric record: {exc}")
            source_id, calc_id = number.get("source_id"), number.get("calculation_id")
            require(bool(source_id or calc_id), f"{label}: source_id or calculation_id required")
            if source_id:
                require(source_id in indexes["sources"], f"{label}: unknown source {source_id}")
            if calc_id:
                require(calc_id in indexes["calculations"], f"{label}: unknown calculation {calc_id}")

        for evidence in records["links"]:
            label = f"evidence link {evidence['id']}"
            require(evidence.get("claim_id") in indexes["claims"], f"{label}: unknown claim")
            require(evidence.get("source_id") in indexes["sources"], f"{label}: unknown source")
            nonempty(evidence, ["locator", "excerpt"], label)
            require(evidence.get("relation") in {"direct", "partial", "context", "contradicts"}, f"{label}: invalid relation")
            require(evidence.get("verification") in {"pending", "verified", "failed"}, f"{label}: invalid verification")
            if evidence.get("verification") == "verified":
                nonempty(evidence, ["reviewer", "assessment"], label)

        raw_text = (project / "report.md").read_text(encoding="utf-8")
        text = rendered_numbers(raw_text, records["numbers"])
        paragraphs = re.split(r"\n\s*\n", text)
        if not re.sub(r"<!--.*?-->", "", text, flags=re.S).strip():
            readiness("report has no substantive content")
        if re.search(r"\bTODO\b|\bTBD\b|@@[A-Z_]+@@|\{\{number:", text):
            readiness("unresolved placeholder in manuscript")
        emitted = []
        types = {"external_observation", "internal_observation", "company_claim", "derived", "assumption", "projection", "interpretation"}
        derivation_edges = {}
        for claim in records["claims"]:
            label = f"claim {claim['id']}"
            nonempty(claim, ["text"], label)
            require(claim.get("type") in types, f"{label}: invalid type")
            require(claim.get("status") in {"proposed", "supported", "qualified", "unsupported", "rejected", "superseded"}, f"{label}: invalid status")
            require(claim.get("importance") in {"high", "medium", "low"}, f"{label}: invalid importance")
            require(type(claim.get("emitted")) is bool, f"{label}: emitted must be boolean")
            for field in ("derived_from", "qualified_by", "contradicted_by"):
                related = claim.get(field, [])
                require(isinstance(related, list) and all(isinstance(value, str) for value in related), f"{label}: {field} must be a list of claim IDs")
                if isinstance(related, list):
                    require(len(set(related)) == len(related), f"{label}: duplicate IDs in {field}")
                    for related_id in related:
                        require(related_id in indexes["claims"], f"{label}: unknown claim {related_id} in {field}")
                        require(related_id != claim["id"], f"{label}: cannot relate to itself in {field}")
            derivation_edges[claim["id"]] = claim.get("derived_from", []) if isinstance(claim.get("derived_from", []), list) else []
            calc_id = claim.get("calculation_id")
            if calc_id:
                require(calc_id in indexes["calculations"], f"{label}: unknown calculation")
            if not claim.get("emitted"):
                continue
            emitted.append(claim)
            if claim.get("status") not in {"supported", "qualified"}:
                readiness(f"{label}: emitted claim is {claim.get('status')}")
            excerpt = rendered_numbers(claim.get("report_excerpt", ""), records["numbers"])
            matching = [paragraph for paragraph in paragraphs if excerpt and excerpt in paragraph]
            require(bool(matching), f"{label}: report_excerpt not found in one manuscript paragraph")
            qualification = claim.get("required_qualification", "")
            if claim.get("status") == "qualified" and not qualification:
                readiness(f"{label}: qualified claim needs required_qualification")
            if qualification:
                require(any(qualification in paragraph for paragraph in matching), f"{label}: qualification missing from claim paragraph")
            if claim.get("type") == "company_claim":
                require(claim.get("publication_authorization") in {"approved", "pending", "public"}, f"{label}: invalid publication_authorization")
                if claim.get("publication_authorization") == "pending":
                    readiness(f"{label}: company publication authorization pending")
                nonempty(claim, ["attribution"], label)
                require(any(claim.get("attribution", "") in paragraph for paragraph in matching), f"{label}: company attribution missing")
            links = [row for row in records["links"] if row.get("claim_id") == claim["id"]]
            support = [row for row in links if row.get("verification") == "verified" and row.get("relation") in {"direct", "partial"}]
            if claim.get("type") == "external_observation" and matching:
                adjacent = set(citation_ids(pandoc_ast("\n\n".join(matching), project)))
                require(bool(adjacent & {row.get("source_id") for row in support}), f"{label}: external observation lacks an adjacent supporting citation")
            if not support and not calc_id:
                readiness(f"{label}: no verified supporting evidence or calculation path")
            if claim.get("status") == "supported" and support and all(row["relation"] == "partial" for row in support) and not calc_id:
                readiness(f"{label}: partial evidence requires a qualified claim")
            for evidence in links:
                if evidence.get("verification") != "verified":
                    readiness(f"{label}: linked passage {evidence['id']} not verified")
                if evidence.get("relation") == "contradicts" and not evidence.get("disposition"):
                    readiness(f"{label}: contradiction {evidence['id']} has no disposition")
        visiting, complete = [], set()

        def visit_derivation(claim_id):
            if claim_id in visiting:
                cycle = visiting[visiting.index(claim_id):] + [claim_id]
                errors.append(f"claims: derivation cycle {' -> '.join(cycle)}")
                return
            if claim_id in complete:
                return
            visiting.append(claim_id)
            for basis_id in derivation_edges.get(claim_id, []):
                if basis_id in derivation_edges:
                    visit_derivation(basis_id)
            visiting.pop()
            complete.add(claim_id)

        for claim_id in derivation_edges:
            visit_derivation(claim_id)
        if not emitted:
            readiness("no material claims declared as emitted; record coverage or use the lightweight review workflow")

        ast = pandoc_ast(text, project)
        cited = citation_ids(ast)
        for key in cited:
            require(key in indexes["sources"], f"unregistered citation: {key}")
        images = image_paths(ast)
        figures = {row.get("path"): row for row in records["figures"]}
        for path in images:
            file_exists(path, "manuscript image")
            require(path in figures, f"unregistered manuscript figure: {path}")
        for figure in records["figures"]:
            label = f"figure {figure['id']}"
            nonempty(figure, ["source_note", "units", "time_basis"], label)
            file_exists(figure.get("path"), label, tracked=True)
            file_exists(figure.get("data_path"), label, tracked=True)

        issues = read_json(project / "qa/issues.json")
        if not isinstance(issues, list):
            raise ValueError("qa/issues.json must be a list")
        for issue in issues:
            nonempty(issue, ["id", "description", "status", "severity"], "QA issue")
            require(issue.get("severity") in {"blocker", "material", "minor"}, "invalid issue severity")
            require(issue.get("status") in {"open", "resolved", "accepted"}, "invalid issue status")
            if issue.get("status") == "accepted":
                nonempty(issue, ["disposition"], f"issue {issue.get('id')}")
                if issue.get("severity") == "blocker":
                    readiness(f"issue {issue.get('id')}: blockers must be resolved, not accepted")
            if issue.get("status") == "open":
                if issue.get("severity") in {"blocker", "material"}:
                    readiness(f"open {issue['severity']} issue: {issue['id']}")
                else:
                    warnings.append(f"open minor issue: {issue['id']}")

        if release:
            digest = content_digest(project)
            build = read_json(project / "output/build.json")
            require(build.get("content_digest") == digest, "build is stale: tracked content changed")
            expected = {f"output/report.{fmt}" for fmt in formats}
            artifacts = build.get("artifacts", {})
            require(set(artifacts) == expected, "build artifact list differs from requested formats")
            for relative, fingerprint in artifacts.items():
                path = file_exists(relative, "release artifact")
                if path:
                    require(sha256(path) == fingerprint, f"artifact changed after build: {relative}")
                    require(path.stat().st_size > 0, f"empty release artifact: {relative}")
            require(build.get("citations") == cited, "build citation inventory differs from manuscript")
            require(set(build.get("toolchain", {})) == {"report_common.py", "build_report.py"}, "missing build toolchain fingerprints")
            for script, fingerprint in build.get("toolchain", {}).items():
                path = Path(__file__).parent / script
                require(path.is_file() and sha256(path) == fingerprint, f"build helper changed: {script}; rebuild")
            reviews = read_json(project / "qa/reviews.json")
            if not isinstance(reviews, list):
                raise ValueError("qa/reviews.json must be a list")
            latest = {row["kind"]: row for row in reviews}
            for kind in sorted(required_reviews(config)):
                review = latest.get(kind)
                if not review:
                    errors.append(f"missing review: {kind}")
                    continue
                require(review.get("content_digest") == digest, f"stale {kind} review: content changed")
                require(review.get("artifacts") == artifacts, f"stale {kind} review: artifacts changed")
                nonempty(review, ["reviewer", "method", "checked_at"], f"review {kind}")
                require(review.get("method") in {"independent", "self", "rendered", "tool", "unavailable"}, f"{kind}: invalid review method")
                if kind.startswith("visual:") and review.get("status") == "pass":
                    require(review.get("method") == "rendered", f"{kind}: pass requires rendered inspection")
                if kind == "cold_reader" and review.get("status") == "pass":
                    require(review.get("method") == "independent", "cold_reader: pass requires an independent fresh reader")
                if review.get("status") == "pass":
                    require(review.get("method") != "unavailable", f"{kind}: unavailable check cannot pass")
                path = file_exists(review.get("notes_file"), f"review {kind}")
                if path:
                    require(sha256(path) == review.get("notes_sha256"), f"{kind}: review notes changed")
                if review.get("status") == "waived":
                    if kind not in {"visual:pdf", "visual:docx", "cross_format"}:
                        errors.append(f"{kind}: evidence and editorial review cannot be replaced by a waiver")
                    nonempty(review, ["authorization"], f"waiver {kind}")
                    warnings.append(f"{kind} not verified; owner-authorized limitation: {review.get('authorization')}")
                else:
                    require(review.get("status") == "pass", f"{kind} review has not passed")
            require(build.get("status") == "built", "build did not complete")
    except (OSError, ValueError, KeyError, TypeError, AttributeError, subprocess.SubprocessError) as exc:
        errors.append(f"cannot validate project: {exc}")
    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project_directory", type=Path)
    parser.add_argument("--release", action="store_true")
    args = parser.parse_args()
    errors, warnings = validate(args.project_directory, args.release)
    for message in warnings:
        print(f"WARNING: {message}")
    for message in errors:
        print(f"ERROR: {message}")
    label = "Release controls" if args.release else "Preflight"
    print(f"{label}: {'FAIL' if errors else 'PASS with limitations' if warnings else 'PASS'}; {len(errors)} errors, {len(warnings)} warnings.")
    print("Semantic support, completeness, calculations, and visual quality require the recorded human/agent reviews.")
    return int(bool(errors))


if __name__ == "__main__":
    raise SystemExit(main())
