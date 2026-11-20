#!/bin/sh
set -eu
repo=$(cd "$1" && pwd)
out=$2
here=$(cd "$(dirname "$0")" && pwd)/author
r="$repo/research/moonshot-005-program/results"
h="$r/bit-spread-rs-physical-word/author"
cut="$r/bit-spread-isolated-middle-cut/author"
comp="$r/bit-spread-source-owner-compiler/author/compile_source.py"
k="$r/bit-gf64-actual-k-atlas/author/output"
d="$r/bit-minimum-cache-d-atlas/author/output/CHARTS.json.gz"
s="$r/bit-spread-h263-source/author/output/COEFFICIENTS.json.gz"
mkdir -p "$out"
cc -O3 -march=native -shared -fPIC "$h/gf64_matmul.c" -o "$out/ops.so"
cc -O3 -march=native -shared -fPIC "$here/invert.c" -o "$out/invert.so"
python -B "$here/whole.py" --repo "$repo" --h-author "$h" --isolated-author "$cut" --k-words "$k" --d-charts "$d" --source "$s" --repair "$cut/output/WORDS.json.gz" --library "$out/ops.so" --inverse-library "$out/invert.so" --compiler "$comp" --out "$out"
python -B "$here/verify.py" --repo "$repo" --h-author "$h" --isolated-author "$cut" --k-words "$k" --d-charts "$d" --source "$s" --repair "$cut/output/WORDS.json.gz" --library "$out/ops.so" --inverse-library "$out/invert.so" --source-compiler "$comp" --cuts "$here/output/SELECTED-CUTS.json" --out "$out"
