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
replay="$r/bit-physical-terminal-quotient/author"
mkdir -p "$out/program/output" "$out/review"
cp "$here/author/output/TERMINAL-RECEIPTS.json.gz" "$out/program/output/"
cc -O3 -march=native -shared -fPIC "$h/gf64_matmul.c" -o "$out/ops.so"
cc -O3 -march=native -shared -fPIC "$can/stream.c" -o "$out/stream.so"
c++ -O3 -march=native -shared -fPIC "$here/author/field24.cpp" -o "$out/packed.so"
c++ -O3 -march=native -shared -fPIC "$here/review/reciprocal.cpp" -o "$out/reciprocal.so"
for sec in small large; do
    python -B "$here/author/build.py" --repo "$repo" --transfer "$h" --k-words "$k" --d-charts "$d/CHARTS.json.gz" --mult "$out/ops.so" --packed "$out/packed.so" --sector "$sec" --out "$out/program/$sec"
    python -B "$here/review/action.py" --repo "$repo" --canonical "$can" --replay "$replay" --h-words "$h/output" --d-words "$d" --k-words "$k" --stream-lib "$out/stream.so" --program "$out/program" --out "$out/review" --sector "$sec"
    python -B "$here/review/foreign.py" --repo "$repo" --canonical "$can" --replay "$replay" --h-words "$h/output" --d-words "$d" --k-words "$k" --stream-lib "$out/stream.so" --program "$out/program" --lib "$out/reciprocal.so" --owner-dir "$out/review" --out "$out/review" --sector "$sec"
done
python -B "$here/author/price.py" --repo "$repo" --transfer "$h" --k-words "$k" --d-charts "$d/CHARTS.json.gz" --mult "$out/ops.so" --packed "$out/packed.so" --small "$out/program/small" --large "$out/program/large" --out "$out/program/output"
python -B "$here/review/price.py" --program "$out/program" --lib "$out/reciprocal.so" --out "$out/review"
