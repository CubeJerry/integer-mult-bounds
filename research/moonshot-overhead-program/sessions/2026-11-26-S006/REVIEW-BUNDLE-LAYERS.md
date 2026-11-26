# Independent review of consecutive additive layers on representative Frobenius bundles

**Result.** Let $b=3c$, $q=2^b$ and $K=\mathbb F_q$. There is a specified layout for each of $2c+2$ successive additive-remainder states. It uses $(3+o(1))q$ literal bits with all finite-field coordinates stored as full $b$-bit words. On these supplied layouts, any $r$ consecutive transitions take $O(rq(1+\log(b+2))^3+2^c\operatorname{poly}(b))$ multitape bit steps in either direction and $O(q)$ cells ever visited. In particular an unbounded number $r=\max(1,\lfloor\sqrt b/(1+\lceil\log_2(b+2)\rceil)^3\rfloor)$ fits $O(q\sqrt b)$, with the finite initial range handled directly. The starting and ending state use the same orbit representative for each large bundle. This decision concerns a proper part of the binary transform.

## The field, quotient and real stored words

Write $\sigma(x)=x^2$, $L=\mathbb F_{2^c}$ and $E=\ker\operatorname{Tr}_{K/L}$. The trace on $L$ is the identity because $[K:L]=3$, so $K=E\oplus L$. Define $V=E\oplus\mathbb F_2\,1$ of dimension $v=2c+1$. If $e_i=\sigma^i\alpha$ is a normal basis, take $\eta=e_0+e_c$. Its cyclic support $\{0,c\}$ has period $3c$: a translation interchanging the two indices would require $2c=0\bmod 3c$. The conjugates of $\eta$ generate the even-parity plane in each of the $c$ triples $\{i,i+c,i+2c\}$. These planes form $E$, since the relative trace sums all three coordinates on each triple. Thus $\eta$ has field degree $b$, and $V$ is exactly the Frobenius span of $U=\langle1,\eta\rangle$ for this choice. This construction also works for even $c$. A different nonzero vector of $E$ need not have the same orbit dimension for general $c$.

The quotient $K/V$ is Frobenius-isomorphic to $L/\mathbb F_2$. For $0\le i<c$ and $g=\gcd(i,c)$ the quotient has
\[
 |\operatorname{Fix}(\sigma^i)|=2^{g-1}\bigl(1+\mathbf1_{\,2\mid c/g}\bigr).
\]
Indeed $\sigma^i x+x=0$ has a $g$-dimensional kernel on $L$. In a normal basis on $L$, its $g$ cycles each have length $c/g$, and the vector $1$ has all coordinates one: the sum of the basis vectors is fixed and nonzero by independence. An equation with right side $1$ is soluble exactly when each cycle has even parity, hence exactly when $c/g$ is even. Each soluble equation has $2^g$ solutions and each quotient class uses two solutions. Burnside gives $R=c^{-1}\sum_{i<c}|\operatorname{Fix}(\sigma^i)|$ representative bundles. For $i>0$, $g\le c/2$. Consequently
\[
 b\,2^v R=3q\bigl(1+O(c\,2^{-c/2})\bigr).
\]
The count includes every full field coordinate, including within-bundle redundancy.

Choose any binary linear complement to $\mathbb F_2\,1$ in $L$ to represent classes, then select the least representative of each quotient orbit in a fixed order. This section need not commute with Frobenius. For a selected $t$ of quotient period $h$, write $\sigma^h t=t+\epsilon$, $\epsilon\in\{0,1\}$. The local point table $Y_t(v')=Y(t+v')$ satisfies
\[
 Y_t(\sigma^h v'+\epsilon)=\sigma^h Y_t(v').
\]
These stabilizer conditions are necessary and sufficient. Transport from the retained bundle to every conjugate uses $Y(\sigma^i z)=\sigma^iY(z)$. Any two paths differ by a multiple of $h$, for which the displayed condition supplies consistency. Different orbits are disjoint. A full equivariant table has a unique degree-below-$q$ interpolant with binary coefficients, since conjugating its coefficients preserves its values at all $q$ points. Conversely every such binary polynomial supplies an equivariant table. Every local remainder state below is bijective to the retained point tables, so its legal inputs have exactly $q$ independent bits. For $c=2$ the nonzero class of $\mathbb F_4/\mathbb F_2$ is fixed and every lift has $\epsilon=1$. Ignoring the translation already fails on $Y(X)=X$. Reconstructing conjugate bundles is a semantic argument. The local tape operations never request an omitted bundle.

## A compatible coefficient order for every stage

Fix an ordered basis $v_0=1,v_1=\eta,v_2,\ldots,v_{v-1}$ of $V$. Let $W_j=\langle v_0,\ldots,v_{j-1}\rangle$ and $S_j(X)=\prod_{u\in W_j}(X-u)$. Then $S_0=X$, $\gamma_j=S_j(v_j)\ne0$ and $S_{j+1}=S_j^2+\gamma_j S_j$. Induction gives binary-linearity in the argument. Extend the ordered basis of $V$ by a basis of the chosen section to obtain a full basis of $K$. The resulting ordinary additive evaluation descent uses exactly these as its bottom $v$ stages. The products $B_h=\prod_{i:h_i=1}S_i$ are monic of degree $h$, so the first $2^j$ form a basis of degree-below-$2^j$ remainders in the global variable $X$.

At stage $j$, on representative $t$, enumerate the cosets
\[
 a+W_j,\qquad a=t+\sum_{i=j}^{v-1}x_i v_i
\]
in increasing ordinary binary order of the high indices $x_i$. In each coset store its interpolation remainder in increasing $B_h$ order, $0\le h<2^j$. At stage $j+1$ a parent polynomial is $P_0+S_jP_1$, with $P_0$ and $P_1$ in the contiguous low and high coefficient halves. Its two children at anchors $a$ and $a+v_j$ are
\[
 Q_0=P_0+S_j(a)P_1,\qquad Q_1=Q_0+\gamma_jP_1.
\]
These agree with the parent on their respective cosets by additivity. The inverse obtains $P_1=(Q_0+Q_1)/\gamma_j$ and $P_0=Q_0+S_j(a)P_1$. Output the whole low child followed by the whole high child. This is exactly the next stage's input order in both directions. The case $j=0$ outputs polynomial-basis field words at $t+\sum_i x_i v_i$ in binary order.

The same proof allows one consistent choice of normalization at each index. Replace $S_j$ by $S_j/\mu_j$, where $\mu_j$ is $1$ or $\gamma_j$. The two-child formula uses twiddle $S_j(a)/\mu_j$ and gap $\gamma_j/\mu_j$. Relative to the monic format, coordinate $h$ is multiplied by $\prod_{i:h_i=1}\mu_i$. A switch of an existing interface's normalization requires these diagonal factors. The claimed schedule can use the monic choice throughout.

## Fixed-tape costs, including reusable storage

The standing [S005 field construction](https://github.com/CubeJerry/integer-mult-bounds/blob/69632d87c99b5a75d0b44a7d964e6550e457e016/research/moonshot-overhead-program/sessions/2026-11-26-S005/route-a/binary-factor-stream-compiler.md) supplies deterministic polynomial-in-$b$ preparation of a binary field and a normal basis. Gaussian elimination gives the basis and section above. The linearized coefficients of all $S_j$, values $S_j(v_i)$, required inverses and binary-counter cumulative increments use polynomial preparation and $O(b^3)$ table bits. Nothing in these tables has length $2^j$. Entries such as $\gamma_j^{-1}$ are prepared once, independently of the data.

Enumerate the $2^{c-1}$ possible class representatives and test each for orbit minimality by iterating Frobenius on $L/\mathbb F_2$. The projection to the chosen section occurs after conjugation. This can be repeated as a sequential generator at each level using polynomial local cells. The total bill $r2^c\operatorname{poly}(b)$ is $2^c\operatorname{poly}(b)=o(q)$ for $r\le b$. Field and flag preprocessing are polynomial. Scanning all quotient candidates has the separate exponential-in-$c$ bill just charged.

At a level $j$, $S_j(t)$ starts the twiddle for each selected bundle. Advancing a high-prefix counter through $k$ trailing ones changes the twiddle by the precomputed XOR of the first $k+1$ active table entries $S_j(v_i)$. The required cumulative value is found by scanning $k+1$ adjacent $b$-bit records and returning to the beginning. Ordinary binary increment and rewind fit the same bill. Carry lengths have geometric frequency in every complete prefix enumeration, so the amortized motion is $O(b)$ per parent. Stage selection, initialization and rewinds per representative cost $\operatorname{poly}(b)$ per representative, already covered above.

A parent has $2^j$ pairs of coefficients. Copy its first half to a sequential scratch bank and rewind. Read it jointly with the second input half, write the first output half to the next bank, and buffer the second output half on another tape. Rewind the second-output buffer, append it, then return the scratch heads to their markers. The reverse scan has the same structure, with $Q_0,Q_1$ as the two input halves and $P_0,P_1$ as output. All local bank motion is linear in the parent size. Alternating two complete stream banks between levels and returning their heads costs $O(q)$ per level even when $j$ grows. A fixed number of banks suffice, and their visited intervals are reused.

Each pair uses a fixed number of local field operations. In a polynomial basis, binary polynomial convolution can be packed into $O(b\log(b+2))$ bits by spacing input coefficients by $\lceil\log_2(b+1)\rceil$ bits. The parity of each digit of the integer product is its binary-convolution coefficient. Fixed monic reduction uses the reversed modulus and its prepared truncated inverse, a constant number of local products and scans. The published multitape $O(t\log(t+2))$ integer multiplier on these short words, together with sequential packing, extraction and local head returns, fits $O(b(1+\log(b+2))^3)$ per field operation. Each stage has $R2^{v-1}=O(q/b)$ pairs. All local numerical work regions occupy $\operatorname{poly}(b)$ cells and are revisited at the same markers. The above store, banks and re-used polynomial work regions therefore have $O(q)$ total visited cells through the entire chain. The stated time follows, including setup and returns. A crude field implementation with $O(b^2)$ work per pair would not justify this time.

## Which root parameters can use these indices

For the [S005 integer caller](https://github.com/CubeJerry/integer-mult-bounds/blob/69632d87c99b5a75d0b44a7d964e6550e457e016/research/moonshot-overhead-program/sessions/2026-11-26-S005/route-a/unramified-polynomial-crt-caller.md), write $B=\lceil\log_2(n+2)\rceil$, $h=\lceil n/B\rceil$ and choose its original exponent $b_0$ with $2h\le 2^{b_0}<4h$. Choose instead $b=3\lceil b_0/3\rceil$. Then $0\le b-b_0\le2$ and $2h\le q=2^b<16h$. Keep the same coefficient precision $H$, the least power of two at least $2B+\lceil\log_2(h+1)\rceil+2$. The integer product coefficients satisfy the same guard $h(2^B-1)^2<2^H$, and its degree is below $2h-1<q$. Since $b=B-O(\log B)$ up to additive constants and $H\le (6+o(1))B$, one still has $b\le H\le8b$ eventually and $qH=\Theta(n)$. This shows cofinal availability of the stated degree family at every root length with at most four times the original number of field points. A caller using the new degree must construct its factor and carry interfaces for that degree. The binary block arithmetic itself uses $b$-bit field words and no $H$-bit lift.

The missing binary operations include the initial conversion from the caller's independent monomials, the complement of these layers, and the terminal conversion to the caller's irreducible-factor order and polynomial residues, in both directions. Global re-expansion of omitted bundles has no small cost attached here. Neither a full binary CRT cost nor any new higher-precision remainder digit cost has been established.

## Independent exact replay

The accompanying verifier builds each subspace polynomial in two ways. It compares every intermediate list with independent Lagrange interpolation in the global monomial basis followed by triangular change to the product basis. It tests two constant and two alternating conventions for the normalization at successive levels, every corresponding inverse, and the actual terminal point order. It rejects a forced unit gap, reused anchor twiddles, interleaved children and applying normalized formulas to unconverted monic input. For $b=3,6,9$ it uses all representative bundles and every binary basis monomial, eight dense binary inputs, and four arbitrary local field tables. For $b=12,15,18,27$ it checks three six-level slices, including nonzero high prefixes, on the latter twelve input families.

| $b$ | $v$ | $R$ | Representatives with nonzero affine shift | Compared intermediate lists |
|---:|---:|---:|---:|---:|
| 3 | 3 | 1 | 0 | 480 |
| 6 | 5 | 2 | 1 | 6,080 |
| 9 | 7 | 2 | 0 | 58,688 |
| 12 | 9 | 4 | 2 | 1,728 |
| 15 | 11 | 4 | 0 | 1,728 |
| 18 | 13 | 8 | 2 | 1,728 |
| 27 | 19 | 30 | 0 | 1,728 |

All 72,160 forward or reverse intermediate lists match, across 5,456 round trips. The quotient fixed counts are checked for every exponent modulo $c$ in every field. For $b=3,6,9$ a separate reconstruction of the full equivariant table covers all 8, 64 and 512 points, respectively. At $b=6,12,18$ the polynomial $X$ rejects dropping each observed nonzero stabilizer translation. The finite checker uses dense interpolation and pseudorandom normal-basis test fixtures. The asymptotic algorithms use the field preparation and sparse subspace-polynomial computations described above.

The critical-chain and lead reviewers developed the large-bundle and consecutive-layer constructions. The CRT worker independently derived the coefficient, stabilizer, layout and tape identities and ran this separate finite implementation. Prepared for Jerry Chen (@CubeJerry) with substantial AI assistance.
