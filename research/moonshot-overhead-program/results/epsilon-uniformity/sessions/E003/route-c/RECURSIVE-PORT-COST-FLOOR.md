# A positive normalized floor for the retained recursive converter invoice

Status: **proved restricted recursive-invoice obstruction; independent review pending**.
This is not a lower bound for tape movement, interchange, or multiplication.

The previous matrix-rank theorem rules out removing the square-root
logarithm while retaining the literal linear cost of every full-row
conversion. The programme already avoids that price by recursively using
its order-three target in the converters. This note addresses that changed
invoice directly. It shows that arbitrary low-degree matrix predictors and
variable finite repair depths cannot make the retained converter's local
normalized stage invoice tend to one.

## 1. Exact model

Fix `m>=1` and the same independent local eigenvalues as in Theorem M1 of
`MATRIX-PREDICTION-RANK-BARRIER.md`. A node transforms `W` independent
rows by the target `f I_W` or its inverse. Its local program has ordinary
affine-query stages and spectral ports, as in that theorem. Let `t` be
the maximum affine-query degree of the input-output map after all spectral
ports have been replaced by zero. The node's nonrecursive stage invoice is
at least `Wt`. This is an explicit full-batch stage pricing assumption.
Pencils on smaller subsets are not silently priced as full-batch stages.

If its port dimensions are `h_1,...,h_s`, each dimension is charged for
`q` sequential recursive applications of the same target or its inverse
on `h_r` rows. All children have the same `m` local queries. Their inputs
may be correlated: full-rate correctness on arbitrary inputs is retained.
Finite leaves compute the target without ports, so their degree and stage
invoice are at least `m` per row. Every branch terminates after finitely
many repair nodes. Other expenses are nonnegative and may be added.

For the order-three word in
`routes/B/characteristic-two-order-three-interchange.md`, equations
O3-3 and O3-6a, `q=4`: a table on h rows has two target transforms in its
forward converter and two in its inverse. The elementary proof below
allows arbitrary table coefficients and widths and does not assume the
source's particular window, Hermite polynomial or two predictor passes.
Removing those extra assumptions only makes this invoice more favorable.

Write `C_m(W)` for the total number of row-stages charged by any such
finite repair tree. Retain

    delta_m(t)=2^-m sum_(j<=floor((m-t-1)/2)) binom(m,j)

for `0<=t<m`, and set it to zero when `t>=m`.
M3 gives `sum_r h_r >= W delta_m(t)` at every node. Inverse targets
obey the same theorem because inverse local eigenvalues are also distinct
and nonzero.

## 2. A finite explicit bound for the four-transform converter

**Theorem R1.** In the model above with `q=4`, for every integer
`m>=4096`, every batch size W and every finite repair tree,

    C_m(W) >= (6/5) W sqrt(m).                              (R1)

The predictor depths and table dimensions may vary from node to node.

### Binomial estimate

Let `M_m=max_j 2^-m binom(m,j)`. For every `m>=1`,

    M_m <= sqrt(2/(3m)).                                    (R2)

For even `m=2v`, put `a_v=binom(2v,v)/4^v`. Induction gives
`a_v<=1/sqrt(3v+1)`: it is exact for v=0, and

    ((2v+1)/(2v+2))^2 <= (3v+1)/(3v+4)

because the cross-multiplied right numerator exceeds the left numerator
by v. For odd `m=2v+1`,
`M_m=((2v+1)/(2v+2)) a_v`; squaring and cross-multiplying gives
the same weaker R2. Directly, the needed difference is
`10v^2+11v+5/2>=0`. The case m=1 also satisfies R2.

By binomial symmetry, the missing mass between the central half and the
cutoff for `delta_m(t)` is at most `(t+1)M_m/2`. This handles both parities
and integer rounding. Hence

    delta_m(t) >= 1/2-(t+1)/sqrt(6m).                        (R3)

### A subsolution inequality

Put `A=6/5` and `c=4/sqrt(6)`. For every `t>=0` and `m>=4096`,

    t+4 A sqrt(m) delta_m(t) >= A sqrt(m).                  (R4)

If `t>=A sqrt(m)` this is immediate. Otherwise put `r=t/sqrt(m)`.
Using R3, the left side divided by `sqrt(m)`, minus A, is at least

    A+r(1-cA)-cA/sqrt(m)
      >= A(2-cA-c/sqrt(m)) > 0.

Here `1-cA<0`, so the minimum on `0<=r<=A` is at its right endpoint.
For the final strict inequality, `1/sqrt(m)<=1/64` and

    c(A+1/64) = 4*(389/320)/sqrt(6) < 2,

since `(389/160)^2=151321/25600 < 6`.

### Tree induction

A leaf costs at least `mW>=A sqrt(m)W`. Suppose the bound holds for all
children of an internal node. Its total invoice is at least

    Wt + q A sqrt(m) sum_r h_r
      >= W[t+4 A sqrt(m) delta_m(t)]
      >= A sqrt(m)W,

by M3 and R4. Induction over the finite tree proves R1. No infinite
same-size recursion, fixed depth or common predictor is assumed. QED.

## 3. The sharp asymptotic potential supplied by the rank bound

Let `Q(c)=Pr[Z>=c]` for a standard normal random variable and
`phi(c)=exp(-c^2/2)/sqrt(2pi)`. For fixed integer `q>2` define

    Lambda_q = inf_(c>=0: q Q(c)<1) c/(1-q Q(c)).             (R5)

**Theorem R2.** Under the same invoice model,

    liminf_(m->infinity) inf_(W, finite trees)
      C_m(W)/(W sqrt(m)) >= Lambda_q.                       (R6)

This is the best asymptotic scalar potential obtained from M3 alone;
it is not an assertion that any actual predictor achieves it.

To prove R6, fix `0<A<Lambda_q`. The elementary de Moivre--Laplace
limit, uniformly for c in a compact interval, gives

    delta_m(floor(c sqrt(m))) -> Q(c).                     (R7)

One may obtain this form by the central-binomial ratio expansion and
Riemann sums: for `j=O(sqrt m)`, mode-relative mass is
`exp(-2j^2/m+o(1))`, uniformly on each fixed scaled interval; the mode
mass is asymptotic to `sqrt(2/(pi m))`. Chebyshev bounds remove the
tails. The integer cutoff changes the scaled endpoint by `O(m^-1/2)`.

For every `0<=c<=A`, the function `c+q A Q(c)-A` is strictly positive.
When `qQ(c)>=1` this follows from c>0, and at c=0 it follows from q>2.
Otherwise it is equivalent to `A<c/(1-qQ(c))`, which is R5. Compactness
gives a positive minimum. By R7, for all sufficiently large m,

    t+q A sqrt(m) delta_m(t) >= A sqrt(m)

for every integer `0<=t<=A sqrt(m)`. Larger t are immediate. Apply the
same finite-tree induction as before, then let A increase to `Lambda_q`.

For characterization, `qQ(c)` decreases continuously from q/2 to zero.
On its feasible interval the derivative of the ratio in R5 has numerator

    g(c)=1-q[Q(c)+c phi(c)],   g'(c)=q c^2 phi(c)>0.

It has exactly one zero `c_q`, lying beyond the point where `qQ(c)=1`.
The ratio tends to infinity at both ends of the feasible interval, so

    q[Q(c_q)+c_q phi(c_q)]=1,
    Lambda_q=1/(q phi(c_q)).                               (R8)

These equations define the constant exactly. Any decimal values in the
finite verification receipt are diagnostics, not inputs to R1 or R2.

## 4. What the obstruction changes

The source's recursive constant-tail correction removes the earlier
`sqrt(log m)` local overhead; R1 does not contest that. It proves that
the unchanged four-transform converter and full-batch stage invoice
retain a fixed loss above the normalized root scale, even if the
predictor is nonsymmetric, the row mixing is arbitrary and its repair
parameters change at every finite node. Tuning only the window or the
table dimensions therefore cannot make this model's local normalized
coefficient tend to one.

To transfer this into a spatial-recursion obstruction one would need a
separate proof that a full-batch pencil stage incurs at least the stated
unit of smaller-swap call cost, and a correct composition rule for those
invoices. The tape paper's upper-bound shared-pencil invoice alone does
not supply that lower bound. Consequently this note makes no claim that
the true runtime of its algorithm has this normalized floor.

Changing the converter word, allowing a genuinely cheaper rank-sensitive
second predictor application, sharing work across spatial levels, or a
different representation is outside the model. Endpoint proofs using
bounded spatial depth also need their own setup/threshold analysis;
R1 by itself does not rule them out.

Open next question: can one implement a full spectral port with fewer
than four complete target-transform applications, or retain a shared
intermediate conversion across several correction phases? That is an
explicit mechanism change capable of invalidating the invoice premise.

Credits: the OpenAI spectral-port interface, the programme's characteristic-two
order-three words, the degree/rank methods credited in M1--M4, Jerry Chen
(@CubeJerry), and AI-assisted E003 proof development. No full tape execution,
human refereeing or formal-kernel verification is claimed.
