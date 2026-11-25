# Guarded constant-space execution of compact stream primitives

Status: **proved local fixed-tape space refinement; independently accepted by
Route B** in `../route-b/REVIEW-PHYSICAL-SUPPLIERS.md`.
This is not a new multiplication envelope. It removes a parameter-dependent
proportional-space coefficient from specified compact operations under
explicit large-field guards. Changing templates, radices and coefficient
fields between recursion levels remains a separate question.

Sources: OpenAI `math@3344da59991ed94f9ba711217b29c1d760badfa6`, November
tape `build/interchange.tex` (ordered streams, rectangle delivery and
visited space), `build/walsh.tex`, and `build/uniformity.tex` (common-tape
serialization). Immediate predecessors at programme checkpoint
`a2d9c4b00c02dadf7bdc970acf9190dfabf9ec32` are E002
`route-a/HEIGHT-PRICED-AFFINE-STREAMS.md`,
`route-a/SUCCINCT-ROW-EXECUTION.md`,
`route-c/succinct-cyclic-executor.md`,
`route-c/polynomial-interchange-invoice.md`, and
`route-b/polynomial-walsh-precision.md`. Their algebraic identities and
time bounds are imports. The refined space bounds below follow directly
from their specified layouts.

Volumes count **encoded bits**, and space counts cells ever visited on one
fixed finite-alphabet multitape machine. All proportional constants below
are absolute. A parameter-dependent number of physical tapes is forbidden.

## 1. Affine-run headers are paid by their whole runs

Let `Q>=2`, `P,B>=1`, and `1<=a<Q` with `gcd(a,Q)=1`. Write
`Q=a q+s`, `0<=s<a`, and `V=PQB`. The predecessor affine scaling splits
each prefix fiber into a runs containing q or q+1 whole B-bit blocks.
Its key length is `h=ceil(log2 a)` bits per run, not per payload bit.

**Lemma G1.** If `qB>=h`, the complete predecessor run-sort/scaling
construction and its inverse visit at most `C V` payload-and-key cells,
plus a fixed polynomial in coefficient and range descriptor bit lengths.
Their earlier time bound is unchanged.

**Proof.** Keys occupy `P a h<=P a q B<=V`. Padding every run to
q+1 blocks and the run count to a power of two gives less than 4V payload
bits, by HS4. Every keyed working array therefore has at most 5V bits,
up to constant delimiters. Stable binary radix passes use a fixed number
of such arrays. All passes reuse the same marked intervals; no fresh
interval is allocated for a new key bit. Key registers are reused from
run to run. The inverse has the same run lengths and key count.
Transposition and reversal use a fixed number of complete payload arrays.
Thus the union of visited payload regions has size at most C V. ∎

**Corollary G2.** If numerator and denominator magnitudes of a rational
scaling are at most `2^H`, `H>=1`, and

    log2 Q >= 2H+4,                                      (G1)

then G1 holds for every B>=1 after coefficient reduction. Indeed
`a<=2^H`, `q=floor(Q/a)>=2^(H+4)`, and `h<=H`. Inverse scaling reverses
the same short-coefficient construction, rather than introducing the
possibly large residue of an inverse. Signs require ordinary reversal.

The payload condition is sufficient, not necessary. Without it the
literal tagged implementation has no absolute proportional-space bound:
take Q=a+1 and B=P=1. Its `a ceil(log2 a)` key bits exceed every fixed
multiple of V=a+1 as a grows. This is a limitation of that implementation,
not a lower bound for modular permutation algorithms. The root's separate
header-free affine sorter may remove this guard altogether; the present
proof does not depend on that stronger construction.

## 2. General row-sort headers and structured rotations

For a row stream `[P] x [R] x [B]`, SR1 attaches
`ceil(log2(2R))` destination bits to each whole B-bit row.

**Lemma G3.** If `B>=ceil(log2(2R))`, SR1 uses at most C V payload-and-key
cells plus its descriptor/register region. A polynomial-size sum of
weighted row permutations has the same space bound if terms are processed
sequentially, retaining only the input, one term and the output accumulator.

**Proof.** All headers together occupy at most `PRB=V` bits. Sorting
uses an absolute number of arrays of size at most 2V. The same term
buffer and accumulator are reused for every summand. The term count
multiplies time, not simultaneous or ever-visited payload storage. ∎

For cyclic formula factors the guard is unnecessary: E002 C3--C5 already
use coordinate rotations, masks and one accumulator, with O(V) payload
space and polynomial descriptor/index storage. They never attach a key to
each module row. An arbitrary succinct matrix cannot be substituted for
this proved masked-translation structure.

## 3. Guarded local compilation theorem

**Theorem G4.** Fix an integer K>=1. A family of local stream plans
indexed by m>=2 has actual time `V m^{O(1)}` and visited space `C V`,
with C independent of m, if all the following properties hold:

* Plan descriptions and scalar registers occupy a fixed polynomial in
  m and `log(2V)` bits, of absolute degree at most K. Computations are
  sequential and their actual bit costs are polynomial in the same data.
* There are at most `m^K` compact row maps, ordered affine instructions,
  masks, aligned additions, copies and reversals. All coefficient heights
  and row-key lengths are at most `m^K`. Each operation is one of the
  stated predecessor processors: its proportional time is `V poly(m)`
  and its genuine one-time setup has fixed-degree cost in m and log V.
  This premise excludes arbitrary polynomial-in-log V work per data bit.
* An absolute number of payload arrays of size at most `C0 V` suffice
  to serialize the list. Every rectangular/check array fits the same
  parent-volume bound, and its region is reused. C0 is absolute.
* Each rational field scaling acts modulo `Q=b^f`, b>=2, with
  `f>=2m^K+4`. Each general row-sort input has at least `m^K+1` payload
  bits per sorted row. Cyclic coordinate rotations need no row-size guard.
* The volume includes one complete b^f field, hence `V>=2^f`.

**Proof.** Apply G2 to rational scalings and G3 to general row sorts.
Ordinary shifts, reversals, comparisons and aligned arithmetic use a fixed
number of payload scans and sequential register regions. The third premise
bounds the number of retained arrays independently of m. A polynomial
number of operations reuses them, so its count increases only time.

Put `z=log2(2V)`. The field guard implies `m^K<=z`. Every additive
register/setup-space term is bounded by a fixed power of z after changing
an absolute constant. For each fixed c, `z^c<=C_c 2^(z-1)=C_c V`.
Thus all descriptor, construction and coefficient registers fit another
absolute multiple of V. Their sequential bit computations have at most
polynomial-m time per bit after using the analogous fixed-degree
`poly(log V)<=C V` absorption for genuine setup. Operations repeatedly
executed per row retain their explicitly charged polynomial-m coefficient;
they are not relabelled as one-time setup. Marked regions are reused, so
these bounds apply to cells ever visited. ∎

The absolute-array premise is indispensable. Retaining m parent-sized
copies violates it even if each individual arithmetic operation is cheap.
The theorem also does not license a generic bit operation costing poly(log V)
at every payload bit; only the predecessor amortized scans and stated
row computations are used.

## 4. The stronger spatial base guard is still polynomial

For the E002 interchanger the split is

    f=floor((e-ell)/(m+2a)),       a=D_I-2.

The compact family has `a,ell,H,log2 W<=m^K` after one absolute
enlargement of K. Therefore

    e >= ell+(m+2a)(2m^K+5)                              (G2)

implies the affine field guard. Any sorted module row retaining one full
spatial field has payload `B>=b^f>=2^f>m^K+1`, proving its row guard.
Zero-width spatial boundaries are handled directly.

The right side of G2 is polynomial in m. Below it, ordinary direct
one-digit interchange takes `O(eV log(2b))` time and absolute O(V) payload
space. For a growing b, pad each of the two one-digit ranges to the next
power of two (total inflation less than four), exchange their binary
digits by elementary bit moves, and discard the known padding. This
charges O(log(2b)) scans; no factor polynomial in the numeric value b
is needed. A fixed radix recovers the source O(eV) statement.
Strengthening the base guard therefore preserves a polynomial-m local
time bill times this explicit radix factor. It does not create an exponential-in-m threshold or a
parameter-dependent proportional-space coefficient.

If a variable choice obeys `m<=e^beta` and the right side of G2 is
at most `C m^A`, one fixed rational `0<beta<1/A` makes the guard true
at every sufficiently large e. The finite remaining widths use direct
operations. This is a useful supplier for a nonstationary recurrence;
the recurrence and full multiplication composition are separate.

## 5. Actual component coverage and remaining gates

| Operation | Absolute payload-space mechanism | Required caller fact |
|---|---|---|
| Cyclic scalar factors | Original input, one translated term, one accumulator | Preserve the specified module and field encoding. |
| Rational affine scaling | G1--G2 bound every run header and padded array | G2's nonbase field guard, or a header-free supplier. |
| General row permutation | G3 bounds destination headers | Every sorted row has its spatial suffix. |
| Dense small checks/spectral repair | Input, check and output arrays; all coefficient registers reused | Serialize roles; no parent-sized buffer per role. |
| Ordered affine factors | Serial triangular instructions with fixed payload copies | Existing recursive field-permutation calls remain paid. |
| Numerical rational scalars | Coefficient/temporary width poly(m) fits record width k | The separate k>=poly(m) precision guard. |

The numerical route's `polynomial-auxiliary-cost-audit.md`, last two
sections, explicitly supplies the absolute-array argument: process one
rectangle at a time, keep the input and output accumulator, retain at most
one transformed source collection and one common temporary batch. Each
collection is a subset of the full label batch. The finite repair children
have volume V/8. The characteristic-two route similarly uses V/16 repair
children and one label-grouped spatial child of volume at most 2V/N<=2V/3.
These are uniform geometric payload ratios, provided the caller preserves
their exact layouts and encoding. Full-volume reserve descents must park
only descriptors, as in the source proof.

Still unproved here: changing radix and coefficient field across levels;
all grouped calls retaining the needed spatial suffix; complete variable-
template call counts; the final numerical/physical recurrence and common
precision; input/output and full-product assembly. They cannot be inferred
from a local space lemma. The note intentionally leaves these as separate
global obligations.

Open next questions: independently check every source local map against
the absolute-array premise; verify variable-alphabet full-rate packing;
combine these guards with the two distinct arity schedules for interchange
and Walsh. No endpoint, new unconditional multiplier, full execution,
formal proof build or human review is claimed.

Credits: Jerry Chen (@CubeJerry); the pinned OpenAI stream, rectangle and
serialization proofs; E002 compact processors; substantial AI-assisted
E003 analysis. Existing factorization and source identities retain their
predecessor credits and scope.
