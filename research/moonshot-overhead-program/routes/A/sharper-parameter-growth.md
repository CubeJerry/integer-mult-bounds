# Sharper finite-parameter growth and its overhead envelope

Status: **accepted unconditional quantitative source refinement** following
independent Route C review and the lead's end-to-end acceptance during S002.
This preserves `explicit-extraction-theorem.md` as the coarser sixth-power
record. The physical compiler, finite constructor, common-cap assembly and
restart machine are unchanged. Source pin:
OpenAI `math@3344da59991ed94f9ba711217b29c1d760badfa6`.

All logarithms in this note are binary. Put J=j+2>=3, choose a prime
100J<=p<=200J and an even 100J<=L<=202J, and set
rho=1/2+1/(2J). Try m=2^u+1 with u running through powers of two.
Write x=log2 m. The complete interchange coefficient must be at most
m^rho/2; the pre-padding Walsh coefficient must be at most A^rho/4.
The latter permits padding by at most two while retaining a half margin.

## 1. An absolute interchange call invoice

Let D be the rational address dimension, lambda the endpoint incidence,
r the scalar label rank, N the label count, and R the independent scalar
rows per label. Every source address conversion acts on at most 2D fields,
so its lower/permutation/lower factorization uses at most 2D pair swaps.
There are at most 2N lambda endpoint incidences. Allowing preparation and
undo at each endpoint costs at most 8RND lambda calls per pencil.
For each query, the rank-r input and output lists each have at most
r(1+lambda) terms. Their conversions cost at most 4mRrD(1+lambda) calls.
Scalar row maps and scans add no calls in this metric. Therefore

    calls per input row per pencil
       <=32D(1+lambda)(1+mr/N).                           (S1)

Serialization changes the separately charged non-call cost and preserves
these recursive child volumes and calls.

For odd m, binary prediction has degree d_pred=2B+1, where
B=ceil(sqrt(2m r0)) and r0=ceil(log2(2m)). If b is the least power
of two at least d_pred, then for x>=3

    b<=8 sqrt(m(x+2)).                                    (S2)

Indeed r0<=x+2 and b<2d_pred<=4sqrt(2m(x+2))+6. Repair uses four
predictor applications, hence 4b pencils, plus at most 2/m^2 further
calls per input row.

Choose q=2^t minimally with q^{p^2}>=C_r m, where
C_r=(1+(2p-1)^{p-1})^{p+1}. Then mr/N<=1. Including the batching
factor at most two and the 2(D-2) reserve calls gives

    Lambda_I<=1024 b D(1+lambda).                         (S3)

Before repair/reserves the bound is 512bD(1+lambda); their sum is at
most 2D+4/m^2<=4bD(1+lambda), so 1024 is conservative.

## 2. A uniform logarithmic label estimate

The exact label bounds give, with h=2p-1,

    D<=2+hq^h,
    lambda<=binom(h,p)^{p+1}(q-1)^p t^{p(p-1)},
    t<=x/p^2+log2(2p)+2.                                 (S4)

The last inequality follows from log2 C_r<=p^2(log2(2p)+1).
For x>=p>=3, binom(h,p)<=2^h and lambda>=1 give

    log2[D(1+lambda)]
       <=(3p-1)t+p(p-1)log2 t+3p^2
       <=3x/p+4p^2 log2(3x).                             (S5)

For the second line substitute (S4), use log2(2p)<=p to bound its
additional linear term by 5p^2, and note t<=3x. The remaining term
is p^2(log2(3x)+8)<=4p^2 log2(3x), since log2(3x)>3.
Thus, uniformly in the growing prime,

    log2 Lambda_I<=x/2+3x/p+4p^2 log2(3x)
                         +(1/2)log2(x+2)+13.             (S6)

## 3. The binary Fourier call invoice

At ell=2 and even L, choose q=2^t minimally with q^{L/2}>=m. Then

    D_F<=1+Lq,   lambda_F<=2(2+t)^L.

There are at most 2^L q^{L/2} charged rectangles. Every endpoint uses at
most 2D_F calls, so endpoint operations cost at most 4D_F lambda_F calls
per input row per pencil. Charged common transforms add at most
2D_F m 2^L q^{-L/2}<=2D_F 2^L<=D_F lambda_F. A pencil therefore costs
at most 5D_F lambda_F calls per row.

Write d=m+D_F-1 and A=2d. The 4b pencils and repair conversions give

    sigma/W<=20bD_F lambda_F+4d/m^3<=32bD_F lambda_F       (S7)

whenever D_F<=m. Base descent multiplies calls and independent rows by the
same degree, preserving (S7). For x>=L>=16, we have t<=2x/L+1,
D_F<=3L 2^{2x/L}, and log2(3L)<=L/2; these imply D_F<=m. Hence

    log2(sigma/W)<=x/2+2x/L+L log2(3x)
                    +(1/2)log2(x+2)+log2(3L)+9.          (S8)

We used 2+t<=3x and (S2). Since A>=m, an excess at most x/(2J)-2
in (S8) suffices for sigma/W<=A^rho/4, including the stated padding margin.

## 4. A concrete cubic-logarithmic search bound

Let

    x0=2^30 J^3 log2 J.                                  (S9)

For every x>=x0 the two contraction tests and all finite-size guards pass.
Using p in [100J,200J] and L in [100J,202J], (S6) and (S8) give

    log2 Lambda_I+1-x/2
       <=(3/100)x/J+160002 J^2 log2(3x),                  (S10)
    log2(sigma/W)+2-x/2
       <=(2/100)x/J+1000 J^2 log2(3x).                    (S11)

These include the additive margin constants. To verify them, x>=x0 is
larger than p,L and 300. Bound log2(x+2) and log2(3L) by log2(3x),
absorb each remaining additive constant into twice log2(3x), and use
4p^2<=160000J^2 and L<=202J.

At x0,

    log2(3x0)<=32+4log2 J<25log2 J.

Thus 160002J^2 log2(3x0)<2^22 J^2 log2 J, while
x0/(4J)=2^28 J^2 log2 J. The ratio log2(3x)/x decreases for
x>=x0, proving

    160002 J^2 log2(3x)<=x/(4J).                          (S12)

The sum of 3/100 and 1/4 is less than 1/2. Equations (S10),(S11)
therefore establish both required contraction margins throughout this range.

The interchange label count satisfies

    log2 N=(2p-1)^2 t
       <=4x+4p^2(log2(2p)+2)<=5x,

because 4p^2(log2(2p)+2)<=160000J^2(log2 J+11)<=x0.
For Fourier, log2(q^L)<=2x+L<=3x. Also p<=m. Finally d_pred<=m:
for u>=16, 2^u>=32(u+2), so
2sqrt(2m(u+2))+3<=m/2+3<=m for m=2^u+1. These prove all actual
acceptance guards N<=m^5, q^L<=m^3, p<=m, and d_pred<=m.

The first power-of-two u>=x0 has u<2x0+2 and x< u+1. The actual
finite search consequently accepts by

    log2 m_j<=C J^3 log2 J                                (S13)

for an absolute C, for example a fixed enlargement of 2^31. Failed smaller
trials are bounded by the final accepted dimensions as in the finite
generator proof. This sharpens O(J^6) without changing the construction
or replacing its integral multivariate predictor.

## 5. Propagating the sharper profile through the actual compiler

Keep Rhat(m)=2^{2^{m^100000}} and all the accepted source-compiler
profiles. Only the bound for m_j changes. From (S13), fixed powers of
Rhat and the separate absolute shape cutoff give

    log2 D_j, log2 L(N_j)
       <=2^{2^{C1 J^3 log2 J}}=:E_j                      (S14)

for one absolute C1. Here D_j is the actual prefactor after generation,
common-cap chunking and scheduling, and N_j is the valid common-cap
threshold, exactly as in E4--E9 of `explicit-extraction-theorem.md`.

To spell out the tower: log2 m_j=O(J^3 log J), hence
m_j^100000<=2^{O(J^3 log J)},
log2 Rhat(m_j)=2^{m_j^100000}<=2^{2^{O(J^3 log J)}}.
The generator, scalar interpretation, numeric radix factors, precision,
setup, space compression and polynomial index weight are all fixed powers
of this finite envelope. Their logarithms and log2 L(N_j) therefore obey
(S14), with one enlarged absolute constant. No physical cost is removed
or newly treated as unit cost in this refinement.

Use the same fixed machine and sparse candidates J=2^h, h>=2. Let

    s=log2 L(n),   z=log2 log2 s,
    Y=[z/(2C1 log2 z)]^{1/3},
    h=floor(log2 Y),   J=2^h,   j=J-2.                   (S15)

For sufficiently large s, Y>=4 and Y/2<J<=Y. Since Y<=z,

    C1 J^3 log2 J<=z/2,
    E_j<=2^{2^{z/2}}=2^{sqrt(log2 s)}=:F(s).              (S16)

As in the sixth-power proof, F(s)<s and F(s)=o(s/Y). The first
inequality proves eligibility n>=N_j, rather than merely optimizing an
ineligible formal prefactor. The second follows because
log2(F(s)Y/s)=sqrt(log2 s)-log2 s+log2 Y tends to minus infinity.
The exact sparse exponent excess is 1/J, so the common-cap schedule gives

    log2 H(n)<=O(1)+log2 D_j+s/J
             <=O(1)+F(s)+2s/Y
             =O(s [log2 log2 log2 s / log2 log2 s]^{1/3}). (S17)

With the parameter refinement accepted, the already constructed fixed
finite-alphabet multitape machine satisfies

    T(n)=O(n sqrt(L(n))
             2^{O(s(n)[log2 log2 log2 s(n)/
                             log2 log2 s(n)]^{1/3})}),
    visited cells=O(n).                                  (S18)

All formulas are for sufficiently large n, with the fixed correct fallback
handling the remaining lengths. The absolute prime-shape cutoff is still
named separately; no numerical BHP cutoff is asserted.

## 6. What is sharper, and what remains open

This improves the analysis of the same source construction. If z=log2 log2 s,
the ratio between the new logarithmic overhead scale and the coarser one is

    [(log2 z)/z]^{1/3} / z^{-1/6}
       = (log2 z)^{1/3}/z^{1/6} -> 0.

Thus an envelope with the new scale is asymptotically smaller than any
fixed positive-constant exponential envelope on the earlier scale. This
comparison is to our coarse extraction, not to an unspecified published
o(1). It remains far larger than 2^{O(s^beta)} for every fixed beta<1,
and does not reach the poly(s) benchmark or constant overhead.

The change arises from balancing the actual uniform label loss
3x/p+O(p^2 log x) against a target x/J with p=Theta(J). This requires
x=O(J^3 log J); the earlier sixth power was merely conservative. The large
finite integral predictor/repair description remains the dominant global
cost. No characteristic-zero count evaluator is imported into interchange.

Verification: a finite exact inequality checker accompanies this note. It
checks majorants and guard conditions on finite parameter ranges, including
dyadic rounding and negative controls; it does not replace the unbounded
proof, implement the tape multiplier, or provide Lean kernel certification.

Next: seek a different finite-characteristic representation that reduces
the dominant template growth, preserving these accepted profiles. Credits: OpenAI source
constructions and their cited predecessors, @CubeJerry, and AI-assisted
quantitative proof extraction.
