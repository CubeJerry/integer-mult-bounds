# Reproduction

Run from the repository root with Python3 and SymPy. Use disposable output paths; keep frozen evidence unchanged. Dependency and publication manifests pin inputs and outputs.

```bash
MOONSHOT_CHECK_OUT=/tmp/moonshot-s017-cp5
mkdir -p "$MOONSHOT_CHECK_OUT"
python research/moonshot-005-program/results/bit-canonical-common-delivery/author/build_canonical_lowering.py --repo . --base research/moonshot-005-program/results/bit-canonical-mask-source/author/masked-M1/WORD.json --engine research/moonshot-005-program/results/bit-leaf-capacity-quotient/author/check.py --price-engine research/moonshot-005-program/results/bit-common-terminal-reuse/independent-review/check.py --out $MOONSHOT_CHECK_OUT/canonical-common-one --count 1
python research/moonshot-005-program/results/bit-canonical-common-delivery/author/build_canonical_lowering.py --repo . --base research/moonshot-005-program/results/bit-canonical-mask-source/author/masked-M1/WORD.json --engine research/moonshot-005-program/results/bit-leaf-capacity-quotient/author/check.py --price-engine research/moonshot-005-program/results/bit-common-terminal-reuse/independent-review/check.py --out $MOONSHOT_CHECK_OUT/canonical-common-two --count 2
python research/moonshot-005-program/results/bit-canonical-common-delivery/root-review/check.py --repo . --base research/moonshot-005-program/results/bit-canonical-mask-source/author/masked-M1/WORD.json --one research/moonshot-005-program/results/bit-canonical-common-delivery/author/canonical-common-one/WORD.json --two research/moonshot-005-program/results/bit-canonical-common-delivery/author/canonical-common-two/WORD.json --out $MOONSHOT_CHECK_OUT/lower-review.json
```

All14 commands pass and19 output artifacts reproduce byte-for-byte across the four packages. The author uses its original decimal32 price engine where applicable; independent reviews use separate narrower enclosures. No frozen numerical report was altered to match another rounding convention. Source-transport author reproduction preserves the original helper bytes and only parameterizes repository access in its driver. Author reruns establish reproduction, not another independent review. See session CHECKPOINT5-VALIDATION.json and CHECKPOINT5-REPRODUCTION.json.
