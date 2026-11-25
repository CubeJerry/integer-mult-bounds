# What a fixed bilinear sparse-error supplier must already compute

Status: **proved scoped obstruction; independently audited by Route C and
the session lead**. This note
studies a possible supplier for the ordinary sparse-residual corrector in
`deterministic-sparse-residual-repair.md`. It proves no running-time lower
bound and supplies no new complete multiplication algorithm.

The exact and rounded statements have different conclusions. Exact
unrounded outputs have a fixed exceptional support under a sufficiently
large input grid. Rounding permits more flexibility, but the coefficient
matrices must already approximate almost all convolution forms to high
accuracy. Neither statement applies to an unrestricted adaptive nonlinear
candidate algorithm.

## 1. Setup

Let `h>=1`, let `D=2h`, and put

\[
 P_i(a,b)=\sum_{\substack{0\le j,k<h\\j+k=i}}a_jb_k
          =a^T H_i b,\qquad 0\le i<D.
\]

Here `H_i` has ones at positions `(j,k)` with `j+k=i` and zeroes elsewhere.
The final coefficient `P_(D-1)` is identically zero. A **fixed bilinear
candidate** is a collection

\[
 Q_i(a,b)=a^T G_i b
\]

of real matrices `G_i` chosen independently of the input values. Set
`F_i=P_i-Q_i=a^T M_i b`, where `M_i=H_i-G_i`. The candidate may have any
shared implementation; nothing below restricts its bilinear rank or
counts the arithmetic steps used to evaluate it.

## 2. Exact unrounded sparse error forces a fixed support

**Theorem S1.** Let `S` be a finite set of real numbers with
`|S|>=s+2`. Suppose that for every `a,b` in `S^h`, at most `s` of the
exact real numbers `F_i(a,b)` are nonzero. Then at most `s` of the
polynomials `F_i` are nonzero polynomials. In particular, there is a fixed
set of at most `s` output positions outside which `Q_i=P_i` identically.

### Proof

If `s+1` distinct errors `F_i` were nonzero polynomials, their product
would be nonzero because the real polynomial ring is an integral domain.
Each factor has degree at most one in each individual input variable.
Their product consequently has degree at most `s+1` in each variable.

A nonzero polynomial with individual degree below `|S|` cannot vanish on
the entire Cartesian grid `S^(2h)`. This elementary grid fact follows by
induction on the number of variables: expand in the final variable; at
least one coefficient polynomial remains nonzero on the smaller grid by
induction, leaving a nonzero univariate polynomial of degree below `|S|`.
It cannot have every element of `S` as a root.

There is therefore an input at which the product of the `s+1` errors is
nonzero. All those errors are nonzero on that input, contradicting the
hypothesis. QED.

For a `b`-bit digit grid this condition is `2^b>=s+2`. The conclusion
concerns **exact unrounded candidate values**. It does not say that a
rounded bilinear candidate has a fixed exceptional support. It also does
not say that computing all but a fixed small set of coefficients requires
the time of the best known multiplication algorithm.

**Optional rational form.** The same proof applies when the error values
are `F_i=N_i/Q`, the common denominator `Q` is nowhere zero on the input
grid, and every numerator `N_i` has individual variable degree at most
`d`: the sufficient grid condition is `|S|>d(s+1)`. The degree charged
here is that of the actual error numerator, including the contribution
from multiplying the target polynomial by `Q`. No denominator is free.

**Finite-field counterpart.** Over `F_q`, no large-grid condition is
needed for a constant-factor conclusion. A nonzero matrix `M` of rank
`r>=1` gives

\[
 \Pr_{a,b\in F_q^h}[a^TMb\ne0]
       =(1-q^{-r})(1-q^{-1})\ge(1-q^{-1})^2.
\]

Indeed, `a^TM` is zero with probability `q^-r`; otherwise its dot product
with uniform `b` is uniform in `F_q`. If a fixed bilinear candidate has
at most `s` wrong coefficients on every input, linearity of expectation
therefore bounds the number of its nonzero error forms by
`s/(1-1/q)^2`. This finite-field statement is separate from integer
rounding. The session lead supplied this extension.

## 3. A fourth-moment lemma for separately affine forms

Let `epsilon_1,...,epsilon_h` and `delta_1,...,delta_h` be mutually
independent uniform signs. Any polynomial `Z(epsilon,delta)` that is
affine in the epsilon block and affine in the delta block can be written

\[
 Z=c_0(\delta)+\sum_{j=1}^h c_j(\delta)\epsilon_j,
\]

where every `c_j` is affine in `delta`.

**Lemma S2.** Such a polynomial satisfies

\[
 \mathbb E Z^4\le9(\mathbb E Z^2)^2.                 \tag{S2}
\]

### Proof, including the constant

For constants `v_0,...,v_h`, direct expansion and cancellation of odd
sign moments give

\[
\begin{aligned}
 \mathbb E\left(v_0+\sum_jv_j\epsilon_j\right)^4
 &=v_0^4+6v_0^2\sum_jv_j^2
       +3\left(\sum_jv_j^2\right)^2-2\sum_jv_j^4\\
 &\le3\left(v_0^2+\sum_jv_j^2\right)^2.
\end{aligned}                                                    \tag{S3}
\]

Condition first on `delta`. By (S3), followed by Cauchy--Schwarz and
another use of (S3) for each affine function `c_j`,

\[
\begin{aligned}
 \mathbb E Z^4
 &\le3\sum_{j,k=0}^h\mathbb E(c_j^2c_k^2)\\
 &\le3\sum_{j,k=0}^h
          \sqrt{\mathbb E c_j^4\,\mathbb E c_k^4}\\
 &\le9\left(\sum_{j=0}^h\mathbb E c_j^2\right)^2
  =9(\mathbb E Z^2)^2.
\end{aligned}
\]

This proves the lemma. It uses no randomness assumption on the actual
inputs: the random signs will only witness the existence of a difficult
deterministic input.

## 4. Rounded sparse error requires accurate coefficient matrices

Take an integer `U>=2` permitted by the digit grid, and restrict inputs
to `a_j,b_k` in `{0,U}`. Let `round` denote any nearest-integer rule;
its behavior at half-integers can be arbitrary.

**Theorem S3.** Suppose that for every such input, at most `s` of the
rounded values `round(Q_i(a,b))` differ from the exact integers
`P_i(a,b)`. Then

\[
 \#\{i:\|H_i-G_i\|_F\ge4/U^2\}\le16s.             \tag{S4}
\]

Consequently, all but at most `16s` output coefficient matrices must be
within Frobenius distance `4/U^2` of their exact convolution matrices.

### Proof

Choose `a_j=U(1+epsilon_j)/2` and `b_k=U(1+delta_k)/2` with independent
uniform signs. In the orthogonal sign expansion of
`F_i=a^T M_i b`, the coefficient of `epsilon_j delta_k` is
`U^2 (M_i)_(j,k)/4`. Thus

\[
 \sigma_i^2:=\mathbb E F_i^2
      \ge U^4\|M_i\|_F^2/16.                       \tag{S5}
\]

If `||M_i||_F>=4/U^2`, then `mu:=sigma_i^2>=1`. Set `Y=F_i^2` and
`Bad={Y>1/4}`. Cauchy--Schwarz and Lemma S2 give

\[
 \mu\le\frac14+\mathbb E(Y\,1_{Bad})
       \le\frac14+\sqrt{\mathbb E Y^2\Pr(Bad)},
 \qquad \mathbb E Y^2\le9\mu^2.
\]

Consequently,

\[
 \Pr(Bad)\ge\frac{(\mu-1/4)^2}{9\mu^2}\ge\frac1{16}.       \tag{S6}
\]

On this strictly defined event `|F_i|>1/2`, rounding must be wrong at
output `i`, independently of the tie convention. If `r` matrices satisfy
the norm condition, the expected number of wrong outputs is at least
`r/16`, by linearity of expectation. The assumed worst-case bound is
`s`, so `r<=16s`. QED.

Here `sigma_i^2` is an uncentered second moment, not necessarily a
variance. Route C supplied the strict-event sharpening from the original
valid but weaker constant 36 to 16 during its independent audit.

The real-coefficient restriction in this theorem ensures that nearest
integer rounding and the ordinary fourth moments have their usual
meaning. It is an exact statement about the candidate values; extra
floating-point or finite-precision implementation errors need a separate
budget and do not enter the proof for free.

## 5. Consequence for reducing each output form's rank

The nonzero rows and columns of `H_i` form a partial permutation matrix.
Let `r_i=rank H_i`; all its `r_i` nonzero singular values equal one.
If `rank G_i<r_i`, choose a unit vector in the active column space of
`H_i` and in `ker G_i`. Such a vector exists by the dimension bound.
Its image under `H_i-G_i` has norm one. Therefore

\[
 \|H_i-G_i\|_F\ge\|H_i-G_i\|_{op}\ge1.             \tag{S7}
\]

Since `U>=2`, every such output is counted in (S4). Under Theorem S3's
sparse-error promise, at most `16s` coefficient forms can have lower
matrix rank than the exact forms.

This is a constraint on individual output forms, **not on the total
bilinear rank of a shared convolution algorithm**. Efficient algorithms
can share products among many full-rank output forms. The theorem does
not rule out such sharing, other nonlinear suppliers, data-dependent
branches, or a new algorithm computing every coefficient exactly.

## 6. Relation to the repair component

The sparse corrector can recover unknown ordinary errors for
`s<=2^((log n)^tau)`, fixed `tau<1`, in time below `n sqrt(log n)` in
the packed regime described in its own theorem. These gates explain a
remaining difficulty for one candidate supplier class. With exact fixed
bilinear outputs and a large enough digit grid, all exceptional outputs
must belong to a fixed small set. With rounded fixed bilinear outputs,
almost every coefficient matrix must already have error on the scale
`U^-2` or smaller. Neither conclusion provides a supplier or converts the
repair theorem into a complete multiplication bound.

The arguments are elementary grid nonvanishing, fourth-moment estimates,
and a dimension bound. They are recorded as a scoped application and
make no priority claim for those underlying methods.

Prepared for @CubeJerry with substantial ChatGPT assistance.
