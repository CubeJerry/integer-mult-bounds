#!/usr/bin/env bash
# Rebuild the numerical time proofs with the pinned compiler and math library.
set -euo pipefail
test "$#" -eq 1
session_dir=$(cd -- "$(dirname -- "$0")" && pwd)
mathlib_dir=$(cd -- "$1" && pwd)
test "$(git -C "$mathlib_dir" rev-parse HEAD)" = d13f23b723b8a846827a245b89c10fc7d3f11612
git -C "$mathlib_dir" diff --quiet HEAD -- Mathlib lean-toolchain lake-manifest.json
lean --version | grep -F 'version 4.34.1'
scratch=$(mktemp -d)
trap 'rm -rf "$scratch"' EXIT
mkdir -p "$scratch/S008"
cp "$session_dir/full-cutoff.lean" "$scratch/S008/NumericalCutoff.lean"
cp "$session_dir/native-contraction.lean" "$scratch/S008/NativeContraction.lean"
cp "$session_dir/whole-profile.lean" "$scratch/S008/WholeProfile.lean"
cp "$session_dir/all-lengths.lean" "$scratch/S008/AllLengths.lean"
base_path=$(cd "$mathlib_dir" && lake env printenv LEAN_PATH)
cd "$scratch"
export LEAN_PATH="$PWD:$base_path"
for name in NumericalCutoff NativeContraction WholeProfile AllLengths; do
    lean -j1 -DwarningAsError=true -o "S008/$name.olean" "S008/$name.lean"
done
cat > Axioms.lean <<'CHECK'
import S008.NativeContraction
import S008.AllLengths
#print axioms S008.NativeQuantitative.shared_rounding
#print axioms S008.NativeQuantitative.native_weight_quarter
#print axioms S008.NumericalCutoff.unit_501_of_71
#print axioms S008.WholeProfile.raw_excess_71
#print axioms S008.WholeProfile.natlog_501_of_invoice
#print axioms S008.AllLengths.dyadic_middle
#print axioms S008.AllLengths.coprime_excess
CHECK
lean -j1 -DwarningAsError=true Axioms.lean
leanchecker -v --fresh S008.NativeContraction
leanchecker -v S008.AllLengths

