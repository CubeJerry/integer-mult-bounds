# Reproduction

Run from the repository root with Python3 and SymPy. Frozen scientific inputs and outputs are pinned by the dependency and publication manifests. Use a disposable output directory.

```bash
MOONSHOT_CHECK_OUT=/tmp/moonshot-s017-cp4
mkdir -p "$MOONSHOT_CHECK_OUT"
mkdir -p "$MOONSHOT_CHECK_OUT/nondiagonal-author"
cp research/moonshot-005-program/results/complex-nondiagonal-cyclic/author/check_nondiagonal_cyclic.py "$MOONSHOT_CHECK_OUT/nondiagonal-author/"
cp research/moonshot-005-program/results/complex-nondiagonal-cyclic/author/check_cyclic_quarter.py "$MOONSHOT_CHECK_OUT/nondiagonal-author/"
python $MOONSHOT_CHECK_OUT/nondiagonal-author/check_nondiagonal_cyclic.py --repo .
python research/moonshot-005-program/results/complex-nondiagonal-cyclic/root-review/check.py --author-result research/moonshot-005-program/results/complex-nondiagonal-cyclic/author/NONDIAGONAL-RESULT.json --proof research/moonshot-005-program/results/complex-nondiagonal-cyclic/author/NONDIAGONAL-CYCLIC-IMPLEMENTATION.md --out $MOONSHOT_CHECK_OUT/nondiagonal-review.json
```

All17 commands across six packages pass. Thirty-two output artifacts reproduce byte-for-byte. The remaining author source-comparison report is identical after rebasing exactly its three input-path metadata strings; all rows, ranks, source pins, prices and witnesses are unchanged. See the session CHECKPOINT4-VALIDATION.json and CHECKPOINT4-REPRODUCTION.json. Author reruns establish reproduction, not another independent proof.
