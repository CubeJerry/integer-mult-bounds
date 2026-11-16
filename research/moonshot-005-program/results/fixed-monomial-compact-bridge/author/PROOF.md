# Fixed columnwise monomial tables from compact dirty controls

**Conditional physical construction. Pending independent review. No new kappa.**
This extends the reviewed two-control Toffoli bridge to a fixed number of
controls and supplies an explicit lowering for every fixed finite address
permutation. It retains exactly the physical primitives and layer domain of
the compact-control theorem. The finite table is fixed before column width,
layer parameters or input length varies.

## 1. Fixed multiple-control selected-bit gate

Fix an integer g>=1 and the retained movement exponent0<tau<1. Let g disjoint
source slots x_1,...,x_g and a target slot y each contain fK address bits, with
selected positions j_i=rho+iK for0<=i<f and a single fixed0<=rho<K. The slots
are complete ranges and may occur in any order with arbitrary intervening
spectators. The complete address and every descriptor have O(A) bits,
including every physical slot width; this is the retained record-paid domain.
The desired operation is

    y_(j_i) <- y_(j_i) XOR product_(a=1..g) (x_a)_(j_i).

Under the retained record-paid rotations, arbitrary-width chunk swaps, full
rectangular fields and eventual parameter domain, this has tariff

    O(volume*((f log p)^tau+1)).

The fixed constant can depend exponentially on g. Every other address bit,
all temporary coordinates and the arbitrary complete payload records have
the exact prescribed endpoint. There is no initialized payload or new
productive input. As in the two-control case, the displayed operation
permutes the positions of arbitrary records rather than changing their values.

For n=f-1>0 reserve g complete nG-bit front fields u_1,...,u_g, a further
nG-bit front field t, and one nG-bit back field b. Let B=2^G. Define the
earlier-control toggle E by the retained four-update construction with

    c_i=product_(a=1..g) (u_(a,i) mod2).

Every E uses four width-nG swaps and four record-paid rotations. Its target
offset is a fixed-degree polynomial-time function of the earlier controls,
independent of its own target. It restores t on the good set and leaves every
u_a unchanged. Loading or unloading selected x_a bits in u_a uses the same
swap-to-back, ordered rotation and swap-back operation as in the Toffoli
bridge, with two swaps and one rotation.

Let epsilon(0),...,epsilon(2^g-1),epsilon(2^g)=epsilon(0)=0 be the cyclic
binary-reflected Gray sequence. At each vertex execute E; on each edge load
the corresponding source into its u_a on a0-to1 transition and unload it
on a1-to0 transition. The sequence returns every u_a and b. On the good set,
its cumulative target toggle is

    XOR_(epsilon in {0,1}^g) product_a (U_a XOR epsilon_a X_a)
      = product_a [U_a XOR (U_a XOR X_a)]
      = product_a X_a.

This factorization over the binary field proves the identity for every
dirty-control and true-source tuple. There are exactly2^g vertices and2^g
edges. Hence the literal low-position construction has

    6*2^g compact swaps and5*2^g record-paid rotations.

The case g=1 reproduces the retained later-source binary row-addition counts;
g=2 reproduces the reviewed24-swap/20-rotation Toffoli construction.

## 2. Guards, repair and complete physical costs

Declare bad every address with an initial radix-B digit equal to B-1 in any
u_a or t, or a low target guard failing

    2B <= floor(segment/2) < 2^(K-1)-2B.

At every Gray vertex each u_a is exactly its original integer digit plus
either0 or X_a. The good-set condition therefore prevents every load overflow.
Each completed E preserves its target guard and restores t. Thus the same
induction as for Toffoli proves the ideal multiple-control toggle on the
entire good set. The union bound becomes

    delta <= min(1,n*((g+1)*2^-G+8*2^(G-K))).

The ideal gate is an involution fixing all source bits, temporary fields and
target guards. The actual word is a global bijection, since all its modular
rotation offsets are independent of their target. Agreement on the invariant
good set implies actual bad-set invariance. Exact exceptional-stream repair
by the destination keys T S^-1 follows with current inverse controls and all
the same payload extraction, holes, sorting and reinsertion charges. The
number of instructions is fixed for fixed g, so the offset and key arithmetic
remains polynomial in the retained descriptor bound A.

For G=4 ceil(log2 p)+6, n<=p and eventually
K>=G+4 ceil(log2 p)+10, the exact bound is

    delta <= (2g+3)/(128p^3).

It follows from `(g+1)/(64p^3)+1/(128p^3)`. With A=O(p) and record length
exceeding every fixed power of p, the repair and rotation costs are O(volume).
The constant number of width-nG swaps gives the claimed tariff. A finite
number of small parameter cases may be handled by the retained fallback;
the assertion is uniform only in the declared eventual parameter family.

For the omitted highest selected position, put its target after all g selected
control bits by at most one width-one coordinate swap with the latest one.
One ordered bit-target rotation by their product implements the gate. Undo
that swap. This exact O(volume) operation also handles f=1. Repair the low
word first.

In the recursive layout let d denote the layer dimension, independently of
the fixed control count g. Keep the original row-index reservation, put H=dG,
and reserve

    q_F=ceil((g+1)H/K), q_B=ceil(H/K).

The front/back total is at most `(g+2)dG/K+2`. Whole-row padding and role
splits preserve all g+2 complete dirty fields because the row index excludes
their coordinates. The same small-D fallback keeps all reserved axes within
the original dimension. Fixed g changes only the reservation and instruction
constants, so the retained recurrence, stopping rule and strict outer gaps
have the same form. Every completed gate fixes reserved coordinates and
commutes with their previously executed individual kernels.

## 3. Constructive lowering of a fixed finite permutation

Fix h>=1 logical address bits and a permutation pi of their2^h possible
values. The following is a finite explicit source program, not a data-
dependent address gather. Decompose pi into cycles, and each cycle into
transpositions, using at most2^h-1 arbitrary transpositions overall.

For a transposition (a,b), choose a shortest hypercube path
a=v_0,v_1,...,v_l=b. Its length l is at most h. Let s_i transpose the adjacent
vertices v_(i-1),v_i. Executing

    s_1,s_2,...,s_l,s_(l-1),...,s_1

transposes only a and b and fixes every other vertex. Thus at most2h-1
hypercube-edge transpositions implement each arbitrary transposition.

An edge differs in one bit k. Its transposition is exactly a target-k NOT
controlled on the other h-1 bits equalling the fixed common pattern. Translate
each zero-pattern control by one, use the positive multiple-control gate with
g=h-1, and undo those translations. All translations are already retained
affine selected-bit gates. They also follow directly from the earlier-control
toggle with constant c=1, using four swaps/four rotations plus the same guard
repair and highest-bit rotation. For h=1 only this translation is needed. No
clean ancilla or additional logical bit is needed.

Consequently any fixed pi has an explicit finite recipe of at most

    (2^h-1)(2h-1)

multiple-control gates, each surrounded by at most2(h-1) affine translations.
These are conservative bounds; the actual source may use a much shorter
recipe. The inverse reverses the list and each gate is separately charged.
Tensor-lifting the fixed recipe acts as pi on each of f designated columns;
its correctness follows by ordinary composition, not by a distribution of
tensor powers over sums.

## 4. Fixed unit phases and exact monomial table theorem

Let q:{0,1}^h -> Z/4 be any fixed table, and a an optional separate absolute
one-column phase. A complete monomial table sends

    |x> -> i^(a+q(x)) |pi(x)>.

At f columns, the phase is exactly `i^(a*f+sum_i q(x_i))`. Evaluate the fixed
lookup and residue from each record address in polynomial descriptor setup,
then apply the sign change or real/imaginary exchange to its full coefficient
encoding. This is O(volume) in the retained record regime and adds no
coefficient height. Apply the permutation recipe after the phase if q is
input-indexed. If a phase table is output-indexed, its value before the permutation is
q_out(pi(x)); conversely, an input-indexed phase applied after the permutation
is q_in(pi^-1(y)). The inverse monomial has permutation pi^-1 and input phase
`-a-q(pi^-1(y))`. These conventions are part of the literal table.

**Theorem.** For every fixed h, pi, q and absolute phase a, the corresponding
columnwise monomial and its actual inverse admit the retained tariff
`O(volume*((f log p)^tau+1))` under the stated complete-field reservations and
parameter domain, with a fixed finite number of tapes. The construction uses
only retained swaps, polynomial-offset ordered rotations, affine translations,
unit phases and exact exceptional-stream repair. It introduces no further
candidate-specific physical primitive assumption. Its finite constants must
be included in the actual source/compiler invoice.

Here h and the whole table are fixed before f,p or multiplication input size
varies. This theorem makes no claim that arbitrary unstructured permutations
of a growing address space have a cheap tariff. It changes the admitted
fixed-template monomial class without changing those quantifiers.

## 5. Verification and remaining work

The proof uses the reviewed Toffoli bridge and the exact retained source
interfaces, with source copies and SHA256 pins in DEPENDENCIES.json. Run:

```sh
python3 check.py --out output
```

Expected status: PASS_FIXED_MONOMIAL_COMPACT_BRIDGE. The checker constructs
the literal Gray modular words for g=1,...,5, checks5,460 binary Gray
identities through g=6, rejects126 missing-vertex controls and six missing
closing edges, and replays5,120 guarded/bad modular states with inverses and
repair. It constructs and replays all40,320 three-bit permutations, all120
four-bit transpositions and256 four-bit permutation samples. It rejects
missing path returns and missing negative-control translations. Another4,680
phase/inverse cases test the actual table conventions and tensor phase;
negative controls detect unlifted absolute phase and wrong inverse indexing.
It also checks1,024 exact rational guard bounds and the retained dependency
bytes. These finite checks corroborate, not replace, the parameter-uniform
construction above.

The theorem supplies physical source admission only. It gives no profitable
complex caller, complete BIT supplier, new multiplication exponent, or proof
of any of the five foundational assumptions. All source acquisition, exact
operator identities, whole-job endpoint gauges, recursive expenses and
strict supplier inequalities remain separately required.
