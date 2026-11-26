#!/usr/bin/env bash
# Verify S006 using the pinned Lean release and unchanged OpenAI plan modules.
set -euo pipefail
formal_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
run_dir=$(mktemp -d)
trap 'rm -rf -- "$run_dir"' EXIT
mathlib_sha=d13f23b723b8a846827a245b89c10fc7d3f11612
openai_sha=3344da59991ed94f9ba711217b29c1d760badfa6
export MATHLIB_NO_CACHE_ON_UPDATE=1
lean --version | tee "$run_dir/version.txt"
grep -F 'version 4.34.1' "$run_dir/version.txt" >/dev/null
if [[ -n ${S006_MATHLIB_DIR:-} ]]; then
  mathlib_dir=$(CDPATH= cd -- "$S006_MATHLIB_DIR" && pwd)
else
  mathlib_dir=$run_dir/mathlib
  git init -q "$mathlib_dir"
  git -C "$mathlib_dir" remote add origin https://github.com/leanprover-community/mathlib4.git
  git -C "$mathlib_dir" fetch -q --depth=1 origin "$mathlib_sha"
  git -C "$mathlib_dir" checkout -q --detach FETCH_HEAD
fi
test "$(git -C "$mathlib_dir" rev-parse HEAD)" = "$mathlib_sha"
git -C "$mathlib_dir" diff --quiet HEAD --
proof_root=$run_dir/proofs
source_dir=OAI/Computability/NearSquareRoot
mkdir -p "$proof_root/$source_dir"
for module in KernelColumn KernelPass; do
  curl --fail --silent --show-error --location --retry 3 \
    "https://raw.githubusercontent.com/openai/math/$openai_sha/lean/$source_dir/$module.lean" \
    -o "$proof_root/$source_dir/$module.lean"
done
test "$(git hash-object "$proof_root/$source_dir/KernelColumn.lean")" = 5e4a90e86fbe6b1e52d90480c4b4e3477284d3db
test "$(git hash-object "$proof_root/$source_dir/KernelPass.lean")" = 7fcb8ff3060b9059b6e89f087fde71482fce66ed
cp "$formal_dir/RepairDyadic.lean" "$formal_dir/FrobeniusBundles.lean" "$proof_root/"
mapfile -t modules < <(awk '$1 == "import" && $2 ~ /^Mathlib([.]|$)/ {print $2}' \
  "$proof_root/$source_dir/"*.lean "$proof_root/"*.lean | sort -u)
cd "$mathlib_dir"
lake exe cache get "${modules[@]}"
export S006_PROOF_ROOT=$proof_root
lake env bash -euo pipefail -c '
  cd "$S006_PROOF_ROOT"
  export LEAN_PATH="$PWD:$LEAN_PATH"
  lean -o OAI/Computability/NearSquareRoot/KernelColumn.olean OAI/Computability/NearSquareRoot/KernelColumn.lean
  lean -o OAI/Computability/NearSquareRoot/KernelPass.olean OAI/Computability/NearSquareRoot/KernelPass.lean
  lean -DwarningAsError=true -o RepairDyadic.olean RepairDyadic.lean
  lean -DwarningAsError=true -o FrobeniusBundles.olean FrobeniusBundles.lean
' | tee "$run_dir/axioms.log"
for theorem in plan_entries_dyadic actual_repair_gaps gap_has_factor_73 native_plan_excludes_singleton_repair; do
  grep -F "Moonshot.WalshPlan.$theorem" "$run_dir/axioms.log" >/dev/null
done
for theorem in finest_stable_partition one_bundle_of_top; do
  grep -F "Moonshot.FrobeniusBundles.$theorem" "$run_dir/axioms.log" >/dev/null
done
if grep -E 'sorryAx|Lean\.ofReduceBool|Lean\.trustCompiler' "$run_dir/axioms.log"; then
  exit 1
fi
