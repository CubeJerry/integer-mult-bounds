# Independent audit of the one-shot fresh-body obstruction

**Pass for the explicitly restricted model. No new kappa.** Root reviewed the
source tag comparison, backwards deletion, two query-only bounds and invoice.
The ordinary body algebra must be the fixed finite collective tensor
translation algebra, or another explicitly verified algebra constant at the
constructed sign points. Per-column or width-growing translations are outside
the proof. Root identified this required scope clarification; the author
incorporated it before admission.

## Sign comparisons are physical

Each fresh seven-axis body block is the product of seven commuting
square-root-of-translation Gaussians. In their Fourier basis a one-column
frequency eta has Gaussian eigenvalue i^weight(eta). Duplicate that frequency
in two tensor columns and put zero frequencies in all other columns. The
body Gaussian then has sign (-1)^weight(eta), while every collective
translation has sign (-1)^(2 omega(w,eta))=1. Select an odd-weight eta for
one block and zero for the other independent blocks to vary that block's
sign alone. Arbitrarily large widths can be used, so head-algebra
faithfulness is compatible with these comparisons. Independent head inputs
remain unrestricted. A per-column translation distinguishes these points;
the checker records this negative control.

## Tag identity and native deletion

For a stage E_s(f)=(I+(f-1)P_s)N_s, its unique fresh body factor appears nowhere
else. At the positive reference point let U_s be the complete suffix. Then
M_- M_+^-1=U_s(I-2P_s)U_s^-1. A diagonal whole-block Gaussian endpoint has
the same ratio I-2P_s^target. Therefore U_s P_s U_s^-1=P_s^target, and each
stage's body has exactly rank(P_s)/D=2+i_s final recipients. This yields
sum d_i=2m+I. Inverse body orientations have the same negative sign and cause
no exception. Non-diagonal tag matrices do not certify a diagonal endpoint.

For a row selector E supported on bodyless outputs, E P_s^target=0 implies
E U_s P_s=0. Since N_s-I is supported inside P_s, these selected rows receive
no contribution from that native. Deleting natives backwards preserves the
selected suffix rows at each step, proving E M=E K for the query-only word K.
This is a row identity on all inputs, not merely a rank count.

The two-head matching representation applied to E K gives bodyless head rank
H0<=q1+2q2. The separate count h1+h2<=q1+q2 follows by imposing zero
source/affected-bank conditions for the queries along ordinary-only prefixes.
Their common kernel has codimension at most qD. Its projector belongs to the
finite ordinary *-algebra. On this kernel K agrees with the invertible
ordinary-only word O. Since the selected endpoint has no rank-zero component,
ordinary bimodularity yields EOP=0; comparing ker(EO) with im(P) proves the
count bound. The projector is not a physical operation or a free service.

## Complete price

Let a=8^t-7^t, 0<t<1. For a body-bearing endpoint,
(7d+r)^t<=d7^t+r a. The global head-conservation inequality, exact total body
degree and the two bodyless bounds give

    T <= (2m+I)[7]+2m a+q1[1]+q2[2].

For the bodyless combination the needed coefficients are 2-2^t>0 and
2^t-1-a>0; these follow from concavity and decreasing increments. The paid
price is m([1]+[7]+[8])+I[7]+q1[1]+q2[2], hence

    P-T >= m(1+[7]-[8])>0.

All optional idles are paid. Removing them does not rescue fresh-tag fission.
Other costs can only increase this deficit. Reused or split body blocks,
separated repeated applications, noncollective translations, head/body mixing,
extra heads and changed endpoint retention remain outside the theorem.

## Exact controls

`check.py` independently checks the actual duplicated-frequency sign points,
noncommutative tag identity, a routed bodyless-row deletion and meaningful
scope/endpoint mutants. It imports no author code and writes `RESULT.json`.
Expected status `PASS_INDEPENDENT_FRESH_BODY_TAG_CONTROLS`. The finite examples
supplement the preceding universal proof and do not replace it.

Credit @CubeJerry, source/compiler and tensor-representation predecessors,
Worker B's tag theorem and root's independent scope and proof audit, with
substantial OpenAI assistance. All five foundations remain retained.
