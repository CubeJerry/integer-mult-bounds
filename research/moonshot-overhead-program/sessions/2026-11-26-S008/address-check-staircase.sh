#!/usr/bin/env bash
set -euo pipefail
test "$#" -ge 1 && test "$#" -le 2
scope=all
if test "$#" -eq 2; then scope=$2; fi
source_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
mathlib_dir=$(CDPATH= cd -- "$1" && pwd)
test "$(git -C "$mathlib_dir" rev-parse HEAD)" = d13f23b723b8a846827a245b89c10fc7d3f11612
git -C "$mathlib_dir" diff --quiet HEAD -- Mathlib lean-toolchain lake-manifest.json
lean --version | rg -F 'version 4.34.1'
area=$(mktemp -d)
trap 'rm -rf "$area"' EXIT
mkdir -p "$area/S008"
cp "$source_dir/full-cutoff.lean" "$area/S008/NumericalCutoff.lean"
cp "$source_dir/whole-profile.lean" "$area/S008/WholeProfile.lean"
cp "$source_dir/all-lengths.lean" "$area/S008/AllLengths.lean"
cp "$source_dir/routing-piecewise.lean" "$area/S008/Piecewise.lean"
cp "$source_dir/routing-history.lean" "$area/S008/PiecewiseHistory.lean"
cp "$source_dir/address-native-staircase.lean" "$area/S008/ThreeSlope.lean"
cp "$source_dir/address-refined-curve.lean" "$area/S008/TrueLabelCurve.lean"
cp "$source_dir/address-refined-cardinality.lean" "$area/S008/TrueLabelCardinality.lean"
cat > "$area/StaircaseChecks.lean" <<'LEAN'
import S008.ThreeSlope
#print axioms S008.ThreeSlope.legal_degree
#print axioms S008.ThreeSlope.height_cap
#print axioms S008.ThreeSlope.all_later_knots
#print axioms S008.ThreeSlope.early_endpoints
#print axioms S008.ThreeSlope.interpolate
#print axioms S008.ThreeSlope.earlier_guard
#print axioms S008.ThreeSlope.dyadic_middle
#print axioms S008.ThreeSlope.coprime_excess
LEAN
cat > "$area/LetterChecks.lean" <<'LEAN'
import S008.TrueLabelCardinality
#print axioms S008.TrueLabel.cardinals_to_true_letter
#print axioms S008.TrueLabel.true_letter_invoice
#print axioms S008.TrueLabel.effective_band
#print axioms S008.TrueLabel.limiting_band
LEAN
case "$scope" in
  staircase|letters|all) ;;
  *) exit 64 ;;
esac
cd "$mathlib_dir"
lake env bash -euc '
  cd "$1"
  export LEAN_PATH="$PWD:$LEAN_PATH"
  build() {
    for module in "$@"; do
      echo "Compiling S008.$module"
      lean -j1 -DwarningAsError=true -o "S008/$module.olean" "S008/$module.lean"
    done
  }
  build NumericalCutoff
  if test "$2" != letters; then
    build WholeProfile AllLengths Piecewise PiecewiseHistory ThreeSlope
    leanchecker -v S008.ThreeSlope
    lean -j1 -DwarningAsError=true StaircaseChecks.lean
  fi
  if test "$2" != staircase; then
    build TrueLabelCurve TrueLabelCardinality
    leanchecker -v S008.TrueLabelCurve
    leanchecker -v S008.TrueLabelCardinality
    lean -j1 -DwarningAsError=true LetterChecks.lean
  fi
' bash "$area" "$scope"
