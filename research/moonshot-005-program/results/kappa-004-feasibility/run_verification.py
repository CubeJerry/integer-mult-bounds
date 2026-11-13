#!/usr/bin/env python3
"""Reproduce the intermediate-target assessment without rewriting evidence.

This verifies exact finite invoices and source pins. It does not admit a
physical supplier or replay native endpoint words.
"""
from __future__ import annotations

import hashlib
import json
from fractions import Fraction
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


HERE = Path(__file__).resolve().parent


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def run(script: Path, *args: str) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(
        [sys.executable, "-I", "-B", str(script), *args],
        capture_output=True,
        check=False,
    )


def main() -> None:
    with tempfile.TemporaryDirectory(prefix="moonshot-004-review-") as name:
        temporary = Path(name)
        complex_dir = HERE / "complex"
        result = run(complex_dir / "check_004_moment.py")
        require(result.returncode == 0, result.stderr.decode())
        require(result.stdout == (complex_dir / "EXACT-004-RESULT.json").read_bytes(),
                "Complex receipt differs")

        independent = HERE / "complex-independent"
        independent_output = temporary / "independent.json"
        result = run(independent / "verify.py", "--output", str(independent_output))
        require(result.returncode == 0, result.stderr.decode())
        require(independent_output.read_bytes() == (independent / "RESULT.json").read_bytes(),
                "Independent complex receipt differs")

        bit = temporary / "bit"
        shutil.copytree(HERE / "bit", bit)
        result = run(bit / "verify.py")
        require(result.returncode == 0, result.stderr.decode())
        require((bit / "RESULT.json").read_bytes() == (HERE / "bit" / "RESULT.json").read_bytes(),
                "BIT receipt differs")

        # A valid JSON whitespace change must still violate the exact source pin.
        bit_input = bit / "SOURCE-BIT-RESULT.json"
        bit_input.write_bytes(bit_input.read_bytes() + b" ")
        bad = run(bit / "verify.py")
        require(bad.returncode != 0 and b"Changed published histogram fixture" in bad.stderr,
                "BIT changed-source control was not rejected")

        complex_copy = temporary / "complex"
        shutil.copytree(complex_dir, complex_copy)
        caller = complex_copy / "inputs" / "FULL-RESULT.json"
        caller.write_bytes(caller.read_bytes() + b" ")
        bad = run(complex_copy / "check_004_moment.py")
        require(bad.returncode != 0 and b"Source SHA256: FULL-RESULT.json" in bad.stderr,
                "Complex changed-source control was not rejected")

    # Bind the independently read admitted values to unchanged canonical bytes.
    selected = json.loads((HERE / "source-evidence" / "SELECTED-RESULT.json").read_bytes())
    claim_bytes = (HERE / "source-evidence" / "SELECTED-CLAIM.json").read_bytes()
    require(hashlib.sha256(claim_bytes).hexdigest() == selected["certificate_sha256"],
            "Canonical selected claim pin differs")
    claim = json.loads(claim_bytes)
    bit_receipt = json.loads((HERE / "bit" / "RESULT.json").read_bytes())
    admitted = bit_receipt["selected"]
    require(admitted["kappa"] == claim["kappa"] == selected["kappa"],
            "Selected kappa differs")
    require(admitted["uniform_complex_U"] == claim["uniform_templates"][0]["saving"],
            "Complex supplier differs")
    require(admitted["completed_ordinary_BIT_b0"] == claim["admitted_BIT_saving"],
            "Completed ordinary supplier differs")
    require(admitted["covered_BIT_C"] == claim["covered_BIT_saving"],
            "Covered supplier differs")
    complex_receipt = json.loads((HERE / "complex" / "EXACT-004-RESULT.json").read_bytes())
    independent_receipt = json.loads((HERE / "complex-independent" / "RESULT.json").read_bytes())
    independent_input = json.loads((HERE / "complex-independent" / "INPUT.json").read_bytes())
    require(complex_receipt["full_result_sha256"] == selected["source_certificate_sha256"],
            "Full caller differs from selected source")
    require(complex_receipt["source_profiles"]["Q"] == independent_input["profiles"]["Q_actual"],
            "Independent actual-Q profile differs")
    left = next(x for x in complex_receipt["rows"] if x["kappa"] == "1/250")
    right = next(x for x in independent_receipt["targets"] if x["kappa"] == "1/250")
    for left_name, right_name in [
        ("d", "d"),
        ("current_Q_remaining_limit", "actual_Q_additional_room_infinity"),
        ("current_Q_terminal96_limiting_deficit", "current_Q_terminal_96_deficit_infinity"),
    ]:
        a, b = left[left_name], right[right_name]
        interval_a = (Fraction(a["lower"]), Fraction(a["upper"]))
        interval_b = (Fraction(int(b["lower_numerator"]), int(b["denominator"])),
                      Fraction(int(b["upper_numerator"]), int(b["denominator"])))
        require(max(interval_a[0], interval_b[0]) <= min(interval_a[1], interval_b[1]),
                "Independent .004 intervals disagree: " + left_name)
    print("PASS_INTERMEDIATE_004_ASSESSMENT_THREE_PACKAGES_AND_SOURCE_CONTROLS")
    print("No new complete kappa; endpoint and supplier admission remain open.")


if __name__ == "__main__":
    main()
