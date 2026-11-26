# Complete movement clock with the three native slopes

Let $t=\log_2\log_2 n$. For the $R=240$ integer multiplier, counting physical tape transitions through the final output, the stronger high-width conclusion is

$$
t\ge8{,}931{,}714{,}897{,}907{,}030
\quad\Longrightarrow\quad T(n)\le n(\ln n)^{501/1000}.
$$

This statement covers both the original $X=2^{26}$ and revised $X=2^{24}$ global Walsh dispatchers. At these input lengths both execute the same procedure. The exponent checkpoint $9\cdot10^{15}$ is a simpler sufficient value. The [all-input bound](address-native-staircase.md) at coefficient 63 uses the revised dispatcher. Their visited-cell bound is $2^{32}n$.

## Review of the shared native statistic

Use the [three-slope supplier](address-native-staircase.md) and its [rational checker](address-native-staircase.py). At $y=\log_2 e$ the true native arity has $s=\log_2 m\ge y/240-1$. For $D=2^j$, put $Q=3j+\lceil\log_2(3j+3)\rceil+2$. At $s\ge QD^3$, let $U=\lceil s\rceil$ and $b=\lfloor U/D^3\rfloor$. The base inequality $b+3\le2^{b-3j}$ holds at $Q$ and persists by doubling. Thus $U+2<2^b$, and the selected dyadic degree $d$ satisfies $d\ge D$. All transfers below act on the actual arity and all issued calls.

When $d=D$, the all-child invoice gives

$$
 (\sigma+2)/s\le 3/D+
 D^2[\log_2(s+2)+3+35/D^2]/s.
$$

The last ratio decreases. For $s\ge aQD^3$ its bracket at the left endpoint is at most $4Q/3$. This yields slopes $(11/3)/D$ and $(10/3)/D$ at $a=2,4$. At $a=1$ use the independent $(17/4)/D$ bound. When $d>D$, its dyadic jump gives the still smaller $17/(8D)$ throughout. The right slopes decrease at every switch, including between degree bands. The resulting continuous $H$ with $H(0)=0$ is concave and increasing. Crossing multiple switches in one native call only increases its available potential drop.

The normalized heights $h_j=H(S_{j,1})/(240D^2Q_j)$ satisfy

$$
 h_5=577283/67584,\qquad
 h_{j+1}=20/3+\frac{Q_j}{4Q_{j+1}}(h_j-7/4).
$$

This follows by adding the three interval lengths times their slopes. The bound $h_j\le43/5$ is invariant. At all three later vertices the exact cubings $240c_a^3<(433/8)^3 a^2$ from the supplier suffice. At the three early positive vertices, independent summation gives heights 15,728,880, 16,773,360 and 24,883,440; respective lower log bounds are $124/5,25,26$. In particular $(31{,}457{,}762)^5>2^{124}$. Using concavity of $\Phi$ on each affine segment gives $H(y)\le(433/8)\Phi(y)$ for every $y\ge0$. The native interchanger and its direct/adaptive guard are unchanged.

In the widened global Walsh range the actual candidate-enumeration invoice is bounded by $2^{m^{55}+11+16m^3}m^{129}<2^{m^{56}}$. The existing denominator bound at $X\ge2^{24}$ gives $Y\le X/64+1$ and hence $56Y\le15X/16\le X-7$. Thus $m^{56}\le k/32$, while $2000X\le k/32$ still pays the controller powers. Applying these two inequalities to the original $m^{60}$-multiple shows the complete setup costs below $2^{k/4}$, less than the actual $2^{k/3}$ leading spectator reserve. Each finite catalogue uses at most $m^{55}$ bits. The modulus, staged mask and cumulative-bank bounds continue to hold. Applying the typed movement at $f/a\le1/(2m)$ gives $B_W=433/8+33/4=499/8$. At $z\ge4096$ one has $4\log_2(z+2)\le\Phi(z)/12$ and $\Phi(z)\ge576$; the exact inequality $(63-499/8-1/12)576\ge182+2(499/8)+1$ completes the outer smooth join. The small and middle branches use the separately priced raw and dyadic programs. This verifies the published all-length 63 variant and its single changed guard.

The original global direct branch at $X<2^{26}$ can also pay $48\Phi(X)$ using the older, larger prefactor. Its direct comparison gives $X/2\le70\Phi(X)$ and $\Phi(X)\le2^{19}$, by cubing with $X^2\log_2(X+2)\le2^{52}\cdot27$. Hence the excess is at most $22\cdot2^{19}<2^{24}$. This observation uses $A_W=2^{2^{24}+28}(1+5120)$; the smaller prefactor in the all-input 63 result uses the revised global guard.

## A decreasing density for the full history

Write $P=\Phi$, $L=48$, $\gamma=33/4$, $c=L-\gamma=159/4$. The historic Walsh potential is

$$
 G(x)=L P(x)+\max\{0,\max_{0\le v\le x}(H(v)-cP(v))\}.
$$

The [typed-width proof](routing-piecewise-walsh.md) uses this $H$ without changing any location, coefficient, arity or adaptive local call. In particular a true local direct width $x<2^{24}$ costs at most $2^{19}V\sqrt a\,2^{48\Phi(x)}$ by the [base invoice](walsh-node.md). Every nonbase ordinary and data bill has room under $A_W=2^{110}(1+5120)$. The parent pays its real inherited reserve exactly once and the historical surplus preserves the paid spatial quarter.

For $t\ge z>0$, both $H(t)/t$ and $P(t)/t$ are nonincreasing because the functions are concave and vanish at zero. The same holds for $G(t)/t$. To prove this, for $v\le z$ a nonpositive surplus is already covered by $LP(t)$; a positive fixed surplus divided by $t$ decreases. For $z\le v\le t$ put $r=v/t$. Then $H(v)\le vH(z)/z$ and $P(v)\ge rP(t)$. Consequently

$$
 \frac{LP(t)+H(v)-cP(v)}{t}
 \le (L-cr)\frac{P(t)}t+r\frac{H(z)}z
 \le\frac{(1-r)LP(z)+r[H(z)+\gamma P(z)]}{z}
 \le G(z)/z .
$$

The [kernel-checked density theorem](routing-density.lean) proves this inequality for an arbitrary earlier charge and real outer scale. The zero-surplus contribution satisfies the same inequality. In particular $G(t+2)/t$ decreases, as the product of $G(t+2)/(t+2)$ and $(t+2)/t$. The other normalized charges $1/t$ and $\log_2(t+2)/t$ also decrease. A successful endpoint therefore controls every later real width, including across all future native switches.

## Rational endpoints

After the [outer integer join](integer-clock.md) the bound on the logarithmic excess over $n\sqrt{\log_2 n}$ is at most $182+4\log_2(t+2)+G(t+2)$ in the high branch. Use 183 in place of 182 to reserve one binary exponent bit. This yields $2T(n)\le n(\log_2 n)^{501/1000}$. Because $\ln2\ge1/2$, the displayed natural-logarithm bound follows.

At either adjacent test point, $H$ has active slope $17/32768$ and intercept $3035148971130625/1024$ at $x=t+2$. Its preceding vertex is $v=6{,}201{,}245{,}580{,}657{,}120$, with $H(v)=6{,}181{,}211{,}607{,}280$. On each completed affine interval the convex function $H-cP$ reaches its maximum at an endpoint. The [exact independent checker](routing-refined-walsh.py) enumerates all 29 earlier vertices, including zero. The largest previous surplus lies below 1,158,519,021,433. The current surplus at either adjacent point exceeds 1,170,615,213,370 and gives the actual maximum. It follows that the varying-prefactor test is the single movement comparison

$$
 t/1000>
 183+4\log_2(t+2)+3035148971130625/1024+
 (17/32768)(t+2)+(33/4)\Phi(t+2).
$$

| Charged cutoff test | Last failing integer | First passing integer |
|---|---:|---:|
| Prior common left-endpoint allowance $2^{25}+220$ | 8,931,803,133,527,016 | 8,931,803,133,527,017 |
| Small physical high-branch allowance $183+4\log_2(t+2)$ | 8,931,714,897,907,029 | 8,931,714,897,907,030 |

The checker brackets each log by the 24-term positive atanh series with a rigorous remainder. It brackets every cube root on a denominator-$2^{80}$ grid by exact integer cubing. At the last failure of the sharper test the invoice exceeds the target by more than $0.000133976$; at the first pass it is below by more than $0.000246303$. For the older fixed allowance, $2^{25}+220$ dominates its varying prefactor and the conversion bit at the tested left endpoint. Monotonicity of the actual normalized invoice supplies all later lengths. The like-for-like reduction relative to the previous 11,665,715,140,844,862 cutoff is 2,733,912,007,317,845. The thresholds locate where these upper invoices certify the unit coefficient.

## Reproducible formal conclusion

The [finite-frame proof](routing-refined-frame.lean) reconstructs a uniform historic bound using $D=1{,}160{,}000{,}000{,}000$ and the final five affine supports. Four knot checks suffice after the last early width whose height is below $D$. Their rigorous logarithmic lower bounds are $49,50,51,839/16$, and $(6{,}201{,}245{,}580{,}657{,}122)^{16}>2^{839}$ proves the final one. The [all-later proof](routing-refined-clock.lean) combines this frame with the independent [112-bit endpoint proof](recount-refined.lean) and exact conversion to natural logarithms. The [schedule theorem](routing-refined-schedule.lean) reconstructs the actual 29 rational height and slope rows, checks continuity and decreasing slopes, and checks membership of every support used by the bound. Retaining the last measured slope can only enlarge the true native shape after later switches.

The final theorem `S008.Piecewise.Refined.schedule_natural_clock` takes the complete rounded physical invoice and the checked packing inequality $X\le t+2$ as premises. Its conclusion covers every $n$ at and above the sharper threshold with unit coefficient. The finite/interchanger tape schedules and the sizes of their issued calls are established in the supplier notes. The [reviewer script](routing-check-lean.sh) accepts a mathlib checkout followed by `--refined`. Its optional `--fresh` flag replays the entire transitive target in an empty Lean environment.

Prepared for Jerry Chen (@CubeJerry) with ChatGPT research assistance.
