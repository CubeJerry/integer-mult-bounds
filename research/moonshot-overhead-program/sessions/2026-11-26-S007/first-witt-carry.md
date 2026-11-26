# The first lift of the literal polynomial CRT

The [two-stage outer transform](macro-triadic-product.md) improves the single modulo-four square below to $O_\eta(qb/(1+\log b)^\eta)$ steps and $O(q)$ cells. All remaining operations in formula (1) fit the same clock by the [complete binary directory](binary-transform-and-product.md). The first carry and the complete bidirectional modulo-four FS1 transform therefore both achieve that clock. The $O(qb)$ and $O(qb\log b)$ constructions below are independent fallback estimates. [Converse reduction](first-carry-converse.md)

Let $b=3c$, $q=2^b$, and keep the FS1 order of the monic irreducible factors $g$ of $X^q-X$ over $\mathbf F_2$. For their literal zero-one coefficient lifts, the modulo-four CRT and its inverse admit an $O(qb)$ deterministic fixed-tape algorithm with $O(q)$ cells ever visited. A direct older convolution supplier in the same construction gives $O(qb\log(b+2))$. The sharper bound uses the [wide modulo-four convolution compiler](mod-four-batch.md). The only global operation beyond a fixed number of [binary CRTs](full-plane-crt.md) and near-linear local work is the divided square
$$
H(F)(X)=\sum_{i<j}f_i f_j X^{i+j},\qquad f_i\in\mathbf F_2 .
$$

## Literal factors and the monomial output

Work in $K_g=\mathbf F_2[X]/g$, with $z=X\bmod g$ and $d=\deg g$, including $d=1$ and every proper subfield degree. In the length-two Witt coordinates, $[x]=(x,0)$ and $2[t]=(0,t^2)$. Addition of $(a,A),(b,B)$ gives $(a+b,A+B+ab)$. Thus the second Witt component of a literal binary polynomial $F([z])$ is $H(F)(z)$. The first is $F(z)$. A shift from $[z]$ to $\alpha=[z]+2[t]$ adds $(tF'(z))^2$ to the second Witt component by first-order Taylor expansion. The same rule holds for the actual factor $g$. As $g'(z)$ is a unit, the unique choice of $t$ satisfies
$$
 t=\sqrt{H(g)(z)}/g'(z).
$$
It gives a root of the literal factor. Evaluation there identifies its monic degree-$d$ quotient over $\mathbf Z/4$ with $W_2(K_g)$. Both are free of rank $d$ over $\mathbf Z/4$ and the evaluation on the $d$ power-basis columns reduces to the usual isomorphism over $\mathbf F_2$.

Write the true monomial remainder $r+2k$ with bit coefficients and degree $<d$. Comparing $F(\alpha)$ with $r(\alpha)+2k(\alpha)$ gives
$$
 k(z)=\sqrt{\,H(F)(z)+H(r)(z)\,}
       +\frac{\sqrt{H(g)(z)}}{g'(z)}\big(F'(z)+r'(z)\big). \tag{1}
$$
Here $r=F\bmod g$ and $r'$ is its specified polynomial derivative. The local $H(r)$ term converts from Witt coordinates back to literal monomial coefficient digits. Squaring (1) checks both occurrences of inverse Frobenius. The derivative shift agrees with [S005 factor-lift transport](../2026-11-26-S005/route-a/factor-lift-carry-transport.md).

Compute $F'$, all $r$, and $H(F)\bmod(X^q-X)$ in coefficient order. The latter is one fold because $\deg H(F)\le2q-3$; every high monomial $X^j$, $j\ge q$, maps to $X^{j-q+1}$. Two further binary CRT calls supply $F'\bmod g$ and $H(F)\bmod g$ everywhere. For each compact factor, obtain $H(g)$ and $H(r)$ from ordinary packed integer squares: separate input bits by $\lceil\log_2(d+2)\rceil$ bits and read the second bit of each product digit. The square coefficient is its zero-or-one diagonal plus twice the unordered-pair count. Integers have $O(d\log(d+2))$ bits here. For a field square root, write $g=g_e(X)^2+Xg_o(X)^2$ and likewise $p=p_e^2+Xp_o^2$. Because $g'(z)=g_o(z)^2\ne0$,
$$
 \sqrt{z}=g_e(z)/g_o(z),\qquad \sqrt{p(z)}=p_e(z)+\sqrt{z}\,p_o(z).
$$
Compact polynomial half-GCD, products and reductions cost $d\operatorname{polylog}(d+2)$ tape steps per factor, as in the [local arithmetic analysis](point-factor-directory.md). The sum over the FS1 stream is $O(q\operatorname{polylog}(b+2))$ and fits the binary CRT clock. A local workspace polynomial in $b$ is reused throughout.

For arbitrary input coefficients $F_0+2F_1$, add $(F_1\bmod g)$ to the $k$ of (1). For the inverse, first invert the supplied binary low remainders to get $F_0$. Evaluate (1) on it and add the resulting carry to the supplied high remainders. One binary inverse recovers $F_1$. All sums of upper digits in these last steps are over $\mathbf F_2$.

## A physical divided-square supplier

A single square of the literal $F$ in $(\mathbf Z/4)[X]$ returns $H(F)$ in the second coefficient bits. Choose $M=3^Q$ minimally with $\varphi(M)>2q-2$, so $M=O(q)$. Embed $F$ in
$$
 S_M=(\mathbf Z/4)[W]/(W^{2M/3}+W^{M/3}+1).
$$
The ordinary square fits below $\varphi(M)$, hence suffers no cyclotomic reduction at the root. Use the triadic recursion of [Cantor–Kaltofen, §§2–3, especially Lemmas 2.2 and 3.1](https://kaltofen.math.ncsu.edu/bibliography/91/CaKa91.pdf).

For $Q>3$ set $u=\lfloor Q/2\rfloor+1,\ v=Q-u,\ m=3^u,\ n=3^v$. Then $m=3n$ or $9n$ and $n\varphi(m)=\varphi(M)$. Group coefficients with exponents $in+j$ into $n$ words $A_j(Y)$ in $S_m$, with $Y=W^n$. For two operands let $C_j$ denote their ordinary outer product coefficients in $S_m$. The untwisted cyclic product returns $U_j=C_j+C_{j+n}$. For the second product use the twist $\delta^j$ on both inputs, where $\delta=Y^{m/(3n)}$. Inverse transform and untwist to get $V_j=C_j+\omega C_{j+n}$, $\omega=\delta^n=Y^{m/3}$. Here $1+\omega+\omega^2=0$ and $(\omega-1)(\omega^2-1)=3$, a unit modulo four. Hence $C_{j+n}=(V_j-U_j)(\omega^2-1)/3$ and $C_j=U_j-C_{j+n}$. Return the $n$ small words $C_j+YC_{j+n}$. Each cyclic product uses pointwise multiplication after ordinary length-$n$ transforms with principal root $Y^{m/n}$; the cyclotomic identities over the integers specialize to $S_m$. The total number of small products is exactly $2n$.

A radix-three stage takes linear time in the current $\varphi(M)$-coefficient volume. Split the stream at its selected trit into three banks, process aligned triples, and interleave the banks in a monotone pass. Every twiddle is a monomial power of $Y$. Embed a length-$2m/3$ word in $m$ coefficients, rotate modulo $Y^m-1$, then subtract the high third from each lower third. A constant number of head scans suffices. Shift arithmetic and control per word take $\operatorname{poly}(Q)$ steps, absorbed by $m$. Digit reversal takes $O(Q)$ radix passes on these words. For the original $i,j$ transpose on individual coefficients, pad each of the two dimensions to a power of two (at most fourfold), and use $O(Q)$ transpositions of two bit-address positions at linear volume per swap. Reconstruction uses the inverse transpose. [Tape interchange with one-bit fields](https://github.com/openai/math/blob/3344da59991ed94f9ba711217b29c1d760badfa6/preprints/The-logarithmic-exponent-of-integer-multiplication-on-tapes-November-24-2026/build/interchange.tex#L18-L30)

Thus normalized time satisfies $\tau(Q)\le2\tau(\lfloor Q/2\rfloor+1)+O(Q)$. Subtracting two from the recursion parameter gives the usual halving recurrence, so $\tau(Q)=O(Q\log(Q+2))$. With bounded direct base cases this yields $O(qb\log(b+2))$ steps. Keep waiting parent banks once on suspension stacks and pop successive child packets directly from a pending stream, placing replies on an output stream. No child traverses the preceding packets. Each individual child has size $\varphi(m)=\varphi(M)/n$ and the children are sequential. Parent extents and active descendants therefore fit $O(q)$ marked cells on a fixed number of tapes, reused throughout.

For the sharper clock, perform just that first Cantor–Kaltofen layer. Its $2n$ child products all have length $s=\varphi(m)$, and $2n=s$ or $s/3$. They form a batch fitting $B\ge s^{1/2}$; repeated inputs in a square are permitted for an algorithm correct on arbitrary pairs. Apply the [wide modulo-four compiler](mod-four-batch.md), using its enlarged fixed native groups for this aspect. A child returns an ordinary product. Fold it modulo $Y^m-1$ and then reduce its high third as above, in $O(s)$ time. The batch volume is $2n\varphi(m)=2\varphi(M)=O(q)$, with $O(qb/(1+\log b)^\eta)$ batched work. The top-level triadic passes cost $O(qb)$ and dominate; peak visited cells stay $O(q)$. The modulo-four batch uses the independently priced conventional short product above, so the two uses of polynomial multiplication are well founded.

## Checks on actual factors

The [independent program](check-first-witt-carry.py) compares (1) to signed monic division modulo four. It covers all binary inputs for $b=1,2,3,4$, and basis, pair and dense inputs at $b=6$. It also checks every full modulo-four input for $b=1,2,3$. There are 425,222 binary factor comparisons, 72,163 of them in proper nonprime subfields, and 262,944 full modulo-four factor comparisons. Packed integer squaring agrees with the direct unordered-pair sum on 68,021 inputs. [Exact counts and counterexamples](first-witt-carry-receipt.json)

For $g=X^2+X+1$ at $b=4$, $F=X^2$ has high residue $1+X$; omitting the square root gives $X$. At the same factor, $F=1+X$ has high residue zero; omitting $H(r)$ gives $1+X$. For $g=X^3+X+1$ at $b=6$, $F=X^3$ has high residue $1+X$ while omitting the literal-root shift gives $X+X^2$. These factors lie in genuine proper subfields. Equation (1) and the two-bit supplier resolve the first lift. General precision and the campaign's smaller square-root overhead require additional work.
