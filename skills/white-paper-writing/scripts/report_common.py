"""Shared records, deterministic rendering, and content fingerprints (stdlib only)."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import subprocess


MODES = {"investigate", "decide", "explain", "argue"}
AUDIENCES = {"builders", "researchers", "assurance_reviewers"}
FORMATS = {"md", "pdf", "docx"}
RECORDS = {
    "claims": "evidence/claims.json",
    "sources": "evidence/sources.json",
    "links": "evidence/links.json",
    "calculations": "evidence/calculations.json",
    "numbers": "evidence/numbers.json",
    "figures": "figures/register.json",
}
TRACKED_DIRS = ("planning", "evidence", "research", "analysis", "drafts", "figures", "assets", "sources")
NUMBER_TOKEN = re.compile(r"\{\{number:([A-Za-z0-9_-]+)\}\}")


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def local_path(project: Path, relative: str) -> Path:
    if not isinstance(relative, str) or not relative or Path(relative).is_absolute():
        raise ValueError(f"expected a project-relative path: {relative!r}")
    path = (project / relative).resolve()
    if not path.is_relative_to(project.resolve()):
        raise ValueError(f"path escapes project: {relative}")
    return path


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def content_files(project: Path) -> dict[str, str]:
    paths = [project / name for name in ("project.json", "report.md", "control/decisions.md")]
    for directory in TRACKED_DIRS:
        paths.extend((project / directory).rglob("*"))
    result = {}
    for path in sorted(set(paths)):
        if path.is_file() and not any(part.startswith(".") or part == "__pycache__" for part in path.relative_to(project).parts):
            relative = str(path.relative_to(project))
            local_path(project, relative)
            result[relative] = sha256(path)
    return result


def content_digest(project: Path) -> str:
    encoded = json.dumps(content_files(project), sort_keys=True).encode()
    return hashlib.sha256(encoded).hexdigest()


def load_records(project: Path) -> dict:
    return {name: read_json(project / path) for name, path in RECORDS.items()}


def rendered_numbers(text: str, numbers: list[dict]) -> str:
    index = {row["id"]: row for row in numbers}
    def replace(match):
        key = match.group(1)
        if key not in index:
            raise ValueError(f"unknown number token: {key}")
        return str(index[key]["display_value"])
    return NUMBER_TOKEN.sub(replace, text)


def pandoc_ast(text: str, project: Path) -> dict:
    result = subprocess.run(
        ["pandoc", "--from=markdown", "--to=json"], input=text,
        text=True, encoding="utf-8", capture_output=True, check=True, cwd=project,
    )
    return json.loads(result.stdout)


def nodes(value):
    if isinstance(value, dict):
        yield value
        for item in value.values():
            yield from nodes(item)
    elif isinstance(value, list):
        for item in value:
            yield from nodes(item)


def citation_ids(ast: dict) -> list[str]:
    return list(dict.fromkeys(
        citation["citationId"]
        for node in nodes(ast) if node.get("t") == "Cite"
        for citation in node["c"][0]
    ))


def image_paths(ast: dict) -> list[str]:
    return [node["c"][-1][0] for node in nodes(ast) if node.get("t") == "Image"]


def inlines(text: str) -> list[dict]:
    result = []
    for index, word in enumerate(text.split()):
        if index:
            result.append({"t": "Space"})
        result.append({"t": "Str", "c": word})
    return result


def link(label: str, target: str) -> dict:
    return {"t": "Link", "c": [["", [], []], inlines(label), [target, ""]]}


def prepare_document(project: Path, config: dict, records: dict) -> tuple[dict, list[str]]:
    text = rendered_numbers((project / "report.md").read_text(encoding="utf-8"), records["numbers"])
    ast = pandoc_ast(text, project)
    cited = citation_ids(ast)
    sources = {source["id"]: source for source in records["sources"]}
    missing = set(cited) - sources.keys()
    if missing:
        raise ValueError(f"unregistered citations: {sorted(missing)}")
    numbering = {key: index for index, key in enumerate(cited, 1)}

    # Work on Pandoc's parsed citation nodes, never regex-rewrite raw prose/code.
    def transform(value):
        if isinstance(value, dict):
            if value.get("t") == "Cite":
                parts = []
                for index, citation in enumerate(value["c"][0]):
                    if index:
                        parts.extend(inlines("; "))
                        parts.append({"t": "Space"})
                    parts.extend(citation.get("citationPrefix", []))
                    if citation.get("citationPrefix"):
                        parts.append({"t": "Space"})
                    key = citation["citationId"]
                    parts.append(link(f"[{numbering[key]}]", f"#ref-{key}"))
                    suffix = citation.get("citationSuffix", [])
                    if suffix:
                        parts.append({"t": "Space"})
                        parts.extend(suffix)
                return {"t": "Span", "c": [["", [], []], parts]}
            return {key: transform(item) for key, item in value.items()}
        if isinstance(value, list):
            return [transform(item) for item in value]
        return value

    ast = transform(ast)
    for key in ("title", "subtitle", "author"):
        if config.get(key):
            ast["meta"][key] = {"t": "MetaString", "c": config[key]}
    figures = {row["path"]: row for row in records["figures"]}
    blocks = []
    for block in ast["blocks"]:
        blocks.append(block)
        for path in dict.fromkeys(image_paths(block)):
            if path in figures:
                blocks.append({"t": "Para", "c": [{"t": "Emph", "c": inlines(figures[path]["source_note"])}]})
    if cited:
        blocks.append({"t": "Header", "c": [1, ["references", [], []], inlines("References")]})
        references = []
        for key in cited:
            source = sources[key]
            content = inlines(f"[{numbering[key]}] {source['reference']}")
            url = source.get("url_or_path", "")
            if url.startswith(("https://", "http://")):
                content.extend([{"t": "Space"}, link(url, url)])
            if source.get("retrieved_date"):
                content.append({"t": "Space"})
                content.extend(inlines(f" Accessed {source['retrieved_date']}."))
            references.append({"t": "Div", "c": [[f"ref-{key}", [], []], [{"t": "Para", "c": content}]]})
        # Pandoc treats ref-* anchors as bibliography entries. Keep them in a
        # bibliography container so its LaTeX writer supplies the list environment.
        blocks.append({"t": "Div", "c": [["", ["csl-bib-body"], []], references]})
    ast["blocks"] = blocks
    return ast, cited


def required_reviews(config: dict) -> set[str]:
    result = {"evidence", "editorial"}
    if config.get("reader_test_required") is True:
        result.add("cold_reader")
    result.update(f"visual:{fmt}" for fmt in config["formats"] if fmt in {"pdf", "docx"})
    if len(config["formats"]) > 1:
        result.add("cross_format")
    return result
