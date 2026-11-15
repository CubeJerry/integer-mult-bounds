# Reproduction

Use Python3 and SymPy. Run from this package in a scratch copy; replace REPO
with the absolute pinned repository root and OUT with a separate output path.
The adjacent four-source package is required. Do not overwrite frozen receipts.

```sh
python3 -B six-axis/author/build.py --source ../bit-four-axis-feedback/author/output/WORD.json --out OUT/six-words
python3 -B six-axis/author/check.py --repo REPO --package six-axis/author --out OUT/six-check
python3 -B author/check.py --repo REPO --four ../bit-four-axis-feedback/author/output/WORD.json --six six-axis/author/output/WORD.json --out OUT/gate
python3 -B review-root/check.py --repo REPO --four ../bit-four-axis-feedback/author/output/WORD.json --six six-axis/author/output/WORD.json --certificate author/output/RESULT.json --out OUT/root.json
python3 -B review-root/check_six_source.py --repo REPO --word six-axis/author/output/CLOSED-WORD.json --out OUT/six-root.json
```

Expected PASS statuses and exact results are frozen beside the corresponding
scripts. The two root scripts are independent of author code; the six-source
root checker imports only the root's own geometric utilities. The proof is
uniform over fields/widths as stated, and these checks certify the actual
native stars and frozen source premises. No new κ.
