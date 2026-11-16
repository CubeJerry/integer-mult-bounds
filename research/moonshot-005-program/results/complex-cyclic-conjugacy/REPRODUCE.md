# Reproduction

Run from the repository root with Python 3 and SymPy. The output directory below is disposable; choose another task-specific path if needed. Frozen input and result hashes are in PUBLICATION-MANIFEST.json and DEPENDENCIES.json.

```bash
MOONSHOT_CHECK_OUT=/tmp/moonshot-s017-cp3
mkdir -p "$MOONSHOT_CHECK_OUT"
mkdir -p "$MOONSHOT_CHECK_OUT/complex-author"
cp research/moonshot-005-program/results/complex-cyclic-conjugacy/author/check_cyclic_quarter.py "$MOONSHOT_CHECK_OUT/complex-author/"
cp research/moonshot-005-program/results/complex-cyclic-conjugacy/author/check_cyclic_conjugacy.py "$MOONSHOT_CHECK_OUT/complex-author/"
python $MOONSHOT_CHECK_OUT/complex-author/check_cyclic_quarter.py
python $MOONSHOT_CHECK_OUT/complex-author/check_cyclic_conjugacy.py
python research/moonshot-005-program/results/complex-cyclic-conjugacy/root-unit-review/check.py --author-result research/moonshot-005-program/results/complex-cyclic-conjugacy/author/CYCLIC-RESULT.json --proof research/moonshot-005-program/results/complex-cyclic-conjugacy/author/CYCLIC-QUARTER-INTERFACE.md --out $MOONSHOT_CHECK_OUT/cyclic-unit-root.json
python research/moonshot-005-program/results/complex-cyclic-conjugacy/root-conjugacy-review/check.py --author-result research/moonshot-005-program/results/complex-cyclic-conjugacy/author/CONJUGACY-RESULT.json --proof research/moonshot-005-program/results/complex-cyclic-conjugacy/author/CYCLIC-CONJUGACY.md --out $MOONSHOT_CHECK_OUT/cyclic-conjugacy-root.json
```

All listed commands pass. The author/reviewer reports, words, invoices and histories reproduced in this checkpoint match 17 frozen JSON artifacts byte-for-byte across the four packages. See the session validation and reproduction ledgers for exact comparisons. Repeated author execution is reproduction, not an independent proof.
