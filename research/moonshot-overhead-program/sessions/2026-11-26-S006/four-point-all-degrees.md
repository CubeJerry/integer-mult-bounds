# Four-point Frobenius support at arbitrary extension degree

**Extension of C001-CRT4.** Let $K=\mathbb F_{2^b}$, $q=2^b$, $\sigma z=z^2$, $\eta\in K\setminus\mathbb F_2$ and $d=[\mathbb F_2(\eta):\mathbb F_2]$. Set $W=\{0,1\}$ and $U=W+\mathbb F_2\eta$. Consider the ordinary four-point remainder on every coset of $U$, in global monomials or a local graded basis of degrees $0,1,2,3$. For every $b\ge16$, separate normalized canonical words for the scalar/Frobenius classes of the actual stage coordinates require at least $qd/16$ bits. In particular this is $\Omega(qb)$ for a full-degree $\eta$ at every sufficiently large degree $b$, including composite $b$. This proves a representation cost for this additive stage. Other choices of $\eta$ need their actual $d$, and joint encodings or cross-stage fusion remain outside the claim.

## Stabilizer and exact row action

Let $\Gamma$ be the subgroup of $\mathbb Z/b$ consisting of $i$ with $\sigma^i U=U$; write $r=b/|\Gamma|$. Since $\sigma$ fixes 0 and 1 and $\sigma^i\eta$ remains nonbinary, $i\in\Gamma$ exactly when $\sigma^i\eta=\eta+c_i$ for $c_i\in\mathbb F_2$. The map $i\mapsto c_i$ on $\Gamma$ is an additive homomorphism with kernel the multiples of $d$ modulo $b$. The image is trivial or has order two. In the second case $d$ is even, and the nontrivial element of $\Gamma/(d\mathbb Z/b)$ is the unique element of order two in $\mathbb Z/d$. Hence
\[
 r=\begin{cases}
 d/2 & d\text{ is even and }\sigma^{d/2}\eta=\eta+1,\\
 d   & \text{otherwise}.
 \end{cases}
\]
In particular $\sigma U=U$ exactly when $\eta^2=\eta+1$, equivalently $d=2$. Thus global monomial coordinates and the actual graded basis $1,X,s,Xs$ with $s=X^2+X$ admit one-step monomial transport exactly in the $\mathbb F_4$ case. The basis polynomials here have binary coefficients, so conjugation simply permutes stable cosets. Necessity follows from the leading row. A general local graded basis can change sufficiency through its own lower coordinates.

For clarity, let $E$ evaluate polynomials of degree below $q$ at all points of $K$. The binary-reachable tables $y$ satisfy $y_{\sigma z}=y_z^2$. Conversely interpolation and Frobenius force all their coefficients to be binary. The tables span $K^q$ over $K$ because $E$ is invertible and binary coefficient vectors span the input. Thus a power of a linear row with support $S$, on binary inputs, agrees with the restriction of a linear row supported on $\sigma^iS$; an equality up to a nonzero scalar on reachable inputs is a genuine row equality.

The leading monomial coefficient on $A=a+U$ is
\[
    \ell_A(y)=D_U^{-1}\sum_{z\in A} y_z,\qquad
    D_U=\prod_{v\in U\setminus\{0\}}v.
\]
The Lagrange denominator at every $z$ is $D_U$ since $z-(A\setminus\{z\})=U\setminus\{0\}$. Graded top coordinates differ only by a fixed nonzero scalar. A conjugate leading row matches another leading row only if $\sigma^i A$ itself is a $U$-coset, which forces $i\in\Gamma$. For $i\in\Gamma$, $\sigma^i$ permutes the nonzero members of $U$, hence fixes $D_U$, and a match does occur up to the allowed scalar. Inserting other rows as intermediate identifications cannot merge distinct such orbits because the projective Frobenius transformations compose.

## Counting good cosets uniformly in $b$

Call $A$ good if its $b$ conjugates are pairwise disjoint. A bad coset has $A\cap\sigma^i A\ne\varnothing$ for at least one $1\le i<b$ after translating a conjugate pair by a Galois automorphism. Then $a+\sigma^i a\in U+\sigma^i U$. Both two-planes contain $W$, so the latter set has at most eight elements. The binary linear map $a\mapsto a+\sigma^i a$ has kernel $\mathbb F_{2^{\gcd(i,b)}}$. Counting all possible preimages, summing over $i$ and dividing the number of translates by four gives
\[
 G_b:=\#\{\text{good cosets}\}\ \ge\
 q/4-2\sum_{i=1}^{b-1}2^{\gcd(i,b)}.
\]
The right side may be negative for small $b$. For $b\ge16$ the sum is at most $(b-1)2^{b/2}$ and $2(b-1)2^{b/2}\le q/8$, so $G_b\ge q/8$. The last estimate holds at 16 and the exponential factor on the right grows by $\sqrt2$ per increment of $b$, faster than $b/(b-1)$.

On a good coset the four points lie in four distinct full $b$-element point orbits. Arbitrary values on these points extend compatibly by squaring around the orbits and filling other orbits with zero. Interpolation gives a binary-coefficient polynomial. Each good top row is therefore surjective onto $K$, and uniform on $K$ for uniformly random binary inputs. Its entire scalar/Frobenius class has this marginal property because nonzero fixed scaling and any Frobenius power are bijections. One representative must hold a full $b$ bits in canonical scalar slots, or in mean length under separate prefix coding.

The subgroup $\Gamma$ acts freely on the good cosets. The preceding support identity gives exactly $G_b/|\Gamma|$ classes of good top rows, and at least that many separate representatives in a layout for the whole stage. Their cost is at least $rG_b$. Since $r\ge d/2$, this is at least $qd/16$ for $b\ge16$. Writing the corresponding canonical word stream requires the same bit volume even if its storage is reused. The fixed-alphabet costs follow up to absolute constants. The inverse butterfly visits the same specified state, as proved in the original four-point note.

The one-step statement is specifically about two-planes containing $1$. An odd composite degree divisible by three has a stable trace-zero plane in its $\mathbb F_8$ subfield, which does not contain $1$. For even $b$, taking $\eta\in\mathbb F_4\setminus\mathbb F_2$ is a genuine stable case and yields only an order-$q$ lower bound here. This extension supplies no bound for general binary CRT, the actual carry or complete multiplication.

## Independent verification

The accompanying exact finite checker tests all 840 nonbinary field elements in degrees $4,6,8,9$ against the stabilizer formula. For one representative of each of the 14 observed $(b,d,r)$ cases, it builds all actual $1,X,s,Xs$ interpolation weights, checks monomial closure by normalized row signatures, computes binary ranks of all good leading rows, and counts their projective classes. The stable $\mathbb F_4$ choices at degrees 4, 6 and 8 pass as positive controls. The degree-9 trace-zero plane exercises the exclusion above.

| $b$ | $d$ | $r$ | Good cosets | Good top classes |
|---:|---:|---:|---:|---:|
| 6 | 2 | 1 | 12 | 2 |
| 6 | 6 | 3 | 12 | 6 |
| 6 | 6 | 6 | 4 | 4 |
| 8 | 2 | 1 | 48 | 6 |
| 8 | 8 | 4 | 48 | 24 |
| 8 | 8 | 8 | 44 | 44 |
| 9 | 3 | 3 | 126 | 42 |
| 9 | 9 | 9 | 121 | 121 |

The table reports the actual checker representative at each displayed $(b,d,r)$; the number of good cosets can depend on $\eta$. The lead proposed the all-degree strengthening. The CRT worker checked the argument and wrote independent finite controls. This is AI-assisted mathematical review for Jerry Chen (@CubeJerry), not a Lean check or external human review. The additive FFT and UC caller attributions in the original note apply.
