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
mod=OAI/Computability/IntegerMultiplication/TMModel
mkdir -p "$(dirname "$mod")"
if [[ -n ${S008_OPENAI_TMMODEL:-} ]]; then
  cp "$S008_OPENAI_TMMODEL" "$mod.lean"
elif [[ -n ${S008_OPENAI_DIR:-} ]]; then
  git -C "$S008_OPENAI_DIR" show "$openai_sha:lean/$mod.lean" > "$mod.lean"
else
  curl -fsSL --retry 3 "https://raw.githubusercontent.com/openai/math/$openai_sha/lean/$mod.lean" -o "$mod.lean"
fi
test "$(git hash-object "$mod.lean")" = 06cbddcc5618309f39c41dbe44a97cd9b85f2040
cp "$session_dir"/compiler-{controller,indexed-transfer,indexed-export}.lean "$stage/"
cd "$library"
if [[ ! -f .lake/build/lib/lean/Mathlib/Basic/Finite/Prod.olean ]]; then
  lake exe cache get Mathlib/Basic/Finite/Prod.lean
fi
lake env bash -euc '
  cd "$1"
  export LEAN_PATH="$PWD:$LEAN_PATH"
  for name in OAI/Computability/IntegerMultiplication/TMModel compiler-controller compiler-indexed-transfer; do
    lean -DwarningAsError=true -o "$name.olean" "$name.lean"
  done
  lean -DwarningAsError=true --run compiler-indexed-export.lean > "$1/rule"
' bash "$stage"
python3 -I -B "$session_dir/compiler-indexed-transfer.py" --table "$stage/rule"
