#!/usr/bin/env bash
# Usage: bash walsh-check-lean.sh PATH_TO_OPENAI_MATH PATH_TO_PINNED_MATHLIB
# Requires the pinned Lean release on PATH and Mathlib's imported modules built/cached.
set -euo pipefail
test "$#" -eq 2
session_dir=$(cd -- "$(dirname -- "$0")" && pwd)
openai_dir=$(cd -- "$1" && pwd)
mathlib_dir=$(cd -- "$2" && pwd)
openai_sha=3344da59991ed94f9ba711217b29c1d760badfa6
mathlib_sha=d13f23b723b8a846827a245b89c10fc7d3f11612
test "$(git -C "$mathlib_dir" rev-parse HEAD)" = "$mathlib_sha"
git -C "$mathlib_dir" diff --quiet HEAD -- Mathlib lean-toolchain lake-manifest.json
root=$(mktemp -d)
trap 'rm -rf "$root"' EXIT
kernel=OAI/Computability/NearSquareRoot
token=OAI/Computability/IntegerMultiplication/Port
mkdir -p "$root/$kernel" "$root/$token"
for module in KernelColumn KernelPass; do
    git -C "$openai_dir" show "$openai_sha:lean/$kernel/$module.lean" > "$root/$kernel/$module.lean"
done
git -C "$openai_dir" show "$openai_sha:lean/$token/Token.lean" > "$root/OriginalToken.lean"
test "$(git hash-object "$root/$kernel/KernelColumn.lean")" = 5e4a90e86fbe6b1e52d90480c4b4e3477284d3db
test "$(git hash-object "$root/$kernel/KernelPass.lean")" = 7fcb8ff3060b9059b6e89f087fde71482fce66ed
test "$(git hash-object "$root/OriginalToken.lean")" = 7926eb0b192567a40b0513eddfbd937b206c63b0
# Follow the contribution's previous narrow-import build of the unmodified declaration body.
{
    printf '%s\n' 'import Mathlib.Data.Rat.Lemmas' 'import Mathlib.Tactic.Ring'
    tail -n +2 "$root/OriginalToken.lean"
} > "$root/$token/Token.lean"
test "$(git hash-object "$root/$token/Token.lean")" = c3bb81d443674cc63fe1dbaf47c9025d1d1ba4ca
cp "$session_dir/../../contributions/explicit-overhead/formal/ModularWalshExact.lean" "$root/"
test "$(git hash-object "$root/ModularWalshExact.lean")" = db7c503a6b55e9f46e1fc79aa0e14b5caaf8623e
cp "$session_dir/walsh-aligned-proof.lean" "$root/WalshAligned.lean"
cd "$mathlib_dir"
lake env bash -euo pipefail -c '
    cd "$1"
    export LEAN_PATH="$PWD:$LEAN_PATH"
    lean --version | tee version.txt
    grep -F "version 4.34.1" version.txt >/dev/null
    for module in "$2/KernelColumn" "$2/KernelPass" "$3/Token" ModularWalshExact; do
        lean -DwarningAsError=true -o "$module.olean" "$module.lean" > /dev/null
    done
    lean -DwarningAsError=true -o WalshAligned.olean WalshAligned.lean | tee axioms.txt
' bash "$root" "$kernel" "$token"
python3 - "$root/axioms.txt" <<'PY'
from pathlib import Path
import re
import sys

expected = set('full_spacing_product subset_spacing_dvd_factorial oriented_spacing_eq '
               'lagrange_den_dvd repair_entry_den_dvd correction_eq_short aligned_scalar_token'.split())
seen = set()
for name, axioms in re.findall(r"'Moonshot\.AlignedWalsh\.(\w+)' depends on axioms: \[([^\]]*)\]",
                              Path(sys.argv[1]).read_text()):
    if set(axioms.split(', ')) - {'propext', 'Classical.choice', 'Quot.sound'}:
        raise SystemExit(f'Unexpected axioms for {name}: {axioms}')
    seen.add(name)
if seen != expected:
    raise SystemExit(f'Unexpected theorem set: {seen ^ expected}')
print(f'Checked the axiom sets of {len(seen)} aligned-Walsh results.')
PY
