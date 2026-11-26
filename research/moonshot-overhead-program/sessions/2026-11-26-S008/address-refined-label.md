# Eventual coefficient 53 from the true label width

For the same fixed $R=240$ integer multiplier with its $X=2^{24}$ outer Walsh guard, put $L=1+\log_2 n$, $x=\log_2 L$ and $\Phi(x)=(x^2\log_2(x+2))^{1/3}$. For every sufficiently large $n$,
$$
 T(n)\le n\sqrt L\,2^{53\Phi(x)},\qquad S(n)\le 2^{32}n.
$$
The proof computes the exact asymptotic envelope of one continuous upper bound using the actual label word length. Its logarithmic overhead coefficient has upper limit
$$
 8+\sqrt[3]{240}\left(7+\frac{\ln 2}{3}\right)
     =52.9371013839\ldots .
$$
This is a property of the charge used to prove an upper bound. The [all-input coefficient 63](address-native-staircase.md) and the [finite unit-coefficient $0.501$ threshold](address-review-profile.md) supply separate explicit range statements. The [effective continuation](coefficient-53.md), with an [independent proof check](compiler-review-refined-label.md#a-numerical-guard), proves the coefficient 53 when $\log_2\log_2n\ge2^{69110}$.

## The actual child invoice

Use $\sigma=\log_2(\sum_iV_i/(V\sqrt m))$ for the complete native child list and $s=\log_2m$. In the notation of [the finite ternary label construction](../../routes/B/characteristic-two-label-geometry.md) and [its audited numerical invoice](child-volume.md), $d\ge16$ is dyadic, $h_0=2d-1$, $t=\lceil (s+2d^2-2)/d^2\rceil$, $q=2^t$, and
$$
 2^\sigma\le2^{33}D_g(1+\lambda),\quad D_g=4+2h_0q^{h_0},\quad
 \lambda\le {h_0\choose d}^{d+1}(q-1)^d t^{d(d-1)} .
$$
The finite $t^{d(d-1)}$ factor here uses the true number of bits per letter. From $D_g\le8h_0q^{h_0}$ and the binomial upper bound $2^{h_0}$,
$$
 \sigma+2\le39+\log_2 h_0+(d+1)h_0+(h_0+d)t+d(d-1)\log_2t.
$$
We have $t\le s/d^2+3$, $\log_2h_0\le d$, and $(d+1)h_0\le 2d^2+2d$. Because $39+12d\le d^2$ at every $d\ge16$, the actual complete invoice satisfies
$$
 \sigma+2\le 3s/d+d^2(\log_2 t+3). \tag{1}
$$
The [kernel-checked cardinality transfer](address-refined-cardinality.lean) derives (1) directly from the displayed total mass and binomial/letter alphabet bound for all positive integral bit widths, verifying the logarithm, dimension, degree and multiplicative inequalities. The independent coarse estimate $(\sigma+2)/s\le17/(4d)$ remains available when the actual degree is larger than the guaranteed candidate.

## A continuous concave native majorant

Write $R=240$, $y=\log_2e$, and use the previously proved [integer degree thresholds](address-native-staircase.md). At band $j\ge4$, put
$$
 D=2^j,\quad Q_j=3j+\lceil\log_2(3j+3)\rceil+2,\quad
 S_j=R(Q_jD^3+2),\quad U_j=8Q_{j+1}/Q_j .
$$
If $S_j\le y<S_{j+1}$, let $p=y/R-2$ and $\tau=p/(Q_jD^3)$. Then $1\le\tau<U_j$, $p+1\le s\le p+2$, and the actual degree is at least $D$. Also $Q_{j+1}\le Q_j+4\le2Q_j$, $U_j\le16$, $Q_j/(3j)\to1$, and $U_j\to8$.

In this band define
$$
 E_j=\frac{j+\log_2(8Q_{j+1}+1)+3}{Q_j},\qquad
 \rho(y)=\frac{3+E_j/\tau}{D}.
$$
If the actual $d=D$, then $t\le (p+2)/D^2+3\le D(8Q_{j+1}+1)$, since $p<8Q_{j+1}D^3$ and $D\ge16$. By (1) and $s\ge p$, its one-width charge $(\sigma+2)/s$ is at most $\rho(y)$. If $d>D$, the next possible degree is at least $2D$ and the coarse invoice gives $(\sigma+2)/s\le17/(8D)<3/D$. Thus $\rho$ covers every actual node. We have $0<E_j<2$ and $E_j\to1/3$. For the uniform upper bound use $Q_j\ge18$, $8Q_{j+1}+1\le16Q_j+1\le2^{Q_j-3}$, and $j<Q_j$.

Let $H_*(0)=0$ with slope $1/2$ through $y_A=R(2^{17}+2)$, the existing direct-width cutoff. From there define $H_*$ by integrating the above $\rho(y)$. The switch is inside the $j=4$ band. The new slope there is below $5/16<1/2$. Inside each band it decreases, and at an interband switch the previous left slope is at least $3/D$, while the new right slope is at most $5/(2D)$. Thus $H_*$ is increasing and concave everywhere. Boundaries may use their right slope. For every child $1\le f\le e/m$,
$$
 H_*(y)-H_*(\log_2 f)\ge s\rho(y)\ge\sigma+2 .
$$
This yields the same quarter of the native potential, native direct base, adaptive local charge and external adapter, with $H_*$ as shape. In particular the physical binary caller of positive slot width $u$ still costs at most $5120 V\sqrt u\,2^{H_*(\log_2u)}$. The unbounded function and its logarithms are never evaluated by the machine.

## Exact limiting coefficient of this native majorant

For $j\ge5$ put $b_j=H_*(S_j)/(R D^2Q_j)$. Integrating across a whole band gives
$$
 b_{j+1}=\frac{Q_j}{4Q_{j+1}}
       \big[b_j+3(U_j-1)+E_j\ln U_j\big]. \tag{2}
$$
The coefficient of $b_j$ is at most $1/4$ and tends to $1/4$. The bracket's inhomogeneous term is bounded and tends to $21+(\ln8)/3$. Hence the sequence is bounded and
$$
 b_j\longrightarrow b=7+\frac{\ln 2}{3}.
$$
Indeed (2) minus its limiting fixed point gives $b_{j+1}-b=r_j(b_j-b)+o(1)$ with $0\le r_j\le1/4$, forcing the limsup of the absolute difference to vanish.

At any $y=R(Q_jD^3\tau+2)$ in this band the exact normalized height equals $b_j+3(\tau-1)+E_j\ln\tau$, in units of $R Q_jD^2$. Uniformly for $1\le\tau\le U_j$, the quotient $\Phi(y)/(R^{2/3}Q_jD^2\tau^{2/3})$ tends to one. Its cube is
$$
\left(1+\frac{2}{Q_jD^3\tau}\right)^2
 \frac{\log_2(R(Q_jD^3\tau+2)+2)}{Q_j},
$$
and the numerator logarithm is $3j+\log_2Q_j+O(1)$ uniformly since $\tau\le16$. Consequently the limiting normalized function on $1\le\tau\le8$ is
$$
 F(\tau)=\frac{b+3(\tau-1)+(\ln\tau)/3}{\tau^{2/3}}.
$$
Its derivative has the sign of $\tau+1/3+2-2b/3-(2/9)\ln\tau$, which is strictly increasing on this interval. The maximum therefore occurs at an endpoint. The fixed-point identity gives $F(1)=F(8)=b$. Uniform convergence on the bounded range and $U_j\to8$ prove the upper bound, and $\tau=1$ in every band realizes the limiting value. Thus
$$
 \limsup_{y\to\infty}\frac{H_*(y)}{\Phi(y)}
      =\alpha_*=\sqrt[3]R(7+\ln(2)/3).
$$

The formal [continuous-band certificate](address-refined-curve.lean) proves the limiting endpoint bound and the numerical $M=1447/200$, $E=167/500$, $U\le8001/1000$ version used in the effective continuation. It also verifies (1) from its expanded logarithmic cardinality invoice. A direct Jensen argument gives an alternative to the derivative test. Put $r=\tau^{1/3}$ and subtract $M r^2$ from $h+3(r^3-1)+3E\ln r$. For two cube roots $a,b\ge1$ and $r=pa+qb$ with $p+q=1$, $p,q\ge0$, write $v=pq(b-a)^2$. Then
$$
 \ln r-p\ln a-q\ln b\le v/(ab)\le v
$$
by applying $\ln u\le u-1$ to $r/a$ and $r/b$. The corresponding cubic and square Jensen differences are $v(a+b+r)$ and $v$. Thus the weighted endpoint residual minus the interior residual is at least $v[3(a+b+r)-M-3E]\ge0$ when $M+3E\le9$, which holds in both applications. This proves the maximum assertion on the complete real interval, including its endpoints.

## Fourier and full-integer transfer

The [true-slot Walsh movement invoice](walsh-node.md#only-actual-column-maps-use-the-interchanger) after dividing by $\sqrt a$ has $m^8$ remaining: the factor $\sqrt{f/a}$ pays $m^{-1/2}$ from $m^{17/2}$. For adaptive log-width $x$, the *actual* $m=2^{Y(x)}-1$ with
$$
 Y(x)=\left\lceil(x^2\lceil\log_2(x+2)\rceil)^{1/3}\right\rceil .
$$
The two ceiling errors show $Y(x)/\Phi(x)\to1$. In particular $m^8\le2^{8Y(x)}$. Define $Y$ by this same formula on all nonnegative real arguments and consider
$$
 G_*(x)=48\Phi(x)+
 \max\left\{0,\ \sup_{0\le v\le x}\big[H_*(v)+8Y(v)-48\Phi(v)\big]\right\}.
$$
Use a supremum to allow the upward ceiling jumps. Every bounded interval has a finite value. The excess above $48\Phi$ is nondecreasing, preserving the complete [Walsh spatial quarter](walsh-child-clock.md). At the current node, $G_*(x)\ge H_*(x)+8Y(x)$, which pays the actual local slot because $\log_2 f\le x$ and $H_*$ increases. Direct widths, finite additions, and the outer CRT and placements use the same constants as the [widened Walsh supplier](address-native-staircase.md). In particular $G_*(x)\ge H_*(x)$ throughout.

Since $\alpha_*+8>48$, the historical maximum gives
$$
 \limsup_{x\to\infty}G_*(x)/\Phi(x)=\alpha_*+8.
$$
For the upper inequality split the supremum at a fixed large $v_0$. The earlier bounded contribution divided by $\Phi(x)$ vanishes. For $v\ge v_0$, any positive contribution is at most $(\alpha_*+8-48+\varepsilon)\Phi(v)\le(\alpha_*+8-48+\varepsilon)\Phi(x)$. For the lower inequality evaluate the uncorrected expression at $v=x=S_j$ and let $j$ grow. The leading factor $8$ here uses actual arities and thus differs from the uniform all-width allowance $33/4$.

The complete joined integer invoice has logarithmic excess above $n\sqrt{\log_2 n}$ bounded by $182+4\log_2(z+2)+G_*(z+2)$ for $z=\log_2\log_2n$. The function $G_*$ is increasing, and $\Phi(z+2)/\Phi(z)\to1$ and $\log_2(z+2)/\Phi(z)\to0$. The excess divided by $\Phi(z)$ therefore has limsup at most $\alpha_*+8$. Finally $\ln2<7/10$ by the degree-three positive exponential series at $7/10$, and the rational inequality $240(217/30)^3<45^3$ proves $\alpha_*+8<53$. The strict gap absorbs the outside constant and logarithmic costs at all sufficiently large lengths, with the asserted unit multiplicative coefficient. The complete returned integer words and common total visited space obey the same proof as the all-input result.

Prepared for Jerry Chen (@CubeJerry) with substantial ChatGPT research assistance.
