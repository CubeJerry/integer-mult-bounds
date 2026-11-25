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

## 4. Rebalancing the same window-marked repair does not remove the factor

There is a stronger two-resource statement if one keeps the source's
uniform use of all translated shifts and marks every row outside one
contiguous count window. At each fixed frequency the count then has
distribution `C~Binomial(m,1/2)`. Set

\[
 \delta=\Pr[C\notin[u,v]].
\]

On `R` independent rows with equal shift multiplicities, the marked
set has exactly `R delta` rows. A Hermite table sized to contain that
set has `s>=R delta`. The literal source conversion protocol performs
`4s` full-row conversions, each invoiced at `m` smaller swaps. Thus
its conversion invoice is at least `4m delta` per input row. This
counts the specified protocol; it does not prove that every possible
conversion or repair needs this many calls.

**Theorem W2.** For every sufficiently large `m` and every integer
window `[u,v]` in `[0,m]`,

\[
 (v-u)+m\Pr[C\notin[u,v]]
       \ge\frac1{16}\sqrt{m\ln m}. \tag{W4}
\]

One explicit conservative valid range for the proof below is `m>=2^512`.
Consequently the sum of pencil depth and the full-conversion invoice
cannot be `O(sqrt(m))` in this window-marked protocol. This is a
two-resource obstruction: either the predictor depth has the excess,
or the marked full-row conversions have a still larger cost.

### Proof without asymptotic normal approximations

Let `c=floor(m/2)` be a binomial mode. Chebyshev's inequality and
`Var(C)=m/4` put at least `3/4` of the probability in at most
`2 sqrt(m)+2` counts around `m/2`. Since a mode has maximal mass,

\[
 \Pr[C=c]\ge\frac{3}{16\sqrt m}. \tag{W5}
\]

For an integer `0<=t<=c/4`, compare consecutive probabilities:

\[
 \frac{\Pr[C=c+t]}{\Pr[C=c]}
 =\prod_{i=1}^t\frac{m-c-i+1}{c+i}
 \ge\exp\left(-\frac{6t(t+1)}m\right). \tag{W6}
\]

Indeed each ratio is at least `1-2i/c`; here `2i/c<=1/2` and
`ln(1-x)>=-2x` on `[0,1/2]`. Sum the logarithms and use
`c>=m/3`. A negative displacement of size `t` has the mass of a
positive displacement of size at most `t+1`, by binomial symmetry.

Write `D=v-u`. If `D>=sqrt(m ln m)/16`, (W4) is immediate.
Otherwise put `s=floor(sqrt(m))` and consider the two bands

\[
 \{c+D+1,\ldots,c+D+s\},\qquad
 \{c-D-s,\ldots,c-D-1\}.
\]

Their nearest points are more than `D` apart, so an interval of width
`D` cannot meet both. One entire band lies outside `[u,v]`. At the
stated range of `m`, both bands lie in `[0,m]`, their relevant mode
displacements satisfy the condition of (W6), and every required
`t(t+1)` is at most `(D+sqrt(m)+2)^2`. With `l=ln m>=256`,

\[
 \frac{6(D+\sqrt m+2)^2}{m}
 \le6(\sqrt l/16+2)^2\le l/4.
\]

For the last inequality, expand the square: it is enough that
`29l/128>=1.5 sqrt(l)+24`, which holds at `l=256` and increases
thereafter. The displacement condition follows, for example, from
`ln m<=sqrt(m)` and `m>=2^512`.

Each of the at least `sqrt(m)/2` outside-band counts has mass at
least `3 m^(-1/4)/(16 sqrt(m))`. Hence

\[
 \delta\ge\frac3{32}m^{-1/4},\qquad
 m\delta\ge\frac3{32}m^{3/4}
          \ge\frac1{16}\sqrt{m\ln m}.
\]

The last inequality again follows from `ln m<=sqrt(m)`. This proves
(W4). The large explicit cutoff simplifies constants; no numerical
normal approximation or uncomputed tail threshold enters the proof.

### Sharpness for this resource accounting

The source's window has `D=O(sqrt(m log m))` and
`delta<=1/(2m^3)`. Its original matrix-root predictor has at most
`2D` stages for large `m`. Therefore the resource quantity

\[
 \text{predictor depth}+m\delta
\]

is `O(sqrt(m log m))`. Together with (W2) and (W4), its optimal
order within this particular window-marked family is
`Theta(sqrt(m log m))`. Binary Hermite's four predictor applications
and four conversion batches change only constants in this comparison.

This conclusion allows one to rebalance the window arbitrarily; it is
not merely tied to the source's convenient error target `m^-3`.
It still requires all translated shifts with equal multiplicity,
marking the whole complement of the window, and the literal full-row
conversion bill. A smaller shift family with another count law,
fortuitous correctness outside the window combined with a smaller
marked set, or a new repair mechanism is outside the conclusion.

## 5. Consequence for the next endpoint attempt

The near-critical recurrence in `NONSTATIONARY-RECURSION.md` needs an
actual normalized child mass close enough to one that its excesses
are summable. Merely replacing the original large matrix root by a
more compact exact-window representation does not provide that mass:
the predictor depth remains as in (W3). The inference to mass is
conditional on the separate per-stage invoice described above.

S002's pairwise-independent constant-tail protocol changes the window
and the repair and is **not ruled out** by the window-marked resource
tradeoff. Its own conversion, division, precision, movement and space
costs must be evaluated under its changed interface. The literal
finite-characteristic lift barriers in the parent notes and S002's
complementary supported-transfer theorem concern a different resource;
they should not be added to this depth bound without a shared cost model.

The useful research decision is therefore precise: improve the row
representation to reduce constants, but an endpoint attempt must also
change the vanishing-error window/repair invoice, exploit cheaper
stage accounting with a proof, or supply another mechanism entirely.

Credits: the cited OpenAI predictor and repair constructions, S002 compact
prediction and constant-tail programme, and @CubeJerry. This application
and its elementary finite checks were developed with GPT-6 Astra Pro.

## Finite verification receipt

`check_window_depth.py` passes under `python3 -I -B`. It checks 10,625
integer band values, 5,310 nonzero odd-characteristic degree witnesses,
64 characteristic-four negative controls, 2,925 exact comparisons of
centered-window mass, and the source's integer tail budget at twelve
widths from two through 4,096. The adjacent JSON also gives illustrative
values of the optimized window resource functional. Those floating
values are not runtime measurements or proofs of the asymptotic lower
bound. The universal degree and resource theorems are proved above.

## Independent written review

On 2026-11-25 the lead independently reviewed the degree and window-resource proofs and found no blocker. The review checked the unit-of-two hypothesis, Boolean subcube, affine-query degree, source-window clamping, binomial mode mass, probability-ratio bound, two-band coverage and explicit large-`m` cutoff. The distinction between a predictor-depth bound, the specified window/repair resource invoice and an unconditional multiplication-time lower bound is retained throughout.
