#!/usr/bin/env python3
"""Compile the isolated pure-Std S005 proofs and record exact source/axiom receipts."""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile

FILES = (
    "ArenaSchedule.lean",
    "BatchPath.lean",
    "CopiedCountFormula.lean",
    "CountSemantics.lean",
)
ALLOWED_AXIOMS = {"propext", "Quot.sound", "Classical.choice"}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--lean", required=True, type=Path)
    parser.add_argument("--output", type=Path, default=Path("verification.json"))
    args = parser.parse_args()
    root = Path(__file__).resolve().parent
    lean = args.lean.resolve()
    version = subprocess.run(
        [str(lean), "--version"], check=True, text=True, capture_output=True
    ).stdout.strip()
    records = []
    with tempfile.TemporaryDirectory(prefix="s005-count-proof-") as temporary:
        build = Path(temporary)
        environment = os.environ.copy()
        environment["LEAN_PATH"] = str(build)
        for filename in FILES:
            source = root / filename
            compiled = build / (source.stem + ".olean")
            command = [
                str(lean), "-DwarningAsError=true", "-o", str(compiled), str(source)
            ]
            result = subprocess.run(
                command, cwd=root, env=environment, text=True, capture_output=True
            )
            summaries = re.findall(
                r"depends on axioms: \[([^\]]*)\]", result.stdout
            )
            used = {
                value.strip()
                for summary in summaries
                for value in summary.split(",")
                if value.strip()
            }
            if result.returncode or "sorryAx" in result.stdout + result.stderr:
                raise RuntimeError(
                    f"{filename} did not verify:\n{result.stdout}{result.stderr}"
                )
            if not used <= ALLOWED_AXIOMS:
                raise RuntimeError(f"{filename} uses unexpected axioms: {used}")
            if not summaries and "does not depend on any axioms" not in result.stdout:
                raise RuntimeError(f"{filename} printed no dependency checks")
            records.append({
                "file": filename,
                "sha256": sha256(source),
                "command": command,
                "lean_path": str(build),
                "exit_code": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "printed_axioms": sorted(used),
            })
    report = {
        "checked_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
        "toolchain": version,
        "source_toolchain": "leanprover/lean4:v4.34.1 (not built)",
        "programme_pin": "62d9d8e917379cb2edc17c9761e12e2345bc01f4",
        "openai_pin": "3344da59991ed94f9ba711217b29c1d760badfa6",
        "scope": (
            "Abstract allocation/batch contracts; literal copied balanced "
            "count-formula syntax, local and whole-word exact semantics, "
            "literal zero padding, copied-tree size and degree bounds. "
            "No physical machine refinement, cyclic factorization, OAI "
            "build, comparator or multiplier theorem."
        ),
        "verifier_sha256": sha256(Path(__file__).resolve()),
        "dependency_order": list(FILES),
        "records": records,
    }
    output = args.output if args.output.is_absolute() else root / args.output
    output.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({
        "verified_files": len(records),
        "toolchain": version,
        "receipt": str(output),
        "status": "pass",
    }))


if __name__ == "__main__":
    main()

