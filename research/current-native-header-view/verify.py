"""Cold exact physical descriptor and actual phase-control replay.

Prepared for @CubeJerry with substantial OpenAI assistance. Apache-2.0.
"""
import argparse
from hashlib import sha256
import json
from pathlib import Path
import sys
import tempfile

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
CODE = ("header_sources.py", "header_view.py", "source_binding.py", "fixture_tools.py",
        "check_descriptor.py", "check_phase.py", "verify.py", "DEPENDENCIES.json")


def normalized(value):
    return json.loads(json.dumps(value, sort_keys=True))


def encoded(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()


def pins():
    return {name: sha256((HERE / name).read_bytes()).hexdigest() for name in CODE}


def run():
    before = pins()
    from header_sources import authenticate, need
    source_files = authenticate()
    from check_descriptor import run as descriptor_run
    descriptor = normalized(descriptor_run())
    from check_phase import run as phase_run
    phase = normalized(phase_run())
    need(pins() == before, "unchanged scientific source bytes during replay")
    selected = json.loads((HERE / "vendor/phase/vendor/binding/vendor/SELECTED-RESULT.json").read_text())
    assumptions = sorted(x["id"] for x in selected["assumptions"])
    need(selected["kappa"] == "781451/250000000" and 6030 in selected["source_prs"]
         and len(assumptions) == 5, "selected record and all five assumptions retained")
    receipt = dict(schema_version=1, scope="first caller-local native encoded header and selected phase controls",
        source_pins=before, source_files=source_files, selected_kappa=selected["kappa"],
        assumptions=assumptions, parent_ambient=145, gamma=1,
        descriptor_sha256=sha256(encoded(descriptor)).hexdigest(),
        phase_sha256=sha256(encoded(phase)).hexdigest(),
        all23_fields_checked=True, normal_optimized_comparable=True,
        full_global_reservation_admission=False, full_native_invocations=0,
        complete_parent_or_fourier_executed=False,
        status="PASS_CURRENT_NATIVE_HEADER_VIEW")
    return descriptor, phase, receipt


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-result", action="store_true")
    args = parser.parse_args()
    with tempfile.TemporaryDirectory(prefix="native-header-fresh-bytecode-") as cache:
        sys.pycache_prefix = cache
        descriptor, phase, receipt = run()
    for name, value in (("DESCRIPTOR-RESULT.json", descriptor),
                        ("PHASE-RESULT.json", phase), ("RESULT.json", receipt)):
        target = HERE / name
        if args.write_result:
            target.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")
        elif json.loads(target.read_text()) != value:
            raise ValueError("exact replay differs: " + name)
    print(json.dumps(receipt, sort_keys=True))
    print("PASS_CURRENT_NATIVE_HEADER_VIEW")


if __name__ == "__main__":
    main()
