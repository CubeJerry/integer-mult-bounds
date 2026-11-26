# Independent audit of the direct mixed-error predictor gates

**Verdict: pass for Mix1–Mix7 with the declared independence, record
encoding and fixed-bilinear hypotheses.** These gates address the mixed
promise directly and allow input-dependent outlier positions. They are
not unrestricted multiplication lower bounds.

Condition on all inputs except the designated missing coordinate. Its
two target values are separated by U, and the open good intervals have
width M<=U. At most one can contain the unchanged candidate. Averaging
gives outlier probability at least one half per coordinate and a single
input with at least ceil(N/2) outliers. The half-open one-sided intervals
also remain disjoint at M=U. No independence of outlier events is used.

The regular low-support-degree application is valid: no reduced monomial
with support below m has the full target shift. Constant row mixing
cannot create the missing coefficient of the designated input variable.
A decoder seeing only its predicted coordinate remains independent of
that variable. Access to other computed coordinates, a raw input, or a
multi-component record must satisfy the stronger stated independence
premise; the draft correctly avoids inferring it from one missing bit.

For the bilinear gate, the independent-sign expansion gives the second
moment lower bound, and two conditional affine fourth-moment bounds give
the factor nine, including constant and linear terms. If |F_i|>B+delta,
the rounded residual is an outlier. Splitting its second moment at that
radius and applying Cauchy–Schwarz yields Mix4. Summing probabilities
uses only the all-input outlier count, proving Mix5 despite adaptive
exceptional sets. The mu_i>=4R^2 threshold gives probability at least
1/16 exactly; the Frobenius threshold and rank-deficient-form constants
follow. The rank-distance proof via ker(G_i) intersected with H_i's
active column space is sound and requires no total-rank additivity.

The signed hybrid threshold B=M/2 and one-sided threshold B=M match the
two corrector promises, including the explicit rounding guard. The
conclusion remains a constraint on each fixed candidate's forms, with
no lower bound on shared bilinear rank or nonlinear adaptive suppliers.

An isolated replay in `replay-mixed-predictor-gates/` passes 8,160
missing-input corners, 256 adaptive-outlier bounds, 9,300 bilinear/rounding
values, 81 rank-distance controls, 225 second/fourth-moment checks,
658 strict-tail bounds, and 225 each of the energy and rank invoices.
The oversized-interval negative control is retained.
