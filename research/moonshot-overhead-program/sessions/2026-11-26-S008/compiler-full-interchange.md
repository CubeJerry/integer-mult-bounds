# A complete numerical binary interchange

For a binary field width $u\ge0$ and arbitrary positive occupied prefix, gap and suffix counts $p,g,h$, let $V=pgh\,2^{2u}$ be the number of independently specifiable bits. Set $\Phi(z)=(z^2\log_2(z+2))^{1/3}$. A fixed deterministic multitape machine performs the exact two-slot interchange on every such word, at cost
$$
 T_2(V,u)\le 5120\,V\sqrt{1+u}\;2^{156\Phi(\log_2(u+2))},
 \qquad S_2(V,u)\le 2{,}359{,}424\,V .
 \tag{1}
$$
Here space is the total number of tape/address cells ever visited. These are $A_I=5120$ and $B_I=156$ in the literal [selected Walsh supplier](walsh-node.md). In particular the selected Walsh layer's subsequent $\max(48,B_I+9)$ equals 165 for this root degree. The larger smooth coefficients 240, 288 and 576 also satisfy (1). Independently, a piecewise width potential gives the unit-coefficient result
$$
 T_2(V,u)\le V u^{501/1000}
 \quad\text{for}\quad
 \log_2 u\ge142{,}427{,}437{,}055{,}876{,}871 .
 \tag{2}
$$
The simpler condition $u\ge 2^{2^{57}}$ suffices. These are field-width cutoffs. The integer caller has its own width relation, other layers and threshold.

## The sharper child sum

Use the [numerical child-volume theorem](child-volume.md), including all three finite repair transforms, their retained row volumes, true padding and all full-volume reserve calls. At an adaptive node write $s=\log_2 m\ge2^{17}$, $l=\log_2(s+2)$, $U=\lceil s\rceil$, $v=\lceil\log_2(U+2)\rceil$. Let $d$ be the largest dyadic with $d^3v\le U$. If $\Lambda$ denotes the total volume of the issued native children divided by the true incoming volume, equation (4) of that theorem gives
$$
 q=\log_2(\Lambda/\sqrt m)\le 33+3s/d+d^2(l+3).
 \tag{3}
$$
The same $d$ occurs in both terms. Put $z=d(l/s)^{1/3}$. Then $z^3\le1+1/s$ and $z^3>l/(8v)$. Since $U+2\le s+3\le\sqrt{2}(s+2)$, one has $v\le l+3/2$ and $l/v\ge34/37>(31/32)^3$. Thus $31/64\le z\le33/32$. Furthermore $\Phi(s)\ge4096$ and $l\ge17$. The function $3/z+(20/17)z^2$ is decreasing throughout this interval, since $2(20/17)(33/32)^3<3$. Dividing (3) by $\Phi(s)$ gives the uniform bound
$$
 \frac{q}{\Phi(s)}
 \le \frac{33}{4096}+\frac{3}{31/64}+\frac{20}{17}(31/64)^2
 =\frac{13{,}982{,}555}{2{,}158{,}592}<\frac{13}{2}.
 \tag{4}
$$
This rounds the same scheduled child volume more tightly. No geometric incidence or reserve is deleted.

## A width potential for all native calls

For native ternary field width $e$, write $a=\max(1,e)$, $y=\log_2 a$ and $P_C(W,e)=W\sqrt a\,2^{C\Phi(y)}$. The native root degree is $R=4096$ and the direct/adaptive threshold is $E=2^{R(2^{17}+2)}$. The [numerical node](node-integrated.md) costs at most $256(e+1)W$ below $E$, and at most $m^{256}W$ in its own transitions above it, with equality $e=E$ in the adaptive branch. Each child has width $1\le f\le e/m$. Its input may depend on earlier replies. Its volume and width are still charged exactly once.

On an adaptive node, $y/R-1\le s\le y/R$. Define $L=\log_2(y+2)$, $r=Rs/y\le1$ and $\xi=\log_2(s+2)/L$. One has $r\ge1-R/y$ and $1-\xi\ge11/L$ because $(y+2)/(s+2)\ge R/2=2^{11}$. Also $y\ge RL$ on the entire domain. For example $\log_2(y+2)\le\sqrt y$ for $y\ge32$, by its value at 32 and its smaller derivative thereafter, and $y\ge R^2$. For $c=13/2$, take $C=(3/2)cR^{1/3}=156$. Monotonicity of the logarithm and concavity of the two power functions give
$$
\begin{aligned}
 C(\Phi(y)-\Phi(y-s))-c\Phi(s)
 &\ge cR^{-2/3}\Phi(y)[r-r^{2/3}\xi^{1/3}]\\
 &\ge cR^{-2/3}\Phi(y)[(1-\xi)/3-R/y]\\
 &\ge \frac{8c}{3}\left(\frac{y}{RL}\right)^{2/3}\ge\frac{52}{3}>2 .
\end{aligned}
 \tag{5}
$$
For the first line use $(1-s/y)^{2/3}\le1-2s/(3y)$; the positive logarithmic difference in $\Phi(s)/\Phi(y)$ pays the rounding loss in $m$. Combining (4), $\sqrt f\le\sqrt{e/m}$ and (5) bounds the sum of $P_C$ over *all* children by $P_C(W,e)/4$.

On a direct node $y<R(2^{17}+2)=536{,}879{,}104$. One has $y\le(2C)^3\log_2(y+2)$ all the way to that endpoint. Up to $2^{24}$ use $(2C)^3\ge2^{24}$, and above it use $24(2C)^3=728{,}911{,}872$. Therefore $C\Phi(y)\ge y/2$ and the direct time is at most $512P_C(W,e)$, including $e=0$. On an adaptive node $m^{256}\le e^{1/16}\le\sqrt e$. Induction on actual width, adding the local clock and at most a quarter of the inducted allowance, proves
$$
 T_3(W,e)\le512 W\sqrt{\max(1,e)}\,2^{156\Phi(\log_2\max(1,e))}.
 \tag{6}
$$
The union of all native visits is at most $2^{18}W$ by the arena proof. Only external binary calls use a range adapter.

The [physical range adapter](address-range.md) takes $n=2^u$, the smallest $t=3^e\ge n$, then pads and restricts both axes using at most $512V$ additional transitions and $128V$ additional visited cells in total. It has $e\le u$, $t<3n$ and $W=pgh\,t^2<9V$, also at $u=0$. Equations (6) and the adapter give (1), with $512+9\cdot512=5120$ and $128+9\cdot2^{18}=2{,}359{,}424$. This includes normalized output and arbitrary independently populated spectator ranges.

## A piecewise potential for the unit coefficient

A second consequence of (3) retains the actual dyadic scale. Since $d^3v\le s+1$, $v\ge17$ and $d\ge16$, one has $s\ge4096d$. Multiplying (3) plus 2 by $d$ gives
$$
 d(q+2)\le35d+3s+(s+1)(1+3/17)\le(17/4)s.
 \tag{7}
$$
Indeed $35d+20/17\le37d\le37s/4096<(5/68)s$, which is the available margin.

Let $Y_A=4096(2^{17}+2)$ and, for $5\le j\le13$, set
$$
 Y_j=4096((3j+6)2^{3j}+2).
$$
When $y\ge Y_j$ the chosen dyadic $d$ is at least $2^j$. In fact $U\ge(3j+6)2^{3j}$. If $v\le3j+6$ this proves $U\ge 2^{3j}v$ immediately. Otherwise $U>2^{v-1}-2\ge2^{3j}v$. The second inequality holds first at $v=3j+7\le46$, where $2^{v-1}=64\cdot2^{3j}$, and then by doubling for each increment of $v$.

Define a continuous, increasing, concave $H(y)$ with $H(0)=0$. Its slope is $1/2$ up to $Y_A$, then $17/(4\cdot2^4)$ up to $Y_5$. At $Y_j$ for $5\le j\le13$ change to slope $\lambda_j=17/(4\cdot2^j)$, retaining $\lambda_{13}$ for every $y\ge Y_{13}$. On each adaptive node with current slope $\lambda$, (7) gives $q+2\le\lambda s$, and $H(y)-H(\log_2 f)\ge\lambda s$ by concavity and $f\le e/m$. The sum over children of $W_i\sqrt f\,2^{H(\log_2 f)}$ therefore costs at most one quarter of $W\sqrt e\,2^{H(y)}$, even if a child crosses several width thresholds. Before $Y_A$ this parent potential equals $W\max(1,e)$; the adaptive local bound and native width induction work exactly as above. Thus for $u\ge1$ the full binary machine satisfies
$$
 T_2(V,u)\le5120\,V\sqrt u\,2^{H(\log_2u)} .
 \tag{8}
$$

Exact integer additions over the nine finite intervals give
$$
 Y_{13}=101{,}330{,}991{,}615{,}844{,}352,\qquad
 H(Y_{13})=121{,}106{,}649{,}321{,}472 .
$$
For $y\ge Y_{13}$, $H(y)=H(Y_{13})+(17/32768)(y-Y_{13})$. Since $\log_2 5120<13$, the linear condition $H(y)+13\le y/1000$ suffices for (2). Its crossing occurs at
$$
 \frac{H(Y_{13})-(17/32768)Y_{13}+13}{1/1000-17/32768}
 =\frac{93{,}574{,}826{,}145{,}711{,}104{,}000}{657}.
$$
Taking the ceiling gives (2). The [rational replay](compiler-interchange-check.py) recomputes the interval values and both rational comparisons, checks actual integer child invoices around their parameter boundaries, and verifies positivity across root switches. The complete machine and the recurrence are written results built on the frozen finite identities, the [independent native review](compiler-native-review.md) and the [independent child recount](routing-review-child.md). The fixed-exponent cutoff is a sufficient upper bound for this implementation.

Prepared for Jerry Chen (@CubeJerry) with ChatGPT research assistance. S003 and AQ-P supplied the finite algebra and recursive program. S008 supplies the numerical clock, physical adapter, sharper uniform comparison and finite-width crossover.
