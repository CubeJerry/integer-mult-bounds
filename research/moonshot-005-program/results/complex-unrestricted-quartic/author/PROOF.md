# A quartic head fixes both original ports in every three-native LUL caller

Consider the actual normalized complex natives

\[
 L=\begin{pmatrix}a&0&0\\1&a&0\\0&0&1\end{pmatrix},\qquad
 U=\begin{pmatrix}a&-a^2&0\\0&a&0\\0&0&1\end{pmatrix}.
\]

Here $a=1_{\rm pre}\otimes A^{\otimes W}$ on a bank of dimension $D$, $A=C_bR$ on four tail bits with $C_b=((1+i)1+(1-i)X_b)/2$ and $R|a,b,c,d\rangle=(-1)^{abd}|b,c,d,a\rangle$. In particular $A$ and $A^{-1}$ have two flat entries per row and column, and $A^2$ has four. Ordinary coefficients have a fixed finite catalogue of collective root-four tail monomials and freely varying coefficients on a fixed prefix. Each claimed interstage or endpoint unit has an ordinary inverse. The proof uses arbitrary such units algebraically. Physical compilations are asserted only for the literal control below.

**Theorem.** Let $E=LCUQL=O\,\operatorname{diag}(F_{r_j})I_{\rm in}$, where $C,Q,O,I_{\rm in}$ are arbitrary ordinary units and the three independent Gaussian heads are invertible on whole banks. A rank-$r$ head has $2^r$ flat entries per tail row and column, with modulus $2^{-r/2}$ and ordinary boundary monomials permitted. For all sufficiently large faithful widths, if any head has rank four, all other heads have rank at most two and at least one has rank zero. The ordered profile is therefore at most $(4,2,0)$. At a quartic head $j$ one has

\[
 I_{\rm in}^{-1} e_j=e_1 v,\qquad e_j^T O^{-1}=u e_0^T
\]

for invertible one-bank ordinary coefficient matrices $u,v$ at the width in question. The row $e_0^T E$ and column $E e_1$ contain quartic words only, and $E_{01}$ is invertible. The profile bound is attained on every positive width by $C=Q=1$. No restriction on either interstage's spectator or active blocks precedes this conclusion.

## Why a degree-three inverse can identify an original input

For projectively distinct one-letter unitaries $g,h$ their tensor-lift normalized Gram entry has absolute value $(|\operatorname{tr}(g^*h)|/16)^W\to0$. Combining equal labels with their true width phases first, each fixed finite joint list is independent for sufficiently large widths. A finite fixed prefix is handled by coefficient entries. In particular an expression whose individual labels have maximum absolute entry strictly less than one has zero intersection with the ordinary catalogue. Every monomial translate of $F_r$ still has exactly the same maximum and the same number of entries. A product having $d$ factors from $A,A^{-1}$ separated by monomials has at most $2^d$ entries per column. Multiplication by one inverse Gaussian on either side increases the maximum entry by at most $\sqrt2$. These are statements about word labels before taking linear combinations. A large scalar coefficient does not alter its projective word label. Widths divisible by four suffice for uniform impossibility.

The literal inverses are

\[
 L^{-1}=\begin{pmatrix}a^{-1}&0&0\\-a^{-2}&a^{-1}&0\\0&0&1\end{pmatrix},\qquad
 U^{-1}=\begin{pmatrix}a^{-1}&1&0\\0&a^{-1}&0\\0&0&1\end{pmatrix}.
\]

For a quartic write $x=I_{\rm in}^{-1}e_j$, $y=Oe_j$. The identity

\[
 QLx=U^{-1}C^{-1}L^{-1}y F_4
\]

has maximum at most $(\sqrt2)^3/4=1/\sqrt2$ on every one-letter term at right. The ordinary component of $QLx$ vanishes by separation. Multiplication on the left by $Q^{-1}$ preserves the ordinary space and its nonordinary complement, since multiplying a nonmonomial label by a monomial cannot make it monomial. Thus the ordinary component of $Lx$ vanishes. It is exactly $(0,x_0,x_2)^T$. Hence $x=e_1 v$, and $v$ is invertible since $x$ is injective on a $D$-dimensional bank. Indeed $I_{\rm in}$ supplies an ordinary left inverse to $v$.

At the other end put $z=e_j^T O^{-1}$, $b=e_j^T I_{\rm in}$. The row identity

\[
 z L C=F_4 b L^{-1}Q^{-1}U^{-1}
\]

uses the same bound and right ordinary invariance. The ordinary component of $z L$ is $(z_1,0,z_2)$. Thus $z=u e_0^T$, with $u$ invertible by surjectivity and the corresponding ordinary right inverse. Only here have the genuine physical input and output ports been identified.

## Forced interstage flags and the ordinary residual corner

From the isolated column and row, every nonzero word of $e_0^T E=u^{-1}F_4 b$ and $E e_1=y F_4 v^{-1}$ is quartic. In particular $H=E_{01}=u^{-1}F_4 v^{-1}$ because $z y=1$. The spectator input in $E_{02}$ skips the rightmost Gaussian and the spectator output in $E_{21}$ skips the leftmost. Their words have at most $2^{1+2}=8$ entries per column. Thus $E_{02}=E_{21}=0$.

Write $c_{ij}=C_{ij}$, $q_{ij}=Q_{ij}$. The actual corner is

\[
 H=a\,[c_{00}a q_{01}+c_{01}a q_{11}-c_{00}a^2q_{11}+c_{02}q_{21}]\,a.
\]

Inside the brackets the four-, two-, and one-support sets are disjoint. Surrounding each one-letter word by the same $A$ on both sides is a bijection on projective labels. In particular these three sets stay mutually disjoint, even when multiple paths inside one set cancel. The one- and two-support terms can have at most eight entries after the two exterior factors; the isolated corner is purely sixteen-support. Their entire contributions therefore vanish by separation, leaving the **unprojected** equality $H=-a c_{00}a^2q_{11}a$. At every such faithful width full rank $D$ of the product makes both $c_{00},q_{11}$ genuine rank-$D$ square operators. No inverse of a projected matrix or degree piece is used.

Removing the sole exterior $a$ from $E_{02}=0$ gives

\[
 -c_{00}a^2q_{12}+(c_{00}a q_{02}+c_{01}a q_{12})+c_{02}q_{22}=0.
\]

The four-, two-, and one-support components separately vanish. The first forces $q_{12}=0$, the second $q_{02}=0$. Now $Qe_2=e_2q_{22}$ has full column rank, so $q_{22}$ is invertible and $c_{02}=0$. Likewise after removing the rightmost $a$ from $E_{21}=0$,

\[
 -c_{20}a^2q_{11}+(c_{20}a q_{01}+c_{21}a q_{11})+c_{22}q_{21}=0.
\]

It follows that $c_{20}=c_{21}=0$ using $q_{11}$ invertible, then $c_{22}$ invertible because row $e_2^T C=(0,0,c_{22})$ is surjective, and finally $q_{21}=0$. Consequently the literal $E_{22}=c_{22}q_{22}$ is invertible and ordinary. If all three heads had positive rank this corner would be a linear combination of nonordinary projective labels. Thus at least one other head has rank zero.

## No second high head

For every other head $k$, $e_j^TO^{-1}O e_k=0$ implies that its first physical output is zero. Write $Oe_k=(0,h,t)^T$. Its inverse-native pullback $L^{-1}(0,h,t)^T=(0,a^{-1}h,t)^T$ has only one inverse Gaussian factor. The subsequent $C^{-1}$ is ordinary and $U^{-1}$ adds at most one more. If $r_k\ge3$, every label of $U^{-1}C^{-1}L^{-1}O e_k F_{r_k}$ then has maximum entry at most $2/\sqrt8<1$. The first input-isolation argument forces $I_{\rm in}^{-1}e_k$ into the same original $e_1$ bank already filled by $I_{\rm in}^{-1}e_j$. Two independent full banks cannot occupy that single $D$-dimensional subspace. This proves the remaining bound. This argument itself does not constrain profiles with maximum at most three.

As a further source check, the forced flags give $E_{12}=a c_{12}q_{22}$ and $E_{20}=c_{22}q_{20}a$. If the actual profile is $(4,2,0)$, class one is absent. Separation and the invertible factors then force $c_{12}=q_{20}=0$, so both physical interstages are block diagonal between active banks and the spectator. A proposed sharp control with a nonzero such transfer is rejected.

## Sharp literal constructor and whole-profile price

Direct noncommutative block multiplication, using the same invertible element $a$ throughout, gives

\[
 L U L=\begin{pmatrix}0&-a^4&0\\a^2&0&0\\0&0&1\end{pmatrix}.
\]

These are all three original inputs with an actual independent quartic, a quadratic and an ordinary job. The physical output ordering is a permutation of labels with a sign on its first bank. Fixed independent public bank labels can also be returned by a signed two-bank swap consisting of three elementary ADDs and two sign SCALEs as counted in the checker. The retained three native normalizations, bodies, idles, original targets and any restoration are charged. No additional Gaussian query, owned bank, nonzero initializer, temporary lifetime or runtime inverse is invoked by this identity.

For $[n]=n^t$, $0<t<1$, the retained three-native invoice is $P=3[1]+6[7]+3[8]$. With 21 shared body axes the sharp target is $[25]+[23]+[21]$. Strict concavity gives $[25]+[21]<2[23]$, while strict subadditivity gives $[1]+2[7]+[8]>[23]$. Thus $P$ exceeds the entire target before any further expenses. The accompanying checker encloses the $t=199/200$ deficit by integer 200th-root comparisons. This is a scoped optimal construction and obstruction. It gives no new κ, complete complex supplier, or discharge of any of the five foundational assumptions. The next all-chart cases with positive optimistic budget have maximum rank three, including $(3,2,2)$ and $(3,3,1)$.

Credit @CubeJerry, authors of the admitted physical lower/upper native, same-plus source and collective separation, and S022 Worker C with OpenAI assistance. Starting programme commit `e31d437b489a416446fdd7e294bc2238829c5925`.
