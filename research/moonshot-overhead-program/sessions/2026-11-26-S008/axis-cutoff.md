# The short-axis window at smaller numerical lengths

Put \(t=\log_2 k\). The same odd-coprime descending search in the [elementary axis certificate](../../contributions/explicit-overhead/coprime-axes.md) succeeds for every \(t\ge2^{31}\). The window, width, candidates and physical algorithm stay identical.

Partition primes into \((\sqrt u,u]\) starting at \(u=z=k^{6/5}\). Stop when the lower endpoint would be below \(2^{15}\). The residual primes are at most \(2^{30}\). For each large band the original shell estimate gives \(\sum1/p\le2\ln2+3/a<8/5\), now with \(a=\lfloor\log_2\sqrt u\rfloor\ge15\). Indeed \(\ln2<25/36\), since the exponential series there through degree four exceeds 2 by \(43441/40310784\). For a large-band prime, \(-\ln(1-1/p)\le(32768/32767)/p\). The independent survival probability exceeds \(1/5\), since \((8/5)(32768/32767)<1601/1000<\ln5\). For the last comparison integrate \(2/(1-z^2)\) from 0 to \(2/3\). The first five nonnegative terms give \(2\sum_{j=0}^4(2/3)^{2j+1}/(2j+1)>1601/1000\), and the full integral is \(\ln5\).

Keep the same even truncation depths \(4+2j\). The relative Bonferroni error is at most
\[
 5\sum_{j\ge0}\frac{(8/5)^{5+2j}}{(5+2j)!}
 \le \frac{5(8/5)^5}{120(1-(8/5)^2/42)}
 =\frac{28672}{61625}<\tfrac12 .
\]
Residual survival is at least \(2^{-30}\), so the conservative main density \(2^{-65}(2t)^{-3}\) remains valid. The upper product of monomial indices is still \(D_0 z^{14}\).

Each prime in \((2^{j-1},2^j]\) divides \({2^j\choose2^{j-1}}<2^{2^j}\). The product \(D_0\) of residual primes satisfies \(\log_2D_0<\sum_{j=1}^{30}2^j<2^{31}\). With \(Y=\lfloor 2^{20\lceil\log_2 k\rceil}/k^2\rfloor\ge k^{18}/2\), the original argument bounds its three errors divided by \(Y\), including primes above \(z\) dividing the previously chosen product, by
\[
 4t D_0\,2^{-6t/5},\qquad 2\,2^{-t/5},\qquad4\,2^{-17t}.
\]
At \(t\ge2^{31}\), the first is at most \(4t2^{-t/5}\). Each term is below \(2^{-70}t^{-3}\), a quarter of \(2^{-65}(2t)^{-3}\), since \(t/5>72+4\log_2t\) at \(2^{31}\) and beyond by monotonicity. A surviving coprime exists for every \(A\le2^{k+1}\) in the prescribed window. Apply this with \(A=2\prod_{\rm earlier}a_i\). As in the cited proof, the occupied product is \(S\ge2^{k-1}\ge2h\). No implicit short-prime-interval threshold enters.

The [search and CRT ledger](routing-outer-permutations.md) prices the actual search including failed trials by \(k^{40}\) transitions and \(k^6\) visited cells. Its computational inequalities use \(k\ge2^{32}\); this note supplies the smaller search-success premise. The polynomial setup/layer bounds in [outer-layers.md](outer-layers.md) hold with \(k\ge2^{256}\), \(k^{1125}\le2^k\), \(2^{100}b_0<2^k\), \(k^{21}+1\le2^{k/8}\), all valid for \(t\ge2^{31}\). The full multiplier also has a Walsh size guard.
