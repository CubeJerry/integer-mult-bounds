# Independent review of the demand-only encoded prefix

**Accepted as an exact finite typed prefix, with the weaker stated contract.**
No complete native, supplier or new κ follows. The retained input information
is physical; current cochart access to deferred helper values is not granted.

The reviewer wrote `review_demand_prefix.py` independently of the construction
and author verifier. It imports no author module and replays all physical
instructions over 1,880 independent rational input columns. It separately
replays the pinned first-copy source prefix, authenticates all frames and the
source SHA, and checks every first-copy instruction remains in literal source
order. The script uses primitive integer, maximum-pivot row reduction for the
missing-helper check, rather than the author's minimum-pivot rational basis.

## Accepted invariants and operation bill

At cut 25,897, the 26,346-instruction physical transcript has exactly 24,860
ADD, 1,380 SCALE, 95 MOVE and 11 INIT instructions. Every scalar operand is
currently live in the declared chart. Every public MOVE is strictly ascending,
every owned MOVE has comparable distinct frames, and its actual ownership flag
matches the physical holder's type. All source COPY-zero conditions are checked
as identities on every formal input.

The verifier checks seven funded second-main MOVEs against their source
itineraries **and their actual current virtual-difference payloads**. It checks
all 400 final current-main difference decoders using current physical holders.
Four additional owned MOVEs each have rank one. Thus the new paid Gaussian
moment is exactly four; the scalar and storage costs remain positive expenses
for any complete invoice. There are 11 owned lifetimes, 11 simultaneously live
owners and no retirement in this prefix.

All 400 entering input differences remain in explicit physical holders at their
original charts. The first-copy source prefix has no INIT/CLEAR and only
nonzero SCALE and invertible scalar additions, so it retains all 1,480 entering
first-copy inputs. Together these facts prove retention of all 1,880 independent
entering arrays, not merely retention of a finite collection of sampled values.
This does not give free future movement, rereading or recomputation.

The dependency-closure proof is sound for this declared horizon. Each kept
arrival has earlier cochart parents whose physical holders survive, and the
literal main departure snapshots preserve old carrier versions. Omitting
unmarked arrivals is justified by absence from this horizon's dependency
closure, not by a claim that those virtual fields vanish or never matter again.

## A deliberately missing current helper

The reviewer independently derives, at chart 381,

    Δ332 = (−q33 + q108 + q109)/2.

It is outside the span of current difference observations there. The stronger
check also places it outside the span of **all** current physical destination
rows, including the exact common first-copy fields. Adding the target row as a
permitted observation makes the span test succeed, a positive control against a
vacuous rejection. Original q33 and q109 remain physically stored elsewhere.
The packet therefore genuinely changes the all-live-helper interface; it does
not satisfy that earlier contract accidentally or by an uncharged oracle.

## Verification controls and scope

The independent verifier rejects three transcript mutations without relying on
an author checksum: a new owned MOVE marked public, a corrupted actual main
MOVE payload, and a false retained-input holder. Both ordinary and `python -O`
execution produce identical receipts. The checked author files and imported
author replay dependency are bound in `DEMAND-PREFIX-REVIEWED-FILES.json`.

The reported full-horizon fixed-graph profile has 2,879 auxiliary arrivals.
The reviewer audited the graph recurrence, causal cochart parent checks and
backward root closure, but did not independently construct a complete physical
word for that losing policy. The profile remains a source-bound computational
result of the author graph algorithm, not a global lower bound. Its positive
rank count already exceeds the unchanged allowance below 98.399076951.

The prefix still requires a continuation construction, final difference/output
recovery, owned cleanup, positive scalar/precision/tape tariffs and a complete
recursive invoice. All original foundational assumptions remain. Neither this
review nor the favourable four-route prefix establishes a new complete κ.

## Reproduction

From the directory containing this independent reviewer, substitute the actual
source and packet paths:

```sh
python -B review_demand_prefix.py --source SOURCE --transcript ../demand-prefix.json.gz --author-receipt ../DEMAND-PREFIX-RESULT.json --output DEMAND-PREFIX-REVIEW.json
python -O -B review_demand_prefix.py --source SOURCE --transcript ../demand-prefix.json.gz --author-receipt ../DEMAND-PREFIX-RESULT.json --output DEMAND-PREFIX-REVIEW-OPTIMIZED.json
```

Expected status: `PASS_INDEPENDENT_TYPED_MAIN_DEMAND_AND_RETAINED_INPUT_PREFIX`;
400 main decoders, 400 retained inputs, seven main departure payloads, four
rank-one added MOVEs, and three rejected mutations. Prepared for @CubeJerry by
a separate OpenAI research worker, with substantial AI assistance.
