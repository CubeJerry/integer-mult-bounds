# Independent review of the unit-coefficient threshold after the staircase improvement

Let $z=\log_2\log_2 n$, $x=z+2$, and let $H$ be the full infinite three-slope native majorant in [the uniform proof](address-native-staircase.md). The complete integer invoice and one exponent bit for the natural-log output convention require
$$
  183+4\log_2(z+2)+48\Phi(x)
       +\max_{0\le u\le x}\{H(u)-(159/4)\Phi(u)\}\le z/1000.
$$
The maximum includes $u=0$, where the expression is zero. The concavity of $\Phi$ makes the expression convex on each affine span of $H$, so it suffices to evaluate the exact knot heights and the terminal point $x$.

I independently evaluated all 30 arguments at $z=8931714897907030$ and at $z-1$. [The checker](address-review-profile.py) implements its own binary-logarithm intervals and integer cube roots. After writing a positive integer as $2^e r$ with $1\le r<2$, it bounds $\ln r$ by 52 terms of $2\operatorname{artanh}((r-1)/(r+1))$ and the explicit geometric tail beginning at degree 105. All denominators use rational arithmetic. Dividing by an independently enclosed $\ln2$ gives $\log_2$. Each profile is then outward-rounded on a 112-bit binary grid by a checked integer cube root. At both adjacent arguments the terminal point strictly wins against every earlier knot, including the origin.

| $z$ | certified interval for $10^{12}$ times the residual (right side minus left side) |
|---:|---:|
| 8,931,714,897,907,029 | $[-133976519,-133976518]$ |
| 8,931,714,897,907,030 | $[246303494,246303495]$ |

The larger endpoint controls the entire tail. Put $x_0=z_0+2$. At $u\le x_0$ the historical term is no larger than the computed prefix maximum $D=H(x_0)-(159/4)\Phi(x_0)\ge0$. The three terms after division by $z$ then involve $1/z$, $\log_2(z+2)/z$, and $\Phi(z+2)/z$, all decreasing. For $x_0\le u\le x$, concavity of $H,\Phi$ from the origin gives $H(u)\le (u/x_0)H(x_0)$ and $\Phi(u)\ge (u/x)\Phi(x)$. The resulting envelope is a linear interpolation, with weight $u/x$, between $48\Phi(x)$ and $(x/x_0)H(x_0)+(33/4)\Phi(x)$. The former is already covered by the old prefix. In the latter case $(x/z)H(x_0)/x_0$ and $\Phi(x)/z$ decrease in $z$. At the starting endpoint this second expression is exactly the tested terminal invoice. This proves the inequality for every later real $z$.

The independent replay certifies the sharper sufficient threshold for the actual whole-program invoices. It establishes at that threshold the unit coefficient against $n(\ln n)^{501/1000}$, by the same [integer-logarithm convention conversion](routing-piecewise-walsh.md). The two adjacent signs concern the stated sufficient invoice.

## Refinement using the true letter length

Keeping the integer knots and replacing a band slope by $(3+\bar E_j/a)/2^j$ for $a=1,2,4$, with $\bar E_j=(j+\lceil\log_2(8Q_{j+1}+1)\rceil+3)/Q_j$, gives a further rational upper bound by [the true-label inequality](address-refined-label.md). The original $y_A$ divides the $j=4,a=1$ interval. The independent script also implements these slope changes and evaluated all 30 possible maxima at both new adjacent arguments. This time the earlier breakpoint $S_{13,1}=6201245580657120$ strictly won on both checks, including comparison against the actual terminal point.

| $z$ | certified interval for $10^{12}$ times the residual |
|---:|---:|
| 7,519,517,465,920,987 | $[-325836553,-325836552]$ |
| 7,519,517,465,920,988 | $[53248687,53248688]$ |

The same tail proof applies with $D$ equal to the actual earlier maximum. At $x_0$, the second density bound $H(x_0)+(33/4)\Phi(x_0)$ passes because the current surplus is strictly less than $D$. The first bound $48\Phi(x_0)+D$ passes by the positive residual. Both decrease after division by $z$ exactly as above. Thus $z\ge7519517465920988$ suffices for the unit-coefficient natural-log bound on every later input length. The previous integer fails this particular complete charge.

Prepared for Jerry Chen (@CubeJerry) with substantial ChatGPT research assistance.
