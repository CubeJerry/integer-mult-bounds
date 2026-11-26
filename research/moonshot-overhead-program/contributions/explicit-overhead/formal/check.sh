#!/usr/bin/env bash
# Verify S006 using the pinned Lean release and unchanged OpenAI plan modules.
set -euo pipefail
formal_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
run_dir=$(mktemp -d)
trap 'rm -rf -- "$run_dir"' EXIT
mathlib_sha=d13f23b723b8a846827a245b89c10fc7d3f11612
openai_sha=3344da59991ed94f9ba711217b29c1d760badfa6
export MATHLIB_NO_CACHE_ON_UPDATE=1
lean --version | tee "$run_dir/version.txt"
grep -F 'version 4.34.1' "$run_dir/version.txt" >/dev/null
if [[ -n ${S006_MATHLIB_DIR:-} ]]; then
  mathlib_dir=$(CDPATH= cd -- "$S006_MATHLIB_DIR" && pwd)
else
  mathlib_dir=$run_dir/mathlib
  git init -q "$mathlib_dir"
  git -C "$mathlib_dir" remote add origin https://github.com/leanprover-community/mathlib4.git
  git -C "$mathlib_dir" fetch -q --depth=1 origin "$mathlib_sha"
  git -C "$mathlib_dir" checkout -q --detach FETCH_HEAD
fi
test "$(git -C "$mathlib_dir" rev-parse HEAD)" = "$mathlib_sha"
git -C "$mathlib_dir" diff --quiet HEAD --
proof_root=$run_dir/proofs
source_dir=OAI/Computability/NearSquareRoot
mkdir -p "$proof_root/$source_dir"
for module in KernelColumn KernelPass; do
  curl --fail --silent --show-error --location --retry 3 \
    "https://raw.githubusercontent.com/openai/math/$openai_sha/lean/$source_dir/$module.lean" \
    -o "$proof_root/$source_dir/$module.lean"
done
test "$(git hash-object "$proof_root/$source_dir/KernelColumn.lean")" = 5e4a90e86fbe6b1e52d90480c4b4e3477284d3db
test "$(git hash-object "$proof_root/$source_dir/KernelPass.lean")" = 7fcb8ff3060b9059b6e89f087fde71482fce66ed
token_dir=OAI/Computability/IntegerMultiplication/Port
mkdir -p "$proof_root/$token_dir"
curl --fail --silent --show-error --location --retry 3 \
  "https://raw.githubusercontent.com/openai/math/$openai_sha/lean/$token_dir/Token.lean" \
  -o "$run_dir/original-token.lean"
test "$(git hash-object "$run_dir/original-token.lean")" = 7926eb0b192567a40b0513eddfbd937b206c63b0
# Keep all published declarations and narrow the umbrella import.
{
  printf '%s\n' 'import Mathlib.Data.Rat.Lemmas' 'import Mathlib.Tactic.Ring'
  tail -n +2 "$run_dir/original-token.lean"
} > "$proof_root/$token_dir/Token.lean"
test "$(git hash-object "$proof_root/$token_dir/Token.lean")" = c3bb81d443674cc63fe1dbaf47c9025d1d1ba4ca
for name in RepairDyadic FrobeniusBundles ModularWalshExact TraceBundles AdditiveTraceLayers; do
  cp "$formal_dir/$name.lean" "$proof_root/"
done
mapfile -t modules < <(awk '$1 == "import" && $2 ~ /^Mathlib([.]|$)/ {print $2}' \
  "$proof_root/$source_dir/"*.lean "$proof_root/$token_dir/Token.lean" "$proof_root/"*.lean | sort -u)
cd "$mathlib_dir"
lake exe cache get "${modules[@]}"
export S006_PROOF_ROOT=$proof_root
lake env bash -euo pipefail -c '
  cd "$S006_PROOF_ROOT"
  export LEAN_PATH="$PWD:$LEAN_PATH"
  lean -o OAI/Computability/NearSquareRoot/KernelColumn.olean OAI/Computability/NearSquareRoot/KernelColumn.lean
  lean -o OAI/Computability/NearSquareRoot/KernelPass.olean OAI/Computability/NearSquareRoot/KernelPass.lean
  lean -o OAI/Computability/IntegerMultiplication/Port/Token.olean OAI/Computability/IntegerMultiplication/Port/Token.lean
  for module in RepairDyadic FrobeniusBundles ModularWalshExact TraceBundles AdditiveTraceLayers; do
    lean -DwarningAsError=true -o "$module.olean" "$module.lean"
  done
  for module in RepairDyadic FrobeniusBundles ModularWalshExact TraceBundles AdditiveTraceLayers; do
    leanchecker -v "$module"
  done
  if [[ ${S006_FRESH:-0} == 1 ]]; then
    for module in RepairDyadic FrobeniusBundles ModularWalshExact TraceBundles AdditiveTraceLayers; do
      leanchecker -v --fresh "$module"
    done
  fi
' | tee "$run_dir/axioms.log"
python3 - "$run_dir/axioms.log" <<'PY'
from pathlib import Path
import re
import sys

log = Path(sys.argv[1]).read_text()
targets = {
    "WalshPlan": "twoTermGap_eq checkBlock_has_nondyadic_entry plan_entries_dyadic actual_repair_gaps gap_has_factor_73 native_plan_excludes_singleton_repair",
    "FrobeniusBundles": "finest_stable_partition one_bundle_of_top",
    "CompactSpecialization": "correction_from_inverse correction_exact quotient_spec scalar_spec canonical_scalar_unique matrix_entry_tickets signed_lift_of_ticket scalar_maps_ticket row_pass_tickets source_row_pass_lift target_entry_integer target_scaled_input walsh_sum_bound correct_plan_exact_walsh compact_target_exact_walsh",
    "AdditiveLayers": "rootProduct_zero_iff_address gaps_of_independent independent_field_equivalence subspace_eq_rootProduct forward_is_evaluation inverse_forward forward_inverse Example.field_four_roundtrip",
    "TraceBundles": "no_flip_count even_flip_count empty_odd_flip disjoint_signs kernel_iff_pair_image unique_trace_split full_period_direction",
}
expected = {f"Moonshot.{group}.{name}" for group, names in targets.items() for name in names.split()}
allowed = {"propext", "Classical.choice", "Quot.sound"}
reported = set()
pattern = r"^'([^']+)' (?:depends on axioms: \[([^\]]*)\]|does not depend on any axioms)"
for name, names in re.findall(pattern, log, re.M):
    axioms = {item.strip() for item in names.split(",") if item.strip()}
    if axioms - allowed:
        raise SystemExit(f"Unexpected axioms for {name}: {sorted(axioms - allowed)}")
    reported.add(name)
if reported != expected:
    raise SystemExit(f"Unexpected theorem list; missing={sorted(expected-reported)}, extra={sorted(reported-expected)}")
print(f"Verified the axiom sets of {len(reported)} named results.")
PY
