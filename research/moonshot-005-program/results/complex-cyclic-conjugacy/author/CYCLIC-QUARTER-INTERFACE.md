# Exact all-width units for the quarter-phase interstage family

**Proved ordinary source and inverse construction, with explicit operation
accounting. The three-native `(4,2,1)` endpoint is still unresolved. No new
supplier or kappa is claimed.**

## 1. Why this interface is being used

The middle-native criterion leaves an actual ordinary conjugacy problem.
Sampling invertible one-column matrices from a large tensor-word span does
not prove that the same expression is an ordinary unit at unbounded widths.
This family replaces that gap by four exact three-by-three matrices and a
literal fixed inverse recipe. It also permits four different bank routings,
controlled by quarter phase, before the square-cross native.

The one-column source is the admitted four-bit
`A=C_b D_acd P`, with its exact ordinary gauges `S,L4,R4`. Let
`D_b=diag(i^b)` on its 16 addresses. For a fixed admitted unitary monomial `T`,
put `h=T^-1 D_b T` and `h_V=h^(tensor V)`.
Examples are `D_b`, `D_c`, `L4 D_b L4`, and `R4 D_c R4`.
The latter two are genuine nonlinear phase controls; using `R4 D_b R4`
instead would merely repeat `D_b`, since the R4 permutation preserves b.
All these tables and their inverses are actual ordinary services.

All three retained fields are at the same chart, with arbitrary independent
values. The interstage acts on head coordinates only. Shared body services
are unchanged and remain paid.

## 2. A complete unit criterion and inverse

Fix `Q_0,...,Q_3` in `M_3(Q(i))`, independently of V, and define

    Q(h_V)=sum_(j=0)^3 Q_j tensor h_V^j,
    q_s=sum_(j=0)^3 i^(sj) Q_j,      s=0,1,2,3.        (1)

**Theorem.** The following are equivalent:

* `Q(h_V)` is invertible for every positive integer V;
* it is invertible for every sufficiently large V;
* all four fixed matrices `q_s` are invertible.

When these conditions hold, an inverse at every V is

    Q(h_V)^-1=sum_(j=0)^3 R_j tensor h_V^j,
    R_j=(1/4) sum_(s=0)^3 i^(-sj) q_s^-1.             (2)

Thus every inverse coefficient is an explicitly computable fixed Gaussian
rational. There is no growing matrix inverse, advice table, or unproved
one-column-to-tensor lifting in this criterion.

**Proof.** Since `h_V^4=I`, its exact orthogonal spectral projections are

    Pi_s=(1/4)sum_(j=0)^3 i^(-sj) h_V^j.

They satisfy `Pi_s Pi_t=delta_st Pi_s` and `sum_s Pi_s=I`.
Equation (1) becomes `Q(h_V)=sum_s q_s tensor Pi_s`.
For `V>=3`, every `i^s` occurs in the spectrum: choose an input address
whose b-bit count among the V columns is s, and then conjugate by `T_V^-1`.
This is possible for s=0,1,2,3. Hence a singular `q_s` makes the operator
singular at every V>=3. If every `q_s` is invertible, spectral multiplication
proves (2) at every V, including the smaller widths. Fourier inversion gives
the displayed coefficients exactly.

The same proof applies to a finite choice of coefficient tables indexed by
`V mod 4`, provided all sixteen sector matrices are checked. A result in only
one width residue is not promoted to the four-case statement.

## 3. A literal ordinary implementation

There are two exact implementations. Conjugating all three fields by `T_V`,
applying the sector matrix, and conjugating back is a valid initial upper
bound. The following direct-control implementation removes all six of those
monomial services for this particular conjugated-diagonal family.

Write the one-column monomial as `T e_x=tau(x)e_(pi(x))`. Directly,

    T^-1 D_b T e_x=i^(beta(x)) e_x,
    beta(x)=b(pi(x)).                                  (3a)

The two appearances of tau cancel. Thus h is already diagonal in the
original input coordinates; its sixteen-entry Boolean table beta is fixed.
For a tensor address the phase is `i^s`, with

    s = (sum of beta(x_column) across columns) mod 4.

At that address apply the fixed scalar three-by-three map `q_s` to its three
field values. No permutation of any field is performed. This is exactly (1).
Using `q_s^-1` gives the inverse. It preserves every arbitrary input as part
of the required invertible transformation; no clean input, extra productive
field or erased owner is introduced.

The four scalar matrices can be factored once by exact Gauss-Jordan
elimination. A conservative bound per matrix is six **weighted** row
additions `destination += c source`, three nonzero row SCALEs and three
row SWAPs. Reverse the reduction to obtain its forward factorization.
The same instruction count bounds its inverse. Across four sectors this is
24 weighted additions, 12 SCALEs and 12 SWAPs. A weighted addition is not
silently priced as one unweighted retained ADD. For nonzero c it has the
literal source-restoring compilation

    SCALE(source,c); ADD(destination,source); SCALE(source,c^-1).

Applying the resulting four fixed sequences conditionally on s gives a
conservative literal schedule of at most

    24 conditional unweighted whole-field ADD passes,
    60 conditional whole-field SCALE passes,
    12 conditional whole-field SWAP passes,
    0 monomial adapter services.                       (3)

The fixed nonzero scalars and their inverses belong to Q(i); their retained
fixed-scalar arithmetic and precision contracts remain explicit obligations.
The small displayed example uses Gaussian-integer/dyadic coefficients and
can have a much smaller specialized schedule. This is a deliberately
conservative upper bound, not a free application of
a spectral projector. A specialized matrix may use fewer instructions, but
such a reduction must be shown for the actual matrix. The zero-adapter claim
uses (3a); it is not an assertion that arbitrary monomial services are free.

Each conditional pass scans the same complete Cartesian address range as
the corresponding ordinary field pass. An odometer stores the current
address and the state s. After a changed four-bit head column, replace its old
beta contribution by the new one using the fixed sixteen-entry table. This
takes constant work per changed column; the number of digit updates over the entire range is geometrically
bounded by a constant times the number N of addresses. Its setup and control
storage are O(V), and its total combinatorial work is O(N+V). At each entry
the arithmetic is one of a fixed finite list of retained scalar primitives.
Thus the construction uses O(N) such primitive calls plus O(N+V) control
work, with the actual precision, layout and tape costs of those primitives
still charged. It supplies no random access or masked subrange for free.

No interstage data are discarded. A scalar swap's local buffers belong to the
retained scalar-operation implementation, not an unpaid full field owner.
The construction does not prove the global precision/tape or compiler
foundation; it gives this specific source and inverse in terms of their
retained explicit primitives.

The operator norm is controlled independently of V:

    ||Q(h_V)||_2 <= max_s ||q_s||_2,
    ||Q(h_V)^-1||_2 <= max_s ||q_s^-1||_2.              (4)

Equality holds once every sector appears. For every intermediate instruction,
an explicit bound follows by multiplying the finite elementary matrix norms;
`|Re c|+|Im c|` gives a rational upper bound for each scalar magnitude.
The unused conjugating monomials have norm one, and the direct implementation
does not execute them. Therefore neither endpoint nor prefix
amplification silently grows with tensor width.

## 4. Actual quarter-sector bank routing and the active rewind

For any four permutations `pi_0,...,pi_3` of the three bank labels, take
`q_s` to be their permutation matrices. Formula (2) replaces each permutation
by its inverse, so this is an exact all-width ordinary unit. It is unitary
and can instead use at most three conditional bank SWAPs per sector,
twelve in total, plus the state scan and no monomial adapters.

This routing is composed with `H_clock=S^-1 D_b` on one or both **active**
banks of L/U, before or after the routing. Every such fixed clock is an
actual monomial service, with its exact inverse, and is charged separately.
The clocks are not conjugated-diagonal expressions of form(3a); their
permutations are not removed by the direct-control simplification.
The admitted identity

    A H_clock A = D_b A (S^-1 D_b S)

changes a two-head path into a rank-one Gaussian with real ordinary gauges.
It supplies a genuine route outside the fixed path-rank grading hypothesis.
It is not by itself an independent extra job.

A clock on only the native's idle bank commutes through that native. On one
side it moves to an outer ordinary encoding; on the other it is absorbed
into the next interstage. The revised construction therefore uses active
bank clocks, rather than counting an idle-only clock as new early coupling.

For a first routing with at most two active clocks and a second interstage of
the form (1), a conservative additional ordinary invoice is the routing's
conditional passes, at most two clock services, and all items in (3) for the
actual second interstage and any needed inverse/endpoint encoding. All three
native calls and their three common-body idle services remain unchanged.

## 5. Verification controls and status

The exact checker reconstructs a nontrivial four-sector matrix family,
Fourier-interpolates its coefficients and inverse, and verifies their product
in `Q(i)[z]/(z^4-1)` as a matrix identity. It also verifies an explicit
conditional permutation family and actual finite inverse schedules.

A negative control makes only `q_3` singular. Its collective operator is
invertible at widths one and two, where that sector is absent, and singular
at every width at least three. This explicitly rejects a small-width unit
test as an all-width admission. Another control retains the genuine
collective polynomial and rejects tensoring its one-column sum.

The caller search uses exact one-column word products as formal tensor
symbols, then solves phase-sector equations modulo65537 for discovery.
Any candidate still needs exact Gaussian-rational coefficient lifting,
every width-phase case, actual independent Gaussian endpoint factorization,
and the complete source/ordinary/precision/recursive invoice. No failed
sample is a general impossibility theorem. No profitable caller, complete
supplier, foundational discharge or new kappa has been established.

Credit @CubeJerry and the retained source, tensor separation, compact phase
and ordinary compiler contributors; Worker B with substantial OpenAI
assistance. Root supplied the direct-control simplification (3a), removing
the initial six-adapter upper bound. Independent review is separate from
author checks.
