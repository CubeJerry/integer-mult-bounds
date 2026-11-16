# Reproduction

Run from the repository root with Python3 and SymPy. Use disposable output paths; keep frozen evidence unchanged. Dependency and publication manifests pin inputs and outputs.

```bash
MOONSHOT_CHECK_OUT=/tmp/moonshot-s017-cp5
mkdir -p "$MOONSHOT_CHECK_OUT"
mkdir -p "$MOONSHOT_CHECK_OUT/complex-author"
cp research/moonshot-005-program/results/complex-source-transport/author/* "$MOONSHOT_CHECK_OUT/complex-author/"
python $MOONSHOT_CHECK_OUT/complex-author/check_source_transport.py --repo .
python research/moonshot-005-program/results/complex-source-transport/root-review/source-transport/check.py --repo . --proof research/moonshot-005-program/results/complex-source-transport/author/SOURCE-TRANSPORTED-ROUTING.md --author-result research/moonshot-005-program/results/complex-source-transport/author/SOURCE-TRANSPORT-RESULT.json --out $MOONSHOT_CHECK_OUT/transport-review.json
python $MOONSHOT_CHECK_OUT/complex-author/check_coherent_pivot.py
python research/moonshot-005-program/results/complex-source-transport/root-review/coherent-pivot/check.py --proof research/moonshot-005-program/results/complex-source-transport/author/COHERENT-FIRST-PIVOT.md --support-proof research/moonshot-005-program/results/complex-source-transport/author/SOURCE-TRANSPORTED-ROUTING.md --support-review research/moonshot-005-program/results/complex-source-transport/root-review/source-transport/RESULT.json --author-result research/moonshot-005-program/results/complex-source-transport/author/COHERENT-PIVOT-RESULT.json --out $MOONSHOT_CHECK_OUT/coherent-review.json
```

All14 commands pass and19 output artifacts reproduce byte-for-byte across the four packages. The author uses its original decimal32 price engine where applicable; independent reviews use separate narrower enclosures. No frozen numerical report was altered to match another rounding convention. Source-transport author reproduction preserves the original helper bytes and only parameterizes repository access in its driver. Author reruns establish reproduction, not another independent review. See session CHECKPOINT5-VALIDATION.json and CHECKPOINT5-REPRODUCTION.json.
