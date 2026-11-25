# A singly exponential finite profile and its uniform tape envelope

Status: **accepted by the session lead and independent Routes B and C**.
The final reviews are `../B/review-fixed-field-physical-composition.md`,
`../C/REVIEW-A-FIXED-FIELD-EXTRACTION.md` and
`../../verification/S002/lead-review-fixed-field-extraction.md`. The finite
count construction is explicit; no unproved IP4 representation hypothesis
is assumed in the theorem below. Earlier accepted envelopes remain valid
as separate historical results.

Write L(n)=1+log2 n and s(n)=log2 L(n). All logarithms are binary.
The source pin is OpenAI
`math@3344da59991ed94f9ba711217b29c1d760badfa6`.

## 1. Assembled theorem and exact dependencies

**Theorem Q.** The explicit count-bit formulas and full-rate factorization
in `characteristic-two-count-formula.md`, the characteristic-two labels
and order-three closure in Route B, and the accepted quantitative physical
compiler give one fixed deterministic finite-alphabet multitape multiplier
with

\[
 T(n)=O\!\left(n\sqrt{L(n)}\,
 2^{\,O\left(s(n)
       \left({\log\log s(n)\over\log s(n)}\right)^{1/3}
       \right)}\right),
 \qquad \text{visited cells}=O(n).                     \tag{Q1}
\]

The formula is for sufficiently large n, with a fixed exact fallback at
every other length. All constants are absolute. The source's one absolute
prime-shape cutoff is retained separately and is not assigned a numerical
value.

The new data-field construction is used for physical interchange. The
numerical Walsh side uses B's rational Newton/division template, whose
exact coefficient lists and quantitative source operations are audited in
`../B/pairwise-newton-division.md`,
`../B/polynomial-auxiliary-cost-audit.md` and
`../B/order-three-template-profile.md`. The two sides have different
coefficient algebras; their common physical interface is the completed
interchange operation on encoded tape symbols. No rational coefficient is
reduced modulo two.

## 2. Complete call margins at cubic-logarithmic parameter growth

For j>=1 put J=j+2, theta_j=1/2+1/J and rho_j=1/2+1/(2J).
Take d to be the least power of two at least 100J, so d<200J, and take
an even Fourier distance parameter L in [100J,202J]. As before, try odd
m=2^u+1 with u running through powers of two; write x=log2 m.

For the characteristic-two labels put h=2d-1 and choose q=2^t minimally
with q^{d^2}>=C_r m, where C_r=2^{2d^2-2}. The exact label estimates are

    mr_*/N<=1,   t<=3+x/d^2,
    D_I<=2+hq^h,
    lambda_I<=binom(h,d)^{d+1}(q-1)^d t^{d(d-1)}.        (Q2)

The absolute source endpoint invoice S1 from the earlier sharper note
applies to the new scalar rank factors as well: at most
32D_I(1+lambda_I)(1+mr_*/N)<=64D_I(1+lambda_I) calls per independent
row per shared-swap pencil. The order-three query identity expresses both
query powers through this one shared-swap pencil plus actual pointwise
comparison scans, so it adds no recursive pencil calls.

The new predictor has D_pred=6ceil(sqrt m)<=12sqrt m stages. The finite
four-child repair closure and the final three-transform swap word give,
with depth a=ceil(x/4),

    sigma_Q/W <= 8D_pred R_pencil+3m*4^{-a}.

Thus sigma_Q/W<=8192sqrt(m)D_I(1+lambda_I). Including the leading-row
factor at most two and 2(D_I-2) occupied-reserve calls gives the conservative
complete spatial coefficient

    Lambda_I <= 32768sqrt(m)D_I(1+lambda_I).             (Q3)

These are actual finite row programs on arbitrary independent inputs.
The four child phases each have 1/16 of their parent's rows, and their
total mass is 1/4. Both positive and inverse order-three transforms occur
as the required converter words; no same-size circular call is assumed.

For x>=d>=2, the elementary estimates in (Q2) imply

    log2[D_I(1+lambda_I)]
        <=3x/d+10d^2 log2(4x),
    log2 Lambda_I
        <=x/2+3x/d+10d^2 log2(4x)+15.                 (Q4)

For example, log2 D_I<=ht+log2(2h),
log2(1+lambda_I)<=1+h(d+1)+dt+d(d-1)log2 t, and
t<=3+x/d^2<=4x. Substitution gives (Q4) with considerable slack.
The label count satisfies log2 N=h^2t<=4x+12d^2<=5x once x>=12d^2.

On the rational Walsh side keep the original binary label construction.
One pencil costs at most 5D_F lambda_F calls per row, as in S7. The
pairwise-shift Newton predictor has at most 7sqrt m stages. Its finite
two-child repair closure gives at most
(8/3)*7sqrt(m)*5D_F lambda_F+4sqrt(m), hence

    sigma_F/W <=128sqrt(m)D_F lambda_F.                 (Q5)

Here D_F<=m and A=2(m+D_F-1)<=4m. The same estimates as S8 bound the
logarithm of the extra Fourier factor by
2x/L+L log2(3x)+log2(3L)+O(1).

Choose

    x0=2^40 J^3 log2 J.                                (Q6)

For x>=x0, d<200J and (Q4) give

    log2 Lambda_I+1-x/2
       <=(3/100)x/J+400002J^2 log2(4x).

At x0, log2(4x0)<32log2 J and the second term is less than x0/(4J).
The ratio log2(4x)/x decreases thereafter. The complete interchange
coefficient is therefore at most m^rho_j/2. The strictly smaller Fourier
loss in (Q5) likewise gives the pre-padding margin sigma_F/W<=A^rho_j/4.
This margin includes a possible factor-two leading-row padding.

The polynomial-label guards N<=m^5 and q_F^L<=m^3, D_pred<=m, and all
source fixed geometric guards also hold above x0. The first power-of-two
trial exponent u beyond x0 is at most 2x0+2. An actual finite search thus
accepts with

    log2 m_j <= C0 J^3 log2 J.                           (Q7)

Every trial constructor terminates, and failed smaller trials fit the final
accepted finite-data envelope. No unknown initial trial or free numerical
optimization is part of this selection.

## 3. One singly exponential finite envelope for both interfaces

The count-formula theorem gives actual formulas of polynomial size and
degree D_pred=O(sqrt m), so their whole-identity cyclic factorizations have
row dimension 2^{m^C}. All 3^m shifts, the common finite algebra, its
coordinate tables, exact exception tables, and the finite contraction
unrolling have actual construction time and space bounded by 2^{m^C}
after increasing one absolute C. The additional depth-a batch factor is
16^a<=16m, and the completed target is the ordinary swap product over F2.
Descent to an F2 basis therefore multiplies independent input rows and
calls by the same degree, preserving the normalized bill. Intermediate
order-three transforms need not act componentwise over F2.

The numerical Walsh template has polynomial row widths and rational
coefficient heights. Its full spectral and binary column-operation tables
contain at most 2^{O(m)}poly(m) bits and can be constructed in that time.
The explicit operation audit lists every representative map, sign, label
conversion, row map and finite contraction node. The child Fourier calls
retain the source shared endpoint order. The retained ordinary work may
be overcounted polynomially; recursive calls may not.

Both label geometries have polynomial-m rational matrix dimensions and
bit heights under the accepted guards. Include the complete nonzero
compatibility list, factor inverses, pivots, diagonal units and completed
batch width before choosing the odd address radix. Numeric magnitudes and
bounded radix search cost are at most 2^{m^C}, by the already audited
rational-address construction. Therefore one common finite bound is

    P_m <= 2^{m^{C1}}.                                 (Q8)

This bounds local list/instruction sizes, numeric address coefficients
and radix, numerical coefficient bit heights, expanded algebra coordinates,
actual generation time, retained descriptions and workspace. Every scalar
alphabet is encoded in coordinates on the fixed binary tapes, not through
an exponentially larger alphabet truth table.

## 4. Numerical preparation and the unchanged physical compiler

The rational Walsh coefficients require one explicit preparation step.
For each listed coefficient a/b of bit height at most P_m, compute a
dyadic approximation at the chosen O(k) precision by ordinary integer
division. This is setup, with a fixed polynomial cost in k and P_m. Each
record then multiplies by its prepared coefficient with the fixed short
O(k log k) multiplier, as in the accepted source precision ledger.

The source's normalized maps and B's rational finite tables have bounded
heights and hence bounded norms. The total local logarithmic amplification
is polynomial in P_m. The ledger sums these gains along recursion paths,
charges the polynomial number of rounding events and input norm, and
chooses absolute O(k) precision once k exceeds P_m^K. Coefficient-rounding
error is bounded by its scalar error times the finite row/array norm and
is included in the same estimate. No denominator is inverted per record,
and no data-dependent spectral lookup or transform is free.

The finite characteristic-two processor itself is exact. Its comparisons,
endpoint changes, dense coordinate arithmetic, source/target scans and
parked arrays are serialized by the same finite-template compiler. The
four-child contraction has child volume V/16, the Walsh contraction V/8,
and each is processed depth first. Their parked volumes form geometric
series. Spatial reserve calls retain only descriptors after the main
arrays are released. Thus no recursion-depth factor multiplies live volume.

The compiler charges record parsing, packed-XOR sorting and guards,
ordinary scalar setup, interpreted finite instructions and all physical
movement. Its fixed short-block assembly, CRT and final carries are
unchanged. Arbitrary completed batch widths are allowed with the source's
explicit leading padding and the quarter acceptance margin above.

Consequently, after absorbing the visible log^4 L factor with slack
theta_j-rho_j=1/(2J), there are absolute K and U_abs with

    a_j,c_j,g_j,d_j <= P_(m_j)^K,
    tau_j(v) <= a_j v L(v)^theta_j,
    space_j(v) <= c_j v+d_j                 for v>=U_j,
    U_j <= max{U_abs,2^{P_(m_j)^K}}.                    (Q9)

Here g_j is actual generation time and d_j includes retained generation
and description workspace. Shape checks and a correct schoolbook branch
make every candidate total and correct at all other input lengths.
U_abs is the source's fixed prime-shape cutoff, independent of j. No
numerical value for it is needed for correctness or asserted by (Q9).

## 5. Full common-cap and schedule profile

Apply the proved wrapper in `scheduler-and-chunking.md`. For sparse
J=2^h, h>=2, set j=J-2 and choose r_j as the least power of two at least
4c_j. With

    N_j=ceil(max{8c_j,4(c_j+d_j),r_j U_j}),

each chunk v=ceil(n/r_j) at n>=N_j satisfies v>=U_j and
c_j v+d_j<=n/2. Actual diagonal assembly costs
g_j+O((a_j+1)c_j n L(n)^theta_j), including the r_j^2 chunk products,
O(nr_j) movement/carry work and exact 2n-bit output. All wrappers have
one absolute O(n) visited-cell allowance.

The actual prefix-weight restart schedule on the diagonally enumerated
(h,log2 r) attempts contributes a factor polynomial in log P_(m_j) and h.
Generation, erasure, clocks, cleanup and unsuccessful capped attempts are
inside that bill. The correct fixed fallback guarantees termination.
From (Q7)--(Q9), the resulting coefficients D_j obey

    T(n)<=C2 n sqrt(L(n)) [1+D_j L(n)^{1/J}],
                                           n>=N_j,
    log2 D_j, log2 L(N_j)
        <=2^{C3 J^3 log2 J}=:E_J.                       (Q10)

The estimate follows because log2 P_(m_j)<=m_j^{C1}
<=2^{O(J^3 log J)}, every remaining coefficient is a fixed power of P,
and log2 L(2^{P^K})=O(1+log2 P). It retains the additive generator
workspace in N_j and the fixed U_abs cutoff.

## 6. Eligible sparse inversion

Put s=log2 L(n), z=log2 s and, for sufficiently large s,

    Y=[z/(2C3 log2 z)]^{1/3},
    h=floor(log2 Y),   J=2^h,   j=J-2.                 (Q11)

Then h>=2, Y/2<J<=Y and log2 J<=log2 z. Hence

    C3 J^3 log2 J<=z/2,
    E_J<=2^{z/2}=sqrt(s)<s.                             (Q12)

The threshold estimate in (Q10) proves n>=N_j. Since
sqrt(s)=o(s/Y), the same equation gives

\[
 \log_2 H(n)
 \le O(1)+\log_2 D_j+s/J
 \le O(1)+\sqrt{s}+2s/Y
 =O\!\left(s\left({\log\log s\over\log s}\right)^{1/3}\right).
                                                               \tag{Q13}
\]

This establishes (Q1), with the finite and physical composition gates accepted.
Candidate choice is part of the proof of the fixed scheduled machine's
bound; it is not free advice depending on n.

## 7. Scope

The representation premise IP4 has been replaced by the explicit
characteristic-two bit-formula constructor. The separate all-odd-prime
dyadic hypothesis IP remains open. The degree-controlled formulas rely
on characteristic-two Boolean carry identities and are generally not
multilinear as formal polynomials. Their spectral values, degree budgets
and full-rate occupancy are the properties used here.

The new displayed scale improves the preceding accepted formula envelope:

    [(log log s)/(log s)]^{1/3}
       / [(log log s)^{1/3}/(log s)^{1/6}]
       = (log s)^(-1/6) -> 0.

This comparison is between the programme's explicit upper envelopes, not
an improvement over an unspecified published o(1). The displayed
upper-bound scale for log H still grows faster than s^beta for every fixed
beta<1. No lower bound on the actual overhead, positive benchmark exponent,
polynomial-s endpoint or constant overhead follows.

This is a mathematical algorithm/profile construction supported by finite
exact checks and independent source audits. It is not a complete tape
implementation, practical threshold estimate or proof-assistant build.
Credits: the source authors and cited matrix-factorization literature;
B's characteristic-two geometry, group-word repair and rational Walsh
component; @CubeJerry; AI-assisted count-formula and uniform composition.

## 8. Finite quantitative verification

`verify_fixed_field_growth.py` passed 4,121 exact parameter/margin/guard
cases, 4,121 negative controls omitting the sufficient threshold constant,
290 exact characteristic-two label majorants and 546 sparse-profile
rounding cases. It uses integer and rational arithmetic only. Results are
saved in `fixed-field-growth-verification.json`. The finite checks support
the explicit inequalities; they do not construct the giant templates or
execute the complete multiplier.
