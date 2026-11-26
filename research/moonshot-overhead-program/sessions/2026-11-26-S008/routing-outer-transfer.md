# Leading-one transfer at the existing integer cutoff

Put $Z=2^{100}$, $K=2^Z$, $L=\log_2 k$, $X=\lceil\log_2(k+2)\rceil$, $b=\lceil\log_2(2k)\rceil$, and $\Phi(x)=(x^2\log_2(x+2))^{1/3}$. At $k\ge K$ use $A_I=5120$, $B_I=576$, $A_W=2^{2^{24}+28}(1+A_I)$ and $B_W=832$. The ordinary-cost and Walsh suppliers together imply a leading coefficient of one at every input length

$$
n\ge 2^{2K},\qquad
T(n)\le n(\log_2 n)^{1/2+357/10^9}.
$$

The integer check below also admits $35683/10^{11}$ in place of $357/10^9$. These are transfers from the stated actual interchange, Walsh, short-axis, permutation and arithmetic suppliers on this domain. Their written physical implementations and primary correctness arguments retain their own verification status.

## Numerical assembly

Take $N=2^k$. Each full permutation or CRT sees at most $2^{10}Nk$ payload bits by the ordinary caller, covering both signed components on the $72k$ fractional-bit grid. The $2048k$-bit phase-construction precision is confined to polynomial setup work. Stage phase coefficients in compact, contiguous words before any repeated scans. Supply the permutation executor with dense local target addresses after extracting them from the setup catalogue.

For brevity write $Q=Nk\sqrt k\,2^{832\Phi(X)}$. On this range the binary-interchange multiplier obeys $1+J(k)\le 3A_I\sqrt k\,2^{576\Phi(X)}$. The factor of three covers $\sqrt{1+k}$ and the additional one.

| Work | Bound used in the sum |
|---|---|
| One selected Walsh layer, including its position operations and centered lift | $2^{18} A_W bQ$ by [the actual Walsh supplier](walsh-node.md). |
| One Fourier permutation layer | $2^{72}b^3\,(2^{10}Nk)(1+J(k))+k^{1120}\le A_W b^3 Q$ by [the guarded-switch supplier](routing-outer-permutations.md). The first coefficient after substitution is $2^{82}\cdot3\cdot5120$, less than $A_W/2$. |
| All phase layers combined, plus parameter generation, pointwise products, final scaling, packing and exact readout | $k^{850}+2^{100}b Nk^{3/2}+k^{40}\le A_W bQ$. Fewer than $3N$ complex products per phase use at most $12N$ real products. The [word supplier](word-toom.md) costs at most $2^{48}k^{3/2}$ per real product even under the ordinary caller’s $2^{12}k$ operand padding. The $2^{100}$ coefficient includes all three schedules, private ports, signed additions, shifts, compacted table scans and raw binary carries. [Ordinary tape ledger](outer-layers.md) |
| Three CRTs combined | $2^{75}b^4\,(2^{10}Nk)(1+J(k))+k^{1125}\le A_W b^4 Q$ by [the permutation supplier](routing-outer-permutations.md). |

For the additive inequalities, $k^{1200}\le 2^k$ for $k\ge2^{32}$, since $k/\log_2 k$ increases there. The ordinary arithmetic bounds have more than a factor of eight of slack. Distinct tables or inputs parked through another pass need no coefficient search per data record. Repeated table scans use the compact staged interval.

Every required permutation or Walsh layer costs at most $2^{19}A_W b^3 Q$. There are at most $3\cdot2^{29} b$ global layers across two forward transforms and one adjoint. The combined three CRTs and all ordinary arithmetic are separate terms, each at most $A_W b^4 Q$. Therefore

$$
T\le (3\cdot 2^{48}+2) A_W b^4Q < 2^{55} A_W b^4Q. \tag{1}
$$

Write $l=\log_2 n$, $d=\lceil l\rceil$ and $h=\lceil n/d\rceil$. The actual digit packing takes $k=\lceil\log_2(4h)\rceil$. Since $d\le l+1\le4\cdot 2^{l/2}$, $k\ge l/2\ge K$. Also $N<8h\le16n/d\le n$ for $d\ge16$. Hence $k\le l$ and $Nk<16n$. Conversely $n\le hd\le N(2k+1)/4\le Nk$, so a fixed number of scans of the raw input and exactly $2n$ output digits are covered. Because $\log_2(1+A_I)<13$, the logarithmic prefactor in (1) after conversion to $n$ is less than $2^{24}+100+4\log_2 b$. We use $2^{25}+4\log_2 b$.

## One exact endpoint check for all larger inputs

At $L\ge Z$, $X,b\le L+2$. Both $1+2/L$ and $\log_2(L+4)/L$ decrease there. The latter follows because $L/(L+4)<\ln(L+4)$ in its derivative. The same applies to $\log_2(L+2)/L$. Consequently

$$
\frac{2^{25}+4\log_2 b+832\Phi(X)}{L}
\le \frac{C+832\bigl((Z+2)^2\log_2(Z+4)\bigr)^{1/3}}{Z},
\qquad C=2^{25}+404. \tag{2}
$$

Indeed $\Phi(X)^3/L^3\le(1+2/L)^2\log_2(L+4)/L$. For the logarithmic prefactor use $\log_2(Z+2)<101$. To certify excess $1/2{,}500{,}000=4\cdot10^{-7}$, it is enough to use $\log_2(Z+4)<101$. The following strict integer inequality holds.

$$
(Z-2{,}500{,}000C)^3 >
  (2{,}500{,}000\cdot832)^3 (Z+2)^2\cdot101. \tag{3}
$$

The left/right ratio exceeds $1.39472$. For the sharper comparison, $\log_2(1+4/Z)<8/Z<1/1024$ implies $\log_2(Z+4)<102401/1024$. With $(p,q)=(357,10^9)$, and also $(35683,10^{11})$, one has $pZ>qC$ and

$$
1024 (pZ-qC)^3 > (832q)^3 (Z+2)^2 102401. \tag{4}
$$

The ratio in (4) exceeds $1.00145$ for the first pair and $1.00002$ for the second. Equations (1) through (4) give the claimed leading-one result. For orientation, the main positive term of this same cost expression already exceeds $(35682/10^{11})\log_2 k$ right at $k=K$. Cubing reduces this statement to $35682^3 Z < (832\cdot10^{11})^3\cdot100$. This comparison concerns only the positive invoice for the chosen suppliers.

## Sharpened same-machine coefficients

The independently [reviewed width potential](routing-review-interchange.md) gives $B_I=156$ at $A_I=5120$. Separating ordinary work from guarded XORs in the [Walsh supplier](walsh-node.md) gives $B_W=\max(102,B_I+41)=197$. Indeed the coarse event inventory is at most $2^{60}m^{37}$. Each event has ordinary toll at most $m^{61}V$ but only a matrix event issues at most $64m^2$ packed XORs. The two resulting powers are $m^{98}$ and $m^{39}$ respectively, and the rounded numerical arity satisfies $\log_2(m+1)\le(33/32)\Phi(x)$. Thus the ordinary term contributes at most $102\Phi$ and the guarded term at most $(B_I+41)\Phi$ in its logarithmic clock. The spatial exponent coefficient 48 is smaller. The same $A_W$ absorbs the fixed transition factors. A subsequent improvement of either positive invoice also permits this specialization.

Replacing 832 by 197 everywhere in (1)–(4) gives a leading-one bound of $n(\log_2n)^{0.50000008449}$ for the same $Z=2^{100}$. This uses $(p,q)=(8449,10^{11})$ in the exact cube test. More generally for a guard $Z=2^t$ replace the constant $404$ by $4(t+1)$, and use $\log_2(Z+4)<t+1$. The rational comparison for $B_W=197$ and excess $1/1000$ already passes at $t=59$, with a left/right ratio exceeding $1.25666$.

The sharpened [Walsh column-map count](walsh-node.md#only-actual-column-maps-use-the-interchanger), independently checked against the query and seed roles in [the physical review](routing-review-walsh.md), puts $B_W=\max(48,B_I+9)=165$. It prices the exact $f$-bit slots on their extracted row volume, leaving the nonlinear data-dependent check table as an address-preserving scalar. Its smaller $k$ guard and the [short-axis proof](recount-integration.md#short-coprime-axes-at-the-smaller-global-guard) apply at $t=58$. The same executable cube comparison therefore gives the following two complete specializations:

| Required $k\ge K=2^{2^t}$ | Leading-one upper bound |
|---|---|
| $t=58$ | $n(\log_2n)^{501/1000}$ |
| $t=100$ | $n(\log_2n)^{0.50000007077}$ |

Any later validated decrease in a positive supplier coefficient also preserves these bounds. The cumulative visited-cell bound on these fast inputs is [numerically priced](routing-outer-space.md).

## Exact length cutoff of a power-of-two width guard

Let $K=2^Z$ with integer $Z\ge3$, and set $A=2^{K-3}$. For this paragraph $d=\lceil\log_2 n\rceil$, $n\ge2$. The real packing rule used by the caller satisfies

$$
k\ge K\ \Longleftrightarrow\ 4\lceil n/d\rceil>2^{K-1}
\ \Longleftrightarrow\ n>Ad .
$$

On the integer slice $2^{d-1}<n\le2^d$ there is a failure precisely when $2^{d-1}<Ad$, equivalently $2^{d-K+2}<d$. Let $D=K+Z-2$. At $d=D$ the left side of the last inequality equals $K<D$. At $D+1$ it equals $2K>D+1$, and each subsequent increment doubles it. Also $2^{D-1}=AK<AD<2AK=2^D$. Thus the *last* input length having $k<K$ is $AD$. At that length $h=A$ and $k=K-1$. The least sufficient lower endpoint covering every subsequent input length is therefore

$$
n_* = 2^{K-3}(K+Z-2)+1. \tag{5}
$$

For a dispatcher using the literal width test $k\ge K$, the global leading-one bounds hold for all $n\ge n_*$ at their corresponding $K$. To implement that dispatcher, measure $n$ and its logarithmic digit width $d$, compute $h=\lceil n/d\rceil$ by binary division on words of at most $d+2$ digits, and compute $k=\mathrm{bitlength}(4h-1)$. The comparison $\mathrm{bitlength}(k)\ge Z+1$ is a fixed finite-state chain, so no huge threshold is materialized. The preparatory $O(d^2)$ steps fit the polynomial fast setup. A machine instead explicitly routed to a quadratic fallback for every $n<2^{2K}$ retains that chosen switch. The usual power-of-two condition $n\ge2^{K+Z-2}$ suffices for the literal width test. The test $n>2^{K-3}\lceil\log_2 n\rceil$ may pass at some smaller lengths because $\lceil n/\lceil\log_2 n\rceil\rceil$ can decrease at a power-of-two boundary. Equation (5) is sharp for admissibility of this guard.

## The root-degree-240 machine

For the final [fixed $R=240$ native machine](node-root-parameter.md), one can instead use $B_I=61$ and the same $A_I=5120$. The typed Walsh bill then has $B_W=70$. Equation (1) with that substitution is also the [full integer ledger](integer-clock.md). Put $x=\log_2\log_2n$. After division by $n\sqrt{\log_2 n}$ the logarithm of its entire clock is bounded by

$$
2^{25}+4\log_2(x+2)+70((x+2)^2\log_2(x+4))^{1/3}. \tag{6}
$$

All fast guards hold for $x\ge2^{48}+1$. At an endpoint $z<2^{55}-4$, put $C=2^{25}+220$. Using the decreasing ratios in (2), the bound $n(\log_2 n)^{501/1000}$ holds for the actual machine at every $x\ge z$ as soon as

$$
(z-1000C)^3 > 70000^3(z+2)^2\log_2(z+4),\qquad z>1000C. \tag{7}
$$

The [rational interval certificate](routing-outer-threshold.py) proves (7) at $z=18{,}536{,}231{,}398{,}600{,}959$ and proves the strict reverse at $z-1$. It bounds $\ln((1+t)/(1-t))$ for $0\le t\le1/3$ between the first 24 terms $2\sum_{i=0}^{23}t^{2i+1}/(2i+1)$ and this sum plus $2t^{49}/(49(1-t^2))$. Apply this first to $\ln2$, and then to $\ln((z+4)/2^j)$ with $j=\lfloor\log_2(z+4)\rfloor$. All endpoint comparisons are strict rational comparisons. Thus a sufficient input length is

$$
n\ge 2^{\,2^{18{,}536{,}231{,}398{,}600{,}959}} .
$$

This also works with the larger $A_W$ used above and with the initially chosen fallback at $n<2^{2K}$, as $z>2^{48}+1$. The adjacent signs locate the first integer satisfying this particular conservative inequality. They do not provide a lower bound on the running time.

[Exact integer replay](routing-outer-transfer.py). Prepared for Jerry Chen (@CubeJerry) with ChatGPT research assistance.
