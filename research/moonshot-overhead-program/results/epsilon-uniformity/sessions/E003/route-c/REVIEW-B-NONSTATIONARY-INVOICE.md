# Independent C review of the nonstationary invoice obstruction

Reviewer: E003 Route C. Result: **accepted as a restricted certificate
obstruction**. This is independent written AI-assisted mathematical review,
not a physical running-time lower bound, human refereeing, or a formal
kernel certificate.

Reviewed `../route-b/NONSTATIONARY-INVOICE-BARRIER.md` and its imported
S003 `route-a/nested-label-invoice-barrier.md` in full. The latter is at
programme `c65aac1156a46d10c0ef2aa36fd846c7a93518e1`. Source comparisons
use OpenAI `math@3344da59991ed94f9ba711217b29c1d760badfa6`, tape
`build/interchange.tex`, read in full. Snapshot hashes are recorded in
`review-b-source-hashes.json`.

## 1. Exact rank and unequal levels are covered by the predecessor

Theorem N concerns the specified first-differing-bit rectangle family and
the equality invoice `I_m=D(1+lambda)(1+m a)`, where a is the actual
scalar rank fraction. Its proof does not assume `m a<=1`. I independently
checked the elementary-symmetric matrix identity, the square-zero
implication, and the restriction proving

    rank e_d(M[1],...,M[2d-1]) >= r^d (n-r)^(d-1).

The tensor restriction keeps the first d factors in a complement of the
kernel and the remaining factors in the kernel. Exactly one summand
survives, so no cancellation or generic-rank premise is used. Iteration
gives `a>=2^(1-P(t+1))` for arbitrary nesting and different power-of-two
distances.

For the rational address rank, the previous adjacency matrix is invertible
modulo two and hence over Q. Its constant-vector and orthogonal subspaces
are invariant. The constant block of the rational Gram matrix cannot
vanish: the proposed equality has 2-adic valuations at least two and
exactly one on its two sides. Thus
`D=2+h_ell(N_(ell-1)-1)` is valid. This justifies the exact
dimension/incidence/rank tradeoff imported by B.

Dropping the nesting factor `2^(ell-2)>=1` from N8 is legitimate and
leaves a lower bound uniform in all selected local parameters.

## 2. Inverting the necessary scale

Write `x=log2 m`, `b=log2 I_m`. If `b<x/64`, the allowed real value
`J=x/b>64` makes the hypothesis of Theorem N an equality. Rearranging gives

    b^3 >= x^2 log2(x/b)/128.

For `b<x^(3/4)`, the logarithm is greater than `(log2 x)/4`, yielding
`b>=(1/8)x^(2/3)(log2 x)^(1/3)`. Otherwise the larger `x^(3/4)` bound
suffices. The branch `b>=x/64` also dominates the asserted profile for
`x>=2^16`. I checked the constants in both comparisons; `1/16` is
conservative. For the bounded interval, `D>=2` and `lambda>=1` give
`b>=2`, so one smaller absolute constant covers every m>=2.

The conclusion is a uniform lower bound on the **invoice**, including
when label depth grows with m. It does not reinterpret an implementation
upper bound as a lower bound on the work necessary to compute the map.

## 3. Arbitrary rounded schedules

For the explicitly defined recurrence, the normalized multiplier is

    C_i I_(m_i) sqrt(m_i e_(i+1)/e_i).

The assumptions `e_(i+1)>=e_i/(8m_i)` and `C_i>=sqrt(8)` make it at
least `I_(m_i)`. That coefficient condition is necessary and explicit.
Every nonnegative toll can then be discarded for this lower estimate.

For `z_i=log2 m_i>=1`, the same interface gives

    log2 e_i-log2 e_(i+1) <= z_i+3 <=4z_i.

Hence `sum z_i` is at least a fixed positive fraction of `log2 e_0`,
up to the terminal constant. Moreover `Phi(z)/z` is decreasing for
positive z because `z/(z+2)-ln(z+2)<0`. Therefore

    sum_i Phi(z_i) >= Phi(sum_i z_i).

Neither monotone arities nor a prescribed depth is used. The result
applies to every admitted rounded width chain. For a fully explicit
last comparison, `Phi(y/8)>=Phi(y)/(4*2^(1/3))` when y>=32.

I requested only the small domain correction Phi(0)=0, which B added:
the original statement permitted e_0=1 outside Phi's initial domain.
It has no effect on any positive-width asymptotic estimate.

## 4. Scope and consequence

This establishes a matching `Phi(log e)` logarithmic scale for the chosen
conservative equality certificate. Exact ranks, arbitrary label nesting,
asymmetric distances and changing arities are permitted. The lower width
guard, endpoint coefficient and rectangle partition remain premises.
A physical schedule paying less than that certificate remains possible.
No lower bound on integer multiplication, all routing or all finite
representations has been proved.

The independent order-five construction changes a separate
repair/converter interface. Its constant-factor savings do not remove
this rank/incidence/dimension profile.

Credit: the source and predecessor authors, S003's actual-rank proof,
E003 B's inversion and chain theorem, @CubeJerry, and AI-assisted
independent review. No claim of authorship of B's theorem is made.
