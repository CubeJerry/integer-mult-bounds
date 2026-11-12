# Hosted inverse-transpose cohort companion

Read PROOF.md, output/RESULT.json, output/AUDIT.json and MANIFEST.json.
The actual77795-word supplies352 transpose terms on88 hosted X2 values,
retains all eight forward completions and completes no reverse diagonal.
The actual reverse residual rank remains96. Independent review accompanies
the package; author checks alone are not called independent verification.

Set REPO to the repository root, REC to the cohort-reconstruction directory,
and OUT to a new output directory:

```sh
python -B build.py --repo "$REPO" --reconstruction "$REC" --output "$OUT"
python -B audit.py --repo "$REPO" --reconstruction "$REC" --output "$OUT"
python -B check_charts.py --repo "$REPO" --reconstruction "$REC" --output "$OUT"
```

Expected:77795 instructions,703 raw MOVEs, peak43, margin/native about
41.01712837582312. Four wrong-word mutants and the phase mutant reject.
The only new chart pairs versus the recovered eight parent are3→1105 and
1105→127. The normal/optimized builders produce identical word and result
bytes in the tested environment; chart engines require enabled assertions.

All local chart IDs refer to the pinned eight-cohort parent. No complete
native, supplier or new κ is claimed. Unpaid reuse of its spent routes is
outside the construction.
