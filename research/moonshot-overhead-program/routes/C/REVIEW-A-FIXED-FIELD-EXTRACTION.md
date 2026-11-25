# Independent review of the fixed-field extraction

Route C, S002, 2026-11-25. Read the complete current
`../A/fixed-field-extraction-theorem.md`, Q1--Q13. The independent finite
count-formula proof and exact checks are in `CHAR2-COUNT-BIT-FORMULA.md`.
The previously conditional interface and profile were reviewed in
`REVIEW-B-IP4-BRIDGE.md`; its missing representation premise is now supplied
by the count-bit construction.

**Gate: PASS for Theorem Q as a mathematical algorithm/profile composition
using the programme's accepted physical and common-cap contracts.**
There is no remaining IP4 representation hypothesis in this theorem. The
all-odd-characteristic dyadic hypothesis remains a different open target.
This gate does not claim an executed full tape machine or formal proof.

## 1. New interchange margin

With `d` the least power of two at least `100J`, one has
`100J<=d<200J`. The characteristic-two label bounds give

    m r_*/N<=1, t<=3+x/d^2,
    D_I<=2+(2d-1)q^(2d-1),
    lambda_I<=binom(2d-1,d)^(d+1)(q-1)^d t^(d(d-1)).

The absolute shared-pencil endpoint bill is therefore at most
`64 D_I(1+lambda_I)`. Both order-three query powers use that same swap
pencil plus charged pointwise comparisons; they do not duplicate the
recursive endpoint calls.

For a transform, the two-predictor repair has nonrecursive call bill
`2 D_pred R_pencil` and four child phases of normalized row mass 1/16.
Finite unrolling thus gives coefficient at most
`(8/3) D_pred R_pencil + m 4^(-a)`. The final three-transform word gives

    sigma_Q/W <=8 D_pred R_pencil+3m 4^(-a).

Using `D_pred=6 ceil(sqrt(m))<=12sqrt(m)` and `a=ceil(x/4)`, the main
term is at most `6144sqrt(m)D_I(1+lambda_I)` and the remainder at most
`3sqrt(m)`. The stated 8192 constant safely covers both. The further
factor-two leading padding and `2(D_I-2)` occupied-reserve calls fit
the 32768 constant in Q3. These constants cover the complete caller,
rather than only one predictor pencil.

The logarithmic estimate follows directly by adding

    log2 D_I <=(2d-1)t+log2(2(2d-1)),
    log2(1+lambda_I)
       <=1+(2d-1)(d+1)+dt+d(d-1)log2 t.

Substituting `t<=3+x/d^2` and `t<=4x` leaves
`3x/d+10d^2 log2(4x)` with substantial slack for `x>=d>=2`.
Thus Q4 has the stated absolute constants. The label count obeys
`log2 N<=(2d)^2(3+x/d^2)<=4x+12d^2`, giving `N<=m^5`
when `x>=12d^2`.

## 2. Rational Walsh margin and trial acceptance

The numerical Walsh predictor uses at most `7sqrt(m)` stages. Two
applications, finite contraction factor at most 4/3, and the per-pencil
bound `5D_F lambda_F` give
`(280/3)sqrt(m)D_F lambda_F`. The direct leaf remainder is at most
`4sqrt(m)`. Consequently the constant 128 in Q5 is valid.

At `x0=2^40 J^3 log2 J`, with `J>=3`,

    log2(4x0)=42+3log2 J+log2 log2 J <32log2 J.

For example `log2 log2 J<=log2 J` and
`42<=28log2 J` already suffice. Hence

    400002 J^2 log2(4x0)
      <12800064 J^2 log2 J
      <x0/(4J).

The ratio `log2(4x)/x` decreases for all subsequent x. Since the linear
interchange term is at most `(3/100)x/J`, the complete excess, including
the extra bit for the half margin, is below `x/(2J)`. This proves the
interchange acceptance test.

For Walsh, adding the two bits for the quarter margin to Q5 gives an
excess bounded by

    2x/L+L log2(3x)+log2(3L)+10.

At `100J<=L<=202J`, the first term is at most `(2/100)x/J`, and the
remaining terms are smaller than the already paid
`400002 J^2 log2(4x)`. Thus the pre-padding quarter margin follows at
the same x0. `A>=m` only improves it. The label, reserve and stage guards
also hold there. Taking the next dyadic trial exponent increases x0 by
at most a fixed factor, preserving `log2 m_j=O(J^3 log2 J)`.

## 3. Finite data and physical interface

The full-rate factorization of the new polynomial-size formulas has
dimension `2^(m^C)`, including all shifts. Its common odd conductor, F4
coordinate algebra, unit-difference checks, actual exception tables and
constructor have the same single-exponential profile. The finite
contraction multiplies independent width by at most `16m`. Completed
swap maps have F2 coefficients, so basis descent multiplies independent
width and calls together. No claim that intermediate order-three maps
act separately on F2 coordinates is required.

The rational numerical Walsh component remains separate. Its rational
divisions never enter the characteristic-two ring. All of its endpoint
and representative maps are the audited binary column maps and signs;
their tape movement is charged through the completed interchange caller.
The rational row coefficients are approximated once by integer division
at the prescribed dyadic precision. Their listed heights, operation
counts and norms are within the finite envelope, so setup and coefficient
rounding are covered by the existing numerical ledger. Record
multiplication still uses the fixed short multiplier.

The completed width is included before compatible address-radix choice.
Thus an exponentially large width is not silently omitted from the
numeric address bill. Its radix search and all rational compatibility
data remain `2^(m^C)` after increasing C. Coordinate arithmetic is charged
by the dimension and tables, without enumeration of the entire algebra's
elements as a scalar alphabet.

The accepted physical compiler therefore has the same contract
`a,c,d,g<=P^K`, `U<=max(U_abs,2^(P^K))`, now with `P<=2^(m^C)`.
All new ordinary maps, comparisons, coefficient preparation and parked
arrays are inside that contract. The depth-first V/16 and V/8 finite
closures retain geometric parked volume. If ordinary predictor work
requires a P-dependent constant number of arrays, its factor is in c;
it does not become a recursion-depth factor. The source reserve discipline
and independently audited common cap remain applicable.

For completeness, the cap calculation remains explicit. At
`r_j>=4c_j` and `n>=4(c_j+d_j)`,

    c_j ceil(n/r_j)+d_j <= n/4+c_j+d_j <= n/2.

The condition `n>=r_j U_j` makes every chunk size eligible. Input, output,
diagonal assembly, interpreter state and cleanup use the separate absolute
linear allowance. Attempts abort before crossing their marked physical
cap; the restart schedule does not simultaneously retain their arrays.
This is a bound on visited cells, not just peak logical row count.

## 4. Profile and eligible sparse inversion

Substitution of the trial bound yields

    log2 D_j, log2 L(N_j) <=2^(C J^3 log2 J)=E_J.

This includes generation and additive retained workspace through the
common-cap threshold, the chunk products and physical diagonal assembly,
the restart weight, and the one fixed absolute prime-shape cutoff.
No numerical value for that fixed cutoff is needed for correctness.

For `s=log2 L(n)`, `z=log2 s`, take

    Y=(z/(2C log2 z))^(1/3), J=2^floor(log2 Y).

Then `Y/2<J<=Y` and `log2 J<=log2 z`, so `E_J<=sqrt(s)`.
The threshold bound proves actual eligibility `n>=N_j`. The same
candidate gives

    log2 H(n)<=O(1)+sqrt(s)+2s/Y
       =O(s (log2 log2 s/log2 s)^(1/3)).

The fixed scheduled machine discovers successful attempts without being
given the asymptotic parameter choice. Every finite small range is handled
by its exact fallback. This proves Q1 within the stated accepted contracts.

The improvement is a comparison between explicit upper envelopes. The
displayed scale is smaller than the preceding formula scale by
`(log2 s)^(1/6)`, but remains larger than every fixed `s^beta`, beta<1.
No lower bound on the actual overhead, benchmark endpoint or practical
threshold follows. The characteristic-two quotient formula and its
full-rate compilation are the new mechanism; a formal multilinear
formula lower bound does not apply to it.

No mathematical blocker was found in Q1--Q13. The finite count formula
was independently tested in `count-bit-formula-verification.json`; the
new absolute margins were checked directly above. Earlier isolated
replays cover the group words, both repair directions, label geometry,
common cap and compiler profile. This review does not substitute finite
sampling for the asymptotic proofs or claim a complete source build.
