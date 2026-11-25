# Independent lead review of the coupled Walsh invoice barrier

Disposition: **accept the abstract equality-invoice theorem W1 and its
general tradeoff W8**, with the stated positive normalized routing-toll
and literal local-loss premises. This is not a runtime lower bound.

The lead read `../route-b/WALSH-TOLL-INVOICE-BARRIER.md` in full and
independently checked the following argument. For a nonnegative
normalized invoice, every prefix multiplier is at least one. Thus its
logarithm H simultaneously dominates the largest logarithmic arity toll
`kappa max z_i` and the sum of local logarithmic losses
`c_l sum sqrt(z_i log2(z_i+2))`. Rounded width progress gives
`sum z_i >= (log2(a_0)-log2(E))/(1+c_w)`. These bounds apply to one
and the same invoice, with no interchange of a minimum and maximum.

Since `log2(z+2)/z` decreases for positive z, capping every z_i by
H/kappa yields

    H^3 >= c_l^2 kappa (sum z_i)^2 log2(H/kappa+2).

The first polynomial lower estimate for H makes the logarithm on the
right comparable to log2(log2(a_0)+2). Substitution proves the two-thirds
scale. The bounded roots and empty chain require the written additive
constant; they are not silently dropped. The least-cost continuation
argument also covers different policies in equal-width children, because
their positive coefficients sum to the same mu_i. It does not cover
arbitrary mixtures of successor widths.

For W8 the same cap gives
`H^(2-alpha) >= c y (log2(H+2))^beta`. With fixed alpha<1 and beta>=0,
an initial positive-power lower estimate and a second substitution give
the claimed exponents. Eventual monotonicity and the bounded initial
range are explicitly premises. The g=1 specialization indeed yields
a square-root logarithmic-certificate floor; it is not polynomial
overhead in the active logarithmic width.

## Source applicability and limitation

The lead's separate `binary-walsh-label-invoice-barrier.md` derives an
exact binary Gram rank, exact canonical odd-support rectangle incidence,
and a nonzero highest Newton coefficient. Those prove a lower bound on
a specified positive **local invoice**, rather than reversing the known
upper estimate. Its independent source-normalization review is separate.

W1 additionally needs a retained toll proportional to
`sqrt(a) m^kappa`, with a fixed positive kappa, after normalization by
active width. Ordinary m^C scalar work per payload volume does not imply
that premise. Nor does an upper bound of that form on a physical executor
imply a lower bound on the executor's true work. The theorem applies to
the equality certificate that deliberately retains those charges.
Sharing middle-coordinate routing, changing the finite label mechanism,
or a different width interface can invalidate its premises and remain
legitimate research routes. No change to the programme's admitted H or
kappa_ov follows from this obstruction alone.

Review type: independent AI-assisted written mathematical check. No new
finite test is required for this short real-variable implication, and
none is claimed. Exact finite checks for the separate binary label
supplier are recorded in its own receipt. No human or formal review.
