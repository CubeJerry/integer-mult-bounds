# An exact ordered-partition profile for the state-tree invoice

Status: **proved local invoice refinement; independent review pending**.
This extends the lead/A minimum-tree construction by evaluating its
weighted moment and giving an explicit integer label profile. It does
not change the admitted complete multiplication scale. All physical
middle-routing work remains paid by the earlier source executor.

Supplier: A `ROUTING-STATE-TREE-SHARING.md`, SHA-256
`4958f7396176546c8929ee4a6e8d1faf4e4c471a9781e41415c993115b25c6b8`,
independently checked in `REVIEW-WEIGHTED-STATE-MST.md`.

## 1. The exact infinite moment

Let F_L be the number of ordered set partitions of an L-element set:

```
F_L=sum_(r=1)^L r! S(L,r),
```

where S(L,r) is a Stirling number of the second kind. Expanding powers
in falling factorials and summing their elementary geometric series gives

```
A_L=sum_(k>=1) k^L 2^(-k)=2F_L.                       (P1)
```

Let C(j) be the exact threshold component polynomial from the tree
supplier. Its moment is therefore

```
sum_(j>=1) C(j)2^(-j)=2A_L-1       for odd L,
sum_(j>=1) C(j)2^(-j)=A_L-1        for even L.
```

Define the positive integer

```
kappa_L=2F_L-1                    for odd L,
kappa_L=F_L-1                     for even L.         (P2)
```

For q=2^t, t>=2, the exact tree formula telescopes to

```
M=q kappa_L-E_(L,t),
E_(L,t)=(1/2)sum_(s>=0) C(t+s)2^(-s)-lambda.          (P3)
```

Here lambda is the number of odd states. Since C is increasing and
lambda<=C(t), the displayed error is nonnegative. Consequently

```
M<=q kappa_L.                                        (P4)
```

This is sharper than the earlier coarse factorial estimate and is exact
in its limiting coefficient: for fixed L, E_(L,t) grows polynomially
in t, so M/q tends to kappa_L as t tends to infinity. No numerical
approximation of an infinite sum is needed to evaluate kappa_L.

## 2. A uniform two-sided range

For t>=4L, the ratio of successive terms `(t+s+1)^L 2^(-s)` is at
most 2/3. One direct bound is

```
(1+1/(t+s+1))^L
 <=sum_(r>=0) [L/(t+1)]^r <=4/3.
```

Since C(t+s)<=(t+s+1)^L, P3 gives
`0<=E_(L,t)<=(3/2)(t+1)^L`. Also kappa_L>=A_L/3 for L>=2, and
the k=L summand gives `A_L>=L^L/2^L`. Hence

```
E_(L,t)/(q kappa_L)
 <=(9/2)2^(L-t)[(t+1)/L]^L.                          (P5)
```

For t>=8L the right side decreases with t and, at t=8L, is at most
`(9/2)(9/128)^L<1/2`. Therefore

```
(q/2) kappa_L<=M<=q kappa_L             for t>=8L.    (P6)
```

Each ordered partition is a function from `[L]` to `[L]` whose image
is an initial interval, with the function values specifying block order.
This is an injection, while the all-singleton partitions contribute L!.
Thus `L!<=F_L<=L^L`. Since D<=Lq and F_L>=L, the actual closed-tree
free invoice satisfies

```
F_tree=Theta(q F_L)                   for t>=8L,
log2 F_tree=t+L log2 L+O(L).                         (P7)
```

For even L an unconditional upper bound, valid for every t>=2, is

```
F_tree=2D+8M<=10q F_L<=10q L^L.                      (P8)
```

The exact growth is in L rather than the large power of t in the Gray
upper invoice. This is a local call-list improvement; it does not make
the charged terms or ordinary routing disappear.

## 3. An all-arity integer parameter choice

Let m be the number of queries, x=ceil(log2 m)>=64, and choose only
integer parameters:

```
a=ceil(log2 x),       b=floor(log2 a),       S=a-b+5,
L=2 floor(sqrt(x/S)),
t=ceil(2x/L)+6,       q=2^t.                          (P9)
```

The square root is computed exactly as `isqrt(x//S)`. Here L is even
and at least two. There is no fixed-parameter subsequence or real-number
comparison in this selection.

Let `N=q^L` and `D=2+L(q-2)`. Write s=L/2. The canonical charged list
has at most twice its top term, since successive
`binom(L,j)q^j`, j<=s, grow by at least a factor two. Thus

```
m binom(L,s) q^(-s)<=2^(-2L),
m r_charged/N<=2^(1-2L)<=1/8.                        (P10)
```

This is the actual charged-rank reserve guard. It follows from m<=2^x,
`binom(L,s)<=2^L`, and `Lt/2>=x+3L`. Moreover
`Lt<=2x+7L<=4x` for x>=64, so `N<=2^(4x)<=m^5`. The dimension guard
`D^2<=m` holds eventually, since `log2 D=O(sqrt(x log x))`; it can be
tested by exact integers, with the already authorized bounded-length
fallback at failed lengths. This paragraph does not treat an unchecked
asymptotic guard as valid at every finite size.

Use the sufficient positive local label invoice

```
J_actual=1+D+F_tree+mD binom(L,s) q^(-s).             (P11)
```

The full charged list costs at most twice its displayed top term, so
an absolute enlargement pays it. The retained Newton stage and finite
repair constants are separate from this label invoice, exactly as in
the earlier local interfaces. By P8, P10 and F_L>=L,

```
J_actual<=13 q F_L<=13 q L^L.
```

Put u=sqrt(x/S). For x>=64, u>=2 and
`2(u-1)<=L<=2u`. Also `log2 L<=S/2`: it suffices that
`S>=2^(b-3)`, which follows from `S>=a/2>=2^(b-1)`.
Consequently

```
t<=sqrt(xS)+2S+7,
log2 J_actual<=2sqrt(xS)+2S+11.                      (P12)
```

All stated constants are explicit. Since
`S=log2 x-log2 log2 x+O(1)`, this gives the refined local upper profile

```
log2 J_actual
 <=2sqrt(x[log2 x-log2 log2 x+O(1)])+O(log x).         (P13)
```

The leading order remains Psi(x). P13 records useful lower-order
information made available by the actual new tree schedule. It is not
a claim that every previous schedule has a matching lower bound with
the opposite lower-order sign, nor that the displayed constant is
optimal among all labels or physical executors.

## 4. Scope and verification

This is a local finite-state and positive-invoice result. It preserves
the charged-rank reserve and polynomial label count, and it uses the
already reviewed tree transitions. A complete multiplication claim
still requires the fixed-machine generation, routing, precision,
cleanup and common-space interface. The existing same-scale admission
is unchanged. The separate positive normalized routing toll in the
coupled lower-bound theorem is still a premise.

`verify_state_tree_moments.py` checks exact ordered-partition counts,
finite tree identities, the two-sided moment range, integer parameter
guards and sufficient invoices. Its receipt states the actually tested
finite cases. It does not evaluate an infinite sum numerically or run
a multiplier.

Credits: @CubeJerry; the E003 lead/A tree construction and endpoint
suppliers; Route B's independent moment evaluation and integer profile;
substantial ChatGPT assistance. No new programme-best or exhaustive
priority claim is made.
