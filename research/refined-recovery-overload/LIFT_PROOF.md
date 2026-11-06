# Actual integer-frame attainment and the complete-output bound

This is the independent construction half of the depth-27 result. It uses
the literal 112-by-8 integer matrix `M` from
`research/precision-state-frontier/FIXTURE.json`, SHA-256
`2ca4d7550fcae5b757ec500f87aee1d2ef9f64b59e4abe2bda93319521304af8`.
The inherited rounded map and frame group are

    K(z) = z - M R(M^T z / 52),
    G = {W in GL_112(Z): M^T W = M^T},

with componentwise nearest-integer rounding, half ties away from zero.
Source facts are `M^T M=56I` and the self-dual binary `[8,4,4]` code
`C=ker(M mod 2)`. The frame sequence has one initial refinement:
`z_1=K(2x)`, `z_(j+1)=K(U_j z_j)`. Source and preceding recovery results
retain #5444, #6327 and #6660 credit. Neither the argument nor its verifier
imports the new lower-bound optimization.

## 1. A literal integer splitting of the source lattice

Let `P=(3,5,6,7,8,9,10,31)` be eight zero-based physical row indices and
let `B` have the corresponding source row vectors as its columns. Exact
rational inversion verifies that `B` is nonsingular, every source row
`m_j` has **integral** coordinates `c_j=B^-1 m_j`, and `2B^-1` is integral.
The greatest absolute value in these 112 coordinate vectors is four.
The same row indices occur in #6660; its `2e_i` witnesses alone would not
establish the assertion about every source row. That stronger property is
checked here on the literal matrix.

The eight selected rows generate the full image lattice
`Lambda=M^T Z^112`. For each of the 104 remaining indices `j`, put

    k_j = e_j - sum_i (c_j)_i e_(P_i).

Then `M^T k_j=0`. Every integer vector has the unique decomposition

    x = sum_(j outside P) x_j k_j
        + sum_i [x_(P_i)+sum_(j outside P)(c_j)_i x_j] e_(P_i).

Thus the `k_j` are an integer basis of `ker_Z(M^T)` and this is a direct
sum splitting of the full integer lattice, not merely a rational basis.
Every integer automorphism of this rank-104 kernel lattice extends by the
identity on the displayed complement to an element of `G`.

Because `2Z^8` is contained in `Lambda`, the binary image of `M` lies in
the reduction of this kernel lattice. Indeed, for an integer mode vector
`q`, choose `w` with `M^T w=28q`; then `Mq-2w` is in the kernel and has
the same binary reduction as `Mq`. The reduction has dimension four.

Reduction `GL_104(Z) -> GL_104(F2)` is surjective. Binary Gaussian
elimination factors an invertible binary matrix into row swaps and row
additions. Each swap is an integer unimodular operation, and each addition
lifts to an integer elementary shear with the indicated exact inverse.
Reversing the elimination gives an explicit lift; no determinant or
coefficient is inverted in the integers.

Consequently any injective linear map from the source syndrome space
`V=F2^8/C` into the reduced kernel lattice is realizable by an actual
integer frame in `G`. A common ambient identification can make the first
map the literal source map, so the first cumulative frame is `W_1=I`.

## 2. A four-dimensional relation space with balanced one-point kernels

Use the source quotient basis represented by mode columns `0,1,2,4`.
Each representative has odd parity. In these four coordinates, the even
syndrome hyperplane is spanned by `1001`, `1010`, `1100` (binary masks
9, 10, 12). For every nonzero `k in F2^4`, choose any basis of the
annihilator of `k`. Mapping its three values into that even hyperplane
gives a rank-three map `A_k:F2^4 -> V`, with kernel `{0,k}`.

Take one copy each of `A_1,A_2,A_3` and two copies of each remaining
`A_k`. There are 27 blocks. Their simultaneous map is injective, and
every nonzero parameter has at least 25 nonzero block images. Hence its
four-dimensional image `L` in `V^27` meets no single coordinate block
nontrivially.

Form `V^27/L`, of dimension 104. Each coordinate copy of `V` injects into
this quotient and the 27 copies span it. Identify it with the reduction
of the actual source kernel, aligning the first coordinate copy with the
source image. Section 1 lifts each resulting injection to `W_j in G`,
with `W_1=I`. Set

    U_j = W_(j+1)^-1 W_j.

These are fixed, known, integer unimodular mode-preserving frames, and
`(U_(j-1)...U_1)^-1=W_j` as required by the chain's chronology. This
establishes realizability of the full relation code; an abstract binary
configuration is not being substituted for an integer-frame construction.

The literal generator uses exactly the annihilator and quotient operations
above. It produces 27 cumulative frames, the first identity and the others
using 209--304 kernel-coordinate swaps or elementary shears. The verifier
checks all 112 integer columns of every frame, both exact inverse and
`M^T W_j=M^T`, then checks the image of all eight actual source columns.
Integer lifts are not claimed short or physically inexpensive.

## 3. The attained zero fiber

For the parity box `[-6,6]^8`, a syndrome has mass

    A = 51,008,161                    at zero,
    B = 50,979,600                    at a nonzero even syndrome,
    D = 50,983,170                    at an odd syndrome.

The verifier obtains these directly by enumerating all 256 parity vectors
of the actual source and adding `7^(8-weight) 6^weight`; it does not trust
the symbolic formulas from the lower-bound optimization.

For output zero, backward quotient choices have the form

    q_j = r_j - 14 sum_(k>j) q_k,       r_j in [-6,6]^8.

In particular `q_j mod2 = r_j mod2`. This uses the cumulative later
quotient, not just the next quotient. The 4-dimensional syndrome relation
space therefore gives precisely 16 positive product terms in the fiber.
Its zero parameter contributes `A^27`; three nonzero parameters have one
zero block and contribute `AB^26`, while the other twelve have two zero
blocks and contribute `A^2 B^25`. Thus the constructed sequence has

    |fiber(0)| = A^27 + 3 A B^26 + 12 A^2 B^25.

The separate primary proof establishes the matching universal lower bound.
The present construction proves its integer-frame attainment.

## 4. Every output, including half ties and adaptive backward boxes

Fix an output `y`. The exact inverse-history identity is

    2x = sum_j W_j M q_j + W_27 y.

The per-mode backward recursion and scalar interval lemma from #6327 say
that once later quotients are fixed, each coordinate of `q_j` lies in an
interval containing at most 13 integers. This includes the literal
half-away tie rule. Conversely every such quotient history satisfying
the displayed parity equation is a unique preimage. Mode preservation
and deterministic forward replay establish this equivalence.

Modulo two, each `q_j` determines a syndrome in `V`. The 27 image spaces
span dimension 104, so the parity equation has either zero or exactly
`2^(108-104)=16` syndrome tuples. Fix one tuple. At every backward step,
`q_j` is confined to a fixed coset of `C` and a product of eight intervals
of length at most 13. Every such box-coset intersection contains at most
`A` points: the binary-character expansion has unsigned bound

    (1/16) sum_(c in C) 13^(8-weight(c)) = A.

This bound holds for every interval start, so it remains valid when the
box depends on later quotient choices. Backward conditioning therefore
bounds each fixed-syndrome history count by `A^27`, and gives

    max_y |fiber(y)| <= 16 A^27.

No joint Fourier majorant for all history coordinates, independence of
successive interval starts, or claim that zero is the worst output is
needed. Exact integer comparisons give

    2^695 < A^27+3AB^26+12A^2B^25 <= 16A^27 < 2^696.

Together with the universal zero-fiber lower bound, this proves that the
minimum fixed packed recovery tag has **696 bits**, over the whole
mode-preserving frame class. The same explicit constructed sequence
attains that packed optimum. The exact optimum of the maximum fiber's
cardinality remains open; equality at zero is not asserted for it.

## 5. Scope and independent checks

`independent_attainment.py` checks the source matrix, actual integer
lattice splitting, 3,024 full frame columns, every lifted source column,
all relation terms and the exact bit sandwich. It also forward-executes
and reconstructs the complete 27-stage chain on zero, all 112 unit inputs
and eight fixed-seed signed samples. The latter are finite corroboration;
the algebraic proof establishes the all-input statement.

Controls reject a source row outside the integer image lattice, a changed
relation receipt, a dependent stage, a forbidden single-stage relation,
an omitted actual lift shear, an integer inverse sign error invisible
over F2, and a 695-bit claim. Normal and optimized Python use explicit
exception checks, not assertions.

Frames change the output function. Fixed known frames, exact integers,
one initial refinement and full output access are retained assumptions.
No physical tag, efficient codec, native caller, bounded-register
implementation, paid supplier invoice or new kappa is supplied. All five
selected framework assumptions remain. Prepared for @CubeJerry with
substantial OpenAI Codex assistance, including independent construction
and checking relative to the lower-bound code. Credit zxv, Ali Romman,
Brian, Nick Petalas and the #5444/#6327/#6660 source lineage. Apache-2.0.
