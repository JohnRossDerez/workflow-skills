#!/usr/bin/env python3
"""Bind an actually performed review to its notes, current content, and built artifacts."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path

from report_common import content_digest, local_path, read_json, required_reviews, sha256, write_json


def record_review(project: Path, *, kind: str, reviewer: str, method: str,
                  notes_file: str, status: str, authorization: str = "") -> dict:
    project = project.resolve()
    config = read_json(project / "project.json")
    if kind not in required_reviews(config):
        raise ValueError(f"review kind is not required for this project: {kind}")
    if not reviewer.strip() or method not in {"independent", "self", "rendered", "tool", "unavailable"}:
        raise ValueError("reviewer and a supported method are required")
    if status not in {"pass", "fail", "not_run", "waived"}:
        raise ValueError("invalid review status")
    if kind.startswith("visual:") and status == "pass" and method != "rendered":
        raise ValueError("visual pass requires rendered inspection; extraction is insufficient")
    if kind == "cold_reader" and status in {"pass", "fail"} and method != "independent":
        raise ValueError("cold-reader review requires an independent fresh reader")
    if status == "pass" and method == "unavailable":
        raise ValueError("an unavailable check cannot pass")
    if status == "waived" and (not authorization.strip() or kind not in {"visual:pdf", "visual:docx", "cross_format"}):
        raise ValueError("only artifact-check limitations can be waived, with recorded owner authorization")
    notes = local_path(project, notes_file)
    if not notes.is_file() or not notes.read_text(encoding="utf-8").strip():
        raise ValueError("write substantive review notes before recording the result")
    if notes in {(project / "qa/reviews.json").resolve(), (project / "qa/issues.json").resolve()}:
        raise ValueError("use a separate review notes file")
    build = read_json(project / "output/build.json")
    digest = content_digest(project)
    if build.get("content_digest") != digest:
        raise ValueError("build is stale; rebuild before recording release QA")
    for relative, fingerprint in build["artifacts"].items():
        if sha256(local_path(project, relative)) != fingerprint:
            raise ValueError(f"built artifact changed: {relative}")
    record = {
        "kind": kind, "status": status, "reviewer": reviewer, "method": method,
        "notes_file": notes_file, "notes_sha256": sha256(notes),
        "content_digest": digest, "artifacts": build["artifacts"],
        "checked_at": datetime.now(timezone.utc).isoformat(),
    }
    if authorization:
        record["authorization"] = authorization
    path = project / "qa/reviews.json"
    reviews = read_json(path)
    if not isinstance(reviews, list):
        raise ValueError("qa/reviews.json must be a list")
    reviews.append(record)
    write_json(path, reviews)
    return record


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project_directory", type=Path)
    parser.add_argument("--kind", required=True)
    parser.add_argument("--reviewer", required=True)
    parser.add_argument("--method", choices=["independent", "self", "rendered", "tool", "unavailable"], required=True)
    parser.add_argument("--notes-file", required=True)
    parser.add_argument("--status", choices=["pass", "fail", "not_run", "waived"], required=True)
    parser.add_argument("--authorization", default="")
    args = parser.parse_args()
    try:
        row = record_review(args.project_directory, kind=args.kind, reviewer=args.reviewer,
                            method=args.method, notes_file=args.notes_file, status=args.status,
                            authorization=args.authorization)
    except (OSError, ValueError, KeyError) as exc:
        print(f"REVIEW NOT RECORDED: {exc}")
        return 1
    print(f"Recorded {row['kind']}: {row['status']} against content {row['content_digest'][:12]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
