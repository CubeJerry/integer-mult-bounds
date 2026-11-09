"""Portable exact replay of the separately authored sparse-hardware review."""
from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import sys
import tempfile

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "review/independent_current_phase.py"
PIN = "cd2aed187ef6a664f41c7799d3b66a0d1992ce46c1fb4f3546c3c9ca2e68b4ba"


def main():
    raw = SOURCE.read_bytes()
    if sha256(raw).hexdigest() != PIN:
        raise ValueError("unchanged independently authored checker")
    with tempfile.TemporaryDirectory(prefix="current-phase-independent-") as directory:
        root = Path(directory)
        sys.pycache_prefix = str(root / "fresh-bytecode")
        target = root / "receipt.json"
        spec = importlib.util.spec_from_file_location("independent_current_phase", SOURCE)
        module = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = module
        exec(compile(raw, str(SOURCE), "exec"), module.__dict__)
        sys.argv = [str(SOURCE), "--package", str(HERE), "--output", str(target)]
        module.main()
        actual = json.loads(target.read_text())
        expected = json.loads((HERE / "review/RESULT.json").read_text())
        if actual != expected:
            raise ValueError("independent current-phase exact receipt differs")
    print("PASS_CURRENT_PHASE_INDEPENDENT_REVIEW")


if __name__ == "__main__":
    main()
