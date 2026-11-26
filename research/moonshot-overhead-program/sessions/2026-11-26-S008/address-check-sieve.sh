#!/usr/bin/env bash
set -euo pipefail
test "$#" -eq 1
source_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
mathlib_dir=$(CDPATH= cd -- "$1" && pwd)
test "$(git -C "$mathlib_dir" rev-parse HEAD)" = d13f23b723b8a846827a245b89c10fc7d3f11612
git -C "$mathlib_dir" diff --quiet HEAD -- Mathlib lean-toolchain lake-manifest.json
lean --version | grep -F 'version 4.34.1'
area=$(mktemp -d)
trap 'rm -rf "$area"' EXIT
mkdir -p "$area/S008"
cp "$source_dir/address-sieve.lean" "$area/S008/AxisSieve.lean"
cat > "$area/AxisChecks.lean" <<'LEAN'
import S008.AxisSieve
#print axioms S008.AxisSieve.degree_tail
#print axioms S008.AxisSieve.bonferroni_indicator
#print axioms S008.AxisSieve.interval_divisor_discrepancy
#print axioms S008.AxisSieve.single_omission
#print axioms S008.AxisSieve.exact_small_prime_product
#print axioms S008.AxisSieve.bonferroni_relative
#print axioms S008.AxisSieve.positive_survivor
LEAN
cd "$mathlib_dir"
lake env bash -euc '
  cd "$1"
  export LEAN_PATH="$PWD:$LEAN_PATH"
  lean -j1 -DwarningAsError=true -o S008/AxisSieve.olean S008/AxisSieve.lean
  leanchecker -v S008.AxisSieve
  lean -j1 -DwarningAsError=true AxisChecks.lean
' bash "$area"
