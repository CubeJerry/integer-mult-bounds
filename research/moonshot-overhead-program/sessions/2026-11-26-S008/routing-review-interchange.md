# Independent review of the 156 width potential and the unit coefficient

The [complete binary interchange](compiler-full-interchange.md) passes this review, conditional on its linked native clock, child-volume and adapter suppliers. I used the existing all-call estimate (4) of [child-volume.md](child-volume.md), which already includes the full-volume reserves; I independently reviewed its literal ceilings and actual caller volume [previously](routing-review-child.md).

With $s=\log_2m$, $l=\log_2(s+2)$ and $z=d(l/s)^{1/3}$, the same dyadic $d$ controls both positive summands. Since $v\le l+3/2$, $l/v\ge34/37>(31/32)^3$. The maximality of $d$ gives $31/64\le z\le33/32$. The derivative of $3/z+(20/17)z^2$ is negative even at the upper endpoint, because $(40/17)(33/32)^3<3$. Consequently $33/4096+3/(31/64)+(20/17)(31/64)^2=13982555/2158592<13/2$ bounds the complete logarithmic charge divided by $\Phi(s)$.

Let $y=\log_2e$, $R=4096$, $L=\log_2(y+2)$, $r=Rs/y$ and $\xi=l/L$. Odd-root rounding gives $r\ge1-R/y$, and $1-\xi\ge11/L$. The excess in the proposed parent exponent beyond $(13/2)\Phi(s)$ is at least $(13/2)R^{-2/3}\Phi(y)(r-r^{2/3}\xi^{1/3})$. Concavity of the cube root bounds the final bracket below by $(1-\xi)/3-R/y$. As $y\ge RL$, the difference is at least $(52/3)(y/(RL))^{2/3}>2$. The parameter in front of $\Phi(y)$ is exactly $(3/2)(13/2)4096^{1/3}=156$. Direct widths extend through $y<536879104$, which is below $24(312)^3$ and includes a separately immediate portion $y\le2^{24}$. This pays the $256(e+1)V$ fallback. The marker-preserving range adapter contributes $512V$ time and $128V$ cells and increases the encoded input by less than nine, yielding $A_I=5120$ and total space coefficient $2359424$.

For the separate fixed-exponent certificate, $s\ge17d^3-1\ge4096d$ on $d\ge16$. Thus $d(q+2)\le3s+(20/17)(s+1)+35d\le17s/4$. Each breakpoint $Y_j$ gives $d\ge2^j$: when $v>3j+6$ the worst first value is $v=3j+7\le46$, and $64\cdot2^{3j}-2\ge v 2^{3j}$ there. This spacing increases under subsequent doubling. The left segment of any crossing child lies on a slope at least the current slope, since they decrease. Summing these rational slopes anew gives

$$
Y_{13}=101330991615844352,\quad H(Y_{13})=121106649321472,
\quad
\frac{H(Y_{13})-(17/32768)Y_{13}+13}{1/1000-17/32768}
=\frac{93574826145711104000}{657}.
$$

The independently computed ceiling is $142427437055876871$, below $2^{57}$. The [finite checker](compiler-interchange-check.py) also passed 1174 rounded parameter probes and 3400 concavity probes. This review establishes the stated field-width and prefactor transfers at their written level. Prepared for Jerry Chen (@CubeJerry) with ChatGPT research assistance.
