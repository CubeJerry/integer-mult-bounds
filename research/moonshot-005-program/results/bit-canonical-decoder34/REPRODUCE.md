# Reproduction

Run from the repository root with Python3 and SymPy. Use disposable output paths; keep frozen evidence unchanged. Dependency and publication manifests pin inputs and outputs.

```bash
MOONSHOT_CHECK_OUT=/tmp/moonshot-s017-cp5
mkdir -p "$MOONSHOT_CHECK_OUT"
python research/moonshot-005-program/results/bit-canonical-decoder34/author/build.py --repo . --base research/moonshot-005-program/results/bit-canonical-common-delivery/author/canonical-common-one/WORD.json --engine research/moonshot-005-program/results/bit-leaf-capacity-quotient/author/check.py --price-engine research/moonshot-005-program/results/bit-cyclic-import-source/independent-review/check.py --out $MOONSHOT_CHECK_OUT/decoder34
python research/moonshot-005-program/results/bit-canonical-decoder34/root-review/check.py --repo . --base research/moonshot-005-program/results/bit-canonical-common-delivery/author/canonical-common-one/WORD.json --word research/moonshot-005-program/results/bit-canonical-decoder34/author/WORD.json --author-result research/moonshot-005-program/results/bit-canonical-decoder34/author/RESULT.json --out $MOONSHOT_CHECK_OUT/decoder-review.json
python research/moonshot-005-program/results/bit-canonical-decoder34/author/check_closure.py --repo . --word research/moonshot-005-program/results/bit-canonical-decoder34/author/WORD.json --engine research/moonshot-005-program/results/bit-leaf-capacity-quotient/author/check.py --price-engine research/moonshot-005-program/results/bit-cyclic-import-source/independent-review/check.py --out $MOONSHOT_CHECK_OUT/closure-author
python research/moonshot-005-program/results/bit-canonical-decoder34/root-review/check_closure.py --repo . --word research/moonshot-005-program/results/bit-canonical-decoder34/author/WORD.json --author-result research/moonshot-005-program/results/bit-canonical-decoder34/author/CLOSURE.json --out $MOONSHOT_CHECK_OUT/closure-review.json
```

All14 commands pass and19 output artifacts reproduce byte-for-byte across the four packages. The author uses its original decimal32 price engine where applicable; independent reviews use separate narrower enclosures. No frozen numerical report was altered to match another rounding convention. Source-transport author reproduction preserves the original helper bytes and only parameterizes repository access in its driver. Author reruns establish reproduction, not another independent review. See session CHECKPOINT5-VALIDATION.json and CHECKPOINT5-REPRODUCTION.json.
