# Reproduction

Run from the repository root with Python3 and SymPy. Frozen scientific inputs and outputs are pinned by the dependency and publication manifests. Use a disposable output directory.

```bash
MOONSHOT_CHECK_OUT=/tmp/moonshot-s017-cp4
mkdir -p "$MOONSHOT_CHECK_OUT"
python research/moonshot-005-program/results/bit-sourcewide-substitution/author/build_extra42.py --repo . --base research/moonshot-005-program/results/bit-cyclic-import-source/author/WORD.json --engine research/moonshot-005-program/results/bit-leaf-capacity-quotient/author/check.py --price-engine research/moonshot-005-program/results/bit-common-terminal-reuse/independent-review/check.py --out $MOONSHOT_CHECK_OUT/extra42
python research/moonshot-005-program/results/bit-sourcewide-substitution/author/build_extra43.py --repo . --base research/moonshot-005-program/results/bit-sourcewide-substitution/author/extra42/WORD.json --engine research/moonshot-005-program/results/bit-leaf-capacity-quotient/author/check.py --price-engine research/moonshot-005-program/results/bit-common-terminal-reuse/independent-review/check.py --out $MOONSHOT_CHECK_OUT/extra43
python research/moonshot-005-program/results/bit-native-raw2-return/author/build.py --repo . --base research/moonshot-005-program/results/bit-sourcewide-substitution/author/extra43/WORD.json --out $MOONSHOT_CHECK_OUT/raw2-base43
python research/moonshot-005-program/results/bit-sourcewide-substitution/author/build_encoded_lower_triples.py --repo . --base research/moonshot-005-program/results/bit-sourcewide-substitution/author/raw2-base43/WORD.json --engine research/moonshot-005-program/results/bit-leaf-capacity-quotient/author/check.py --price-engine research/moonshot-005-program/results/bit-common-terminal-reuse/independent-review/check.py --stages 3 --out $MOONSHOT_CHECK_OUT/coded-chain
python research/moonshot-005-program/results/bit-sourcewide-substitution/root-review/check.py --repo . --base research/moonshot-005-program/results/bit-sourcewide-substitution/author/raw2-base43/WORD.json --stages research/moonshot-005-program/results/bit-sourcewide-substitution/author --out $MOONSHOT_CHECK_OUT/sourcewide-review.json
```

All17 commands across six packages pass. Thirty-two output artifacts reproduce byte-for-byte. The remaining author source-comparison report is identical after rebasing exactly its three input-path metadata strings; all rows, ranks, source pins, prices and witnesses are unchanged. See the session CHECKPOINT4-VALIDATION.json and CHECKPOINT4-REPRODUCTION.json. Author reruns establish reproduction, not another independent proof.
