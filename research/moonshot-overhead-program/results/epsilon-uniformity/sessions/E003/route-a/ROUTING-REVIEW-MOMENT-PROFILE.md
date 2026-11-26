# Independent review of the tree moment and integer local profile

Disposition: **accepted as a local positive-invoice refinement**. Reviewer:
E003 routing A. Read the entire B note `../route-b/STATE-TREE-MOMENT-PROFILE.md`
at SHA-256 `b4216256a1bd2fa16c5564390e36a2f7f9facbfd3f73f7acf07e936451656888`,
the complete verifier at SHA-256
`e71eff12f6afba1d945f93c2ad270abbeb7aef072ba2e40a92fca9be4d821a09`,
and its recorded receipt. No additional numerical tests were run.

## Exact moment and tail sign

Expanding k^L in falling factorials gives A_L=2F_L exactly. The shifted
component moments are 2A_L-1 for odd L and A_L-1 for even L. Subtracting
the finite tree sum from its infinite moment gives precisely

    q kappa_L-M=(1/2)sum_(s>=0)C(t+s)2^(-s)-lambda.

The tail begins at C(t), not C(t-1). Its sign is correct: the weights
(1/2)2^(-s) sum to one, C is increasing, and lambda<=C(t). Thus the
error is nonnegative. For fixed L it is polynomial in t, establishing
the displayed limiting coefficient as well as the unconditional upper
bound. No infinite sum is being estimated from finite floating samples.

For t>=4L, the consecutive-term ratio is at most 2/3 by the stated
geometric bound. This gives E<=(3/2)(t+1)^L. The inequality
kappa_L>=A_L/3 holds already at L=2, and A_L>=L^L/2^L follows from
one summand. P5 follows with coefficient 9/2. Its right side decreases
for t>=8L and is at most (9/2)(9/128)^L there, which is less than 1/2.
Hence the two-sided range P6 is correct with absolute constants.

The injection F_L<=L^L is valid: an ordered partition is encoded uniquely
by the function taking each element to its block index, whose image is
an initial interval. Singleton ordered partitions give L!. For even L,
2D+8M<=10qF_L follows from D<=Lq, F_L>=L and kappa_L=F_L-1.

## Integer all-arity parameters and reserve

The integer formula `isqrt(x//S)` equals floor(sqrt(x/S)). For x>=64,
the resulting u=sqrt(x/S) is at least two and L is an even integer at
least two. The charged rectangle terms grow geometrically up to their
top term. Since Lt/2>=x+3L and binom(L,L/2)<=2^L, their top normalized
term is at most 2^(-2L), and the full list satisfies the claimed
rank reserve <=1/8. Zero coefficients can only reduce that list.

The count Lt<=2x+7L<=4x is valid; for example L<=2sqrt(x) and x>=64
already give 7L<=2x. The ceiling x=ceil(log2 m) causes no gap in
N<=m^5: the smallest integer m in that ceiling class is 2^(x-1)+1,
and 4x<=5(x-1) for x>=5. The verifier checks that worst-case m.

The D^2<=m guard is correctly treated as eventually true and explicitly
testable, not silently admitted for every x>=64. Its failed finite range
remains subject to fallback. The reported integer profile is therefore
not a claim that all executor guards pass at every finite arity.

To check P12, L<=2sqrt(x/S) and S>=2^(b-3) imply log2 L<=S/2.
Also L>=2(u-1) yields
`2x/L<=S u^2/(u-1)<=sqrt(xS)+2S`.
Combining this with ceil rounding, P8 and the reserve gives the displayed
`2sqrt(xS)+2S+11` bound. The coefficient 13 prices the defined sufficient
label invoice; the note explicitly retains the full charged-list and
Newton/repair normalization constants separately. The lower-order
`log x-log log x+O(1)` form follows from the integer definitions of a,b,S.

## Verification scope and scientific conclusion

The verifier independently computes ordered-partition moments through
Stirling and Eulerian recurrences, checks finite tree telescoping, uses
exact fractions for the reserve/invoice, and tests both ends of each
ceiling class. Its square-root invoice checks round upward; the written
inequalities above supply the exact real bound. The receipt's 1,479
moment cases, 153 two-sided checks and 200 integer profiles have the
stated finite scope; this review does not claim a fresh replay.

No blocking gap was found. The improvement is local to the tree call
invoice and its explicit parameter choice. It supplies neither a new
complete multiplication H nor an unpriced common basis, routing routine,
precision bound or visited-space coefficient. Those limitations are
correctly stated. This is independent AI-assisted written review, not
formal verification or human refereeing.
