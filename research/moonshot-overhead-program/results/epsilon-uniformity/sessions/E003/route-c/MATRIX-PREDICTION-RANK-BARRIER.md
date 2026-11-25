# A matrix prediction and spectral-port barrier

Status: **proved in the stated algebraic/invoice model; independent review pending**.
No multiplication running-time lower bound or new complete upper bound follows.

This removes the count-symmetry, diagonal-output, complete-shift-family and
single-table restrictions of the earlier programme's prediction/repair
obstruction. The scalar parity degree/error phenomenon is classical
Razborov--Smolensky mathematics. The contribution here is a self-contained
matrix-rank formulation, its applicability to the characteristic-two
order-three construction, and the resulting source-specific port invoice.

## 1. Exact matrix theorem on a two-point product

Let `F` be any field, `m,W>=1`, and for each `i` choose distinct nonzero
`a_i,b_i in F`. For `x in {0,1}^m` put

    f(x)=product_i (a_i(1-x_i)+b_i x_i).

Let `P(x)` be a `W by W` matrix of polynomials, each of total degree at
most the integer `t`, where `0<=t<m`. Put

    k=floor((m-t-1)/2),
    B(m,k)=sum_(j=0)^k binom(m,j),
    delta_m(t)=2^(-m) B(m,k).

**Theorem M1.** With rank taken over `F`,

    sum_(x in {0,1}^m) rank(f(x) I_W-P(x)) >= W B(m,k).       (M1)

In particular some input has rank defect at least `W delta_m(t)`.
The number of independent rows and every off-diagonal entry of `P` are
unrestricted. This is an average-rank statement, not an inference that a
matrix with many nonzero diagonal entries must have high rank.

### Proof

Define field-valued weights

    alpha_i=a_i/(a_i-b_i),    beta_i=-b_i/(a_i-b_i).

They satisfy `alpha_i+beta_i=1`, are nonzero, and

    alpha_i/a_i+beta_i/b_i=0.                                (M2)

Let `E_mu` be the product weighted sum with weights `alpha_i,beta_i`
at `x_i=0,1`. These are algebraic weights; positivity or a probability
interpretation is not assumed. Put `z_i=x_i-beta_i` and
`phi_S=product_(i in S) z_i`. Then

    E_mu[z_i]=0,       E_mu[z_i^2]=alpha_i beta_i !=0.

Consequently the Gram matrix of the `B(m,k)` functions `phi_S`, `|S|<=k`,
is diagonal, with nonzero entry `product_(i in S) alpha_i beta_i`.
Call it `G`; it has full rank `B(m,k)` in every characteristic.

For any polynomial `r` of degree less than `m`,

    E_mu[f^(-1) r]=0.                                       (M3)

It is enough to check a monomial. Since its degree is below `m`, it
misses some variable, and that coordinate factor is zero by M2.

Set `Q(x)=I_W-f(x)^(-1)P(x)`. Since `t+2k<m`, M3 applies entrywise to
`P(x) phi_S(x) phi_T(x)` for every `|S|,|T|<=k`. Therefore the block
moment matrix is

    sum_x mu(x) v(x)v(x)^T tensor Q(x) = G tensor I_W,        (M4)

where `v(x)=(phi_S(x))_(|S|<=k)`. The right side has rank `W B(m,k)`.
Every summand on the left has rank at most `rank Q(x)`, because
`v(x)v(x)^T` has rank one. Subadditivity of rank gives M1, and multiplication
by the nonzero scalar `f(x)` leaves each rank unchanged. QED.

For `t>=m` define `delta_m(t)=0`; the resulting statement is trivial.
The hypotheses that the two local target values are distinct and nonzero
are essential. For example, characteristic-two `+1,-1` coincide, and the
target is constant. There is no such degeneration for `omega,omega^2`
in `F4`.

## 2. General local alphabets and affine-query depth

Let each local spectrum `S_i` be a finite set of at least two distinct
nonzero elements of `F`, and let the target be `f(q)=product_i q_i`.
An affine-query stage is a matrix

    A_0 + sum_i sum_l A_(i,l) psi_(i,l)(q_i),                 (M5)

where all row matrices are independent of the spectrum and each `psi`
is an arbitrary function of one local eigenvalue. Between stages permit
arbitrary spectrum-independent linear maps, arbitrary finite auxiliary
rows, copies and additions. The final input-output map has `W` independent
input and output rows. Define its depth as the greatest number of M5
stages on an input-output path. No arbitrary spectrum-dependent map is
included for free in M5.

**Corollary M2.** If the depth is at most `t`, then on every selected
two-point subcube of the local spectra the final matrix satisfies M1.
In particular some realized spectrum has normalized rank defect at least
`delta_m(t)`. Moreover, averaging uniformly over the entire product of
the `S_i` gives average normalized rank defect at least `delta_m(t)`.

Proof: on a two-point set every `psi` is an affine function of the
corresponding Boolean coordinate. Every final entry therefore has degree
at most `t`, by induction through the linear circuit. Apply M1. For the
last statement choose a uniformly random unordered pair in each `S_i`
and then a uniform endpoint of each pair. The resulting point is uniform
on the entire product, and averaging M1 proves the claim. QED.

Row-specific shifts, different predictors, arbitrary finite row widths
and nonsymmetric coefficient choices are included. A shift merely changes
the one-coordinate functions in M5. No shift distribution is assumed.

## 3. Multiple interacting spectral tables

The row-error count and matrix rank must be distinguished. If `P(q)` is
diagonal, its rank defect is exactly the number of wrong rows. For a
nondiagonal predictor the defect can be low rank even when every row is
wrong. The following theorem charges the appropriate rank capacity.

Consider a finite linear program on any finite live state. At each
spectrum it is a product of composable matrices, with fixed linear input
injection and output projection. At the r-th use of a spectral port,
write its state update as

    M_r(q)=A_r(q)+U_r(q) C_r(q) V_r(q),                     (M6)

where the added term factors through a space of dimension `h_r`.
The matrices involving the spectral port may depend arbitrarily on `q`.
Replace each added term by zero. Require that the remaining input-output
map `P_0(q)` is a depth-`t` affine-query program in the sense of Section 2.
All pencil stages on the surviving paths must be counted in this `t`.
The original program is required to output `f(q) I_W` at every spectrum.

**Theorem M3.** Such an exact program must have

    sum_r h_r/W >= delta_m(t).                              (M7)

Proof: telescoping the product of state updates, replacing one port at a
time, writes the output difference `fI-P_0` as a sum of terms, each
factoring through the corresponding `h_r`-dimensional port. Left and
right multiplication cannot increase rank, so its rank is at most
`sum_r h_r` at every spectrum. Corollary M2 supplies a spectrum at which
the rank is at least `W delta_m(t)`. QED.

For clarity, for square state matrices the underlying identity is

    M_s...M_1-A_s...A_1
      = sum_r M_s...M_(r+1) (M_r-A_r) A_(r-1)...A_1.

The same identity holds for composable rectangular maps. Injection,
projection, scratch registers and a feed-forward linear circuit can be
included in the state representation. Every port occurrence is charged;
using the same table repeatedly does not make those occurrences free.
This is not a theorem about data-dependent nonlinear control.

If the local port widths depend on `q`, the proof instead gives the
necessary average inequality

    E_q[sum_r h_r(q)]/W >= delta_m(t).                       (M8)

Consequently the worst-frequency total width satisfies M7 as well.
The lower bound does not claim that a port of the given width can always
repair an arbitrary defect; it is only a necessary capacity condition.

## 4. Quantitative source-invoice consequence

All logarithms in this section are natural. For any fixed `c>0`, let
`t_m=floor(c sqrt(m ln m))`. Then

    delta_m(t_m)=m^(-c^2/2+o(1)).                            (M9)

Here the `o(1)` is with fixed `c`. To verify M9, the threshold `k` is
`m/2-(c/2)sqrt(m ln m)+O(1)`. Chernoff's bound gives the upper exponent.
For the lower exponent, the mode mass is `Theta(m^(-1/2))`, and for
displacement `j=O(sqrt(m ln m))` its probability ratio to the mode is

    exp(-2j^2/m+O(j^3/m^2+j/m)).

Sum `floor(sqrt(m/ln m))` consecutive levels immediately below `k`.
The exponent changes by only `O(1)` over that band, giving a tail at least
`(ln m)^(-1/2) exp(-c^2 ln m/2+O(1))`. Odd m follows from one-bit
convolution, or the identical adjacent-ratio proof. This proves M9.
The programme's `routes/C/COUNT-PREDICTION-BARRIER.md`, Lemma C2, gives
the elementary central-mass and adjacent-ratio details independently.

Suppose the declared invoice charges one unit for each counted pencil
depth and `m^gamma` units per normalized spectral-port dimension. For
fixed `gamma>1/2`, define its value as

    I=t+m^gamma sum_r h_r/W.

**Corollary M4.** Every family in M3 satisfies

    liminf_(m->infinity) I/sqrt(m ln m) >= sqrt(2gamma-1).    (M10)

Proof: fix `0<c<sqrt(2gamma-1)`. If `t>=c sqrt(m ln m)` the depth alone
gives the claim with c. Otherwise monotonicity of `delta_m` and M7--M9
give port cost at least `m^(gamma-c^2/2+o(1))`, which dominates
`sqrt(m ln m)` because its exponent exceeds `1/2`. Take the lower limit
and then let c increase to the stated constant. QED.

At the source's literal full-row conversion price, `gamma=1`, this
invoice is at least `(1-o(1))sqrt(m ln m)`. In particular no `O(sqrt m)`
invoice is possible in this model. This statement applies to the entire
surviving query program after the spectral tables have been zeroed, not
automatically to the degree of the first predictor before Hermite repair.

For the binary source, one spectral table on `2s` rows has port dimension
`2s` and four-s full row conversions; their literal source charge is
`4ms`. The full program has at most four predictor applications. Thus
the model and its constant factors are directly checkable from Fourier
`build/repair.tex`, `lem:hermite-repair`, `thm:repair`, `cor:swap-repair`.
Charging `m` per port is weaker than that specified conversion invoice.
The source itself obtains `O(sqrt(m log m))` stages with smaller
conversion cost, so the order is sharp for this two-resource accounting.

The characteristic-two order-three gate also falls within the algebraic
theorem: on a nontrivial pair its eigenvalues in `F4` are
`omega,omega^2`, both distinct and nonzero. Independent pairs realize the
entire two-point product. The constant-tail *recursive* repair used by the
newer programme is not contradicted: it deliberately does not pay the
literal `m` price for each correction row. Its recursive cost must be
analyzed on its own terms.

## 5. Exact scope and consequences for research

The earlier source obstructions excluded arbitrary nonsymmetric predictors,
nondiagonal full-rate row mixing and interacting repair tables. M1--M4
show that these changes alone cannot evade the binomial depth/port
tradeoff, provided the surviving non-port computation has the stated
affine-query depth. The field may have characteristic two when the local
target eigenvalues remain distinct, so the order-three construction is
covered without a mistaken parity specialization.

The result does **not** lower-bound the cost of implementing a pencil,
prove that every tape algorithm incurs the declared conversion price,
or rule out a better repair recurrence. It does not bound the true
integer-multiplication overhead or the weighted scheduler's runtime.
It supplies no additional premise for an upper-bound theorem.

Open next questions:

1. Can the constant-tail recursive correction attain a normalized
   per-level mass approaching one, with all port costs and local tolls
   charged? M4 says why retaining the linear full-row price cannot do it.
2. Can endpoint layout changes be shared so that pencil depth no longer
   costs a fixed positive recursive-call amount per independent row?
   That would change the invoice premise rather than violate M1.
3. What stronger matrix-rank profile is available for ternary spectra?
   The two-point restriction is universal but does not use all three
   eigenvalues simultaneously.

## 6. Sources, prior art and verification limits

Source pin: OpenAI `math@3344da59991ed94f9ba711217b29c1d760badfa6`.
Read source chain: Fourier `build/repair.tex`, labels named above; tape
`build/interchange.tex`, `eq:interchange-pencil` and
`eq:interchange-stage-cost`; programme fixed-field and order-three notes
at starting programme head `a2d9c4b00c02dadf7bdc970acf9190dfabf9ec32`.
The finite source `4ms/W` call accounting is an upper-bound invoice for
that implementation, not a universal minimum time.

The scalar parity binomial-tail bound is classical: Roman Smolensky,
*On representations by low-degree polynomials*, FOCS 1993,
DOI `10.1109/SFCS.1993.366874`. An explicitly read expository treatment
is Yuval Filmus, *Smolensky's Lower Bound* (September 2010), Theorem 5.2
and Corollary 5.3,
<https://www.cs.toronto.edu/tss/files/papers/Smolensky.pdf>.
For related primary research and error-dependent MOD lower bounds see
Srinivasan, Tripathi and Venkitesh, *On the Probabilistic Degrees of
Symmetric Boolean Functions*, FSTTCS 2019, Lemmas 8--11,
<https://doi.org/10.4230/LIPIcs.FSTTCS.2019.28>.
No priority claim is made for the underlying degree-error principle.
The full proofs above do not depend on an unproved citation.

Credits: Jerry Chen (@CubeJerry), the OpenAI manuscript authors and their
predecessor sources, Razborov--Smolensky degree methods, and the programme's
earlier count/window analyses. This E003 extension and checks are
AI-assisted mathematics, not human refereeing or Lean certification.
