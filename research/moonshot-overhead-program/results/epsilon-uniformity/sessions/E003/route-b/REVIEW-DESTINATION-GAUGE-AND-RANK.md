# Independent review of destination gauge sharing and its changed invoice

Disposition: **pass for the stated source-compatible local schedule and
rank-weighted arithmetic**. This is a genuine change in the free-rectangle
call list. The older literal endpoint lower bound is not carried over
unchanged; the new invoice has its own lower-bound proof.

Reviewed files and SHA-256:

* A `ROUTING-DESTINATION-GAUGE-SHARING.md`:
  `c19dc584e19d6b54907dd386cb447a106923d9e931e2da5acb1f529172aee04e`.
* Lead `rank-weighted-walsh-invoice.md`:
  `0f2537e62bb76e0c031f4d6f6a2cccb50e85b0a1e656402f03355966c6a719c4`.

The source is OpenAI math
`3344da59991ed94f9ba711217b29c1d760badfa6`, Fourier `kernel.tex` and
`binary.tex`. Their hashes and the actually read endpoint sections are
recorded in `REVIEW-RATIONAL-WALSH-SPACE.md` and
`REVIEW-BINARY-WALSH-INVOICE.md`.

## 1. An explicit Fourier complement identity

Here is an independent coordinate derivation of A's complement lemma.
Let F_d be normalized Walsh on F2^d, and let B be any invertible binary
matrix whose first v columns span a specified subspace V. Its remaining
columns are any vector-space complement. Let P_B pull a function back
from ordinary coordinates to B coordinates, so `(P_B X)(z)=X(Bz)`.
Directly changing the summation variable in Fourier gives

```
F_d P_B^(-1)=P_(B^(-T))^(-1) F_d.
```

Since each normalized binary Fourier transform is its own inverse,

```
F_d P_B^(-1)(F_v tensor I)
   =P_(B^(-T))^(-1)(I tensor F_(d-v)).                 (G1)
```

Thus a partial endpoint with ordinary output coordinates can factor as

```
P_B^(-1)(F_v tensor I) M
 =F_d [P_(B^(-T))^(-1)(I tensor F_(d-v)) M],           (G2)
```

where M contains its existing input coordinate/sign maps. No inverse of
the restricted pairing on V appears. In particular G1 remains valid
when V is degenerate. Apply this identity to both halves and to every
f-bit column to obtain exactly 2(d-v) residual one-axis transforms.
All scalar normalizations are already supplied by the normalized calls.

## 2. The source phases permit one common destination gauge

At destination w the original auxiliary space is `K_w=d_w^perp`, with
dimension d=D-1 and a fixed label-specific basis and paired dual.
For a free rectangle, its final endpoint transforms along
`V=H^perp subset K_w`, of dimension v=D-r. The source separates the
final quadratic phase into an auxiliary phase fixed by w and a
distinguished phase. The latter is constant on V-cosets and is already
part of the query-specific middle operation.

Consequently the endpoint has the form `D_w P_B^(-1)(F_v tensor I) M`
in each half, with the same auxiliary phase D_w for every rectangle
incident to w. Choose `E_w=D_w F_d`. Equation G2 gives the stated
residual of dimension `d-v=r-1`, with only monomial changes in addition.
These changes use the source's polynomial-dimensional binary maps and
are charged as physical routing; they are not declared free.

The common accumulator must hold **all free contributions in the
E_w-inverse layout**. Applying E_w once after that sum is correct by
linearity. Charged and ordinary pointwise terms stay in a separate
ordinary-coordinate accumulator and are added afterwards. This avoids
putting an unperformed transform through a charged term or mask.
Row matrices commute because their action is on an independent row
coordinate, not on the transformed address directions.

The original first endpoint is still shared across all queries of a
rectangle. Its replacement final residual is also executed after
the query sum. A fixed number of full and subset arrays suffices;
sequential rectangles reuse scratch. Complete ranges, full-rate row
count and f-bit child widths are unchanged. Basis construction, scalar
heights and the additional monomial lists remain polynomial in m.
The normalized residuals and E_w are unitary, so the existing local
polynomial logarithmic-gain allowance remains sufficient.

## 3. Exact span and weighted incidence

For a product side with nonempty proper symbol subsets of sizes s_i,
the independent coordinate-difference spaces have dimensions s_i-1.
They contain no nonzero constant function because each vanishes at an
omitted symbol. Their sum is direct. The base label vector is outside
the difference space (equivalently it has norm one whereas differences
have zero self-pairing), giving `r=1+sum_i(s_i-1)` exactly.

At a fixed endpoint, unequal first-difference choices have side sizes
`2^(t-h)`, h=1,...,t. Therefore their total excess size is q-1-t.
Choosing which unequal coordinate supplies that excess gives

```
mu=sum_inc r=lambda+(q-1-t)lambda'.
```

Both sides of each canonical rectangle have equal size and equal r.
The changed free bill is therefore exactly

```
2mu+2(mu-lambda)+2(D-1)
 =2(D-1)+2lambda+4(q-1-t)lambda'.                     (G3)
```

The common 2(D-1) term is paid once per destination row. It is not
omitted merely because it is smaller than the incidence terms.

## 4. The lead's uniform arithmetic comparison passes

Write z=(t-1)/(t+1). For even L,

```
lambda'/lambda=L/(t+1) (1-z^(L-1))/(1-z^L),
```

whose bracket lies between (L-1)/L and one. This follows by comparing
the sums of L-1 and L consecutive powers of z. For odd L the bracket
is `(1+z^(L-1))/(1+z^L)`, between one and two. Hence

```
(L-1)lambda/(t+1)<=lambda'<=2L lambda/(t+1).
```

For t>=2, use `q-1-t>=q/4`, `D<=Lq`, `L-1>=L/2` for the lower
comparison. For the upper comparison use `qL<=2D`,
`lambda>=t+1`, and `D>=t+1`. These give precisely the lead's
absolute bounds

```
D lambda/[4(t+1)]
 <= D+lambda+2(q-1-t)lambda'
 <=10D lambda/(t+1).                                 (G4)
```

Thus the free part saves Theta(t) uniformly for t>=2. The assertion
does not extend to a total invoice dominated by charged or ordinary
routing work.

For the new positive invoice J_rank, the cases L=2 and t=1 have
charged term at least m and are immediate. Otherwise, putting
`v=L-2>=1`, `x=log2 m`, and `b=log2 J_rank`, the actual new terms give

```
b>=t-1+v log2(t+1),    b>=x-vt.
```

If b>=x/2, the required bound follows for x>=16. Otherwise vt>x/2.
For t<=sqrt(x), decreasing `log2(t+1)/t` gives
`b+1>=(sqrt(x)/4)log2 x`; for t>=sqrt(x), AM-GM gives
`b+1>=sqrt(x log2 x)`. Since the latter square root is at least eight,
these imply `b>=sqrt(x log2 x)/4`. This independently verifies the
fresh lower bound for the changed invoice, without borrowing the old
2D-lambda argument after its mechanism has changed.

## 5. Admission and limits

The refinement is compatible with the source numerical executor and
does reduce its stated free Fourier-axis call list. Its direct physical
middle-routing allowance is still polynomial in m. The new invoice's
local logarithmic loss remains Omega(Psi(log m)), with the older
optimized construction supplying a matching upper scale. Therefore
the coupled equality-invoice theorem still applies **when its separate
positive normalized routing toll is retained**.

The current proof does not establish the arithmetic count as a lower
bound on all possible endpoint schedules, does not require the same
gauge for a different label construction, and does not lower-bound
machine time. A separate finite verifier checks explicit normalized
matrices and counts; no full tape multiplier or formal proof kernel
was run in this review.

Credits: @CubeJerry; pinned OpenAI endpoint and normalization identities;
E003 A's constructive common-destination gauge; lead's exact weighted
invoice; substantial ChatGPT multi-agent assistance.
