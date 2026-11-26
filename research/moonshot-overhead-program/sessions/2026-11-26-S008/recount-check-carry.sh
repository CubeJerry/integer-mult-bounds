#!/usr/bin/env bash
# Verify the carry supplier against the two pinned source checkouts.
set -euo pipefail
test "$#" -ge 1 && test "$#" -le 2
session_dir=$(cd -- "$(dirname -- "$0")" && pwd)
mathlib_dir=$(cd -- "$1" && pwd)
original_dir=
if [[ $# == 2 ]]; then original_dir=$(cd -- "$2" && pwd); fi
original_sha=3344da59991ed94f9ba711217b29c1d760badfa6
test "$(git -C "$mathlib_dir" rev-parse HEAD)" = d13f23b723b8a846827a245b89c10fc7d3f11612
git -C "$mathlib_dir" diff --quiet HEAD -- Mathlib lean-toolchain lake-manifest.json
lean --version | grep -F 'version 4.34.1'
stage=$(mktemp -d)
trap 'rm -rf "$stage"' EXIT
modules=(OAI/Computability/IntegerMultiplication/TMModel OAI/Computability/IntegerMultiplication/Goal
         OAI/Computability/NearSquareRoot/Specification OAI/Computability/NearSquareRoot/VisitedCells)
blobs=(06cbddcc5618309f39c41dbe44a97cd9b85f2040 6fd24def585459e192e582a7dfcc4f0f808c1658
       0df09baa9b15ef9d572f99586666cea07f77d4da 4b209de9ccd7c35dc07ce5b5736d757b29ca91b2)
for i in "${!modules[@]}"; do
  name=${modules[i]}
  mkdir -p "$stage/$(dirname "$name")"
  if [[ -z $original_dir ]]; then
    curl -fsSL --retry 3 "https://raw.githubusercontent.com/openai/math/$original_sha/lean/$name.lean" -o "$stage/$name.lean"
  elif [[ -f $original_dir/$name.lean ]]; then
    cp "$original_dir/$name.lean" "$stage/$name.lean"
  else
    git -C "$original_dir" show "$original_sha:lean/$name.lean" > "$stage/$name.lean"
  fi
  test "$(git hash-object "$stage/$name.lean")" = "${blobs[i]}"
done
for name in Handoff Product Carry; do
  cp "$session_dir/recount-${name,,}.lean" "$stage/Recount$name.lean"
  modules+=("Recount$name")
done
base_path=$(cd "$mathlib_dir" && lake env printenv LEAN_PATH)
cd "$stage"
export LEAN_PATH="$PWD:$base_path"
for name in "${modules[@]}"; do
  lean -j1 -DwarningAsError=true -o "$name.olean" "$name.lean"
done
leanchecker -v RecountCarry
