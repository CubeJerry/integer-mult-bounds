#!/usr/bin/env bash
# Check the physical rules and optionally one arbitrary-data trace against frozen source.
set -euo pipefail

if (( $# < 2 || $# > 3 )); then
  echo "usage: bash node-check-lean.sh PATH_TO_OPENAI_MATH PATH_TO_PINNED_MATHLIB [width|tables|nine|copy|xor|seventytwo|eightyone]" >&2
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
mode=${3:-width}
case "$mode" in
  width|tables|nine|copy|xor|seventytwo|eightyone) ;;
  *) echo "unknown source proof mode: $mode" >&2; exit 2 ;;
esac
cp "$session_dir/node-width-dispatch.lean" "$stage/WidthDispatch.lean"
local_modules=(WidthDispatch)
if [[ "$mode" != width ]]; then
  while read -r source module; do
    cp "$session_dir/$source" "$stage/$module.lean"
    local_modules+=("$module")
  done <<'MODULES'
recount-handoff.lean RecountHandoff
node-source-bridge.lean NodeBridge
MODULES
  python3 -I -B "$session_dir/node-source-tables.py" --extras --split "$stage/NodeTables.lean"
  local_modules+=(NodeTablesSupport)
  for path in "$stage"/NodeTablesRule*.lean; do
    module=${path##*/}
    local_modules+=("${module%.lean}")
  done
  local_modules+=(NodeTables)
  while read -r source module; do
    cp "$session_dir/$source" "$stage/$module.lean"
    local_modules+=("$module")
  done <<'MODULES'
node-direct-zero.lean NativeZero
node-symbolic.lean NodeSymbolic
node-symbolic-cases.lean NodeSymbolicCases
node-exact-cells.lean NodeExactCells
node-locality.lean NodeLocality
node-composition.lean NodeComposition
node-data-oblivious.lean NodeDataLayout
node-linear-tapes.lean NodeLinearTapes
node-affine-tags.lean NodeAffineTags
MODULES
fi
if [[ "$mode" != width && "$mode" != tables ]]; then
  python3 -I -B "$session_dir/node-certified-traces.py" "$mode" "$stage/NativeCertificate.lean"
  shopt -s nullglob
  for path in "$stage"/NativeCertificateWins*.lean "$stage"/NativeCertificateFrames*.lean; do
    module=${path##*/}
    local_modules+=("${module%.lean}")
  done
  local_modules+=(NativeCertificateData)
  for path in "$stage"/NativeCertificatePart*.lean; do
    module=${path##*/}
    local_modules+=("${module%.lean}")
  done
  local_modules+=(NativeCertificate)
fi
if [[ "$mode" != width ]]; then
  {
    for module in WidthDispatch NativeZero NodeSymbolicCases NodeExactCells NodeComposition NodeAffineTags; do
      echo "import $module"
    done
    if [[ "$mode" != tables ]]; then
      echo 'import NativeCertificate'
    fi
    echo '#print axioms S008.NodeSource.check_sound'
    echo '#print axioms S008.NativeZero.all_inputs'
    echo '#print axioms S008.Symbolic.check_sound'
    echo '#print axioms S008.ExactCells.cardinality'
    echo '#print axioms S008.Locality.install_checked'
    echo '#print axioms S008.Composition.ambient_card'
    echo '#print axioms S008.Composition.full_visited'
    echo '#print axioms S008.DataLayout.matched'
    echo '#print axioms S008.DataLayout.direct_safe'
    echo '#print axioms S008.LinearTapes.superposition'
    echo '#print axioms S008.LinearTapes.basis_suffices'
    echo '#print axioms S008.AffineTags.affine_three'
    echo '#print axioms S008.AffineTags.affine_visited'
    if [[ "$mode" != tables ]]; then
      echo "#print axioms S008.Certified.$mode.certified"
      echo "#print axioms S008.Certified.$mode.exact_cells"
    fi
  } > "$stage/NodeProofBundle.lean"
  local_modules+=(NodeProofBundle)
fi
last=${local_modules[-1]}
fresh=${S008_NODE_FRESH:-0}
if [[ "$mode" == width ]]; then
  fresh=${S008_NODE_FRESH:-1}
fi
cd "$mathlib_dir"
mathlib_lean_path=$(lake env printenv LEAN_PATH)
cd "$stage"
export LEAN_PATH="$stage:$mathlib_lean_path"
for module in "${mods[@]}" "${local_modules[@]}"; do
  lean -j1 -DwarningAsError=true -o "$module.olean" "$module.lean" || {
    rc=$?
    echo "Lean failed in $module with status $rc" >&2
    exit "$rc"
  }
done
if [[ "$fresh" == 1 ]]; then
  leanchecker -v --fresh "$last"
else
  leanchecker -v "$last"
fi
