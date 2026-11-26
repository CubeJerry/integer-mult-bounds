# Independent C review of the optimized state-tree invoice

Disposition: **pass within the declared positive local invoice**.
This is an independent algebraic and asymptotic proof review, not a
machine-runtime lower bound, an independent execution of the finite
moment checker, or an admission of a new global multiplication scale.

Reviewed complete files:

- B `STATE-TREE-OPTIMAL-LOCAL-INVOICE.md`, SHA-256
  `991a31bd50685619602aeadae9e0a35f64ccde6853751d841581d282b156d86c`.
- Its supplier `STATE-TREE-MOMENT-PROFILE.md`, SHA-256
  `b4216256a1bd2fa16c5564390e36a2f7f9facbfd3f73f7acf07e936451656888`.

The source-compatible state-tree construction and retained charged
routine have their separately recorded A/B/lead reviews. This note
checks the new analytic optimization using that exact tree formula.

## 1. Moment supplier

The falling-factorial expansion gives
`sum_(k>=1) k^L 2^(-k)=2F_L` exactly, where F_L counts ordered set
partitions. Substituting the odd/even threshold component polynomials
and telescoping the finite tree sum gives precisely the stated
`M=q kappa_L-E_(L,t)`. The tail error has the displayed coefficient
one half; it is nonnegative because its geometric weights sum to one,
the component polynomial increases, and `C(t)>=lambda`.

For `t>=4L`, the ratio of successive tail majorants is at most two
thirds. Together with `kappa_L>=A_L/3`, this gives P5 with its factor
9/2. At `t>=8L` it is below one half, proving the claimed two-sided
range. The elementary estimates `L!<=F_L<=L^L` are justified by the
singleton ordered partitions and the initial-image function injection.
For even L the unconditional `F_tree<=10qF_L` bound is valid.

The integer profile uses an even L and an exact integer square root.
Its top charged term is at most `2^(-2L)`, and the whole charged list
is at most twice that term. The stated reserve and polynomial label
count follow. With `x=ceil(log2 m)`, the last conversion
`2^(4x)<=m^5` is valid throughout the stated x>=64 range because
`log2 m>x-1`. The dimension guard is appropriately deferred to an
exact check plus bounded-length fallback, not asserted at every size.
The inequalities leading to P12 hold: for u=sqrt(x/S)>=2,
`t<=sqrt(xS)+2S+7` and `L log2 L<=sqrt(xS)`.

## 2. Lower-envelope proof

All three O2 inequalities are valid for the declared J. In particular,
the tree has lambda vertices and at least lambda-1 unit-cost edges,
while `lambda>=(t+1)^(L-1)`. One direct count of this latter fact is to
choose the first L-1 state symbols arbitrarily and then choose the last
symbol to make the support parity odd. The highest charged term and
`D>=q` give `b>=x-Lt/2`, including odd L.

Restricting to `b<=4sqrt(xA)` is legitimate for a lower-envelope proof.
The deductions `Lt>=x`, `L<=2b`, and
`t>=sqrt(x)/(8sqrt(A))` hold once `b<=x/2`. If `t<8L`, the two lower
bounds on b multiply to the displayed contradiction for A>8192.
Thus the explicit eventual cutoff A>=16384 safely puts every
potentially optimal invoice in the two-sided moment range.

There, `F_tree>=2qF_L` supplies O3. The constraints then give
`log2 L>=A/2-B/2-2`. Since `2+log2 e<7/2`, the choice
`R=A-B-7` yields

    b >= 2(x-b)/L+(R/2)L >= 2sqrt((x-b)R).

Solving this quadratic gives exactly
`b>=2sqrt(xR+R^2)-2R`, with no dropped positive-invoice term needed.
The integer upper profile in the moment note has
`S=A-B+O(1)`, so it matches this lower envelope. The additive O(A)
remainders can indeed be placed inside a bounded term in the square
root, since `A^(3/2)/sqrt(x)` tends to zero. This proves the stated

    inf log2 J = 2sqrt(x[log2 x-log2 log2 x+O(1)]).

The separate q=2 exception has a retained charged bill at least m and
does not challenge this infimum. Neither proof silently removes a
charged contribution, replaces the fixed tree by an arbitrary executor,
or promotes the local optimized invoice to a physical-runtime bound.

No mathematical amendment is requested. Reviewed by E003 route C on
2026-11-26, with substantial AI assistance; no human-refereeing or
formal-proof claim.
