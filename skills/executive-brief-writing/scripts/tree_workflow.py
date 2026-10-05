#!/usr/bin/env python3
"""Validate, disclose, schedule, and invalidate the writing architecture graph."""

from __future__ import annotations

import argparse
from collections import defaultdict, deque
import json
from pathlib import Path
import re

from report_common import AUDIENCES, MODES, read_json, write_json


KINDS = {"root", "section", "leaf", "exhibit", "connective"}
STATUSES = {"planned", "supported", "drafted", "validated"}
STATUS_RANK = {name: rank for rank, name in enumerate(("planned", "supported", "drafted", "validated"))}
ROLES = {"root", "researcher", "leaf_writer", "semantic_reviewer", "proofreader"}
DELEGATED_ROLES = (ROLES - {"root"}) | {"cold_reader"}
REASONING_EFFORTS = {"low", "medium", "high", "xhigh", "max"}
NODE_ID = re.compile(r"[A-Za-z][A-Za-z0-9_-]*")
ARCHITECTURE_VERSIONS = {1, 2, 3}
PROOF_DIRECTIONS = {"top_down", "bottom_up", "re_earning"}
RHETORICAL_ROLES = {"orient", "define", "demonstrate", "complicate", "compare", "resolve", "transition", "conclude"}
VISUAL_ROLES = {"none", "map", "mechanism", "comparison", "evidence", "decision"}


def architecture_path(project: Path) -> Path:
    return project.resolve() / "planning/architecture.json"


def load_architecture(project: Path) -> dict:
    value = read_json(architecture_path(project))
    if not isinstance(value, dict):
        raise ValueError("planning/architecture.json must be an object")
    return value


def concepts_path(project: Path) -> Path:
    return project.resolve() / "planning/concepts.json"


def load_concepts(project: Path, *, required: bool = False) -> list[dict]:
    path = concepts_path(project)
    if not path.exists() and not required:
        return []
    value = read_json(path)
    if not isinstance(value, list) or any(not isinstance(row, dict) for row in value):
        raise ValueError("planning/concepts.json must be a list of objects")
    return value


def message_path(project: Path) -> Path:
    return project.resolve() / "planning/message.json"


def load_message(project: Path, *, required: bool = False) -> dict:
    path = message_path(project)
    if not path.exists() and not required:
        return {}
    value = read_json(path)
    if not isinstance(value, dict):
        raise ValueError("planning/message.json must be an object")
    return value


def validate_message(project: Path, *, release: bool = False) -> tuple[list[str], list[str], dict]:
    errors: list[str] = []
    warnings: list[str] = []
    message = load_message(project, required=True)
    if message.get("schema_version") != 1:
        errors.append("message: unsupported schema_version")
    if message.get("status") not in {"planned", "defined"}:
        errors.append("message: status must be planned or defined")
    if message.get("proof_direction") not in PROOF_DIRECTIONS:
        errors.append("message: invalid proof_direction")
    fields = ("reader_start", "reader_end", "communicative_thesis", "central_tension")
    if message.get("status") == "defined":
        for field in fields:
            if not isinstance(message.get(field), str) or not message[field].strip():
                errors.append(f"message: missing {field}")
    else:
        (errors if release else warnings).append("message: communication contract remains planned")
    return errors, warnings, message


def _cycles(edges: dict[str, list[str]], node_ids: set[str]) -> list[list[str]]:
    cycles: list[list[str]] = []
    visiting: list[str] = []
    active: set[str] = set()
    complete: set[str] = set()

    def visit(node_id: str) -> None:
        if node_id in active:
            start = visiting.index(node_id)
            cycles.append(visiting[start:] + [node_id])
            return
        if node_id in complete:
            return
        active.add(node_id)
        visiting.append(node_id)
        for target in edges.get(node_id, []):
            if target in node_ids:
                visit(target)
        visiting.pop()
        active.remove(node_id)
        complete.add(node_id)

    for node_id in sorted(node_ids):
        visit(node_id)
    return cycles


def validate_architecture(
    project: Path,
    *,
    release: bool = False,
    claim_ids: set[str] | None = None,
    claim_records: dict[str, dict] | None = None,
    purpose: str | None = None,
) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    try:
        tree = load_architecture(project)
        schema_version = tree.get("schema_version")
        if schema_version not in ARCHITECTURE_VERSIONS:
            errors.append("architecture: unsupported schema_version")
        message: dict = {}
        if schema_version == 3:
            message_errors, message_warnings, message = validate_message(project, release=release)
            errors.extend(message_errors)
            warnings.extend(message_warnings)
        if tree.get("purpose") not in MODES:
            errors.append("architecture: invalid purpose")
        elif purpose is not None and tree.get("purpose") != purpose:
            errors.append("architecture: purpose differs from project mode")
        if tree.get("audience") not in AUDIENCES:
            errors.append("architecture: invalid audience")
        root_id = tree.get("root_id")
        nodes = tree.get("nodes")
        if not isinstance(nodes, list) or not nodes:
            return [*errors, "architecture: nodes must be a nonempty list"], warnings
        if any(not isinstance(node, dict) for node in nodes):
            return [*errors, "architecture: every node must be an object"], warnings

        ids = [node.get("id") for node in nodes]
        if any(not isinstance(node_id, str) or not NODE_ID.fullmatch(node_id) for node_id in ids):
            errors.append("architecture: invalid or missing node ID")
        if len(set(ids)) != len(ids):
            errors.append("architecture: duplicate node IDs")
        index = {node["id"]: node for node in nodes if isinstance(node.get("id"), str)}
        node_ids = set(index)
        if root_id not in index:
            errors.append("architecture: root_id does not identify a node")

        children: dict[str, list[str]] = defaultdict(list)
        dependencies: dict[str, list[str]] = {}
        parent_edges: dict[str, list[str]] = {}
        sequences: list[int] = []
        for node_id, node in index.items():
            label = f"architecture node {node_id}"
            for field in ("title", "question"):
                if not isinstance(node.get(field), str) or not node[field].strip():
                    errors.append(f"{label}: missing {field}")
            if node.get("kind") not in KINDS:
                errors.append(f"{label}: invalid kind")
            if node.get("status") not in STATUSES:
                errors.append(f"{label}: invalid status")
            budget = node.get("budget_words")
            if isinstance(budget, bool) or not isinstance(budget, int) or budget < 0:
                errors.append(f"{label}: budget_words must be a nonnegative integer")
            sequence = node.get("sequence")
            if isinstance(sequence, bool) or not isinstance(sequence, int) or sequence < 0:
                errors.append(f"{label}: sequence must be a nonnegative integer")
            else:
                sequences.append(sequence)
            answer = node.get("answer")
            if not isinstance(answer, str):
                errors.append(f"{label}: answer must be text")
            elif node.get("status") != "planned" and not answer.strip():
                errors.append(f"{label}: supported or drafted node needs an answer")

            if schema_version in {2, 3}:
                for field in ("reader_outcome", "acceptance_criteria"):
                    if not isinstance(node.get(field), str) or not node[field].strip():
                        errors.append(f"{label}: missing {field}")
            if schema_version == 3:
                if node.get("rhetorical_role") not in RHETORICAL_ROLES:
                    errors.append(f"{label}: invalid rhetorical_role")
                if node.get("visual_role") not in VISUAL_ROLES:
                    errors.append(f"{label}: invalid visual_role")
                for field in ("new_information", "handoff"):
                    if not isinstance(node.get(field), str):
                        errors.append(f"{label}: {field} must be text")
                if node.get("status") != "planned" and not node.get("new_information", "").strip():
                    errors.append(f"{label}: supported or drafted node needs new_information")

            parent_id = node.get("parent_id")
            if node_id == root_id:
                if parent_id is not None or node.get("kind") != "root":
                    errors.append(f"{label}: root must have kind root and no parent")
            elif parent_id not in index:
                errors.append(f"{label}: unknown parent {parent_id!r}")
            else:
                children[parent_id].append(node_id)
                parent_edges[node_id] = [parent_id]
                if schema_version in {1, 2}:
                    parent_sequence = index[parent_id].get("sequence")
                    if isinstance(sequence, int) and isinstance(parent_sequence, int) and sequence <= parent_sequence:
                        errors.append(f"{label}: sequence must follow its parent")

            node_dependencies = node.get("dependencies")
            if not isinstance(node_dependencies, list) or any(not isinstance(value, str) for value in node_dependencies):
                errors.append(f"{label}: dependencies must be a list of node IDs")
                node_dependencies = []
            elif len(set(node_dependencies)) != len(node_dependencies):
                errors.append(f"{label}: duplicate dependencies")
            for dependency in node_dependencies:
                if dependency not in index:
                    errors.append(f"{label}: unknown dependency {dependency}")
                if dependency == node_id:
                    errors.append(f"{label}: node cannot depend on itself")
            dependencies[node_id] = node_dependencies

            claims = node.get("claim_ids")
            if not isinstance(claims, list) or any(not isinstance(value, str) for value in claims):
                errors.append(f"{label}: claim_ids must be a list")
                claims = []
            elif len(set(claims)) != len(claims):
                errors.append(f"{label}: duplicate claim IDs")
            if claim_ids is not None:
                for claim_id in claims:
                    if claim_id not in claim_ids:
                        errors.append(f"{label}: unknown claim {claim_id}")

            if schema_version in {2, 3}:
                for field in ("basis_claim_ids", "requires_concept_ids", "introduces_concept_ids"):
                    values = node.get(field)
                    if not isinstance(values, list) or any(not isinstance(value, str) for value in values):
                        errors.append(f"{label}: {field} must be a list of IDs")
                    elif len(set(values)) != len(values):
                        errors.append(f"{label}: duplicate IDs in {field}")
                if claim_ids is not None:
                    for claim_id in node.get("basis_claim_ids", []):
                        if claim_id not in claim_ids:
                            errors.append(f"{label}: unknown basis claim {claim_id}")

            draft_path = node.get("draft_path")
            if not isinstance(draft_path, str) or not draft_path.strip():
                errors.append(f"{label}: missing draft_path")
            elif Path(draft_path).is_absolute() or ".." in Path(draft_path).parts:
                errors.append(f"{label}: draft_path must remain inside the project")
            elif node.get("status") in {"drafted", "validated"} and not (project.resolve() / draft_path).is_file():
                errors.append(f"{label}: missing draft file {draft_path}")

        if len(sequences) != len(set(sequences)):
            errors.append("architecture: node sequences must be unique")

        for cycle in _cycles(parent_edges, node_ids):
            errors.append(f"architecture: parent cycle {' -> '.join(cycle)}")
        for cycle in _cycles(dependencies, node_ids):
            errors.append(f"architecture: dependency cycle {' -> '.join(cycle)}")
        compile_edges = {
            node_id: [*children.get(node_id, []), *dependencies.get(node_id, [])]
            for node_id in node_ids
        }
        for cycle in _cycles(compile_edges, node_ids):
            errors.append(f"architecture: compile cycle {' -> '.join(cycle)}")

        if root_id in index:
            reachable: set[str] = set()
            pending = [root_id]
            while pending:
                node_id = pending.pop()
                if node_id in reachable:
                    continue
                reachable.add(node_id)
                pending.extend(children.get(node_id, []))
            for node_id in sorted(node_ids - reachable):
                errors.append(f"architecture node {node_id}: unreachable from root")

        descendants: dict[str, set[str]] = {}

        def collect_descendants(node_id: str) -> set[str]:
            if node_id not in descendants:
                values: set[str] = set()
                for child_id in children.get(node_id, []):
                    values.add(child_id)
                    values.update(collect_descendants(child_id))
                descendants[node_id] = values
            return descendants[node_id]

        concept_index: dict[str, dict] = {}
        if schema_version in {2, 3}:
            concepts = load_concepts(project, required=True)
            concept_ids = [row.get("id") for row in concepts]
            if any(not isinstance(value, str) or not NODE_ID.fullmatch(value) for value in concept_ids):
                errors.append("concepts: invalid or missing ID")
            if len(set(concept_ids)) != len(concept_ids):
                errors.append("concepts: duplicate IDs")
            concept_index = {row["id"]: row for row in concepts if isinstance(row.get("id"), str)}
            prerequisite_edges: dict[str, list[str]] = {}
            introduced_by: dict[str, str] = {}
            for concept_id, concept in concept_index.items():
                label = f"concept {concept_id}"
                for field in ("canonical_name", "definition"):
                    if not isinstance(concept.get(field), str) or not concept[field].strip():
                        errors.append(f"{label}: missing {field}")
                aliases = concept.get("aliases")
                if not isinstance(aliases, list) or any(not isinstance(value, str) or not value.strip() for value in aliases):
                    errors.append(f"{label}: aliases must be a list of nonempty strings")
                elif len(set(aliases)) != len(aliases):
                    errors.append(f"{label}: duplicate aliases")
                if not isinstance(concept.get("assumed_known"), bool):
                    errors.append(f"{label}: assumed_known must be boolean")
                prerequisites = concept.get("prerequisite_ids")
                if not isinstance(prerequisites, list) or any(not isinstance(value, str) for value in prerequisites):
                    errors.append(f"{label}: prerequisite_ids must be a list of IDs")
                    prerequisites = []
                elif len(set(prerequisites)) != len(prerequisites):
                    errors.append(f"{label}: duplicate prerequisite IDs")
                for prerequisite in prerequisites:
                    if prerequisite not in concept_index:
                        errors.append(f"{label}: unknown prerequisite {prerequisite}")
                    if prerequisite == concept_id:
                        errors.append(f"{label}: cannot require itself")
                prerequisite_edges[concept_id] = prerequisites
                introduced_at = concept.get("introduced_at")
                if introduced_at is not None and introduced_at not in index:
                    errors.append(f"{label}: unknown introduction node {introduced_at!r}")
                if not concept.get("assumed_known") and introduced_at not in index:
                    errors.append(f"{label}: unfamiliar concept needs introduced_at")
                if introduced_at in index:
                    introduced_by[concept_id] = introduced_at
            for cycle in _cycles(prerequisite_edges, set(concept_index)):
                errors.append(f"concepts: prerequisite cycle {' -> '.join(cycle)}")

            for node_id, node in index.items():
                label = f"architecture node {node_id}"
                required = node.get("requires_concept_ids", [])
                introduced = node.get("introduces_concept_ids", [])
                for concept_id in [*required, *introduced]:
                    if concept_id not in concept_index:
                        errors.append(f"{label}: unknown concept {concept_id}")
                for concept_id in introduced:
                    if introduced_by.get(concept_id) != node_id:
                        errors.append(f"{label}: introduction disagrees with concept {concept_id}")
                for concept_id, introduction_node in introduced_by.items():
                    if introduction_node == node_id and concept_id not in introduced:
                        errors.append(f"{label}: missing declared introduction of {concept_id}")
                node_sequence = node.get("sequence")
                for concept_id in required:
                    concept = concept_index.get(concept_id, {})
                    introduction_node = introduced_by.get(concept_id)
                    if concept.get("assumed_known") or introduction_node is None:
                        continue
                    introduction_sequence = index[introduction_node].get("sequence")
                    if isinstance(node_sequence, int) and isinstance(introduction_sequence, int) and introduction_sequence > node_sequence:
                        errors.append(f"{label}: requires {concept_id} before its introduction")
                for concept_id in introduced:
                    for prerequisite in concept_index.get(concept_id, {}).get("prerequisite_ids", []):
                        prerequisite_record = concept_index.get(prerequisite, {})
                        prerequisite_node = introduced_by.get(prerequisite)
                        if prerequisite_record.get("assumed_known") or prerequisite_node is None:
                            continue
                        prerequisite_sequence = index[prerequisite_node].get("sequence")
                        if isinstance(node_sequence, int) and isinstance(prerequisite_sequence, int) and prerequisite_sequence > node_sequence:
                            errors.append(f"{label}: introduces {concept_id} before prerequisite {prerequisite}")

        for node_id, node in index.items():
            status = node.get("status")
            node_children = children.get(node_id, [])
            if status in STATUS_RANK:
                for child_id in node_children:
                    child_status = index[child_id].get("status")
                    if child_status in STATUS_RANK and STATUS_RANK[child_status] < STATUS_RANK[status]:
                        errors.append(f"architecture node {node_id}: status exceeds child {child_id}")
            is_leaf = not node_children
            if release:
                if status != "validated":
                    errors.append(f"architecture node {node_id}: release requires validated status")
                if is_leaf and node.get("kind") != "connective" and not node.get("claim_ids"):
                    errors.append(f"architecture node {node_id}: evidentiary leaf has no claim IDs")
                if schema_version in {2, 3} and not is_leaf and node.get("kind") != "connective":
                    basis = node.get("basis_claim_ids", [])
                    if not basis:
                        errors.append(f"architecture node {node_id}: synthesis has no descendant claim basis")
                    descendant_claims = {
                        claim_id
                        for descendant_id in collect_descendants(node_id)
                        for claim_id in index[descendant_id].get("claim_ids", [])
                    }
                    for claim_id in basis:
                        if claim_id not in descendant_claims:
                            errors.append(f"architecture node {node_id}: basis claim {claim_id} is not in a descendant")
                    if claim_records is not None:
                        declared_derivation: set[str] = set()
                        for claim_id in node.get("claim_ids", []):
                            derived = set(claim_records.get(claim_id, {}).get("derived_from", []))
                            declared_derivation.update(derived)
                            if claim_id not in descendant_claims and not (derived & set(basis)):
                                errors.append(f"architecture node {node_id}: synthesis claim {claim_id} does not derive from its basis")
                        if node.get("claim_ids") and not set(basis).issubset(declared_derivation | descendant_claims):
                            errors.append(f"architecture node {node_id}: synthesis claims do not cover the declared basis")
            elif status != "validated":
                warnings.append(f"architecture node {node_id}: {status}")
    except (OSError, ValueError, KeyError, TypeError) as exc:
        errors.append(f"cannot validate architecture: {exc}")
    return errors, warnings


def validate_orchestration(project: Path) -> list[str]:
    errors: list[str] = []
    try:
        policy = read_json(project.resolve() / "control/orchestration.json")
        if not isinstance(policy, dict) or policy.get("schema_version") != 1:
            return ["orchestration: unsupported or missing schema_version"]
        concurrency = policy.get("max_concurrent_subagents")
        if isinstance(concurrency, bool) or not isinstance(concurrency, int) or not 1 <= concurrency <= 3:
            errors.append("orchestration: max_concurrent_subagents must be from 1 to 3")
        prohibited = policy.get("prohibited_models")
        if not isinstance(prohibited, list) or "gpt-6-astra" not in prohibited:
            errors.append("orchestration: gpt-6-astra must remain explicitly prohibited")
        roles = policy.get("roles")
        if not isinstance(roles, dict) or not ROLES.issubset(roles):
            errors.append("orchestration: required model roles are missing")
            roles = {}
        profiles = {name: roles.get(name) for name in ROLES | ({"cold_reader"} if "cold_reader" in roles else set())}
        profiles["compatibility_worker"] = policy.get("compatibility_worker")
        profiles["single_model_fallback"] = policy.get("single_model_fallback")
        for name, profile in profiles.items():
            if not isinstance(profile, dict):
                errors.append(f"orchestration {name}: model profile must be an object")
                continue
            if not isinstance(profile.get("model"), str) or not profile["model"].strip():
                errors.append(f"orchestration {name}: missing model")
            elif "astra" in profile["model"].lower():
                errors.append(f"orchestration {name}: Astra models are prohibited")
            if profile.get("reasoning_effort") not in REASONING_EFFORTS:
                errors.append(f"orchestration {name}: invalid reasoning_effort")

        runs = read_json(project.resolve() / "control/agent-runs.json")
        if not isinstance(runs, list) or any(not isinstance(row, dict) for row in runs):
            errors.append("orchestration: control/agent-runs.json must be a list of objects")
        else:
            for index, row in enumerate(runs):
                label = f"agent run {index + 1}"
                for field in ("role", "model", "reasoning_effort", "status"):
                    if not isinstance(row.get(field), str) or not row[field].strip():
                        errors.append(f"{label}: missing {field}")
                if isinstance(row.get("model"), str) and "astra" in row["model"].lower():
                    errors.append(f"{label}: Astra models are prohibited")
                if row.get("role") not in DELEGATED_ROLES:
                    errors.append(f"{label}: invalid delegated role")
                if row.get("reasoning_effort") not in REASONING_EFFORTS:
                    errors.append(f"{label}: invalid reasoning_effort")
                if row.get("status") not in {"completed", "limited", "failed"}:
                    errors.append(f"{label}: invalid status")
                for field in ("node_ids", "artifacts"):
                    value = row.get(field)
                    if not isinstance(value, list) or any(not isinstance(item, str) for item in value):
                        errors.append(f"{label}: {field} must be a list of strings")
    except (OSError, ValueError, KeyError, TypeError) as exc:
        errors.append(f"cannot validate orchestration: {exc}")
    return errors


def ready_nodes(tree: dict, phase: str) -> list[dict]:
    index = {node["id"]: node for node in tree["nodes"]}
    children: dict[str, list[str]] = defaultdict(list)
    for node in tree["nodes"]:
        if node["parent_id"] is not None:
            children[node["parent_id"]].append(node["id"])

    def at_least(node_id: str, status: str) -> bool:
        return STATUS_RANK[index[node_id]["status"]] >= STATUS_RANK[status]

    ready: list[dict] = []
    for node in tree["nodes"]:
        node_id = node["id"]
        dependencies = node["dependencies"]
        node_children = children.get(node_id, [])
        if phase == "research":
            selected = (
                node["status"] == "planned"
                and not node_children
                and all(at_least(value, "supported") for value in dependencies)
            )
        elif phase == "draft":
            selected = (
                node["status"] == "supported"
                and all(at_least(value, "drafted") for value in dependencies)
                and all(at_least(value, "drafted") for value in node_children)
            )
        else:
            selected = (
                node["status"] == "drafted"
                and all(at_least(value, "validated") for value in dependencies)
                and all(at_least(value, "validated") for value in node_children)
            )
        if selected:
            ready.append(node)
    return ready


def disclosure_rows(
    tree: dict,
    start_id: str | None = None,
    concepts: list[dict] | None = None,
    message: dict | None = None,
) -> list[dict]:
    index = {node["id"]: node for node in tree["nodes"]}
    root_id = tree.get("root_id")
    if root_id not in index:
        raise ValueError(f"unknown disclosure root: {root_id!r}")
    if start_id is not None and start_id not in index:
        raise ValueError(f"unknown disclosure root: {start_id!r}")
    children: dict[str, list[str]] = defaultdict(list)
    for node in tree["nodes"]:
        if node["parent_id"] is not None:
            children[node["parent_id"]].append(node["id"])
    for node_ids in children.values():
        node_ids.sort(key=lambda node_id: index[node_id]["sequence"])

    def ancestor_path(node_id: str) -> list[dict]:
        ancestors: list[dict] = []
        seen = {node_id}
        parent_id = index[node_id].get("parent_id")
        while parent_id is not None:
            if parent_id in seen or parent_id not in index:
                raise ValueError(f"invalid ancestor path for {node_id}")
            seen.add(parent_id)
            parent = index[parent_id]
            ancestors.append({"id": parent_id, "title": parent["title"], "synthesis": parent["answer"]})
            parent_id = parent.get("parent_id")
        return list(reversed(ancestors))

    preorder: list[str] = []

    def visit(node_id: str) -> None:
        preorder.append(node_id)
        for child_id in children.get(node_id, []):
            visit(child_id)

    visit(root_id)
    if tree.get("schema_version") == 3:
        narrative_order = [node["id"] for node in sorted(tree["nodes"], key=lambda row: row["sequence"])]
    else:
        narrative_order = preorder

    selected_ids = set(narrative_order)
    if start_id is not None:
        selected_ids = set()
        pending = [start_id]
        while pending:
            node_id = pending.pop()
            if node_id in selected_ids:
                continue
            selected_ids.add(node_id)
            pending.extend(children.get(node_id, []))

    concept_index = {row["id"]: row for row in (concepts or [])}
    assumed_known = {concept_id for concept_id, row in concept_index.items() if row.get("assumed_known")}
    global_position = {node_id: position for position, node_id in enumerate(narrative_order)}

    def beat_summary(node_id: str | None) -> dict | None:
        if node_id is None:
            return None
        node = index[node_id]
        return {
            "id": node_id,
            "title": node["title"],
            "rhetorical_role": node.get("rhetorical_role", ""),
            "new_information": node.get("new_information", ""),
            "handoff": node.get("handoff", ""),
        }

    rows: list[dict] = []
    for node_id in narrative_order:
        if node_id not in selected_ids:
            continue
        node = index[node_id]
        position = global_position[node_id]
        previous_id = narrative_order[position - 1] if position else None
        next_id = narrative_order[position + 1] if position + 1 < len(narrative_order) else None
        established_concepts = set(assumed_known)
        established_claims: set[str] = set()
        last_concept: dict[str, tuple[str, int]] = {}
        last_claim: dict[str, tuple[str, int]] = {}
        for prior_position, prior_id in enumerate(narrative_order[:position]):
            prior = index[prior_id]
            for concept_id in prior.get("introduces_concept_ids", []):
                established_concepts.add(concept_id)
                last_concept[concept_id] = (prior_id, position - prior_position)
            for concept_id in prior.get("requires_concept_ids", []):
                last_concept[concept_id] = (prior_id, position - prior_position)
            for claim_id in prior.get("claim_ids", []):
                established_claims.add(claim_id)
                last_claim[claim_id] = (prior_id, position - prior_position)
        relevant_concepts = set(node.get("requires_concept_ids", [])) | set(node.get("introduces_concept_ids", []))
        relevant_claims = set(node.get("claim_ids", [])) | set(node.get("basis_claim_ids", []))
        rows.append({
            "depth": len(ancestor_path(node_id)),
            "id": node_id,
            "kind": node["kind"],
            "title": node["title"],
            "question": node["question"],
            "synthesis": node["answer"],
            "ancestor_path": ancestor_path(node_id),
            "draft_path": node["draft_path"],
            "reader_outcome": node.get("reader_outcome", ""),
            "acceptance_criteria": node.get("acceptance_criteria", ""),
            "rhetorical_role": node.get("rhetorical_role", ""),
            "new_information": node.get("new_information", ""),
            "handoff": node.get("handoff", ""),
            "visual_role": node.get("visual_role", "none"),
            "claim_ids": node.get("claim_ids", []),
            "basis_claim_ids": node.get("basis_claim_ids", []),
            "required_concepts": [concept_index[value] for value in node.get("requires_concept_ids", []) if value in concept_index],
            "introduced_concepts": [concept_index[value] for value in node.get("introduces_concept_ids", []) if value in concept_index],
            "document_message": message or {},
            "previous_beat": beat_summary(previous_id),
            "next_beat": beat_summary(next_id),
            "established_concept_ids": sorted(established_concepts),
            "established_claim_ids": sorted(established_claims),
            "last_mentions": {
                "concepts": {value: {"node_id": last_concept[value][0], "beats_back": last_concept[value][1]} for value in sorted(relevant_concepts & set(last_concept))},
                "claims": {value: {"node_id": last_claim[value][0], "beats_back": last_claim[value][1]} for value in sorted(relevant_claims & set(last_claim))},
            },
        })
    return rows


def invalidate(
    tree: dict,
    changed: set[str],
    *,
    changed_concepts: set[str] | None = None,
    changed_claims: set[str] | None = None,
) -> set[str]:
    index = {node["id"]: node for node in tree["nodes"]}
    unknown = changed - set(index)
    if unknown:
        raise ValueError(f"unknown node IDs: {', '.join(sorted(unknown))}")
    reverse_dependencies: dict[str, set[str]] = defaultdict(set)
    for node in tree["nodes"]:
        for dependency in node["dependencies"]:
            reverse_dependencies[dependency].add(node["id"])

    seeds = set(changed)
    for node in tree["nodes"]:
        concept_ids = set(node.get("requires_concept_ids", [])) | set(node.get("introduces_concept_ids", []))
        claim_ids = set(node.get("claim_ids", [])) | set(node.get("basis_claim_ids", []))
        if concept_ids & (changed_concepts or set()) or claim_ids & (changed_claims or set()):
            seeds.add(node["id"])
    affected = set(seeds)
    pending = deque(seeds)
    while pending:
        node_id = pending.popleft()
        parent_id = index[node_id]["parent_id"]
        candidates = set(reverse_dependencies.get(node_id, set()))
        if parent_id is not None:
            candidates.add(parent_id)
        for candidate in candidates - affected:
            affected.add(candidate)
            pending.append(candidate)
    for node_id in affected:
        index[node_id]["status"] = "planned"
    return affected


def dependent_record_ids(records: list[dict], changed: set[str], fields: tuple[str, ...]) -> set[str]:
    """Expand changed record IDs through reverse semantic dependencies."""
    index = {row.get("id"): row for row in records if isinstance(row.get("id"), str)}
    unknown = changed - set(index)
    if unknown:
        raise ValueError(f"unknown record IDs: {', '.join(sorted(unknown))}")
    consumers: dict[str, set[str]] = defaultdict(set)
    for record_id, record in index.items():
        for field in fields:
            for dependency in record.get(field, []):
                if dependency in index:
                    consumers[dependency].add(record_id)
    affected = set(changed)
    pending = deque(changed)
    while pending:
        record_id = pending.popleft()
        for consumer in consumers.get(record_id, set()) - affected:
            affected.add(consumer)
            pending.append(consumer)
    return affected


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    validate_parser = subparsers.add_parser("validate")
    validate_parser.add_argument("project", type=Path)
    validate_parser.add_argument("--release", action="store_true")
    ready_parser = subparsers.add_parser("ready")
    ready_parser.add_argument("project", type=Path)
    ready_parser.add_argument("--phase", choices=("research", "draft", "review"), required=True)
    invalidate_parser = subparsers.add_parser("invalidate")
    invalidate_parser.add_argument("project", type=Path)
    invalidate_parser.add_argument("node_ids", nargs="*")
    invalidate_parser.add_argument("--concept-id", action="append", default=[])
    invalidate_parser.add_argument("--claim-id", action="append", default=[])
    disclose_parser = subparsers.add_parser("disclose")
    disclose_parser.add_argument("project", type=Path)
    disclose_parser.add_argument("--node")
    args = parser.parse_args()

    if args.command == "validate":
        errors, warnings = validate_architecture(args.project, release=args.release)
        errors.extend(validate_orchestration(args.project))
        for warning in warnings:
            print(f"WARNING: {warning}")
        for error in errors:
            print(f"ERROR: {error}")
        return int(bool(errors))
    tree = load_architecture(args.project)
    if args.command == "disclose":
        for row in disclosure_rows(
            tree, args.node, load_concepts(args.project), load_message(args.project)
        ):
            print(json.dumps(row, ensure_ascii=False))
        return 0
    if args.command == "ready":
        for node in ready_nodes(tree, args.phase):
            print(f"{node['id']}\t{node['kind']}\t{node['title']}\t{node['draft_path']}")
        return 0
    if not args.node_ids and not args.concept_id and not args.claim_id:
        parser.error("invalidate requires a node ID, --concept-id, or --claim-id")
    changed_concepts = dependent_record_ids(
        load_concepts(args.project, required=bool(args.concept_id)), set(args.concept_id), ("prerequisite_ids",)
    )
    claims = read_json(args.project.resolve() / "evidence/claims.json")
    if not isinstance(claims, list) or any(not isinstance(row, dict) for row in claims):
        raise ValueError("evidence/claims.json must be a list of objects")
    changed_claims = dependent_record_ids(
        claims, set(args.claim_id), ("derived_from", "qualified_by", "contradicted_by")
    )
    affected = invalidate(
        tree,
        set(args.node_ids),
        changed_concepts=changed_concepts,
        changed_claims=changed_claims,
    )
    write_json(architecture_path(args.project), tree)
    print("Invalidated: " + ", ".join(sorted(affected)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
