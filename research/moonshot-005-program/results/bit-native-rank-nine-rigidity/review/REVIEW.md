# Native rank-nine rigidity from the normal equations

Let $O$ be the directed graph of orthogonal pairs among the 111 authenticated roots and $K=I+O$. Work over a field $F$ of characteristic two. The fitting locus consists of $111$ by $111$ blocks of size $b$, with diagonal $I_b$, arbitrary blocks on the 6,470 directed foreign edges and zero elsewhere. Its canonical point is $K\otimes I_b$. All matrices here act on original labelled roles.

## Independent tangent computation

Let $V=F^{111}$, and let $E$ be the space of scalar matrices supported on the directed foreign edges. At a matrix $K$ of rank nine the tangent to the locus of rank at most nine consists of the $A$ with $A\ker K\subseteq\operatorname{im}K$. Indeed, choose any nonsingular nine-by-nine pivot block, eliminate it, and differentiate the complementary Schur equation. This is precisely the map

\[
 \Phi:E\longrightarrow\operatorname{Hom}(\ker K,V/\operatorname{im}K),\qquad
 A\longmapsto (v\mapsto A v\bmod\operatorname{im}K).
\]

The checker forms $K$ from actual root dot products. Independent binary row reductions give pivot indices $0,1,2,4,8,9,14,30,59$ and complete bases of the left and right nullspaces, each of dimension 102. For each pair of basis vectors $u,v$, form the equation $u^TAv=0$ directly in the 6,470 allowed directed edge positions. The resulting 10,404 equations have rank 6,360, so the allowed tangent has dimension 110. For each native role $t$, the oriented incidence vector of the edges incident to $t$ satisfies every equation. Their rank is 110, hence

\[
 \ker\Phi=\{A_{ij}=O_{ij}(z_i-z_j):z_i\in F\}.
\]

The binary calculation extends to all characteristic-two fields, since rank is witnessed by a binary minor and the binary dependencies persist. The coordinate-wise decomposition of $F^b\otimes(F^b)^*$ shows the same normal equations act independently on the $b^2$ payload matrix entries. Thus the complete block tangent has dimension $110b^2$. It consists exactly of $A_{ij}=O_{ij}(Z_i-Z_j)$ for arbitrary $Z_i\in M_b(F)$. Allowing diagonal variables as a fault increases the scalar tangent dimension to 221. In contrast, each one of the 6,470 isolated directed edge perturbations has nonzero compressed rank one.

## Formal deformations and the connected component

Let $R=F[[t_1,\ldots,t_m]]$, with maximal ideal $\mathfrak m$. Suppose a fitting $M$ over $R$ specializes to $K\otimes I_b$ and has vanishing $(9b+1)$-minors. The old $9b$ pivot minor is a unit. If $M$ has been reduced to $K\otimes I_b$ modulo $\mathfrak m^d$, its homogeneous error at order $d$ satisfies the normal equations from the Schur complement. For each monomial separately, the block tangent calculation writes it as a native conjugation difference. Conjugate by a block diagonal matrix $\operatorname{diag}(I_b+Z_i)$ with $Z_i$ homogeneous of degree $d$ to remove that error. These successive matrices converge $\mathfrak m$-adically. Consequently

\[
 M=\operatorname{diag}(G_i)(K\otimes I_b)\operatorname{diag}(G_i)^{-1},\qquad G_i\equiv I_b\pmod {\mathfrak m}.
\]

Fixing $G_{i_0}=I_b$ at one native root removes the common right factor. The same induction works for every commutative separated, complete local characteristic-two ring $A$ with residue field $F$: each $\mathfrak m^d/\mathfrak m^{d+1}$ is an $F$-vector space, the finite normal system tensors with it, and representatives of the resulting role differences can be lifted independently into $\mathfrak m^d$. The resulting units converge in the complete ring. A coefficient-field splitting and Noetherian hypotheses are unnecessary for this formal statement.

One obtains a global separation statement over an algebraic closure. In the affine scheme of all native fits of rank at most $9b$, the canonical gauge orbit is an open and closed irreducible component. To see openness, choose a spanning tree of the undirected native graph, with one directed block pointing from each parent to its child. On the open set where those 110 oriented blocks are invertible, there is a regular, unique normalization making them all $I_b$ and fixing the root gauge. The open set is the product of $\operatorname{GL}_b^{110}$ and this normalized fitting slice. At the canonical point of the slice every tree-edge tangent is zero; because all tangent vectors are exactly incidence differences, the entire slice tangent is zero. Its local ring is Noetherian with maximal ideal $\mathfrak n$. Vanishing $\mathfrak n/\mathfrak n^2$ and Nakayama's lemma give $\mathfrak n=0$. Hence the canonical slice point is isolated and reduced. In a finite-type Noetherian scheme an isolated reduced local point is open in a neighborhood and is an irreducible component disjoint from the others. Translating by the gauge group makes the full canonical orbit open.

Closedness holds even if singular foreign blocks are allowed elsewhere. On the orbit the identities $M_{ij}M_{ji}=I_b$ hold on every edge. Let $P_i$ be the ordered product taking the directed tree path from the fixed root to $i$, and $Q_i$ the product of the opposite directed blocks in reverse order. The polynomial identities $M_{ij}=P_i Q_j$ on all foreign edges and the reciprocal identities cut out exactly the orbit: they force $Q_i=P_i^{-1}$ and $M_{ij}=P_iP_j^{-1}$, with $P_{i_0}=I_b$. This is a closed subscheme, isomorphic on the displayed open set to $\operatorname{GL}_b^{110}$. Thus a connected algebraic family of native rank-at-most-$9b$ fits meeting the canonical orbit lies entirely in it. This does not assert all rank-at-most-$9b$ fits are connected to the canonical one.

## Exact price of a square-zero perturbation

For any scalar matrix $A$ and $N\in M_b(F)$ with $N^2=0$, let $r=\operatorname{rank}N$ and $\delta=\operatorname{rank}(v\mapsto Av\bmod\operatorname{im}K\mid\ker K)$. There is a basis of the payload with $r$ two-dimensional Jordan blocks and $b-2r$ zero coordinates. Each Jordan block gives

\[
 \begin{pmatrix}K&A\\0&K\end{pmatrix}.
\]

Projection of its image to the lower space has rank nine. In the upper kernel of that projection, the image is $\operatorname{im}K+A\ker K$, of dimension $9+\delta$. Summing the independent copies proves the exact identity

\[
 \operatorname{rank}(K\otimes I_b+A\otimes N)=9b+r\delta.
\]

It holds for every scalar $A$. For native-supported $A$ and nonzero $N$, it assigns zero excess precisely to a native coboundary. In that case $G_i=I_b+z_iN$ realizes the actual fitting as a gauge conjugate. The receipt recomputes whole binary block ranks for isolated and reciprocal directed edges and for a nonzero native coboundary at $(b,r)=(2,1),(4,1),(5,2)$.

The same image calculation covers a collection of payload perturbations $D_{ij}$ satisfying $D_{ij}D_{kl}=0$ for every pair of directed edges. Their common image span $U$ lies in their common kernel, so splitting $F^b=U\oplus C$ gives a single upper triangular block with diagonal $K\otimes I_U,K\otimes I_C$. Its exact excess is the rank of the compressed map $\ker(K\otimes I_C)\longrightarrow\operatorname{coker}(K\otimes I_U)$ induced by the off-diagonal perturbation. Individual square-zero of each block need not provide these pairwise annihilations.

Run `python -B check.py --repo REPO --out OUT`. Credit the original 111 native roots, canonical rank-nine fit, retained orbit equations and the scalar factor-tangent candidate. Independently derived and checked with substantial OpenAI assistance.
