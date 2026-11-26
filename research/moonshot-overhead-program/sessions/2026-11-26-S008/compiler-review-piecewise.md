# Independent review of the piecewise whole-integer threshold

I checked [the piecewise Walsh and integer transfer](routing-piecewise-walsh.md) at blob 1443114ff74a1803334115ac88965ed0c230aac6 against the native width staircase, the actual separated Walsh move, its spatial quarter and the integer packing. These inputs imply

$$
  T(n)\le n(\log_2 n)^{501/1000}
  \quad\text{when}\quad \log_2\log_2n\ge 11{,}665{,}715{,}140{,}844{,}862 .
$$

The parent program uses the independently priced $R=240$ and leaves the staircase as a proof bound. On a node at width $x$, the historical surplus
$$
 M(x)=\max(0,\max_{0\le z\le x}[H(z)-(159/4)\Phi(z)])
$$
is nondecreasing. Thus the existing child quarter for $48\Phi$ persists for $G=48\Phi+M$. Further, $G(x)\ge H(v)+(33/4)\Phi(x)$ for every $v\le x$, since $\Phi(v)\le\Phi(x)$. In the issued local slot the factor $\sqrt{f/a}\le1/\sqrt{2m}$ pays half a power of $m$, leaving $m^8$ in the actual $m^{17/2}$ local routing bill. Its logarithm costs at most $(33/4)\Phi(x)$. The $m^{45}$ ordinary term fits $48\Phi(x)$. The constant terms fit the published $A_W$. These checks preserve the list of data-bearing calls. The larger root placements and CRTs use $G(X)\ge H(\log_2 k)$.

The weighted geometric mean $a^{2/3}b^{1/3}$ is jointly concave and increasing in both arguments. Its composition with $a=x$ and $b=\log_2(x+2)$ proves concavity of $\Phi$ on the closed nonnegative domain. Consequently $H-(159/4)\Phi$ is convex on each affine part and its maximum on every closed subinterval occurs at an endpoint. I separately summed the actual $R=240$ slopes and obtained $Y_{13}=5{,}937{,}362{,}789{,}990{,}880$, $H(Y_{13})=7{,}096{,}092{,}733{,}680$ and the final intercept $4{,}112{,}174{,}977{,}105{,}665/1024$. The previous height is $1{,}654{,}234{,}951{,}920$. The final breakpoint excess is less than $2{,}220{,}000{,}000{,}000$ by rational cubing. This supplies the two candidate terms at every larger width.

For $t=\log_2\log_2n$, $Nk\le16n$ and $k\le\log_2n$ convert the joined clock to the two scalar tests at $t+2$. Both $\log_2(t+2)/t$ and $\Phi(t+2)/t$ decrease on this domain. For the second quantity, cube it to obtain $(1+2/t)^2\log_2(t+4)/t$. Its factors are positive and decreasing. The affine contribution divided by $t$ also decreases. Thus the left-endpoint comparisons cover the full real interval thereafter.

The [independent rational replay](compiler-review-piecewise.py) calculated 112 bits of each binary logarithm by repeated squaring, starting from the exact normalized dyadic argument. Squaring, thresholding against 2 and optional halving took place on a 400-bit fixed grid with outward rounding at every operation. The side of 2 on which the squared interval lies fixes its next binary logarithm digit. All 112 decisions were resolved. At 11,665,715,140,844,861, the historical test passed and the movement test failed. At the stated next integer both passed. Both also passed at 11,700,000,000,000,000. Those adjacent signs concern this two-term sufficient test. The numerical space proof and the scientific scope of the complete written integer construction are given in [the joined program](integer-clock.md).
