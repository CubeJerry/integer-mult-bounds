# Independent audit of the remaining shared-Fourier invoice scale

**Verdict: pass for SI1–SI7 as a positive-invoice theorem.** It correctly
rederives the bound after the new executor, instead of applying an old
unshared invoice to a changed mechanism.

The top equality-kernel coefficient is 2^-r. On the tensor subspace with
exactly r zero-sum coordinates, lower-degree terms vanish and the top
term has nonzero eigenvalue 2^-r q^r. The disjoint such spaces prove
rho>=binom(2r,r)(q-1)^r. Since binom(2r,r)>=2^r, q-1>=q/2 and D>=q,
the charged term is at least m q^(1-r), independently of free incidence.

For b=log2 J0, the three inequalities SI5 are valid. If r=1, b>=x.
If t=1, eliminating r from b>=2r-1 and b>=x+1-r gives
b>=(2x+1)/3. Otherwise, b<x/2 forces (r-1)t>x/2 and hence
b>x log2(t)/t while b>=t. For t>=sqrt(x), multiplying these bounds
gives the stated squared inequality. For 2<=t<=sqrt(x), the minimum
of log2(t)/t on that interval is its right endpoint when x>=16;
the resulting bound is stronger than SI4. The b>=x/2 case follows
from x>=2log2 x. All boundary cases used in the theorem are covered.

The constructive choice r=ceil(sqrt(x/log2 x))+1 and
t=ceil(x/(r-1)) has (r-1)t>=x. In the charged upper bound, the q
factor from D cancels that exponent, leaving O(r+log r) in the
logarithm. Free incidence, dimension and tree bounds have logarithm
O(sqrt(x log x)), while log2 N=2rt=O(x). Thus polynomial local
parameter volume and the matching constructive order are justified.

The lower bound deliberately sets S=T=0, retaining only the specific
one-axis incidence toll lambda and the charged-rank term. It does not
prove that another executor must pay lambda, nor an actual runtime
lower bound. Sharing the remaining leaf maps, changing geometry or
changing the correction kernel remains outside this invoice theorem.
