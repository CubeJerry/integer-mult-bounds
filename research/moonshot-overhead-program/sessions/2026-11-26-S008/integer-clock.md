# Numerical clock for the full integer product

The [complete final dispatcher](all-lengths.md) covers all input lengths with coefficient 63 after its one stated guard change. The earlier coefficient-71 configuration below details the shared large-input clock and its first sufficient \(0.501\) threshold. The [sharper piecewise audit](routing-refined-walsh.md) applies to both configurations in that range.

Write \(\ell=\log_2 n,\ x=\log_2\ell,\ \Phi(x)=(x^2\log_2(x+2))^{1/3}\). Logarithms in the numerical leading coefficient are base two. A run starts with two arbitrary \(n\)-bit words on a single tape separated by one symbol and outputs exactly \(2n\) bits on an otherwise blank tape. The number of tapes, alphabet and control are fixed. All tape cells ever visited count, including erased scratch and the initial heads.

Fix \(R=240\) for every native interchange. The public range price is \(J(u)=5120\sqrt{1+u}\,2^{61\Phi(\log_2(u+2))}\). See [node-integrated.md](node-integrated.md), [node-root-parameter.md](node-root-parameter.md), [compiler-full-interchange.md](compiler-full-interchange.md) and [address-range.md](address-range.md). This uses \(2m^{120}V\le2\sqrt e\,V\) and counts every grouped child and full reserve. The [Walsh compiler](walsh-node.md) pays ordinary scalar events and true spatial matrix events separately. It gives \(B_W=\max(48,61+9)=70\). A safe coefficient is \(A_W=2^{2^{24}+28}(1+5120)\). The smaller same-machine \(2^{110}(1+5120)\) also works by the tightened ordinary proof. The conclusions below already follow with the larger coefficient.


Set \(K=2^{2^{48}}\). For \(n\ge2^{2K}\) the following large-input argument applies. The [all-length theorem](all-lengths.md) sets the final dispatcher and proves the same smooth profile on every \(n\ge2\). Put \(b=\lceil\log_2n\rceil,\ h=\lceil n/b\rceil,\ k=\lceil\log_2(4h)\rceil,\ N=2^k,\ b_0=\lceil\log_2(2k)\rceil,\ X=\lceil\log_2(k+2)\rceil\). Then \(b<2k,\ k\ge K,\ k\le\ell\le b,\ Nk\le16n\). Indeed \(n\le bh\le b2^{k-2}\) and \(\log_2b\le b/2\); also \(4h\le8n/b\le n/2\) for \(b\ge16\). Now \(N<8h\) gives the volume bound. The [axis witness](axis-cutoff.md) guarantees the actual coprime search from \(\log_2 k\ge2^{31}\). Finite Walsh setup applies at \(X\ge2^{48}\).

## Complete price of the three transforms

Use full complex records of at most \(1024k\) bits and residue records of \(100k\) bits. Three transforms of at most \(2^{29}b_0\) layers cover the two forward maps and the adjoint. A selected Walsh layer costs at most \(2^{18}A_W b_0 Nk\sqrt k\,2^{70\Phi(X)}\). A [full block-permutation layer](routing-outer-permutations.md) costs \(2^{72}b_0^3(1024Nk)(1+J(k))+k^{1120}\); all three extra CRTs together cost at most \(2^{75}b_0^4(1024Nk)(1+J(k))+k^{1125}\). Phase preparation, short-word products, pointwise multiplication, scaling and output together cost at most \(k^{850}+2^{100}b_0Nk^{3/2}\) by [outer-layers.md](outer-layers.md). These charges include exceptional addresses, table generation, every recurrent access, precision control and the \(2n\)-bit output.


As \(1+J(k)\le3\cdot5120\sqrt k\,2^{61\Phi(X)}\), \(b_0\le k\) and \(k^{1200}\le2^k\), their sum, including root dispatch, is at most
\[
 2^{55}A_W b_0^4 Nk\sqrt k\,2^{70\Phi(X)}. \tag{1}
\]
The Walsh term has coefficient below \(2^{49}A_W\). All permutation and CRT coefficients together are less than \(2^{130}\) before \(b_0^4Nk\sqrt k\,2^{70\Phi(X)}\), well below \(2^{54}A_W\) with either choice of \(A_W\). Within [the independent spatial bill](routing-outer-space.md), two disjoint re-used external calling families have uniform guarded volume limits \(1024Nk\) and \(100Nk\); their worst head extents, accumulated over all calls and both movement directions, plus the remaining marked banks visit fewer than \((399969\cdot1124+2^{22})Nk\) cells. There are fewer than 8192 fast-program heads even when dormant. The direct branch in [schoolbook.md](schoolbook.md) therefore satisfies the same common linear bound as the fast one, namely \(2^{32}n\) ever-visited tape/address pairs for every positive \(n\).

## Explicit rate and unit threshold

Since \(k\le\ell\), both \(b_0,X\le x+2\). Taking logs after division by \(n\sqrt\ell\) in (1) bounds excess time by \(2^{25}+4\log_2(x+2)+70\Phi(x+2)\) in binary logarithmic units, even with the larger \(A_W\). The function \(\log_2(z+2)/z\) decreases for \(z\ge2\). Consequently \(\Phi(x+2)\le(1+2/x)\Phi(x)\) and \(70(\Phi(x+2)-\Phi(x))\le140\). At \(x\ge2^{48}\), \(2^{25}+140\le x^{2/3}/2\), and \(4\log_2(x+2)\le x^{1/3}\le x^{2/3}/2\). The middle inequality holds at the left endpoint and the power term's derivative is larger throughout. We obtain
\[
 \boxed{T(n)\le n\sqrt{\ell}\,2^{71\Phi(x)}},\qquad n\ge 2^{2K}. \tag{2}
\]
Equivalently \(\delta(n)\le71(\log_2(x+2)/x)^{1/3}\) on this range. Replacing \(\ell\) by the programme convention \(L=1+\log_2n,\ x=\log_2L\) gives the same upper bound by monotonicity.

Set \(D=(71{,}000)^3,\ t_*=55D=19{,}685{,}105{,}000{,}000{,}000\). We have \(t_*+2<2^{55}\) and \(t_*>2^{48}+1\). At \(x=t_*\) this gives \(D\log_2(x+2)\le x\), and the comparison persists for every larger \(x\) by the same decreasing ratio. Cubing gives \(71\Phi(x)\le x/1000\). For \(n\ge 2^{\,2^{t_*}}\), the clock (2) therefore yields
\[
 \boxed{T(n)\le n(\log_2n)^{501/1000}},\qquad S(n)\le2^{32}n. \tag{3}
\]
This is a worst-case step count with leading coefficient one. The threshold is sufficient. Its logarithm twice in base two is \(t_*\). All bounds cover leading zeros and arbitrary input words, not just the oracle replays.
