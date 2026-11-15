# Checkpoint5 certificate order qualification

Some independent A source reviewers construct their handoff dictionary from a
Python set of live owners. Their actual cache row order can therefore vary
between processes. Coefficient witnesses indexed by that order vary with it.
The frozen original receipts and hashes are retained unchanged.

The portable checkpoint runner distinguishes byte-identical reproduction from
basis-order-equivalent reproduction. For the latter it permits only the named
raw-cache row/witness ordering fields and the corresponding acquired-W witness.
It checks equality of the row/witness multiset, equality of every other receipt
field, and exactly recombines every raw/W coefficient witness against its own
declared history order. It independently checks the acquired relation against
the relevant raw row order. An unrelated difference or invalid witness fails.

This is not a relaxed mathematical gate or replacement of source pins. Original
word/proof/script hashes are still exact. Author constructions and all other
receipts are compared byte-for-byte. The two original comparison attempts
exposed this output-order behavior; the final portable run validates it explicitly.
One harness attempt also scheduled the separate structural receipt too late;
that sequencing was corrected. No mathematical source or theorem changed.

Reproduce from any checkout with the committed dependencies present:

```sh
python3 -B research/moonshot-005-program/sessions/2026-11-15-S015/reproduce-checkpoint5.py \
  --repo /absolute/path/to/checkout --out /absolute/path/to/new-reproduction
```

The final receipt records exact command counts, hashes, comparison kinds and
reindexed fields. Independent mathematical review remains separate from
reproduction of either author's or reviewer's code. No new κ.
