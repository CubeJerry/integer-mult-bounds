# A two-sided spectator constraint rules out every profitable same-plus head profile

For the S021 three-native complex source, every ordinary change at the first interface that preserves the active two-bank input subspace has total independent head rank at most six. Its best possible movement invoice already misses the target. This covers arbitrary output and input bases. The S021 source and its third-input shears satisfy the stronger ceiling five.

## Model and theorem

Let one tail letter have dimension 16. Retain the paid S021 normalization $a=I_{\rm pre}\otimes A^{\otimes W}$, where $A=C_b R$, $R(a,b,c,d)=(b,c,d,a)$ with input sign $(-1)^{abd}$ and $C_b=((1+i)I+(1-i)X_b)/2$. Put $s=\mathrm{SWAP}_{cd}$, $S=Z_\sigma\otimes s^{\otimes W}$, $P=(I+S)/2$, $N=I-P$. The genuinely fixed sign bit makes $P,N$ each have half the whole-bank dimension $D$.

Ordinary coefficients use a fixed finite catalogue of collective root-four tail monomials, with arbitrary matrices on a fixed prefix. Exterior coefficients may depend on width. An ordinary unit must have an ordinary inverse. Every endpoint head $F_r$ is an independent invertible Gaussian word, with $2^r$ nonzeros of modulus $2^{-r/2}$ per tail row/column, up to separate ordinary boundary gauges. The argument only needs these support and modulus properties. All widths are positive, all three input banks are arbitrary, and any uniform conclusion must hold at arbitrarily large widths divisible by four.

Retain
$$
L=\begin{pmatrix}a&0&0\\I&a&0\\0&0&I\end{pmatrix},\qquad
U=\begin{pmatrix}a&-a^2&0\\0&a&0\\0&0&I\end{pmatrix},\qquad
C=\begin{pmatrix}P&0&-N\\P&I&-N\\N&0&P\end{pmatrix}.
$$

The changed first interface is $C'=CK$, with
$$
K=\begin{pmatrix} B & g\\0&k\end{pmatrix},
$$
where $B$ is any ordinary two-bank unit, $g$ any ordinary two-entry column, and $k$ any ordinary one-bank unit. This class includes every ordinary change that preserves the entire active input subspace and has this block-unit inverse. Its full algebra may be used to prove a necessary condition without asserting a physical compiler for all such coefficients.

**Theorem.** Suppose $LCKUQL=O\,\mathrm{diag}(F_{r_0},F_{r_1},F_{r_2})I_{\rm in}$, where $Q,O,I_{\rm in}$ are arbitrary actual ordinary three-bank units.

1. At least one $r_j\le1$. Every $r_j\le3$, and at most one $r_j$ is three. Ordered nonincreasingly, the profile is componentwise bounded by $(3,2,1)$.
2. If $B=\left(\begin{smallmatrix}d&e\\0&d_1\end{smallmatrix}\right)$ with $ad_1=da$, every $r_j\le2$, and the ordered profile is bounded by $(2,2,1)$. This includes the base source and every S021 third-input shear, as well as arbitrary second-column shears $e$ and transported changes of chart.

## Source identities in physical banks

The literal inverse and the third forward row of the first unit are
$$
C^{-1}=\begin{pmatrix}P&0&N\\-I&I&0\\-N&0&P\end{pmatrix},\qquad
e_2^TLC=(N,0,P).
$$
Write $M=LCKU$ for the portion before $QL$. As $P N=0$, $e_2^T U=e_2^T$ and $e_2^T K=(0,0,k)$,
$$
P e_2^T M=(0,0,Pk). \tag{1}
$$
As $e_2^T U^{-1}=e_2^T$ and $e_2^T K^{-1}=(0,0,k^{-1})$, the inverse gives
$$
e_2^T M^{-1}=k^{-1}(-N a^{-1},0,P). \tag{2}
$$
The two identities hold for every $B,g,k$ in the theorem, including a nonzero lower-left block in $B$. Inverse natives are used only in the argument. No free runtime inverse is counted.

## Fixed-catalogue separation

For finitely many projectively distinct one-letter unitaries $G_j$, the off-diagonal entries of their normalized Hilbert–Schmidt Gram matrix at width $W$ have moduli $(|\operatorname{tr}(G_i^*G_j)|/16)^W\to0$. Thus the Gram matrix is invertible for all sufficiently large widths. Projectively identical words are grouped with their actual scalar. Fixed prefix matrix units preserve independence, including for width-dependent exterior coefficients. Disjoint projective catalogues then span disjoint spaces.

Write $\mathcal F_1$ for the span of words with at most one Gaussian rank-one factor and ordinary monomial factors. Its generators have largest entry $1$ or $1/\sqrt2$ and at most two nonzeros per row. Left and right ordinary multiplication preserve $\mathcal F_1$.

## A low head and the high-head output space

Equation (1) gives $P e_2^T M QL=(0,0,Pk) QL$, a nonzero row in $\mathcal F_1$ since $P\ne0$ and both $k,QL$ are invertible. If all heads had rank at least two, the endpoint expression for the same row would contain only translates of heads with at least four nonzeros per row. Separation would make that row zero. Hence at least one head has rank at most one.

Isolate separately any head $F_r$, $r\ge3$, by the ordinary input column $I_{\rm in}^{-1}e_j$. Write its physical output column from $O$ as $(u,v,w)^T$. Then $MQLI_{\rm in}^{-1}e_j=(u,v,w)^T F_r$. The third inverse row (2), multiplication by $k$, and the complementary ordinary left projections $N,P$ imply
$$
Na^{-1}u F_r\in\mathcal F_1,\qquad P w F_r\in\mathcal F_1.
$$
The one-letter terms of the first expression have largest entry at most $\sqrt2\,2^{-r/2}\le1/2$. A row of $A^{-1}$ has two entries of modulus $1/\sqrt2$, both surrounding tail monomials preserve absolute values up to permutation, and $F_r$ is flat on its support. The second bound is $2^{-r/2}\le1/\sqrt8$. Both catalogues are disjoint from generators of $\mathcal F_1$ even if cancellations occur among their own words. Separation, then right cancellation of the invertible $F_r$, gives $N a^{-1}u=0$ and $P w=0$.

The first equality implies $u=(a S a^{-1})u$. Here $q=A s A^{-1}$ has four nonzero entries per row. The projective monomial group $G$ and its coset $qG$ are disjoint, forcing the ordinary coefficient $u=0$. This uses the finite catalogue; the physical involution $q$ has a nonzero plus eigenspace.

Consequently each high-head output lies in
$$
\{(0,v,w):w=Nw\},
$$
a common space of dimension $3D/2$. Two independent such heads would have joint output rank $2D$ under $O$, a contradiction.

## A quartic cannot reach that high-output space

The first physical bank of any high-head output is zero. The literal native inverses are
$$
 L^{-1}=\begin{pmatrix}a^{-1}&0&0\\-a^{-2}&a^{-1}&0\\0&0&I\end{pmatrix},
 \qquad
 U^{-1}=\begin{pmatrix}a^{-1}&I&0\\0&a^{-1}&0\\0&0&I\end{pmatrix}.
$$
Thus $L^{-1}(0,v,w)^T=(0,a^{-1}v,w)^T$ uses at most one inverse Gaussian factor per word. The central $K^{-1}C^{-1}$ is ordinary, and $U^{-1}$ adds at most one more inverse Gaussian. If $r=4$, every term of $M^{-1}(0,v,w)^T F_4$ therefore has largest entry at most $(\sqrt2)^2/4=1/2$. The exact word equals $QLI_{\rm in}^{-1}e_j\in\mathcal F_1$. Separation forces the whole column to vanish, contradicting invertibility of $QLI_{\rm in}^{-1}$. This proves the first conclusion.

For the transported upper-triangular subfamily use the additional physical probe $b=(-I,I,I)$. The exact identity $bLC=(I,a,S)$ yields
$$
 bM=(d a,\;-d a^2+e a+a d_1 a,\;g_0+a g_1+Sk).
$$
When $ad_1=da$ the middle entry is $ea$, so the row has degree at most two after $QL$. A cubic head has eight entries per row, disjoint from the at-most-four of any such coefficient. For its isolated column this gives $-u+v+w=0$. Already $u=0$ and $w=Nw$, so the high-head output is $(0,-w,w)^T$, of rank at most $D/2$. This excludes the cubic and proves the second conclusion.

## Physical cost, control and next obligation

Use $[m]=m^t$, $0<t<1$. The prior common-body invoice pays $3[1]+6[7]+3[8]$ in all cases. Each output receives 21 body axes. The first class of sources has target value at most $[24]+[23]+[22]$; the transported subclass has at most $2[23]+[22]$. Both are below the price because strict subadditivity gives $1+2\cdot7^t+8^t>23^t$ and concavity gives $[24]+[22]\le2[23]$. At $t=199/200$ the two corresponding source-minus-target deficits are respectively $0.418623272570444221776297370875\ldots$ and $1.398040877411441465757688701150\ldots$. Every ordinary pass, prefix normalization, original target restoration, compiler, precision, ownership/erasure and recursive expense remains additional.

The companion construction gives an actual source with every input in classes 1, 2 and 4 and a full invertible quartic corner. The theorem excludes an independent quartic despite that positive identity. To escape this result within the same-plus word, the first interface must change the spectator row of $K$ away from $(0,0,k)$ or change the native arrangement or model. Simply recharting or arbitrarily mixing the active two-bank subspace cannot pay for the needed profile. No new κ or foundational discharge.

Credit @CubeJerry, the S021 paid-prefix and same-plus predecessor authors, and S022 Worker C with OpenAI assistance.
