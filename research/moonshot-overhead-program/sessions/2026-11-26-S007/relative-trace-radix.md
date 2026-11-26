# A complete change to relative-trace digits

Let $a=2^c$, $b=3c$, $h=a^2$, $q=a^3$, and work over the binary field. Set
$$
U(X)=X^a+X,\qquad T(X)=X^h+U(X),\qquad S(X)=T(X)^2+T(X).
$$
A fixed number of ordinary one-head tapes converts arbitrary contiguous binary coefficients of $f$ to all $a$ ordered degree-$<h$ digits $D_i$ in $f=\sum_{i<a}D_i(X)T(X)^i$, and conversely. The machine visits $O(q)$ cells and takes $O(qb/(1+\log_2(b+2))^{1/4})$ steps. Any fixed rational $0<\eta<1/2$ can replace $1/4$, for its own fixed machine. Two wide-record upper Pascal transforms account for the superlinear work. [Tape implementation](striped-pascal.md)

The S006 prefix produces $2^r$ ordinary polynomials in increasing block order. Its paid inverse returns $q$ ordered coefficients in $O(q\sqrt b)$ steps. Apply the construction below. On return, the paid S006 forward prefix restores the original blocks. This bypasses the remaining trace-squared divisions and uses an alternative downstream layout. Each $k<h$ supplies a length-$a$ binary polynomial to the smaller full CRT at degree $c$, for total raw child volume $ha=q$.

## Two ordered shears

Pack the ordinary polynomial as $P(X,Z)=\sum_{j<a}p_j(X)Z^j$ with $\deg p_j<h$, so $f=P(X,X^h)$. A row is ordered by increasing $X$-exponent $k$. For slope $e\in\{1,a\}$, substitution $Z\mapsto Z+X^e$ sends the bit at $(j,k)$ to $(i,k+e(j-i))$ exactly when $i$ is a bitwise subset of $j$. Indeed $(Z+X^e)^j$ factors over the set bits $u$ of $j$ into $Z^{2^u}+X^{e2^u}$. Independent source contributions add by XOR.

Pad each row to $N=2h$ bits. Rotate row $j$ so that column $k$ moves to $\lambda=k+ej\pmod N$. Apply the upper Boolean zeta (Pascal) transform on $j$ at every fixed $\lambda$, then rotate output row $i$ by $-ei$. This implements substitution modulo $X^N-1$. After either shear and after both, the true $X$-degree is at most $h-1+a(a-1)=2h-a-1$. Each shift spends part of the original $Z$-degree, with largest slope $a$. Consequently no actual output wraps. The composed substitution is $Z\mapsto Z+U(X)$.

To rotate a row, spool the two intervals at its wrap point and concatenate them in the opposite order. Rewind both scratch heads between rows. Its cut uses $O(b)$ bits, with polynomial setup per row and amortized constant-cost ripple counters over a complete scan. Each of $a$ rows has length $2h$, so rotations, setup, returns and padding together cost $O(q)$. The two Pascal calls reuse scratch banks.

## One bounded carry

Write each sheared row $A_j(X)+X^h B_j(X)$ with $\deg A_j<h$ and $\deg B_j<h-a$. The final $B_{a-1}=0$ because the top coefficient in $Z$ is unchanged. For the forward direction evaluate at $Z=T$, where $T+U=X^h$. Replacing $X^h$ by $T+U$ gives the actual digit, taking $B_{-1}=0$,
$$
D_j=A_j+U B_j+B_{j-1}.
$$
Each term has degree below $h$. Monicity and distinct leading degrees $hj+k$ prove uniqueness. In reverse, begin with arbitrary $D_j$, apply the same two shears, and evaluate at $Z=X^h$. The ordinary block is $A_j+B_{j-1}$. The two formulas represent the same polynomial in their respective bases, which proves both inverse compositions. Two fixed shifts of the current high half, one saved previous high half and one output bank suffice. All heads scan and return within $O(h)$ per row. Every stage reuses $O(q)$ marked cells including input and output.

## Converse on wide independent arrays

A fast canonical $T$ synthesis also implements upper Pascal on $2^u$ rows with $2^{2u}$ independent lanes at constant volume overhead. Choose the least odd $c\ge u+3$, so $a/8\ge2^u$, $a^3\le2^{12}2^{3u}$. Work over $\mathbf F_4$ with $\omega^2+\omega+1=0$, by using binary synthesis on each of two basis components. Define $D_{x,z}P(X,Z)=P(\omega^xX,\omega^zZ)$. With $C_H$ denoting $Z\mapsto Z+H(X)$,
$$
D_{x,z}^{-1} C_U D_{x,z}=C_{\omega^z U(\omega^{-x}X)} .
$$
Since $a=2^c\equiv2\pmod3$, the choices $(x,z)=(0,1),(1,1+a)$ give equal $X^a$ coefficients $\omega$, and $X$ coefficients $\omega,\omega^a$ that sum to $1$. Composing implements $C_X$.

Place the bit in row $j<2^u$, lane $\ell<2^{2u}$ at column $a+\ell-j$ of row $j$, with zeros elsewhere. Its index is nonnegative. After either or both conjugated shears its column is at most $a+2^{2u}-1+a(2^u-1)<a^2$. Thus every literal synthesis unpacks into the ordinary $h$-bit rows of the bivariate shear without carry. All rows beyond $2^u$ remain zero. Column $a+\ell-i$ of final row $i$ is the desired Pascal sum. Scalings use a fixed table on $j,k\bmod3$ and two binary components. Four binary syntheses and $O(q)$ other tape steps suffice. The padding here belongs to the converse reduction. The forward integer caller still rounds to $3\mid b$ with its original at-most-fourfold increase.

The [checker](verify-trace-shears.py) compares ordinary monic long division, unrestricted Horner synthesis, and direct subset sums. It checks independent input digits and every binary basis column at smaller degrees. [Finite receipt](trace-shears-receipt.json) Coxon studies basis changes for additive FFTs. The construction here uses the two separated monomials below the leading relative-trace term and prices movement in both directions. [Coxon, J. Symbolic Computation 104 (2021)](https://doi.org/10.1016/j.jsc.2020.10.002)
