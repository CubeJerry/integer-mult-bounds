# Independent review: event 40710 preparation bound

Reviewed by `/root/assembly_gate` against the frozen #7481 source, the
retained native and precision contracts, `worker-a/public-cache-interface`,
and a fresh exact-Q audit of the single-promise history circuit.

## Finding

**The rank-eight path lower bound is correct under the proof's explicit
premise that demoted input 1459 is unavailable as an initial resource. That
premise must be enforced by the relation/demotion model before the bound is
used against the 40710 cache.** The exact same-promise history circuit uses
1459's initial frame-189 row as a provider, so losing only 1459's final
rank-one target does not by itself establish unavailability of that initial
row.

## A54 proof checks

- The verifier is pinned to #7481 native bytes and replays the strict prefix
  through event 40709. On the promised probe (x_{885}=x_{1459}=1), all other
  inputs zero, 885 stays at empty frame 3 and 1459 stays at frame 189. 885 is
  written at event 30780 but never used as a donor or transported before the
  candidate. With the demoted 1459 entrance excluded, every nonempty-frame
  history is zero while the required candidate value varies on the promised
  one-parameter family.
- The retained grammar admits INIT/CLEAR only on owned fields, COPY only into
  fresh owned zero storage, and same-frame scalar contacts. Public MOVE is
  strictly nested and positive rank. The precision validator drops its
  exact-zero flag on every MOVE because a rounded child need not preserve
  zero. There is no public zero-retag opcode.
- The compiler replay checks the actual signed tableaux and absolute phases
  for 3→189 rank 8, 3→105 rank 1, and 105→189 rank 7. The paid route bound
  itself applies to any new whole-field scalar dependency path: rank-zero
  scalar contacts preserve frame, every MOVE contributes
  \(|\Delta\dim|\), and any path from dimension 0 to dimension 8 has total
  movement rank at least 8. For (0\le\kappa\le1),
  (f(r)=r^{1-\kappa}) is increasing and subadditive, so that path costs at
  least (f(8)). Branching or sharing new paths cannot avoid one nonzero
  input-to-target dependency path. Injecting 885 into already-paid carrier
  943 would change its original history; that route is explicitly outside
  the fixed-history scope, and the verifier rejects that mutant.
- With one 40710 credit, the gross target/debit allowance is
  (f(8)-f(1)). Under the unavailable-1459 premise the compulsory path
  costs at least (f(8)), leaving net gain at most (-f(1)=-1) per call.
  The pinned 17-call complex invoice therefore moves by at most (-17).
  The receipt checks negativity at the three stated \(\kappa\) values.
  This is a one-credit complex-moment bound, not a BIT or whole-system
  theorem and not a bound on every other credit under the same promise.

## Single-promise history cross-check

I independently replayed all 6,279 MOVE arrivals and 1,501 initial rows,
grouped by exact physical frame ID, and computed exact-Q row bases for all
979 observed frame banks. All 7,780 rows are independent within their banks.
For (u=-e_{1459}-e_{705}+e_{885}), exactly frame 189's 16-row bank contains
u; no MOVE row is a whole-zero under this relation. The unique circuit has
latest support at event 40710:

\[
  c_{40710}=e_{885}+e_{943}
    = e_{1459}+(e_{705}+e_{943})+u.
\]

The strict providers are the initial owner-1459 row at frame 189 and the
owner-705 MOVE arrival at event 40708, also at frame 189. Since each full bank
is independent, the representation of (u) is unique. If an arrival (c)
could be reconstructed from (u) and strictly earlier rows, that would give
a representation of (u) whose latest event is at most (c); hence only the
latest arrival in the unique circuit can be enabled. This independently
checks B57's one-circuit/latest-arrival argument for this relation.

## Required scope condition

The provider identity above uses the demoted helper's initial row directly.
If that initial frame-189 value is still a usable source after dropping its
final rank-one target, then the cache identity is already supplied by strict
earlier frame-189 observations under (u=0), and the frame-3→189 dependency
path is not compulsory for that credit. The A54 bound is valid only when the
chosen demotion removes that input from the available resources or separately
charges its reconstruction. A source-level basis change must state and
verify that rule; “its productive target was demoted” alone is insufficient.

The exact-Q all-frame census limits this single promise to the one MOVE
credit at 40710 and no whole-zero MOVE. This makes the one-credit preparation
bound relevant to a global single-promise gate only if B57's census scope is
accepted and the demoted-initial-resource condition is compatible with the
same promise. It does not cover a different relation, changed original
histories, or the paid-carrier injection possibility.

## Reproduction receipt

`check_one_circuit.py` performs the independent exact-Q replay and writes
`ONE-CIRCUIT-REVIEW.json`. It checks the exact provider identity, strict
chronology, all original history-row independences, zero-MOVE absence, and a
wrong-provider-sign negative control. Its source is the pinned #7481 WORD;
it only reads A54/B57 artifacts for final byte-level comparison.
