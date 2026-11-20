# Independent review and the sharp integer batch-width degree

At saving 0.0050000005, the 23,040-lane tariff has a funded single product grade whose homogeneous compiler uses at most $N^{18}$ arbitrarily initialized productive fields. Among **fixed intermediate words followed by the $B^{D(e)}$ homogeneous batching rule** of #7828, the integer degree 18 is sharp for this tariff and price. A physical source realizing this tariff and compatible outer suppliers remain open.

## Independent source and price review

The reviewer read Ali Romman's pending #7826 at f927ed7ffbb2b8870f109d59ddd94e1f87becb13 and #7828 at 03b572b3b9ab72c6ba67762e85e1630cda1daad5. The checker obtains the two-call $P_2,T_2$ and native paid and helper histograms $N,H$ from the pinned E-free caller receipt. It recovers $Q$ by dividing the physical four-bit MOVE counts of the bank-480 atlas by $4\cdot480$ and adding the target's return excess $128/3840$ at rank eight. For each even $m$ this gives

$$
P_m=(m/2)P_2+18(m-1)(Q-N),\qquad
T_m=(m/2)T_2-18(m-1)H .
$$

The coefficient of $m$ is obtained by differencing the $m=4$ and $m=2$ profiles. The three slope certificates and all crossing brackets in the author proof pass. Affineness of the centered derivatives extends the $m=4$ bounds to every $m\ge4$. The $m=2$ case needs its separate center at 9. The target derivative at zero already lies below the center $\log13$ there. Monotonicity of a positive histogram's weighted mean of the log rank turns the endpoint test into the entire #7828 chord criterion. The limiting coefficient and the $m=870$ word have unique roots; the $m=2$ gap stays negative for every saving at or above 1/200. This establishes the unattained supremum in $(.00500220831285,.00500220831286)$, the finite crossing in $(.00500000060450,.00500000060451)$ and the all-finite-$m$ one-stage exclusion.

The numerical method uses integer square roots on a $2^{360}$ grid. To enclose $r^s$, repeatedly square-root dyadic intervals for $r$ and multiply the factors selected by the binary digits of $s$. After 140 digits, multiplying the upper result once by the current root bounds the remaining factor by monotonicity. For $\log_2 r$, successively square and normalize a containing interval in $[1,2)$, retaining a bit only when both interval ends agree. The one natural-log conversion uses $\log 2=\sum_{j\ge1}2^{-j}/j$ with its geometric tail. The checker imports no author or upstream verification code.

The reviewer recovered all thirteen product-type counts by an independent divisor search. For the exact weights $w_k=W_k k^t$, the smallest selected $w_k/n_k$ exceeds the largest remaining $w_j/(n_j+1)$ by more than $2.56\cdot10^{-13}$. Thus the certificate is a global mode for the exact weights as well as the rational approximations in the author proof. This follows by exchanging factors in the decreasing lists $w_k/1,w_k/2,\ldots$.

## An integral cutoff giving degree 18

Let $t=1-.0050000005$, $v=2^{42}$, and take the verified type. Its grade $K$ satisfies

$$
\log_2 K-v\log_2(99/2)>3{,}127{,}469{,}285 .
$$

Choose $J=160^{v/2}$, an integer. The modal-type probability bound gives $BK^t\ge T(t)^v/(v+1)^{13}$. The unsplit paid products contribute at most $P(t)^v$. The split products contribute at most $2P(1)^vJ^{t-1}$. Independent dyadic bounds give

$$
v\min\left(1-P(t)/T(t),\quad
1-\frac{P(1)}{T(t)\,160^{(1-t)/2}}\right)>630 .
$$

Since $13(42+1)+3=562$, the ratio of the two charges to retained grade is below $3/8$. The same calculation separately verifies the author's $13^v$ cutoff. Every child has rank at most $J$. A path with $D\ge1$ active levels needs at least $K(K/J)^{D-1}$ initial axes, at least $((99/2)/\sqrt{160})^{vD}$. The type has $B\le B_0^v$ slots, where $B_0=42{,}455{,}715{,}840$ includes all six binary copies. The integer comparison

$$
99^{18}=834513761450087614416078625185528201
 > B_0(4\cdot160)^9
 =764814184147086658303426560000000000
$$

gives $B^D\le N^{18}$. Root tiles reuse the batch sequentially. The $D=0$ case is immediate.

## Why degree 17 fails for this schedule

Consider any fixed repetition $v\ge1$ of the same complete integer source at the same $t$. Retain $B$ distinct slots of one grade $K$. Split each paid product into positive ranks summing to that product rank. Let $h<K$ be the largest resulting paid rank. Suppose the intermediate word is strictly funded. Concavity for positive ranks and conservation of their sum force

$$
BK^t>P(t)^v,\qquad BK^t>h^{t-1}P(1)^v .
$$

For all $s\ge0$, the retained slots satisfy $BK^{t+s}\le T(t+s)^v$. Take $s=1/1000$. Integer-root arithmetic proves all three strict inequalities.

| Inequality | Certified positive difference exceeds |
|---|---:|
| $P(1)>(25/2)^{1-t}T(t)$ | 92,315,478 |
| $50^s P(t)>T(t+s)$ | 15,935,362 |
| $P(t)>4^{17}50^t$ | 850,049,569,301 |

The first gives $h>(25/2)^v$. The second gives $K<50^v$. The third, combined with $BK^t>P(t)^v$, gives $B>4^{17v}$. In particular $B>(K/h)^{17}$.

For this fixed intermediate word define $e_1=K$ and $e_{j+1}=K\lceil e_j/h\rceil$. The schedule defines $D(e)=0$ below $K$ and $D(e)=1+D(h\lfloor e/K\rfloor)$ otherwise. Monotonicity gives $D(e_j)\ge j$. Also $e_{j+1}\le(K/h)e_j+K$, hence $e_j=O((K/h)^j)$ with a constant depending only on the fixed word. Choose $N_j$ the smallest power of two at least both $2M$ and $M\lceil e_j/K\rceil$, where $M$ is the fixed product ambient. Root tile capacity $K\lfloor N_j/M\rfloor$ is at least $e_j$. Its prescribed root batch therefore satisfies $W_{N_j}\ge B^j$, while $N_j^{17}=O((K/h)^{17j})$. Their ratio is unbounded. The construction above establishes the exact smallest integer width degree for this schedule at this price. This leaves real exponents between 17 and 18, other source packings, mixed grades and alternative scheduling open.

## Ordinary and outer interfaces

The one-stage threshold from the historical ordinary offer is $3112961/621875000$. All four finite-stage suprema are reproduced by exact fractions. PR #7826 supplies a stronger conditional route when the new word meets its open interface. The stopped program must expose all calls and bad cases, return each before consumption, have a strict pathwise decrease in child volume, local $O(V(1+n))$ work, $O(V)$ aggregate requested volume and private backing, and bounded full-frame parking. The fixed physical group, fresh stock and restoration obligations apply at each borrowed call. The six binary copies in the payload and the odd prime for eventual address coordinates serve different purposes. The author retains the need to prove all-column projectors and their lifts before importing the fallback multiplier $1+64N^5/q$.

Under these hypotheses, strict $\mu(1-C)<1$ and $C<\min(1/128,1-1/128)$ put the self-hosted exponent strictly below $1-C$. The fixed logarithmic factors are absorbed at the advertised ordinary offer. The upstream consumer has explicit caps below .005 for its earlier BIT words. A .005 conclusion requires a freshly justified cap, actual radius and stock estimates, and all outer guards on a compatible complex invoice.

Run this directory's check using the following command.

    python3 -I -B check.py --repo REPO --out FRESH

The checks include exact dyadic-power controls, both failed price tests, the small-m cutoff, an interior chord failure, a too-small global cutoff and the homogeneous degree-17 obstruction. Credit @CubeJerry, Ali Romman, Cinna Davis and the retained source contributors for their respective constructions. The new review and fixed-schedule width result use substantial OpenAI assistance. No new complete κ.
