# Universal arbitrary-order generic Stein-rank lower bound

Working proof, independently checked in outline by the orchestrator.
No actual fine-prime or rounded-source applicability is claimed.

Let d>=1, N=2^d and let x_0,...,x_(N-1) be any ordering of F_2^d. Set
H(q)_ij=product_(k:(x_i xor x_j)_k=1) q_k and E(A)=A-ZAZ^T, where Z is
the ordinary nilpotent one-step lower shift. The claim is

`rank_(Q(q_1,...,q_d)) E(H(q)) >= 2 ceil((N+3)/5)`.

Every fixed d admits a proper real algebraic exceptional set outside which
the bound holds simultaneously for every vertex ordering and for the
corresponding exact inverses. In particular the simultaneous good set is
dense and full-measure in (0,1)^d. This does not prove full rank N, nor a
pointwise theorem for every distinct tuple. The proof below gives a minor
with an integer coefficient ±1, hence a formally nonzero polynomial over
every field. It does not assert the existence of a good point in each
finite field.

## 1. Translation matchings and an explicit minor

For each nonzero mask v, let M_v be the perfect matching on positions
whose vertices carry labels differing by v, and let P_v be its permutation
matrix. Let m_v count its edges joining consecutive positions. The path
directions x_i xor x_(i-1), i=1,...,N-1, therefore have multiplicities m_v,
with sum m_v=N-1 and m_v<=N/2.

Form a multigraph by putting the original matching M_v in color + and its
shift by one position in color -, dropping the unique original pair that
meets N-1 before shifting. The shifted matching misses exactly vertices0
and mate_v(N-1)+1. Every other vertex has one edge of each color. There is
one open path and C_v closed alternating cycles; a double parallel edge is
a cycle of length2. The open path has an even number of vertices because
both endpoints meet original matching edges. All cycles are even.

The signed adjacency matrix is E(P_v). A parallel cycle contributes the
zero2x2 matrix. On each longer cycle, the alternating signs give recurrence
`z_(j+1)=z_(j-1)` in its kernel, leaving exactly two dimensions over every
field. The open even path is nonsingular. Consequently

`rank E(P_v)=N-2C_v`.

There is a stronger certificate: remove two adjacent vertices from each
closed cycle and keep the whole open path. The induced graph is a disjoint
union of even paths, with all edge coefficients ±1. Each even-path adjacency
determinant is ±1, by its unique perfect matching. Thus the retained
principal minor, of size r_v=N-2C_v, has determinant ±1. This includes
characteristic2, where a parallel +/− pair still cancels.

Write q^v=product_(k:v_k=1) q_k. Since
`H(q)=sum_v q^v P_v`, the same principal minor of E(H(q)) has coefficient
±1 at monomial `(q^v)^r_v`. Indeed every determinant term uses r_v entries,
each entry is multilinear, and reaching exponent r_v on every selected
variable and zero on every other variable forces every selected entry to
use exactly q^v. Its coefficient is precisely the signed-adjacency minor.
Therefore generic rank is at least max_v (N-2C_v).

## 2. Two complementary cycle counts

Put m=max_v m_v. Every closed component contains an original matching
edge that is not adjacent in the linear ordering. If all its original edges
were adjacent, start at its least vertex k. Its original edge must lead to
k+1; the shifted edge then leads to k+2. The next original edge is forced
to k+3, and so on. This strict ascent cannot close inside a finite component.
Distinct cycles use distinct original edges, so

`C_v <= N/2-m_v`, and hence `max_v rank E(P_v) >= 2m`.

Let L_v be the number of parallel two-cycles. Each other cycle has at
least four vertices and the unique open path has at least two. Thus

`C_v <= (N-2)/4 + L_v/2`.

A parallel component on positions a,b, both positive, occurs exactly when
their path directions agree:

`x_a xor x_(a-1) = x_b xor x_(b-1)`.

Its unique translation mask is v=x_a xor x_b. Conversely each such pair
gives exactly that parallel component. Therefore

`sum_(v!=0) L_v = sum_(u!=0) binom(m_u,2)`.

Since every m_u<=m and their sum is N-1, this is at most
`(m-1)(N-1)/2`. Averaging the cycle bound over the N-1 masks gives

`min_v C_v <= (N+m-3)/4`,

and so `max_v rank E(P_v) >= (N-m+3)/2`. Combining both estimates yields

`max_v rank E(P_v) >= max(2m,(N-m+3)/2) >= (2N+6)/5`.

Every rank r_v is even. Rounding upward to an even integer proves
`max_v r_v >= 2 ceil((N+3)/5)`. The formula also gives the correct complete
rank2 and4 for N=2 and4. No asymptotic omission of small dimensions is used.

## 3. Quantifiers, inverse transfer and cost scope

For each ordering choose one of the certified nonzero minor polynomials.
There are finitely many orderings; their product is a nonzero polynomial
over R. Away from its zero set, every ordering obeys the bound. The zero
set of a nonzero real polynomial has empty interior and measure zero,
by induction on the number of variables and the one-variable root bound.
Thus the positive cube contains a dense full-measure set of simultaneous
good tuples. This is the precise meaning of generic here.

For any invertible A, the block matrix [[A,Z],[Z^T,A^-1]] has Schur
complements E(A) and Erev(A^-1)=A^-1-Z^T A^-1 Z. Its two rank factorizations
give rank E(A)=rank Erev(A^-1). With the reversal permutation J, JZJ=Z^T,
so rank E(A^-1)=rank E(JAJ). Reversal is another allowed ordering. Hence
the uniform all-order forward result implies the uniform all-order inverse
result, without a persymmetry premise. H(q) is positive definite for
0<q_i<1 since each2x2 factor has eigenvalues1±q_i.

For the ordinary lower/upper triangular Toeplitz factors L(u),U(v),
`E(L(u)U(v))=u v^T`. Thus an exact sum of k such products requires
`k>=rank E(A)`. Materializing both full length-N generator vectors costs
2kN scalar slots, giving an all-order generic Ω(N^2) count for this format.
No general rank/runtime lower bound, free gauge, source-parameter admission,
conditioning margin, rounded theorem or multiplication-kappa change follows.

## 4. Discovery limits and controls to preserve

The stronger determinant-not-identically-zero claim remains unproved.
Coordinate-only connected-graph certificates cover4368/5040 translated
normalized d3 orders. Allowing every nonzero translation mask covers all
5040, but explicit d4/d5 orders have every mask graph disconnected.
These are failures of a sufficient certificate, not generic counterexamples.

At the actual rational tuple q=(1/2,1/3,1/5), the ordering
[0,1,2,3,7,5,6,4] has exact rank6, not8. Its determinant is
`product_i(1-q_i^2)^2 (ab-ac-bc)^2 (ab+ac+bc)^2`.
The standard Gray ordering has different squared factors. Distinct
parameters alone do not certify full rank, and finite modular nonzero
checks do not settle a universal all-d determinant theorem.
