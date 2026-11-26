#!/usr/bin/env bash
# Rebuild the rounded Walsh transfer and replay its Lean kernel certificates.
set -euo pipefail
test "$#" -ge 1 && test "$#" -le 3
session_dir=$(cd -- "$(dirname -- "$0")" && pwd)
mathlib_dir=$(cd -- "$1" && pwd)
shift
use_fresh=false
use_refined=false
for mode in "$@"; do
    case "$mode" in
        --fresh) use_fresh=true ;;
        --refined) use_refined=true ;;
        *) exit 2 ;;
    esac
done
test "$(git -C "$mathlib_dir" rev-parse HEAD)" = d13f23b723b8a846827a245b89c10fc7d3f11612
git -C "$mathlib_dir" diff --quiet HEAD -- Mathlib lean-toolchain lake-manifest.json
lean --version | grep -F 'version 4.34.1'
out_dir=$(mktemp -d)
trap 'rm -rf "$out_dir"' EXIT
mkdir -p "$out_dir/S008"
cp "$session_dir/full-cutoff.lean" "$out_dir/S008/NumericalCutoff.lean"
cp "$session_dir/whole-profile.lean" "$out_dir/S008/WholeProfile.lean"
cp "$session_dir/routing-piecewise.lean" "$out_dir/S008/Piecewise.lean"
cp "$session_dir/routing-history.lean" "$out_dir/S008/PiecewiseHistory.lean"
cp "$session_dir/routing-native-facets.lean" "$out_dir/S008/NativeFacets.lean"
cp "$session_dir/routing-density.lean" "$out_dir/S008/PiecewiseDensity.lean"
modules=(NumericalCutoff WholeProfile Piecewise PiecewiseHistory NativeFacets PiecewiseDensity)
replay_modules=(Piecewise PiecewiseHistory NativeFacets PiecewiseDensity)
if "$use_refined"; then
    cp "$session_dir/recount-sharp.lean" "$out_dir/S008/RecountSharp.lean"
    cp "$session_dir/recount-refined.lean" "$out_dir/S008/RecountRefined.lean"
    cp "$session_dir/routing-refined-frame.lean" "$out_dir/S008/RefinedFrame.lean"
    cp "$session_dir/routing-refined-clock.lean" "$out_dir/S008/RefinedClock.lean"
    cp "$session_dir/routing-refined-schedule.lean" "$out_dir/S008/RefinedSchedule.lean"
    modules+=(RecountSharp RecountRefined RefinedFrame RefinedClock RefinedSchedule)
    replay_modules+=(RefinedFrame RefinedClock RefinedSchedule)
fi
target=${modules[-1]}
base_path=$(cd -- "$mathlib_dir" && lake env printenv LEAN_PATH)
cd -- "$out_dir"
export LEAN_PATH="$PWD:$base_path"
for module in "${modules[@]}"; do
    lean -j1 -DwarningAsError=true -o "S008/$module.olean" "S008/$module.lean"
done
printf 'import S008.%s\n' "$target" > Axioms.lean
cat >> Axioms.lean <<'CHECK'
#print axioms S008.Piecewise.shifted_prefix_density
#print axioms S008.Piecewise.Facets.native_is_scheduled
#print axioms S008.Piecewise.weighted_quarter
#print axioms S008.Piecewise.native_slot_covered
#print axioms S008.Piecewise.phi_blend
#print axioms S008.Piecewise.typed_data_gain
#print axioms S008.Piecewise.ordinary_45_gain
#print axioms S008.Piecewise.historical_envelope
#print axioms S008.Piecewise.rounded_natlog_at_simple
CHECK
if "$use_refined"; then
    cat >> Axioms.lean <<'CHECK'
#print axioms S008.Piecewise.Refined.rounded_frame
#print axioms S008.Piecewise.Refined.paid_all_later
#print axioms S008.Piecewise.Refined.measured29_valid
#print axioms S008.Piecewise.Refined.schedule_natural_clock
CHECK
fi
lean -j1 -DwarningAsError=true Axioms.lean
if "$use_fresh"; then
    leanchecker -v --fresh "S008.$target"
else
    for module in "${replay_modules[@]}"; do leanchecker -v "S008.$module"; done
fi
