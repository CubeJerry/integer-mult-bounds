# A 2/3 scale barrier for one literal variable-arity certificate

Status: proved scoped certificate theorem, independently reviewed by C.
See ../route-c/review-variable-invoice-barrier.md for the reviewed snapshot. This lower
bounds a specified sufficient invoice, not the interchanger, multiplier,
or endpoint problem.

Let m>=2, z=log2 m, d>=2 and t>=1 be integers except that m may be real.
Retain the sufficient rank guard and literal incidence charge

    2^(t d^2) >= 2^(2d^2-2) m,
    lambda=binom(2d-1,d)^(d+1)(2^t-1)^d t^(d(d-1)).     (VB1)

No power-of-two restriction on d or minimality of t is needed.

## 1. Local invoice

**Lemma VB1.** Absolute c>0,z0 exist such that every point satisfying
VB1 with z>=z0 obeys

    log2 lambda >= c z^(2/3)(log2 z)^(1/3).              (VB2)

Proof. The guard gives t>=z/d^2+2-2/d^2. As in A's fixed-family proof,
binom(2d-1,d)>=2^(d-1) and 2^t-1>=2^(t-1). Consequently

    log2 lambda >= d^2-1+d(t-1)+d(d-1)log2 t
                 >= (3/4)d^2+z/d+(d^2/2)log2 t.       (VB3)

Put a=(z/log2 z)^(1/3), b=z^(1/3)(log2 z)^(1/6).
If d<=a, the middle term is at least the claimed scale. If d>=b,
the first term is at least three quarters of it. Otherwise

    t>=z/d^2 >= z^(1/3)/(log2 z)^(1/3),
    log2 t >= (log2 z-log2 log2 z)/3 >= (log2 z)/6

for all sufficiently large z. The last term is then at least
(a^2/12)log2 z, a fixed positive multiple of the scale. QED.

The retained constructive choice d within a fixed factor of
(z/log(z+2))^(1/3), with minimal guarded t, has
log2[D(1+lambda)]=O(z^(2/3)(log(z+2))^(1/3)). Thus this local literal
invoice has the stated order. A smaller true algorithmic bill is not
excluded by the majorant's size.

## 2. Variable-scale certificates

Set Phi(z)=(z+1)^(2/3)(log2(z+2))^(1/3). Suppose a particular
multiplicative recursion certificate assigns each step a nonnegative
logarithmic normalized charge at least c0 Phi(z_i), z_i=log2 m_i>=1,
and the width reductions satisfy

    sum_i z_i >= c1 Y,       0<z_i<=C1 Y,              (VB4)

for absolute positive c0,c1,C1 and Y=log2 U. Then

    sum_i c0 Phi(z_i) >= c2 Phi(Y)                    (VB5)

for all large Y, with a fixed positive c2.

Proof. Uniformly for 1<=z<=C1Y,
Phi(z)/z>=c3 Phi(Y)/Y for some fixed c3>0. Above a fixed initial
constant, use the decreasing ratio (log z/z)^(1/3) and the constant
comparison between it and Phi(z)/z. The bounded initial interval has
positive minimum ratio, while Phi(Y)/Y tends to zero. The factor C1
changes only the constant. Multiply by z_i, sum, and apply VB4. QED.

## 3. Application and exact limits of the conclusion

VB5 is a statement about a specified certificate. To apply it, one must
actually retain a positive multiple of the literal incidence in the
normalized per-level invoice. An upper bound of the form
`Lambda_m <= C sqrt(m) D_m(1+lambda_m)` alone does not prove that the
algorithm or every proof pays lambda. A certificate that deliberately
multiplies these displayed majorants does pay it; cancellation of the
sqrt(m) factors against square-root width reduction leaves the displayed
incidence factors. Fixed multiplicative rounding factors change constants,
provided their logarithmic costs are included.

For a chain reducing a root logarithmic width Y to a bounded or
polylogarithmic terminal width, `u_child <= C u_parent/m` does not by itself
supply the needed *lower* bound on the sum of log m: it only gives an upper
bound on the next width. Verify both sides of the actual integer width
relation, or retain VB4 as an explicit hypothesis. For the E002 composite
radix, the checked relations `u/(4m) <= v <= u/m+2` and a geometric decline
of log u give `sum log m = Theta(log U)` up to an O(log log U) error.
The reserve and main calls use this same deterministic width chain.
Thus the chosen product of literal majorants cannot certify logarithmic
overhead `o(Phi(log U))` merely by changing that arity schedule.

The result does not rule out a smaller physical invoice, a tighter
simultaneous delivery argument, cancellation between endpoint work,
a different label family, or a different interchange or multiplication
architecture. In particular it is not a time lower bound for any of
those algorithms, and it says nothing prohibitive about an exact
square-root endpoint. The sufficient rank guard in VB1 can itself be
wasteful. The binomial expression in VB1 is an incidence *majorant*;
showing its unavoidable size within this certificate is not proving
that actual incidences always attain it.

The proposed variable-arity construction, if its physical and numerical
admission gates close, achieves this same scale in its certificate.
That would make the present barrier useful for choosing the next research
move: improve the actual local geometry/delivery bound or change the
certificate, rather than continue optimizing only the schedule of the
same charged majorants.

Source dependencies: the pinned OpenAI tape geometry and E002 Route A's
LITERAL-LABEL-PROFILE-BARRIER.md; the elementary minimization and
variable-scale lemma here are new in this session. This document has no
role as a premise of the admitted Theorem P. It is a scoped written
argument, with independent review requested, not formal verification.

Credits: Jerry Chen (@CubeJerry), the source authors and prior programme,
and substantial ChatGPT multi-agent assistance.
