# Independent audit of the monotone mixed-supplier gate

**Verdict: pass for Mono1–Mono3 and the sharp product count.** This is
the stated fixed nonnegative bilinear model, not a general multiplication
or tape-time lower bound.

One-hot inputs force each expanded coefficient to be in [0,1] on the
correct antidiagonal and zero everywhere else. Every used nonnegative
product has rectangular support. Without cancellation a nonempty rectangle
contained in one antidiagonal must be a singleton, and a shared product
cannot serve two different output indices. Thus actual products, rather
than unrelated output matrix ranks, pay for every positive monomial.

At the all-U input an absent coefficient causes residual at least U^2,
which is an outlier because M<=U^2. All monomials in each nonexceptional
output therefore require products. The S largest antidiagonal lengths
sum to Sh-floor(S^2/4), giving the displayed lower bound. Omitting those
S entire outputs attains it on every input, with nonnegative error.
Fractional positive coefficients cannot reduce the product count.

The threshold and sign exclusions are necessary. A larger threshold can
make the zero candidate valid even at S=0. Signed intermediate forms
can cancel unsupported rectangle entries, and nonlinear rounding needs
a separate model. The draft correctly retains all these qualifications
and credits the classical monotone convolution argument.

An isolated replay in `replay-monotone-mixed/` passes 66,066 zero-one
subcandidates, 21,343 support rectangles, 4,160 extremal sums, 162
fractional candidate bounds at 2,592 corners, and 256 signed-cancellation
controls, with the explicit large-threshold counterexample. No physical
runtime inference beyond the stated separately executed products is made.
