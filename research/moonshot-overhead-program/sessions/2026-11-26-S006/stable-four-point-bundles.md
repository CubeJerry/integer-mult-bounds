# Consecutive additive remainder stages in Frobenius-stable bundles

Let $K=\mathbf F_{2^b}$, $q=2^b$, $\sigma x=x^2$, $W=\langle1\rangle_{\mathbf F_2}$, and $U=\langle1,\eta\rangle_{\mathbf F_2}$ with $\eta\notin W$. Binary input means all polynomials in $\mathbf F_2[X]_{<q}$. The four coefficients of the remainder on $a+U$ form the block of the ordinary additive transform. A bundle retains all four coefficients of each of its constituent blocks. The basis used inside a bundle may be any invertible $K$-linear mixture.

For the infinite family $b=3^t$, $t\ge1$, a full-degree direction permits $\Theta(\sqrt b/(\log b)^2)$ consecutive forward or inverse additive remainder levels in $O(q\sqrt b)$ fixed-head tape steps and $O(q)$ ever-visited bits. The two streams use one full $b$-bit word per retained coefficient. A fixed Toom-3 multiplier suffices for $b^\epsilon$ consecutive stages whenever $0<\epsilon<3/2-\log_3 5$. Both endpoints already use representatives of the same stable bundles. The standard four-point stage is one of these levels.

## Which support partitions admit dense semilinear transport?

Write $y_z=f(z)$. The tables reachable on binary inputs satisfy $y_{\sigma z}=\sigma y_z$; interpolation proves the converse. They span $K^K$ over $K$, since the evaluation map is invertible and the binary coefficient vectors span $K^q$. For a $K$-linear row with coefficients $c_z$ on points $B$, its square on these inputs is the restriction of the row with coefficients $\sigma c_z$ on the corresponding points $\sigma z$.

Every complete remainder block interpolates its point evaluations by an invertible change of coordinates. Consequently all rows of a bundle with support $B$ span the coordinate rows on precisely $B$. An invertible dense matrix common to the complete bundle, followed or preceded by the prescribed one-step scalar Frobenius, can identify its data with those of a bundle $B'$ on every binary input exactly when $B'=\sigma B$. Indeed the row spans agree on the full evaluation space by the preceding spanning test, and equality of coordinate subspaces implies equality of supports. Conversely conjugate all point values, permute them into the target order and change to its chosen coordinates. This argument tests one common Frobenius per transported bundle. Allowing unrelated twists on different entries or unrestricted binary-linear joint encodings changes the question.

Put $V=\sum_{i=0}^{b-1}\sigma^i U$. Every stable partition coarsening the $U$-cosets relates $x$ and $x+u$ for every $x$ and $u\in U$. Conjugating gives these relations for each $\sigma^i U$; transitivity gives them for $V$. The cosets of $V$ themselves form a stable partition, so they give the finest such coarsening.

For odd $b$, the normal basis theorem identifies $K$ with the regular Frobenius module $\mathbf F_2[T]/(T^b-1)$. This ring decomposes into all the distinct irreducible factors of $T^b-1$, each with multiplicity one. Its fixed line is $\mathbf F_2 1$. The hull $V$ consists of that line and the nontrivial factors on which $\eta$ has nonzero projection. The field degree of $\eta$ is the least common multiple of the orders of roots of those factors, since this is exactly its Frobenius period.

For odd prime $b$, every nontrivial factor has degree $d_0=\operatorname{ord}_b(2)$, and all dimensions $1+jd_0$, $1\le j\le(b-1)/d_0$, occur. In particular each nonbinary direction forces at least $2^{1+d_0}\ge 2(b+1)$ points per bundle. For $b=3^t$, full degree forces a primitive-$b$ factor, since all proper divisors divide $b/3$. The identity $v_3(4^{3^s}-1)=s+1$, by induction using $x^3-1=(x-1)(x^2+x+1)$, gives $\operatorname{ord}_{3^t}(2)=2b/3$. There is exactly one primitive factor. Hence $\dim V\ge1+2b/3$, sharp by retaining just this factor in $\eta$. A normal $\eta$ forces $V=K$ at every degree. Semisimplicity was used only for the odd-degree factor calculations.

Bundle size alone does not determine representative storage. If $B$ belongs to a bundle orbit of length $r$, every point orbit of length $\ell$ meeting $B$ has $r\mid\ell$ and contributes exactly $\ell/r$ points to $B$. Its freely chosen value lies in $\mathbf F_{2^\ell}$ and determines the entire point orbit; different orbits are independent. Thus the projection on that bundle has exactly $2^{r|B|}$ possible vectors and the information over all representative bundles is exactly $q$ independent bits.

## Full words on a sharp $3$-power family

Write $b=3c=3^t$, $H=\mathbf F_{2^c}$, $P=\ker\operatorname{Tr}_{K/H}$. The relative trace restricts to the identity on $H$. Every nonzero $\eta\in P$ has degree $b$, since all proper subfields lie inside $H$. The $2c$-dimensional space $P$ is the unique primitive-$b$ Frobenius summand. Indeed the fixed space of $\sigma^c$ is $H$, and the other summand has the asserted dimension and is irreducible. Put
$$
 V=\mathbf F_2 1\oplus P,\qquad T=\ker(\operatorname{Tr}_{H/\mathbf F_2}).
$$
Because $c$ is odd, $K=V\oplus T$ equivariantly. The quotient action on $T$ has order dividing $c$. The fixed points of $\sigma^i$ on $H$ form $\mathbf F_{2^{g}}$ with $g=\gcd(i,c)$. The absolute trace of $H$ restricts to that subfield's absolute trace since $c/g$ is odd. Hence the fixed space on $T$ has dimension $g-1$. Burnside's lemma gives the number of representative bundles
$$
 R=\frac{1}{c}\sum_{i=0}^{c-1}2^{\gcd(i,c)-1}.
$$
Store each representative $\alpha+V$ in full, with one $b$-bit word per coefficient or point. The exact width is
$$
 b|V|R=3q\!\left(1+\sum_{i=1}^{c-1}2^{\gcd(i,c)-c}\right)=(3+o(1))q .
$$
Indeed all the proper gcds are at most $c/3$ when $c>1$. A normal direction gives one size-$q$ bundle and $qb$ bits under this same full-word rule. The within-bundle representative count is a different object from counting a separate canonical word for each scalar Frobenius class of the original four-point coordinates.

## One forward and inverse butterfly on the representative stream

Choose a basis $(1,\eta,v_2,\ldots,v_{2c})$ of $V$. Enumerate $\alpha\in T$ in a fixed binary basis and process only the least member of each orbit. Inside that representative, enumerate the $U$-cosets by $a=\alpha+\nu$, for $\nu$ in the binary span of the $v_j$, using binary counter order. The forward record consists of the four coefficients of $P_0+sP_1$ on $a+U$, where $s=X^2+X$ and each $P_j$ is linear or constant. The reverse record consists of the two coefficients of each of the linear remainders $Q_i$ on $a+i\eta+W$, $i=0,1$, adjacent in that order. The actual two-way operations are
$$
 Q_i=P_0+s(a+i\eta)P_1,\qquad
 P_1=(Q_1+Q_0)/s(\eta),\qquad P_0=Q_0+s(a)P_1 .
$$
These follow by reduction on the two pairs. They hold for arbitrary local records and give the correct binary-reachable representatives in both directions. The data on omitted bundles are determined by conjugating point values; the clock here processes only the specified streams.

All control can be generated uniformly. Polynomial-size binary linear algebra computes bases for $P,T,V$, a nonzero $\eta\in P$, and $s(\eta)^{-1}$ (by field exponentiation). Each of the $2^{c-1}$ elements of $T$ can be tested for being orbit-minimal by at most $c$ squarings and fixed-basis comparisons, costing $q^{1/3}\operatorname{poly}(b)$ tape steps in total. For an accepted $\alpha$, initialize $s(a)=s(\alpha)$. Each increment of the inner counter toggles an initial segment of the direction bits. Scan and return across the corresponding initial segment of the $b$-bit words $s(v_j)$, updating $s(a)$ by addition. The total number of direction toggles is less than twice the number of counter states. This costs $O(b)$ head steps amortized per record, including resets; work polynomial in $b$ per representative is also covered by the outer enumeration. Input and output streams advance monotonically.

For an explicit uniform field-word implementation take a primitive $3b$th root $\zeta$ in $\mathbf F_2[Z]/(Z^{2b}+Z^b+1)$. This polynomial is $\Phi_{3b}$ and is irreducible by the same order calculation. Since $2^b\equiv-1\bmod 3b$, $a_0=\zeta+\zeta^{-1}\in K$ has degree $b$ because the degree-$2b$ element $\zeta$ satisfies $X^2+a_0X+1=0$. The elements $r_j=\zeta^j+\zeta^{-j}$ for $1\le j\le b$ are a binary basis of $K$. Indeed $r_b=1$ and $r_j$ for $j<b$ is monic of degree $j$ in $a_0$ by the two-term recurrence $r_{j+1}=a_0r_j+r_{j-1}$, $r_0=0$. For $j<b$ the ambient expansion is $\zeta^j+\zeta^{2b-j}+\zeta^{b-j}$. Expansion takes a constant number of forward/reverse XOR scans. Projection reads the high coordinates $2b-j$ and the constant for $r_b$.

Pack the two ambient bit polynomials in base $2^L>2b$ with $L=O(\log(b+2))$. Their integer product contains the coefficient sums without interdigit carry. Keep each parity bit, fold exponents at least $3b$ via $\zeta^{3b}=1$, then fold $\zeta^{2b+i}=\zeta^{b+i}+\zeta^i$ for $0\le i<b$, by fixed scans. Fixed Toom-3 has exponent $\tau=\log_3 5<3/2$. Each representative record needs $O(1)$ field products at $O((b\log(b+2))^\tau)$ tape steps per product. The $R|V|/4=O(q/b)$ records therefore take
$$
 O\!\left(qb^{\tau-1}(\log(b+2))^\tau+q^{1/3}\operatorname{poly}(b)\right)=o(q\sqrt b).
$$
The two streams use $O(q)$ ever-visited bits. Reuse the same polynomial-in-$b$ control, basis and product workspace for every record; all rewinds are included above.

## Consecutive levels on the same stream order

Write $D=2c+1$, $\beta_0=1$, $\beta_1=\eta$ and complete the above ordered basis of $V$ by $\beta_2,\ldots,\beta_{D-1}$. Let $W_j$ be the span of its first $j$ vectors and
$$
 s_j(X)=\prod_{w\in W_j}(X-w),\qquad d_j=s_j(\beta_j)\ne0 .
$$
Then $s_0=X$ and $s_{j+1}=s_j^2+d_js_j$ by splitting the roots into $W_j$ and $\beta_j+W_j$. Induction proves additivity of every $s_j$. If $i=\sum i_h2^h$, define $B_i=\prod_hs_h^{i_h}$. Each $B_i$ is monic of degree $i$, so $B_0,\ldots,B_{2^j-1}$ form a basis for the actual polynomial remainders at level $j$. In particular the four-point basis is exactly $1,X,s_1,Xs_1$ with $s_1=X^2+X$. One may instead take $h_j=s_j/d_j$ throughout for normalized additive coordinates. The formulas then use $h_j(a)$ and unit difference. Crossing specifically between the two four-point conventions multiplies or divides its two upper coefficients by $d_1$, a single constant number of field products per four-word record.

On each representative bundle order level-$j$ records by the integer address with binary direction bits $D-1,\ldots,j$; in each record order the coefficients by increasing $i<2^j$. The point representing a parent $W_{j+1}$-coset is $a=\alpha+\sum_{h>j}a_h\beta_h$. Its two children are consecutive in the level-$j$ order, first the child at $a$, then the one at $a+\beta_j$. The parent coefficients split into consecutive halves $A_i,B_i'$ since $B_{i+2^j}=s_jB_i$ for $i<2^j$. Reduction on the two children replaces these halves by
$$
 L_i=A_i+tB_i',\qquad H_i=L_i+d_jB_i',\qquad t=s_j(a).
$$
The inverse forms $B_i'=(L_i+H_i)/d_j$ and $A_i=L_i+tB_i'$. These coefficient identities hold on every local remainder. Output in the order $(L_i)_i,(H_i)_i$ is exactly the next forward pass's input; the analogous concatenation of the inverse halves restores the preceding order. Every child lies in the same retained bundle.

Compute all $d_j,d_j^{-1}$ and $s_j$ on the binary field basis and the $\beta_h$ by the displayed linearized recurrence in $\operatorname{poly}(b)$ steps; no degree-$2^j$ polynomial is expanded. On a given layer, select its table once. Test or enumerate the representative $\alpha$ as above, and initialize $s_j(\alpha)$ by a polynomial-size linear computation per representative. The higher-bit coset counter updates $t$ using the prefix of the ordered table $s_j(\beta_{j+1}),s_j(\beta_{j+2}),\ldots$ at amortized $O(b)$ head steps per parent, including return of its table head. Across all at most $D$ passes the outer enumeration, local starting values and table setup together cost $q^{1/3}\operatorname{poly}(b)$.

On one head per bank, copy a parent's first half to a scratch tape, rewind that tape, and pair it with the second half as the input advances. Emit the first output half directly, spool the second half to another scratch tape, then rewind and append it. Return both scratch heads to their fixed origins between parents. The same procedure handles inverse recombination. A $j$-bit counter marks each half length in $O(j+2^j)$ total counter steps. Hence all movement besides field arithmetic costs $O(b2^j)$ per parent. Rewind the two full stream banks once per pass and interchange their roles. The number of banks and scratch tapes stays fixed, and every pass uses the same intervals of length $O(q)$. Each short product's work heads can be cleared and returned to their fixed origins within its own time bound.

Let $\mu(b)$ bound one field-word multiplication including packing and reduction. For any $r$ consecutive layers within $W_0,\ldots,W_D$, in either order, the number of scalar pairs per layer is $R|V|/2=O(q/b)$, independent of $j$. The resulting bound is
$$
 O\!\left(q^{1/3}\operatorname{poly}(b)+rq\bigl(1+\mu(b)/b\bigr)\right)
$$
steps and $O(q)$ ever-visited bits. The binary integer operands in the explicit field product above have $O(b\log(b+2))$ bits. On these short operands the fixed-tape integer multiplication theorem gives $\mu(b)=O(b(\log(b+2))^2)$. Thus $r=O(\sqrt b/(\log(b+2))^2)$ fits $O(q\sqrt b)$. With fixed Toom-3 the same conclusion holds for $r=O(b^{3/2-\tau}/(\log(b+2))^\tau)$, including $\lfloor b^\epsilon\rfloor$ for every $0<\epsilon<3/2-\tau$. [Harvey and van der Hoeven, *Integer multiplication in time $O(n\log n)$*](https://annals.math.princeton.edu/2021/193-2/p04)

The contiguous run may start at the point-value boundary $W_0$ or end at any chosen intermediate level. All endpoint data must already have the specified representative ordering. Conversion from the binary coefficient input, conversion to another orbit encoding and a complete transform at the target clock remain open. These degrees are sparse.

The accompanying finite checker independently interpolates four-point remainders and reconstructs all binary evaluation points for $b=3,9$. It runs all $D$ adjacent levels forward and backward at both degrees and tests every intermediate polynomial directly at every point of its coset. It checks the representative count at $b=27$.

The additive stage and earlier scalar lower bound are described in [four-point additive CRT and Frobenius compression](https://github.com/CubeJerry/integer-mult-bounds/blob/335d099aa205220acc3941d77b6a8a9202f4488a/research/moonshot-overhead-program/sessions/2026-11-26-S006/four-point-frobenius-obstruction.md).
