#!/usr/bin/env bash
# Rebuild one physical proof against the original OAI finite-tape definitions.
set -euo pipefail

case ${1:-handoff} in
  handoff) local_modules=(RecountHandoff) ;;
  product) local_modules=(RecountHandoff RecountProduct) ;;
  *) echo 'Usage: recount-check-lean.sh [handoff|product]' >&2; exit 2 ;;
esac
test "$#" -le 1

session_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
staging=$(mktemp -d)
trap 'rm -rf "$staging"' EXIT
openai_sha=3344da59991ed94f9ba711217b29c1d760badfa6
mathlib_sha=d13f23b723b8a846827a245b89c10fc7d3f11612
export MATHLIB_NO_CACHE_ON_UPDATE=1
lean --version | tee "$staging/version.txt"
grep -F 'version 4.34.1' "$staging/version.txt" >/dev/null

if [[ -n ${S008_MATHLIB_DIR:-} ]]; then
  mathlib_dir=$(CDPATH= cd -- "$S008_MATHLIB_DIR" && pwd)
else
  mathlib_dir=$staging/mathlib
  git init -q "$mathlib_dir"
  git -C "$mathlib_dir" remote add origin https://github.com/leanprover-community/mathlib4.git
  git -C "$mathlib_dir" fetch -q --depth=1 origin "$mathlib_sha"
  git -C "$mathlib_dir" checkout -q --detach FETCH_HEAD
fi
test "$(git -C "$mathlib_dir" rev-parse HEAD)" = "$mathlib_sha"
git -C "$mathlib_dir" diff --quiet HEAD -- Mathlib lakefile.lean lean-toolchain lake-manifest.json

proof_root=$staging/proofs
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
for i in "${!modules[@]}"; do
  path=${modules[i]}.lean
  mkdir -p "$proof_root/$(dirname "$path")"
  if [[ -n ${S008_OPENAI_DIR:-} ]]; then
    git -C "$S008_OPENAI_DIR" show "$openai_sha:lean/$path" > "$proof_root/$path"
  else
    curl -fsSL --retry 3 "https://raw.githubusercontent.com/openai/math/$openai_sha/lean/$path" -o "$proof_root/$path"
  fi
  test "$(git hash-object "$proof_root/$path")" = "${blobs[i]}"
done
cp "$session_dir/recount-handoff.lean" "$proof_root/RecountHandoff.lean"
if [[ ${local_modules[-1]} == RecountProduct ]]; then
  cp "$session_dir/recount-product.lean" "$proof_root/RecountProduct.lean"
fi

cd "$mathlib_dir"
needed=(Mathlib/Basic/Finite/Prod Mathlib/Data/Nat/Log Mathlib/Analysis/SpecialFunctions/Pow/Real
        Mathlib/Data/Set/Card Mathlib/Data/Int/Interval Mathlib/Algebra/BigOperators/Group/Finset/Basic)
if [[ ${local_modules[-1]} == RecountProduct ]]; then
  needed+=(Mathlib/Tactic/Ring Mathlib/Tactic/Linarith)
fi
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
  for module in "$@"; do
    lean -j1 -DwarningAsError=true -o "$module.olean" "$module.lean"
  done
  leanchecker -v --fresh "${!#}"
' bash "$proof_root" "${modules[@]}" "${local_modules[@]}"
