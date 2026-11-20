#!/bin/sh
set -eu
repo=$(cd "$1" && pwd)
out=$2
here=$(cd "$(dirname "$0")" && pwd)
r="$repo/research/moonshot-005-program/results"
h="$r/bit-spread-rs-physical-word/author"
m="$r/bit-native-complete-middle-charts/author"
d="$r/bit-minimum-cache-d-atlas/author/output"
k="$r/bit-gf64-actual-k-atlas/author/output"
f="$r/bit-minimum-terminal-storage/author/output"
w="$r/bit-global-native-rank-rigidity/author/output/WITNESS.json.gz"
can="$r/bit-native-rs-return-distance/stream"
replay="$r/bit-physical-terminal-quotient/author"
mkdir -p "$out/author" "$out/review"
cc -O3 -march=native -shared -fPIC "$h/gf64_matmul.c" -o "$out/ops.so"
cc -O3 -march=native -shared -fPIC "$here/author/rank.c" -o "$out/rank.so"
cc -O3 -march=native -shared -fPIC "$can/stream.c" -o "$out/stream.so"
python -B "$here/author/check.py" --repo "$repo" --h-author "$h" --isolated-author "$r/bit-spread-isolated-middle-cut/author" --right-author "$r/bit-native-right-cut-partitions/author" --k "$k" --f "$f" --d-charts "$d/CHARTS.json.gz" --weighted "$w" --library "$out/ops.so" --fast-author "$m" --inverse-library "$out/rank.so" --out "$out/author"
python -B "$here/author/prefix.py" --repo "$repo" --h-author "$h" --k "$k" --d-charts "$d/CHARTS.json.gz" --weighted "$w" --library "$out/ops.so" --fast-author "$m" --inverse-library "$out/rank.so" --out "$out/author"
python -B "$here/review/check.py" --repo "$repo" --canonical "$can" --replay "$replay" --h-words "$h/output" --d-words "$d" --k-words "$k" --f-words "$f" --stream-lib "$out/stream.so" --author "$out/author" --out "$out/review"
if [ -e "$here/author/output/CHARTS.json.gz" ]; then
    python -B "$here/author/charts.py" --repo "$repo" --h-author "$h" --k "$k" --d-charts "$d/CHARTS.json.gz" --weighted "$w" --library "$out/ops.so" --fast-author "$m" --rank-library "$out/rank.so" --charts "$here/author/output/CHARTS.json.gz"
    python -B "$here/author/count.py" "$here/author/output/CHARTS.json.gz" "$here/author/output/COUNT.json"
fi
if [ -e "$here/author/output/PAIRS.json.gz" ]; then
    python -B "$here/author/charts.py" --repo "$repo" --h-author "$h" --k "$k" --d-charts "$d/CHARTS.json.gz" --weighted "$w" --library "$out/ops.so" --fast-author "$m" --rank-library "$out/rank.so" --charts "$here/author/output/PAIRS.json.gz"
    python -B "$here/author/paircover.py" --repo "$repo" --pairs "$here/author/output/PAIRS.json.gz" --out "$out/author/PAIR-RESULT.json"
fi
