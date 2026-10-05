#!/usr/bin/env python3
"""Emit a stable, read-only inventory of repository refactor evidence."""

from __future__ import annotations

import argparse
import ast
import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable


IGNORED_DIRECTORIES = {
    ".git",
    ".ipynb_checkpoints",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    ".tox",
    ".venv",
    "__pycache__",
    "build",
    "dist",
    "node_modules",
    "site-packages",
    "unsloth_compiled_cache",
    "venv",
}
CONFIG_SUFFIXES = {".ini", ".json", ".toml", ".yaml", ".yml"}
ENTRYPOINT_NAMES = {"__main__.py", "app.py", "cli.py", "main.py", "manage.py"}
TEST_PARTS = {"test", "tests"}


@dataclass(frozen=True, slots=True)
class ImportEdge:
    source: str
    target: str


@dataclass(frozen=True, slots=True)
class Inventory:
    root: str
    python_files: tuple[str, ...]
    entrypoints: tuple[str, ...]
    tests: tuple[str, ...]
    configuration: tuple[str, ...]
    documentation: tuple[str, ...]
    internal_imports: tuple[ImportEdge, ...]
    parse_failures: tuple[str, ...]


def visible_files(root: Path) -> Iterable[Path]:
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        relative = path.relative_to(root)
        if any(part in IGNORED_DIRECTORIES for part in relative.parts):
            continue
        yield path


def internal_roots(root: Path, python_files: Iterable[Path]) -> set[str]:
    roots: set[str] = set()
    for path in python_files:
        parts = path.relative_to(root).parts
        if parts[0] == "src" and len(parts) > 1:
            roots.add(Path(parts[1]).stem)
        else:
            roots.add(Path(parts[0]).stem)
    return roots


def imported_roots(tree: ast.AST) -> set[str]:
    imports: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.update(alias.name.partition(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
            imports.add(node.module.partition(".")[0])
    return imports


def has_main_guard(tree: ast.AST) -> bool:
    for node in ast.walk(tree):
        if not isinstance(node, ast.If):
            continue
        test = node.test
        if not isinstance(test, ast.Compare) or len(test.ops) != 1:
            continue
        if not isinstance(test.left, ast.Name) or test.left.id != "__name__":
            continue
        if not isinstance(test.ops[0], ast.Eq) or len(test.comparators) != 1:
            continue
        comparator = test.comparators[0]
        if isinstance(comparator, ast.Constant) and comparator.value == "__main__":
            return True
    return False


def inventory(root: Path) -> Inventory:
    files = tuple(visible_files(root))
    python_files = tuple(path for path in files if path.suffix == ".py")
    known_roots = internal_roots(root, python_files)
    import_edges: set[ImportEdge] = set()
    guarded_entrypoints: set[Path] = set()
    parse_failures: list[str] = []

    for path in python_files:
        relative = path.relative_to(root).as_posix()
        try:
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=relative)
        except (OSError, SyntaxError, UnicodeError) as error:
            parse_failures.append(f"{relative}: {type(error).__name__}: {error}")
            continue
        if has_main_guard(tree):
            guarded_entrypoints.add(path)
        import_edges.update(
            ImportEdge(relative, imported)
            for imported in imported_roots(tree)
            if imported in known_roots
        )

    relative = lambda path: path.relative_to(root).as_posix()
    entrypoints = {
        path
        for path in python_files
        if path.name in ENTRYPOINT_NAMES or "scripts" in path.relative_to(root).parts
    } | guarded_entrypoints

    return Inventory(
        root=str(root),
        python_files=tuple(relative(path) for path in python_files),
        entrypoints=tuple(sorted(relative(path) for path in entrypoints)),
        tests=tuple(
            relative(path)
            for path in python_files
            if TEST_PARTS.intersection(path.relative_to(root).parts)
            or path.name.startswith("test_")
            or path.name.endswith("_test.py")
        ),
        configuration=tuple(
            relative(path)
            for path in files
            if path.suffix.lower() in CONFIG_SUFFIXES
            or path.name in {"Dockerfile", "Makefile"}
        ),
        documentation=tuple(
            relative(path) for path in files if path.suffix.lower() in {".md", ".rst"}
        ),
        internal_imports=tuple(sorted(import_edges, key=lambda edge: (edge.source, edge.target))),
        parse_failures=tuple(sorted(parse_failures)),
    )


def markdown(report: Inventory) -> str:
    sections: list[str] = [f"# Repository Inventory: `{report.root}`"]

    def add_paths(title: str, paths: tuple[str, ...]) -> None:
        lines = [f"## {title} ({len(paths)})", *(f"- `{path}`" for path in paths)]
        sections.append("\n".join(lines))

    add_paths("Entrypoint Candidates", report.entrypoints)
    add_paths("Configuration", report.configuration)
    add_paths("Documentation", report.documentation)
    add_paths("Tests", report.tests)
    sections.append(
        "\n".join(
            [
                f"## Internal Import Edges ({len(report.internal_imports)})",
                *(f"- `{edge.source}` -> `{edge.target}`" for edge in report.internal_imports),
            ]
        )
    )
    add_paths("Parse Failures", report.parse_failures)
    sections.append(f"Python files scanned: {len(report.python_files)}")
    return "\n\n".join(sections) + "\n"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", type=Path, help="repository root to inventory")
    parser.add_argument("--format", choices=("json", "markdown"), default="json")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = args.root.resolve()
    if not root.is_dir():
        raise SystemExit(f"not a directory: {root}")
    report = inventory(root)
    if args.format == "markdown":
        print(markdown(report), end="")
    else:
        print(json.dumps(asdict(report), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
