#!/bin/sh
set -eu
repo=$(cd "$1" && pwd)
out=$2
here=$(cd "$(dirname "$0")" && pwd)
r="$repo/research/moonshot-005-program/results"
h="$r/bit-spread-rs-physical-word/author"
k="$r/bit-gf64-actual-k-atlas/author/output"
d="$r/bit-minimum-cache-d-atlas/author/output"
can="$r/bit-native-rs-return-distance/stream"
raw="$r/bit-physical-terminal-quotient/author"
mkdir -p "$out/author" "$out/review"
cc -O3 -march=native -fPIC -shared "$h/gf64_matmul.c" -o "$out/ops.so"
cc -O3 -march=native -fPIC -shared "$here/author/field.c" -o "$out/arith.so"
cc -O3 -march=native -fPIC -shared "$can/stream.c" -o "$out/stream.so"
python -B "$here/author/check.py" --repo "$repo" --library "$out/ops.so" --arith "$out/arith.so" --out "$out/author" --emit
for sector in small large; do
    python -B "$here/review/forward.py" --repo "$repo" --canonical "$can" --replay "$raw" --h-words "$h/output" --d-words "$d" --k-words "$k" --stream-lib "$out/stream.so" --assign "$here/author/output/ASSIGNMENT.json" --matrices "$out/author/matrices" --sources "$out/author/matrices" --out "$out/review" --sector "$sector"
done
