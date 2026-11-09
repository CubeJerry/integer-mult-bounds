"""Cold exact replay of the current signed-format Gaussian monomial join.

Prepared for @CubeJerry with substantial OpenAI assistance. Apache-2.0.
The receipt excludes wall time and includes actual physical action counts.
"""
import argparse
from hashlib import sha256
import json
from pathlib import Path
import shutil
import sys
import tempfile

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))


def source_control(authenticate, need):
    row = next(row for row in json.loads((HERE / "DEPENDENCIES.json").read_text())["files"]
               if row["path"] == "vendor/monomial/signed_phase.py")
    with tempfile.TemporaryDirectory(prefix="current-phase-source-control-") as directory:
        root = Path(directory)
        target = root / row["path"]
        target.parent.mkdir(parents=True)
        shutil.copyfile(HERE / row["path"], target)
        (root / "DEPENDENCIES.json").write_text(json.dumps(dict(files=[row])))
        need(authenticate(root) == 1, "source control authentic baseline")
        with target.open("ab") as output:
            output.write(b"\n# adverse frozen-source change\n")
        try:
            authenticate(root)
        except ValueError:
            return "altered_signed_phase_rejected_before_import"
    raise ValueError("altered phase source was accepted")


def run():
    from phase_binding import authenticate, need
    count = authenticate()
    selected = json.loads((HERE / "vendor/binding/vendor/SELECTED-RESULT.json").read_text())
    assumptions = sorted(value["id"] for value in selected["assumptions"])
    need(selected["kappa"] == "781451/250000000" and 6030 in selected["source_prs"],
         "unchanged selected source")
    need(set(assumptions) == {"native_all_columns", "owned_erasure", "compiler",
                              "precision_tape", "analytic_recovery"},
         "all five selected assumptions retained")
    result = dict(source_exports=count, source_control=source_control(authenticate, need),
                  selected_kappa=selected["kappa"], assumptions=assumptions,
                  complete_selected_packet_executed=False)
    from check_fixture import run_case
    result["single"] = run_case(f=1, K=2, rho=0)
    result["forward"] = run_case(f=2, K=1, inverse=False)
    result["inverse"] = run_case(f=2, K=1, inverse=True)
    result["phase"] = run_case(f=2, K=1, affine=False, outer=2, rows=2, coefficients=3)
    rejected, owner = run_case(guard=True, affine=False, coefficients=3, return_state=True)
    result["guard"] = dict(rejection=rejected,
                           valid_retry=run_case(reuse=owner, affine=False, coefficients=3))
    large, owner = run_case(H=2, affine=False, return_state=True)
    reused, fresh = run_case(H=1, affine=False, reuse=owner), run_case(H=1, affine=False)
    need(reused["physical_actions"] == fresh["physical_actions"], "current-call cleanup time")
    need(reused["retained_cells"] > fresh["retained_cells"], "historical backing is retained")
    result["reuse"] = dict(large=large, reused_small=reused, fresh_small=fresh)
    from check_selected import run as selected_control
    result["selected_control"] = selected_control()
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-result", action="store_true")
    args = parser.parse_args()
    # This applies to transitive source imports too. -B alone does not prevent
    # reading an old bytecode cache. No child interpreter is launched here.
    with tempfile.TemporaryDirectory(prefix="current-phase-fresh-bytecode-") as directory:
        sys.pycache_prefix = directory
        result = json.loads(json.dumps(run(), sort_keys=True))
    encoded = json.dumps(result, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()
    receipt = dict(schema_version=1,
        scope="current-coded signed Gaussian monomial and actual selected phase-control binding",
        sha256=sha256(encoded).hexdigest(), result=result)
    target = HERE / "RESULT.json"
    if args.write_result:
        target.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n")
    elif json.loads(target.read_text()) != receipt:
        raise ValueError("complete exact current-phase replay differs")
    print(json.dumps(receipt, sort_keys=True))
    print("PASS_CURRENT_CODED_GAUSSIAN_MONOMIAL")


if __name__ == "__main__":
    main()
