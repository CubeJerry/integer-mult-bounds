# Succinct execution of power-of-two cyclic factors

Status: proved structural and tape component; independent review and finite
replay pending. This is not yet a complete multiplier theorem.

The predecessors are `routes/B/formula-full-rate-linearization.md` and
`routes/A/power-two-degree-predictor.md`, at programme head
`0607d044d1d09489580da0e5828588820e1a6775`. The tensor factorization is
established prior mathematics credited there. This note concerns its
actual row-index maps and execution, not a new factorization identity.

## 1. Syntax and representation

Work over a fixed characteristic-two field K, later F4. The query variables
are formal commuting scalars at this stage. Every positive-degree subtree
has a prescribed positive factor length. Constant-only subtrees are identified by syntactic degree zero and folded
by exact field arithmetic. A positive-degree subtree is never removed
merely because its coefficient or value becomes zero for a particular shift. Normalize to these operations:

* An affine leaf has length one, width one and at most k listed terms.
* Padding from length a to d>=a appends d-a identity factors.
* Scaling by c multiplies the stage-zero factor by c and leaves all other
  factors unchanged. This remains valid when c=0.
* A product of lengths a,b and widths r,s has length a+b and width rs;
  factors first act on the first tensor coordinate, then on the second.
* A sum has both children padded to length d, where d is a power of two.
  Its width is d r s. The characteristic-two cyclic sum has twist one.

Every copied subtree is counted in formula size S; there is no sharing.
Assign one module coordinate `a_s in Z/d_s Z` to each sum node s, in
preorder. Product nodes concatenate their coordinate lists. For the shifted count
family, retain exactly the same syntax and degree budgets for every shift
beta. Do not prune beta-dependent zero leaves, constant scalings, or
branches: only F4 leaf/scale coefficients vary. They are computed from
the O(log m)-bit pairwise-shift seed in polynomial m time. Then

    w = product_s d_s,   log2 w = sum_s log2 d_s <= S log2 D,    (C1)

where D bounds all budgets. Leaves, pads and scales add no coordinates.

## 2. Exact index formula at an addition

Let a sum node have length d and child modules U,V. At total grade t,
identify its grade-t space with `(a,u,v)`, with child cyclic grades a and
`t-a mod d`. Its stage-t factor is the sum of

    left:  (a,u,v) -> (a+1 mod d, A_a u, v),
    right: (a,u,v) -> (a, u, B_(t-a mod d) v).                    (C2)

Here A_a u and B_b v are linear maps, possibly with many terms. This is
directly `L_A tensor I + I tensor L_B`, restricted to total grade t.
Both summands increase total grade by one. Wraparound a=d-1 is included.

At a product of lengths a,b, stage t selects the first child's factor t
if t<a; otherwise it selects the second child's factor t-a. The other
module is unchanged. A pad enters its child if t<a and is identity at
all other stages. A scale contributes c exactly at local stage zero.

All local stages are computed from the *input* module coordinates.
Output coordinates are not substituted into descendant stages prematurely.

## 3. A polynomial list of masked translations

**Theorem C3.** Fix a root stage t. Its affine factor has the exact form

    A_t(X)=sum_(nu=1)^M X_(j_nu) P_(epsilon_nu) D_(nu,t),        (C3)

where `X_0=1`, `M<=k S+S`, D is diagonal, and each summand means

    input row a contributes c_(nu,t)(a) X_(j_nu)
    times its value to output row a+epsilon_nu.                 (C4)

Every component of epsilon_nu is zero or one modulo the corresponding
d_s. The mask/scalar c_(nu,t)(a) belongs to K and may vanish. Its value
and output index are computable in polynomial time in S,k,log D from the
formula, t and the binary row tuple. The complete list of evaluator
programs has polynomial construction time and space; it does not list w
matrix rows. The column-vector order in (C3) is input diagonal first.

**Proof.** Expand only the *linear action of one stage*. At a sum choose
left or right in (C2). Left increments that sum coordinate and passes
input grade a. Right leaves it unchanged and passes `t-a mod d`. At a
product create its two child branches with complementary interval guards;
exactly one is active at each row. A pad contributes its child branch
with guard t<a and an identity terminal with guard t>=a. A scale contributes
c or one according to its current local stage. A leaf selects one of its
at most k listed affine terms.

Each resulting branch is one root-to-terminal path. Its scalar is the
product of all stage guards and scale/leaf coefficients. Its module map
increments exactly those sum coordinates where that path chose left.
Every other coordinate is fixed. Thus it is a fixed translation of the
product of cyclic groups, restricted by an input-dependent mask; it is
injective on its support. All guards use input coordinates.

The number of leaf terminals is the original number of leaf occurrences,
not a product of branch counts in disjoint subtrees: a path enters one
child at a time. Each pad adds at most one identity terminal. Therefore
M<=k S+S. A path has length at most S and uses arithmetic on O(log D)-bit
numbers, modular subtraction, comparison and fixed-field arithmetic.
Direct traversal constructs and evaluates all paths within a fixed
polynomial bound. Summing them reconstructs (C2) and every other node
rule, proving the exact matrix identity. QED.

Collect paths with the same j to obtain an implementation of each affine
coefficient matrix A_j. Spatial query X_j is not executed separately for
every path. In the source shared-pencil compiler A_j acts on the already
routed streams. The decomposition replaces that scalar-row operation and
adds no spatial query calls.

## 4. A fixed-tape implementation without width-many scans

Assume a row-major stream with module coordinates in C1 order, followed
by a nonempty spatial payload of arbitrary length. Arbitrary external
prefix groups are allowed. Every module row has independent input; none
is initialized as scratch. Values use a fixed binary alphabet.

**Lemma C4 (coordinate translation).** Incrementing one module coordinate
modulo d takes O(V) symbol moves and O(V) visited payload cells on a fixed
number of tapes, plus polynomial work in binary range descriptors. Here
V is the complete encoded stream volume.

For a prefix before this coordinate, write its d equal-length blocks as
`B_0,...,B_(d-1)`. The output is `B_(d-1),B_0,...,B_(d-2)`. In one input
scan put each group's last block on one temporary tape and its other
blocks on another. Both tapes retain the groups in prefix order. Merge
by alternating one last block and the corresponding d-1 ordinary blocks.
Tape motion is sequential except for whole-tape returns, each costing
O(V). Equal-range counters use amortized ripple advancement, resets and
returns as in the source elementary-stream lemma; their entire contents
are not reread per symbol. Temporary intervals are reused.

At most S such increments implement any translation in C4 in O(SV)
moves and O(V) visited payload cells. This uses neither w tapes nor w
complete-array passes.

**Lemma C5 (mask and sum).** A term in C4 takes one scan computing its
mask/scalar once per module row, followed by the translations in C4. Every
row has at least one encoded symbol, so polynomial computation per row
costs at most polynomial(S,k,log D) times V. Multiply each symbol of the
row by its scalar, or output zero for a vanishing mask. Accumulate the
translated stream into the same canonical output-row order.

For all M terms retain the original input, reuse one working copy, and
keep an output accumulator. This uses a fixed number of streams and O(V)
visited payload cells, plus polynomial(S,k,log D,log V) descriptor/index
storage. Clear or overwrite the same intervals each pass, charging returns.
Total actual work is

    polynomial(S,k,log D) V
      + polynomial(S,k,log D,log V).                            (C5)

The latter is setup with a fixed absolute polynomial degree. It may be
kept explicit, or absorbed by `log^c(2+V)<=C_c V`; it is not charged away
once per datum. External prefix indices are advanced by the same scan
counters; the masks reset and repeat on their module rows.

If repair extends scalars to `F_(4^e)` while predictor coefficients remain
in F4, represent each symbol by e F4 coordinates. Multiplication by an
F4 coefficient is coordinatewise. More general represented field
arithmetic costs polynomial e and must be charged separately. The
structured-check refinement has `e=O(log m)`.

## 5. Consequence for the count formulas

The predecessor power-of-two count predictor has S=poly(m), D=O(sqrt m),
at most three terms per affine indicator leaf and base field F4. Although
its fully occupied module can have `w=2^(poly(m))` rows, C3--C5 implement
each affine coefficient matrix on concatenated rows in polynomial m work
per encoded input symbol. The actual index-plan constructor takes
polynomial m time/space. Descriptor storage is polynomial m plus a fixed
polynomial in the external range bit lengths.

This is the scalar-row operation of a *single source shared pencil*.
It does not execute spatial queries for free or alter their recursive-call
invoice. It also does not establish the spectral repair, rational layout,
leading batching, Walsh precision or complete uniform-scheduler budgets.
Those independent interfaces decide the end-to-end consequence.

This result applies to the proved masked-translation structure, not an
arbitrary succinct or sparse matrix. An expanded matrix remains valid
but can be unnecessarily expensive for this particular construction.

Credits: the established cyclic matrix-factorization tensor construction
and source predictor credited in predecessor files; the predecessor
power-of-two and structured-shift refinements; Jerry Chen (@CubeJerry);
AI-assisted E002 Route C index and tape analysis.

## 6. Exact finite support

`verify_succinct_cyclic.py` independently constructs the dense formal-affine
factors and the path evaluators for 13 formulas, including zero scalings,
unequal padding, nested products/sums, and wraparound grades. It checks 35
exact formal-affine factor identities, 441 path descriptions, and 9,585
path/row evaluations, up to row dimension 64. It additionally checks 560
full cyclic products at all F4 assignments in its small examples.
Omitting the left grade rotation is rejected in 24 factors, and replacing
`t-a` by `t+a` is rejected in 10. The receipt is
`succinct-cyclic-verification.json`. These checks do not execute a tape
program or prove the universal/asymptotic statements.
