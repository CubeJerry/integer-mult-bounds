# Changing arities alone cannot improve the retained 2/3 invoice scale

Status: **proved scoped charged-recurrence obstruction; independently
reviewed by C** in `../route-c/REVIEW-A-NONSTATIONARY-INVOICE-BARRIER.md`.
This is a lower bound on a specified positive upper-invoice
expression. It is not a lower bound on the actual runtime of an arbitrary
implementation, on all interchangers, or on integer multiplication.

The local input is the independently reviewed
`nested-label-invoice-barrier.md` (Theorem N), with the same OpenAI and
programme source pins. C's `SYMMETRIC-LABEL-INVOICE-LOWER-BOUND.md` gives
an independently derived stronger local constant in the symmetric
occupied-label subcase. The new statement concerns the accumulation of
these literal invoices along arbitrary varying-arity schedules.

A and C independently derived this varying-arity consequence in the same
session and then cross-reviewed it. C's companion
`NONSTATIONARY-LITERAL-INVOICE-BARRIER.md` proves strict concavity by an
exact second-derivative discriminant and gives a general regular-split
version. The present note gives a stronger explicit local constant and
terminal factor. These are convergent proofs of one retained-method
finding, not separate novelty claims.

All logarithms are base two. Set

    F(x)=x^(2/3)(log(x+2))^(1/3), x>=0, F(0)=0.

## 1. An unconditional local bound within the nested invoice family

At any depth ell>=2 choose the exact nested labels of Theorem N, allowing
different power-of-two distances at different levels and any q=2^t.
Let D be their actual rational Gram rank, lambda their exact prescribed
rectangle incidence, and r/N their actual binary rank fraction. At arity
m>=4 define the literal pencil invoice

    I_m=D(1+lambda)(1+m r/N).                            (NI1)

**Lemma NI.** Uniformly over all these choices,

    log I_m >= F(log m)/128.                            (NI2)

No rank-occupancy assumption is needed.

**Proof.** Put x=log m. First suppose x>=4096. Define the real number

    J=(1024 x/log x)^(1/3).

Then J>=64. If I_m<=m^(1/J), Theorem N, even omitting its factor
2^(ell-2), would imply

    x >= J^3 log J/128.

But log J=(10+log x-log log x)/3 >= (log x)/6 for x>=4096.
Consequently the right side is at least (4/3)x, a contradiction. Thus

    log I_m > x/J
             =2^(-10/3)x^(2/3)(log x)^(1/3)
             >= F(x)/16.                              (NI3)

The last inequality uses log(x+2)<=2log x. This is stronger than (NI2).

For 2<=x<4096, every such family has D>=23 and lambda>=27. The smallest
preceding label set already has size eight, and the exact Gram formula
gives D>=2+3(8-1)=23. The incidence recurrence starts at least at three
and its next value is at least 3 times its square, hence at least 27.
Thus I_m>=23*28>2^9. On the other hand,

    F(x)<=F(4096)<1024,

because 4096^2 log(4098)<2^28<2^30. Therefore
log I_m>9>F(x)/128. This proves (NI2). QED.

The deliberately loose factor 128 makes the statement cover all arities
from four onward. Optimizing this constant has no bearing on the scope or
asymptotic conclusion.

## 2. A property of the target function

The function F is increasing. Moreover,

    F(x)/x=(log(x+2)/x)^(1/3)

is decreasing for x>0. Indeed the derivative of log(x+2)/x has the sign
of x/(x+2)-ln(x+2), which is negative. It follows directly that

    F(a)+F(b)>=F(a+b), a,b>=0.                          (NI4)

To see this, replace each ratio F(a)/a and F(b)/b by the smaller ratio
F(a+b)/(a+b), then add. Induction gives the same inequality for any
finite sum. Also for 0<=c<=1,

    F(cx)>=c F(x),                                     (NI5)

which follows either from the decreasing ratio or from concavity of the
logarithm. These facts avoid any approximation to a continuous arity
schedule.

## 3. The precise class of charged recurrences

Consider any finite decreasing width chain e_0,e_1,...,e_k, terminating at
1<=e_k<=E for a fixed base threshold E>=1. At each nonbase level choose
an arity m_i>=4, any member of the nested label family in section 1, and
a charged multiplier Lambda_i. Assume only

    e_(i+1) >= e_i/(8m_i),
    Lambda_i >= 8sqrt(m_i) I_(m_i).                     (NI6)

The first hypothesis excludes a large unbilled consumption of the active
width. It holds for the executed compact adaptive split once leading
batch digits and reserve fields fit their stated guards. The second is
an optimistic subinvoice of the present full source charge: its predictor
degree is at least sqrt(m), it bills 8 D_pred shared pencils, leading
padding is at least one, and reserve calls only add nonnegative mass.
Using an ambient dimension larger than the exact Gram rank only increases
the invoice. A different call mechanism must be tested separately.

Define the **charged recurrence value** B_i, not the actual machine time,
by any nonnegative local bills b_i and a base bill B_k>=1:

    B_i=b_i+Lambda_i B_(i+1).                           (NI7)

An upper-bound proof that evaluates precisely these positive invoices
inherits this recurrence. An actual implementation may cost less; no
reverse inference from its upper bound is made.

## 4. The varying-arity obstruction

**Theorem NI.** Every charged recurrence in section 3 satisfies

    B_0/sqrt(e_0)
       >= E^(-1/2) 2^[F(log(e_0/E))/320]                (NI8)

when e_0>=E. In particular, no choice of arities, asymmetric distances or
nesting depths within this invoice and split class makes the normalized
charged value 2^o(F(log e_0)).

**Proof.** Put U_i=B_i/sqrt(e_i). From (NI6)--(NI7),

    U_i >= Lambda_i sqrt(e_(i+1)/e_i) U_(i+1)
         >= sqrt(8) I_(m_i) U_(i+1)
         >= I_(m_i) U_(i+1).                            (NI9)

The normalized base value is at least E^(-1/2). By (NI2), iterating gives

    log(U_0 sqrt(E)) >= (1/128) sum_i F(log m_i).        (NI10)

Writing y_i=log m_i>=2, the split hypothesis also gives

    log(e_i/e_(i+1)) <= y_i+3 <= (5/2)y_i.

Telescoping and using e_k<=E imply

    sum_i y_i >= (2/5)log(e_0/E).                       (NI11)

Apply (NI4), monotonicity and (NI5):

    sum_i F(y_i) >= F(sum_i y_i)
                 >= (2/5)F(log(e_0/E)).                 (NI12)

Substitution into (NI10) proves (NI8). QED.

The theorem permits a different arity and different nested geometry at
every level, arbitrarily uneven width decrements, and any nonnegative
ordinary-work bill. It does not assume a fixed-power arity rule. The
adaptive upper construction matches this exponent in its retained
positive invoice up to absolute constants.

## 5. What a further improvement would have to change

This obstruction leaves several concrete possibilities open: reduce the
physically paid endpoint incidence through a new shared execution; find
a different rectangle/Gram family; replace the current predictor/pencil
call factor; or justify a substantially different width decomposition
with all direct work and occupied reserve costs charged. It also leaves
room for a sharper analysis of actual call lists that abandons the
literal positive upper invoice.

The result does not establish an Omega bound for actual transpose time,
does not imply that a stream requires lambda passes, and does not
lower-bound the optimal residual multiplication overhead. Its purpose
is to locate the exact retained-method obstruction after the compact
executor and varying-arity improvements.

## 6. Verification and credit

A finite checker accompanies this note. It checks the subadditivity
inequality and telescoping argument on uneven arity schedules, and
rejects a model schedule that consumes width without the (NI6) charge.
The unbounded theorem is the proof above; finite arithmetic cannot
certify an implementation or all label ranks.

`python3 -B verify_nonstationary_invoice.py` passed 336 exact lower-witness
invoice checks across seven nested/asymmetric families, 109 inversion
grid points, 640 uneven schedules and a fast-descent negative control.
Output is `nonstationary-invoice-verification.json`. C independently
reviewed the constants and hypotheses. A also replayed C's different
checker and reviewed its concavity/generalized-split argument.

Credits: OpenAI source routing and recursive tape construction; S002
characteristic-two labels; C's independently convergent symmetric
obstruction; A's independently reviewed nested asymmetric extension;
B's compact adaptive family and constant-space interfaces. Prepared for
Jerry Chen (@CubeJerry) with substantial AI assistance.
