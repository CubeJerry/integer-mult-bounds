# Cross-review of Route B's independent count-aliasing argument

Status: **passed within its stated scope**. This is an independent agent
review, not independent human review or formal-kernel certification.

Reviewed file: `routes/B/count-aliasing-obstruction.md`, SHA-256
`760bcc7c6edfa24e197d657709ff839d23930db50057f769a33bc074652f406f`.
Later changes need delta review.

The central-window collision, the exact optimum
`1/2 + (1/2) sum_r |P_r-P_(r+p)|`, and the Fourier/Parseval proof were
checked independently. The normalization is correct: on p residues the
squared difference norm is `(1/p) sum_(h odd) |lambda_h|^(2m)`. Bounding
all p terms by the largest one, then using Cauchy--Schwarz, gives precisely
the stated `sqrt(p)/2` advantage. The exponential relaxation and necessary
parameter inequality (N) have the correct directions and constants.

The row-weighted shift averaging is also valid and does not require a large
or uniform shift family. A field extension preserves count residues, so it
does not remove the obstruction. The proof concerns functions of the scalar
count; integral multivariate divided-power representations remain outside it.
When `F_p` denotes a field, p is an odd prime as required by the source;
the cyclic-distribution calculation itself works for any odd integer modulus.

Route C obtained the same Parseval approach independently and retained the
full spectrum instead of bounding it by p copies of its largest term. This
gives the sharper bound in `INTERCHANGE-COUNT-OBSTRUCTION.md`:

\[
 \Delta^2\le\frac{2e^{-a}}{1-e^{-8a}},\qquad
 a=\pi^2m/(4p^2).
\]

The two arguments are compatible. Route B's simpler bound is enough for
fixed-p asymptotics. The sharper form proves failure greater than one quarter
already at `m>=p^2`, which combines with the new rational-Gram rank bound to
exclude ordinary-count predictors at *every* parameter choice satisfying
the published sublinear reserve contraction.

The shared Parseval insight should retain independent Route B and Route C
provenance. Neither note originates the source predictor or the general
finite-cycle Fourier method. The combined source-specific Gram consequence
is a further programme result.

Route C's exact verifier computes the same optimum by integer binomial
residue sums, exhausts all residue-sign functions at p=3,5,7 for its listed
inputs, and checks the stronger one-quarter consequence. Its final run
passed; no separate Route B aliasing verifier was available at the time of
this review, so no such rerun is claimed.
