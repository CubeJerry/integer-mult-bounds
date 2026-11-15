# Reproduction

Use Python3 with SymPy. Run from a scratch copy of this package; retain the
repository at its reviewed source pins. Preserve required sibling package paths
or replace them by their absolute paths in that repository. Replace REPO with its absolute root
and OUT with a separate existing output directory. Some frozen scripts write
sibling receipts, so do not run those against the committed scientific tree.

```sh
python3 -B author/run.py --repo REPO --out OUT/author
python3 -B independent-c/check.py --repo REPO --word author/output/CLOSED-WORD.json --out OUT/closed
python3 -B independent-c/check.py --repo REPO --word author/output/WORD.json --out OUT/live
```

Expected PASS statuses and exact source/result hashes are in the frozen
receipts and manifest. The checkpoint ledger records separate mathematical
review, negative controls and exact reproduction comparisons. An author
rerun is not independent proof verification. No new κ.
