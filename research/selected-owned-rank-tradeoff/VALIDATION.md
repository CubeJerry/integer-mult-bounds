# Validation status

Primary normal and optimized replays passed under CPython 3.12.14, Linux
x86_64, standard library. The complete authenticated 71,261-event source
scan found 23 nonzero owned entrance rows with supports 79–314 and rank
histogram `{1:10,2:4,3:1,4:6,5:1,6:1}`. Exact integer 200th-power comparisons
certify every target moment enclosure. Finite algebraic controls cover 2,184
rank/work triples and 5,460 exact Gaussian entries.

An independent model-assisted review derived the sparse-row bound, scanned
all 23 source rows by reverse-prefix adjoints, and checked the target budget
using a separate exact-root implementation. It passed with the explicit
single-data-input, inherited Gaussian normal-form and full-pass tariff scope
in PROOF.md. See review/REVIEW.md and review/REVIEWED-FILES.json.
No full selected cold replay, native phase catalogue, compiler
materialization, Lean or human review was run for this scoped result.

The initial discovery scan computed all complete rows. The delivered verifier
recomputes those source expressions with explicit frame/domain checks and
equality-checks saved row hashes. Both were written by the construction worker
and are not called independent review. The separate reverse-source audit
checks the actual nonzero pivots and full support sizes without importing
the author's verifier.

All three packaged commands below completed successfully in normal and
optimized (-O) Python modes. Each pair produced identical output, preserved
in review/PACKAGED-*.txt. The source paths were supplied explicitly during
the targeted-export run; defaults resolve to the same pinned files in a
canonical checkout.

```sh
python3 -I -B research/selected-owned-rank-tradeoff/verify.py
python3 -I -B research/selected-owned-rank-tradeoff/independent.py
python3 -I -B research/selected-owned-rank-tradeoff/independent_budget.py
```

Expected markers: PASS_SELECTED_OWNED_RANK_TRADEOFF,
PASS_INDEPENDENT_REVERSE_OWNED_AUDIT, PASS_INDEPENDENT_OWNED_BUDGET.
The independent finite checks contain 518 projection cases and 3,290
integer rank/work inequalities, plus rejected pivot, rank and frame mutations.
