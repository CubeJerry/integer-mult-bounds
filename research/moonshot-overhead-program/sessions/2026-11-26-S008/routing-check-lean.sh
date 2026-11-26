#!/usr/bin/env bash
# Rebuild the rounded Walsh transfer and replay its Lean kernel certificates.
set -euo pipefail
test "$#" -ge 1 && test "$#" -le 2
if test "$#" -eq 2; then test "$2" = --fresh; fi
session_dir=$(cd -- "$(dirname -- "$0")" && pwd)
mathlib_dir=$(cd -- "$1" && pwd)
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
base_path=$(cd -- "$mathlib_dir" && lake env printenv LEAN_PATH)
cd -- "$out_dir"
export LEAN_PATH="$PWD:$base_path"
for module in NumericalCutoff WholeProfile Piecewise PiecewiseHistory NativeFacets; do
    lean -j1 -DwarningAsError=true -o "S008/$module.olean" "S008/$module.lean"
done
cat > Axioms.lean <<'CHECK'
import S008.NativeFacets
#print axioms S008.Piecewise.Facets.native_is_scheduled
#print axioms S008.Piecewise.weighted_quarter
#print axioms S008.Piecewise.native_slot_covered
#print axioms S008.Piecewise.phi_blend
#print axioms S008.Piecewise.typed_data_gain
#print axioms S008.Piecewise.ordinary_45_gain
#print axioms S008.Piecewise.historical_envelope
#print axioms S008.Piecewise.rounded_natlog_at_simple
CHECK
lean -j1 -DwarningAsError=true Axioms.lean
if test "${2:-}" = --fresh; then
    leanchecker -v --fresh S008.NativeFacets
else
    leanchecker -v S008.Piecewise
    leanchecker -v S008.PiecewiseHistory
    leanchecker -v S008.NativeFacets
fi
