#!/usr/bin/env python3
"""Build requested report formats from one parsed document; publish only a complete build."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import shutil
import subprocess
import tempfile

from report_common import content_digest, content_files, load_records, local_path, prepare_document, read_json, sha256, write_json
from validate_report_project import validate


def build(project: Path) -> dict:
    project = project.resolve()
    errors, warnings = validate(project)
    if errors:
        raise ValueError("preflight failed:\n" + "\n".join(errors))
    for warning in warnings:
        print(f"DRAFT LIMITATION: {warning}")
    config = read_json(project / "project.json")
    fingerprint = content_digest(project)
    records = load_records(project)
    ast, cited = prepare_document(project, config, records)
    if not ast["blocks"] or all(block.get("t") == "RawBlock" for block in ast["blocks"]):
        raise ValueError("cannot build an empty manuscript")
    output = project / "output"
    output.mkdir(exist_ok=True)
    version = subprocess.run(["pandoc", "--version"], text=True, encoding="utf-8", capture_output=True, check=True).stdout.splitlines()[0]
    with tempfile.TemporaryDirectory(prefix="report_build_") as temporary:
        stage = Path(temporary)
        document = stage / "document.json"
        write_json(document, ast)
        logs = []
        for fmt in config["formats"]:
            destination = stage / f"report.{fmt}"
            command = ["pandoc", str(document), "--from=json", "--standalone", f"--output={destination}"]
            # TeX defaults to English. Avoid requiring optional babel language
            # packs merely for an English locale; preserve locale in other formats.
            if config.get("lang") and (fmt != "pdf" or not config["lang"].startswith("en")):
                command.append(f"--metadata=lang:{config['lang']}")
            if fmt == "md":
                command.extend(["--to=gfm", "--wrap=none"])
            elif fmt == "pdf":
                engine = config.get("pdf_engine", "pdflatex")
                if engine not in {"pdflatex", "xelatex", "lualatex"}:
                    raise ValueError("unsupported pdf_engine")
                command.extend([f"--pdf-engine={engine}", "--variable=geometry:margin=0.8in", "--variable=fontsize:11pt"])
                if config.get("pdf_header"):
                    command.append(f"--include-in-header={local_path(project, config['pdf_header'])}")
            elif fmt == "docx" and config.get("reference_doc"):
                command.append(f"--reference-doc={local_path(project, config['reference_doc'])}")
            result = subprocess.run(command, cwd=project, text=True, encoding="utf-8", capture_output=True)
            logs.append({"format": fmt, "returncode": result.returncode, "stderr": result.stderr})
            if result.returncode:
                raise RuntimeError(f"{fmt} build failed; previous outputs preserved:\n{result.stderr}")
            # Pandoc can silently omit missing images; do not release that build.
            if "Could not fetch resource" in result.stderr or "Could not find image" in result.stderr:
                raise RuntimeError(f"{fmt} resource warning; previous outputs preserved:\n{result.stderr}")
            if not destination.is_file() or not destination.stat().st_size:
                raise RuntimeError(f"{fmt} build produced no content")
        if fingerprint != content_digest(project):
            raise RuntimeError("project changed while building; outputs not published")
        # Only generated output paths are replaced, after every requested format succeeds.
        for fmt in config["formats"]:
            shutil.copy2(stage / f"report.{fmt}", output / f"report.{fmt}")
        shutil.copy2(document, output / "document.json")
        manifest = {
            "schema_version": 1, "status": "built", "content_digest": fingerprint,
            "inputs": content_files(project), "built_at": datetime.now(timezone.utc).isoformat(),
            "pandoc": version, "citations": cited, "logs": logs,
            "artifacts": {f"output/report.{fmt}": sha256(output / f"report.{fmt}") for fmt in config["formats"]},
            "toolchain": {name: sha256(Path(__file__).parent / name) for name in ("report_common.py", "build_report.py")},
        }
        write_json(output / "build.json", manifest)
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project_directory", type=Path)
    args = parser.parse_args()
    try:
        result = build(args.project_directory)
    except (OSError, ValueError, RuntimeError, subprocess.SubprocessError) as exc:
        print(f"BUILD FAILED: {exc}")
        return 1
    print(json.dumps({"built": list(result["artifacts"]), "citations": len(result["citations"]), "content_digest": result["content_digest"]}, indent=2))
    print("Build completed. Review artifacts and record QA before release validation.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
