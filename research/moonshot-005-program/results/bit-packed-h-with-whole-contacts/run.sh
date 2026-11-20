#!/bin/sh
set -eu
repo=$(cd "$1" && pwd)
out=$2
r="$repo/research/moonshot-005-program/results"
here=$(cd "$(dirname "$0")" && pwd)
h="$r/bit-spread-rs-physical-word/author"
mid="$r/bit-native-complete-middle-charts/author"
k="$r/bit-gf64-actual-k-atlas/author/output"
d="$r/bit-minimum-cache-d-atlas/author/output"
old="$r/bit-spread-packed-h-facet-fibres/author"
f="$r/bit-minimum-terminal-storage/author/output"
can="$r/bit-native-rs-return-distance/stream"
raw="$r/bit-physical-terminal-quotient/author"
mkdir -p "$out/author" "$out/review"
cc -O3 -march=native -fPIC -shared "$h/gf64_matmul.c" -o "$out/ops.so"
cc -O3 -march=native -fPIC -shared "$mid/invert.c" -o "$out/inv.so"
cc -O3 -march=native -fPIC -shared "$can/stream.c" -o "$out/stream.so"
python -B "$here/author/check.py" --repo "$repo" --h-author "$h" --middle-author "$mid" --k-words "$k" --d-charts "$d/CHARTS.json.gz" --library "$out/ops.so" --inv-lib "$out/inv.so" --packed-endpoint "$old" --compiler "$r/bit-spread-source-owner-compiler/author/compile_source.py" --assignment "$here/author/output/BEST.json" --baseline-source "$r/bit-spread-packed-source-owner-compiler/author/output-31/RESULT.json" --packing-review "$r/bit-spread-overlap-source/review/check.py" --field-review "$r/bit-spread-h263-source/review/check.py" --parameters "$r/bit-spread-two-centre-packing/author/output/PARAMETERS.json" --out "$out/author" --matrices "$out/GAUGES.npz"
python -B "$here/review/check.py" --repo "$repo" --engine "$can" --forward "$raw" --h-words "$h/output" --d-words "$d" --k-words "$k" --f-words "$f" --stream "$out/stream.so" --gauges "$out/GAUGES.npz" --assignment "$here/author/output/BEST.json" --out "$out/review"
