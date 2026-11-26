# Independent review of the literal binary-Walsh label invoice

Disposition: **pass in the stated canonical positive-invoice scope**.
The result supplies the local profile for the separately proved
`WALSH-TOLL-INVOICE-BARRIER.md`, with its positive routing toll still
an independent explicit hypothesis. Neither result lower-bounds actual
Walsh or multiplication runtime.

Reviewed E003 lead `binary-walsh-label-invoice-barrier.md`, SHA-256
`33a01db8de08abe94f9b37c3467bee494b77968b86b32b5034f5e5e15318273c`.
The source is OpenAI math
`3344da59991ed94f9ba711217b29c1d760badfa6`, Fourier `build/kernel.tex`,
SHA-256 `f960a1c403134df527daafcb9b9e312057750cda922ce930b04e251e1382e361`.
Read its label decomposition, endpoint factorization and complete finite
call invoice. The source normalization proof is `build/binary.tex`,
SHA-256 `5979011cb813600f02b695af5cb320fe926f6e4ccbfaeb05073c9789e63f5fd7`.

## 1. Exact characteristic-two rank

For even q, the zero-sum coordinate-function space E_i has dimension
q-1 and contains the constants. The kernel of the sum map from the
direct sum of all L spaces consists exactly of constant tuples whose
constants sum to zero; it has dimension L-1. Therefore the space U
of row differences has dimension `L(q-1)-(L-1)=1+L(q-2)`.

The displayed fixed row is outside U. If it belonged, each one-coordinate
function `1_(w_i=0)+f_i(w_i)` would have to be constant, by varying
one coordinate independently. Its q-value sum is one, whereas a
constant function on an even number of values sums to zero. This
contradiction proves rank `2+L(q-2)`. It includes q=2, when the exact
rank is two for every L; replacing the rank by a rough Lq estimate
would miss this edge case. The dimension remains at least q.

## 2. Exact nonzero free-rectangle load

The source polynomial p has precisely the positive even distances
through L as roots. At every odd distance its rational value is
nonzero. Thus all odd-distance first-difference rectangles really
occur with nonzero weights in the canonical decomposition.

For a specified letter on either side of an unequal-coordinate
rectangle, each of its t bit positions determines exactly one prefix
and orientation. There are t memberships, not q memberships and not
the number of possible opposite letters. Equal coordinates contribute
one membership. Choosing the odd set of unequal coordinates therefore
gives exactly `sum_(j odd) binom(L,j)t^j` incidences at every label.

For even L, factor the difference of powers using
`(t+1)-(t-1)=2`; after division by two, the first summand alone is
`(t+1)^(L-1)`. For odd L, half the sum of the two powers is at least
`(t+1)^L/2>=(t+1)^(L-1)`. This proves the stated uniform bound,
including t=1.

Every elementary first-difference rectangle has equal-sized halves,
and products preserve this equality. If the source endpoint acts on
2r axes, the destination endpoint acts on `2(D-r)` axes. Their literal
combined cost is consequently exactly 2D times the common side size.
It cannot be undercounted by retaining only the smaller partial
transform. This relies on the declared direct endpoint list; a different
shared implementation would be a different invoice.

## 3. The highest charged term cannot be discarded

The degree-s coefficient of p is `(-1)^s/(2^s s!)`, and that of
`binom(L-k,s)` is `(-1)^s/s!`. Hence the coefficient in the Newton
basis is exactly `2^-s`, which is nonzero. It contributes the entire
canonical list of `binom(L,s)q^s` common-subword rectangles, charged
for every query and divided by `q^L` labels. This is the stated term
`m binom(L,s)q^(-ceil(L/2))`.

There is also a useful absolute upper comparison. For `1<=j<=s`,

```
binom(L,j)q^j / [binom(L,j-1)q^(j-1)]
  = q(L-j+1)/j >=2.
```

Thus the sum of all candidate charged counts is at most twice its
highest count. Omitting any zero lower-degree coefficients can only
decrease that sum, while the highest term is retained. The literal
canonical charged invoice is therefore within a factor two of the
term used in J. This supports the normalization comparison without
an L-dependent implicit coefficient.

As a discriminating mathematical control, omit the charged term and
take L=2,t=1. Then `D(1+lambda_free)=6` is constant for arbitrary m,
so the claimed square-root-logarithmic local barrier would fail.
The nonzero highest coefficient is essential, not cosmetic.

## 4. Uniform lower-bound calculation

Writing `x=log2 m`, `u=L-1` and `b=log2 J`, the exact facts give

```
b>=t+u log2(t+1),
b>=x-(ceil(L/2)-1)t>=x-u t/2.
```

If `b>=x/2`, the desired lower bound follows from
`x>=4 log2 x` for x>=16. Otherwise `ut>x`. The ratio
`log2(t+1)/t` decreases on t>0, since
`t/(t+1)-ln(t+1)<0`. For `t<=sqrt(x)` this yields
`b>=sqrt(x)log2(x)/2>=sqrt(x log2 x)` when x>=16.
For `t>=sqrt(x)`, the inequality
`b>=t+x log2(x)/(2t)` and AM-GM give the still stronger
`sqrt(2x log2 x)`. Both parity cases for L were already included.
The universal parameter bound therefore passes without a hidden
fixed-L or fixed-t constant.

## 5. Connection to the rounded global invoice

Under the admitted source guard `D<=m`, its arity is between 2m and
4m. Its retained rational Newton stage count is Theta(sqrt(m)); the
finite repair changes the completed positive call bill by absolute
factors and adds nonnegative leaf work. The canonical positive pencil
bill is comparable to J by Sections 2--3. Therefore one legitimate
conservative complete upper invoice is `K sqrt(m)J`, with K fixed
and enlarged if necessary to at least sqrt(8).

The source even rounding gives `f>=a/(8m)`. The **declared equality
invoice**, normalized by sqrt(a), consequently has child multiplier
at least J. The lead's local theorem supplies `c Psi(log m)` logarithmic
loss for all large m. Since J>=2, a smaller positive c handles any
fixed bounded admitted arity range as well.

The other premise of the coupled theorem remains a positive normalized
routing toll `c_0 m^kappa`. Keeping a polynomial-arity routing upper
bill and evaluating it even at an ideal square-root interchange
envelope produces that equality-invoice term. It does not show that
all possible tape implementations must spend that time. An actual
improvement to physical routing can invalidate this premise and is
outside the obstruction.

Thus the combined result is a rigorously scoped constraint on optimizing
this retained certificate. It is not a reversal of the source call
upper bound into a lower bound for the source machine.

## Verification scope

Read the lead's exact finite verifier and its receipt. The receipt
records 15 ranks, 14,940 canonical rectangles, 231,102 edges, 2,644
side-load checks, 2,142 Newton values and 3,948 exact invoice guards.
These results remain attributed to the lead's actual run; this review
does not claim to have repeated it. The independent evidence here is
the complete unbounded derivation and source-interface check above.
No formal-kernel, full multiplier execution or human review is claimed.

Credits: @CubeJerry; the pinned OpenAI binary routing geometry;
E003 lead's exact local-profile proof; E003 Route B's coupled
nonstationary invoice argument; substantial ChatGPT multi-agent assistance.
