# Actual source spans and the remaining-point quotient at 46 outputs

## Compared words

All three words complete the same 46 original outputs and restore every
original X record. Each is independently replayed from 222 formal columns.

| Word | SHA256 | Movement moment, approximate |
|---|---|---:|
| Five paid returns on protected41 | `a0f0e1b5aa027d9f8faea8a529f47b5757f438f8609e1819af5e2a0f4da3b8fc` | 1612.12264342029803 |
| Original source-wide coded46 | `45479de20faad9d9cd4ace9493057b82fb2c8b6f8baa4ac67134571f2e5cca84` | 1620.46505367233252 |
| Root's protected reduction of coded46 | `de4e5799da70814323cbe233e118c6bb26cbf3ac537bf77d4669db3304f9e460` | 1616.35386920121172 |

The paid-return word saves approximately 8.34241025203449 movement units against
the original coded word and 4.23122578091369 against its protected reduction.
The point-count and movement comparison does not imply literal source-space
containment. The following checks distinguish those claims.

## Literal actual source and common stocks

Rows are recorded only at their actual chronological charts. M1 stock is taken
immediately before the actual `ADD CAP46 P3`; M0 stock is taken immediately
before P7's birth; final retained stock is taken before the first CLEAR.
These are specified snapshots, not grants that a record can be moved upward
or read at an earlier time.

In the table, left denotes paid raw46 and right denotes the indicated coded
word. Union rank is computed in the same 111-dimensional original-X space.

| Actual stock | Raw rank | Original coded rank | Union rank | Relation |
|---|---:|---:|---:|---|
| Ground common rows | 25 | 19 | 28 | Incomparable |
| M1 source rows | 11 | 8 | 11 | Coded stock is contained in raw stock |
| M0 source rows | 5 | 9 | 12 | Incomparable |

For root's reduced coded46, the ground rank is 20 and the union rank remains
28. Its M1 and M0 ranks and inclusion relations are the same as those above.

The raw word retains three M1 directions that the coded word consumed and
repositioned. The coded word has three common directions absent from the raw
common span; the raw word has nine directions absent from the original coded
common span, or eight absent from the reduced coded common span. Accordingly,
neither actual common stock contains the other. The report includes explicit
row witnesses and all per-facet literal-current-stock comparisons.

These facts prevent an invalid claim that the cheaper word literally retains
every coded source contract. It does not. It also prevents interpreting the
rank-nine coded M0 stock as a free replacement for the raw word's actual M1
imports: those records are at different charts.

## Exact equality in the explicitly optimistic remaining-point quotient

Let K be the 46 completed indices. For this diagnostic only, grant every raw
direction `X_k`, `k∈K`, freely everywhere. Equivalently, project every row onto
the 65 unresolved input coordinates. At each receiver i, also grant

1. the X component of every actual record history whose chart is contained in
   `F_i`, including the X component of an original Y record; and
2. every geometric raw local `X_j` with native root j orthogonal to root i.

This is intentionally more permissive than actual custody or a chronological
decoder. It cannot turn arbitrary original Y data into a free raw input in an
actual word; the grant is solely a necessary information-envelope calculation.

**For every one of the 111 receivers, the resulting projected row spaces are
exactly equal for all three compared words.** Both inclusions are checked by
exact binary row reduction. Neither coded word gains a direction on the
unresolved coordinates that the paid-return word lacks, and vice versa.

All three feedback closures stop at exactly 46. Starting with all 46 completed
point directions globally granted, no new unresolved target lies in its
receiver's projected span. Each word has 65 explicit separating duals, one
for each unresolved receiver. Every dual evaluates to one on the missing
target and to zero on every granted projected measurement. Thus even free
decoded-point feedback cannot start a further wave inside this fixed envelope.

The equality explains why the cheaper source is a suitable next cost base
for new work without claiming literal source-contract domination. The coded
construction changes where and how already completed directions are stored;
in this audit it does not improve the remaining-point quotient.

## Control and scope

An extra unresolved native direction is artificially added to one receiver's
common measurement space. The comparison detects a new direction and rejects
containment. This is a control that a source change involving an unresolved
coordinate would invalidate the equality.

The report checks all actual word endpoints, source hashes, chart geometry,
retained values and prices before comparing spans. The span and dual claims
are finite exact binary certificates. Geometric visibility ignores nested
receiver itineraries, and the completed-point quotient grants information
that has no automatic physical implementation. The certificate is therefore
not a complete supplier or an optimality theorem, and it proves no new kappa.

## Reproduction and open next questions

```sh
python3 -B workers/coded/compare_raw_coded46.py \
  --repo programme --raw workers/coded/paid-raw46/WORD.json \
  --coded workers/coded/encoded-lower-triples/outputs46/WORD.json \
          workers/root/protected-point46/WORD.json \
  --engine workers/audit/leaf-capacity-gate/check.py \
  --price-engine workers/audit/review36/check.py \
  --out workers/coded/paid-raw46-comparison
```

The next construction must alter a source, history, or common direction on
the unresolved coordinates. Further decoder fitting over these exact fixed
measurements cannot add an output. The reusable source-wide substitution
lemma remains available, but any use should be compared with fully paid raw
returns and the resulting actual source contracts before expanding it.

The input words retain root and programme attribution. Substantial AI
assistance was used in this finite comparison and documentation.
