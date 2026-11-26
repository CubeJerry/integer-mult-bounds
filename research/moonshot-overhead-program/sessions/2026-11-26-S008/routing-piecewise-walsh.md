# Piecewise native time through the complete rational Walsh caller

For the same fixed $R=240$ [integer machine](integer-clock.md), the following stronger sufficient length uses the actual two-slot widths in its Walsh layers:

$$
\log_2\log_2 n\ge 11{,}665{,}715{,}140{,}844{,}862
\quad\Longrightarrow\quad
T(n)\le n(\ln n)^{501/1000}.
$$

The coefficient of time is one. The complete numerical [visited-cell bound](routing-outer-space.md) is unchanged. The simpler sufficient endpoint $11{,}700{,}000{,}000{,}000{,}000$ needs only two rational cubings. The [full smooth comparison](routing-outer-transfer.md#the-root-degree-240-machine) using $B_W=70$ first passed its own conservative test at $18{,}536{,}231{,}398{,}600{,}959$. The positive smooth term alone still exceeds the target at the new simple endpoint.

## Same native calls with a width-dependent upper bound

Use the [actual dyadic child invoice](compiler-full-interchange.md#a-piecewise-potential-for-the-unit-coefficient), which proves $d(q+2)\le17s/4$ for $s=\log_2m$, actual root-selected dyadic $d$, and $q=\log_2(\sum_iV_i/(V\sqrt m))$. This contains every grouped child and large occupied reserve. Its proof uses the local arity only. Put $R=240$, $Y_A=R(2^{17}+2)$, and $Y_j=R((3j+6)2^{3j}+2)$ for $5\le j\le13$. As in that proof, $y=\log_2 e\ge Y_j$ implies $d\ge2^j$, now using $s\ge y/R-1$. Define the increasing concave function $H(0)=0$ with slope $1/2$ before $Y_A$, $17/64$ from $Y_A$ through $Y_5$, and $17/(4\cdot2^j)$ from $Y_j$ to the next boundary. Retain $17/32768$ forever after $Y_{13}$.

At each adaptive native width $e$ the executed child has $1\le f\le e/m$. If $\lambda$ is the current right slope, $q+2\le\lambda s\le H(y)-H(\log_2 f)$ even when a child crosses several earlier intervals. All child potentials thus use at most one quarter of $V\sqrt e\,2^{H(y)}$. The [$R=240$ node clock](node-root-parameter.md) charges at most $2V\sqrt e$ locally. Direct widths obey $256(e+1)V\le512V\max(1,e)$, and $H(y)=y/2$ there. After the paid range adapter the resulting interchanger satisfies, at $u\ge1$,

$$
J(u)\le5120\sqrt u\,2^{H(\log_2 u)}. \tag{1}
$$

The case $u=0$ has its explicit direct price. Since $H$ increases, using the larger logarithm $\log_2(u+2)$ on the right also gives a valid bound.

## Pricing the actual Walsh path

Use the [spatial child quarter](walsh-child-clock.md) at $48\Phi$ and the [separated column-map bill](walsh-node.md#only-actual-column-maps-use-the-interchanger) at the true slot width $f$. Here $x=\lceil\log_2(a+2)\rceil$ for current active width $a$, $y=\log_2(m+1)\le(33/32)\Phi(x)$, and $f/a\le 1/(2m)$. Define $\gamma=33/4$ and

$$
G(x)=48\Phi(x)+\max\left\{0,\max_{0\le v\le x}
       [H(v)-(48-\gamma)\Phi(v)]\right\}. \tag{2}
$$

The excess $G-48\Phi$ is nondecreasing, so the spatial quarter inequality remains true for $G$ at each rounded child width. Also $G(x)\ge H(v)+\gamma\Phi(x)$ for every $v\le x$. In particular the local nonrecursive movement costs at most a fixed $2^{54}(1+5120)$ times its parent volume, $b\sqrt a$ and $2^{G(x)}$: (1) and $\sqrt{f/a}\le1/\sqrt{2m}$ reduce $m^{17/2}$ to $m^8$, and $m^8\le2^{\gamma\Phi(x)}$. The ordinary $2^{105}m^{45}V$ term fits $2^{105}V\sqrt a\,2^{48\Phi(x)}$, since $45(33/32)<47$. The direct remainder and fixed-additive amortization use the original volume proof. The original $A_W=2^{2^{24}+28}(1+5120)$ pays the base and all fixed factors. Induction therefore gives the complete Walsh layer with the same $2^{18}A_W$ prefactor and $2^{G(X)}$ replacing $2^{70\Phi(X)}$. At the initial and final root positions $G(X)\ge H(\log_2 k)$ pays their actual interchanges. The full CRTs and block layers use the same comparison. Thus the complete joined time is

$$
T\le 2^{55}A_W b^4 Nk\sqrt{k}\,2^{G(X)}
$$

at the actual global address width $k$, $b=\lceil\log_2(2k)\rceil$ and $X=\lceil\log_2(k+2)\rceil$. Formula (2) is a proof majorant only. Constructing a table of its history is unnecessary during execution.

## A finite maximum and checks for every later input

The weighted geometric mean $v^{2/3}w^{1/3}$ is jointly concave and increasing in each nonnegative argument, by weighted Hölder. Since $x\mapsto\log_2(x+2)$ is concave, $\Phi$ is concave on $[0,\infty)$. Thus $H-(159/4)\Phi$ is convex on each interval where $H$ is affine. Its maximum over an initial segment ending at $v$ is attained at an earlier breakpoint or at $v$. Direct rational slope sums give

$$
Y_{13}=5937362789990880,\quad H(Y_{13})=7096092733680,\quad
H(v)=\beta+\alpha v\quad(v\ge Y_{13}),
$$

where $\alpha=17/32768$ and $\beta=4112174977105665/1024$. Set $D=2220000000000$. Every breakpoint before $Y_{13}$ already satisfies $H(Y_j)<D$, since the largest of those heights is $H(Y_{12})=1654234951920$. At the final breakpoint, $(Y_{13}+2)^8>2^{419}$ and

$$
8[4(H(Y_{13})-D)]^3 < 159^3\cdot419\cdot Y_{13}^2 .
$$

Therefore $H(Y_{13})-(159/4)\Phi(Y_{13})<D$ also. For all $v\ge Y_{13}$ this proves the single explicit envelope

$$
G(v)\le\max\{D+48\Phi(v),\, \beta+\alpha v+\tfrac{33}4\Phi(v)\}. \tag{3}
$$

Let $t=\log_2\log_2n$. The real integer packing has $Nk\le16n$, $k\le\log_2n$ and $X,b\le t+2$. Equation (3) at $t+2$ therefore bounds the logarithmic excess over $n\sqrt{\log_2n}$ after adding $2^{25}+4\log_2(t+2)$. For $t\ge z>Y_{13}$ the ratios $1/t$, $\log_2(t+2)/t$ and $\Phi(t+2)/t$ all decrease. For the last, cube it and factor as $(1+2/t)^2\log_2(t+4)/t$. The remaining linear term $\alpha(t+2)/t$ decreases as well. It suffices to test the two terms at the single left endpoint.

Take $C=2^{25}+220$. For each integer endpoint tested below $z+4<2^{54}$, so $C$ bounds its logarithmic prefactor. The two strict tests are positivity of the residuals below and

$$
\begin{aligned}
 (z/1000-C-D)^3 &>48^3(z+2)^2\log_2(z+4),\\
 (z/1000-C-\beta-\alpha(z+2))^3
   &>(33/4)^3(z+2)^2\log_2(z+4).
\end{aligned}\tag{4}
$$

At $z=11700000000000000$ both inequalities hold even on replacing the logarithm by 54. The preexisting positive smooth term $70\Phi(z)$ alone exceeds $z/1000$ there, because $70000^3\cdot53>z$ and $z+2>2^{53}$. For the sharper numerical endpoint, the [checker](routing-piecewise-walsh.py) uses the [24-term rational logarithmic interval](routing-outer-threshold.py). It proves both (4) at $z=11665715140844862$ and a strict failure of at least one at $z-1$. Thus every larger real $t$ passes the sufficient test on the actual selected Walsh supplier and actual $R=240$ interchanger. The comparison improves the smooth test's required value of $\log_2\log_2 n$ by $6870516257756097$. It locates a threshold in the stated time invoices and makes no time lower-bound claim.

The tests leave one full exponent bit for the source convention. At either endpoint, $z+4<2^{54}$ gives $2^{25}+4\log_2(z+2)+1<C$. Applying the same decreasing-ratio argument therefore proves $2T(n)\le n(\log_2 n)^{501/1000}$. Since $\ln 2\ge1/2$ and $501/1000<1$, this yields the stated unit coefficient with $\ln n$.

The original program's fast guards hold since $z>2^{48}+1$. The phase accuracy, full product and marked-space proofs use the same program and therefore continue to apply. The exact piecewise argument concerns this machine's fixed-exponent numerical cutoff; the smooth variable-exponent statement remains available separately. Prepared for Jerry Chen (@CubeJerry) with ChatGPT research assistance.
