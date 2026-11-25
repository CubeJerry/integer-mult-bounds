# Independent review of the order-three characteristic-two closure

Reviewer: Route C, 2026-11-25. Status: **proof passes for the stated
fixed-parameter physical interchange component**; isolated replay is
recorded below. No stronger whole-input overhead is certified here.

Reviewed Route B `characteristic-two-order-three-interchange.md`, SHA-256
`b467b0f01f4406584ad9ef9452a39ffce9f97af3d59192584289d7b5d7d6299a`,
and verifier `d8989eb94dd0afcdbe2fdf264c98d4584700f66e87493539fb4efc0803f1703c`.
I checked its interfaces against the source Fourier `repair.tex`, tape
`interchange.tex`, the separately reviewed characteristic-two labels,
and the finite batch-contraction proof.

## 1. Group words and the actual physical pencil

The F4 identities for C,D,S,T and Q are correct in the stated product
order. At an unequal pair the first coordinate is the smaller address;
`T C S=diag(omega,omega^2)`. At an equal pair every map is separately
defined as identity. The latter condition is necessary and is preserved
through all words. Disjoint-pair operators commute, so the global
converters are exactly `Delta F Delta F` and its inverse, and the final
three-transform word returns the main product of physical swaps.

The power identities `C_j=Q_j+1_(H_j>N_j)` and
`C_j^2=Q_j+1_(H_j<N_j)` hold on both unequal and fixed orbits. Therefore
each order-three predictor pencil uses one source shared-swap pencil
with coefficient A_(j,1)+A_(j,2), plus an ordinary pointwise sum. The
pointwise masks stay in the original layout and are applied to a retained
copy of that pencil's input. They are not incorrectly transported through
the label-dependent rational endpoint maps.

The source comparison scan applies here: a known earlier H_j partitions
the N_j-and-suffix fibre into three runs, whose complete range pays for
reading the control and computing boundaries. Delta is a fixed product
of these ordinary pointwise phases. This is actual fixed-parameter
linear-volume work, although its constant can grow with m.

## 2. Integral prediction and one coefficient algebra

Uniform ternary shifts make the count a sum of independent digits in
{0,1,2}. The window B=3 ceil(sqrt(m)) has outside fraction at most
`2 exp(-9/2)<1/32`, with the stated elementary exponential bound.
Degree 2B and a next-power-of-three root give O(sqrt(m)) pencil stages.
Duplicating every shift block by 32 makes `s=R/32` and `2s=R/16`
integers while retaining equal multiplicity and full-rate inputs.

The localized source ring uses 1/3, which is a unit in characteristic
two. Its primitive three-power root extension supplies all required
Vandermonde nodes. The identity `Phi_(3^a)(1)=3` makes their differences
units even if the specialized finite algebra is not a field. One common
finite free algebra E over F4 contains all coefficients and is reused
unchanged at every finite and spatial recursion depth.

The predictor remains the integral multivariate one. Its eigenvalues
lie in F4 even though its matrix-root implementation and check nodes
need E. That distinction justifies the two-predictor simplification.

## 3. The revised two-predictor repair is valid

For order three in characteristic two the Hermite polynomial is y^4.
Since every predictor multiplier p_i lies in F4, `P^4=P` as an exact
operator. The target multiplier z is a nonzero element of F4 and also
satisfies z^4=z. Hence the source Hermite quotient is
`D_z(y)=(y-z)^2`.

The left check inverse recovers `e_i=(p_i-z)Xhat_i` on the known
outside-window set. The right inverse prescribes
`Zhat_i=(p_i-z)^2 e_i` there. For a nonzero gap its cube equals one,
so Zhat_i=Xhat_i. For a zero gap no correction is needed. Consequently
`PX+PZ+FZ` is exact on all rows. The argument remains valid for arbitrary
E-valued inputs because the nonzero F4 gaps are units in E. Outside-window
rows that become correct after specialization are handled automatically.

Only PX and PZ are evaluated; replacing P^4 X by the already computed
PX is an operator identity, not an extra assumption about the inputs.
The reduction from five predictor applications to two is therefore valid.

## 4. Four child phases and exact batch divisibility

Both F and F^-1 use the same forward converter T and inverse converter S;
the inverse target changes the spectral tuple and target multiplier, not
the common eigenbasis. The forward word has two F^-1 calls and the inverse
word two F calls, with their intermediate Delta factors retained in order.
Each phase acts on 2s=R/16 rows per base label batch.

At finite depth h, `W_h=W0 16^h` provides exactly enough rows to collect
one phase into `W_(h-1)` inputs. Regrouping within each label preserves
the label geometry. Child check rows can be correlated: the child identity
is valid on arbitrary inputs. The spectral table occurs only after both
forward phases and before either inverse phase. No same-size circular
call is present because the finite leaves use the direct m-swap algorithm.

For the maximum of the two target call counts, the recurrence is
`c_h<=a_m+c_(h-1)/4`, with `a_m=2b_pred R_route` and c_0<=m.
This gives `(4/3)a_m+m4^-h`. Three final target calls give precisely
`8b_pred R_route+3m4^-h`. At `h=ceil(log2(m)/4)`, the leaf bill is at
most 3sqrt(m), and `16^h<=16m`. The claimed width and call invoices follow.

## 5. Alphabet, occupied reserves, and spatial recursion

The consistent physical implementation keeps E as its fixed data-letter
algebra throughout. Binary encoding of its coordinates is paid in the
template constant. Under this convention the unexpanded W_h is the
actual number of E-valued streams, so choosing the address radix above
W_h is correct. If one instead physically expands the completed program
into independent F2 streams, both W_h and calls multiply by [E:F2] and
the compatible radix must be selected above that expanded width. The
proof does not need that alternative implementation.

Every main C_j and diagonal acts only on its main field pair. The shared
swap pencil restores all occupied reserve coordinates by the source
endpoint identity. Therefore the full repaired F target, and then the
three-factor Q word, restore reserves and return every original row's
own output. Initial zero accumulators are workspace and are not counted
as independent input rows.

The finite repair tree has child volume ratio 1/16; one child runs at a
time and the parent workspace is parked. The geometric volume bound is
valid with the full fixed base-workspace coefficient retained. The source
spatial recurrence then charges the main batch's factor-two split and
the 2a_route full-volume reserve calls. Those reserve descents happen
only after merge/clear, so they park descriptors rather than a whole
second copy of the active volume. End-access stack reuse bounds visited
cells, not merely live data.

Thus the stated recurrence

    T(e)<=C_template+(2 sigma_Q,h/W_h+2a_route) T(f)

has the correct child-volume coefficient and reserve term. The reviewed
characteristic-two label bounds make its coefficient m^(1/2+o(1));
every fixed exponent above one half follows after selecting sufficiently
large finite parameters. This is a valid alternative fixed-parameter
component. The enormous generic module, finite alphabet, numeric address
scalings and common-cap cost still need their own growth bounds before
any sharper global overhead claim.

## 6. Independent finite replay

The unmodified exact verifier was replayed with its output directory
redirected to `routes/C/order-three-review-replay/`. Replay passed: 390
cyclotomic unit differences, all 64 physical basis rows including eight
equal-field addresses, 3,456 shift/frequency cases, three-label regrouping,
both target signs at depths one and two, and the final swap on 1,458
independent rows. The largest repair case had 19,683 independent rows and
1,259,712 field entries. All six numerical negative controls and the
inverse-before-table dependency control were rejected. Its finite field and
repair checks do not implement generic matrix-root routing or a Turing
machine. The proof's 1/16 phase fraction is accounted for by the exact
ledger, separately from the toy's 4/27 fraction.

No algebraic correction was required in the revised two-predictor proof.
The alphabet convention above is retained as an implementation distinction,
not an objection to the stated E-letter physical component.
