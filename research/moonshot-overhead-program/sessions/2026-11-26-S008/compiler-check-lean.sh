#!/usr/bin/env bash
# Compile the true controller modules against pinned sources and replay every finite rule row.
set -euo pipefail
session_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
stage=$(mktemp -d)
trap 'rm -rf "$stage"' EXIT
openai_sha=3344da59991ed94f9ba711217b29c1d760badfa6
mathlib_sha=d13f23b723b8a846827a245b89c10fc7d3f11612
export MATHLIB_NO_CACHE_ON_UPDATE=1
lean --version | tee "$stage/version"
grep -F 'version 4.34.1' "$stage/version" >/dev/null

if [[ -n ${S008_MATHLIB_DIR:-} ]]; then
  library=$(CDPATH= cd -- "$S008_MATHLIB_DIR" && pwd)
else
  library=$stage/mathlib
  git init -q "$library"
  git -C "$library" remote add origin https://github.com/leanprover-community/mathlib4.git
  git -C "$library" fetch -q --depth=1 origin "$mathlib_sha"
  git -C "$library" checkout -q --detach FETCH_HEAD
fi
test "$(git -C "$library" rev-parse HEAD)" = "$mathlib_sha"
git -C "$library" diff --quiet HEAD -- Mathlib lakefile.lean lake-manifest.json lean-toolchain

cd "$stage"
modules=(
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
for pos in "${!modules[@]}"; do
  mod=${modules[pos]}
  mkdir -p "$(dirname "$mod")"
  if [[ -n ${S008_OPENAI_SOURCEDIR:-} ]]; then
    cp "$S008_OPENAI_SOURCEDIR/$mod.lean" "$mod.lean"
  elif [[ $pos = 0 && -n ${S008_OPENAI_TMMODEL:-} ]]; then
    cp "$S008_OPENAI_TMMODEL" "$mod.lean"
  elif [[ -n ${S008_OPENAI_DIR:-} ]]; then
    git -C "$S008_OPENAI_DIR" show "$openai_sha:lean/$mod.lean" > "$mod.lean"
  else
    curl -fsSL --retry 3 "https://raw.githubusercontent.com/openai/math/$openai_sha/lean/$mod.lean" -o "$mod.lean"
  fi
  test "$(git hash-object "$mod.lean")" = "${blobs[pos]}"
done
for source in compiler-{controller,indexed-transfer,indexed-export,unary,binary-access,binary-export,binary-space}.lean; do
  cp "$session_dir/$source" "$stage/"
done
cd "$library"
needed=(Mathlib/Basic/Finite/Prod Mathlib/Data/Nat/Log Mathlib/Analysis/SpecialFunctions/Pow/Real
        Mathlib/Data/Set/Card Mathlib/Data/Int/Interval Mathlib/Algebra/BigOperators/Group/Finset/Basic)
for module in "${needed[@]}"; do
  if [[ ! -f ".lake/build/lib/lean/$module.olean" ]]; then
    lake exe cache get "${needed[@]/%/.lean}"
    break
  fi
done
lake env bash -euc '
  cd "$1"
  shift
  export LEAN_PATH="$PWD:$LEAN_PATH"
  for name in "$@" compiler-controller compiler-indexed-transfer compiler-unary compiler-binary-access compiler-binary-space; do
    printf "Checking %s\n" "$name"
    lean -j1 -DwarningAsError=true -o "$name.olean" "$name.lean"
  done
  lean -DwarningAsError=true --run compiler-indexed-export.lean > rule
  lean -DwarningAsError=true --run compiler-binary-export.lean > binary-rule
' bash "$stage" "${modules[@]}"
python3 -I -B "$session_dir/compiler-indexed-transfer.py" --table "$stage/rule"
python3 -I -B "$session_dir/compiler-binary-access.py" --table "$stage/binary-rule"
