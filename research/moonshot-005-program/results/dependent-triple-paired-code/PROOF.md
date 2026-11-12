# A dependent E8 triple removes one actual reverse residual direction

**Classification:** a proved finite source-specific construction. Its algebraic identities hold for every independent scalar input. Exact source replay covers all 1880 input directions. Three ordinary forward rows are completed and the actual hosted reverse residual loses one rank. No individual reverse pair, complete shared native, or new κ is claimed.

## Source and interface

Native: `research/shared-wire-split-composition/data/final.json.gz`, SHA256 `2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883`. Baseline: `research/moonshot-005-program/results/eight-packet-seven-corrections-fused/WORD.json.gz`, container SHA256 `1536c714dd3500709c7717b8687b53f98d7a30f482aa5b09e5c25a4a23cf8153`, payload SHA256 `05b503f0c2f219f328353b984ca821db9d6c3cc0225ff3380c551708d247e8d8`.

This is an alternative schedule from that parent. Its benefits and costs must not be added to the separate paired-eight candidate. The 1480 common and 400 private inputs remain independent. Write q_r=v_r-u_r. For hosted i, denote the distinct directions q_Xi,q_Yi,q_X2i,q_Y2i by a_i,c_i,b_i,d_i. The targets are c_i+a_i and b_i-d_i. There are 96 hosted indices. The eight coupled indices have no independent b,d bank; they are excluded from dual encoders, while needed first-X directions remain forward donors.

Let r_i be the source E8 root and G_ij=r_i·r_j, with G_ii=8. The retained packets produce c_i+(Ga)_i/8. Required corrections have matrix A=I-G/8, including A_ii=0. All nonzero foreign entries are ±1/2. The selected indices S=(0,1,98) have

\[
G_{SS}=\begin{pmatrix}8&4&4\\4&8&-4\\4&-4&8\end{pmatrix},\quad
r_0-r_1-r_{98}=0,\quad \operatorname{rank}G_{SS}=2.
\]

The actual first-Y roles are 112,113,210; paired Y2 source roles are 882,883,974.

## Forward current-row construction

The correction supports partition into three disjoint 24-donor groups, with receiver pairs(112,113),(112,210),(113,210). There are no singleton or triple-support donors. Their exact facet intersections are:

| Pair | Chart | Dimension | Canonical frame |
| --- | --- | --- | --- |
| 112,113 | 1095 | 7 | 3,4,25,32,64,128,256 |
| 112,210 | 1096 | 7 | 3,13,16,36,68,132,260 |
| 113,210 | 1097 | 7 | 3,8,21,36,68,132,260 |

Every donor line lies in its group's chart C_g. All nonpivot donors visit C_g, contribute to two stationary aggregates, then reach the hub. One pivot p contributes to the aggregate for a visiting receiver, and its raw field becomes the other receiver i's aggregate:

\[
a_p\leftarrow A_{ip}a_p+\sum_{j\in D_g\setminus\{p\}}A_{ij}a_j.
\]

Here D_g is the donor set and A_ip is nonzero. The pivot passes through i's final facet, deposits the aggregate in a stationary collector, and reaches the hub. All nonpivot originals are then available at the hub. Subtracting their terms and dividing by A_ip restores the pivot exactly.

Receiver 112 visits chart(112,113),113 visits(113,210),210 visits(112,210). Each obtains its other aggregate from the pivot at its final facet. Each route is zero→pair intersection→final facet. No raw field is reset or discarded; none of the nine stationary collectors moves. All 104 original first-X donors are restored at boundary 1852 before any of the 520 retained E8 source reads. The packets still produce c_i+(Ga)_i/8, and the corrections give c_i+a_i for i in S. The parent's seven history corrections remain.

## Inverse-transpose identity and actual source availability

Let B be an m×n matrix of row rank m on independent donor coordinates. Choose an invertible column minor J and replace the corresponding rows of I_n by B, obtaining M. Let E inject into those pivot coordinates. Eliminating the nonpivot identity rows proves M invertible; reading its pivot rows gives M^T E=B^T. Therefore for every b,d,

\[
M^T(M^{-T}b-Ed)=b-B^Td.
\]

This algebra does not establish source availability. The literal word establishes that separately: hosted restrictions of the three pair matrices have sizes 2×23,2×24,2×21 and rank 2. The pivot first-X indices are(2,98),(1,6),(0,7). Their X2 carriers have the same initial line and final hub as the paired first-X carriers. Their selected Y2 sources have the same initial zero and final facets as first-Y receivers.

The word first positions the three selected Y2 sources at their facets. In each disjoint hosted donor group, all X2 carriers reach C_g with their original independent b rows. Explicit INIT/ADD/CLEAR snapshots implement M^{-T}. Two pivot carriers visit their respective facets and subtract the actual d_i rows already present there. All carriers then reach the hub, where explicit snapshots implement M^T. Thus every hosted output is exactly

\[
b_j-\sum_{i\in S}A_{ij}d_i.
\]

There are 136 nonzero transpose coefficients on 68 carriers, not 136 completed duties. No group reads a row changed by another group. Temporary snapshots number at most 24. All new source transformations occur before the parent's common suffix. The changed first-Y and X2 rows have no outgoing read in the suffix, and their only writes there are final recouplings. Exact 1880-column prefix comparison and literal suffix identity therefore preserve the parent's common restoration. The reverse shear has explicit inverse b_j=b'_j+sum_i A_ij d_i, retaining every d direction.

## General residual-rank theorem

Suppose H is an independent hosted bank of size n, S⊂H, G_ii=8, and the entire actual block b→b−A_{S,H}^T d_S has been implemented, with A=I−G/8. Order rows and columns by S,H\S. Relative to target b−d, the remaining residual is

\[
D=\begin{pmatrix}G_{SS}/8&0\\G_{H\setminus S,S}/8&I\end{pmatrix},
\qquad \operatorname{rank}D=n-|S|+\operatorname{rank}G_{SS}.
\]

The identity block contributes n−|S| pivots and eliminates the lower-left block by column operations; the other pivots are those of G_SS. This includes the full diagonal target debt. It requires distinct hosted banks and the entire coefficient block on all hosted donor columns. An abstract coefficient matrix, partial row acquisition, or aliased coupled coordinates does not meet those premises.

For this actual triple, D has rank 96−3+2=95. The source root relation yields the explicit right-kernel direction e_882−e_883−e_974. The same relation is also a left-kernel direction supported on the corresponding X2 rows, so the target combination X2[772]−X2[773]−X2[868] is already correct. Every diagonal entry of D is still 1: no individual reverse pair is complete. The gain cannot be subtracted from the invoice without a legal algorithm exploiting it.

An independent orthogonal selected set has full principal Gram rank and gives no gain by this formula. This explains the earlier paired-eight rank 96 while preserving that package's correct source interface. Dependent target sets offer a concrete constructive route to globally reducing residual rank.

## Full partial invoice and remaining work

The final word has 76039 instructions: 65061 ADD, 3676 SCALE, 6877 MOVE, 212 INIT, 212 CLEAR, one COPY. It allocates 90 owned labels, reaches peak 43 live owned fields, and finishes with zero. Its 559 raw MOVE calls have histogram {1:26,2:133,5:1,6:141,7:7,8:251}, rank sum 3200. Actual split routes are charged, together with all eight retained rank-nine packets.

Using the pinned H4 invoice and original native raw histogram R_src, the complete partial caller is

\[
T=T_4,\qquad P=P_4+18(R_{new}-R_{src})+18\cdot8\{9\}.
\]

Target positions 27344, paid positions 131850, rank surplus 3760. At exponent 199/200 the exact bracket for sum_r(T_r−P_r)r^(199/200)/18 is in RESULT.json, with lower endpoint approximately 43.730571695159306. Relative to this package's forward intermediate, the dual code adds 612 ADD, 136 INIT, 136 CLEAR and 74 raw MOVE instructions; no extra owned MOVE. All scalar operations, snapshots, refinements and recursive calls remain explicit.

There remain 4841 forward foreign coefficients, rank 95 hosted residual, and coupled/global obligations. Even hypothetical 95-field terminal rank-one delivery exceeds the available moment. Rank 95 also does not prove 95 legal deliveries: the fixed terminal interface retains 96 distinct source facets with nonzero residual columns, each needing a first paid departure in a source-restricted terminal repair. The independent review gives this spatial distinction and a sharp 96 rank-one-copy suffix. No price advantage is claimed from a free algebraic rank factorization.

This actual compatible partial code exploits source dependence. It does not prove the remaining work affordable. All uniform supplier, compiler, precision, owned erasure, native/all-columns and analytic-recovery foundations remain.

## Verification and provenance

Final word payload SHA256: `19a7a89b4623f7f095833a46369fad7bf6d63eabd6bf5a7929ed52a87b55b121`; gzip SHA256: `13d43635c2900a7220b5bd1da21e63807d728d4c67ccf2370178f171db62ef0c`. Both intermediate and final words and receipts are identical under normal and optimized Python. Explicit checks remain enabled under `python -O`.

`audit.py` reconstructs the hosted block from source roots, compares all 1880 prefix columns, checks the actual rank and both kernel interpretations, and rejects seven semantic mutants: either dual inverse stage, an injection sign, a missing Y2 facet stop, a primal inverse, a missing forward acquisition stop, and a kernel sign.

All 84 introduced chart maps relative to the fused parent have canonical exact Clifford recipes checked by the retained signed-Pauli/global-phase engine. `CHART-MAPS.json` pins both existing engines. Assertions are enabled for these checks, and a wrong phase is rejected. Reusing that independent implementation is credited explicitly; it is not a newly written engine or a physical supplier. Worker C's separate review independently re-emits the entire word, checks every original E8 read, derives the transpose block and residual rank, and checks an explicit 400-row inverse.

This is new S008 work by the persistent @CubeJerry programme, with substantial OpenAI AI assistance. It builds on the native shared-wire split construction, admitted E8 and fused history packages, new cohort reconstruction and hosted-bank paired identity. Predecessor source paths, notices and credits remain intact.

## Open next questions

The next obligation is one globally compatible larger dependent target set whose actual acquisition and dual schedules remove many residual directions without resetting any raw route or assuming transformed rows available. The rank formula states the benefit only after that full source block exists. Full correction on all 96 hosted rows would leave Gram rank eight, but that alone supplies neither eight legal rank-one final deliveries nor the eight coupled reverse repairs. Exact raw refinement accounting must be combined with legal residual source access. A second route is to preserve encoded current rows across nested cohorts and explicitly derive what each later stage can read. Neither global composition is proved here.
