# Four-point additive CRT stages and Frobenius compression

**C001-CRT4.** At every prime extension degree $b\geq 5$, the ordinary four-point additive remainder stage on parallel cosets fails the proposed monomial Frobenius transport. For its actual graded coefficients, a layout retaining one normalized scalar per conjugacy class requires $\Omega(2^b b)$ bits. Arbitrary joint encodings and transforms that fuse across the four-point boundary remain open.

## The additive block in both directions

Write $K=\mathbb F_{2^b}$, $q=2^b$ and $\sigma(z)=z^2$. Evaluation $E$ identifies $K[X]_{<q}$ with $K^K$. Binary input means every polynomial of degree below $q$ with coefficients in $\mathbb F_2$.

For an additive subspace $U$ of size $m$ and each coset $A=a+U$, put $p_A=\prod_{z\in A}(X-z)$. The partial transform $C_U$ outputs the $m$ coefficients of $f\bmod p_A$ for all $q/m$ cosets, in a prescribed local basis. This map is invertible over $K$ by interpolation on each coset. At this full partial stage the top coordinate in any basis of successive degrees $0,\ldots,m-1$ is a nonzero scalar multiple of the leading monomial coefficient.

Take $W=\{0,1\}$, $\eta\notin W$, $U=W+\mathbb F_2\eta$, and $s(X)=X^2+X$. Write the cubic remainder on $a+U$ as $P_0+sP_1$ in the graded basis $1,X,s,Xs$, with $\deg P_i<2$. Its two linear remainders on $a+i\eta+W$ are
\[
 Q_i=P_0+t_iP_1,\qquad t_i=s(a+i\eta),\quad i=0,1.
\]
This follows because $s$ is constant on either pair. Conversely $P_1=(Q_1-Q_0)/(t_1-t_0)$ and $P_0=Q_0-t_0P_1$, with $t_1-t_0=\eta^2+\eta\ne0$. This is the usual additive evaluation butterfly. The four-point leading coefficient is the coefficient of $X$ in $P_1$. These formulas go both ways on every independent local polynomial. See Algorithm 2 of [Li, Chen, Kuo, Cheng and Yang, *Frobenius Additive Fast Fourier Transform*](https://arxiv.org/abs/1802.03932).

## Which coordinate identities persist on binary inputs?

The reachable evaluation tables are exactly the tables satisfying $y_{\sigma z}=y_z^2$. One implication is evaluation of a binary polynomial. For the other, interpolate a unique $f$ of degree below $q$. Then $f^{(2)}(z^2)=f(z)^2=f(z^2)$ everywhere, so uniqueness makes every coefficient binary. The reachable set spans $K^q$ over $K$ because the binary coefficient vectors contain all $q$ standard basis vectors and $E$ is invertible.

In evaluation coordinates, every row belonging to $A$ is supported inside $A$. Lagrange interpolation gives the leading coefficient row
\[
 \ell_A(y)=\sum_{z\in A}
       \frac{y_z}{\prod_{w\in A\setminus\{z\}}(z-w)} .
\]
All weights are nonzero. Its support equals $A$.

For a row $\ell(y)=\sum c_z y_z$ with support $S$, its $2^i$-th power on reachable tables equals the restriction of the $K$-linear row $\sum\sigma^i(c_z)y_{\sigma^i z}$, supported on $\sigma^i S$. Equality up to a fixed nonzero scalar with any other row on the binary inputs therefore implies equality of the corresponding $K$-linear rows on all evaluation tables. This spanning argument prevents false identifications induced by testing only binary coefficients.

Consequently a monomial transport of all graded stage rows under $\sigma$ requires $\sigma A$ to fit inside a $U$-coset. Both sets have $m$ elements. Equality forces $\sigma U=U$. Conversely, when $\sigma U=U$, coefficient conjugation in the global monomial basis permutes the remainder polynomials by $p_A^{(2)}=p_{\sigma A}$. Thus Frobenius stability of $U$ is necessary and sufficient for monomial transport in the global monomial coefficient layout. Necessity also holds in any local graded layout, with arbitrary reorderings and nonzero fixed normalizations.

If $S$ also denotes coordinatewise squaring on arrays, the transported semilinear map is $C_U S C_U^{-1}$. For $C_W=L C_U$, any pair of monomial descriptions must satisfy $L M_U=M_W L^{(2)}$. Inverting $L$ gives the equivalent inverse relation. The $W$-state in global coordinates $1,X$ admits monomial transport since $W$ is stable. Failure of the four-point state therefore blocks both directions of this actual layer, even allowing the proposed monomial permutations to exchange records globally. The inverse starts from the corresponding reachable evaluations, equivalently from binary CRT residues after any correct conversion to evaluations.

## Prime degrees and arbitrary coset-local bases

For prime $b\ge5$, no two-dimensional $U$ is stable. If it were, $\sigma|_U$ would have order dividing both $b$ and $|\mathrm{GL}_2(2)|=6$. It would fix $U$ pointwise, contrary to $\mathrm{Fix}(\sigma)=\mathbb F_2$. Any $\sigma^i$ with $1\le i<b$ generates the same Galois group, so none stabilizes $U$. Thus the leading row on $A$ is equivalent to no other actual stage row under any Frobenius power and fixed scalar. The identity power supplies no other row either, by invertibility.

There is a stronger necessity for arbitrary invertible coset-local coordinates. In a closed monomial layout, if $z,z'$ share a row's support, every $\sigma^i(z-z')$ belongs to $U$ because every transformed row is supported on a $U$-coset. Each row is therefore supported in a coset of $U_*=\bigcap_{i=0}^{b-1}\sigma^i U$. For the four-point family, every $\sigma^iU$ contains $W$, and every nontrivial conjugate is a different two-plane, hence $U\cap\sigma^iU=W$ for $1\le i<b$. A row mixing the two $W$-pairs in $A$ has no partner under any nonidentity power. If no row mixes them, invertibility forces exactly two independent rows on each pair. Such a re-encoding has reduced the four-point state to separate two-point coordinates. It has not produced a monomial four-point mixing step.

## Amount of materialized data

Call $A$ good when its $b$ conjugates are pairwise disjoint. A nontrivial intersection between any two conjugates implies $A\cap\sigma^i A\ne\varnothing$ for some $1\le i<b$. Then $a+\sigma^i a\in U+\sigma^i U$. The left-hand map has kernel $\mathbb F_2$, and the set on the right has size at most $m^2$. Summing over $i$, at most $2m^2(b-1)$ translates $a$ can be bad. Since the condition is constant on cosets, at least $q/m-2m(b-1)$ cosets are good.

All $m$ points of a good coset lie in distinct full $b$-element Frobenius orbits. Assign arbitrary values in $K$ to them, extend the assignments by squaring around each orbit, and set other orbits to zero. Interpolation gives a binary-coefficient polynomial with these values. Thus every nonzero row on a good coset ranges over all of $K$ and is uniform on $K$ for uniformly chosen binary input.

Consider the specified representation that stores one separately decodable normalized scalar per equivalence class of the actual stage coordinates under fixed scalar multiplication and any Frobenius power. Each good leading row is a separate class requiring a full $b$-bit slot. With $m=4$ its slots alone use at least
\[
              b\,[q/4-8(b-1)]=\Omega(qb)
\]
bits along the primes. Separate prefix codes for the scalar values also have at least this mean length, by their uniform marginals and linearity of expectation. Jointly the reachable state still has only $q$ independent bits. More generally, one genuine pair-mixing row on a fixed positive fraction of all cosets already gives the same order, since only $O(b)$ cosets are bad.

A fixed alphabet requires $\Omega(qb)$ visited cells to materialize the canonical slots. Emitting all these words as a stream can reuse cells but writes $\Omega(qb)$ bits, which exceeds $q\sqrt b\,(\log(b+2))^C$ for every fixed $C$ along these degrees. The cost holds even with all conjugations, scalars and directories supplied at no cost. It is a property of this emitted representation, not an information or running-time lower bound for alternative CRT algorithms.

The support criterion also rules out a simple length adjustment for an entire ordinary graded additive flag. Monomiality at every layer now forces every member of the flag to be Frobenius-stable. S005 showed by normal-basis characteristic polynomial that this is possible only for a power-of-two extension degree. For $b_0=2^h+1$ take the integer input length $n=3b_0\,2^{b_0-3}$. Its UC digit width is $b_0+O(\log b_0)$, so its digit count is asymptotic to $3\cdot 2^{b_0}/8$. Its required scale $2\,(\mathrm{digit\ count})\le q<4\,(\mathrm{digit\ count})$ selects $q_0=2^{b_0}$. The next eligible extension degree $2^{h+1}=2b_0-2$ gives $q'=q_0^2/4$. Even the padded binary array alone exceeds $O(n)$ on these lengths. A different packing or skipping actual layers needs a separate analysis.

## Decision and verification

Freeze scalar-orbit materialization through these graded, parallel additive-coset stages. Neither the binary CRT supplier $B(b)$ nor the literal first carry $K_1$ or aggregate higher-precision budget in UC6 improves. The result leaves other partitions, jointly coded states, fused stages that do not emit these rows, and other integer callers open.

The accompanying finite replay solves $M C_U^{(2)}=C_U$ directly by dense elimination for stable and unstable stages. It separately computes the binary rank of the top row by its values on the monomial inputs. At degrees $5,7,11$, the respective coset counts are $8,32,512$, with $5,28,506$ good cosets. The top row has full binary rank on $6,29,507$ cosets. These are finite controls for the proof, with no charge of dense elimination to a prospective fast supplier.

Li et al. establish Frobenius-additive acceleration on Cantor data and assume power-of-two extension degree in Theorems 3.4–3.5. [Gao and Mateer](https://www.math.clemson.edu/~sgao/papers/GM10.pdf) also give additive FFTs in arbitrary ambient binary extension fields with arithmetic operation counts. The support and materialization proof answers the more specific stage and tape question posed in S005. No literature priority or general impossibility claim is made.

The S005 UC, FS, KC and FL authors supplied the distinct CRT caller and carry problems. Prepared for Jerry Chen (@CubeJerry), with substantial AI assistance.
