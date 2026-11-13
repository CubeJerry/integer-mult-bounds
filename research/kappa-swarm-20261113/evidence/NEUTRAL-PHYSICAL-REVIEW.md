# Independent review: helper-1354 neutral zeroing

## Conclusion

The helper-zero specialization has an exact all-input **scalar** reduction.
Swap public helper IDs 1354 and 1500 everywhere, reduce public width from 1501
to 1500, keep the old owned IDs 1501–1568, and treat new owned ID 1500 as the
old helper 1354. Add `INIT 1500` at chart 252 before the source and
`CLEAR 1500` at chart 127 after it. Deleting the five scalar events below
preserves every remaining main/helper endpoint over the other 1500 arbitrary
inputs. I independently replayed that candidate under the source's chart and
lifecycle grammar while **retaining all 6,279 MOVEs**.

This is not a physical supplier admission. The optimized #7481 invoice gives
the zero transfer at event 48865 for free, but it belongs to public role 1343,
not newly owned role 1500. A CLEAR/INIT pair on ID 1500 does not implement that
transfer. The current one-swap reduction must either keep and charge event
48865 or separately prove an allowed zero-state chart retag for public role
1343. A's tree result explicitly remains an ideal relaxation and makes no
emitted-word claim.

## Exact scalar reduction

Both 1354 and 1500 are helpers, outside all 400 main input/output roles.
Their target ranks are 7 and 1. Under the swap, each new public role
`q < 1500` carries old role `swap(q)`, where `swap` exchanges 1354 and 1500.
Thus old helper 1500 remains an arbitrary public input and its identity target
appears at new public ID 1354. Old helper 1354 is replaced by the zero-owned
ID 1500. The exact rational replay verifies that its final row is zero after
the specialization; all other helpers retain their own unit rows and every
main output row stays unchanged.

The only deleted scalar instructions are:

| Event | Instruction | Exact zero condition after setting input 1354 to zero |
| ---: | --- | --- |
| 38193 | `SCALE 1354, -1` | destination row is zero |
| 48866 | `ADD 1354, 1343, 1` | source row is zero |
| 49468 | `SCALE 1354, -1/4` | destination row is zero |
| 57816 | `ADD 1343, 1354, 1` | source row is zero |
| 59203 | `ADD 772, 1354, -1` | source row is zero |

For a linear `ADD` or `COPY`, adding an identically zero source leaves the
destination row unchanged. Scaling a zero row also leaves it zero. These are
exact rational identities for every remaining input, not cancellations at
selected numerical values. The candidate grammar replay confirms all
remaining scalar cochart checks, all public/owned MOVE directions, and the
new owner's init/clear lifecycle. The new owner is live across the source;
the replay observes peak live-owned count 51 with 69 owned slots available.

## The free transfer is a separate obligation

The sole zero MOVE is event 48865:

```text
MOVE owner 1343, chart 252 -> chart 127, public
```

The source row is supported only on input 1354 immediately before this MOVE,
so it is zero after specialization. The MOVE has rank 7, and the next
surviving operation on role 1343, event 48867, uses chart 127. Role 1343
remains public after swapping 1354 with 1500. Removing the MOVE alone leaves
its current chart at 252 and makes the following event ill-typed. Replacing it
with `CLEAR/INIT` is also disallowed for this public role under the retained
ownership grammar. The new owned role is 1500; the zero transfer is not on
that slot.

Keeping and charging event 48865 is valid and was done in my candidate replay.
If an implementation instead omits it, it needs a precise compiler rule for
retagging an identically-zero public field and proof that the rule is allowed
by the retained interface. No such rule is established here. No frame reset
for nonzero data is assumed.

## Invoice consequence

The frozen exact tree-DP record covers 102 variables in 78 factors, including
an 8,018,560-state tree factor via min-sum dynamic programming. Its nine
`min(r,k)` frame maxima are all zero; A also compared restricted Cartesian
enumerations against the tree recurrence on nine controls. For helper 1354, the optimized paid
histogram differs from the old one only by removing one rank-seven MOVE; the
lost helper target is also rank seven. The complete 17-call invoice therefore
loses 17 rank-seven targets and 17 rank-seven paid jobs, leaving its signed
rank histogram unchanged pointwise. This holds for every rank-price function,
not just at `.0038` or `.004`.

Restoring the public MOVE's rank-seven charge makes the signed histogram worse
by 17 at rank seven. Ordinary compiler work, the added owner lifetime, and
other reset/allocation charges are additional costs. Thus the ideal tree
relaxation supplies an upper bound; it does not show a positive moment gain.
The new INIT/CLEAR and five deleted scalar operations can still change finite
compiler or precision constants, so those require a fresh complete accounting.

## Remaining implementation checks

- **Phase:** exact scalar rows show a no-op on the relevant input subspace, but
  the transformed Clifford/operator replay must verify relative and global
  phases after deleting the five gates and changing owned boundaries.
- **Precision:** recompile or replay the altered schedule. Exact zeros in the
  rational model must be shown to remain exact at the precision-tape layer;
  INIT/CLEAR and any omitted/retained MOVE costs must be charged.
- **Caller:** remap old helper 1500 to new public ID 1354 in every one of the
  17 native invocations, remove old helper 1354's target, and recompute caller
  interfaces and full budgets. The 400 main roles are unchanged; helper-order
  and width assumptions still need an explicit caller check.
- **Ownership/allocation:** validate the 69-slot declaration, lifetime peak,
  address routing, and lifecycle charges in the actual compiler model.

No full kappa is claimed. Helper 1354 remains a neutral input specialization
whose lost target and ideal rank-seven movement saving cancel. The source is
#7481, an unselected comparator, and changed contacts, changed frames beyond
the tested corridor, or caller/source resynthesis are outside this receipt.

## Receipt files

- `review.py` / `review-result.json`: independent exact rational row replay,
  role swap/demotion, candidate grammar check, and invoice delta audit.
- A's current ideal result is `worker-a/cold-compose/COMPOSE-SCAN.json` and
  its 17-call expansion is `worker-a/cold-compose/FULL-INVOICES.json`; no A
  files were changed.
