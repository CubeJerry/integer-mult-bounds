# Lead review of the exact tree moment and integer profile

Disposition: **accept the local moment and parameter refinement** in
`route-b/STATE-TREE-MOMENT-PROFILE.md`, reviewed at SHA-256
`b4216256a1bd2fa16c5564390e36a2f7f9facbfd3f73f7acf07e936451656888`.
The lead read the complete proof and checked its algebra and all displayed
parameter inequalities. B's finite checks are attributed to its own
receipt; this review does not claim to rerun them.

The exact ordered-partition moment agrees with the lead's independent
telescoping calculation during the tree investigation. Writing
A_L=sum k^L/2^k and F_L=sum r!S(L,r), falling-factorial summation gives
A_L=2F_L. The odd and even component polynomials have moments 2A_L-1
and A_L-1 respectively. Substitution into the finite MST formula gives
M=q kappa_L-E with the stated error. Its nonnegativity follows from
the monotone C polynomial, total geometric weight two, and lambda<=C(t).

For t>=4L the displayed tail ratio is at most 2/3. The lower estimate
kappa_L>=A_L/3 includes the tight smallest even case L=2, A_L=6.
At t>=8L the resulting ratio bound is decreasing and at most
(9/2)(9/128)^L<1/2. This proves the uniform two-sided estimate without
claiming it at arbitrary smaller t. Ordered partitions inject into
functions [L] to [L] with initial-interval image, so L!<=F_L<=L^L.
The free invoice and its logarithmic profile follow with the claimed
constants. For even L, 2Lq+8q(F_L-1)<=10qF_L is valid for every t>=2.

For the integer profile, x=ceil(log2 m)>=64, S=a-b+5 and
L=2 isqrt(x//S) avoid real-valued parameter tests. Put u=sqrt(x/S).
The lower rounding bound L>=2(u-1), together with u>=2, gives
2x/L<=sqrt(xS)+2S. The ceiling in t contributes at most seven.
The bound log2 L<=S/2 follows from S+log2 S>=a+2; the stated
S>=a/2>=2^(b-1) is stronger than necessary. Therefore the explicit
13qL^L sufficient invoice has logarithm at most
2sqrt(xS)+2S+11, including all rounding constants.

The top charged term is at most 2^(-2L) because Lt/2>=x+3L and
binom(L,L/2)<=2^L. Summing the geometric charged list costs at most
another factor two. Also Lt<=2x+7L<=4x and 4x<=5log2 m for x>=64,
which justify N<=m^5. The dimension guard is asserted only eventually
and remains an exact finite preflight with schoolbook fallback. It is
not silently assumed at every x>=64.

The refined minus-log-log term belongs to this sufficient local invoice.
It is neither a matching lower-order lower bound for all prior methods
nor a new complete multiplication envelope. Ordinary routing, numerical
precision, generation and the common visited-space contract still come
from the separately reviewed executor. The earlier complete admission
is unchanged. No additional practical or formal execution is claimed.
