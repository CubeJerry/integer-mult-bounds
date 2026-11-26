#!/usr/bin/env bash
# Verify the contribution using the pinned Lean release and OpenAI plan modules.
set -euo pipefail
formal_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
run_dir=$(mktemp -d)
trap 'rm -rf -- "$run_dir"' EXIT
mathlib_sha=d13f23b723b8a846827a245b89c10fc7d3f11612
openai_sha=3344da59991ed94f9ba711217b29c1d760badfa6
export MATHLIB_NO_CACHE_ON_UPDATE=1
export MOONSHOT_PROOF_MODULES="RepairDyadic FrobeniusBundles ModularWalshExact TraceBundles AdditiveTraceLayers BundleTransport TraceCoefficientPrefix GroupedComposition TraceShearRadix GroupedAmbientWords TraceFibreJoin TraceRadixRank TraceRadixMatrix RadixCircuitCharges AffineTraceGrid RootFactorDirectory BinaryFactorInventory ProjectedDirectory ProjectedTraceCRT MaskedTensorPascal"
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
copy_openai_module() {
  local relative_path=$1 destination=$2
  if [[ -n ${MOONSHOT_OPENAI_DIR:-} ]]; then
    git -C "$MOONSHOT_OPENAI_DIR" show "$openai_sha:lean/$relative_path" > "$destination"
  else
    curl --fail --silent --show-error --location --retry 3 \
      "https://raw.githubusercontent.com/openai/math/$openai_sha/lean/$relative_path" -o "$destination"
  fi
}
for module in KernelColumn KernelPass; do
  copy_openai_module "$source_dir/$module.lean" "$proof_root/$source_dir/$module.lean"
done
test "$(git hash-object "$proof_root/$source_dir/KernelColumn.lean")" = 5e4a90e86fbe6b1e52d90480c4b4e3477284d3db
test "$(git hash-object "$proof_root/$source_dir/KernelPass.lean")" = 7fcb8ff3060b9059b6e89f087fde71482fce66ed
token_dir=OAI/Computability/IntegerMultiplication/Port
mkdir -p "$proof_root/$token_dir"
copy_openai_module "$token_dir/Token.lean" "$run_dir/original-token.lean"
test "$(git hash-object "$run_dir/original-token.lean")" = 7926eb0b192567a40b0513eddfbd937b206c63b0
# Keep all published declarations and narrow the umbrella import.
{
  printf '%s\n' 'import Mathlib.Data.Rat.Lemmas' 'import Mathlib.Tactic.Ring'
  tail -n +2 "$run_dir/original-token.lean"
} > "$proof_root/$token_dir/Token.lean"
test "$(git hash-object "$proof_root/$token_dir/Token.lean")" = c3bb81d443674cc63fe1dbaf47c9025d1d1ba4ca
for name in $MOONSHOT_PROOF_MODULES; do
  cp "$formal_dir/$name.lean" "$proof_root/"
done
mapfile -t modules < <(awk '$1 == "import" && $2 ~ /^Mathlib([.]|$)/ {print $2}' \
  "$proof_root/$source_dir/"*.lean "$proof_root/$token_dir/Token.lean" "$proof_root/"*.lean | sort -u)
cd "$mathlib_dir"
if [[ ${MOONSHOT_OFFLINE:-0} != 1 ]]; then
  lake exe cache get "${modules[@]}"
fi
export S006_PROOF_ROOT=$proof_root
lake env bash -euo pipefail -c '
  cd "$S006_PROOF_ROOT"
  export LEAN_PATH="$PWD:$LEAN_PATH"
  lean -o OAI/Computability/NearSquareRoot/KernelColumn.olean OAI/Computability/NearSquareRoot/KernelColumn.lean
  lean -o OAI/Computability/NearSquareRoot/KernelPass.olean OAI/Computability/NearSquareRoot/KernelPass.lean
  lean -o OAI/Computability/IntegerMultiplication/Port/Token.olean OAI/Computability/IntegerMultiplication/Port/Token.lean
  for module in $MOONSHOT_PROOF_MODULES; do
    lean -DwarningAsError=true -o "$module.olean" "$module.lean"
  done
  for module in $MOONSHOT_PROOF_MODULES; do
    leanchecker -v "$module"
  done
  if [[ ${S006_FRESH:-0} == 1 ]]; then
    for module in $MOONSHOT_PROOF_MODULES; do
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
    "AffineTraceGrid": "forward_rectangle rectangle_lift_degree inverse_one_fold inverseLift_degree exists_cubic_chart round_trip fibre_iff recover_at recover_degree forward_at moore_ne_zero forward_evaluates",
    "RootFactorDirectory": "recover_literal_remainder at_conjugate selected_points_injective independent_directory binary_factor_iff binary_factor_product binary_directory_lift binary_directory_product binary_factor_at_selected",
    "MaskedTensorPascal": "pair_phase tensor_mul choose_phases masked_tensor",
    "ProjectedDirectory": "annihilate_polynomial_combinations projected_annihilator_iff moment_shift_formula moment_recurrence_iff_minpoly_dvd finite_projected_window descending_cutoff_cofactors",
    "ProjectedTraceCRT": "matrix_inverse trace_fixed binary_trace_bit binary_matrices",
    "TraceShearRadix": "two_shifts row_split forward_trace reverse_trace",
    "GroupedAmbientWords": "fibre_remainder grouped_then_fibre grouped_fibre_coefficient grouped_and_full_same_fibre",
    "TraceFibreJoin": "translated_period same_orbit_iff_twisted actual_orbit_period recover_parent twisted_iff untwisted_iff frobenius_twisted recover_children actual_pair_remainder translated_pair fibre_from_coefficients actual_trace_fibre_join",
    "TraceRadixRank": "trace_monic_degree odd_power_band_rank trace_power_band_rank",
    "TraceRadixMatrix": "trace_order inverse_window_rank trace_both_directions trace_ordered_rank",
    "RadixCircuitCharges": "trace_circuit_budget sum_charges_le interval_rank_le",
    "GroupedComposition": "actual_grouped_division",
    "CoefficientPrefix": "feedback_square_zero streamed_binary_split trace_power_form trace_power_exact truncated_quotient_remainder binary_quotient_remainder",
    "BundleTransport": "stable_coset_support reverse_transport finite_stable_coset_remainder address_injective transported_binary_at_point finite_frobenius_remainder unique_source_digit sourceDigit_bijective transport_at_point binaryHorner_conjugate binary_remainder_transport",
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
