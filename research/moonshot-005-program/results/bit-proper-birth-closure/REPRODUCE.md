# Reproduction

Run from the repository root with Python 3 and SymPy. The output directory below is disposable; choose another task-specific path if needed. Frozen input and result hashes are in PUBLICATION-MANIFEST.json and DEPENDENCIES.json.

```bash
MOONSHOT_CHECK_OUT=/tmp/moonshot-s017-cp3
mkdir -p "$MOONSHOT_CHECK_OUT"
python research/moonshot-005-program/results/bit-proper-birth-closure/review/check.py --repo . --word research/moonshot-005-program/results/bit-proper-birth-reduction/author/proper-birth41/WORD.json --engine research/moonshot-005-program/results/bit-leaf-capacity-quotient/author/check.py --out $MOONSHOT_CHECK_OUT/fresh-closure
```

All listed commands pass. The author/reviewer reports, words, invoices and histories reproduced in this checkpoint match 17 frozen JSON artifacts byte-for-byte across the four packages. See the session validation and reproduction ledgers for exact comparisons. Repeated author execution is reproduction, not an independent proof.
