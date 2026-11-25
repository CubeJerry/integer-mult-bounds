# Lead independent review: physical suppliers and the outer caller

Status: **component acceptance and P-O interface closure**. The complete
two-scale theorem still requires the separate P-I/P-W audit. This is
AI-assisted written review, not human refereeing, formal refinement, or
execution of the complete multiplication machine.

## 1. Source coverage

The lead read these complete files at OpenAI
`math@3344da59991ed94f9ba711217b29c1d760badfa6` during E003:

* November tape `interchange.tex`, `permutations.tex`, `walsh.tex`,
  `integers.tex`, and `uniformity.tex`;
* November Fourier `repair.tex`, `kernel.tex`, and `binary.tex`;
* September tape `sections/02-streams.tex`.

Also read in full: E002's outer-tape audit; the predecessor pairwise
Newton/division and polynomial auxiliary-cost notes; E003 A's guarded
streams, comparison labels, full-rate field packing and shared-pencil
schedule; S003's explicit dyadic geometry; B's two-scale implication.
Other source/archive coverage remains partial. This is not a claim to
have checked every dependency or all cited publications in full.

The concurrent geometry is at programme commit
`c65aac1156a46d10c0ef2aa36fd846c7a93518e1`, path
`sessions/2026-11-26-S003/route-b/explicit-dyadic-geometry.md`.
The original E003 programme pin is
`a2d9c4b00c02dadf7bdc970acf9190dfabf9ec32`.

## 2. Shared swap pencils: accepted local schedule

The source low-rank identity gathers, at basis row i and query j,

    X_i(S_(i,j)^(-1)z) + sum_((L,K): i in K) X_(L,j)(z).

The revised schedule must retain raw X_(L,j), before A_j. This was
made explicit after lead review: a work copy receives A_j for direct
delivery; the raw sum enters U_j. The rank-label inverse and A_j commute
because they act on different indices. No address mask is commuted across
an arbitrary coordinate change.

Each U_j has encoded relative volume r*/N. The actual guard m r*/N<=1
pays all m retained intermediates with one input-volume region. The first
pass prepares each source rectangle once, handles every query, and returns
its direct destination accumulator to ordinary coordinates. The second
pass delivers completed low-rank terms through prepared destination
rectangles. Endpoint work is repeated only an absolute number of times.
The two contributions cancel at the same ordinary address, exactly as
required by the source routing identity.

Input, output, rank, source, destination and temporary streams occupy a
fixed number of volume-sized regions. Serial row/label scans can raise
the polynomial-m time exponent without adding m payload tapes. Spatial
calls retain their actual volume weights. The conservative factor-four
schedule surcharge is valid for the earlier geometry. S003's different
elementary lists add their own absolute factor and doubled dimension;
the old numerical admission constant cannot simply be reused. B now
uses a fresh absolute geometric constant. **Accept Theorem PS.**

## 3. Comparison flags and changing fields

In the ordinary spectral layout each H_j precedes N_j. The three N_j
runs below/equal/above H_j give the required labels. Keeping the m
current flags costs O(m) control bits and polynomial-m scans. Complete
Q-by-suffix fibers pay field-loop setup; a long prefix is advanced
amortizedly rather than reread per record. This validates CL's stated
layout and makes no claim for arbitrary scattered predicates.

Full-rate packing is an exact F2-vector-space bijection: d independent
bit rows become one degree-d field row at each opaque payload-bit
position. Input and child volumes contain the same d, so normalized
call volume is unchanged. FP2's d scans charge their time and reuse a
fixed number of streams. They never allocate one tape per basis element.

A completed spatial permutation is the identity on payload bits. Its
child may choose another coefficient field without embedding the parent's
field, since the payload is arbitrary binary data. A finite-repair target
F or F^-1 is not such a permutation: it retains its parent's field and
template throughout local unrolling. The amended FP note states this
boundary. Intermediate mixed bit words need not encode meaningful
numerical values; a completed exact bit permutation adds no rounding
error. **Accept CL and FP1--FP3 with these interfaces.** Global visited
space still needs the contracting-stack argument.

## 4. S003 fixed radix three: accepted explicit construction

The hyperbolic completion G=[[B,I],[I,0]] has inverse [[0,I],[I,-B]],
even for singular B. With e,z_v of square two and orthogonal,
(e+z_v)/2 and (e-z_v)/2 have the required unit Gram block. Removing
their two primal pivots makes projection of the complement injective.

Rectangle star pivots are disjoint. The cross vector's primal z
coefficient is -2, proving independence from the stars. Its square is
8-8=0 and its star pairings vanish by the rectangle Far relations.
Its reserve coordinates are

    2 a_v - sum_a(f_(a,l_a)+f_(a,k_a)),

namely `a+2 sum s` at a source and `-a+2 sum t` at a destination.
The distinguished anchor coefficient is one and all stars have separate
unit pivots. These are explicit unimodular changes with no uncontrolled
elimination denominator.

The common layout places the complement early, the pair centrally and
isotropic differences late. Residual endpoint maps are lower triangular
in that order. Earlier-target shears pay two explicit interchanges;
reserve preparations are shared across queries. All diagonal units are
powers of two, so radix three works at every arity and initial binary
padding is less than nine. This removes the growing-prime-menu premise.
The lead accepts this by its basis/pivot argument. A/B's isolated exact
replays are additional evidence; this note does not claim the lead ran
those particular replays.

## 5. P-O: replacing the source call interfaces

Put

    F(u)=sqrt(1+u) 2^(C Phi(log2(u+2))),
    Phi(y)=y^(2/3)(log2(y+2))^(1/3).

Assume the separately proved interchanger costs V F(u), up to fixed
logarithmic factors, and the selected-bit Walsh routine has the stated
F(a) envelope with an absolute O(k)-bit record width. F is increasing.
These are explicit contracts, not substitutions into fixed-rho constants.

### Record permutations

In `permutations.tex` a guarded XOR pass uses an absolute number of
equal-width interchanges and rotations. Offset/rank calculations have a
fixed polynomial degree in k. Its G=C_guard log(2k) guard pays prefix
setup and makes exceptional tagged sorting cost O(V). Replace the
interchange contribution directly by V F(L), with O(log k) passes.
Short chunks use O(log k) elementary moves. Thus bulk XOR costs
V(1+F(L)) poly(log k) plus polynomial setup; no power-law identity for
F is used.

The two-involution position permutation and controlled Beneš networks
call those same passes. They therefore cost V F(k) poly(log k).
The source CRT has O(log k)-bit target blocks and a fixed free-control
fraction. Table generation, destination keys and cleanup retain their
charged scans. O(k)-bit tags fit a constant multiple of record width and
are removed before completed recursive payload calls.

### Short Fourier layers and preparation

The source uses b=ceil(log2 n), h=ceil(n/b), k=ceil(log2(4h)), N=2^k,
so Nk=Theta(n) and k=Theta(log n) with absolute comparison constants.
Short-axis selection/trial division remains fixed polynomial-k work.
Its eventual prime-interval assertion is imported unchanged. Failed
shapes use direct multiplication. The interchanger's radix three does
not change that independent outer prime assertion.

The balanced CRT tree has O(log k) depths, each with at most
k/2+O(log k) control bits. The synchronized Fourier construction has
O(log k) unitary layers. Its borrowed-coordinate identity restores
arbitrary occupied neighbors. Reflection count and phase denominators
are independent of the new template. Block tables have polynomial size;
full diagonal streaming writes fewer than 2N products across all prefix
stages. Phase application and pointwise multiplication therefore cost
O(Nk log k) plus polynomial setup. The fixed short-word multiplier is
the source's pre-existing primitive, not a circular call to this theorem.

Each selected Walsh layer uses O(k/log k) bits. B's bound is at most
F(k) poly(log k). P-W must separately justify rational arithmetic,
physical maps and absolute precision; fixed-template source constants
alone would not justify this substitution.

### Numerical boundary and exact output

The source's fixed allowances are norm 2^(13k), Walsh error 2^(-50k),
phase/coefficient errors 2^(-70k), and transform error below 2^(-40k).
If P-W supplies these with one absolute O(k)-bit format, the source
unitary-layer induction applies. Exact permutations add no error.
An explicit numerical-admission guard is needed before choosing that
format; time/space caps alone cannot certify rounding accuracy.

The three-transform convolution and sqrt(S) scaling then have Euclidean
error less than 1/2. The cyclic length exceeds 2h-2, so rounding every
valid coordinate recovers its integer coefficient. The carry scan uses
O(k)-bit carries, costs O(Nk), and writes the full contiguous 2n-bit
product. Hence outer work stays within

    n sqrt(L(n)) 2^(O(Phi(log2 L(n)))).

Marked region reuse, inverse CRT, occupied-coordinate restoration and
exact fallback are unchanged. The common-space chunk wrapper is a
separate part of B's composition proof. **P-O is supplied for the
explicit P-I/P-W contracts.** This does not by itself prove those two
contracts.

## 6. Remaining gate at this review

The important remaining space question is the numerical Walsh executor.
E002 allowed polynomial-m proportional workspace, which is insufficient
for B's poly(log k) bound when m grows as 2^Phi(log a). A fixed-array
schedule for rational row maps and shared Fourier endpoints must replace
that old bound. Route A is supplying this schedule. Route C separately
audits the analytic, setup, precision and common-space implication.

Credits: @CubeJerry; pinned OpenAI manuscript proofs; E002's audits;
S003's explicit dyadic construction; E003 A/B/C suppliers; substantial
AI-assisted composition review. No complete multiplier execution,
formal-kernel build, human review or literature-priority claim.
