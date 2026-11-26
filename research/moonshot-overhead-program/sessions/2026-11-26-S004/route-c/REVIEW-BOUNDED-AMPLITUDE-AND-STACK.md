# Independent audit of amplitude correction and child stacks

**Verdict: pass for A1–A7 after the explicit a<=tau cap in the one-sided
branch; pass for A's fixed-tape dispatch supplier.** This is a promised
corrector and scoped supplier obstruction, with no fast approximate
candidate or new complete multiplication bound.

## Algebra and operation count

The principal-root argument is valid over Z/2^a despite zero divisors.
For n=mk, omega=y^(m/k) has order dividing 3k, and each nontrivial
geometric sum factors through 1+y^m+y^(2m). Thus omega is principal
and 3k is a unit, giving the DFT and its inverse over the ring.

The idempotent (2-u^k-u^(2k))/3 is zero at precisely the k frequencies
divisible by three and one at the remaining 2k; it is one modulo
u^(2k)+u^k+1. The cyclic embedding therefore gives exactly 2k recursive
products. Charging 3k instead would invalidate the desired recurrence.

The ordered lift is essential and correct. After reduction in u, true
coefficient polynomials are sums of products of degree-below-m blocks,
hence have y-degree below 2m. Their canonical R_m representatives are
those exact polynomials. Only then is u=x^m,y=x substituted and the
result reduced in R_n. This avoids a false homomorphism from E into
R_n. Ordinary products embed without wraparound in the least n>=h.

Ring additions and twiddle rotations cost O(ma) bit steps. The latter
are zero-extended cyclic shifts followed by a fixed number of passes
using y^(2m)=-y^m-1. Modular division by three selects one of three
lifts and uses fixed-divisor bitwise division in O(a) time. The ceiling
recurrence F(ell)<=2F(ceil(ell/2))+O(ell) gives the stated A5 bound.

## Fixed tapes and every visited cell

A's supplier provides an actual head discipline. Frequency operands
are stacks consumed from their ends. The next child's two records
are at the corresponding heads. On every other fixed tape the child
starts above a current-frame marker, with ancestors below it. It uses
the same finite set of tape roles and returns to its own markers,
leaving one canonical output record on the parent's output stack.
Transfers and suffix cleanup cost O(ma) per child.

Output grows as inputs shrink, and all parent tops remain inside their
O(na) intervals. One record-order reversal costs O(na), preserving
record-internal bit order. Partner-stream copies, butterfly passes,
merges and digit reversal remain inside current suffixes. Their heads
move monotonically over O(na) cells per stage, giving O(na log k).
No tape or marker color is assigned to a recursion level.

Since m<=n/3, maximum rightward extent on each tape is bounded by a
fixed constant times a(n+m+...), a geometric series. Siblings reuse
overlapping suffix ranges. Descriptor lengths, including repeated a,
fit this bound. Thus the argument controls cells ever visited as well
as live cells. A schedule that scanned the parked parent prefix for
every child would fail, but the given stack schedule does not do so.

## Correction, certification and scope

Under the amplitude promise, M>2B gives the unique centered residual.
Input reductions, candidate subtraction, lifting, addition and carries
have O(V) volume. The capped a<=tau makes the modular workspace O(V).
The stated packed-input and sub-square-root-logarithmic regimes follow.

The one-sided mass test is sound because E_i-r_i is a nonnegative
multiple of M. Its total is zero only when every difference is zero.
The scalar product A(1)B(1) must be charged separately for constant h
and large tau; the revised note does so. I requested an explicit cap
a<=tau in this branch, now integrated. Since 2^tau>2Emax, larger
budgets need no larger workspace and capping preserves acceptance.

The supplier gates also pass. The stated regular-shift basis witness
detects the missing full-shift coefficient of a low support-degree
predictor. It is an ordinary-amplitude obstruction only at that
declared linear interface. For fixed real bilinear forms, the second
moment is at least U^4 times Frobenius error squared divided by 16.
Uniform absolute error implies A7; lowering the rank of an individual
partial anti-identity convolution form costs Frobenius error at least
one. Neither gate is a total bilinear-rank or general runtime bound.

## Isolated replay

The copy in `replay-bounded-amplitude/` passes 192 principal-root sums,
24 DFT/inverse controls, 60 full ring products and 405 recursive products
with exact 2k invoices. It also passes 1,305 zero-frequency certificates,
46 division-by-three checks, 12 full amplitude corrections, 12 positive
mass tests, 2,047 ceiling-recursion bounds and 60 bilinear controls.
Adverse cases reject a non-strict modulus, unpromised alias, signed mass
cancellation and wrong ordinary embedding. These are exact arithmetic
controls, not machine timing tests; the physical conclusion rests on
the explicit stack and scan schedule audited above.
