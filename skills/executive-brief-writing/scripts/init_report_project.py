#!/usr/bin/env python3
"""Initialize an executive brief project; preserve existing files and refuse legacy migration."""

from __future__ import annotations

import argparse
from pathlib import Path

from report_common import FORMATS, MODES, RECORDS, read_json, write_json


def initialize(project: Path, mode: str, title: str, formats: list[str], workflow: str = "full") -> None:
    project = project.resolve()
    if workflow not in {"compact", "full"}:
        raise ValueError("workflow must be compact or full")
    if mode not in MODES or not formats or set(formats) - FORMATS:
        raise ValueError("choose a supported mode and nonempty subset of md,pdf,docx")
    if (project / "report.tex").exists() and not (project / "project.json").exists():
        raise ValueError("legacy workspace: migrate to a separate project; see references/contracts.md")
    if (project / "project.json").exists():
        existing = read_json(project / "project.json")
        if not isinstance(existing, dict):
            raise ValueError("project.json must be an object")
        existing_workflow = existing.get("workflow", "full")
        if existing_workflow not in {"compact", "full"}:
            raise ValueError("existing workflow must be compact or full")
        if existing_workflow != workflow:
            raise ValueError("workflow differs from existing project; migrate explicitly to a separate project")
    project.mkdir(parents=True, exist_ok=True)
    config = {
        "schema_version": 1, "mode": mode, "title": title, "workflow": workflow,
        "author": "Research", "lang": "en-US", "depth": "standard",
        "structure": "flexible", "approval_policy": "adaptive", "gates": [],
        "formats": formats, "pdf_engine": "pdflatex", "reader_test_required": True,
    }
    architecture = {
        "schema_version": 3,
        "purpose": mode,
        "audience": "decision_owner",
        "root_id": "N0",
        "nodes": [{
            "id": "N0", "parent_id": None, "kind": "root", "title": title,
            "question": "What must the executive understand, decide, or do?", "answer": "",
            "reader_outcome": "The executive can explain the supported answer, decision, and limits.",
            "acceptance_criteria": "The synthesis is reconstructed by its children without unsupported novelty.",
            "rhetorical_role": "orient", "new_information": "", "handoff": "",
            "visual_role": "none",
            "claim_ids": [], "basis_claim_ids": [], "dependencies": [],
            "requires_concept_ids": [], "introduces_concept_ids": [], "budget_words": 800,
            "status": "planned", "draft_path": "report.md", "sequence": 0,
        }],
    }
    orchestration = {
        "schema_version": 1,
        "policy_date": "2026-09-22",
        "max_concurrent_subagents": 3,
        "prohibited_models": ["gpt-6-astra"],
        "roles": {
            "root": {"model": "gpt-6-sol", "reasoning_effort": "high"},
            "researcher": {"model": "gpt-6-sol", "reasoning_effort": "medium"},
            "leaf_writer": {"model": "gpt-6-sol", "reasoning_effort": "high"},
            "semantic_reviewer": {"model": "gpt-6-sol", "reasoning_effort": "high"},
            "cold_reader": {"model": "gpt-6-sol", "reasoning_effort": "medium"},
            "proofreader": {"model": "gpt-6-luna", "reasoning_effort": "medium"},
        },
        "compatibility_worker": {"model": "gpt-6-luna", "reasoning_effort": "medium"},
        "single_model_fallback": {"model": "gpt-6-sol", "reasoning_effort": "high"},
    }
    message = {
        "schema_version": 1, "status": "planned",
        "reader_start": "", "reader_end": "", "communicative_thesis": "",
        "central_tension": "", "proof_direction": "top_down",
    }
    objects = {"project.json": config, "planning/architecture.json": architecture,
               "planning/concepts.json": [],
               "planning/message.json": message,
               "control/orchestration.json": orchestration, "control/agent-runs.json": [],
               **{path: [] for path in RECORDS.values()}, "qa/issues.json": [], "qa/reviews.json": [],
               "control/state.json": {"stage": "intake", "status": "in_progress", "next_action": "Inspect inputs and complete the brief."}}
    texts = {
        "report.md": "<!-- Draft the executive brief after inspecting inputs and selecting the purpose. -->\n",
        "planning/brief.md": "# Brief\n\nRecord the reader purpose, executive audience, scope, deliverables, and constraints. Add a compact reader-stakes card: attention available, prior belief, trust basis, likely resistance or misreading, authority and feasible action, and what must be remembered. Complete planning/message.json with the executive transformation, selected communicative thesis, central tension, and proof direction before decomposing prose. Record materially different supportable candidate framings and the selection reason in control/decisions.md. Add a voice brief covering the reader-author relationship, formality, familiar business and domain vocabulary, representative author or house-style samples, and expressions or habits to avoid.\n",
        "planning/voice.md": "# Voice profile\n\nStatus: unset\n\nNo author or organizational voice has been selected. Add only an evidence-based profile with provenance, confidence, fingerprint, language choices, tone modulation, negative space, calibration transformations, and a compact runtime card; do not invent one.\n",
        "planning/research.md": "# Research design\n\nRecord decisive questions, required evidence, countertests, search scope, and stopping decisions.\n",
        "research/search-log.md": "# Search log\n\nRecord queries, dates, collections, selected sources, consequential exclusions, and remaining gaps.\n",
        "control/decisions.md": "# Decisions\n\nRecord material user directions and their scope. Do not invent approvals.\n",
    }
    if workflow == "compact":
        objects = {"project.json": config, **{path: [] for path in RECORDS.values()},
                   "qa/issues.json": [], "qa/reviews.json": []}
        texts = {
            "report.md": texts["report.md"],
            "planning/brief.md": "# Brief\n\n<!-- Describe the reader purpose, executive audience, scope, deliverables, and constraints. -->\n",
            "planning/plan.md": "# Plan\n\n<!-- State the reader outcome and thesis. List the ordered outline, consequential dependencies, and known limits. Use plain Markdown; no prescribed headings are required. -->\n",
        }
    for relative, value in objects.items():
        if not (project / relative).exists():
            write_json(project / relative, value)
    for relative, text in texts.items():
        path = project / relative
        if not path.exists():
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text, encoding="utf-8")
    for directory in (("analysis", "assets", "drafts", "sources", "output") if workflow == "full" else ("analysis", "assets", "sources", "output")):
        (project / directory).mkdir(exist_ok=True)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project_directory", type=Path)
    parser.add_argument("--mode", choices=sorted(MODES), default="investigate")
    parser.add_argument("--title", required=True)
    parser.add_argument("--workflow", choices=("compact", "full"), default="compact")
    parser.add_argument("--formats", default="md,pdf")
    args = parser.parse_args()
    initialize(args.project_directory, args.mode, args.title, list(dict.fromkeys(args.formats.split(","))), workflow=args.workflow)
    print(f"Project initialized; existing files preserved: {args.project_directory.resolve()}")


if __name__ == "__main__":
    main()
