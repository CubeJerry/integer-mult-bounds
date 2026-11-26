# Independent review of the three-power representative butterfly

**Decision.** For $b=3c=3^t$, a single four-point/two-point remainder transition has a reversible fixed-tape implementation on the two specified representative layouts. It uses $O(q)$ visited cells and $O(q\,\operatorname{polylog}(b+2))$ time, which is $o(q\sqrt b)$ on this family. The input and output stores use the same Frobenius-orbit representatives of the same large bundles. Conversion from binary coefficients, conversion to a different collection of representatives and all carry maps are separate obligations.

## Which inputs the store represents

Let $K=\mathbb F_{2^b}$, $L=\mathbb F_{2^c}$, $E=\ker\mathrm{Tr}_{K/L}$ and $T=\ker\mathrm{Tr}_{L/\mathbb F_2}$. Since $[K:L]=3$, relative trace restricts to the identity on $L$ and $K=E\oplus L$. Because $c$ is odd, the second trace takes $1$ to $1$. Hence $V=E\oplus\mathbb F_2\cdot1$ has complement $T$ in $K$. One may choose any nonzero $\eta\in E$. It has degree $b$ since the unique maximal proper subfield is $L$, and $E\cap L=0$. The previously proved bound for $b=3^t$ makes $\langle1,\sigma^i\eta\rangle$ of dimension at least $1+2c$. It is contained in the displayed $V$ of exactly that dimension, so they coincide.

Represent each bundle by $B_t=t+V$ with $t\in T$. Choose one such $t$ per Frobenius orbit. The U-format stores the four coefficients of each $\{0,1,\eta,1+\eta\}$-coset remainder inside each retained $B_t$. The W-format stores the two global linear coefficients on each $\{0,1\}$-pair there. Each format on $B_t$ is invertibly equivalent to its $|V|$ point evaluations. For a binary input polynomial, the whole evaluation table satisfies $y_{\sigma z}=y_z^2$. Conversely this condition forces its degree-below-$q$ interpolant to have binary coefficients.

If a retained coset $B_t$ has Frobenius orbit length $h$, then after local interpolation its point table must satisfy $y_{\sigma^h z}=y_z^{2^h}$ on $B_t$. These conditions are necessary and sufficient. To extend a legal table to $\sigma^j B_t$, send the value at $z$ to its $2^j$-th power at $\sigma^j z$. Coprime or full orbit length is not required. Two such paths agree because their difference is a multiple of $h$ and the within-bundle condition can be iterated. Distinct coset orbits are disjoint. This proves a bijection from legal stores to all $q$ independent input bits. A store may contain redundant coordinates and its entries cannot be treated as independent arbitrary compressed data. The linear butterfly and its inverse can nevertheless run on any list of local coefficients, and preserve the reachable stores by their interpretation.

A key distinction is that $\sigma^j U$ need not equal $U$. Transport of an omitted U-remainder is established by first interpreting point values and interpolating on the desired new coset. The local algorithm never performs this global re-expansion, and the reconstruction proof attaches no fast bill to it.

## Counting and moving the actual records

The action on $T$ factors through the $c$-cycle on $L$. For $g=\gcd(i,c)$ its fixed points form the trace-zero slice in $\mathbb F_{2^g}$. Indeed the trace to $\mathbb F_2$ restricts to $(c/g)\mathrm{Tr}_{\mathbb F_{2^g}/\mathbb F_2}$ and $c/g$ is odd. Burnside's formula therefore gives
\[
 R=\frac1c\sum_{i=0}^{c-1}2^{\gcd(i,c)-1}.
\]
As $c$ tends through powers of three, the nonidentity terms have $\gcd(i,c)\le c/3$. Thus the literal store has
\[
 b|V|R=3q\bigl(1+O(c\,2^{-2c/3})\bigr)
\]
bits. This count uses full $b$-bit words, including all redundant internal coordinates. It changes the earlier scalar-orbit count by retaining entire representatives of large bundle orbits.

Use deterministic polynomial-in-$b$ field preparation as in [S005 FS1](https://github.com/CubeJerry/integer-mult-bounds/blob/69632d87c99b5a75d0b44a7d964e6550e457e016/research/moonshot-overhead-program/sessions/2026-11-26-S005/route-a/binary-factor-stream-compiler.md). Squaring matrices give bases of $E,T$ and an explicit complement $S$ to $U$ in $V$ by binary elimination. A nonzero nullspace vector gives $\eta$, and $\delta=\eta^2+\eta$ and $\delta^{-1}$ are prepared once. Enumerate all $t\in T$ and test if each is first in its orbit in a fixed ordering, in $2^{c-1}\operatorname{poly}(b)=o(q)$ steps. There is no need to look up an arbitrary bundle.

For a retained $t$, enumerate $a=t+s$ over $s\in S$. Precompute cumulative XORs of the ordered basis vectors of $S$. After an ordinary binary increment carries through $j$ positions, the corresponding cumulative vector updates the current field element using $O((j+1)b)$ tape steps including rewind of the basis directory. The geometric distribution of carry lengths gives $O(b)$ amortized steps per quartet. Initialization and final rewind per $t$ fit the existing $2^c\operatorname{poly}(b)$ term.

Both input and output orders put the two $W$-pairs consecutively inside the same quartet. Read the cubic in basis $1,X,s(X),Xs(X)$, with $s(X)=X^2+X$, as $P_0+sP_1$, $\deg P_j<2$. Write $Q_0=P_0+s(a)P_1$ and $Q_1=Q_0+\delta P_1$. The inverse computes $P_1=(Q_1-Q_0)/\delta$ and $P_0=Q_0-s(a)P_1$. These are a bounded number of field operations on $b$-bit polynomial-basis words per quartet. Short binary polynomial multiplication by Kronecker packing, fast monic reduction and a reused reciprocal have $b\operatorname{polylog}(b+2)$ bit cost with sequential conversions as in FS1. There are $R|V|/4=O(q/b)$ quartets. All numerical word scratch, bases and counters are reused on fixed tapes. Sequential input, output and return passes fit $O(q)$ cells ever visited, together with a reused polynomial-in-$b$ work interval. The same accounting applies in reverse.

## Exact finite controls

A separately written checker independently interpolates each cubic from its four point values, computes the W-pair linears directly from their two point values, and tests the proposed conversion and inverse. It then expands each resulting representative list through pointwise Frobenius solely as a correctness oracle. For $b=3$ it tests all 256 binary polynomials. For $b=9$ it tests all 512 binary basis monomials and eight dense polynomials. These give 512 and 33,280 quartet round trips, respectively. The literal stores have 24 and 2,304 bits for $q=8$ and $512$. In both cases a nonbinary value at the fixed point zero is rejected by the stabilizer check. These tests do not implement the asymptotic tape schedule.

A large bundle therefore does not imply a large cost for this one stage. An all-degree, both-direction binary CRT still needs the surrounding stages, the actual conversion to and from the caller's factor/monomial order, a joint absolute space schedule, and the separate precision/carry costs. This review does not assign a new $B(b)$ or $D(b,t)$ to UC6.

The critical-chain reviewer proposed the construction and tape schedule. The CRT worker independently checked the Galois descent, counts, local physical bill, and exact finite controls. Prepared for Jerry Chen (@CubeJerry), with substantial AI assistance.
