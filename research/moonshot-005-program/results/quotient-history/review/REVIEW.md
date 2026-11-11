# Independent14-return quotient and history review

**Accepted within the stated source-linear scope. No new kappa.**
Programme lead, S003,2026-11-11. REVIEWED-FILES.json pins8 author files.
Implementations are separate; no author code is imported by the reviewer.

reverse_review.py computes each14 pre-MOVE row by BACKWARD ADJOINT through the
literal source, rather than the author's forward rational replay. It reproduces
the complete400-input rows, quotient rank10, historical rank4,101 historical
distributed inputs, and entry-only targets33272/33281. Its separate10x10 minor
has determinant51/64, using events28141,28169,33554,34467,34479,37597,37606,39217,
40094,41758 and input columns111,42,110,109,82,106,98,102,97,103. Deleting its final
row destroys the determinant. Normal/-O records agree.

history_review.py compares all14 full target rows, independently reverses26
distinct positive historical observations, and verifies all23 positive identities
across the owned and owned/main cases. It checks strict observation phases,
actual canonical spans, lifetimes, value versions and last-MOVE metadata by
separate literal metadata replay.

At the decisive event37606, a separate scalar source execution sets q0=q20=1,
all other q=0. EVERY earlier main/owned destination observation iszero. The
review independently enumerates all10 distinct nonzero historical rows using
reverse adjoints, and the target is4. This proves the dual counterexample even
with unlimited retained earlier rows and all entry inputs. The13 positive
closures and one excluded target have independent evidence. The author's finer
classification of three owned/main-only and ten owned/entry cases is also
supported by exact certificates and reviewed elimination code; the independent
executable focuses on positive closures and the decisive full-history exclusion.

All three owned provenance records are independently reconstructed, including
in-place role1502 with NO MOVE in its lifetime. Exact200th powers verify the
rank3/rank4 price enclosures; rank4's lower price exceeds the hash-pinned
predecessor budget's upper headroom. The inherited upper bound is checked
exactly against the precursor BUDGET.json, not accepted as an unbound number.

## Mathematical audit and limitations

Elimination of all14 independently reproduced rows supplies the upper rank;
the nonzero minor supplies the lower rank over any characteristic-zero field.
Tensoring with the admitted array dimension gives the all-V statement. The
psi counterexample also excludes arbitrary decoders of those indistinguishable
observations. Historical snapshots and entry forms still require acquisition,
retention, precision, control and erasure. Rank10 is an abstract mode count,
not paid arrivals, peakowned fields or physical observers. A helper observation
is a scoped escape, not an implemented shared code. No uniform supplier,
complete tariff, compiler or unconditional theorem follows from finite rows.

## Reproduction from repository root

```sh
P=research/moonshot-005-program/results
Q=$P/quotient-history
python3 -B $Q/review/reverse_review.py --source research/shared-wire-split-composition/data/final.json.gz --current $P/owned-difference-delivery/CERTIFICATE.json --historical $P/historical-owned/WITNESSES.json --output /tmp/quotient-review.json --rows /tmp/quotient-rows.json
python3 -B $Q/review/history_review.py --source research/shared-wire-split-composition/data/final.json.gz --packet $Q --reverse-rows /tmp/quotient-rows.json --budget $P/prepaid-historical-budget/BUDGET.json --output /tmp/history-review.json
```

Expected PASS_INDEPENDENT_ADJOINT_QUOTIENT and
PASS_INDEPENDENT_HISTORY_ADJOINT_AND_DUAL. Repeat with-O; receipts agree.
Review by programme lead with OpenAI assistance, independently of workerB.
