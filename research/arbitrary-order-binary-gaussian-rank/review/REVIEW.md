# Independent review of the arbitrary-order generic binary Gaussian bound

Status: **PASS for the mathematical claim and stated scope**. The frozen proof read was
`research/arbitrary-order-binary-gaussian-rank/PROOF.md`, SHA256
`3e87c32b9cb3695dc42c2ef10da9c05e74d1742a37e49ce0fe5890ea093463dc`.
Canonical source base is `e54523517d0f03e58352e647c403a5af3e525a57`.

This review was performed by a separate OpenAI research agent for
@CubeJerry. It is independent mathematical derivation and separately
implemented exact corroboration, not human review or proof-kernel
certification. The primary verifier was not imported or used as an oracle.

## Exact statement reviewed

For every fixed `d>=1`, put `N=2^d`, and order all binary vectors arbitrarily
as `x_0,...,x_(N-1)`. For

`H(q)_ij = product_{k:(x_i xor x_j)_k=1} q_k`

and the nilpotent one-step lower shift `Z`, the formal rank of
`H-Z H Z^T` over the rational function field is at least

`r_N = 2 ceil((N+3)/5)`.

A single proper real algebraic exceptional set, depending on fixed `d`,
can be chosen so that every tuple in `(0,1)^d` outside it has both forward
and exact-inverse Stein ranks at least `r_N` for **all** vertex orderings.
The consequence for exact sums of ordinary lower/upper triangular Toeplitz
products is a term floor `k>=r_N`, and hence a `2kN` scalar-slot floor only
when both generators of every term are stored densely and separately.

The distinction between formal genericity, a simultaneously good real
tuple, and an actual prescribed fine-prime sequence is essential. The
proof makes that distinction correctly. No gauge invariance of ordinary
Stein rank, rounded rank bound, runtime lower bound or multiplication
conclusion is established or needed.

## 1. Independent graph and minor derivation

Fix a nonzero binary mask `v`. Its label translation is a fixed-point-free
involution, so it gives a perfect matching `M` of positions. The shifted
partial matching consists of the pairs `(a+1,b+1)` for original edges
`(a,b)` not incident with the last position. Exactly one original edge is
dropped. The shifted matching misses vertex `0` and the shifted partner
of the last vertex; those two vertices are distinct.

Retain the two colors even if they connect the same pair. Every vertex
has one original edge, and all except the two endpoints have one shifted
edge. Thus there is exactly one path and all other components are
alternating even cycles. Both endpoints of the path meet original edges,
so the path has an odd number of edges and an even number of vertices.
A coincident pair is a two-edge cycle, not a simple-graph edge to count
once. Its coefficients cancel in `P_v-Z P_v Z^T`.

On a longer alternating cycle, the equation at a vertex forces equality
of its two neighboring coordinates. The kernel is therefore exactly the
two-dimensional space specified independently on the two parities. This
remains true in characteristic two: the edge signs become equal, and the
same equality follows. The even path has nonzero determinant.

More strongly, delete two adjacent vertices from each cycle and retain
the complete path. Every remaining nonempty component is an even path.
Its determinant expansion has only the permutation that pairs consecutive
vertices from an endpoint: a longer permutation cycle cannot occur on an
acyclic graph, and the perfect matching is forced successively from the
endpoints. The determinant is the product of squared edge coefficients
times the sign of the pairing, hence exactly `+1` or `-1`. This proves
the proposed principal-minor certificate of order `N-2C_v` directly;
there is no cancellation hypothesis hidden in the certificate.

### Why the selected coefficient is isolated

Each entry of the full Stein displacement is a linear combination of
squarefree monomials `q^u`, one for each binary mask. Expand a determinant
of order `r=N-2C_v` into products of exactly `r` such monomials. To obtain
the exponent vector `r v`, every factor must contain every variable in
the support of `v`, since no factor contributes more than one copy. No
factor can contain any variable outside that support, since its required
total exponent is zero. Thus every factor must be exactly `q^v`.

Its coefficient is consequently the determinant of the same principal
minor of `P_v-ZP_vZ^T`, including all permutation signs. The coefficient
is `+1` or `-1`, so the polynomial cannot be identically zero over any
field. This argument uses the extremal exponent vector of a squarefree
monomial; it is stronger than merely observing a perfect matching in the
generic support, which would permit cancellations between terms with
shared variables.

## 2. Independent double count

Let `m_v` be the number of consecutive position pairs differing by `v`,
and `m=max_v m_v`. There are `N-1` path steps, giving
`sum_v m_v=N-1`. Each matching contains at most `N/2` adjacent edges.

A closed alternating component cannot have all its original matching
edges adjacent. Starting from its least position `a`, the original edge
would have to go to `a+1`; the shifted edge then goes to `a+2`. The next
original edge cannot return to `a+1`, already matched to `a`, and must go
to `a+3`. Repeating would strictly ascend forever inside a finite
component, a contradiction. Each closed component therefore consumes a
distinct nonadjacent original edge, proving `C_v<=N/2-m_v` and the
rank lower bound `max_v r_v>=2m`.

Let `L_v` count double-edge components. Apart from them, every closed
component occupies at least four vertices, and the open path occupies
at least two. Thus `4C_v<=N-2+2L_v`.

A double edge at positive positions `a,b` means both
`x_a xor x_b=v` and `x_(a-1) xor x_(b-1)=v`. Equivalently the two
consecutive path directions agree. Conversely, any unordered pair of
positions with equal directions yields exactly one double component,
whose mask is the nonzero value `x_a xor x_b`. The positions are distinct,
so that value cannot vanish; the perfect-matching property prevents any
additional incident edge. Consequently

`sum_v L_v = sum_u binom(m_u,2) <= (m-1)(N-1)/2`.

Averaging `4C_v<=N-2+2L_v` over all `N-1` nonzero masks proves that some
mask has `C_v<=(N+m-3)/4`. It follows that

`max_v r_v >= max(2m,(N-m+3)/2) >= 2(N+3)/5`.

The certificate sizes are even. Rounding this bound up to an even
integer gives exactly `2 ceil((N+3)/5)`. The endpoint cases `N=2,4`
are included and do not need a separate asymptotic convention.

## 3. Simultaneous genericity and the inverse

For each ordering select one mask whose certificate meets the bound,
and its nonzero minor polynomial. The product over the finitely many
orderings is nonzero because the polynomial ring over the reals is an
integral domain. The complement of its zero set is open, dense and of
full measure in the positive cube. In particular the ordering may depend
on the chosen tuple: at every good tuple, the conclusion already holds
for every ordering simultaneously. There is no exchange between an
infinite union and a generic assertion here, because `d` is fixed.

This argument does not exhibit a good point of a finite field. A nonzero
formal polynomial may vanish at all points of that field. It also does
not establish any uniform nonvanishing margin, proximity to the
exceptional set, or membership of a prescribed parameter sequence. A
discrete fine-prime family could lie entirely in the exceptional set.

For invertible `A`, Schur elimination of the two diagonal blocks in
`[[A,Z],[Z^T,A^-1]]` gives

`rank E(A) = rank(A^-1-Z^T A^-1 Z)`.

Applying that identity to `A^-1` and conjugating by the reversal matrix
`J`, for which `J Z J=Z^T`, yields

`rank E(A^-1)=rank E(J A J)`.

The reversed order is among the already included orderings. Every
`H(q)` in the positive cube is invertible because the factors have
positive eigenvalues `1+q_i` and `1-q_i`. Therefore the same exceptional
set suffices for all inverse orders. Persymmetry of a particular ordering
is unnecessary, and the proof does not assume it.

## 4. Exact representation cost boundary

For ordinary triangular Toeplitz matrices, subtracting the shifted
`(i-1,j-1)` entry of `L(u)U(v)` leaves `u_i v_j`, including the first
row and column. Thus the displacement has rank at most one per term.
Conversely, telescoping with nilpotent `Z` recovers

`A=sum_{t=0}^{N-1} Z^t E(A) (Z^T)^t`.

A rank factorization of the displacement converts this directly into
that many triangular Toeplitz products. The minimal unrestricted term
count over the field therefore equals the ordinary Stein rank. The
claimed storage floor follows for separate dense generators. Sharing,
sparse or formula descriptions, other shifts, tensor algorithms, and
gauged representations are outside that format and are not excluded.
No setup, precision, routing, restoration or recursive cost is made
free by this algebraic statement.

## 5. Independent executable evidence

`independent_check.py` imports only the standard library. It constructs
the two colored matchings directly from the vertex labels; performs its
own component walk; and checks the two counts and their combined bound.
Its symbolic checker computes the **whole** multivariate principal
determinant by subset dynamic programming, then reads the isolated
coefficient. It does not simply evaluate the author's claimed
coefficient formula. Independent Fraction elimination supplies the
signed-minor determinant and numerical evaluations.

Normal and optimized runs emit identical receipts:

- All translation-normalized orders for `N=2,4,8`: `1+6+5040` orders,
  `1+18+35280` translation graphs. Translation normalization is valid
  because translating every binary label leaves all pairwise XORs and
  all matching graphs unchanged.
- Eight additional deterministic sampled orders at each of `N=16,32,64`,
  seed `91377`, with all nonzero masks: `120+248+504` graphs. These are
  bounded checks, not exhaustive coverage at those dimensions.
- Twenty-two exact multivariate principal determinants, comprising
  316 nonzero terms. Every target coefficient equals the independently
  eliminated signed minor, is `+1` or `-1`, and stays nonzero modulo two.
- The complete eight-vertex exceptional-order determinant is separately
  expanded by the subset-DP and compared coefficient by coefficient with
  the independently multiplied factors
  `prod_i(1-q_i^2)^2 (ab-ac-bc)^2 (ab+ac+bc)^2`. They are equal.
- Thirty-three independently eliminated signed graph ranks/minors.
- Seven controls: zero mask, cyclic-shift replacement, one-vertex
  deletion, equal positive parameters, a distinct positive rank-six
  tuple, the zero-parameter boundary, and nonzero-polynomial versus
  finite-field-point nonvanishing.

The equal-width control is particularly relevant: with Gray order
`[0,1,3,2]` and `q_1=q_2=1/2`, the Stein rank is two, below the generic
bound four. Genericity cannot be silently removed even inside the
positive cube. At `(1/2,1/3,1/5)` the retained eight-vertex order has
rank six, refuting an unsupported full-rank conclusion from distinctness
alone while respecting the proved lower bound six.

Reproduce beside this review:

```sh
python3 -B independent_check.py
python3 -O -B independent_check.py
```

The script prints only by default; `--write PATH` explicitly requests a
receipt file. The frozen normal and optimized receipts are
`RESULT.json` and `RESULT-O.json`. These checks corroborate the argument
above; they do not replace its universal proof or certify an actual
source matrix. No scientific defect or requested change was found.
