# The remaining one-axis incidence toll after endpoint sharing

Status: **proved arithmetic/rank consequence of the new explicit invoice;
independent review requested**. This rederives the scale after the source
and destination execution changes. It does not import the earlier
unshared-invoice barrier as a lower bound for a changed mechanism.

Let q=2^t, L=2r>=2, N=q^(2r), D=2+2r(q-2), and
lambda=sum_(k odd) binom(2r,k)t^k. The copying/accumulation construction
has sufficient free call bill 2(D-1)+2lambda+2S+2T, with nonnegative
exact tree costs S,T. Its lambda term is one auxiliary-axis transform per
rectangle incidence in the specified destination leaf routine.

Let P_(v,w)=product_(h=1)^r(1-Delta(v,w)/(2h)), and let rho be its exact
rational rank. Even allow the charged part to use optimal rank and ignore
both tree costs. Define the relaxed positive invoice

    J0=D+lambda+m D rho/N.                                (SI1)

The actual displayed invoice D+lambda+S+T+m D rho/N is no smaller. The
following statement concerns these positive invoices, not actual runtime.

## 1. A rank lower bound retained under all endpoint changes

Expand p(Delta) in binomial(L-Delta,j). Its highest coefficient is 2^(-r),
by leading polynomial terms. On a tensor subspace with zero-sum alphabet
components in exactly r coordinates and constants elsewhere, every
lower-degree equality kernel vanishes. The top kernel acts by the nonzero
scalar 2^(-r)q^r. These independent subspaces have total dimension

    rho >= binom(2r,r)(q-1)^r.                            (SI2)

This repeats the exact top-degree eigenspace fact from the heterogeneous
Fourier note, with its dependency clear. It does not assume the displayed
charged rectangle list is optimal. Since binom(2r,r)>=2^r, q-1>=q/2,
and D>=q, it follows that

    m D rho/N >= m q^(1-r).                              (SI3)

The old free incidence or span weight is not multiplied into this bound.

## 2. Lower bound even with zero tree work

**Theorem SI.** If x=log2 m>=16, then

    log2 J0 >= sqrt(x log2 x / 2).                        (SI4)

Write b=log2 J0. The D term, highest odd incidence term and SI3 give

    b>=t,
    b>=(2r-1)log2 t+log2(2r),
    b>=x-(r-1)t.                                        (SI5)

For r=1 the last inequality gives b>=x. For t=1, lambda=2^(2r-1),
so b>=2r-1 and b>=x+1-r. Eliminating r yields b>=(2x+1)/3. Both
cases imply SI4 when x>=16.

Now r>=2 and t>=2. If b>=x/2, SI4 follows from x>=2log2 x.
Otherwise (r-1)t>x/2, and the incidence bound implies

    b>x log2(t)/t,       b>=t.                           (SI6)

For t>=sqrt(x), their product gives b^2>=x log2(t)>=x log2(x)/2.
For 2<=t<=sqrt(x), log2(t)/t is unimodal, so its minimum on this
interval is an endpoint. When x>=16 the smaller endpoint value is
log2(x)/(2sqrt(x)). Therefore b>sqrt(x)log2(x)/2, again implying SI4.
This proves the theorem with all small-t and small-r cases included.

The proof sets S=T=0. Further savings only in the large internal flag
and block transforms therefore do not change the logarithmic order while
the specified one-axis lambda toll and retained charged rank remain.
This does not exclude an executor that also shares those leaf transforms
or changes the correction kernel or rectangle incidence.

## 3. Matching constructive order and parameter volume

The canonical charged list has

    N_ch<=sum_(j=0)^r binom(2r,j)q^j<=2^(2r)q^r.

The shared free cost is O(D+lambda+2^t(C L)^L). Choose
r=ceil(sqrt(x/log2 x))+1 and t=ceil(x/(r-1)). Then

    t=O(sqrt(x log x)),
    L log(t+1)=O(sqrt(x log x)),
    t+L log(C L)=O(sqrt(x log x)),
    log2(m D N_ch/N)=O(r+log(r+1)).                       (SI7)

Thus the constructive invoice has logarithm O(sqrt(x log x)), matching
SI4 in order. Also log2 N=2rt=O(x), so labels, coordinate descriptions
and tree lists remain polynomial in local arity m. This parameter choice
does not hide exponential constructor volume.

The admitted global variable-profile multiplier remains unchanged. The
new graph reduces finite local call counts substantially, while the
specified positive invoice still has optimal logarithmic order
Theta(sqrt(x log x)). This is not an actual-time lower bound.

## 4. Concrete next gate

All leaf transforms use the same auxiliary e direction at a fixed label,
but occur between rectangle-dependent maps. Their common direction alone
does not permit adding inputs before the transform. The exact leaf operator
is D_R P_(M_out,R) F_e; its varying monomial factors lie after F_e.

A consequential next construction must substantially reduce the explicit
lambda leaf toll, supply a suitable common basis for those maps, or change
the rectangle geometry. JR and the weaker parity-weighted Fourier gate
remain useful sufficient targets. This is a falsifiable interface for
future work, not a claim that other algorithms must pay lambda.

Credits: the exact top-degree rank calculation; S004's changed graphs;
independent lead observation that D+lambda and charged rank already suffice;
Route C review insights; @CubeJerry; substantial ChatGPT assistance.
