# A numerical overhead bound at every input length

## Final fixed dispatcher

Advance the global Walsh switch to \(X=2^{24}\). This one configuration change, a sharper bound on the actual finite search and a three-slope count of the existing native calls give
\[
 T(n)\le n\sqrt{1+\log_2 n}\;2^{63\Phi(\log_2(1+\log_2 n))}\quad(n\ge2),
 \qquad T(1)\le4096,\qquad S(n)\le 2^{32}n .
\]
Here \(\Phi(x)=(x^2\log_2(x+2))^{1/3}\). The [stronger proof](address-native-staircase.md) identifies the changed guard, its full physical setup price and the all-input join. The [fixed-exponent table](all-exponents.md) gives the sufficient lengths for general \(1/2+1/q\). The [finite-history proof](routing-refined-walsh.md) gives the sharper specialized \(0.501\) result. Both dispatchers have the same large-input execution.

For \(t=\log_2\log_2 n\), the same configuration satisfies the [smooth coefficient 60](profile-limit.md) from \(t=1{,}572{,}864{,}480\) and the [smooth coefficient 53](coefficient-53.md) from \(t=2^{69110}\). Both sharper bounds use \(\sqrt{\log_2 n}\) and leave an additional binary bit of time allowance.

## Independently verified coefficient-71 dispatcher

Let \(L=1+\log_2n,\ x=\log_2 L,\ \Phi(z)=(z^2\log_2(z+2))^{1/3}\). For every \(n\ge2\), one fixed deterministic multitape machine satisfies
\[
                        T(n)\le n\sqrt L\,2^{71\Phi(x)}. \tag{1}
\]
At \(n=1\) it takes at most \(4096\) transitions. The common cap is \(2^{32}n\) tape/address pairs ever visited, including idle heads; see the [spatial accounts](routing-outer-space.md) and [dyadic branch](address-dyadic-caller.md). Write \(\ell=\log_2n,\ z=\log_2\ell\) in the two transform branches. Their stronger formula with \(\ell,z\) implies (1).

## One fixed program

1. Measure \(n\) on the first word and restore the input head. For \(n\le2^{48}\) use the [19-state raw multiplier](schoolbook.md).
2. Otherwise compute \(b=\lceil\log_2n\rceil,\ h=\lceil n/b\rceil,\ k=\lceil\log_2(4h)\rceil,\ N=2^k\). For \(k<2^{4096}\) use three ordinary dyadic Fourier transforms.
3. For \(k\ge2^{4096}\) use the coprime-axis [full clock](integer-clock.md), with \(R=240\). Put \(X=\lceil\log_2(k+2)\rceil\). If \(X<2^{26}\) use unnormalized integer butterflies and round the combined normalization once. Otherwise use the aligned-modulus adaptive executor. [All-width Walsh proof](walsh-node.md).


Compare the bit length of canonical \(k\) with 4097 to test \(k\ge2^{4096}\). Small \(n\) uses only a 49-bit length comparison. For transform inputs, long division of binary \(n\) by \(b\) costs at most \(2^{12}(b+3)^4\) transitions and \(64(b+3)\) cells by marked shift/compare/subtract rounds, included in the polynomial setup. Testing whether \(n\) is a power of two gives \(b\); \(k\) is the bit length of \(4h-1\). For \(n>2^{48}\) we have \(k\ge32\): otherwise \(b<2k\le62\) and \(n\le b2^{k-2}<2^{35}\). On both transform branches \(k\le\ell<2k\) and \(Nk\le16n\).

For \(k\ge2^{4096}\) all tables requiring \(k\ge2^{256}\) fit. The [sharper axis witness](address-axis-window.md) certifies the actual coprime search for every \(k\ge2^{32}\). At \(X\ge2^{26}\), \(\lceil\log_2(X+2)\rceil\le28X/2^{26}\). Since \(62^3>28\cdot8192\), the largest arity has \(128Y\le(63/64)X\), hence \(m^{128}\le k/32\). Even exhaustive Gram/basis construction fits the spectator reserve of a nonempty recursive role. For smaller \(X\) the direct one-group integer butterflies cost at most \(2^{28}Nk^2\) before normalization. Now \(X/\log_2(X+2)\le2^{26}/26<140^3\) gives \(\sqrt{k}\le2^{70\Phi(X)}\). This direct branch uses \(U=1\), with no rational-key catalogue. The [Walsh clock](walsh-node.md) consequently applies across the entire third input range with the absolute coefficient \(A_W=2^{110}\cdot5121\).


## Three inequalities cover all lengths

* **Small.** The raw branch and length test cost at most \(4096n^2\le2^{60}n\). For \(n\ge2\), \(x\ge1,\ \Phi(x)\ge1\), and \(60<71\). The case \(n=1\) has the listed separate bound.
* **Dyadic.** Use forward decimation in frequency on both operands, multiply their identically bit-reversed spectra, and apply the reversed decimation-in-time adjoint. The [dyadic caller proof](address-dyadic-caller.md) prices normalized butterflies, twiddles, full transforms and recovery. Its weaker bound \(2^{160}N(k+1)^6\) suffices. Since \(Nk\le16n\) it is at most \(2^{170}n k^5\). Here \(5\le z<4097\). For \(5\le z\le8\), \(\Phi(z)\ge3\); for \(8\le z\le32\) it is at least 5; for \(32\le z\le64\) it is at least 8. Each interval has \(170+5z\le71\Phi(z)\) by these endpoint comparisons. For \(64\le z\le4097\), \(z\le512\log_2(z+2)\): split at 2048 and use respectively \(\log_2(z+2)\ge6\) and \(\ge11\). Thus \(\Phi(z)\ge z/8\) and \(170+5z\le71z/8\). This gives (1) on the middle range even before using its square-root factor.

* **Coprime box.** Here \(z\ge4096\). Use equation (1) in [the whole clock](integer-clock.md) with the smaller \(A_W\). The logarithm of time divided by \(n\sqrt\ell\) is bounded by \(182+4\log_2(z+2)+70\Phi(z+2)\), since \(55+110+13+4=182\). The [formal profile calculation](whole-profile.lean) proves \(\Phi(z+2)\le\Phi(z)+2\). For \(z\ge4096\), \(64\log_2(z+2)\le z\) by comparison at 4096 and decreasing log density. Cubing gives \(16\log_2(z+2)\le\Phi(z)\). Also \(\Phi(z)\ge512\) because \(4096^2\cdot8=512^3\). Thus \(182+140+1\le3\Phi(z)/4\) and in fact \(2T\le n\sqrt\ell\,2^{71\Phi(z)}\).

The sharper \(0.501\) cutoffs exceed the start of the third branch and its adaptive Walsh domain. Both small-length changes leave their physical execution unchanged. [Large-length implication](integer-clock.md) · [Piecewise transfer](routing-piecewise-walsh.md)

