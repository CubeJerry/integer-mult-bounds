#!/usr/bin/env python3
"""Path-only adapter; authored during recovery, not executed after the outage."""
import hashlib
import importlib.util
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
CHECKER = HERE / "review" / "check_pivot_lemma.py"
EXPECTED = HERE / "review" / "REVIEW-RESULT.json"

def main():
    if hashlib.sha256(CHECKER.read_bytes()).hexdigest() != "4a953929bbe436e1f086bf529cb4509d279addcadb7b410aaed445ce3562d450":
        raise ValueError("frozen independent checker bytes changed")
    spec = importlib.util.spec_from_file_location("recovered_raw_pivot_review", CHECKER)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load frozen checker")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.PROOF = HERE / "PROOF.md"
    with tempfile.TemporaryDirectory(prefix="raw-pivot-review-") as directory:
        module.HERE = Path(directory)
        module.main()
        actual = (module.HERE / "REVIEW-RESULT.json").read_bytes()
        if actual != EXPECTED.read_bytes():
            raise ValueError("independent receipt does not match frozen bytes")
    print("PASS_RECOVERED_RAW_PIVOT_REVIEW")

if __name__ == "__main__":
    main()
