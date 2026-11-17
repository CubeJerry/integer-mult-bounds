# Two chronological source layers complete eight native receivers together

**Proved construction.** On the authenticated 111-role native, one source execution completes $S=\{1,3,73,76,77,80\}$ and $T=\{56,100\}$. The other 103 Y records finish untouched at their own facets. Every X restores raw at Hub while all Y are still pure at ground. The only owned movements are nine physical canonical descents. This receiver set crosses rank four in the normal space. The earlier six-receiver source involved only rank-three normals.

## A general tap-and-regroup construction

Take a core target set S and outer set T. Write $A=S\cup T$, $H=\bigcap_{i\in A}F_i$ and $H_S=\bigcap_{i\in S}F_i$. Partition the donors by $w=N(j)\cap A$, with $D_w=\bigcap_{i\in w}F_i$ and $U=w\cap S$. Suppose the old core gathers its inputs by their core signatures at $C_U=\bigcap_{i\in U}F_i$. Every extended atom with core signature U satisfies $L_j\subseteq D_w\subseteq C_U$. Thus original donors can all tap once on $D_w$ before continuing on their old common route to $C_U$. The earlier tap does not change their value. This allows portions of different new atoms to become one actual later source sum. A one-stage exact-signature delivery theorem, including its near-full antichain bound, does not apply to this joint regrouping.

In this version the native donors orthogonal to every core normal split into those also orthogonal to all of T and those orthogonal to none of T. Sums of the first type are captured at H, then read by every active receiver. The second type still gathers at $H_S$ and supplies the remaining old common sum and any old core mask originals. One verifies that the second type is numerous enough. The original core algorithm then works on every other core cohort exactly as before.

For each $t\in T$ consider the noncommon atoms w containing t. Choose a partition into $c_t$ chains of decreasing signatures, hence increasing actual charts $D_w$. For one chain, the real $Y_t$ will visit the charts and read each actual tap directly. For each other chain reserve a distinct original from the all-common donor group. First capture its raw value at H. Move the original through its chain of $D_w$, add every corresponding stationary tap, and ascend to $F_t$. There a terminal owner retains $x_q+\sum_w s_w$, where $s_w=\sum_{j:N(j)\cap A=w}x_j$. Repeat with the other disjoint physical originals. The condition

$$
    \sum_{t\in T}\max(0,c_t-1)\ \le\ |G_A|
$$

is sufficient for these outer mask originals. It is not necessary for arbitrary shared or cross-target routes. Order all tap occurrences by decreasing signature cardinality; each moving original's earlier site precedes its later one. A donor needed by two outer targets belongs to one atom, is read in one place, and may supply either/both moving carriers or deferred Y readers from that same stationary owner. The donor then physically ascends to its *core* gathering chart. Within the core phase recoding and restoration use only the old core donors and the remaining old-common carriers.

At Hub, undo every old core original recoding. Each moving outer original can now be restored by the exact raw donors in its list of earlier taps. These inverse inputs are actual original X fields at Hub; every reverse ADD is charged. After the canonical bank is formed from raw inputs, $Y_t$ takes its appropriate $K_t$ at ground, the common sum and its private raw-mask compensations at H, the tap rows of its own chain and the retained terminal values at $F_t$. Exactly one copy of each required native $s_w$ remains. The core Y values get their common contribution from H, their residual old-common contribution from $H_S$, and their remaining groups from the old core work. Thus every active output is $y_i+x_i$ and each unselected one is unchanged. The argument holds for any finite charts and sets meeting the listed source conditions, and for every positive whole-record width over every characteristic-two field. All donors, chart locations and cut states must be re-established at a different source.

## Exact eight- and seven-target instances

For $T=\{56,100\}$ the all-common rank-four chart contains 12 native donors. The core-only rank-five cohort has eight. Thirteen noncommon atoms contribute to the new targets. Their 72 actual donors tap on proper charts before regrouping by the old six signatures. Each of the two new receivers has six chains. It reads one chain itself, so five original X fields per receiver suffice. The ten actual mask originals are $0,2,15,16,19,20,39,40,43,44$. The old inner service separately uses original roles $5,7,38,41,42$. These inventories are disjoint. Three tap owners feed both new receivers in the same execution. The word gives every atom's donor list, its physical chart, actual routes and both beneficiary identities. This is simultaneous source formation, not two complete words run on reset inputs.

At operation 788 there are 284 live fields. All 111 X are raw at Hub and all 111 Y are arbitrary and untouched at ground. At operation 1341 all nine canonical fields are physically present at ground, with 293 total live fields. Seventy-one source owners retire dirty. The invoice is 71 INIT, 1,031 ADD, 477 MOVE and 71 CLEAR. It includes 72 actual tap captures, 12 additional transfers into moving outer originals, 76 raw Hub inverse ADDs for these originals, 83 forward and 83 inverse core ADDs, 535 canonical source ADDs and 36 ground canonical reads. The full movement profile and limiting comparison are

$$
155[1]+86[2]+15[3]+86[4]+21[5]+2[6]+103[7]+9[8]
=1614.107933041232804973493249727\ldots,
$$

with necessary room $7.642947169919550272752900640\ldots$ at $t=199/200$. This compares one entire native copy with its genuine closing moves. Neither a continuation after all endpoints close nor an all-111 caller is implied. Additional ordinary, implementation, ownership, precision and recursive requirements remain.

The single-extra proof control uses $T=\{56\}$. Eight noncommon tap atoms on 46 donors require six outer chains, five actual moving originals, and the same five old-core carriers. Its all-222-column word uses 56 INIT, 932 ADD, 437 MOVE and 56 dirty CLEAR. The profile is $114[1]+82[2]+15[3]+66[4]+43[5]+4[6]+104[7]+9[8]$, with moment $1613.631770521224621097600363907\ldots$ and limiting room $8.119109689927734148645786460\ldots$. The two words are alternatives.

## Reproduction

Use `python3 -B build.py --native NATIVE --utility UTILITY --out /tmp/s022-eight`, and add `--single` for the seven-target case. NATIVE is `research/moonshot-005-program/sessions/2026-11-14-S013/cloud/SOURCE-RECOVERY.json`, SHA256 `8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e`. UTILITY is the companion cross-chart-carriers author `build.py`, SHA256 `78454a0967439b113a94214831bfa1facbe9f17523a42b0d1a173786c51c771f`. Baseline `e31d437b489a416446fdd7e294bc2238829c5925`. Expected eight word SHA256 `57603fff38645768b6ffa0047ed693484c448ef899eadb0f3038f4add92009e7`, seven word `0efee1eba69dabe5f7357522a16217b9b1bcff97cd983bf4b211561d1e47bafe`. Eighteen semantic omission controls per source are run against the complete 222-column replay. Universal validity comes from the source equations and not the finite controls alone. Credit @CubeJerry, the shared-meet and S021 stationary-cache predecessors, and OpenAI-assisted source construction and review. No new κ.
