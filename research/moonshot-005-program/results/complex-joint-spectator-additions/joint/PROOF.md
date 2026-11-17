# Both active banks may feed the spectator without producing a profitable independent endpoint

Use the S021 same-plus source $L,C,U,a,S,P,N$, ordinary fixed-prefix finite-tail coefficient algebra and faithful collective widths of the preceding two source packages. Change the first interface by
$$
 J=I+e_{20}(t_0)+e_{21}(t_1).
$$
Both $t_0,t_1$ are arbitrary ordinary coefficients. Neither need commute, be invertible, or have a restricted prefix action. The inverse is $I-e_{20}(t_0)-e_{21}(t_1)$. All endpoint and interstage units may vary independently with the admitted finite catalogue. Claims of physical attainability are made only for the explicit benchmark below.

**Theorem.** If $LCJUQL=O\,\mathrm{diag}(F_{r_0},F_{r_1},F_{r_2})I_{\rm in}$ is an independent whole-bank Gaussian endpoint, then every $r_j\le3$, at least one $r_j\le1$, and $(3,3,1)$ is impossible. Hence $r_0+r_1+r_2\le6$. This strictly extends the one-edge theorem. Source changes including a separately changed active-to-active block remain open.

## The actual four source rows

Write $M=O_0^{-1}LCJU$ in the old S021 output gauge, and $(p_j,z_j,w_j)^T=Qe_j$. Define
$$
 J_0=P-Nt_0,\quad H=N(I+t_0),\qquad
 X_j=P a p_j-N(t_0a p_j+t_1 a z_j),\quad
 U_j=a p_j+S(t_0 a p_j+t_1 a z_j).
$$
The entire $D_j=M Qe_j$ is
$$
 \left(aX_j-aJ_0a^2z_j-aNw_j,\quad
 X_j+Ha^2 z_j-Nw_j,\quad
 U_j-St_0 a^2 z_j+S w_j\right)^T. \tag{1}
$$
The actual source columns are $D_0a+D_1,D_1a,D_2$. Both $X_j,U_j$ use only rank-one tail words and $P X_j=P a p_j$. In particular the additional exact probe is
$$
 P e_1^T M=(P a,0,0). \tag{2}
$$
In the physical output basis, the third inverse row is
$$
 e_2^T(LCJU)^{-1}
 =
 \big((t_1-t_0P-N)a^{-1}+t_1 a^{-2},\
       -t_1 a^{-1},\ P-t_0N\big). \tag{3}
$$
This follows directly from $e_2^TU^{-1}=e_2^T$ and $e_2^T J^{-1}=(-t_0,-t_1,I)$. No inverse native is priced as a free physical operation.

## A quartic cannot survive both directions

The last two rows of (1) have degree at most two before the final $QL$, hence at most three after it. Isolating a supposed quartic with $I_{\rm in}^{-1}e_j$ makes those two rows zero by their support bound. Its isolated *physical* output column must be $O_0(o,0,0)^T=(o,o,0)^T$ with $o$ an invertible ordinary bank matrix, since a unit gives this whole column a left inverse.

The result of (3) on this column, including the Gaussian head, is
$$
 \big[t_1a^{-2}-(t_0P+N)a^{-1}\big]o F_4.
$$
It must belong to the span $\mathcal F_1$ of ordinary/rank-one words because it equals a row of $QL I_{\rm in}^{-1}e_j$. Every one-letter term on the displayed side has largest entry at most $2/4=1/2$, whereas generators of $\mathcal F_1$ have largest entry $1$ or $1/\sqrt2$. By the fixed-catalogue Gram argument the two spans are disjoint at large faithful widths. Cancel $oF_4$ from the resulting zero operator. The rank-two words $t_1a^{-2}$ and rank-one words $(t_0P+N)a^{-1}$ are themselves disjoint, so $t_0 P+N=0$. Its restriction to $\operatorname{im}N$ is the identity, a contradiction. This argument handles repeated quartic heads through individual input isolation.

## An all-high profile would erase a complete row of $Q$

Suppose every $r_j\ge2$. In $D_2$, its last two entries have distinct ordinary, rank-one and rank-two pieces. Their ordinary and rank-one parts give $w_2=0$, $U_2=0$ and $X_2=0$. For any $y,v$, simultaneous equations $P y-Nv=0$ and $y+Sv=0$ imply $y=v=0$ by first using $P,N$ on the equality of their opposite ranges. Here take $y=a p_2$ and $v=t_0a p_2+t_1a z_2$. Hence $p_2=0$ and $t_1a z_2=0$. Invertibility of $Q$ makes $z_2$ invertible, so $t_1=0$ at every tested width.

Write $G$ for the full projective ordinary tail monomial group. No coefficient in the endpoint lies in $G a$, since this right-translate catalogue contains only two-support words. Projection onto $G a$ commutes with ordinary left multiplication. In the third entry of $D_1a$, the only contribution in $G a$ is $S w_1 a$. Indeed stripping the rightmost $a$ from the other words leaves rank one or two, rather than an ordinary label. Thus $w_1=0$.

Finally project the last two entries of $D_0a+D_1$ onto $G a$. Put $R=\operatorname{pr}_{G a}(a p_1)a^{-1}$, an ordinary coefficient. Since now $t_1=0$, those two projected equations, after right-cancelling $a$, are
$$
 P R-N(t_0 R+w_0)=0,\qquad R+S(t_0 R+w_0)=0.
$$
The terms in $D_0a$ with one or two Gaussian factors before the last $a$ have zero projection; the $a^2 z_1$ terms in $D_1$ have four-support words, also outside $G a$. The same two-projector argument forces $R=0$ and $w_0=0$. The complete third row of $Q$ would be zero. This excludes all profiles with minimum rank at least two.

## The two-cubic, one-linear possibility

For completeness use the pair criterion from the one-edge theorem. A projectively pure class-one sum $B$ with $aB$ also entirely class one has only one-letter words whose output pairs differ in coordinate $c$: the two input columns of $A$ overlap exactly for such pairs. The tail permutation of $S$ sends those pairs to $d$-pairs. Every class-one word of $A g A$ has output $b$-pairs, and $S$ preserves those. Consequently if $PB$ uses only $b$-pair words, then $PB=0$ by disjoint catalogues, and $B=-SB$ also forces $B=0$. Only individual tensor-word labels are projected.

Assume all source entries can contain classes one and three only. In $D_2$ the terms of $a X_2$ are disjoint from those of $a J_0 a^2 z_2$ and $aNw_2$: remove the left $a$ and compare two, four and one nonzeros per column. Since $X_2$ is pure class one, $aX_2$ has at most four entries per column and is therefore pure class one. Now $P X_2=P a p_2$ has only $b$-pairs, so the criterion gives $X_2=0$.

In the middle entry of $D_1 a$, the words of $X_1 a$ are disjoint from $H a^2 z_1 a$: remove the rightmost $a$ and compare two versus four entries. The remaining $-Nw_1a$ is class one. Hence $X_1a$ is pure class one (its words have at most four entries). The first entry of $D_1a$ gives the same for $a X_1a$: remove the outer $a$'s to separate it from the middle words with four or one entries. Since $P X_1a=\pi_1(P a p_1a)$ has only $b$-pair words, the criterion yields $X_1=0$.

The probe (2) on the first actual input shows $P a p_0a$ is pure class one, since the other term $P a p_1$ is class one and $P a p_0 a$ has at most four entries per word. Let $B=\pi_1(X_0a)$. The first entry of $D_0a+D_1$ reads
$$
 a X_0 a-aJ_0a^2z_0a-aNw_0a+aX_1-aJ_0a^2z_1-aNw_1.
$$
Here $X_1=0$ and $aNw_1$ is class one. The words of $aX_0a$ are disjoint from $a J_0a^2 z_0a$ and $aNw_0a$ by removing the outer $a$'s. The new comparison to $a J_0a^2z_1$ is crucial: after removing the left $a$, each word of $B$ has two entries per column whereas each word of $J_0a^2z_1$ has four. Distinct words of $X_0a$ stay distinct after left multiplication by $a$. Consequently $aB$ has only allowed classes and has degree at most two relative to $a$ and the class-one $B$; it is pure class one. Finally $P B=\pi_1(P X_0a)=P a p_0a$ has only $b$-pair words. Thus $B=0$ and $P a p_0=0$. Already $P a p_1=P a p_2=0$ by the other two columns, so $(Pa,0,0)Q=0$, contradicting invertibility.

These three deductions exclude every profile of sum at least seven; $(3,3,0)$ is allowed by the bound. In the inherited whole-body invoice, concavity gives target value at most $[24]+[23]+[22]$, strictly below $3[1]+6[7]+3[8]$ for all $0<t_{\rm price}<1$, with deficit at least $0.418623272570444221776297370875\ldots$ at $199/200$. The construction below attains a meaningful column of the nominally profitable $(3,2,2)$ interface, but the whole caller cannot be completed in this family. All additional physical expenses and all five foundations remain. No new κ.

Credit @CubeJerry, the retained S021 same-plus and paid-source authors, and S022 Worker C with OpenAI assistance.
