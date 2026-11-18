# A general complete-graph quotient code and a paid seven-source native word

## Result and scope

There is an explicit simultaneous quotient construction for n sources and n
receivers, where receiver i requests the sum of all sources except source i.
It uses a bank of n−2 field coordinates at each source and one scalar query
from each endpoint of every source-pair plane. The same source query serves
every receiver that sees that plane. The source kernels depend on the donor.

For n=7 this construction embeds in the pinned native root geometry. Its
actual source roles are

    [0,14,15,30,34,38,69],

and the corresponding actual receiver roles are

    [72,85,87,101,98,94,3].

Using F8 with polynomial a^3+a+1, the supplied literal binary record word
has 210 independent original columns. It returns every original X unchanged
at Hub and, for all seven receivers simultaneously, returns

    Y_i' = Y_i + sum_(j != i) X_j

at the actual native facet assigned to i. Each X_j and Y_i has five F8
coordinates, represented by fifteen binary records. Every arbitrary Y
baseline is retained. The exact invoice is

    3933 ADD, 441 INIT, 441 dirty CLEAR, 651 MOVE,
    movement profile 126[1] + 315[5] + 210[7],
    peak 129 live owned binary records.

The coefficient identity has 42 simultaneous foreign blocks, each I_5 over
F8, hence I_15 after binary expansion. This is an actual finite paid native
fragment, not a claim that all 6470 native foreign blocks or the fixed
balanced atlas have been compiled. In particular, all 105 private field
deliveries from source-pair planes to receiver facets are charged. They are
not declared to be free broadcasts or already supplied by shared D4 ports.
No new complete kappa follows.

## 1. General algebraic theorem

Let n>=3, let r=n−2, and let F be a field admitting n linear forms

    phi_0,...,phi_(n−1) in (F^r)*

such that every r distinct forms are independent. For each unordered pair
{j,k}, create a pair plane which can receive the two scalars

    e_(j,k)=phi_k(X_j),       e_(k,j)=phi_j(X_k).

Receiver i sees precisely the pair planes {j,k} with i outside {j,k}.
For each such triple choose a nonzero vector v_(i;jk) in the common kernel
of the r−1 forms phi_l with l outside {i,j,k}. This kernel is a line. Both
phi_j(v_(i;jk)) and phi_k(v_(i;jk)) are nonzero: otherwise r independent
forms would annihilate a nonzero vector.

Send the following scalar from plane {j,k} to receiver i:

    t_(i;jk) = e_(j,k)/phi_k(v_(i;jk))
             + e_(k,j)/phi_j(v_(i;jk)).

Receiver i adds v_(i;jk) t_(i;jk) over its visible planes.

**Theorem.** The result is sum_(j != i) X_j for every i, simultaneously,
for all source values. The source queries are independent of i, and each
plane uses one common lift line for its two donors at that receiver.

**Proof.** Fix i and donor j!=i. The r forms phi_k with k outside {i,j}
are a basis of the dual space. For each such k, the vector

    u_k = v_(i;jk)/phi_k(v_(i;jk))

has phi_k(u_k)=1 and phi_l(u_k)=0 for every other l outside {i,j}.
Thus these vectors are the dual basis, and

    sum_(k outside {i,j}) u_k phi_k(X_j) = X_j.

The j contribution to the receiver's plane sum is exactly this expression.
Summing over j proves the theorem. This uses joint formulas at all edges,
not a separate invertibility test for each source/receiver pair. QED.

The two quotient kernels at plane {j,k} are ker(phi_k) at donor j and
ker(phi_j) at donor k. For n>=4 they are distinct. The common-lift property
therefore does not impose a common source kernel in the actual coordinates.
Each donor uses an MDS collection of its own queries; the forbidden common
dictionary indexed only by physical plane is not being asserted.

## 2. Explicit Vandermonde parameters

If F has at least n elements, take distinct t_0,...,t_(n−1) and set

    phi_k(x_0,...,x_(r−1)) = sum_c t_k^c x_c.

The usual Vandermonde determinant proves the required independence. There
is no field-extension existence search in the supplied n=7 assignment:
F8 is fixed, t_k is the binary field element k for k=0,...,6, and the
irreducible polynomial is a^3+a+1.

One can choose v_(i;jk) to be the coefficient vector of the polynomial

    p_(i;jk)(T) = product_(l outside {i,j,k}) (T−t_l).

Its degree is n−3=r−1. Evaluating at t_l gives the required annihilation,
and evaluation at t_j or t_k is nonzero. In characteristic two, subtraction
is addition, as used by the compiler. These coefficients make all 105
plane outputs and all seven source-form rows completely explicit.

The five output rows of each pair plane are pairwise nonproportional.
Indeed their coefficient ratio is

    p_(i;jk)(t_j)/p_(i;jk)(t_k)
      = C_(jk) (t_k−t_i)/(t_j−t_i),

where C_(jk) is a fixed nonzero constant independent of i. The displayed
fraction is an injective fractional linear function on the allowed t_i.
Consequently each plane's five-by-two output matrix has rank two, and
one common scalar cannot replace its five private outputs. The checker
verifies every pair of output rows exactly over F8.

## 3. Actual native geometry

The layout is pinned by its uncompressed SHA256

    9f3834b7663a25b782531a11ccc22cffb66433de1a9a072059395265fdb07b72.

Every listed source and receiver has an index below 111, so all are genuine
native owners. Exact integer dot products give a diagonal nonzero pairing
between the seven listed receivers and sources. Each receiver is therefore
perpendicular to the other six donors and not to its matching donor. Every
pair of source lines lies in one of the layout's actual A2 planes. The
compiler records all 21 plane indices in the word and checks containment.

This pattern also has a coordinate explanation in the normalized E8 model,
independently supplied by the root reviewer. Let d_j=e_0+e_j, j=1,...,7,
and let w_i have entries +1/2 at 0 and i and −1/2 elsewhere. Both are E8
roots, and w_i dot d_j is 1 for i=j and 0 otherwise. The finite certificate
uses the actual pinned labels above, not a presumed free relabeling of
native owners.

For every output t_(i;jk), its source-pair plane is contained in the true
facet F_i. Thus every upward helper MOVE has a strict real chart inclusion.
No auxiliary source value is introduced at a merely rational chart label.

## 4. Literal binary compilation and restoration

Represent F8 in the basis (1,a,a^2). A fixed scalar multiplication is a
three-by-three binary matrix. Each nonzero entry becomes one co-located
whole-record ADD. The word uses only INIT, ADD, MOVE and charged CLEAR.

First create six field query helpers at each of the seven source lines,
form phi_k(X_j) by ordinary ADDs, and move each query to its actual pair
plane. There are 42 field moves of rank gap one, or 126 binary MOVEs.
All source queries are formed before any original X leaves its source.
The compiler then moves all 35 original field X values unchanged to Hub
and all 35 original field Y values from ground to their receiver facets.
These are 210 binary MOVEs of rank gap seven.

At each pair plane, form one private output helper at a time, move it to
its receiver facet, add its five-coordinate decoded contribution to Y,
and clear it dirty. There are 105 such field helpers and moves, yielding
315 binary MOVEs of rank gap five. After its five outputs, the plane clears
its two query helpers dirty. Every helper is owned, initially zero, live
for all its uses, and retired exactly once. Original records are never
cleared or used as free auxiliary storage.

The binary ADD partition is recorded in RESULT.json. All ADD locations
and all original input columns are checked by two separately implemented
replayers. The 147 field helper lifetimes give 441 INIT and 441 CLEAR.
All helper linear forms are nonzero at retirement, so every CLEAR is
charged dirty. At peak, 42 field queries and one field output coexist,
giving 43*3=129 binary records. Every original source value remains exactly
its own input, and every final output row contains exactly its own arbitrary
Y input plus the six required source inputs in the corresponding lane.

The statement extends to every positive record body width by tensoring
all fixed binary lane maps with the body identity. It does not make
ordinary bit work or the movement price of those records free.

## 5. Verification and limits of integration

Reproduce the author certificate with

    python3 -B build.py --layout LAYOUT.json.gz --out OUTPUT

The independent checker in the companion native-word-review package
imports no author code. It represents each state as a set of original
binary columns, constructs actual rational bases for each chart, verifies
strict inclusion by exact Gaussian elimination, and checks the full final
state. It agrees on every invoice count and rejects an omitted receiver
ADD, an omitted paid source MOVE, and a corrupted arbitrary Y baseline.
The same independent engine accepts the preceding four-source F4 word.

This seven-source word is a complete foreign-subsum fragment with private
deliveries. It does not supply the other native donors or outputs, the
canonical nine packets, the fixed balanced path multiplicities, or a
source-stage compilation of that entire architecture. Its source queries
must not be silently inserted into the balanced atlas at unrestricted
width. The paid upward owned moves place it in the retained nested-owned
model; a stricter descending-only helper model would reject it.

The constructive advance is a single explicit coefficient assignment with
shared source queries and genuinely donor-dependent plane kernels across
seven receivers. Its remaining extension problem is now concrete: realize
these distinct receiver outputs using the same capped shared H-to-D4 ports
and downstream routes, and extend the source-coordinate assignment across
all native receivers. The existing replicated-scalar obstruction and
source Hall criterion remain applicable at their stated scope.

## Attribution

The n=4 donor-dependent F4 construction and literal scheduling pattern are
Worker A's; the general-n dual-basis proof, pinned n=7 embedding, and F8
compiler are Worker B's; the normalized E8 coordinate explanation is the
root reviewer's. Credit @CubeJerry, the native and balanced-atlas authors,
the earlier quotient/gluing work, and substantial OpenAI assistance.
Developed during S023 from programme baseline
8cf982065bccdd62de2856b16635a6ee06dadb0c.
