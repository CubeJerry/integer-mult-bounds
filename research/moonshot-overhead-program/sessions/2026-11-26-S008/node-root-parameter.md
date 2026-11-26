# Native interchange with a smaller fixed root degree

Choose an integer \(240\le R\le4096\) once for the machine, and use the largest odd \(m\le e^{1/R}\) at a native width \(e\). Put
\[
 H_R=R(2^{17}+2),\quad E_R=2^{H_R},\quad
 C_R=\left\lceil(39/4)\sqrt[3]{R}\right\rceil,\quad
 \Phi(y)=(y^2\log_2(y+2))^{1/3}.
\]
Replacing the root-degree literal in the [counted native program](node-integrated.md) and its threshold gives one fixed multitape machine with the same return interface. On arbitrary independent binary prefix/gap/suffix data of bit volume \(V\) and field width \(u\ge0\), it costs
\[
  T_2(V,u)\le5120V\sqrt{1+u}\,2^{C_R\Phi(\log_2(u+2))},\qquad
  S_2(V,u)\le2{,}359{,}424V.
\]
In particular \(C_{240}=61,\ C_{256}=62,\ C_{512}=78,\ C_{4096}=156\). One may take \(R=240\) throughout the integer caller. This improves a numerical coefficient for the previously proved envelope. The affirmative lower endpoint here comes from the proven local bill for the specified implementation.

## Root literal, local clock and return

1. The input width is a canonical most-significant-first binary word, including the one-digit word for zero. A fixed chain of \(H_R+O(1)\) finite states reads symbols until the terminator or the \((H_R+1)\)-st digit. In the first case use the direct branch when there were at most \(H_R\) digits. In the second, the width satisfies \(e\ge E_R\), including equality. Return to the descriptor origin, using at most \(2|e|+3\) transitions for the whole test. The machine never forms \(E_R\), scans \(E_R\) cells or allocates a unary counter for the threshold. The chain is compiled once; in the standard multitape transition and visited-cell model its finite description is independent of the input, and a taken transition costs one. The number of possible control states and the number of tape cells visited are separate quantities. The finite threshold chain makes no spatial call, so a parked frame never has to encode its current position in this chain.
2. On a direct call the original 17-tape machine performs the prescribed ternary coordinate permutation and cleans up its home markers. Opening and closing the marked bank and restoring the parameters cost exactly as in the [direct-port recount](recount-node.md). Its full time is at most \(256(e+1)W\), including \(e=0\), for incoming native bit volume \(W\). It returns the unique canonical reordered data bank, ending with all temporary heads and its caller interface at their specified homes.
3. At the new adaptive cutoff \(e^{1/R}\ge2^{2^{17}+2}\). Thus \(\log_2m\ge2^{17}\); the same label, finite-row, rank and field guards hold. The fixed root search uses at most \(R(|e|+2)\) capped multiplications, with \(R\le4096\) as in the original clock. All long shape, short index and physical bank operation bounds are the same functions of the *actual* \(m,e,P,G,S\). The module and batch proof gives \(\ell\le m^{10}\le e^{1/8}\) for every \(R\ge80\). Consequently the [rounded width proof](child-volume.md) applies, including \(1\le e/(8m)\le f\le e/m<e\), every terminal and reserve call, and their exact repeated incoming volumes. The adaptive procedure invokes the same lower/upper coordinate, coefficient, geometry, finite repair, packing and data transfers at these parameters. After the contracted returns, the last \(2a\) full reserves and the remaining small direct trit moves restore the bank to the mathematical interchange in the caller's original convention. Cascaded full reserves reuse the actual preceding result. Strictly smaller \(f\) terminates every spatial chain. The finite repair height already decreases separately.
4. The nonrecursive body ledger counts an initial setup \(m^{54}W+3m^{60}\), the short control/scalar total \(m^{88}W\), and at most \(m^{38}+m^{12}\) broad events expanded into \(m^{20}\) transfers each. Even rebuilding all short tables on each return, one transfer costs at most \(m^{62}W\), which includes the prepared shape, raw data-port calls and grouped return. The independently recounted issue/return together with serializing and restoring all live control is at most \(2^{18}W\) per transfer. Charging that cost a second time for every candidate transfer gives a simple uniform full bound
\[
 \frac{w}{W}\le m^{120}+m^{94}+m^{88}+3m^{60}+m^{54}
                    +2^{18}(m^{58}+m^{32})\le 2m^{120}.
\]
Indeed \(m>2^{18}\), and the six lower positive terms sum to less than \(m^{120}\) already by replacing each occurrence of \(2^{18}\) by \(m\) and \(3\) by \(m\). The counted handoff covers finite and spatial caller modes, nested descriptors, paired markers and returning current head displacements, including an empty surviving payload at a full reserve. Every nonbase frame therefore spends at most \(2W\sqrt e\) for \(R\ge240\).
5. The parked control proof only requires \(m^{34}\le e\), valid throughout this range. Its \(2^{34}z^3\) per-frame and \(2^{36}(z+1)^5\) path bounds, where \(z=1+\lceil\log_2(2W+1)\rceil\), remain valid even on the shorter cutoff. The unbounded word sizes still obey \(W\ge3^{2e}\), and a nonbase has \(z\ge2^{17}\). Every contracted spatial call has at most half its parent's volume, every finite repair child a sixteenth, and every full reserve parks no other payload. The same fixed tape arrangement and growing/shrinking marked ends apply, including sibling interval reuse. This gives \(2^{18}W_{\rm root}\) total native visited cells. No stack frame or table depends on the old choice \(R=4096\) except through the current small indices or the now smaller fixed integer loop.

The earlier [adaptive source proof](../2026-11-26-S003/route-b/adaptive-interchange.md) chose a single primitive exponent \(K\) for both nonrecursive work and the packed leading width, and imposed \(K/R\le1/8\). The two separate estimates in steps 3 and 4 suffice here: \(\ell\le e^{1/8}\) for the spatial width, and \(w/W\le2\sqrt e\) for the time induction. The retained source algebraic identities only require the legal geometric and positive-width conditions already checked.

## Child potential with these parameters

Use the independent [sharper child estimate](compiler-full-interchange.md). At \(s=\log_2m\) and every legal adaptive arity, the sum of issued child volumes satisfies
\[
    \sum_i W_i\le W\sqrt m\,2^{c\Phi(s)},\qquad c=13/2.
\]
It is independent of \(R\). To see its scope, set \(d\) to the actual largest dyadic integer satisfying the ternary label schedule. The [previous unrounded invoice](child-volume.md) gives \(q=\log_2(\sum_iW_i/(W\sqrt m))\le33+3s/d+d^2(\log_2(s+2)+3)\), including all padded true endpoint, rank, terminal and full reserve calls. On \(z=d(\log_2(s+2)/s)^{1/3}\in[31/64,33/32]\) the term \(3/z+(20/17)z^2\) decreases. Its left endpoint, plus \(33/4096\), is strictly below \(13/2\).

Let \(y=\log_2e,\ L=\log_2(y+2),\ r=Rs/y,\ \xi=\log_2(s+2)/L\), so \(1-R/y\le r\le1\). Because \(y\ge R(2^{17}+2)\ge R^2\) and \(L\le\sqrt y\) on this range, \(y\ge RL\). Also \((y+2)/(s+2)\ge R/2\ge 2^6\), as \(s\le y/R\) and \(y\ge2R\). Hence \(1-\xi\ge6/L\). As \(\Phi(y-s)\le(1-s/y)^{2/3}\Phi(y)\) and a concave power lies below its tangent at 1,
\[
\begin{aligned}
 C_R\big(\Phi(y)-\Phi(y-s)\big)-c\Phi(s)
 &\ge c R^{-2/3}\Phi(y)\big(r-r^{2/3}\xi^{1/3}\big)\\
 &\ge c R^{-2/3}\Phi(y)\big((1-\xi)/3-R/y\big)\\
 &\ge c\,\big(y/(RL)\big)^{2/3}\ \ge\ 13/2>2 .
\end{aligned}
\]
For the first line take \(C_R\ge(3/2)cR^{1/3}\). For the second, \(r^{2/3}\le1\), \(r\ge1-R/y\) and \(\xi^{1/3}\le1-(1-\xi)/3\). The child widths \(f\le e/m\) then give
\[
 \sum_i W_i\sqrt f\,2^{C_R\Phi(\log_2 f)}
      \le \tfrac14 W\sqrt e\,2^{C_R\Phi(y)} .
\]

For a direct width \(1\le e<E_R\), \(y<H_R\) and \(y\le(2C_R)^3\log_2(y+2)\) holds throughout. Up to \(2^{20}\), use \((2C_R)^3\ge(39/2)^3\cdot240>2^{20}\). Above it use \(20(39/2)^3 R>(2^{17}+2)R\). Thus \(C_R\Phi(y)\ge y/2\), paying the entire direct time within \(512W\sqrt e\,2^{C_R\Phi(y)}\). For \(e=0\) use \(\sqrt{\max(1,e)}\) and \(y=0\). The adaptive local bill \(2W\sqrt e\) and the child quarter bound prove the same native inequality by induction. The [external binary adapter](address-range.md) then has \(W<9V,\ e\le u\) and adds \(512V\) transitions and \(128V\) visited cells. This gives the claimed constants, including zero-width requests.

For the endpoints, \(60^3<240(39/4)^3<61^3\), \(61^3<256(39/4)^3<62^3\), \(512(39/4)^3=78^3\) and \(4096(39/4)^3=156^3\). The proof requires no floating-point calculation or real-valued decision by the machine. It supplies a fixed numerical program for each selected integer \(R\) and proves resource inequalities on its actual input-dependent run. An end-to-end encoded adaptive dispatcher with a kernel-checked time proof remains separate.

The [integer replay](node-root-check.py) checks all 3,857 fixed-degree choices, exact cube bounds, and the polynomial tail. The optional command `python3 -I -B node-root-check.py --literal 240` also traverses width descriptors of 31,457,759, 31,457,760, and 31,457,761 bits. It takes 62,915,519, 62,915,521, and 62,915,521 transition tests/moves respectively in the compressed literal control description and takes the adaptive branch only on the last. These are tests of the genuine shape header, not an execution of its astronomical associated payload.

The [formal width dispatcher](node-width-dispatch.lean) defines the literal finite state machine directly in the original four pinned Lean modules. Its theorems prove the binary threshold decision for every natural width, the exact home-restoring transition count, and a visited-cell bound including the original head. Its single-tape installation also proves the corresponding trace on any selected tape in an arbitrary finite ambient machine, preserving every spectator tape. The [clean replay](node-check-lean.sh) compiled it under Lean 4.34.1 and replayed its proof objects with `leanchecker --fresh`.

The [source-level native program appendix](node-source-review.md) records the actual numerical table translations, their unbounded payload-layout and superposition theorems, examined exact coordinate families, and the physical composition and visited-set lemmas.

Prepared for Jerry Chen (@CubeJerry) with substantial ChatGPT research assistance. The altered literal and numerical count reuse the frozen algebra, physical operations and independent comparisons in the linked S003 and S008 notes.
