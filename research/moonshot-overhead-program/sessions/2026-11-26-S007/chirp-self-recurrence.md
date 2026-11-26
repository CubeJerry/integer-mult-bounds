# Exact recursive volume of the two chirp dimensions

This audit concerns the literal S007 plane algorithm with degree-$w$ field coefficients encoded at binary polynomial stride $2w-1$. Put $b=3c$, $a=2^c$, $h=a^2$, $q=a^3$ and $m=a-1$. It is legitimate to call an independent ordinary binary polynomial multiplier at the indicated sizes. Directly replacing this supplier by the same full binary CRT does not yield a contracting square-root or sublinear logarithmic exponent.

A length-$m$ input over a degree-$w$ field has largest packed operand length
$$
 L_w=(m-1)(2w-1)+w=(a-2)(2w-1)+w.
$$
Padding to $m(2w-1)$ adds only $O(w)$ bits. The kernel's last field coefficient is nonzero, so shortening its ambient top coordinate cannot change $L_w$ by more than $w-1$. The packed pointwise modular reductions have ordinary inputs $O(b)$: they do not change the following dominant-volume comparison.

| Source, one full root direction | Number of ordinary binary products | Operand length | Aggregate operand length divided by $q$ |
|---|---:|---:|---:|
| $h$ lower degree-$c$ CRT inputs, packed $c$ lanes per $L$-valued chirp | $\lceil h/c\rceil$ | $L_c$ | $2+o(1)$ |
| Two axes of the retained $K$ grids | $2aP$ | $L_b$ | $12+o(1)$ |

Here the actual multiplicity is $P=2R_{\rm quot}$, since the algorithm evaluates **both** $t=\alpha,\alpha+1$ for each retained S006 quotient orbit, including a twisted orbit where the two planes are Frobenius conjugates. Write $g_j=\gcd(c,j)$. Burnside on normal-coordinate words under rotations and complement gives
$$
 P=\frac1c\sum_{j=0}^{c-1}2^{g_j}\left(1+\mathbf1_{2\mid c/g_j}\right)=a/c+O(2^{c/2}).
$$
The second summand counts fixed words of a complemented shift, possible exactly when each positional cycle has even length. At $c=2$ this is four actual planes, while the ordinary Frobenius action on $L$ has three orbits. Every nonidentity rotation has $g_j\le c/2$. The factor 12 has three independent origins: the $b$-bit words on both actual S006 planes over every quotient orbit occupy $(3+o(1))q$ bits, there are two grid axes, and ordinary binary packing uses asymptotically two bits of stride per coefficient bit. Each operand logarithm is $b/3+O(\log(b+2))$; the harmless ceiling on the last group of $c$ lanes changes the first asymptotic by $o(1)$.

Even the optimistic formal substitution of one transform covering exactly $L_w$ bits per product would insert $(14+o(1))q$ child bits. In a trial clock $q b^\theta$ the ratio of its recursive right-hand side to the proposed parent bound tends to $14/3^\theta$. This exceeds one for every $0\le\theta\le1$, including multipliers with a fixed power of $\log b$ in the overhead. Therefore this ordinary normalized induction cannot establish the proposed saving.

The literal supplier is more expensive. Its generic operation is an **ordinary** product of one variable and one fixed binary polynomial, followed by folding. An exact unreduced product needs root degree $q'\ge2L_w-O(w)$ to avoid wrap. Even if the fixed operand's root residues already exist, it applies one complete forward and one complete inverse transform at that degree. Thus a single root direction generates at least $(56-o(1))q$ child transform bits before rounding $\log_2 q'$ upward to a multiple of three. Rounding only increases this volume; the child degree parameter is still $b/3+O(\log b)$. A construction that changes simultaneously to a cyclic quotient, computes only selected coefficients, shares transforms across raw packets, or encodes the extension product without this binary stride uses a different interface and does not inherit this negative count.

There is also an operational obstruction for the specific literal full recursion, stronger than failure of that induction. Fix any $1<\Lambda<56$. At every sufficiently large internal parameter, the sum of child sizes is at least $\Lambda$ times the current size and every child's logarithmic parameter is at least one third of its parent's, since $L_w\ge a$. Through $\lfloor\log_3(b/B)\rfloor$ levels with fixed sufficiently large $B$, the unaltered recursion therefore creates total bit volume at least $q\Lambda^{\lfloor\log_3(b/B)\rfloor}$. Each specified generic full child call is invoked and emits its whole result, so a fixed number of ordinary tape heads requires at least linear time in the sum of these extents over that level. Taking, for example, $\Lambda=27$ gives $\Omega(qb^3)$ executed steps for the fully expanded generic subroutine procedure. This does not lower-bound a specialized binary multiplication circuit, a fused batch schedule, or the original task. The nonrecursive unconditional binary multiplier remains available and supplies the $O(qb\operatorname{polylog}b)$ result.

The [integer count](verify-chirp-volume.py) checks both Burnside counts explicitly at $c=2$ and gives the actual operand-volume and padded-recursion ratios at sample degrees through $c=509$. [Receipt](chirp-volume-cases.json)
