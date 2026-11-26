#!/usr/bin/env bash
# Check the two original source modules and the repair obstruction against exact pins.
set -euo pipefail
formal_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
verification_root=$(mktemp -d)
trap 'rm -rf -- "$verification_root"' EXIT
mathlib_sha=d13f23b723b8a846827a245b89c10fc7d3f11612
openai_sha=3344da59991ed94f9ba711217b29c1d760badfa6
lean --version | tee "$verification_root/version.txt"
grep -F 'version 4.34.1' "$verification_root/version.txt" >/dev/null
git init -q "$verification_root/mathlib"
git -C "$verification_root/mathlib" remote add origin https://github.com/leanprover-community/mathlib4.git
git -C "$verification_root/mathlib" fetch -q --depth=1 origin "$mathlib_sha"
git -C "$verification_root/mathlib" checkout -q --detach FETCH_HEAD
test "$(git -C "$verification_root/mathlib" rev-parse HEAD)" = "$mathlib_sha"
cd "$verification_root/mathlib"
source_dir=OAI/Computability/NearSquareRoot
mkdir -p "$source_dir"
for module in KernelColumn KernelPass; do
  curl --fail --silent --show-error --location --retry 3 \
    "https://raw.githubusercontent.com/openai/math/$openai_sha/lean/$source_dir/$module.lean" \
    -o "$source_dir/$module.lean"
done
test "$(git hash-object "$source_dir/KernelColumn.lean")" = 5e4a90e86fbe6b1e52d90480c4b4e3477284d3db
test "$(git hash-object "$source_dir/KernelPass.lean")" = 7fcb8ff3060b9059b6e89f087fde71482fce66ed
rings_dir=OAI/LinearAlgebra/FiniteFourier
mkdir -p "$rings_dir"
curl --fail --silent --show-error --location --retry 3 \
  "https://raw.githubusercontent.com/openai/math/$openai_sha/lean/$rings_dir/ProtectedRationals.lean" \
  -o "$rings_dir/ProtectedRationals.lean"
test "$(git hash-object "$rings_dir/ProtectedRationals.lean")" = 039c2439980127018843bba163b09f537bed3590
cp "$formal_dir/RepairDyadic.lean" RepairDyadic.lean
mapfile -t modules < <(awk '$1 == "import" && $2 ~ /^Mathlib([.]|$)/ {print $2}' \
  "$source_dir/KernelColumn.lean" "$source_dir/KernelPass.lean" "$rings_dir/ProtectedRationals.lean" RepairDyadic.lean | sort -u)
lake exe cache get "${modules[@]}"
lake env bash -euo pipefail -c '
  export LEAN_PATH="$PWD:${LEAN_PATH:-}"
  lean -o OAI/Computability/NearSquareRoot/KernelColumn.olean OAI/Computability/NearSquareRoot/KernelColumn.lean
  lean -o OAI/Computability/NearSquareRoot/KernelPass.olean OAI/Computability/NearSquareRoot/KernelPass.lean
  lean -o OAI/LinearAlgebra/FiniteFourier/ProtectedRationals.olean OAI/LinearAlgebra/FiniteFourier/ProtectedRationals.lean
  lean -DwarningAsError=true -o RepairDyadic.olean RepairDyadic.lean
'
