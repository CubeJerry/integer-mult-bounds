# Review and verification record

## Root characteristic/reserve obstruction

Root proved the claim; Route C independently re-derived it from the pinned
source. The separate [review](route-c/ROOT-OBSTRUCTION-REVIEW.md) records the
exact scope. `verify_obstruction.py` checks 1,228 eigenvalue/duality identities,
complete spectra of orders 32, 512 and 8,192, 19,998 integer windows and 42,531
alias pairs, with changed-dimension and window controls. CPython 3.12.14 passed.
These are finite checks supporting a written universal proof, not formal
certification of that proof or an implementation replay of the multiplier.

## Route C variable-arity recurrence and padding

Root reviewed NONSTATIONARY-RECURSION.md and SOURCE-PADDING-BARRIER.md directly,
including every proof. The normalized recurrence unfolds with prefix products;
integer-root/ceiling shrinkage separates log-log widths by positive constants;
the excess, rounding and subcritical polynomial toll sums converge under the
stated hypotheses. The conditional interchange result includes a fixed
dispatcher, uniform physical costs, shrinking-volume or descriptor-only
descents, and fixed input/output representation. These are unproved premises
for the published family. The equality-invoice Walsh obstruction is correctly
separated from actual runtime. No implication to a complete root multiplier
is admitted.

For padding, root checked the exact finite-interval dichotomy: either the
radix exponent is constant and the ratio falls by 2^D, or an exponent jump
forces ratio at least b/2. Source b>W>=2^m is specific to its literal all-shift
batch. The first-digit batching factor is a different loss and is correctly
kept separate. The power-selected plateau claim uses literal materialization;
it does not cover different input-dependent radices or compressed layouts.

Root replayed both exact verifiers under CPython 3.12.14. `check_padding.py`
passed 4,160 interval cases and 30 prime-radix witnesses. `check_recurrence.py`
passed 1,970 integer-root cases and 135 recurrence-boundary cases, with
rounding, critical-toll and fixed-excess controls. These tests supplement,
rather than establish, the asymptotic proofs.

All reviewers are AI agents. No independent human review, Lean build or
complete upstream source-kernel replay is claimed. Route A and B results
remain subject to their separate reviews before final admission.
