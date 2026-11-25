# Review of C's nonstationary literal-invoice barrier

Decision: **accepted in its stated positive-invoice scope**. A read
`../route-c/NONSTATIONARY-LITERAL-INVOICE-BARRIER.md` and its complete
checker, then replayed an isolated copy. A independently reached the
same obstruction in `nonstationary-invoice-barrier.md`; the two notes
are convergent derivations and are credited as one finding.

NI-L's cases are valid. For x>=2^24, either log I>=x^(3/4), which already
dominates g(x)/16, or J=x/log I>x^(1/4)>=64. Substituting this actual J
into the accepted nested theorem gives the displayed cubic inequality.
The smaller finite-x range follows from D>=2 and g(2^24)<2^18. This uses
the actual-rank invoice and does not quietly impose rank occupancy.

The concavity calculation is exact. With L=ln(x+2), multiplying f''/f by
9x^2(x+2)^2 L^2 gives

    -2(x+2)^2 L^2+x(x+8)L-2x^2.

Its discriminant is -3x^3(5x+16), so it is negative for every x>0.
Concavity and g(0)=0 imply the stated finite-sum subadditivity. A's
shorter proof needs only the decreasing ratio g(x)/x; C's stronger
concavity assertion also checks.

NI-P correctly distinguishes a product of pencil invoices from the
normalized time multiplier. Its regular split and coefficient condition
give Lambda sqrt(e_child/e_parent)>=I, so the product bound transfers to
the declared positive invoice certificate. The current source split has
f>=e/(6m) once ell<=e/4, m+2a<=3m and e/(m+2a)>=4; the floor loss is
therefore paid. The source's literal 8D_pred Rpen coefficient exceeds the
required square-root constant. The fast-descent example correctly shows
why a log-width decrement upper bound alone would be insufficient.

The replay command from programme root was:

    python3 -I -B research/moonshot-overhead-program/sessions/2026-11-26-S003/route-a/verify_independent_invoice_barrier.py

It passed 2,048 exact discriminants, 489 local cubic contrapositions, 160
normalized-price cases, 160 nonstationary partitions and three negative
controls. Output is `nonstationary-invoice-barrier-verification.json` in
this directory. Decimal tests are finite evidence, not interval-certified
calculus or a tape execution.

The conclusion is appropriately limited to the literal positive invoice.
It is not a lower bound on actual algorithm time or multiplication, and
does not rule out charging the same geometric implementation more sharply.
This is AI-assisted independent review, not formal or human certification.
