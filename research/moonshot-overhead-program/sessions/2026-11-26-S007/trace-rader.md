# Packed binary traces at the full degree-`c` CRT boundary

Put $N=2^c$, $m=N-1$, $H=N^2$ and $Q=HN$. The actual child inputs are the $H$ independent binary polynomials $p_k$ of degree below $N$. We use coefficient-major rows of $H$ arbitrary lane bits. On the output side the rows are keyed by (factor in the supplied FS1 directory, coefficient of its residue in increasing monomial degree), again with lane varying fastest. The equivalent lane-major format is recovered by the two equal-field interchanges on an $N$-by-$N^2$ bit rectangle. This note supplies an exact two-way reduction to one binary scalar transform on $m$ rows. For prime $m$, that transform reduces to a single fixed ordinary binary convolution per lane. General $m$ has the same trace inverse; the prime-specific permutation must then be replaced by the divisor/unit-group analysis.

## A square binary transform with its dual inverse

Use $K=\mathbf F_{2^c}$, a primitive multiplicative generator $\zeta$, any normal $\gamma$, and the trace-dual element $\delta$ satisfying
$$
 \operatorname{Tr}(\delta\gamma^{2^j})=\mathbf1_{j=0},\qquad 0\le j<c.
$$
The trace pairing is nonsingular, and all conjugates of $\gamma$ form a basis. Its dual consists of the corresponding conjugates of $\delta$. In particular both $\gamma,\delta$ have absolute trace one, since a normal basis cannot sum to zero. The use of two trace elements is essential in general.

Temporarily consider one polynomial $p$. Save $u=p(0)$. In increasing exponent order put $x_0=p_0+p_m$ and $x_i=p_i$ for $1\le i<m$. The $m$ other output bits are
$$
 y_a=\sum_{i\bmod m}x_i\operatorname{Tr}(\gamma\zeta^{ai})
     =\operatorname{Tr}(\gamma p(\zeta^a)),\qquad a\bmod m.
$$
The saved $u$ describes the factor $X$. The row $a=0$ describes the different factor $X+1$. Restore $x$ from arbitrary $m$ binary bits by
$$
 x_i=\sum_{a\bmod m}y_a\operatorname{Tr}(\delta\zeta^{-ai}).
$$
Indeed the $(i,j)$ entry of the proposed inverse times the forward matrix, computed inside $K$, is
$$
 \sum_{r,s=0}^{c-1}\delta^{2^r}\gamma^{2^s}
       \sum_{a\bmod m}\zeta^{a(j2^s-i2^r)}
 =\sum_{t:\,j2^t\equiv i\bmod m}\operatorname{Tr}(\delta\gamma^{2^t})
 =\mathbf1_{i=j}.
$$
Here $t=s-r\bmod c$, $2^c\equiv1\bmod m$, and the order-$m$ geometric sum is 1 when its exponent vanishes and 0 otherwise because $m$ is odd in characteristic two. This argument includes $i,j=0$, repeated congruences from proper Frobenius periods, and $c=1$. Squareness gives the reverse identity for arbitrary independent $y$. Recover $p_0=u$ and $p_m=x_0+u$. Saving, folding, and unfolding cost $O(Q)$ including head returns.

Projected Fourier transforms over the base field are classical. Hong and Vetterli give a general treatment of the connection to finite-field Hartley transforms. The present statement fixes the particular two projection elements, handles every short orbit and the extra affine point, and connects both directions to the specified literal binary CRT. [Hong and Vetterli, IEEE Trans. Information Theory 39 (1993)](https://doi.org/10.1109/18.259646)

## Exactly the FS1 rows and their price

For each nonzero exponent orbit $\mathcal O=\{a_0,2a_0,\ldots,2^{d-1}a_0\}$ take $a_0$ least in ordinary integer order, starting with representatives of exponents in $0,\ldots,m-1$. Here “nonzero” refers to the field evaluation point; the exponent orbit $\{0\}$ is included. Set $\alpha=\zeta^{a_0}$ and form its degree-$d$ minimal binary polynomial $h$. This $h$ occurs exactly once in the supplied FS1 stream, irrespective of the field or normal basis FS1 used at degree $d$. Define the $d\times d$ matrix
$$
 E_{j,i}=\operatorname{Tr}_{K/\mathbf F_2}\!\left(\gamma\alpha^{i2^j}\right),\qquad 0\le i,j<d.
$$
The $j$th trace row in this orbit is $\operatorname{Tr}(\gamma v^{2^j})$ for $v=p(\alpha)$. The $d$ binary monomial coefficients of $p\bmod h$ therefore map, in the displayed order, to exactly those rows by $E$. If all $d$ trace rows vanish, repeat them periodically out to $c$. Trace invariance then gives that $v$ pairs to zero with every conjugate of $\gamma$. Trace nonsingularity makes $v=0$, so all monomial coefficients were zero. Thus $E$ is invertible even for $d<c$ and for $a_0=0$. The factor $X$ simply copies the saved row. No coordinate change between unrelated FS1 finite-field representations is necessary: the reduced binary polynomial is independent of the selected root of the same irreducible.

Setup is within $O(N\operatorname{poly}(c))$ fixed-tape steps and cells. Use FS1's prepared degree-$c$ field and normal basis and solve the trace-dual linear system. Factor the $c$-bit integer $m$ by trial division up to $\sqrt m$, and test field candidates with the usual order test $z^{m/p}\ne1$ at each distinct prime $p\mid m$. At most $N$ candidates are examined. Compute exponent cycles by $\le c$ ordinary modular doublings per exponent and roots by modular powering. Make skinny directory lists (minimal polynomial, FS1 rank) and (minimal polynomial, exponent, conjugate index). Ordinary tape mergesort, merge join and numerical re-sort give the exact forward and inverse destination tables. Gaussian elimination builds each $E^{-1}$ once in finite $\operatorname{poly}(c)$ work per orbit. These lists and all field arithmetic are negligible against $Q=N^3$. A direct alternative generates the degree-$d$ FS1 polynomials from its own supplied choice of fields and normal elements before the skinny join.

Insert the $X$ row and route the $N$ whole $H$-bit rows into (FS1 rank, conjugate index) order, or reverse this routing by their saved source indices. The dimension condition in Tal, Corollary 6.2 is satisfied since $H=N^2$. Thus each direction costs $O(Qc/(1+\log(c+2))^\eta)$ for every fixed rational $0<\eta<1/2$, with $O(Q)$ cells visited, including row keys, setup, clearing and head returns. [Tal, §§2.3, 6](https://eccc.weizmann.ac.il/report/2026/331/download/)

The coordinate-major input $[j<d][k<H]$ of each orbit also needs a physical conversion before its local matrix tiles. Pad $d$ to a power of two below $2d$ and move its at most $\lceil\log_2 d\rceil$ address bits from the left of $k$ to the right. Each one-bit move is a bounded number of complete stable split/join scans, copying each branch to a distinct work tape and then concatenating the branches in the appropriate fixed prefix. Equivalently in reverse, use alternating rows to split by the selected trailing bit. Each move costs $O(dH)$ with the same $O(dH)$ local marked interval; read the slices consecutively and reuse this interval between groups. Trimming yields $[k][j]$. Apply $E$ or $E^{-1}$ to consecutive tiles of $d$ lanes at a time by exact binary matrix multiplication and return the small coordinate field to the original side of $k$ on output. With the same fixed rank exponent $12/5$ and fixed-tape block simulation as [the S007 word conversion](grouped-ambient-words.md), the total new matrix bill is $O(\sum_h Hd^{7/5})=O(Qc^{2/5})$. The moves cost $O(Q\log(c+2))$. At most one partial last tile per group occurs; $H\ge d$ absorbs it. These charges also apply in reverse with independently chosen residue vectors. All streams, scratch banks, finite controls and setups reuse $O(Q)$ cells ever visited. For literal lane-major endpoints add the priced rectangular interchange, $O_\rho(Qc^\rho)$ for any fixed $1/2<\rho<1$.

If $\mathcal T(m,H)$ is the cost of the displayed scalar trace matrix on $m$ records of $H$ bits (or its specified dual), this gives the complete child transform at $\mathcal T(m,H)+O(Qc/(1+\log(c+2))^\eta)$ and the same linear external space plus any kernel scratch. Conversely the paid local conversions and folding realize either trace matrix from the corresponding true child CRT at this price. The input and output exhibit exactly $Q$ independent bits. In the restricted implementation that computes and writes a full $c$-bit field result for every one of the $m$ multiplicative points for **each individual binary lane**, those mandatory output writes alone cost $\Omega(Qc)$ steps. Keeping all these outputs visits $\Omega(Qc)$ cells; producing one tile at a time saves space while retaining the write cost. Packing several independent lanes into one extension-valued polynomial is outside this restricted implementation. The direct scalar trace matrix is also dense: for every unit $a\bmod m$, the sequence $\zeta^{ai}$ covers $K^\times$ and a nonzero trace takes value one on exactly $N/2$ positions. Computing those dot products by separately inspecting each selected input costs $\Omega(HN\varphi(m))$ operations in that further restricted class. Neither count bounds general circuits or multitape algorithms for the packed transform.

## Prime multiplicative order

Suppose $m>1$ is prime. Choose an integer generator $g$ of $(\mathbf Z/m)^\times$ by testing the factors of $m-1$. Factorization and generator search each take at most $O(m\operatorname{poly}(c))$ steps of setup. Let $t(a)=\operatorname{Tr}(\gamma\zeta^a)$ and $L=m-1$. In increasing $v\bmod L$ route $x_{g^{-v}}$ to $I_v$; fix $K_w=t(g^w)$. The single ordinary cyclic convolution
$$
 C_w=\sum_{v\bmod L}I_v K_{w-v}
$$
produces $y_{g^w}=C_w+x_0t(0)$ for every $w$. The missing row is $y_0=t(0)\sum_i x_i$. Here $t(0)=1$. Use the same formula with $t(a)=\operatorname{Tr}(\delta\zeta^{-a})$ for inverse. Integer exponents in the displayed forward/negative positions matter. This is Rader's prime-length reindexing applied after base-field projection, so all convolution coefficients are literally bits. [Rader in Bernstein, §4.8](https://doi.org/10.1007/s40993-022-00402-0)

Compute all discrete-log directory entries by *enumerating* powers of $g$ and sorting skinny (exponent,position) pairs. No unit-time discrete logarithm oracle or full payload lookup is required. Two paid wide-record sorts gather the $I_v$ and restore $C_w$, costing the same $O(Qc/(1+\log(c+2))^\eta)$ per direction. The parity row is accumulated by scanning and XORing with one $H$-bit bank, rewound once per row; adding the repeated $x_0$ row also costs $O(Q)$. A fixed ordinary polynomial product with length-$L$ binary kernel yields this circular convolution by folding its high part once. This reduces the former scalar kernel to **one common fixed binary operand of length $N-2$ for every lane** with linear-size row storage.

For an unconditional tape clock here, append two zero rows to the $L$ rows so the spatial dimension is $N$, then transpose the $N$-by-$H$ rectangle into contiguous lane inputs. Apply the Harvey–van der Hoeven finite-field polynomial multiplier at $p=2$ separately to each lane and the shared true binary kernel, resetting both operand and scratch heads each time. Fold the length-$2L-1$ product and remove/reinsert padded rows before transposing back. Their unconditional Theorem 1.1 gives $O(L\log L\,4^{\log^*L})$ steps per lane. Its own time bounds its visited cells, and $L\log L\,4^{\log^*L}=o(Q)$. Per-invocation visited extrema can be tracked and reset in that many steps; different lanes reuse the same scratch origins. Both prescribed child directions therefore take $O(Qc\,4^{\log^*c})$ steps, $O(Q)$ visited cells, for these degrees. This is a fallback above the desired root budget. Its use does not assume infinitely many Mersenne primes, and the stated prime reduction alone gives no all-degree asymptotic family. [Harvey and van der Hoeven, Theorem 1.1](https://www.texmacs.org/joris/cyclomult/cyclomult.pdf)

The [finite replay](verify-trace-rader.py) checks the two projected binary matrices on every column in both orders for $1\le c\le9$. It tests both normal-basis choices for genuine Duval degree/Lyndon directories and arbitrary independent coefficient and residue batches, comparing Euclidean remainders and independent CRT idempotent recovery. Real widths $H=N^2$ are used through $c=5$. Prime reindexing is compared on every column for $c=2,3,5,7$ and on a full $8191$-bit round trip at $c=13$, with separate field-Horner probes. [Counts](trace-rader-cases.json)
