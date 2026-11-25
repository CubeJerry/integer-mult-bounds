# Independent review of the numerical positive-invoice frontier

Gate: **PASS for the scoped analytic theorem**, with the harmless
constant-normalization clarification below for its matching upper
certificate. This is not a lower bound on the numerical routine or
integer multiplication.

Reviewed lead `numerical-invoice-frontier.md`, SHA-256
`dd6f6475b0dd3f349f021e4929fa75331bd27f7532aa299e0dc429f8d0256d08`.

## 1. Lower theorem

For the specified positive recurrence expansion, `B=log_2 C` is at
least `a max z_i` and at least `b sum g(z_i)`. Both inequalities
use explicitly nonnegative charges, not lower bounds inferred from an
algorithmic upper estimate.

The derivative of `log(z+2)/z` has the sign of
`z/(z+2)-ln(z+2)`, which is negative for z>=1. Consequently

\[
\sum_i\sqrt{z_i\log_2(z_i+2)}
\ge\left(\sum_i z_i\right)
       \sqrt{\log_2(Z+2)/Z},\quad Z=\max_i z_i.
\]

At `P=Y^(2/3)(log_2(Y+2))^(1/3)`, either Z>=P pays aP
locally, or the decreasing ratio gives an accumulated charge at least
a fixed multiple of `Y sqrt(log(P+2)/P)=Theta(P)`. This proves
NI3 for every sequence admitted by NI1, including very uneven ones.
No differential ansatz for the arity schedule is assumed.

## 2. Matching certificate and a constant clarification

To cover the stated arbitrary fixed c0>0, partition
`ceil(max(1,c0)Y)` rather than only Y into parts of size ceil(P)
and one positive remainder. The latter literal choice in the draft is
automatically admissible only when c0<=1. This fixed rescaling changes
no rate. The number of parts is O(Y/P), their total g-charge is
O((Y/P)g(P))=O(P), and every local charge is O(P). The logarithm
of the number of positive terms is O(log Y), also absorbed in P.
Thus the sharpness assertion is correct with this explicit normalization.

The same fixed rescaling applies to the general-kernel matching upper
certificate below. The current physical chain permits a small c0, so the
clarification has no effect on its application or positive theorem.

## 3. General kernel scale

For `0<=nu<1`, `mu>=0`,
`g(z)=z^nu(log_2(z+2))^mu` is nondecreasing, and g(z)/z is
eventually decreasing. Its bounded initial interval has positive minimum.
Therefore for z<=Z*, it is at least a fixed multiple of g(Z*)/Z*.
With

\[
Z^*=Y^{1/(2-\nu)}(\log_2(Y+2))^{\mu/(2-\nu)},
\]

one has `Y g(Z*)/Z*=Theta(Z*)`. The same max-versus-sum argument
proves the lower scale. Since nu<1 is fixed, Z*=o(Y), even after
the fixed logarithmic power. Equal-sized parts give the matching upper
scale; the final remainder and log(number of terms) are lower order.
The boundary case nu=mu=0 gives sqrt(Y) and is covered by the proof.

## 4. Scope and relevance

The actual numerical width chain has `a/(2A)<=f<=a/A` above the
fixed base and A=Theta(m), so each logarithmic width reduction is at
most C log m. Summation supplies NI1. The note correctly does not infer
this from an upper child-width estimate alone.

The retained numerical upper proof elects to charge an unattenuated
polynomial-m local coefficient after normalization by sqrt(a), and a
positive kernel excess of the displayed square-root-log form. NI2
captures that chosen invoice. Merely having upper bounds for those
operations would not force these charges in every implementation; the
note makes the distinction explicit.

The exact-interchanger recurrence is correctly excluded: its ordinary
polynomial-m local work is divided by sqrt(u), so it can be bounded with
polynomial arity and does not supply NI2's local lower charge. The theorem
therefore identifies an independent numerical certificate limitation,
without claiming the same obstruction for exact interchange or for all
possible numerical processors.

This is consistent with the new rectangle-volume observation: improving
the exact geometry alone does not automatically remove the numerical
polynomial-local/kernel balance. A sharper source-operation invoice,
shared query routing, another kernel or another normalization can still
escape. Neither this theorem nor its generalization is a runtime lower
bound or evidence against the exact square-root endpoint.

Credits: @CubeJerry; the source numerical kernel and E002 two-tier
construction; the lead's analytic theorem; substantial ChatGPT
multi-agent assistance. This is a written mathematical review, not formal
verification or full-machine execution.

The narrow sharpness normalization amendment is accepted at SHA-256
`c4307ffa11b6401e79b2b1f4ba65653104ccd2d1906076bc925af7e3f4fde3d8`.
It partitions `ceil(max(1,c0)Y)` as requested. No other mathematical
change is included in this amendment receipt.
