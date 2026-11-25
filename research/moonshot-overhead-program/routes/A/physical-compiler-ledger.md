# Physical compilation with a bounded expanded template

Status: **accepted for the stated source-extraction contract after independent review**. The finite-generator gate is recorded in `../C/REVIEW-A-BOUNDED-GENERATOR.md`; the physical and end-to-end gates are recorded in `../../verification/S002/lead-review-physical-compiler.md` and `../../verification/S002/lead-review-explicit-extraction.md`. This is an AI-assisted mathematical audit, not a formal build or execution of the complete multiplier.

Source pin: OpenAI `math` `3344da59991ed94f9ba711217b29c1d760badfa6`. The
procedures are those in the November tape proof, with September
`02-streams.tex` used for ordered affine scans and counter details.

## 1. A finite envelope P

Assume explicit valid source templates are supplied with one number P>=2
bounding all of the following finite quantities:

* counts of instructions, scalar updates, roles, matrix dimensions, recursive
  calls, arities, field coordinates and coefficient-table entries;
* total binary size of the expanded data and program;
* the **numeric magnitudes** of rational address-map numerators/denominators
  and the compatible prime radix;
* the bit lengths of dyadic numerical coefficients and the coordinates of
  the exact finite scalar algebra.

Assume both exact recursive-call margins are at least 1/2. The parameter P
contains only finite local data. It does not include final multiplication
time, input length, a growing-depth cost, or a supposition that a primitive
already costs P times its input volume.

There is an absolute exponent C such that the following is the proposed
compiler conclusion, for all sufficiently large accepted digit lengths u:

    time <= P^C u L(u)^rho (1+log2 L(u))^4,
    visited cells <= P^C u + d,
    validity threshold U <= max{U_abs,2^{P^C}}.             (PC1)

Here d is retained description/generator workspace, separately bounded by
the actual constructor. U_abs includes the source prime-shape threshold
and is independent of P and target rho. No numerical value is asserted.
The program tests its actual shape and uses the correct fallback, so it
never needs U_abs for correctness. A single interpreter handles all templates.

## 2. Ordered scans and exact finite symbols

Use binary blocks to encode each exact finite-algebra letter; its block width
is <=P. Scalar multiplication is a linear map on at most P coordinates.
Ordinary modular arithmetic and a scan of an explicit coefficient table take
polynomial P work per letter. All additions and multiplications are exact.
This does not use a flat truth table of all algebra elements.

Digit splitting and fixed row maps can be serialized by extracting one class
or role at a time, as in `uniformity.tex`. At most P classes/roles, P updates
and P-sized tables give polynomial P scans. A rational coordinate scaling
has at most P monotone pieces because its *numeric* numerator/denominator was
included in P. Its field-word arithmetic uses schoolbook integer algorithms
on O(log P+f log b) bits. Polynomial work in f is absorbed by the complete
b^f target range, with a polynomial P coefficient. Fixed spectator counters
are advanced by amortized ripple counting; their complete contents are not
read once per data symbol. This is exactly the restriction proved in the
source elementary-stream lemma.

When a coordinate has many earlier controls, decompose its affine map into
at most P one-control shifts and one diagonal scaling. Each processor then
has an absolute number of formal fields/counters; the number of processors
is polynomial in P. This prevents a hidden degree depending on the number
of controls in the polynomial descriptor arithmetic.

Therefore every ordered affine elementary operation has cost P^{O(1)} V
and visits P^{O(1)} V cells. Precomputing its fixed coefficients and endpoints
has polynomial P cost and polynomial cost in the variable descriptor width.
Radix padding has volume factor <b^2<=P^2. Finite field/radix splitting can
be slow in P; none of that work is called a unit-cost operation.

## 3. Interchange recurrence and stack

The previous paragraph bounds the one-level nonrecursive term by P^{O(1)} V.
There are at most P local descents and instructions. With the relative call
contraction <=1/2, geometric summation gives P^{O(1)} V e^rho, including
bounded base widths <=O(P). A main descent has volume ratio <=2/W<1, with
W>=3, so the parked payload volume sums by a factor <=3. Full-volume reserve
descents occur after merging/clearing, and park only a descriptor.

Every descriptor is a fixed list of collapsed lengths and field indices;
it has P^{O(1)} log(2V) bits and is formed with schoolbook arithmetic.
The fixed polynomial in log(2V) is absorbed into V with a coefficient
polynomial in P. The operation count of this arithmetic does not depend on
an arbitrary program hidden in a descriptor: it consists of multiplication,
addition, division, comparison and copies of the listed lengths. End-access
stacks avoid scans through parked ancestors. The active and parked regions
are reused, so this bounds visited cells as well as live cells.

## 4. Bulk XOR, exceptional sorting and controlled blocks

Offset and exceptional-destination calculations perform a fixed number of
binary additions, modular operations and accesses to the finite template on
O(k+log P)-bit words. For the source CRT controls, recovering a left address
and producing its short-axis tables takes a polynomial of fixed degree in k.
Thus these calculations are bounded by P^c (1+k)^e for absolute c,e.

Choose guard parameter

    G=(e+4+ceil(c log2 P)) ceil(log2(2k)).                   (PC2)

The source exceptional fraction is at most 80k 2^-G. Multiplying it by
P^c k^e, and charging O(k) stable radix passes over O(k)-bit tagged records,
is O(V). The same 2^G complete target range pays for each prefix's offset
calculation. Number of guard passes is O((e+log P)log(2k)), whose P-dependence
is polynomial. Short fields L<G use direct bit operations; their number is
at most G and fits the same declared bound. This yields

    P^{O(1)} V(1+L^rho)(1+log k) + P^{O(1)}(1+k)^e.

The source construction of arbitrary controlled small-block permutations
adds two powers of log k, from block batches and Beneš stages. All extra
factors caused by (PC2) remain polynomial in P. The free-control fraction
in the integer application can be fixed absolutely (e.g. 1/4) above its
absolute short-geometry cutoff.

## 5. Why the short-table polynomial degree is uniform

The source uses axis widths <=20 ceil(log2 k) and blocks of at most seven
axes. Thus a short block has <=2^140 k^140 coordinates, a concrete
polynomial independent of the template. The following deliberately slow
implementations have a common fixed polynomial degree:

* Trial division: at most O(k^20) candidates with O(k^10) trial divisors,
  using ordinary arithmetic on O(log k)-bit numbers.
* Matching, borrowed-position allocation, block permutations and Beneš
  switches: explicit tables on <=2^140 k^140 coordinates; even quadratic
  scanning algorithms give a fixed degree below 300 after word operations.
* Local phases: sums of at most O(k^20) roots of unity, with polynomial-size
  order. Range reduction, the Machin formula, convergent sine/cosine series
  and square-root bisection at O(k) precision use polynomially many ordinary
  integer operations. Uniformly bounded denominators in the source pair
  decomposition prevent loss of an unknown number of bits.
* There are O(k) axes/blocks and O(log k) layers. Looping over these does not
  make a polynomial degree depend on P. For a safe common arithmetic/setup
  envelope one can use degree 1000, after an absolute constant enlargement.

This assertion specifies ordinary finite algorithms; it does not infer a
uniform degree merely from a separate `poly_P(k)` notation. Per-record
numerical products still use the source's fixed short-integer multiplier
with O(k log k) time; replacing those by schoolbook k^2 would spoil (PC1).

## 6. Walsh precision, recursion and setup

Every one-level row coefficient has bit height <=P, and there are <=P
serialized scalar updates. A bound `log2 C_level=O(P^2)` covers norms of
all partial sums and copies. The source path-to-common-ancestor argument
then gives propagation gain

    2^{O(P^2)}(1+k)^{O(P^2)}.

The number of recursive nodes in all base-A pieces is at most
4P(1+k)^(log_A sigma) for the nondegenerate source branching. Allowing
an additional (1+log(2+k)) factor handles arbitrary bounded exceptional
branching conventions and is harmless below. Including fixed-degree setup,
all non-volume setup is bounded by

    P^{O(1)}(1+k)^(1001+ceil(log2 P)).                      (PC3)

P2 shows that above k>=P^C (and an absolute cutoff), this setup fits 2^k,
and polynomial propagation gains fit 2^{k/4}. The fixed boundary norm/error
allowances of `integers.tex` then permit a fixed absolute multiple of k bits
per numerical record. Finite coefficients of bit height <=P fit too.

The exact child volume is V/W, unchanged by serialization. Its contraction
margin is at least 1/2. Therefore the Walsh recurrence has P^{O(1)}
coefficient, active-width exponent rho, and one visible logarithmic factor.
Depth-first parking has geometric ratio <=1/2. Descriptor space and setup
fit the same cutoff; successive pieces reuse their work areas.

## 7. Integer assembly and the candidate profiles

Each of three transforms has O(log k) layers. Controlled block permutations
cost at most P^{O(1)} V k^rho (1+log k)^3. Phases and pointwise products use
the fixed O(k log k) short multiplier; coefficient streams use fewer than 2N
products. Exact carry recovery is linear in volume. Thus the visible total
is P^{O(1)} n L(n)^rho (1+log L(n))^4. Space is P^{O(1)}n plus retained
fixed data. Every return/clear/copy is charged at its parent, and no child
volume is replaced by all parent scratch.

For source input length u and record exponent k, u>=2^{2K} ensures k>=K
above an absolute cutoff. Hence k>=P^C translates to U<=2^{P^{C'}} for an
absolute C'. P1 absorbs the fourth power into target slack epsilon with
factor O(epsilon^-4). If 1/epsilon<=P, this remains polynomial P.

The independent source audit accepts the following conclusion:

    a_j,c_j<=P_j^C,  U_j<=max{U_abs,2^{P_j^C}},

with actual generator g_j,d_j supplied separately. This closes (G6) for
the bounded construction in `bounded-source-generator.md`. The complete source extraction is assembled separately in `explicit-extraction-theorem.md`.

Reviewed interface points: exact compatibility of expanded field-algebra letters
with recursion, polynomial-P implementation of affine streams, uniform
short-table degree, and the source's common-cap serialization. Credits:
the cited OpenAI tape proofs and elementary algorithms; @CubeJerry;
AI-assisted quantitative reconstruction.
