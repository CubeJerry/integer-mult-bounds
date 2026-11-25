# Exact-window prediction has an unavoidable pencil-depth cost

Status: **proved restricted algebraic obstruction and resource tradeoff**.
This is not a lower bound for interchange or integer multiplication. It
applies to the source's exact Hamming-window predictor, affine query
pencils, and, for the tradeoff, the specified window-marked full-row repair.

Sources are OpenAI `math@3344da59991ed94f9ba711217b29c1d760badfa6`:
Fourier `build/repair.tex`, count prediction, matrix-root evaluation and
Hermite repair; tape `build/interchange.tex`, spectral conversion and its
`4ms/R` call invoice. The comparison with compact prediction is to S002
`routes/A/compact-complex-predictor.md` at checkpoint
`bbfd1086b7e629375f9891998e4602270d8801cd`.

The polynomial-degree argument is elementary and standard. No priority
claim is made. Its use here identifies a precise limitation on attempts to
reach the endpoint by changing the predictor's linearization alone.

## 1. Exact degree of parity on a Hamming band

Let `K` be a nonzero commutative ring in which two is a unit. This includes
characteristic-zero fields, odd-characteristic fields, and the source's
finite free scalar extensions. Merely requiring characteristic different
from two would not suffice: over `Z/4Z`, parity is the degree-one function
`1-2 sum_i b_i`.

For binary variables `b_1,...,b_m`, put `c=sum_i b_i`. Let
`0<=u<=v<=m`, and write `D=v-u`.

**Theorem W1.** The least total degree of a polynomial over `K` agreeing
with `(-1)^c` at every Boolean input with `u<=c<=v` is exactly `D`.

For the lower bound, fix `u` coordinates to one and `m-v` coordinates
to zero. Leave the remaining `D` coordinates free. This entire Boolean
subcube lies in the prescribed band. On it the desired function is

\[
 (-1)^u\prod_{i=1}^D(1-2b_i).
\]

Its unique multilinear representative has top coefficient
`(-1)^u(-2)^D`, a nonzero unit. Multilinearization by `b_i^2=b_i`
never raises degree. Uniqueness holds over any commutative ring: recover
the coefficients successively from evaluations on subsets, or use the
unit-triangular Boolean evaluation matrix. Therefore a polynomial of
degree less than `D` cannot agree on this subcube.

For the matching upper bound, use the source's integer polynomial

\[
 P(b)=(-1)^u\sum_{h=0}^{D}(-2)^h
 [T^h](1+T)^{-u}\prod_{i=1}^m(1+b_iT).
 \tag{W1}
\]

The coefficient of `T^h` has degree at most `h` in the Boolean variables.
At an input of count `c`, it is the integer `binom(c-u,h)`. In the band,
`0<=c-u<=D`, so the binomial theorem gives `P(b)=(-1)^c`.
All coefficients in (W1) are integers. This proof specializes to odd
characteristic even when `D!` is not invertible. Thus the source's
multivariate integral predictor is degree-optimal for its exact window.

## 2. Arbitrary row enlargement does not reduce this depth

The binary queries are commuting involutions `Q_1,...,Q_m` with all
`2^m` joint sign patterns present. The source's positive-width swaps
satisfy this condition by choosing a two-element orbit in each pair.

Consider a linear program built from affine query pencils

\[
 L_a=A_{a,0}\otimes I+\sum_{j=1}^m A_{a,j}\otimes Q_j
\]

and arbitrary query-independent linear maps on its row registers.
Allow any finite number of additional rows, copies and sums. The depth
`t` is the largest number of pencil applications on an input-output
path. No spectral table or other query-dependent oracle is allowed
inside this predictor program.

At a joint sign pattern `q=(q_1,...,q_m)`, each matrix entry of the
computed map is a polynomial of total degree at most `t` in the signs.
This follows by induction: row-only maps and addition preserve degree;
an affine pencil raises it by at most one. For a prescribed shift
`beta`, substitute `q_j=(-1)^beta_j(1-2b_j)`, which also cannot raise
degree.

Suppose one diagonal input-output coefficient must predict the product
sign correctly whenever `u<=|beta XOR k|<=v`. Taking that one input
row nonzero and all other independent inputs zero isolates this
coefficient. Theorem W1 yields

\[
                         t\ge v-u. \tag{W2}
\]

The bound does not depend on matrix dimension, tensor enlargement,
the number of labels, or the scalar extension. It applies in particular
to a full-rate diagonal predictor `P_beta I`. A more complicated
linearization cannot reduce the depth below the window width. The
source's next-power-of-two matrix root has depth below `2D` when
`D>=2`; S002's characteristic-zero real factorization has depth `D`.
Their depths are therefore already optimal up to the stated factor.

This reasoning is about the predictor before repair. Query-dependent
spectral tables, a changed error promise, nonlinear operations or a new
repair protocol are not contained in its hypotheses.

## 3. The source's window forces a square-root logarithmic excess

For the binary source construction, let

\[
 r=\lceil\log_2(2m)\rceil,\qquad
 B=\lceil\sqrt{2mr}\rceil.
\]

Clamp its integer endpoints to the actual count range:

\[
 u=\max(0,\lfloor m/2-B\rfloor),\quad
 v=\min(m,\lceil m/2+B\rceil),\quad D=v-u.
\]

Clamping matters for small `m`. For example, when `m>=32r`, the
endpoints are unclamped and

\[
 2\sqrt{2mr}\le D\le2\sqrt{2mr}+3.
 \tag{W3}
\]

The predictor must consequently use

\[
 t/\sqrt m\ge2\sqrt{2\lceil\log_2(2m)\rceil}.
\]

The source's `sqrt(log m)` depth factor is thus inherent in its exact
vanishing-error window. A smaller matrix representation could greatly
reduce row count, coefficient preparation and interpreter cost, but
cannot remove this particular factor while retaining that window and
affine-pencil interface.

Turning this depth statement into a recursive-call or tape-time lower
bound requires a separate per-stage invoice. In particular, this note
does not assume without proof that every pencil stage costs at least
one recursive call per input row. Under such an invoice with uniform
positive cost per stage, the window alone precludes a main-call mass
`sqrt(m)(1+o(1))`. Without that additional premise, (W2)--(W3) remain
algebraic depth bounds only.
