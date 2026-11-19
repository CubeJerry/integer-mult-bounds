# A shared native K cut forces one filtered donor quotient

**Proved necessary linear-interface theorem and a constructive local mixer,
conditional on its stated incoming ranks. No specified complete proper map,
strict supplier, new kappa or foundational discharge.**

The S027 saturation theorem required rank 30 from every donor at each
receiver's K boundary. This package additionally identifies the incoming
cut shared by different receivers, proves equality of their donor quotients
and early flags, and constructs a legal phasewise K370 mixer satisfying all
these rank conditions. Its matching to the desired endpoint remains open.

## 1. Computational contract and exact native facts

Let F be any field, and replace each owner in the authenticated bank-480
atlas by s F-symbols, for any positive integer s. Retain the original
routes and chronology. Local operations are linear, stationary snapshots
are charged, and every proper X dependence reaches K through its actual
incoming D owners. No extra informative preload, return, source read or
MOVE enters this proper computation. Arbitrary original Y baselines are
independent; setting Y=0 below only defines X-response matrices.

The native K370 is the plane containing receivers 1, 73 and 80. There are
45 incoming D flags, one early original-X owner and one late original-Y
owner on each flag. Each receiver gets 15 early and 15 late owners from K.
There are 36 native donors perpendicular to K. A donor j lies in exactly
15 of these D charts. Therefore all information about X_j that can enter
K occupies exactly 30s incoming coordinates, of which 15s arrive early.

For each of the three receivers, every foreign donor has exactly sixteen
visible K planes, each delivering 30s coordinates. If the desired complete
proper block B_ij is invertible of size 480s, all sixteen packet blocks
must have rank 30s on donor j. This is the retained saturation argument.
The fresh checker reconstructs the incoming and outgoing counts from all
106,560 actual owner routes, not from a generic incidence picture.

The incoming count 15 flags times two owners holds at all 1,120 K planes
and every supported native donor. There are 100 native receivers whose
all-foreign cuts are tight. Eleven receivers have one exceptional 45-owner
K terminal; the blanket tight-output claim is not extended to them. The
checker records exactly which receiver/K/donor tuples satisfy the premise.

## 2. The common quotient and phase flag

Fix a donor j at K370. Write R_j:F^(480s)->F^(30s) for its response on
the incoming coordinates of the fifteen D flags containing j. Its early
15s rows form R_j^E. Every other incoming D flag has zero j-response by
proper source support.

Let C_ij:F^(480s)->F^(30s) be the outgoing response through K to receiver
i in {1,73,80}. The common actual K word supplies a matrix L_i on all
90s incoming coordinates. If P_j embeds the donor's 30s coordinates into
that tuple, then

    C_ij = L_i P_j R_j.                              (1)

Invertibility of the final foreign block forces rank C_ij=30s. The
incoming cut has only 30s rows. Thus rank R_j=30s, L_i P_j is invertible,
and

    row C_1j = row C_73j = row C_80j = row R_j.       (2)

This is equality of donor restrictions, not a free global common message:
the same L_i must work at every donor, and the row space R_j can depend
on j. Independently choosing three full-rank packet matrices does not
establish (2).

The early 15s output rows of C_ij are independent because all its rows
are independent. They can depend only on R_j^E, which has at most 15s
rows. Consequently rank R_j^E=15s, and all three early output row spaces
equal row R_j^E. With incoming and outgoing coordinates ordered early
then late, the unique coefficient matrix in (1) is block lower triangular:

    L_i P_j = [ A_ij  0 ; B_ij  D_ij ],

where both diagonal 15s-by-15s blocks are invertible. The late rows may
contain early contributions. Their quotient modulo the common early
space is the same 15s-dimensional late quotient for all three receivers.
No equality of the separate late row spaces is asserted.

Since all 30s rows of R_j are independent, every constituent D-to-K flag
has rank 2s on donor j. Hence all 45 D flags at K370 must have rank 2s
on each of their twelve native donors. Every nonzero combination of a
flag's 2s coordinates depends on every one of those donors. This is a
stronger cut requirement than checking nonzero entries one at a time.

An invertible relabelling of a fixed packet does not change these row
spaces. The old sparse K370 row omits donors 15,69,70,92,107 and cannot
be retained in a completion. Adding those five donors repairs only one
necessary support test; the rank, common-quotient, phase and shared-word
conditions still have to hold.
## 3. A simultaneous phasewise mixer at the actual K370

Suppose all incoming R_j have rank 30s. Work over GF(512), compatible
with the sharper source theorem's field. Order the 45 D charts. Choose
45 row parameters x_a=0,...,44 and 45 column parameters y_b=64,...,108
in the polynomial basis of GF(2)[z]/(z^9+z^4+1). Define

    C_ab = 1/(x_a+y_b).

All 90 parameters are distinct. The Cauchy determinant identity shows
that every square submatrix is invertible: its determinant is the product
of pairwise row differences and pairwise column differences divided by
the product of all cross differences. Every factor is nonzero. The full
45-by-45 matrix is therefore invertible, as is every 15-by-15 minor.

Apply C to the early 45 actual owners and C to the late 45 actual owners,
independently. In each phase assign consecutive row blocks of fifteen
to receivers 1,73,80, using their actual outgoing owner identities. At
each donor j, the selected fifteen input columns are precisely its fifteen
D flags. Each receiver's early and late diagonal maps on those columns
is invertible. Therefore every L_i P_j is invertible, and all three
outgoing donor blocks have rank 30s, the common quotient (2), and the
common early flag. The same two matrices work for all 36 donors at once.

Both entire physical phase maps are invertible. No source is read after
departure, no K snapshot is needed by this block-diagonal mixer, and no
new owner or MOVE is introduced. In-place binary ADD compilation uses
the actual owner identities; all pre-existing atlas movement remains
charged. This construction proves that the additional common-quotient
condition is locally attainable once its incoming-rank premise holds.

The forward words use 164,545 binary ADDs per original body copy across
both phases. Including both inverse words gives 329,090. Repeating the
atlas eight times for b=3840 gives 2,632,720 ADDs for these four local
linear transformations. Each coefficient uses nine binary coordinates.
The words allocate no auxiliary owners and use no INIT, CLEAR or extra
MOVE. The inverse words are counted explicitly; their use in the full
pure-early/pure-Y normalization must follow the complete caller's valid
co-location and ordering. The isolated atlas places original X at Hub
and original Y at Ground for such normalization, but this is not a proof
that arbitrary neighbouring source/D operations compose at no extra cost.

This mixer determines how to preserve saturated donor information. It
does **not** force the decoded endpoint to equal the low-excess target.
In particular it has not been glued to the same selected covariant source
coefficients, to D demands, or to the Clifford phase frames. The latter
may mix early and late coordinates, whereas this proof uses their actual
physical phase partition. No covariance property of a hypothetical
reframed K map is silently inferred from scalar Cauchy coefficients.

## 4. Verification, controls and next question

Run with Python's standard library:

```sh
python -B check.py --repo REPOSITORY --out /tmp/k-cut-check
python -B mixer.py --repo REPOSITORY --out /tmp/k-mixer-check
```

`check.py` verifies every native incoming donor cut and the precise
eligible-output coverage, then isolates all 36 K370 donors and three
receivers. Small exact controls separate full individual rank from a
common quotient, and a common quotient from its required early flag.
All six invertible binary two-coordinate basis changes preserve both
the positive quotient and the incompatible-quotient obstruction. Extra
capacity supplies an explicit escape outside the saturated premise.

`mixer.py` verifies irreducibility of the nine-bit field polynomial, all
216 actual donor/receiver/phase minors, the two full phase matrices, and
literal binary ADD words and their inverses on every input coordinate.
It emits the exact field matrix, actual owner orderings and compressed
ADD words. Duplicate-row and omitted-donor-direction controls fail at
ranks 44 and 14. Regenerated compressed data are compared by decompressed
payload; compressor headers are not a mathematical acceptance criterion.

The universal claims follow from the factorization, rank saturation,
causal triangularity and Cauchy determinant proof. The finite checks
authenticate the actual native hypotheses and emitted finite module.
Independent review is separate from rerunning either author checker.

**Open next question:** choose the actual source and D packet rows so that
all incoming donor quotients are full rank and the induced K outputs,
after valid receiver decoding, realize the prescribed common proper B.
The target equations, ordinary costs, owner normalization, strict BIT
and complex suppliers, complete recursion and all five foundations remain.

Credit @CubeJerry, the retained native atlas and actual-route authors,
the S027 saturation and middle-information packages, and the classical
Cauchy determinant identity. S028 worker C developed this incoming-cut
strengthening and finite mixer with substantial OpenAI assistance.
