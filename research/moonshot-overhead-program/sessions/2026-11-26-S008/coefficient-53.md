# An explicit input threshold for coefficient 53

Set \(t=\log_2\log_2 n,\ \ell=\log_2 n,\ \Phi(t)=(t^2\log_2(t+2))^{1/3}\). The fixed multiplier of [the all-length construction](all-lengths.md) satisfies
\[
  \boxed{\quad t\ge2^{69110}\quad\Longrightarrow\quad
      2T(n)\le n\sqrt{\ell}\,2^{53\Phi(t)}.\quad}
\]
Every positive length satisfies the same \(2^{32}n\) visited-cell cap. The input length scale is very large. The [specialized \(0.501\) certificate](routing-refined-walsh.md) applies much earlier. This comparison prices the existing rule with the actual label-bit count; it requires no further change of machine.

Use \(R=240,\ D=2^j,\ Q_j=3j+\lceil\log_2(3j+3)\rceil+2,\ S_j=240(Q_jD^3+2)\). The [true label-width invoice](address-refined-label.md) uses the continuous concave \(H_*\) for all native calls. In the band \(y=240(Q_jD^3\tau+2)\), \(1\le\tau\le U_j=8Q_{j+1}/Q_j\), the derivative of \(H_*\) is \((3+E_j/\tau)/D\), where \(E_j=(j+\log_2(8Q_{j+1}+1)+3)/Q_j\). The derivative is a proof allowance. The actual tape program reads the true label width and pays the previously counted elementary operations.

## A uniform bound after a finite band

Take \(J=11500\). For \(j\ge J\) we have \(3j\le Q_j\le Q_{j+1}\le4j\) and \(Q_{j+1}-Q_j\le4\). Indeed \(3j+6\le2^{j-5}\) at \(j=16\) and that inequality persists by doubling; the ceiling-log increment is at most one. At \(J\), \(J+2<2^{14}\) and \(500(14+9)=11500\). The logarithmic density \(\log_2(j+2)/j\) decreases thereafter, as does \(9/j\). Thus \(\log_2 j+9\le j/500\) for \(j\ge J\). Using \(8Q_{j+1}+1\le64j\), we obtain
\[
 E_j\le167/500=:E,\qquad 8\le U_j\le 8+32/(3J)<8001/1000=:U,
 \qquad \ln U<21/10 .
\]
The last inequality follows already from the first eight terms of the exponential series at \(21/10\).

Let \(b_j=H_*(S_j)/(240D^2 Q_j)\), and \(r_j=Q_j/(4Q_{j+1})\le1/4\). The exact integrated recurrence simplifies to
\[
    b_{j+1}=6+r_j\big(b_j-3+E_j\ln U_j\big)
\]
since \(3r_jU_j=6\). Over all \(j\ge5\), the earlier \(E_j<2,\ U_j\le16\) give \(b_j\le20\): \(H_*(y)\le y/2\) implies \(b_5<17\), and \(6+\max(0,b_j+8)/4\le13\) when \(b_j\le20\).

For \(j\ge J\), put \(B=36169/5000=7+E(21/10)/3\). If the recurrence's parenthesis is negative, \(b_{j+1}\le6\); otherwise it is at most \(6+(b_j-3+E(21/10))/4\). Therefore \((b_{j+1}-B)_+\le(b_j-B)_+/4\). For \(j_0=11510\) and every later band,
\[
 b_j\le B+20/4^{10}<M,\qquad M=1447/200 .
\]
At every real point of such a band, \(\log_2(y+2)\ge Q_j\). Consequently
\[
 \frac{H_*(y)}{\Phi(y)}
 \le 240^{1/3}\frac{M+3(\tau-1)+E\ln\tau}{\tau^{2/3}}.
\]
The derivative of the last quotient has the sign of
\(\tau+E+2-2M/3-(2E/3)\ln\tau\). This expression increases on \([1,U_j]\), so the maximum of the quotient is at one of its endpoints. The first gives \(M\). At the other endpoint use \(U_j^{2/3}\ge4\) and \(4M-[M+3(U-1)+E(21/10)]=3/5000>0\). Hence \(H_*(y)\le44.97\Phi(y)\) for all \(y\ge v_0=S_{11510}\), by \(240M^3<(4497/100)^3\).

## The Walsh history and the outer charges

The physical Walsh choice is \(Y(v)=\lceil(v^2\lceil\log_2(v+2)\rceil)^{1/3}\rceil\). Above \(v_0\), both \(\log_2(v+2)\) and \(\Phi(v)\) exceed 4096. Bounding the two upward rounding errors separately gives
\[
  Y(v)\le(1+1/4096)^{1/3}\Phi(v)+1\le(1001/1000)\Phi(v).
\]
Write \(P=\Phi\). The nondecreasing historical surplus over \(48P(x)\) is the supremum of \((H_*(v)+8Y(v)-48P(v))_+\) for \(0\le v\le x\), from the [true-slot proof](address-refined-label.md). At \(v\ge v_0\) this is bounded by \((52.978-48)P(x)\). At earlier \(v\), \(H_*(v)\le v/2\) and \(Y(v)\le v+3\) because \(\lceil\log_2(v+2)\rceil\le v+2\) for real \(v\ge0\). Thus all earlier surplus is at most \(10(v_0+3)\). If \(x\ge(4v_0)^2\), then \(P(x)\ge\sqrt{x}\ge4v_0\) and \(v_0\ge4\); this pays the same history cap. We have shown \(G_*(x)\le52.978P(x)\) for every such \(x\), including every future arity change.

At \(j_0=11510\) the exact \(Q_{j_0}=34548\) gives \(960(Q_{j_0}+2)<2^{25}\), so \((4v_0)^2<2^{2(3j_0+25)}=2^{69110}\). On the claimed range the full time excess above \(n\sqrt{\ell}\), in binary logarithmic units, is at most \(182+4\log_2(t+2)+52.978P(t+2)\). For \(t\ge2^{30}\), \(4096\log_2(t+2)\le t\) by the one-endpoint bound with \(j=31\); cubing gives \(4\log_2(t+2)\le P(t)/64\). We also have \(P(t)\ge2^{20}\) and \(P(t+2)\le P(t)+2\). Now \(53-52.978-1/64>0.006\), and \(0.006\cdot2^{20}>182+2(52.978)+1\). This pays all outer charges and leaves the stated extra bit. [Exact arithmetic](coefficient-53.py) · [Component theorem](coefficient-53.lean)

The sharper true-label envelope has limiting upper coefficient \(8+\sqrt[3]{240}(7+\ln(2)/3)=52.93710138\ldots\). The finite gate here establishes a numerical onset for coefficient 53. The factor \(\Phi\) persists.
