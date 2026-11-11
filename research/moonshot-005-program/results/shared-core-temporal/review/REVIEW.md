# Independent review of fixed-channel and temporal-switch restrictions

Status: fixed-channel and one-switch proofs pass scoped mathematical review;
the two-switch matrix/rank argument also passes, with source-rank replay
recorded separately. No new κ or native construction is certified here.
This reviewer imports no construction-author scientific code. The reviewer
had read the author's claimed statements before constructing these checks;
this is independent implementation/reasoning, not a blind review.

## Fixed channel and boundary cohorts

Let a be the fixed nonzero copy-read row. Choose v in ker(a), v nonzero,
and input each main copy pair as v times an arbitrary main vector z. With
zero auxiliary inputs, copied main operations preserve the copy mode v and
every aggregate core read vanishes. Consequently the complete lift acts as
v tensor R on that subspace, whatever the core-write broadcast weights are.
Zero auxiliary input is a valid specialization of arbitrary dirty input.

This implies the selected lifted block from the doubled entry cohort
{1,773} to doubled exit cohort {112,882} is nonzero: its kernel-mode
restriction contains the nonzero R block [-1/2,0;0,0]. The required E block
is zero. Invertible main-only boundary factors supported inside complete
frame cohorts multiply that block by invertible left/right factors; they
cannot make it zero. Granting all mixing in an equal-subspace cohort is
at least as permissive as literal matching-chart ADDs, so it is safe for
this negative result. Helper-dependent encodings and cross-chart operations
are expressly outside scope.

The separate reverse-adjoint check reproduces both 2x2 blocks and independently
finds the complete frame cohorts using GF(2) row reduction rather than the
author's subspace enumeration. It also verifies no main COPY/INIT/CLEAR and
no zero main SCALE, so the main-only skeleton is invertible. A modified
source must reestablish those properties.

## One canonical internal exchange

Write the prefix zero-helper main/auxiliary blocks as P,C, suffix main blocks
as A,B, and skeleton prefix/suffix as K,L. For independent input modes x,y,
prefix gives (Px,Ky,Cx). Exchange the active and silent main modes, retaining
auxiliaries; suffix then gives (AKy+BCx,LPx,...). Exchanging output labels
back yields (LPx,AKy+BCx). Independent E outputs require LP=E, AK=E,
BC=0. Original correctness gives AP+BC=E, hence AP=E. Substitution produces
E=E K^-1 L^-1 E and therefore E=LK=R, contradicted by the actual source block.
All products retain their order; no commutation of P,A,K,L is assumed.

A separate finite check covers all 216 GL2(F2) triples and 110,592 GL2(F3)
triples (K,L,E), independently solving P=L^-1 E and A=E K^-1 and checking
AP=E iff E=LK. The F2 cases corroborate the matrix identity, not an attempt
to implement the rational balanced half-broadcast over characteristic two.
A negative control E=-I,R=I passes the diagonal equations but has BC=-2I;
it demonstrates that omitting cross-mode leakage falsely accepts a word.

## Two canonical internal exchanges

For three active segments write blocks (Ai,Bi;Ci,Di) and silent skeleton
maps Ki. Starting with x,y and zero auxiliaries, two exchanges yield

- active: (A3 K2 A1 + B3 D2 C1)x + B3 C2 K1 y;
- silent: K3 A2 K1 y + K3 B2 C1 x.

Since K1,K3 are invertible, independent E endpoints force B2 C1=0,
B3 C2=0, E=K3 A2 K1 and
E=A3 K2 A1+B3 D2 C1. The unchanged source has
E=A3 A2 A1+A3 B2 C1+B3 C2 A1+B3 D2 C1. Subtracting gives
A3(K2-A2)A1=0. Set M=A2-K2. Then im(M A1) is contained in ker(A3),
so rank(M A1)<=nullity(A3), while rank(M)<=rank(M A1)+nullity(A1).
Because E-R=K3 M K1, a necessary condition is

rank(E-R) <= nullity(A1)+nullity(A3).

This argument covers ordered cuts including repeated and endpoint cuts. It
does not include arbitrary extra pre/post matrices, role-local switches,
non-exchange codes, changed source itineraries or changed auxiliary wiring.

For source rank lower bounds, reduction modulo a prime gives a lower bound
on rational matrix rank when all coefficient denominators are invertible.
The prefix main block changes rank by at most one at a main<-auxiliary ADD;
other auxiliary events leave it unchanged and main-only invertible operations
preserve its rank. Reverse suffix propagation has the corresponding at-most-
one change at an auxiliary<-main ADD. Between two checked cuts with ranks
rL,rR and d such possible changes, every intermediate rank is at least
ceil((rL+rR-d)/2). This is a rigorous whole-interval bound, not interpolation
of sampled numerical values.

The source has only one COPY, at event31737, immediately after INIT1504
at event31736. Canonical main-only switches leave that owned target zero,
so its premise is preserved for the reviewed switch class.
COPY is treated as its additive linear extension. It agrees with the real
COPY on the source's required zero-target histories. Any proposed modified
word must also satisfy that zero-target contract; an illegal copy is not an
escape. Formal segment blocks may be evaluated outside that physical domain
for the algebraic necessary condition; no physical arbitrary-cut admission
is inferred. Owned INIT/CLEAR are represented as zero linear maps and retain
their original costs/assumptions.

The independent full audit replays all 287 sampled prefix and suffix ranks
with transposed state sweeps and bottom/right modular elimination, using no
author imports. It recovers rank(E-R)=275 and interval bounds302/303 over
all71,262 source cuts, so the maximum nullity sum195 is strictly smaller.
The portable author's52-sample certificate is an exact subset of those
independently replayed ranks. Separate interval recount yields270/270 and
nullity sum260<275, still sufficient. Those are distinct evidence budgets;
the stronger302/303 bounds must not be attributed to the52-sample subset.

## Scope of this review

The mathematical rank/kernel/commutation arguments above are complete in
their stated normalized model. Finite receipts bind source facts and do not
prove the five global assumptions, exact all-column physical realization,
stock, precision, compiler or outer multiplication bounds. Scalar switches
have zero *recursive* child count but positive scalar and physical costs.
Neither one nor two switches is thereby an implemented H4 core.

Prepared by a separate OpenAI Codex agent for @CubeJerry. This is model-assisted
review, not independent human or formal proof-kernel acceptance. All original
source and predecessor credit in the construction packet remains unchanged.
