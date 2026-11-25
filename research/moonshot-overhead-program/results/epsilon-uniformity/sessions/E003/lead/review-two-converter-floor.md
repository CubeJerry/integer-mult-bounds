# Lead review of the patched two-converter port floor

Disposition: **accepted within the explicit recursive invoice model**.
Read the complete `../route-c/TWO-CONVERTER-PORT-FLOOR.md` and independently
checked its finite-degree cases. This does not assert a physical runtime
or multiplication lower bound. The lead suggested the degree-zero pairing;
Route C derived the exact parity-dependent optimum and verified it.

At t=0, pairing Boolean tuples differing in one coordinate makes the
two defect matrices differ by a nonzero scalar identity. Rank subadditivity
gives exactly W/2 mean defect, including even m. This repairs the raw
binomial tail's parity deficit. The spectral-port telescoping argument
then gives sum h>=W/2 for arbitrary row mixing.

For m=2v+1, degrees 2r-1 and 2r have the same omitted central sum.
The ratios t/(1-2delta) are bounded below by 1/(2M_m), with equality
at t=1. For m=2v, odd t has ratio at least 1/M_m; even t=2r has ratio
at least 2r/(M_m+2r p_(v-1)), increasing in r. The attained minimum
is therefore 2/(M_m+2p_(v-1)) at t=2, no larger than 1/M_m because
p_(v-1)/M_m=v/(v+1)>=1/2. The m=1 and m=2 boundary cases also fit.

These exact minima provide a common scalar subsolution for every node.
The corrected t=0 case has equality, so finite-tree induction does not
allow a fictitious free contracting branch. Direct leaves cost at least
mW and dominate the same potential. Changing among O5 target products
does not alter the argument: each retains distinct nonzero local values
on the two-point cube, and the rank theorem is uniform in those values.

The central-binomial estimate gives the stated uniform lower bound
sqrt(6)/4 times W sqrt(m). It is below one after root normalization;
it must not be called the earlier q=4 above-one floor. The exact odd/even
limits follow from the standard central-binomial asymptotic. A fixed
positive normal-tail scaling cannot find the active bounded degree t=1
or t=2, since its denominator vanishes at that endpoint. The stated
failure of blindly substituting q=2 into the earlier continuum formula
is therefore substantive and correct.

The floor is optimal only for the scalar relaxation based on these rank
bounds. It does not prove a predictor attains them. The O5 converted
check width is 2s, distinct from both defect cardinality and table rank;
the note correctly preserves those distinctions. Rank-sensitive or shared
converters could change the model. Route C's exact finite receipt is
supporting evidence; the lead's acceptance here is a written proof
review, not a claim to have independently rerun that full checker.

Credits: @CubeJerry; the matrix degree/rank and port telescoping proofs;
Route C's parity refinement and exact checks; the lead's zero-degree
repair; substantial AI-assisted review. No formal or human-referee claim.
