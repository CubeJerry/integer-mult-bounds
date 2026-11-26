#!/usr/bin/env bash
# Replay an independent wrapper against the pinned public word under Lean 4.34.1.
# Run: LEAN=path/to/lean LEANCHECKER=path/to/leanchecker bash check-fourier-word.sh /path/to/mobius-x1
set -euo pipefail
source_root=${1:?Pass a checkout of https://github.com/Swapnil-jain/mobius-x1}
script_dir=$(cd -- "$(dirname -- "$0")" && pwd)
word_path=lean/MobiusLean/Word.lean
commit=00ffede3d650d434ebba869cafab4d334edc6d4d
lean_bin=${LEAN:-lean}
checker_bin=${LEANCHECKER:-leanchecker}
# leanchecker invokes a sibling lean process by name.
lean_path=$(command -v -- "$lean_bin")
export PATH="$(dirname -- "$lean_path"):$PATH"
case "$($lean_bin --version)" in *'version 4.34.1,'*) ;; *) echo 'Requires Lean 4.34.1' >&2; exit 2;; esac
stage=$(mktemp -d)
trap 'rm -rf -- "$stage"' EXIT
mkdir -p -- "$stage/MobiusLean"
# git show selects the committed source even if the supplied checkout is dirty.
git -C "$source_root" show "$commit:$word_path" > "$stage/MobiusLean/Word.lean"
cp -- "$script_dir/mobius-lean/FourierShearWord.lean" "$stage/FourierShearWord.lean"
cd -- "$stage"
export LEAN_PATH="$stage${LEAN_PATH:+:$LEAN_PATH}"
"$lean_bin" -DwarningAsError=true -o MobiusLean/Word.olean MobiusLean/Word.lean
"$lean_bin" -DwarningAsError=true -o FourierShearWord.olean FourierShearWord.lean
"$checker_bin" -v --fresh FourierShearWord
