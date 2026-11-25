# A sharp obstruction for the retained numerical cost certificate

Status: **new scoped analytic theorem; independent review requested**.
This is not a runtime lower bound. Its explicitly positive charges define
one certificate; an upper estimate for an actual operation does not prove
that every implementation incurs the charge below.

The exact-interchanger and numerical Walsh schedules in Theorem V are
different. Improving the exact-interchanger envelope alone need not improve
the numerical certificate: polynomial local arity cost and its own kernel
excess already impose the same Phi scale. This note isolates that fact.

## 1. The abstract positive invoice

Let Y>=2 be the logarithmic active width. Take a nonempty finite sequence
of z_i>=1, where z_i represents log_2 m_i. Suppose

    sum_i z_i >= c0 Y                                  (NI1)

for a fixed c0>0. Each width chain must justify NI1 from its actual
integer child widths; it is not inferred from an upper width bound alone.
The E002 numerical chain has log-width decrease log A_i+O(1), with
A_i=Theta(m_i), so it satisfies this condition down to a bounded base.

Put g(z)=sqrt(z log_2(z+2)). Fix positive constants a,b and define the
literal normalized certificate

    C(z_1,...,z_d)=1+sum_(i=1)^d
        2^{a z_i+b sum_(j<i) g(z_j)}
        +2^{b sum_(j=1)^d g(z_j)}.                     (NI2)

The sum is the positive expansion of a one-branch upper recurrence with
local arity bill m_i^a and normalized recursive multiplier 2^{b g(z_i)};
the last term pays a constant positive terminal bill. This is a definition
of the certificate, not an equality with actual execution time. Ignoring
additional routing, preparation and precision costs only makes this
specified certificate smaller.

**Theorem NI1.** For fixed a,b,c0>0 there is c>0 such that every sequence
satisfying NI1 obeys, for all sufficiently large Y,

    log_2 C >= c Y^(2/3)(log_2(Y+2))^(1/3).             (NI3)

**Proof.** Let Z=max_i z_i. Since all prefix charges are nonnegative,
NI2 gives both `log_2 C>=a Z` and `log_2 C>=b sum_i g(z_i)`.
The function `log(z+2)/z` is decreasing for z>=1: after multiplication
by its positive denominator the derivative has the sign of
`z/(z+2)-ln(z+2)<0`. Hence

    sum_i g(z_i) >= (sum_i z_i) sqrt(log_2(Z+2)/Z)
                 >= c0 Y sqrt(log_2(Z+2)/Z).           (NI4)

Let P=Y^(2/3)(log_2(Y+2))^(1/3). If Z>=P, the local bound is at
least aP. If Z<P, monotonicity in NI4 replaces Z by P from below.
Because log(P+2) is within fixed positive factors of log(Y+2),
`Y sqrt(log(P+2)/P)` is within fixed positive factors of P.
The accumulated bound is therefore at least cP. This proves NI3. QED.

This minimum scale is sharp for the abstract invoice. Put
Y0=ceil(max(1,c0)Y) and partition Y0 into as many parts Z=ceil(P) as
possible and a final positive remainder if needed. This ensures NI1 for
every prescribed fixed c0>0. There are at most Y0/Z+1 parts, all at most Z.
Their g-sum is at most `(Y0/Z+1)g(Z)=O(P)`. Every exponent in NI2
is O(P), and the logarithm of the number of terms is O(log Y)=O(P).
Thus `log_2 C=O(P)`. The fixed rescaling and integer rounding change
only constants.
This abstract sharpness claim does not alone validate a physical schedule;
Theorem V separately provides an integer-valid physical upper construction.

## 2. Meaning for the retained Walsh proof

The numerical supplier charges a polynomial-in-m number of local actions
calling a completed width-a interchanger. After normalization by sqrt(a),
its local arity charge still has logarithm O(log m). The displayed rational
kernel majorant has logarithmic normalized excess
`O(sqrt(log m log log m))`. If the positive proof invoice retains fixed
positive multiples of these two displayed majorants, it is exactly of the
NI2 type, up to harmless constants and additional nonnegative charges.
Its Phi-scale floor therefore remains even if an improved interchanger's
own excess is set to zero in that same invoice.

This statement has an essential qualifier: the upper estimates alone do
not imply the lower charged bounds in NI2 for an arbitrary certificate.
One can only apply NI1 to a proof that actually elects to charge these
positive expressions, or after separately proving its corresponding lower
charges. A tighter physical execution bill, a different numerical kernel,
a shared multilevel evaluation, or a different normalization may escape.
The theorem is not a lower bound for the real numerical routine.

For the current even child rule, sufficiently large active a has
`a/(2A)<=f<=a/A` and A=Theta(m). Thus
`log a-log f<=log m+O(1)<=C log m`. Summing until the fixed bounded
direct base gives NI1. The actual slower schedule in V also proves the
matching physical upper majorant by an induction with an additive term.
This note does not replace that induction or its precision/space guards.

The exact-interchanger recurrence is outside this numerical model. Its
ordinary local bill is divided by sqrt(u), so m^K/sqrt(u) can remain
bounded when m is a small power of u. NI2's unattenuated m^a local
charge cannot be transferred to it. This explains why the same arity
schedule cannot automatically serve both branches.

## 3. Other kernel excess scales in the same certificate

More generally retain local logarithmic charge a z and replace g(z) by

    g_(nu,mu)(z)=z^nu (log_2(z+2))^mu,
    0<=nu<1, mu>=0.                                  (NI5)

For any fixed positive coefficients in NI2 and NI1, the sharp abstract
logarithmic invoice scale is

    Y^{1/(2-nu)} (log_2(Y+2))^{mu/(2-nu)}.             (NI6)

The proof is the same maximum-versus-sum argument. Beyond a fixed base,
g(z)/z is decreasing, and its bounded initial interval has positive
minimum. Let
`Z*=Y^{1/(2-nu)}(log_2(Y+2))^{mu/(2-nu)}`. A maximum Z>=Z*
pays the local term. For Z<Z*, the ratio bound pays at least
`cY g(Z*)/Z*=Theta(Z*)`. Equal-sized integer parts near Z* supply the
upper certificate because Z*=o(Y), the number of parts is O(Y/Z*),
and their total g charge is O(Z*). Rounding and the logarithm of the
number of positive terms are lower order.

For nu=mu=1/2, NI6 is Phi(Y). Even a fixed positive normalized
logarithmic kernel loss (nu=mu=0) leaves a sqrt(Y) floor in this particular
numerical invoice. A polynomial-Y envelope would require changing more
than that constant: for example, a shrinking per-level excess with a
compatible complete local bill, cheaper simultaneous address work, or a
different recursive mechanism. None of those properties is asserted here.

The result directs further work toward the numerical kernel/local tape
interface as well as the exact-interchange geometry. It does not authorize
an endpoint impossibility claim. Credits: @CubeJerry, the pinned source
kernel and E002 two-schedule construction, with substantial ChatGPT
multi-agent assistance. No full-machine or formal verification is claimed.
