# Uniform growth bounds for the two-level interchange labels

Status: **proved enabling bounds for labels and recursive-call counts**.
This is not a complete tape running-time bound. It exposes parameter growth
hidden in the fixed-prime asymptotics of the November tape construction.

Source: OpenAI `math@3344da59991ed94f9ba711217b29c1d760badfa6`, tape
`build/interchange.tex`, especially `lem:interchange-labels`,
`eq:interchange-gram`, `eq:interchange-stage-cost`, and the parameter choice.
The graph and tape mechanism are the source's, not a new programme invention.

## 1. Constants valid for every prime and label alphabet

Let p>=3 be prime, h=2p-1, q=2^t with t>=1, n0=q^h and N=q^(h^2).
Set

    C0 = 1+h^(p-1),       Cr = C0^(p+1).

For the source's scalar transfer matrix P_* over F_p, rational address
quotient dimension D, and directed rectangle incidence lambda, the bounds are

    rank(P_*)/N <= Cr q^(-p^2),
    D <= 2+h q^h,
    lambda <= binom(h,p)^(p+1) (q-1)^p t^(p(p-1)).                 (L1)

### Rank proof

The inner matrix P0 has entry 1-dist(v,w)^(p-1). Expanding the power as
ordered products gives at most h^(p-1) nonconstant terms. Each involves at
most p-1 coordinates, so its rank is at most q^(p-1). The constant term
has rank one, giving rank(P0)<=C0 q^(p-1), as well as rank(P0)<=n0.

Expand the analogous outer factor into at most C0 terms. In each term at
least p of the h tensor coordinates retain P0; every other coordinate has
rank at most n0. Therefore

    rank(P_*)/N <= C0 (min(1,C0 q^(-p)))^p <= Cr q^(-p^2).

This proof counts all constants and works for the whole p,q family.

### Address dimension proof

Write K(v,w) for the number of far inner-coordinate pairs. The rational Gram
matrix is J_N tensor I_2 +(K/p) tensor (S-I_2), where S exchanges two basis
vectors. Since rank(S-I_2)=1 and K is a sum of h matrices factoring through
one n0-valued inner coordinate, rank(K)<=h n0. Thus the Gram rank, equal to
the nondegenerate quotient dimension, is <=2+h n0. No data-field rank is
being used as a rational rank in this argument.

### Rectangle proof

For a fixed source inner word, choose its p differing positions in
binom(h,p) ways. At the first differing position there are q-1 destination
letters. At each of the other p-1 positions the first-differing-bit partition
has t incident rectangles. Thus the source or destination incidence of the
inner partition is at most binom(h,p)(q-1)t^(p-1). The outer partition
chooses p positions and takes a product of p inner rectangles. Multiplying
gives the third inequality in (L1). First-differing-bit partitions are
unique for every ordered unequal pair, so this also preserves disjointness.

## 2. A uniform choice and an optimized asymptotic family

For integer m>=2 choose q as the least power of two satisfying

    q^(p^2) >= Cr m.                                             (L2)

It follows that m rank(P_*)/N<=1. Write s=log2 m. Since
log2 Cr=O(p^2 log(p+1)) with an absolute implied constant,

    t <= 1+s/p^2+O(log(p+1)).                                   (L3)

Combining (L1) gives, uniformly in p,m,

    log2[D(1+lambda)]
       <= (3p-1)t + p(p-1)log2(max(1,t)) + O(p^2+log(p+1)).       (L4)

Take p to be a prime between x and 2x, where
x=(s/log2(s+2))^(1/3), for sufficiently large m. Bertrand's postulate
supplies such a prime; the bounded initial range uses p=3. Then

    log2[D(1+lambda)] = O(s^(2/3)(log(s+2))^(1/3)),
    log2 N <= 4s+O(p^2 log(p+1)) = (4+o(1))s,
    log2 D = O(s^(2/3)(log(s+2))^(1/3)).                         (L5)

All implied constants here are absolute. This obtains an explicit family
instead of substituting a growing p into an unquantified O_p estimate.
The choice is not asserted to be globally optimal over different geometries.

## 3. What follows for calls, and what does not

The source stage invoice counts O(D(1+lambda)(1+m rank(P_*)/N)) smaller
interchanges per input stream. Its constant is absolute for the *call*
metric: each coordinate conversion acts on O(D) fields and factors into
at most that many field exchanges. Row arithmetic and tape scans are
separate costs. Source binary prediction/repair uses O(sqrt(m log m))
pencil stages and <=2/m^2 further calls per stream for full conversions.
The main-call count therefore has the uniform bound

    sqrt(m) * 2^{O((log m)^(2/3)(log log(m+2))^(1/3))}.            (L6)

Occupied reserves add 2(D-2) full-stream calls. Their count is
m^{o(1)} under (L5), smaller than (L6). This establishes a one-level
call contraction with exponent

    1/2 + O((log log(m+2)/log m)^(1/3)).                          (L7)

It DOES NOT establish a uniform time recurrence with that exponent. The
source hides the finite row-program's scalar alphabet, row count, tables,
program generation, and non-call scan coefficients in its fixed-parameter
constant. The integral multivariate predictor's generalized Clifford
linearization can be far larger than the label set N. Its scalar extension
and physical encoding must still be bounded and paid. The address radix
must avoid rational matrix denominators, and its padding factor must be
charged. Replacing those constants by one in a variable-m recurrence would
be invalid.

L6 is thus a quantitative local bound for the exact source family, not
an overhead envelope H(n), nor a claim to improve the published n L^(1/2+o(1))
theorem. It identifies where further work matters: the label count is only
m^{4+o(1)}, while the complete scalar program may dominate it enormously.

## Open next questions

1. Quantify the full finite-characteristic predictor representation, fixed
   alphabet encoding, scan instruction list, and compatible prime radix.
2. Determine whether a compact divided-power evaluator avoids the Clifford
   enlargement while preserving full-rate independent inputs and call depth.
3. Check the proposed lower bound for the rational address dimension when
   one increases p to make ordinary count division valid. A field change
   cannot be assumed to leave the routing invoice unchanged.

Credits: OpenAI November 24 tape construction; the Frankl-Wilson/intersection
and routing predecessors cited there; @CubeJerry's programme. Explicit
family accounting developed with OpenAI GPT-6 Astra Pro assistance. No
priority claim beyond this extraction is made.
