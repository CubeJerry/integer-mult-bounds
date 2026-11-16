# Reproduction

Run from the repository root with Python3 and SymPy. Frozen scientific inputs and outputs are pinned by the dependency and publication manifests. Use a disposable output directory.

```bash
MOONSHOT_CHECK_OUT=/tmp/moonshot-s017-cp4
mkdir -p "$MOONSHOT_CHECK_OUT"
python research/moonshot-005-program/results/bit-protected-point-services/author/build.py --repo . --base research/moonshot-005-program/results/bit-native-raw2-return/author/import41/WORD.json --points 10 20 --protect IMPORT_E8 IMPORT_E9 IMPORT_E36 --out $MOONSHOT_CHECK_OUT/point41
python research/moonshot-005-program/results/bit-protected-point-services/author/build.py --repo . --base research/moonshot-005-program/results/bit-sourcewide-substitution/author/outputs46/WORD.json --points 10 --protect IMPORT_E8 IMPORT_E9 IMPORT_E36 --out $MOONSHOT_CHECK_OUT/protected-coded46
python research/moonshot-005-program/results/bit-protected-point-services/independent-review/check.py --repo . --base research/moonshot-005-program/results/bit-native-raw2-return/author/import41/WORD.json --word research/moonshot-005-program/results/bit-protected-point-services/author/point41/WORD.json --author-price research/moonshot-005-program/results/bit-protected-point-services/author/point41/PRICE.json --engine research/moonshot-005-program/results/bit-leaf-capacity-quotient/author/check.py --price-engine research/moonshot-005-program/results/bit-cyclic-import-source/independent-review/check.py --history-engine research/moonshot-005-program/results/bit-native-raw2-return/independent-review/check.py --out $MOONSHOT_CHECK_OUT/point41-review
```

All17 commands across six packages pass. Thirty-two output artifacts reproduce byte-for-byte. The remaining author source-comparison report is identical after rebasing exactly its three input-path metadata strings; all rows, ranks, source pins, prices and witnesses are unchanged. See the session CHECKPOINT4-VALIDATION.json and CHECKPOINT4-REPRODUCTION.json. Author reruns establish reproduction, not another independent proof.
