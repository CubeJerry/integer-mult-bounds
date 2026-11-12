# Park original dual inputs and activate paid zero slots at actual source charts

Read PROOF.md and the separate one/eight RESULT, AUDIT and CHART-MAPS receipts.
The one variant extends the S009 orthogonal-frame-feedback source word and
preserves its public state while exposing a genuine short-activated observation.
The eight variant extends the paired-eight word and completes eight actual
individual hosted reverse outputs, preserving all other parent corrections.
Both are partial source constructions. **No new κ.**

Set REPO to the repository root, REC to the cohort-reconstruction directory,
FRAME to the pinned S009 orthogonal-frame-feedback WORD.json.gz, PAIRED to the
pinned paired-cohort WORD.json.gz, and OUT to a new output directory. Run once
with VARIANT=one and once with VARIANT=eight, choosing PARENT accordingly:

```sh
python -B build.py --repo "$REPO" --reconstruction "$REC" --frame-parent "$FRAME" --paired-parent "$PAIRED" --variant "$VARIANT" --output "$OUT"
python -B audit.py --repo "$REPO" --reconstruction "$REC" --output "$OUT"
python -B check_charts.py --repo "$REPO" --reconstruction "$REC" --parent "$PARENT" --output "$OUT"
```

Expected one:78,126 operations, one actual owned ghost, no changed final
public rows, reverse residual rank88, margin/native37.48775605591529.
Expected eight:77,851 operations, eight actual owned ghosts, eight newly
completed hosted reverse outputs, residual rank88, margin17.358506460845017.
Both retain peak43, all1880 independent inputs, every common output, all
original first-donor values before E8 reads, and all eight rank9 packet costs.

For optimization robustness, run build.py and audit.py again using `python -O`;
the frozen WORD, RESULT and AUDIT bytes are identical. The retained chart
engines must run with assertions enabled. The phase mutant must reject.

Full parent/source pins and exact ghost input rows are in each actual word.
Its `parked_dual_ghosts.observation_boundary` is an honest current-row boundary,
not a fictitious free observation. The full public correction table is
`hosted_reverse_output_corrections`. Inherited event tables and correction
tables with `parent_..._provenance` names describe ancestors only.

Prepared for @CubeJerry with substantial OpenAI assistance, preserving E8,
native, cohort and S009 predecessor attribution. The global code, source cut
capacity, full residual delivery, supplier interfaces and all foundational
assumptions remain unresolved beyond the exact finite claims above.
