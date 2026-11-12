# Fresh source-cohort reconstruction

Read PROOF.md, RECOVERY-COMPARISON.json and MANIFEST.json. This is fresh S008
code, not byte recovery of missing S007 generators. The accompanying worker-c
review independently checks the eight word; smaller variants have fresh author
validation and matching frozen receipts.

From this directory, set REPO to the repository root and OUT to a new directory:

```sh
python -B build.py --repo "$REPO" --output "$OUT" --variant all
python -B check_charts.py --repo "$REPO" --output "$OUT" --variant all
python -B full_replay.py --repo "$REPO" --output "$OUT" --variant eight
```

Expected instruction counts:74856,74943,75085,76277; raw MOVE counts:
455,485,508,559. Running the builder under `python -B -O` reproduces identical
word bytes in the tested environment. Exact chart engines require normal
assertions. Check payload equality across differing compression environments.

All source and engine inputs are pinned and unchanged. No new κ; eight leaves
4601 forward residual coefficients and all reverse duties. The paired-cohort
package is a distinct partial extension with its own complete invoice.
