# Independent review of the literal variable-arity invoice barrier

Gate: **PASS for the stated scoped certificate theorem**, including the
application and limitations section. This is not a lower bound on an
interchanger, multiplication algorithm, or the exact endpoint problem.

Reviewed: lead `variable-invoice-barrier.md`, with the literal rank guard
and incidence majorant inherited from the pinned geometry. The proof uses
no assumption of minimal t or power-of-two d.

## Local minimization

From the rank guard, `t>=z/d^2+2-2/d^2`. The elementary binomial
product gives `log_2 binom(2d-1,d)>=d-1`, and
`log_2(2^t-1)>=t-1`. Therefore the displayed lower bound

\[
\log_2\lambda\ge(3/4)d^2+z/d+(d^2/2)\log_2 t
\]

is valid for d>=2. The three-way partition is correct. For
`a=(z/log z)^(1/3)`, d<=a makes z/d at least
`z^(2/3)(log z)^(1/3)`. For
`b=z^(1/3)(log z)^(1/6)`, d>=b gives the same scale from
`(3/4)d^2`. In the middle interval, `t>=z/b^2` implies
`log t>=log z/6` eventually, while d>a. The last term is then at
least `z^(2/3)(log z)^(1/3)/12`. This proves VB2 with a fixed
positive constant and finite threshold.

The constructive upper estimate for `D(1+lambda)` at
`d=Theta((z/log z)^(1/3))` is the retained uniform geometry bound.
Thus the lower estimate matches the order of this *literal majorant*,
without asserting that the actual incidence count attains it.

## Variable-scale accumulation

For z above a fixed constant, `Phi(z)/z` is within fixed factors of
`(log z/z)^(1/3)`, which is decreasing for z>e. On the bounded
initial interval the ratio has positive minimum. Consequently for all
`1<=z<=C1 Y`, it is at least a fixed multiple of `Phi(Y)/Y`.
Summing and using `sum z_i>=c1 Y` proves VB5. The fixed factor C1
affects only its constant.

The application correctly demands a *lower charged factor* in the chosen
certificate. An upper bound on actual recursive mass alone would not
force that factor; the note explicitly says so. Its width warning is
also correct: an upper child-width estimate cannot establish a lower
bound on total logarithmic arity consumption.

For the actual composite-radix chain, the checked two-sided estimates
give `log u_i-log u_(i+1)=log m_i+O(1)`. Its O(log log U) spatial
depth and bounded/polylogarithmic terminal width imply
`sum log m_i=log U+O(log log U)`. This verifies VB4 for the stated
E002 schedule. More generally, the lower width bound alone yields
`Delta log u<=log m+2<=3log m` when m>=2, which already supplies
the needed lower sum until a subpower terminal width; geometric depth
is useful for the stronger two-sided asymptotic stated in the note.

The conclusion therefore concerns the certificate formed by multiplying
these literal normalized majorants. It does not prevent a sharper true
delivery bill, fewer actual incidences, a different rank guard, another
geometry, cancellation or another architecture. The proposed next target
is appropriately a change in the local geometry/delivery certificate,
rather than an asserted algorithmic impossibility.

This barrier is independent of the positive multiplication proof and is
not used as a premise of it. The review is mathematical, not finite-test
or formal-verification evidence. Credits: @CubeJerry, the pinned source
geometry, Route A's scoped precursor, the lead's derivation, and
substantial ChatGPT multi-agent assistance.

Reviewed snapshot SHA-256:
`35e0b36509268e4785a64f18c9ea4535bf387c088d8fd95f08f7c2add9b85a69`.
