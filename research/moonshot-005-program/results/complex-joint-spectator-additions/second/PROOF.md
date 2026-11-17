# Injecting one arbitrary active input into the spectator still cannot pay

This result crosses the spectator-preserving condition from the preceding theorem. It treats a real change to the third row of the first interface, not a different choice of endpoint basis. The obstruction uses both output support pairs and the literal rightmost native, across all three input columns.

## Source and conclusion

Use the fixed-prefix, finite collective catalogue and exact S021 matrices $L,C,U,a,P,N,S$ in the companion spectator proof. The centre change is now
$$
K=I+e_{21}(t),\qquad K^{-1}=I-e_{21}(t),
$$
where $t$ is any ordinary coefficient. It may be singular, nonmonomial or noncommuting. The conclusions apply to any physical implementation of this change and also to the larger formal coefficient class. Let $Q,O,I_{\rm in}$ be arbitrary three-bank ordinary units and assume the uniform independent endpoint equation
$$
 LCKUQL=O\,\mathrm{diag}(F_{r_0},F_{r_1},F_{r_2})I_{\rm in}.
$$

**Theorem.** Every head has rank at most three, at least one head has rank at most one, and the profile $(3,3,1)$ is impossible. Thus all admissible profiles have total rank at most six. The case $(3,3,0)$ is not excluded by this theorem. Each head is an independent Gaussian job on a whole bank.

Work at sufficiently large faithful widths divisible by four. Fixed-catalogue separation, full ordinary input/output units and the sixteen-letter source are essential throughout. In this proof a class-$j$ catalogue can be enlarged to include all one-letter unitaries with exactly $2^j$ nonzeros in each column. These larger classes are disjoint and invariant under arbitrary left or right monomials. The span of an arbitrary sum of collective words has unique projection $\pi_j$ onto such a class. It follows from their Gram independence, never from the sparse count of a *sum*.

## Forward expressions and a two-pair criterion

For $O_0=E_{10}(I)E_{21}(-I)$ let $M=O_0^{-1}LCKU$. Write the $j$-th ordinary column of $Q$ as $(p_j,z_j,w_j)^T$. Define
$$
 X_j=P a p_j-Nt a z_j,\qquad U_j=a p_j+St a z_j,\qquad
 Y_j=P_2 z_j,\quad Z_j=N_2 z_j,
$$
where $P_2=a^{-2}Pa^2$, $N_2=I-P_2$ are ordinary. Denote $M Q e_j$ by $D_j$. Multiplication gives
$$
 D_j=(aX_j-a^3Y_j-aNw_j,\;X_j+a^2Z_j-Nw_j,\;U_j+Sw_j)^T. \tag{1}
$$
In particular $X_j,U_j$ are sums of rank-one words, and $PX_j=P a p_j$. The three actual columns of $MQL$ are $D_0a+D_1,D_1a,D_2$. A useful exact row is $P e_1^T M=(Pa,0,0)$.

On a single letter, the source $A=C_bR$ sends each input basis point to a pair differing only in output coordinate $b$. Two input basis points have equal output supports precisely when they differ only in coordinate $c$. Otherwise their supports are disjoint. Consequently:

* Every class-one coefficient of $A g A$ with ordinary monomial $g$ has only $b$-pairs as output supports. Indeed mixing the right $A$ across two *different* supports of the left $A$ gives four nonzeros; when the two supports coincide their surviving pair is a $b$-pair.
* If $V$ is a single unitary word with two nonzeros per column and $A V$ has two per column, every output pair of $V$ must differ in coordinate $c$. The same disjoint-support argument applies column by column.
* The tail permutation of $S$ fixes the $b$-pairs and takes $c$-pairs to $d$-pairs. The $b$-, $c$- and $d$-pair catalogues are disjoint projectively.

Let $B$ be a linear combination of class-one words, also with $aB$ entirely class one. The second property applies to every surviving word separately, since left multiplication by $A$ is one-to-one on projective words. Thus $B$ has only $c$-pair words and $P B$ has only $c$- and $d$-pair words. If $P B$ also has only $b$-pair words, separation gives $P B=0$. Then $B=-SB$; its two sides use disjoint $c$- and $d$-pair catalogues, giving $B=0$. All prefix factors and signs remain in the coefficients of these identities.

## At least one head is low

If all three ranks are at least two, the third entry of $D_2$ lies in classes at least two from the endpoint. Formula (1) puts it in ordinary and rank-one words. Separation gives $w_2=0$ and $U_2=0$. Thus $ap_2=-Staz_2$. The second entry of $D_2$ becomes $a^2 Z_2-taz_2$. Its rank-one part must vanish, so $taz_2=0$, hence $p_2=0$. Since $Q$ is a unit, its column $(0,z_2,0)^T$ has a whole-bank left inverse; $z_2$ is physically invertible. This forces $t=0$ at every such width. At $t=0$, $P e_2^T L C U Q L=(0,0,P)QL$ is a nonzero ordinary/rank-one row incompatible with all heads being high. The argument also handles width-dependent coefficients.

## No quartic for any ordinary injection

An independent quartic output column $(u,v,w)^T$ of the *physical* $O$ satisfies $-u+v+w=0$: the physical probe $(-I,I,I)$ after $LCKU$ equals $(a,Sta,S)$, of degree at most two after right multiplication by $QL$. This cannot contain the quartic isolated by $I_{\rm in}^{-1}e_j$.

The third inverse row in physical banks is
$$
 e_2^T(LCKU)^{-1}=\big((t-N)a^{-1}+t a^{-2},\;-t a^{-1},\;P\big).
$$
Its product with $(u,v,w)^T F_4$ is in the ordinary/rank-one span from $QL I_{\rm in}^{-1}e_j$. Each term on the left has largest entry at most $2/4=1/2$ since it contains at most two inverse Gaussian factors before the flat quartic. Hence separation forces zero. After cancelling $F_4$ and separating the ordinary and rank-one terms, obtain $Pw=0$ and $N a^{-1}u=t a^{-1}(u-v)=t a^{-1}w$.

The orthogonal projector $H$ onto $\ker w$ belongs to the ordinary algebra at every fixed faithful width. Indeed the full tail monomial group on sixteen letters is finite, so the algebra of its collective lifts with fixed prefix matrices is finite dimensional, unital and closed under adjoint. The spectral projector of $w^*w$ at zero is a polynomial in it. Uniformly over widths the entire finite group remains an allowed catalogue, even when polynomial coefficients vary. Since $w=Nw$, $\mathrm{rank}\,H\ge D/2$. Multiplication on the right gives $Na^{-1}uH=0$. As $A\,\mathrm{SWAP}_{cd}\,A^{-1}$ is nonmonomial, the ordinary/nonordinary coset argument of the companion theorem forces $uH=0$. Also $vH=(u-w)H=0$. The high output column therefore has a nonzero kernel, contradicting the whole-bank left inverse. No invertibility of $t$ was used.

## The last candidate $(3,3,1)$ fails on the three input columns

Now all complete matrix entries would contain only classes one and three. For an ordinary monomial catalogue $G$, words in $GAG A$ (spaces between factors indicate multiplication) are projectively disjoint from $A^2G A$: remove the rightmost $A$ and compare the two versus four nonzeros per column. Likewise words in $A G A G A$ are disjoint from both $A^3 G A$ and $A G A$: remove the leftmost and rightmost $A$ and compare two versus four or one nonzeros. These disjointness facts hold for unrestricted ordinary monomials, with arbitrary fixed prefix matrices. They are used only to separate the specified source terms.

**Third input.** $X_2$ has only class-one words. In the first entry of $D_2$, the other terms $-a^3Y_2$ and $-aNw_2$ have allowed classes three and one. Hence $aX_2$ can use only classes one and three; its individual words have at most four nonzeros per column, so only one is possible. Since $PX_2=P a p_2$ has only $b$-pair words, the two-pair criterion forces $X_2=0$. In particular $P a p_2=0$.

**Second input.** In the second entry of $D_1 a$, the words of $X_1 a$ have at most four nonzeros per column, are disjoint from those of $a^2 Z_1 a$, and the remaining $-Nw_1a$ is class one. Thus $X_1 a$ has only class-one words. In the first entry, $aX_1a$ is disjoint from $a^3Y_1a$ and $aNw_1a$. Its words have at most four nonzeros once $X_1a$ is confined to class one, so $aX_1a$ is also class one. The class-one projection of $P a p_1 a$ has only $b$-pair words. Since $P X_1a=P a p_1a$ is itself class one, the criterion gives $X_1a=0$, and $P a p_1=0$.

**First input.** The exact probe $P e_1^T M$ gives $P a p_0a+P a p_1$ on this input. Its words have at most four nonzeros, and the endpoint permits only classes one and three. Subtracting the class-one $P a p_1$ shows $P a p_0a$ is pure class one. Its surviving words therefore have only $b$-pair outputs.

Put $B=\pi_1(X_0a)$. The top entry of $D_0a+D_1$ is
$$
aX_0a-a^3Y_0a-aNw_0a+aX_1-a^3Y_1-aNw_1.
$$
Here $X_1=0$, the last two terms already have allowed classes, and the projective catalogues of $aX_0a$ are disjoint from those of $a^3Y_0a,aNw_0a$. Thus $aX_0a$ has only classes one and three. Left multiplication by $A$ is injective on the distinct word labels of $X_0a$; $aB$, made from its class-one subset, has at most four nonzeros per word and is therefore pure class one. Finally ordinary bimodularity gives $PB=\pi_1(PX_0a)=P a p_0a$. This uses only $b$-pair words, so the criterion forces $B=0$ and $P a p_0=0$.

All three entries of $(P a,0,0)Q$ vanish. The left row is nonzero and $Q$ is invertible. This contradiction proves the theorem.

## Constructive and budget consequences

The companion benchmark implements the escaped source $t=\mathrm{SWAP}_{ac}$ and gives an exact whole input column of the sought $(3,3,1)$ tensor endpoint; its cubic part is nonzero. The obstruction above applies even there. It excludes the actual endpoint completion, rather than treating the single-column construction as a contradiction.

The full optimistic invoice remains $3[1]+6[7]+3[8]$. Every surviving profile is bounded in target value by $[24]+[23]+[22]$. Among profiles of total six, $(3,3,0)$ is dominated by $(3,2,1)$ by concavity. Lower totals cannot give a larger target. The deficit is at least $0.418623272570444221776297370875\ldots$ at $t_{\rm price}=199/200$; the same strict all-$0<t_{\rm price}<1$ argument applies. In the theorem $t$ denotes a map and $t_{\rm price}$ the price exponent. All ordinary source changes, full source/target normalizers, compiler, precision, ownership, erasure, and recursive calls remain additional.

A viable changed first interface must leave both the earlier spectator-preserving family and this single second-input shear family, or use another core arrangement. The proof relies on the exact linear forms in (1); arbitrary joint changes of the two active inputs are open. No new complete κ or foundational discharge.

Credit @CubeJerry, S021 paid-source authors, and S022 Worker C with OpenAI assistance.
