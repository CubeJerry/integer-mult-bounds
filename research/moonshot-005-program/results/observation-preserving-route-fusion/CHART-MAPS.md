# Exact introduced chart maps

The source's retained Clifford compiler lowers all 206 chart maps introduced
by unit17 private-route fusion. A separately implemented retained engine checks
the signed Pauli action and exact global phase of each lowered recipe against
the original canonical frame expression C_destination C_source^{-1}. Every
recipe's recursive rank equals the declared positive frame-dimension difference.

These are exact operator-grammar identities using integer Gaussian-dyadic
arithmetic. They are stronger than checking a random vector, and they remove
the possibility that the fused frame pair needs a hidden phase or a different
rank. The wrong-global-phase negative control is rejected. The recipes and
both engine hashes are in CHART-MAPS.json; check_chart_maps.py rejects changed
engine bytes and requires assertions to remain enabled in the inherited compiler.

The two engines are reused from the authenticated source package, not authored
again for this result. This receipt is not represented as a new independent
implementation or as a proof of the source's unbounded-column physical lift.
The native-all-columns, compiler, scalar, layout and precision contracts remain.
The full finite source word and the conditional caller invoice are verified
separately. No complete multiplier or new kappa is claimed.

Reproduce from any directory:

```sh
python3 -B check_chart_maps.py \
  --repo /path/to/integer-mult-bounds \
  --parent /path/to/results/unit17-precompensation/WORD.json.gz \
  --word WORD.json.gz --output /tmp/fusion-chart-maps.json
```

Expected status: PASS_ALL_INTRODUCED_FUSION_CHART_MAPS, 206 introduced maps.
Do not run the inherited exact compiler with Python optimization flags.
