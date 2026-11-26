# Independent review of the prime-power-only count compiler

Disposition: **accepted as the stated finite formula and full-row cyclic
factorization component**. A read all of C's `P-POWER-ONLY-COUNT-COMPILER.md`
and its checker, and re-read predecessor `prime-characteristic-count-formulas.md`.
No odd-characteristic interchanger or multiplication bound follows from
this review. The removed algebra is the auxiliary root extension for sum
gates; separate spectral check/conversion requirements remain separate.

## 1. Exact carry values and actual length budgets

For digit values x,y in {0,...,p-1}, Vandermonde gives
`G_p(x,y)=binom(x+y,p) mod p`, since the two excluded endpoint terms
vanish. Because x+y<=2p-2, this residue is the integer carry of x+y.
Fermat gives `1-(x+y+1)^(p-1)=1_(x+y=p-1)` on this range. The possible
second congruent value 2p-1 lies outside the range. Thus PP-C1 gives the
ordinary carry of x+y+c for c in {0,1}. The output x+y+c in F_p is the
ordinary low digit. No digit information is replaced by the ordinary
count modulo p.

The syntactic change is substantive. At position i, both digit inputs
and the incoming carry have actual padded family length at most p^i.
Each `X-r` addition is budgeted p^i. A product of a copies has length at
most a p^i, so each G summand has length at most p^(i+1). The inner
addition X+Y+1 has length p^i, and `(X+Y+1)^(p-1)c` has length at most
p^(i+1). Therefore every binary addition in the flattened carry sum may
use the actual p-power budget p^(i+1), while the low digit's addition
uses p^i. No equality of formal polynomials after cancellation is needed
to justify a shorter factor family.

Forming H first at rounded p-power length and then multiplying by c
would fail this budget. The rewritten sum duplicates c, which the size
recurrence explicitly charges. Scalars can be folded without consuming
positive nonconstant length; when a constant is a whole child, its
requested positive-length cyclic family has one scalar factor and the
remaining identity factors. This convention handles zero constants too.

## 2. Unfolded formula size and top length

The new recurrence contains two copies of the predecessor carry. The
binomial products and repeated X+Y+1 contribute O(p^2) copies of the
current digit inputs. A_p=128p^2 has ample uniform slack for these
copies, arithmetic nodes and scalar constants. PP-C2 follows by
unrolling the carry recurrence. In the balanced input tree, substituting
the inductive bound gives

    A_p sum_i 2^(k-i)
        [A_p^(r-1) 2^i binom(r-1+i,i)]
     = A_p^r 2^k binom(r+k,k).

The 2^k factor is therefore incurred once in the displayed closed bound,
not once per input-tree level. The additional fixed-offset addition is
one further level. For k<=r=ceil(log2 m), the bound is
`m^{O(1+log p)}` with absolute constants in the O notation.

With t=ceil(log_p(D+1)), every needed digit has budget at most
`p^(t-1)<=D`. Omitting the unused final carry is necessary and is done
both in the proof and implementation. A Lucas term for h has total
product budget `sum h_i p^i=h`. All its internal additions are already
bounded by D. Padding the final Newton sum to the least p-power L>=D
therefore gives L<=pD and p-power budgets throughout. Negative offsets
are legitimate: modulo T^(p^t), `(1+T)^(p^t)=1` in F_p[[T]], including
negative powers because 1+T is a unit. Hence coefficients below p^t
depend only on the residue, exactly the digits constructed by the carry
formulas. Factorials inverted in B_a all have a<p.

The affine binary query substitution requires odd p, as the note states.
For p=2 the finite digit/formula and Frobenius statements are still valid
on their stated inputs; division by two is not asserted there. When p
grows, the formula-size exponent depends on log p. This is explicitly
retained and must not be replaced by an absolute polynomial-m exponent.

## 3. Formal Frobenius and every independent row

The cyclic argument is valid over the commutative polynomial coefficient
ring F_p[q_1,...,q_m], and hence after substitution by commuting queries.
No equality merely on finite spectral tuples is used to deduce the
factorization. On the two graded modules, A and B operate on different
tensor components. Their coefficients commute, so AB=BA. The hypothesis
that every cyclic child product is scalar implies, on every grade,
`A^d=P I` and `B^d=Q I`. For d=p^v the ordinary commuting Frobenius
identity yields `(A+B)^d=(P+Q)I` formally.

A+B advances total grade by one. Restricting successive maps to its d
total-grade slices gives d square affine factors, each slice of dimension
`d r_P r_Q`. The d-fold product starting on any slice is the scalar
identity on that entire slice. Thus every row is an independent input;
there is no initialized one-row subspace or partial-output assumption.
The grade masks in the checker use input grade i and second phase t-i,
which agrees with this restriction.

Padding by identity factors preserves every cyclic product. Concatenating
tensor-extended product families does too: a cyclic cut inside one child
leaves the other child's complete product as a central scalar, and the
remaining pieces form a cyclic product of the first child. Induction
therefore supplies the invariant at every formula node. The maximum
budget L bounds every sum-width multiplier, giving the stated L^S width
majorant and L root factors. Root constants use the positive-length
convention already checked above.

The scalar-slice traversal uses polynomially many grade masks/rotations
in the explicit syntax S,L. A cyclic shift of d equal complete row
blocks is a sequential split/concatenate operation for any integer d;
d need not be a power of two. This supports the claimed succinct scalar
interface only. The note correctly does not infer a shared physical
query-pencil executor or full small-characteristic numerical pipeline.

## 4. Isolated replay and scope

Copied the checker into `p-power-compiler-review-replay/` and ran the copy.
It passed 504 formulas, 47,544 count digits, 47,544 offset digits, 24,924
Newton values, 30,244 actual addition-budget checks, 742 actual digit-size
checks and 936 recurrence majorants. The largest stored unfolding count
was 1,311,481. The checker shares expression references for its own
runtime; it counts unfolding explicitly and does not substitute DAG size.

It also passed 754 primitive carry cases, 192 child cyclic products, 96
sum cyclic products and 21 formal bivariate cyclic products covering
3,225 matrix entries. Ten old-budget, twelve wrong-phase and four
non-p-power Frobenius controls rejected the intended incorrect variants.
The formal coefficient comparisons are material evidence against the
finite-field-evaluation aliasing pitfall, though finite tests are not
the unbounded proof.

Checker SHA-256:
`ff83527440f20499e75553633484edbdd348b201150504bf0f7dd982b78dff97`.
No correction requested. The accepted result is an explicit roots-free
sum-gate compiler for these count formulas, with its factor-p top-length
inflation and growing-p syntax costs included. The missing geometric,
spectral-repair and physical-composition interfaces remain unproved.
