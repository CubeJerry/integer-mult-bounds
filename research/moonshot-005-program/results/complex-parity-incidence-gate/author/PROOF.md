# A sharp 56-mode locality obstruction for the frozen parity-half compiler

**Proved within an explicit incidence and chronology class. This does not
exclude a different complex supplier, square-half geometry, later cross-class
decoding, additional visits, or changed raw-record routes. No new kappa.**

## 1. Inputs and the precise information-flow hypothesis

Use the pinned 104-port omitted-frame native source and the 28 parity halves
of the literal parity-layer word. The 14 full classes have sizes seven or
eight; each is partitioned into halves of sizes (4,3) or (4,4). For a half A,
write A* for its opposite half. Its actual common receiver chart is
C_A=intersection_{i in A} F_i, of dimension six. The exact source incidence is

    {j : L_j is contained in C_A}=A* .                 (1)

The omitted orthogonal frame and every chart in (1) are source-bound finite
objects, independently reconstructed by check.py. No abstract incidence graph
is substituted for the actual source.

Let k be a field, V>=1, and regard a_1,...,a_104 and all original nuisance
inputs y,b,d as independent elements of k^V. In the complex source these are
current a_i=x_i on hosted ports and a_i=x_i-y_i on coupled ports. This is an
invertible change of input coordinates. The desired Y endpoint is

    Y_i=y_i+c_i a_i,

where c_i is a nonzero field scalar (1 or 1/2 in the retained complex word).
Operations and V-by-V coefficients may be arbitrary and noncommuting.

The information-flow class of this theorem is the following. There is a
single subspace U of X-input coefficient rows, of dimension at most qV, such
that, at the final Y_i endpoint for i in A, all X-input coefficient rows lie
in

    U + span_k{the V coordinate rows of a_j : j in A*}.       (2)

The nuisance coordinates need not have this restriction. They are retained
as independent variables, and the demanded final coefficient of y is the
identity. Hypothesis (2) is a precise row-space condition; the next section
proves it for the indicated frozen physical chronology. We do not infer it
merely from a diagram or from the rank of the final residual.

## 2. Why the frozen parity chronology has q<=8

Keep the following actual movement and phase structure of the frozen word:

* Current-a original X and hosted B records go from their own source line to
  the opposite half's C6, then to Hub. The coupled entry reads are performed
  before this stage and define the independent current-a coordinates.
* D records move from ground through omitted mode lines and their class C3,
  then through their own half C6 to their own final facet. Reverse mode owners
  are observed before the C6 source reads. Until they leave their omitted
  lines for Hub they have no a contribution.
* At Hub there are eight forward mode records. Before any Y enters a C6, these
  records have their fixed a-row space U. They move only to their assigned
  C3 anchor station and omitted mode line, as in the frozen source. The anchor
  caches contain those same mode values.
* Each Y subsequently goes through its assigned omitted mode line, possibly
  its class C3, then its own half C6 and its own facet. There is no subsequent
  a-bearing feedback from a C6 or facet to a mode line, another C6, or a C3.
  Stationary correction caches stay at their actual C6 charts.

Arbitrary ground Y precoding, arbitrary linear recoding at the listed actual
cocharts, and arbitrarily many stationary zero-born records are allowed,
provided this phase and information-flow structure is preserved. The eight
forward records may be arbitrary functions of all actual Hub inputs; they
need not remain the author's eight Gram sums. Each supplies at most V new
independent a rows, so dim U<=8V. Arbitrary nuisance mixtures do not enlarge
its a projection.

Before a Y reaches its own C6, any a information that it or a stationary
anchor can have acquired lies in U: mode-line exchanges and class-C3 exchanges
only combine this same information with independent nuisance inputs. At C_A,
(1) gives exactly the opposite-half source coordinates as the additional
available original-X inputs. D or B recoding and stationary caches there
cannot create a new a coordinate outside U plus these source coordinates.
Local recoding of all Y in A preserves the same space. After that C6, each Y
has only its own facet, where its D record has the same allowed a support.
Different target facets are distinct. There is no later route returning these
new local a rows to a shared earlier station. Induction over the actual
chronology therefore establishes (2).

The phase clauses matter. A record returning after a local source read,
a different common receiver chart with external source incidence, an
additional actual source stop, or a genuine later cross-class decoder can
invalidate (2). Such changes must be analyzed and priced separately.

## 3. The all-width rank theorem

Project every completed Y endpoint onto its a coordinates and divide its
row block by c_i. By (2), there exist block matrices Lambda and L such that

    I_(104V)=Lambda U_0+L,                              (3)

where the rows of U_0 span U and the block L_ij may be nonzero only when
j belongs to the opposite half of i's full class. Consequently

    A=I-L=Lambda U_0,     rank A<=qV.                   (4)

On a full class with halves of sizes a and b, the corresponding diagonal
block of A has the form

    A_class = [[I_(aV), P], [Q, I_(bV)]].             (5)

for arbitrary rectangular block matrices P,Q. Its principal identity
submatrices give rank A_class>=max(a,b)V. The full A is block diagonal across
the 14 full classes. Every class has max(a,b)=4. Thus

    rank A >= 14*4V = 56V,    and necessarily q>=56.    (6)

This proof uses no commutativity, invertibility, genericity, positivity, or
scalar diagonalization of the off-diagonal blocks. It holds over every field
for which the specified c_i are nonzero, in particular for the characteristic-
zero complex supplier and all V. It is compatible with unknown independent
Y inputs because their coefficients were never discarded as known values.

For q=8, (4) and (6) contradict each other. No change of scalar coefficients,
local encoder, ground Y precode, or eight Hub mode basis within the stated
flow class can complete all Y targets. A matched reverse correction is not
needed for this contradiction: the forward endpoint alone already fails.
The 48V gap is an information-space gap within (2), not a universal claim
that 48 additional physical returns are necessary.

## 4. Sharpness of the algebraic constant

For a>=b, choose P to embed k^(bV) in the first bV coordinates of k^(aV), and
Q to be the matching projection, so QP=I. Elementary row elimination reduces
(5) to I_(aV) and a zero block, so rank A_class=aV. For (4,4) use the whole
identity pair; for (4,3) use an identity pair on three coordinates. Taking the
direct sum gives rank exactly56V over every field. Hence56 is the exact
algebraic minimum for this locality family. This is not an emitted physical
56-mode source and has no favorable target cost claim.

If the chart-incidence restriction is removed altogether, one could take
L=I and U=0, satisfying the projected equation at rank zero. That artificial
example violates (1) and the diagonal prohibition; it is a negative control
against applying (6) to an enlarged geometry without proving (2) again.

## 5. Full-caller implication and the next escape

The independently replayed actual parity layer leaves the paired cross-class
Gram residual of hosted rank56 and4608 current-a off-diagonal coefficients.
Its complete retained movement invoice has limiting room

    0.9541333063079446... at t=199/200,

with positive fixed-m room first at m=35. Every finite-m room is smaller
than that limiting value. Therefore one additional rank-one MOVE, with the
rest of that source unchanged, already exceeds the target movement inequality
at that exponent. The price check uses exact outward dyadic intervals and the
pinned complete caller; it is not an inference from a rounded decimal.

Together, this theorem and that invoice rule out finishing the frozen
parity layer by only coefficient/codec changes, or meeting the target inequality
by adding movements while leaving all existing movement costs untouched.
They do not rule out changing and reducing existing routes at the same time,
or choosing a genuinely new incidence/decoder structure. The next substantive
complex obligation is to construct such a changed physical source and recompute
its entire invoice, including coupled entries, reverse acquisition, anchors,
owned lifetimes, precision, compiler and all recursive calls.

## Evidence and attribution

Native source SHA256:
`2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883`.
Parity word SHA256:
`f72c890e06437c3b6a177c71019f56e60f30712e5c09c1e241c893c1f180e42d`.
Full caller SHA256:
`d9ba709fa5dcefffe3f3abdcf34600ce188224703cfd743e6db8b58ba4816cb7`.

The finite geometry checks establish the source-specific premise; Sections
1--4 prove the all-field, all-width proposition. Literal source replay and
full-caller interval receipts are separate verification artifacts. Independent
review of this proof is recorded separately. Credit the native E8 source,
omitted-frame and Worker B parity-layer construction, and root's actual
incidence census and block-rank argument. @CubeJerry; OpenAI assistance.
All five foundational assumptions remain. No new complete kappa.
