# The logarithmic factor is in incidences, not rectangle output volume

Status: **proved exact count and conditional target**, not a new physical
implementation or multiplication theorem. This separates two possible
invoices and identifies what a proposed routing improvement must prove.

Use the canonical partition of `canonical-incidence-exactness.md`, with
`q=2^t`, `h=2d-1`, `n0=q^h`, `N=n0^h`, and
`C_d=binom(h,d)`. Let R denote its number of directed outer rectangles.

## 1. Exact rectangle-volume ratio

The inner rectangle count is
`R_in=C_d 2^(d-1)[q(q-1)]^d`. At the outer level
`R=C_d n0^(h-d) R_in^d`. Therefore

\[
\frac R N
=C_d^{d+1}2^{d(d-1)}q^d(1-1/q)^{d^2}.              \tag{RV1}
\]

In contrast, each label's exact canonical incidence is

\[
\lambda=C_d^{d+1}(q-1)^d t^{d(d-1)}.
\]

Their ratio is the average rectangle-side size,

\[
\frac{N\lambda}{R}
=\left(\frac{q t}{2(q-1)}\right)^{d(d-1)}.           \tag{RV2}
\]

Thus the entire `t^(d(d-1))` incidence factor is absent from R/N.
This identity makes no statement about how the rectangle sums are reached
on physical tapes.

## 2. The corresponding optimized count has no log-log factor

Put z=`log_2 m` and retain the sufficient rank guard, taking
`t<=3+z/d^2`. Since `C_d<=2^(2d-1)` and `1-1/q<1`, RV1 gives

\[
\log_2(1+R/N)\le O(d^2)+dt
                 \le O(d^2+z/d).
\]

The retained rational dimension has
`log_2 D<=O(d t+log d)=O(z/d+d)`. A power-of-two distance
`d=Theta(z^(1/3))` therefore gives

\[
D(1+R/N)\le2^{O(z^{2/3})},\qquad N\le m^5          \tag{RV3}
\]

for large m. The guard on N follows as before from
`log N<4z+12d^2`, with `d^2=o(z)`. This is a count of the
normalized total rectangle output volume, not a count of endpoint
incidences.

## 3. The physical contract that would be needed

A useful new endpoint mechanism would have to replace the current complete
shared-pencil invoice by an actual charged bound of the form

\[
R_{\rm pencil}(m)
\le C D(1+R/N)(1+m r_*/N),                          \tag{RV4}
\]

with the same finite-call meaning and arbitrary occupied reserves. It
must supply both rectangle delivery **and** low-rank delivery, including
inverse endpoint changes, source/query sharing, and accumulation in the
same logical address order. Polynomial-m ordinary work is allowed in
this target, but multiplying spatial calls by m is not.

RV4 does not follow from RV1. The source pays for endpoint changes at
every label-rectangle incidence, and the low-rank part pays conversions
for every basis-label incidence at every query. Knowing there are fewer
rectangle outputs does not align arbitrary input rows or place those
outputs in the low-rank basis layouts. A proof improving only the direct
rectangle sums while leaving the low-rank incidence conversions unchanged
would still retain the old loss.

Likewise, storing one sum per rectangle rather than all endpoint copies
does not alone implement the change: preparing a new endpoint for every
query can reintroduce an m factor. A usable construction must retain the
source's sharing or replace it with an explicitly charged alternative.

## 4. Conditional rate if the full contract were achieved

If RV4 and a matching visited-space/compact-preparation bound were proved,
the exact interchanger's local loss would be `2^(O((log m)^(2/3)))`.
The existing polynomial-arity recursion would then yield
`sqrt(U) 2^(O((log U)^(2/3)))` for time per volume, with the
corresponding common-space coefficient.

The numerical Walsh schedule could take `log m=Theta(y^(2/3))`.
Its logarithmic recursive loss would be
`O(y^(1/3)(log y)^(1/2))` from the unchanged rational geometry, while
the potential difference of `y^(2/3)` over a step of length
`Theta(y^(2/3))` is only `Theta(y^(1/3))`. Therefore **that direct
substitution does not close the same log-free envelope**. The numerical
route needs its own better call loss or a retuned potential/schedule.

For instance balancing local arity and the unchanged numerical call loss
suggests a remaining logarithmic correction. This note does not claim its
optimum or a new complete exponent. Its rigorous result is RV1--RV3 and
the precise full-delivery contract RV4 whose absence blocks a physical
improvement. The two-tier numerical caller prevents reading a rectangle
count improvement as an automatic multiplication improvement.

Credits: @CubeJerry; the pinned canonical geometry; E002's exact incidence
count and two-tier recurrence; substantial ChatGPT multi-agent assistance.
No tape implementation, lower bound on multiplication, or positive improved
envelope is claimed.
