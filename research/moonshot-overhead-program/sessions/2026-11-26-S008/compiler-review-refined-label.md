# Independent review of coefficient 53 and its effective onset

The counted $R=240$ multiplier satisfies, with $L=1+\log _2 n$, $x=\log _2 L$ and $\Phi(x)=(x^2\log _2(x+2))^{1/3}$,

$$T(n)\le n\sqrt L\,2^{53\Phi(x)}\qquad\text{whenever}\qquad \log _2\log _2 n\ge2^{69110}.$$

The normalized logarithmic excess over $n\sqrt{\log _2 n}$, divided by $\Phi(\log _2\log _2n)$, has upper limit at most $8+240^{1/3}(7+(\ln2)/3)=52.9371013839181\ldots$. The existing through-halt cap is $2^{32}n$. The cutoff above applies to the coefficient 53. The independent fixed-exponent $0.501$ statement has its own much smaller onset. [Time envelope](address-refined-label.md) · [Effective threshold](coefficient-53.md) · [Native transition ledger](node-root-parameter.md) · [Complete integer ledger](integer-clock.md)

## Actual labels, widths and recursive events

Take $\sigma=\log _2(\sum V_i/(V\sqrt m))$ and $s=\log _2m$. The frozen count already includes the two predictors in every internal finite node, all three order-three words, contracted leaves, the true leading padding, and the $2a$ unpadded full-volume reserves. Its bound is $2^\sigma\le2^{33}D_g(1+\lambda)$. With $h_0=2d-1$, actual letter length $t$ and $q=2^t$, the regular rectangle estimate is $\lambda\le\binom{h_0}{d}^{d+1}(q-1)^d t^{d(d-1)}$. Taking logs in the two separate factors gives

$$\sigma+2\le39+\log _2h_0+(d+1)h_0+(h_0+d)t+d(d-1)\log _2t.$$

Indeed $D_g\le 8h_0 q^{h_0}$, the displayed rectangle majorant is at least one, and the additional two exponent units pay the child quarter. From $t\le s/d^2+3$, $h_0+d<3d$, $\log _2h_0\le d$ and $39+12d\le d^2$ at $d\ge16$, this is bounded by $3s/d+d^2(\log _2t+3)$. The improvement uses the true word length in the existing label formula, without changing the program. [All-child source invoice](child-volume.md) · [Label geometry](../../routes/B/characteristic-two-label-geometry.md)

Put $D=2^j$, $Q=3j+\lceil\log _2(3j+3)\rceil+2$, $Q'=Q_{j+1}$, $S_j=240(QD^3+2)$. With $y=\log _2 e\in[S_j,S_{j+1})$, set $p=y/240-2$, $T=p/(QD^3)$ and $U=8Q'/Q$. For the actual odd-root rounding, $p+1\le s\le p+2$. The integer degree predicate gives $d\ge D$. One proof is to put $b=\lfloor\lceil s\rceil/D^3\rfloor\ge Q$. At $Q$ the inequality $b+3\le 2^{b-3j}$ holds, and doubling preserves it at every subsequent integer $b$. Therefore $\lceil\log _2(\lceil s\rceil+2)\rceil\le b$. [Literal degree predicate](address-native-staircase.md)

For $d=D$, $t\le D(8Q'+1)$ because $T<U$ and $D\ge16$. Thus $(\sigma+2)/s\le(3+E_j/T)/D$, where $E_j=(j+\log _2(8Q'+1)+3)/Q$. When the actual degree switches early, $d\ge2D$ and the older uniform bound gives $(\sigma+2)/s\le17/(8D)<3/D$. Both branches are required because the guaranteed interval can span two actual degrees. The proposed derivative $\rho=(3+E_j/T)/D$ decreases across the band. As $0<E_j<2$, its right value at the next switch is below $5/(2D)<3/D$. The native direct slope $1/2$ dominates its first adaptive derivative as well. The integral $H$ is concave and increasing. Consequently $H(y)-H(\log _2f)\ge s\rho(y)\ge\sigma+2$ for every current child, even across earlier bands. None of $H$, the logarithms, or the suprema below is evaluated on tape. [Range adapter and child potential](compiler-full-interchange.md)

## Normalization at the degree switch

Let $b_j=H(S_j)/(240QD^2)$. Integration gives

$$b_{j+1}=r_j[b_j+3(U-1)+E_j\ln U],\qquad r_j=Q/(4Q').$$

Since $Q/(3j)\to1$, $r_j\to1/4$, $E_j\to1/3$ and $U\to8$. Also $r_j\le1/4$ for every band. Subtracting the limiting fixed point and taking the upper limit of the absolute difference proves $b_j\to b=7+(\ln2)/3$. At $y=240(QD^3T+2)$ the exact integrated height in the same units is $b_j+3(T-1)+E_j\ln T$. Its natural limiting divisor is $T^{2/3}$, since $\log _2(y+2)/Q=(3j+\log _2 Q+O(1))/Q\to1$ uniformly over $1\le T\le U\le16$.

The sign of the derivative of $F(T)=[b+3(T-1)+(\ln T)/3]/T^{2/3}$ equals the sign of

$$T-7/3-(2/9)\ln(2T).$$

This expression is strictly increasing for $T\ge1$. The maximum on $[1,8]$ is at an endpoint and $F(1)=F(8)=b$. Uniformity on the moving intervals follows by extending this formula to $[1,16]$, using $U\to8$ and continuity at eight. The knots $T=1$ attain the limiting height of this majorant. Thus $\limsup H(y)/\Phi(y)=240^{1/3}b$.

At Walsh log-width $v$, its rounded log-arity is $Y(v)=\lceil(v^2\lceil\log _2(v+2)\rceil)^{1/3}\rceil$, so $Y(v)/\Phi(v)\to1$. The exchanged slot has $f/a\le1/(2m)$, leaving $m^8$ after paying the $\sqrt f$ in the actual interchange. Define $G(x)$ as $48\Phi(x)$ plus the running supremum of the positive part of $H(v)+8Y(v)-48\Phi(v)$ over $0\le v\le x$. At the node itself $G(x)\ge H(x)+8Y(x)\ge H(\log _2 f)+8Y(x)$. The arity expense here belongs to the parent, even when its recursive child or true exchange slot is much thinner. The excess $G-48\Phi$ is nondecreasing, so the existing spatial quarter still holds. Ordinary events already fit below the coefficient 48. Splitting the supremum at any fixed large $v_0$ gives $\limsup G/\Phi=8+240^{1/3}b$, since values at $v=x=S_j$ supply the reverse inequality for the majorant. The fixed costs, shifts by 2 and logarithmic outer overhead give the stated upper limit for the integer time invoice. [Walsh local movement](walsh-node.md) · [Spatial contraction](walsh-child-clock.md)

## A numerical guard

For $j\ge J=11500$, $Q'\le4j$. It suffices that $3j+6\le2^{j-5}$, true at 11 and preserved at the next integer by doubling. Also $9+\log _2(j+2)\le j/500$, because its ratio to $j$ decreases and $11502<2^{14}$. Hence $E_j\le167/500$ and $U\le8+32/(3j)<8001/1000$. The positive Taylor polynomial for $\exp(21/10)$ through degree seven exceeds $8001/1000$, so $\ln U\le21/10$.

The recurrence is equivalently $b_{j+1}=6+r_j(b_j-3+E_j\ln U)$. All $b_j\le20$ from $j=5$: the initial value is below 17 by $H(y)\le y/2$, and the recursion preserves 20 using $E_j<2$, $U\le16$ and $\ln16<3$. At $j\ge J$ the positive excess over $h_0=36169/5000$ contracts by a factor at most $1/4$, since $6+(h_0-3+(167/500)(21/10))/4=h_0$. After ten bands $b_j\le M=1447/200$ for all $j\ge11510$. On each interval, substitute $M$ and $167/500$ into the normalized numerator. The derivative sign is again strictly increasing. At the right endpoint $T=8001/1000$ the numerator is at most $4M-3/5000$, and $T^{2/3}\ge4$. At the left endpoint it equals $M$. Since $\log _2(y+2)\ge Q_j$ throughout, $H(y)\le44.97\Phi(y)$ from $v_0=S_{11510}$ onward. The exact cube margin $(44.97)^3-240M^3$ is $50622783/1000000$.

Above $v_0$ both $\log _2(v+2)\ge1000$ and $\Phi(v)\ge2000$ hold. The logarithm ceiling contributes at most $1/3000$ relatively after the cube root and the outer ceiling at most $1/2000$, so $Y(v)\le1.001\Phi(v)$. Earlier the slope gives $H(v)\le v/2$ and $Y(v)\le v+3$. Their total positive historical surplus is at most $10(v_0+3)$. At $x\ge(4v_0)^2$ we have $\Phi(x)\ge\sqrt x\ge4v_0$ and $4.978\Phi(x)\ge10(v_0+3)$. Thus $G(x)\le52.978\Phi(x)$. Exact integer arithmetic gives $Q_{11510}=34548$ and $\operatorname{bitlength}((4v_0)^2)=69110$.

For $z=\log _2\log _2 n\ge2^{69110}$ the full logarithmic invoice over $n\sqrt{\log _2n}$ is at most $182+4\log _2(z+2)+52.978\Phi(z+2)$. Already at $z\ge2^{30}$, $4096\log _2(z+2)\le z$ by the decreasing logarithm-to-width ratio. Cubing gives $4\log _2(z+2)\le\Phi(z)/64$. The shift bound $\Phi(z+2)\le\Phi(z)+2$ and the remaining slack $(53-52.978-1/64)\Phi(z)=(51/8000)\Phi(z)$ cover $182+2(52.978)+1$, since $\Phi(z)\ge2^{20}$. This proves the unit multiplicative coefficient with an extra bit available. [Profile shift](whole-profile.lean)

The exact-rational replay checks the degree predicates at 5,083 real-program rounded arities, including 884 earlier switches to a larger degree. Additional finite checks compare 1,799 monotone quadrature intervals with the antiderivative and 999 interior limiting heights with their endpoint maximum. The scalar estimates for every later input follow from the inequalities above. Reviewed Git blobs are `979ef92e48e6fd0f59b060a9c94635f0567280de` for the limiting proof, `815fd26344d5082599ff69d035bfbeb998ebf4ad` for the complete child sum and `dc4f8fc8c7d822aac8ea1f5d9cf5d5f5bbe962f7` for the dyadic width predicate. [Independent replay](compiler-review-refined-label.py)

Prepared for Jerry Chen (@CubeJerry) with substantial ChatGPT research assistance.
