#!/usr/bin/env bash
# Check the width dispatcher against the pinned physical machine and visit definitions.
set -euo pipefail

if [[ $# != 2 ]]; then
  echo "usage: bash node-check-lean.sh PATH_TO_OPENAI_MATH PATH_TO_PINNED_MATHLIB" >&2
  exit 2
fi
session_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
source_dir=$(CDPATH= cd -- "$1" && pwd)
mathlib_dir=$(CDPATH= cd -- "$2" && pwd)
openai_commit=3344da59991ed94f9ba711217b29c1d760badfa6
mathlib_commit=d13f23b723b8a846827a245b89c10fc7d3f11612
test "$(git -C "$mathlib_dir" rev-parse HEAD)" = "$mathlib_commit"
test "$(git -C "$source_dir" rev-parse "$openai_commit")" = "$openai_commit"
git -C "$mathlib_dir" diff --quiet HEAD -- Mathlib lakefile.lean lean-toolchain lake-manifest.json
stage=$(mktemp -d)
trap 'rm -rf "$stage"' EXIT
lean --version > "$stage/version"
rg -q --fixed-strings 'version 4.34.1' "$stage/version"
mods=(
  OAI/Computability/IntegerMultiplication/TMModel
  OAI/Computability/IntegerMultiplication/Goal
  OAI/Computability/NearSquareRoot/Specification
  OAI/Computability/NearSquareRoot/VisitedCells
)
blobs=(
  06cbddcc5618309f39c41dbe44a97cd9b85f2040
  6fd24def585459e192e582a7dfcc4f0f808c1658
  0df09baa9b15ef9d572f99586666cea07f77d4da
  4b209de9ccd7c35dc07ce5b5736d757b29ca91b2
)
for i in "${!mods[@]}"; do
  path="${mods[i]}.lean"
  mkdir -p "$stage/$(dirname "$path")"
  git -C "$source_dir" show "$openai_commit:lean/$path" > "$stage/$path"
  test "$(git hash-object "$stage/$path")" = "${blobs[i]}"
done
cp "$session_dir/node-width-dispatch.lean" "$stage/WidthDispatch.lean"
cd "$mathlib_dir"
lake env bash -euc '
  cd "$1"
  shift
  export LEAN_PATH="$PWD:$LEAN_PATH"
  for module in "$@"; do
    lean -DwarningAsError=true -o "$module.olean" "$module.lean"
  done
  leanchecker -v --fresh WidthDispatch
' bash "$stage" "${mods[@]}" WidthDispatch
