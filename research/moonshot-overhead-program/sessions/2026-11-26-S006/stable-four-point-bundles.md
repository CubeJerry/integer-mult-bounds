# Consecutive additive remainder stages in Frobenius-stable bundles

Let $K=\mathbf F_{2^b}$, $q=2^b$, $\sigma x=x^2$, $W=\langle1\rangle_{\mathbf F_2}$, and $U=\langle1,\eta\rangle_{\mathbf F_2}$ with $\eta\notin W$. Binary input means all polynomials in $\mathbf F_2[X]_{<q}$. The four coefficients of the remainder on $a+U$ form the block of the ordinary additive transform. A bundle retains all four coefficients of each of its constituent blocks. The basis used inside a bundle may be any invertible $K$-linear mixture.

For every positive multiple $b=3c$ of three, a full-degree direction permits $\Theta(\sqrt b/(\log b)^2)$ consecutive forward or inverse additive remainder levels in $O(q\sqrt b)$ fixed-head tape steps and $O(q)$ ever-visited bits as $b$ grows. The two streams use one full $b$-bit word per retained coefficient. A fixed Toom-3 multiplier suffices for $b^\epsilon$ consecutive stages whenever $0<\epsilon<3/2-\log_3 5$. Both endpoints use representatives of the same stable bundles. The standard four-point stage is one of these levels. Every sufficiently large integer input length admits such a root by increasing its binary CRT extension degree by at most two.

## Which support partitions admit dense semilinear transport?

Write $y_z=f(z)$. The tables reachable on binary inputs satisfy $y_{\sigma z}=\sigma y_z$, and interpolation proves the converse. They span $K^K$ over $K$, since the evaluation map is invertible and the binary coefficient vectors span $K^q$. For a $K$-linear row with coefficients $c_z$ on points $B$, its square on these inputs is the restriction of the row with coefficients $\sigma c_z$ on the corresponding points $\sigma z$.

Every complete remainder block interpolates its point evaluations by an invertible change of coordinates. Consequently all rows of a bundle with support $B$ span the coordinate rows on precisely $B$. An invertible dense matrix common to the complete bundle, followed or preceded by the prescribed one-step scalar Frobenius, can identify its data with those of a bundle $B'$ on every binary input exactly when $B'=\sigma B$. Indeed the row spans agree on the full evaluation space by the preceding spanning test, and equality of coordinate subspaces implies equality of supports. Conversely conjugate all point values, permute them into the target order and change to its chosen coordinates. This argument tests one common Frobenius per transported bundle. Allowing unrelated twists on different entries or unrestricted binary-linear joint encodings changes the question.

Put $V=\sum_{i=0}^{b-1}\sigma^i U$. Every stable partition coarsening the $U$-cosets relates $x$ and $x+u$ for every $x$ and $u\in U$. Conjugating gives these relations for each $\sigma^i U$. Transitivity gives them for $V$. The cosets of $V$ themselves form a stable partition, so they give the finest such coarsening.

For odd $b$, the normal basis theorem identifies $K$ with the regular Frobenius module $\mathbf F_2[T]/(T^b-1)$. This ring decomposes into all the distinct irreducible factors of $T^b-1$, each with multiplicity one. Its fixed line is $\mathbf F_2 1$. The hull $V$ consists of that line and the nontrivial factors on which $\eta$ has nonzero projection. The field degree of $\eta$ is the least common multiple of the orders of roots of those factors, since this is exactly its Frobenius period.

For odd prime $b$, every nontrivial factor has degree $d_0=\operatorname{ord}_b(2)$, and all dimensions $1+jd_0$, $1\le j\le(b-1)/d_0$, occur. In particular each nonbinary direction forces at least $2^{1+d_0}\ge 2(b+1)$ points per bundle. For $b=3^t$, full degree forces a primitive-$b$ factor, since all proper divisors divide $b/3$. The identity $v_3(4^{3^s}-1)=s+1$, by induction using $x^3-1=(x-1)(x^2+x+1)$, gives $\operatorname{ord}_{3^t}(2)=2b/3$. There is exactly one primitive factor. Hence $\dim V\ge1+2b/3$, sharp by retaining just this factor in $\eta$. A normal $\eta$ forces $V=K$ at every degree. Semisimplicity was used only for the odd-degree factor calculations.

Bundle size alone does not determine representative storage. If $B$ belongs to a bundle orbit of length $r$, every point orbit of length $\ell$ meeting $B$ has $r\mid\ell$ and contributes exactly $\ell/r$ points to $B$. Its freely chosen value lies in $\mathbf F_{2^\ell}$ and determines the entire point orbit. Different orbits are independent. Thus the projection on that bundle has exactly $2^{r|B|}$ possible vectors and the information over all representative bundles is exactly $q$ independent bits.

## Full words at every degree divisible by three

Write $L=\mathbf F_{2^c}$ and $P=\ker\operatorname{Tr}_{K/L}$. Choose a normal element $\gamma$ of $K$ over $\mathbf F_2$, and put $\eta=\gamma+\sigma^c\gamma$. Its support in the normal basis is the pair $\{0,c\}$ modulo $3c$. The only translation fixing that pair is zero, so $\eta$ has full field degree $b$. Its Frobenius shifts span $\operatorname{im}(1+\sigma^c)$ because the shifts of $\gamma$ form a basis. The shift by $c$ has $c$ disjoint triples. On each triple $1+\sigma^c$ has image the even-weight subspace, precisely the kernel of $1+\sigma^c+\sigma^{2c}$. Thus
$$
 \langle\sigma^i\eta\rangle_i=P,\qquad \dim P=2c,\qquad
 V=\mathbf F_2 1\oplus P .
$$
Indeed the relative trace restricts to the identity on $L$, so $K=P\oplus L$ and $K/V$ identifies equivariantly with $L/\mathbf F_2$. This construction works also when $c$ is even. The dimension is sharp among full-degree directions when $b$ is a power of three by the factor calculation above.

The $c$ elements $\operatorname{Tr}_{K/L}(\sigma^j\gamma)$ for $0\le j<c$ form a normal basis of $L$ since their ambient basis supports are disjoint triples. Their sum is $1$, the nonzero absolute trace of the normal element $\gamma$. Thus a quotient point is a cyclic binary word of length $c$ modulo complementation. Use the unique lift with first bit zero and order these words in a fixed binary order. To compute its quotient Frobenius, rotate and complement if necessary to restore the first bit. This gives a section for enumerating cosets whether or not the chosen representatives themselves are stable.

For $0\le i<c$ put $g_i=\gcd(i,c)$. Rotation by $i$ has $g_i$ cycles, each of length $c/g_i$. A fixed quotient class has a representative carried either to itself or to its complement. The first condition has $2^{g_i}$ solutions. Alternating along each cycle gives $2^{g_i}$ solutions to the second condition exactly when $c/g_i$ is even, and none otherwise. Divide by two for representatives modulo complementation. Consequently the exact fixed and orbit counts are
$$
 f_i=2^{g_i-1}\bigl(1+\mathbf1_{2\mid c/g_i}\bigr),\qquad
 R=\frac1c\sum_{i=0}^{c-1} f_i .
$$
Store each representative $\alpha+V$ in full, with one $b$-bit word per coefficient or point. The exact stream width is
$$
 b|V|R=3q\!\left(1+\sum_{i=1}^{c-1}2^{g_i-c}
            \bigl(1+\mathbf1_{2\mid c/g_i}\bigr)\right)=(3+o(1))q .
$$
Indeed $g_i\le c/2$ for $i>0$, and for odd $c$ the maximum is at most $c/3$. A normal direction gives one size-$q$ bundle and $qb$ bits under this same full-word rule. The earlier scalar lower bound counted a separate canonical word for each scalar Frobenius class of the original four-point coordinates.

## One forward and inverse butterfly on the representative stream

Choose a basis $(1,\eta,v_2,\ldots,v_{2c})$ of $V$. Enumerate the chosen section of $L/\mathbf F_2$ and process only the least lifted word $\alpha$ in each quotient orbit. Inside that representative, enumerate the $U$-cosets by $a=\alpha+\nu$, for $\nu$ in the binary span of the $v_j$, using binary counter order. The forward record consists of the four coefficients of $P_0+sP_1$ on $a+U$, where $s=X^2+X$ and each $P_j$ is linear or constant. The reverse record consists of the two coefficients of each of the linear remainders $Q_i$ on $a+i\eta+W$, $i=0,1$, adjacent in that order. The actual two-way operations are
$$
 Q_i=P_0+s(a+i\eta)P_1,\qquad
 P_1=(Q_1+Q_0)/s(\eta),\qquad P_0=Q_0+s(a)P_1 .
$$
These follow by reduction on the two pairs. They hold for arbitrary local records and give the correct binary-reachable representatives in both directions. The data on omitted bundles are determined by conjugating point values; the clock here processes only the specified streams.

All control can be generated uniformly. The deterministic degree-$b$ binary field and normal-element preprocessing used by S005-FS1 takes polynomial time in $b$ for the fixed ground field. Polynomial-size linear algebra gives the displayed directions in the chosen polynomial basis. Field exponentiation supplies $s(\eta)^{-1}$. Test the $2^{c-1}$ quotient words by at most $c$ rotations, normalizations and comparisons per word, costing $q^{1/3}\operatorname{poly}(b)$ tape steps in total. For an accepted $\alpha$, initialize $s(a)=s(\alpha)$. Each increment of the inner counter toggles an initial segment of the direction bits. Scan and return across the corresponding initial segment of $b$-bit words $s(v_j)$, updating $s(a)$ by addition. The total number of direction toggles is less than twice the number of counter states. This costs $O(b)$ head steps amortized per record, including resets. Work polynomial in $b$ per representative is also covered by the outer enumeration. Input and output streams advance monotonically. [Bshouty, Diab, Kawar and Shahla, §2](https://arxiv.org/abs/1602.05032v3)

For the ordinary field implementation write $K=\mathbf F_2[Z]/h$ with $h$ monic of degree $b$. Put $\operatorname{rev}_m p=Z^mp(1/Z)$ on polynomials of degree at most $m$. Precompute $u=(\operatorname{rev}_b h)^{-1}\bmod Z^b$ by polynomial-size binary series arithmetic. For a word product $p$ of degree at most $2b-2$, the quotient on division by $h$ is
$$
 k=\operatorname{rev}_{b-1}\bigl((\operatorname{rev}_{2b-1}p)u\bmod Z^b\bigr),
$$
because reversal makes the remainder divisible by $Z^b$ in the reversed division identity. Return $p+hk$. This uses a constant number of binary polynomial multiplications of length $O(b)$. Pack binary coefficients into base $2^e>2b$ with $e=O(\log(b+2))$. The product's digits contain the coefficient sums without interdigit carry. Fixed scans extract each parity bit and handle reversals. With fixed Toom-3, writing $\tau=\log_3 5<3/2$, each product costs $O((b\log(b+2))^\tau)$ tape steps.

At $b=3^t$ an optional explicit field is the degree-$b$ fixed subfield of $\mathbf F_2[Z]/(Z^{2b}+Z^b+1)$. The latter polynomial is $\Phi_{3b}$, irreducible since $\operatorname{ord}_{3b}(2)=2b$. If $\zeta$ denotes its root, then $\zeta+\zeta^{-1}$ has degree $b$ since $2^b=-1\bmod 3b$ and $\zeta$ satisfies $X^2+(\zeta+\zeta^{-1})X+1=0$. A word basis is $1$ together with $\zeta^j+\zeta^{-j}$ for $1\le j<b$, which are monic of successive degrees in $\zeta+\zeta^{-1}$. The finite checker also uses this independent field implementation.

Each four-word record needs $O(1)$ field products. The $R|V|/4=O(q/b)$ records therefore take
$$
 O\!\left(qb^{\tau-1}(\log(b+2))^\tau+q^{1/3}\operatorname{poly}(b)\right)=o(q\sqrt b).
$$
The two streams use $O(q)$ ever-visited bits. Reuse the same polynomial-in-$b$ control, basis and product workspace for every record, with all rewinds included above.

## Consecutive levels on the same stream order

Write $D=2c+1$, $\beta_0=1$, $\beta_1=\eta$ and complete the above ordered basis of $V$ by $\beta_2,\ldots,\beta_{D-1}$. Let $W_j$ be the span of its first $j$ vectors and
$$
 s_j(X)=\prod_{w\in W_j}(X-w),\qquad d_j=s_j(\beta_j)\ne0 .
$$
Then $s_0=X$ and $s_{j+1}=s_j^2+d_js_j$ by splitting the roots into $W_j$ and $\beta_j+W_j$. Induction proves additivity of every $s_j$. If $i=\sum i_h2^h$, define $B_i=\prod_hs_h^{i_h}$. Each $B_i$ is monic of degree $i$, so $B_0,\ldots,B_{2^j-1}$ form a basis for the actual polynomial remainders at level $j$. In particular the four-point basis is exactly $1,X,s_1,Xs_1$ with $s_1=X^2+X$. One may instead take $h_j=s_j/d_j$ throughout for normalized additive coordinates. The formulas then use $h_j(a)$ and unit difference. Crossing specifically between the two four-point conventions multiplies or divides its two upper coefficients by $d_1$, a single constant number of field products per four-word record.

On each representative bundle order level-$j$ records by the integer address with binary direction bits $D-1,\ldots,j$. Within each record order the coefficients by increasing $i<2^j$. The point representing a parent $W_{j+1}$-coset is $a=\alpha+\sum_{h>j}a_h\beta_h$. Its two children are consecutive in the level-$j$ order, first the child at $a$, then the one at $a+\beta_j$. The parent coefficients split into consecutive halves $A_i,B_i'$ since $B_{i+2^j}=s_jB_i$ for $i<2^j$. Reduction on the two children replaces these halves by
$$
 L_i=A_i+tB_i',\qquad H_i=L_i+d_jB_i',\qquad t=s_j(a).
$$
The inverse forms $B_i'=(L_i+H_i)/d_j$ and $A_i=L_i+tB_i'$. These coefficient identities hold on every local remainder. Output in the order $(L_i)_i,(H_i)_i$ is exactly the next forward pass's input; the analogous concatenation of the inverse halves restores the preceding order. Every child lies in the same retained bundle.

Compute all $d_j,d_j^{-1}$ and $s_j$ on the binary field basis and the $\beta_h$ by the displayed linearized recurrence in $\operatorname{poly}(b)$ steps, using only precomputed field values. On a given layer, select its table once. Test or enumerate the representative $\alpha$ as above, and initialize $s_j(\alpha)$ by a polynomial-size linear computation per representative. The higher-bit coset counter updates $t$ using the prefix of the ordered table $s_j(\beta_{j+1}),s_j(\beta_{j+2}),\ldots$ at amortized $O(b)$ head steps per parent, including return of its table head. Across all at most $D$ passes the outer enumeration, local starting values and table setup together cost $q^{1/3}\operatorname{poly}(b)$.

On one head per bank, copy a parent's first half to a scratch tape, rewind that tape, and pair it with the second half as the input advances. Emit the first output half directly, spool the second half to another scratch tape, then rewind and append it. Return both scratch heads to their fixed origins between parents. The same procedure handles inverse recombination. A $j$-bit counter marks each half length in $O(j+2^j)$ total counter steps. Hence all movement besides field arithmetic costs $O(b2^j)$ per parent. Rewind the two full stream banks once per pass and interchange their roles. The number of banks and scratch tapes stays fixed, and every pass uses the same intervals of length $O(q)$. Each short product's work heads can be cleared and returned to their fixed origins within its own time bound.

Let $\mu(b)$ bound one field-word multiplication including packing and reduction. For any $r$ consecutive layers within $W_0,\ldots,W_D$, in either order, the number of scalar pairs per layer is $R|V|/2=O(q/b)$, independent of $j$. The resulting bound is
$$
 O\!\left(q^{1/3}\operatorname{poly}(b)+rq\bigl(1+\mu(b)/b\bigr)\right)
$$
steps and $O(q)$ ever-visited bits. The binary integer operands in the explicit field product above have $O(b\log(b+2))$ bits. On these short operands the fixed-tape integer multiplication theorem gives $\mu(b)=O(b(\log(b+2))^2)$. Thus $r=O(\sqrt b/(\log(b+2))^2)$ fits $O(q\sqrt b)$. With fixed Toom-3 the same conclusion holds for $r=O(b^{3/2-\tau}/(\log(b+2))^\tau)$, including $\lfloor b^\epsilon\rfloor$ for every $0<\epsilon<3/2-\tau$. [Harvey and van der Hoeven, *Integer multiplication in time $O(n\log n)$*](https://annals.math.princeton.edu/2021/193-2/p04)

## Rounding the actual binary CRT caller

For $n$ input bits the unramified caller uses digit width $B=\lceil\log_2(n+2)\rceil$, $h=\lceil n/B\rceil$ input digits, the least $q_0=2^{b_0}\ge 2h$, and precision $H$ the least power of two at least $2B+\lceil\log_2(h+1)\rceil+2$. Take $b=3\lceil b_0/3\rceil$ instead, preserving $B,h,H$. Then $b_0\le b\le b_0+2$ and $2h\le q=2^b\le4q_0<16h$. The original guard $\deg(XY)<2h-1<q$ still holds. Since $b_0=B-O(\log B)$ and $b\le B+O(1)$, the same $b\le H\le8b$ holds for every sufficiently large $n$. Also $qH=\Theta(n)$, with absolute constants. Pairwise comaximality, the degree sum $q$ and the coefficient bound use exactly the same binary-factor and digit arguments at the adjusted degree. This constant-padding variant supplies an admissible field degree at every large input length. The entire factor directory keeps its separate $O(qb\,\operatorname{polylog}(b+2))$ generation charge in the full-precision caller. The binary prefix uses only its polynomial-size field and normal-element setup. [S005 unramified CRT caller, §§1–4](https://github.com/CubeJerry/integer-mult-bounds/blob/69632d87c99b5a75d0b44a7d964e6550e457e016/research/moonshot-overhead-program/sessions/2026-11-26-S005/route-a/unramified-polynomial-crt-caller.md)

The contiguous run may start at the point-value boundary $W_0$ or end at any chosen intermediate level. Its endpoints must have the specified representative ordering. Conversion from the binary coefficient input, conversion to the literal factor-directory encoding, the remaining transform stages and higher-precision carry maps are still open at the target bound.

The accompanying finite checker verifies the full direction degree, cyclic span and every quotient fixed count for $b=3,6,9,12,15,18,27$. At $b=3,6,9$ it independently interpolates all representative four-point remainders, reconstructs all binary evaluation points and checks all $D$ adjacent levels forward and backward. At the four larger degrees it evaluates five consecutive levels on four chosen cosets in both directions. Every tested intermediate polynomial is evaluated directly at every root of its coset. Exact root-padding checks cover all three padding amounts.

The additive stage and earlier scalar lower bound are described in [four-point additive CRT and Frobenius compression](https://github.com/CubeJerry/integer-mult-bounds/blob/335d099aa205220acc3941d77b6a8a9202f4488a/research/moonshot-overhead-program/sessions/2026-11-26-S006/four-point-frobenius-obstruction.md).

The kernel-checked [additive-layer semantics](../../contributions/explicit-overhead/formal/AdditiveTraceLayers.lean) identify the recursive forward map with evaluation of the stated product-basis polynomial at every ordered address. Under independent directions the inverse is two-sided for arbitrary rows at every depth. The Mathlib instantiation covers fields of characteristic two. The enumeration and tape estimates in this note are written proofs.

The [Frobenius transport proof](../../contributions/explicit-overhead/formal/BundleTransport.lean) establishes uniqueness of an omitted remainder on any conjugate coset. Its `finite_frobenius_remainder` connects the actual power map on finite Mathlib fields to the ordered target remainder of every binary coefficient list. `stable_coset_support` admits every anchor difference in the stable direction space, including a nonzero subspace translation. `reverse_transport` proves the explicit construction with the inverse field automorphism undoes the forward transport on arbitrary rows. The induced address permutation is chosen noncomputably for the semantics; the separate physical construction processes only the stored representatives.

## The contiguous binary coefficient input

The same bundle has a sparse vanishing polynomial at the opposite end of the transform. For $b=3c$, write $v=2^{2c+1}$ and $m=c-1$, so $q=v2^m$. Over $\mathbf F_2$ put
$$
 T(X)=X+X^{2^c}+X^{2^{2c}},\qquad S(X)=T(X)^2+T(X).
$$
On $K$, $T$ is the relative trace and $\ker S=V$, since $T(z)^2=T(z)$ is equivalent to $T(z)\in\mathbf F_2$. The polynomial $S$ is monic of degree $v$ and its $v$ distinct roots are exactly $V$. For any anchor $a$, $S(X)+S(a)$ is the vanishing polynomial on $a+V$. The formulas include $c=1$, when cancellation gives $S=X^8+X$.

**Binary coefficient prefix.** For $0\le r\le m$, one fixed multitape program converts the $q$ independent binary coefficients of any $f\in\mathbf F_2[X]_{<q}$, in increasing degree order, bijectively to $2^r$ consecutive ordinary binary polynomials $f_j$, each of degree below $q/2^r$, with
$$
 f(X)=\sum_{j<2^r} f_j(X)\,S(X)^{j2^{m-r}}.
$$
The output sorts $j$ in increasing order and the coefficients of each $f_j$ in increasing degree. Either direction takes $O((r+1)q+\mathrm{poly}(b))$ tape steps and $O(q)$ cells ever visited. In particular the first $\min(c-1,\lfloor\sqrt b\rfloor)$ levels from the caller's actual coefficient end meet the binary $O(q\sqrt b)$ budget. When $c=1$ there is a single identity record.

For the recursive split use $S_i=S^{2^i}=X^h+E_i$, $h=v2^i$, for $i=m-1,m-2,\ldots,m-r$. In characteristic two, squaring scales each exponent. The support of $S_i$ consists of at most six distinct powers of two, so $E_i$ has at most five terms, each of degree at most $h/2$. For one increasing-order parent $A+X^h B$ with both halves of degree below $h$, define
$$
 D(B)=\lfloor E_i B/X^h\rfloor,\qquad
 Q=B+D(B),\qquad R=A+(E_iQ\bmod X^h).
$$
The high half of $E_i B$ has degree below $h/2$. Thus $D^2(B)=0$. The high half of $(X^h+E_i)Q$ is $Q+D(Q)=B$. The low half has precisely the contribution removed from $A$. Consequently $A+X^hB=R+S_iQ$, with $\deg R,\deg Q<h$. Conversely any such pair gives $A=R+(E_iQ\bmod X^h)$ and $B=Q+D(Q)$. The output is physically $R$ followed by $Q$, so repeated splitting and reversed joining preserve the displayed binary order at every depth. This is ordinary monic quotient and remainder on unrestricted independent binary inputs.

Each of the at most five shifts of $E_i$ requires a constant number of scans of two $h$-bit words. Copies, XORs, rewinds and the final ordered write take $O(h)$ steps per parent. A scan is implemented by aligning the appropriate suffix and prefix of the two banks and then moving both heads one cell at a time. The binary counters at each marked end are little-endian and return their heads after an increment or decrement; the total carries over an interval of length $t$ cost $O(t+\log(h+2))$. Each initial shift or limit has $O(b)$ bits. The resulting additive setup per parent is $O(\mathrm{poly}(b))$ for a fixed polynomial and is absorbed by $h\ge v=2^{2c+1}$. A constant number of banks hold the current whole stream, the next stream and one parent's scratch. All layers reuse the same marked intervals. The sum of parent widths in any layer is $q$, and the short control and scratch regions fit the stated $O(q)$ cell cap. No field-word arithmetic occurs in this prefix.

At $r=m$ these are the ordinary base-$S$ digits, with degree below $v$. For each representative $a+V$ its **actual monomial remainder** is
$$
 \operatorname{rem}_{a+V} f(X)=\sum_{j<2^m} f_j(X)\,S(a)^j .
$$
The right-hand side has degree below $v$ and agrees with $f$ on $a+V$, proving the identity. It identifies the remaining simultaneous evaluation on the relative-trace values and the monomial-to-product-basis conversion at the top of the stored bundle. The full $m$-pass radix algorithm takes $\Theta(qb)$ as $b$ grows, because this implementation emits $q$ bits per level. The proved growing coefficient prefix and internal bundle layers have different endpoints. Their meeting transform and the literal factor-directory conversion remain unpriced at the target.

The [binary coefficient checker](verify-trace-coefficient-prefix.js) used six extension degrees from 3 through 18, 134 prefix round trips, 283 complete polynomial identities, and 99 independent ordinary long divisions. It checked 5,472 equality-of-evaluation instances on the actual bundle roots and classified all 4,680 field points at the four smaller degrees. Dropping the high correction, switching the child order or omitting a divisor term each had an explicit failing input.

The [Lean proof of the streamed split](../../contributions/explicit-overhead/formal/TraceCoefficientPrefix.lean) proves that the one-correction formulas give precisely Mathlib's ordinary polynomial quotient and remainder for every input at each actual Frobenius power of the displayed trace polynomial. It proves that the high-half feedback squares to zero. Its algebra applies to every characteristic-two field. The stream ordering and cumulative head-cost proof are given above.

<a id="grouped-binary-remainders"></a>

### A grouped binary CRT boundary of exactly $q$ bits

Write $W=\{t^2+t:t\in\mathbf F_{2^c}\}$, $M=|W|=2^{c-1}$, and $v=|V|$. Every $s\in W$ is an $S$-value and has exactly $v$ preimages in $K$. For each Frobenius orbit in $W$ choose a representative $s$, let $d_s$ be its length, and let $m_s(Y)\in\mathbf F_2[Y]$ be its monic minimal polynomial. Then
$$
 X^q-X=\prod_{[s]}m_s(S(X)).
$$
The factor at $s$ is monic of degree $v d_s$ and vanishes precisely on the $v d_s$ elements mapping to its orbit. These disjoint sets contain all $q$ points. This proves the identity, squarefreeness, and identification of each factor with the product of the original irreducibles having roots in those fibres. The sizes sum to $q$.

At full radix depth write $f_j(X)=\sum_{k<v}a_{jk}X^k$ and $g_k(Y)=\sum_{j<M}a_{jk}Y^j$. Then $f=\sum_{k<v}X^k g_k(S(X))$. The actual grouped binary remainder is
$$
 f\bmod m_s(S(X))
   = \sum_{k<v}X^k\,(g_k\bmod m_s)(S(X)).
$$
Each term after substitution has degree below $vd_s$ and the difference is divisible by $m_s(S)$. The polynomials $X^kS^j$ for $k<v$ and $j<d_s$ have distinct leading degrees $k+vj$ from $0$ to $vd_s-1$. Their coefficients therefore encode the ordinary grouped remainder bijectively. Since the $g_k$ are arbitrary independent binary polynomials of degree below $M$, CRT in $Y$ makes all $g_k\bmod m_s$ independent across $k$ and the different orbits. Exactly $v\sum_{[s]}d_s=q$ **binary coefficient bits** suffice at this boundary. Equivalently, the $k$th monomial coefficient of the coset remainder is $g_k(s)\in\mathbf F_{2^{d_s}}$, represented in the power basis of $s$. Orbit expansion requires the previously proved Frobenius transport when arbitrary ordered product bases are used.

This exact $q$-bit encoding is for the grouped monomial remainders. The fast internal butterfly schedule established above uses full $K$-words, with $(3+o(1))q$ physical bits. Converting from the smaller fields to that schedule, splitting each $m_s(S)$ into the caller’s individual irreducibles, and the entire precision lift still require algorithms at the target cost. The identity isolates $v$ independent length-$M$ binary transforms over the trace-zero index set. Even rearranging the $j$-major coefficient stream into $k$-major order needs an explicit bill. A basic fixed-tape upper bound is $O(qc)$ steps and $O(q)$ visited bits: cyclically rotate the least significant binary address bit to the top by splitting even and odd positions into two streams and concatenating them, or reverse a rotation by interleaving the two halves. At most $c-1$ inverse rotations transfer the $j$-block to the low end. All passes reuse the same three banks. This invoice leaves fast rearrangement and the reduced transforms open.

The checker independently forms each $m_s$ from its actual conjugate roots, composes it with $S$, and multiplies the resulting binary factors. At $b=3,6,9,12$ it recovered $X^q-X$ and compared 81 literal grouped remainders against ordinary binary long division. For example, at $b=12$, $v=512$ and the orbit degrees are $1,1,2,4$, giving $512(1+1+2+4)=4096$ bits. The comparison is about complete binary representations, with no cost assumption for converting between them.
