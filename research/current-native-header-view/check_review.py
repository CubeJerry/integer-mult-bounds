"""Run the unchanged independent checker against its exact frozen receipt.

Prepared for @CubeJerry with substantial OpenAI assistance. Apache-2.0.
"""
from pathlib import Path
import runpy
import sys
import tempfile

HERE = Path(__file__).resolve().parent


def main():
    with tempfile.TemporaryDirectory(prefix="native-header-independent-") as directory:
        root = Path(directory)
        sys.pycache_prefix = str(root / "bytecode")
        output = root / "result.json"
        old = sys.argv
        try:
            checker = HERE / "review/check_header_tables.py"
            sys.argv = [str(checker), "--package", str(HERE), "--output", str(output)]
            runpy.run_path(str(checker), run_name="__main__")
        finally:
            sys.argv = old
        expected = (HERE / "review/normal.json").read_bytes()
        if output.read_bytes() != expected or (HERE / "review/optimized.json").read_bytes() != expected:
            raise ValueError("independent exact receipt differs")
    print("PASS_INDEPENDENT_CURRENT_NATIVE_HEADER_REVIEW")


if __name__ == "__main__":
    main()
