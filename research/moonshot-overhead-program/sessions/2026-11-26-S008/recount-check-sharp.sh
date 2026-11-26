#!/usr/bin/env bash
# Rebuild the quantified, full-prefactor cutoff against the pinned math library.
set -euo pipefail
test "$#" -eq 1
session_dir=$(cd -- "$(dirname -- "$0")" && pwd)
mathlib_dir=$(cd -- "$1" && pwd)
test "$(git -C "$mathlib_dir" rev-parse HEAD)" = d13f23b723b8a846827a245b89c10fc7d3f11612
git -C "$mathlib_dir" diff --quiet HEAD -- Mathlib lean-toolchain lake-manifest.json
lean --version | grep -F 'version 4.34.1'
stage=$(mktemp -d)
trap 'rm -rf "$stage"' EXIT
mkdir -p "$stage/S008"
cp "$session_dir/full-cutoff.lean" "$stage/S008/NumericalCutoff.lean"
cp "$session_dir/recount-sharp.lean" "$stage/S008/RecountSharp.lean"
base_path=$(cd "$mathlib_dir" && lake env printenv LEAN_PATH)
cd "$stage"
export LEAN_PATH="$PWD:$base_path"
for module in NumericalCutoff RecountSharp; do
  lean -j1 -DwarningAsError=true -o "S008/$module.olean" "S008/$module.lean"
done
leanchecker -v --fresh S008.RecountSharp
