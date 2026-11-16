# Reproduction

Run from the repository root with Python3. Keep frozen evidence unchanged.

```bash
MOONSHOT_INVENTORY_OUT=/tmp/moonshot-inventory-correction
mkdir -p "$MOONSHOT_INVENTORY_OUT"
python research/moonshot-005-program/results/bit-semantic-chart-inventory/root-review/check.py --repo . --out $MOONSHOT_INVENTORY_OUT/root.json
python research/moonshot-005-program/results/bit-semantic-chart-inventory/corrected-review/check.py --repo . --early-word research/moonshot-005-program/results/bit-early-source-release/author/WORD.json --base research/moonshot-005-program/results/bit-canonical-mask-source/author/early-paid46/WORD.json --word research/moonshot-005-program/results/bit-canonical-mask-source/author/masked-M1/WORD.json --author-result research/moonshot-005-program/results/bit-canonical-mask-source/author/masked-M1/RESULT.json --engine research/moonshot-005-program/results/bit-leaf-capacity-quotient/author/check.py --price-engine research/moonshot-005-program/results/bit-cyclic-import-source/independent-review/check.py --out $MOONSHOT_INVENTORY_OUT/corrected
```

Both commands pass and both JSON results reproduce byte-for-byte. Root finds ranks[13,13,13,13,13] and intersections[0,3,3,3,3]. The corrected complete review retains all earlier source/price/control checks.
