# Exact finite odd-parity flow proof

## Problem slice

Let \(H=H_4\) be the symmetric Sylvester Hadamard matrix and \(U=H/2\).
For each \(R\in\{5,9,11\}\), let

\[
X_R=\{x\in\mathbb Z^4:\|x\|_2\le R,\ \sum_i x_i\text{ is odd}\}.
\]

Use a bipartite graph with left side \(X_R\) and right side the odd-total-
parity integer vectors reached by parity-preserving nearest corners. An edge
\(x\to y\) is retained exactly when

\[
\|y-Ux\|_2\le1,\qquad
\left|\|y\|_2-\|x\|_2\right|\le\tfrac12.
\]

The finite question is whether this graph has an injection saturating \(X_R\).
The receipts prove yes on all three named balls.

## Odd coset and complete corners

Modulo two, every entry of \(H\) is one. For odd-total-parity \(x\), every
coordinate of \(Hx\) is odd, so every coordinate of \(Ux\) is a
half-integer. The complete error-one integer neighborhood has 16 corners:
in each coordinate choose either nearest integer, giving displacement
\(\varepsilon_i/2\) with \(\varepsilon_i\in\{-1,+1\}\). Each such corner has
squared error \(4(1/2)^2=1\).

The sum of the coordinates of \(Ux\) is \(2x_1\), which is even. Therefore
\(y=Ux+\varepsilon/2\) has odd total parity exactly when
\(\sum_i\varepsilon_i/2\) is odd, equivalently when the number of negative
signs among the four \(\varepsilon_i\) is odd. There are exactly eight such
corners. These are all and only the parity-preserving candidates. Even
total parity has no rounding issue: \(Ux\in\mathbb Z^4\), and
\(\sum_i(Ux)_i=2x_1\) is even.

## Exact bilateral radial test

Set \(m=\|y\|_2^2\) and \(n=\|x\|_2^2\), both nonnegative integers. Then

\[
\left|\sqrt m-\sqrt n\right|\le\tfrac12
\iff m+n-2\sqrt{mn}\le\tfrac14.
\]

Let \(D=4m+4n-1\). If \(D\le0\), the inequality holds. If \(D>0\), it is
equivalent, by squaring nonnegative sides, to

\[
D^2\le64mn.
\]

The implementation uses precisely this branch and no floating point.
Thus the retained edge relation is exact.

## Paired group and orbit capacities

The paired action consists of \((x,y)\mapsto(Ax,By)\) with signed
permutations satisfying \(BH=HA\). The checker enumerates all 384 signed
permutation matrices \(A\); exactly 192 induce signed permutation \(B\).
Both projections are \(W(D_4)\), the signed permutations with sign product
\(+1\). This action preserves parity, Euclidean error, and both norms.

Each orbit is keyed by sorted absolute coordinates, together with the
product of signs when no coordinate is zero. If the pattern has zero
multiplicity \(z>0\), and nonzero-coordinate multiplicities \(m_r\), its
capacity is

\[
\frac{4!}{z!\prod_{r>0}m_r!}\,2^{4-z}.
\]

If there are no zero coordinates, each fixed sign-product class has
capacity

\[
\frac{4!}{\prod_{r>0}m_r!}\,2^3.
\]

For each sorted nonnegative pattern in the radius ball whose coordinate sum
is odd, the generator creates one key if it contains zero and both
sign-product keys otherwise. Oddness is constant throughout each such orbit
because sign changes do not affect parity. It enumerates the eight corners
at each representative, applies the integer radial test, and records the
accepted quotient adjacencies. The paired action transports these edges
over the complete input and output orbits. Adjacent orbit pairs are
biregular by transitivity on each side.

## Quotient flow gives a full finite injection

The quotient network assigns source capacity \(|I|\) to each input orbit
\(I\), sink capacity \(|O|\) to each accepted output orbit \(O\), and a
capacity larger than all finite node capacities to every active orbit-pair
adjacency. The saved certificates give positive integer orbit-pair flows.
The verifier checks every input row sum, every output column sum, all sink
capacities, and total flow conservation.

When the flow saturates all inputs, distribute \(f_{I,O}\) uniformly over
the individual edges in each biregular orbit-pair edge set \(E(I,O)\):
assign weight \(f_{I,O}/|E(I,O)|\) to each edge. Each input vertex then has
total fractional degree one, since \(|E(I,O)|=|I|d_{I,O}\). Each output
vertex has total fractional degree at most one, since
\(|E(I,O)|=|O|e_{I,O}\) and the quotient sink flow into \(O\) is at most
\(|O|\). For any finite input subset \(T\), its outgoing fractional weight
is \(|T|\), at most the total weight on its neighbor set, at most
\(|N(T)|\). Hall's theorem gives an actual finite injection saturating
every input.

The saved source-side cut lists a union \(T\) of full input orbits and its
exact full neighbor union \(N(T)\). The verifier reconstructs the complete
quotient neighborhood and checks its capacity. Here each cut has
\(|T|=|N(T)|\); it is a complete-neighborhood receipt accompanying the
positive matching flow, not an obstruction.

## Finite results and limits

The three exact domain counts and flow totals appear in README.md and
RESULT.json. Every ball in the named set has a feasible bilateral
half-unit rounding injection. These finite matchings do not prove the
unbounded Hall condition for the countably infinite odd lattice, and the
flow receipts do not define a single global map. No extrapolation, global
construction, or multiplication-bound claim is made.
