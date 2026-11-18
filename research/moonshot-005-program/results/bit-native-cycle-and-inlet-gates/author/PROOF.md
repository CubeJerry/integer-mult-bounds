# Exact canonical normalization, native gauge equations, and unavoidable line taps

**Proved within the interfaces stated below. No new supplier or κ.**

The S022 balanced source has 5,760 field coordinates at each of 111 real
donors and receivers. Its proof makes every one of the 6,470 foreign transfer
blocks invertible, and the mixed construction fixes 69 common rows. Neither
fact by itself identifies the other rows. This note gives an exact test for
what source and receiver changes of basis can accomplish on a fixed block
assignment. It also verifies the canonical-ground reduction and a chronological
obstruction to replacing the real line taps by later snapshots.

The native geometry is read from S013 `SOURCE-RECOVERY.json`, SHA-256
`8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e`.
The balanced factor has SHA-256
`346e7604b000ba057e49e8dcae639eaf1b8d82aeb1466f8b959a84390971dfa7`.
The fixed programme baseline is `8cf982065bccdd62de2856b16635a6ee06dadb0c`.

## 1. Arbitrary linear canonical decoding still forces the proper matrix

Let `O` be the 111-by-111 binary orthogonality matrix of the native root
lines: `O_ij=1` exactly when `j` is a foreign donor in receiver facet `F_i`.
It has zero diagonal. Put `K=I+O`. The independent checker gives

\[
 \operatorname{rank}_{\mathbf F_2}K=9,
 \qquad \operatorname{rank}_{\mathbf F_2}O=108.
\]

For every receiver `i`, restriction of `row(K)` to the input columns
outside `N(i)` has rank nine. Thus no nonzero word of this code is supported
entirely on the foreign neighbors of one receiver. Binary full-rank minors
remain nonzero after any characteristic-two field extension; taking direct
sums or tensoring by an arbitrary positive internal width preserves this
injectivity.

Consider any linear two-wave realization at that width. Grant arbitrary
linear decoding of the nine fixed canonical packets, arbitrary processing
of the independent original Y bank at ground, and arbitrary local block
operators, including singular and noncommuting ones. Suppose every other
X-dependent contribution moves only through the proper increasing source
diagram. By nesting its contribution `B_ij` vanishes unless `j` belongs to
`N(i)`. The actual final output has the form

\[
 A y+C Hx+B x,
\]

where the rows of `H` form a basis of the canonical code, with the relevant
bank multiplicity understood. Every row of `CH` lies in that code. This
separation is an identity between actual input/output maps; it does not
permit a free physical read or reorder a computation.

The target `y+x` first forces `A=I`. On the complement of `N(i)`, the proper
part vanishes, so the canonical row `CH` agrees with the `i`th row of `K`:
both have its identity block at `i` and zeros at all other complement ports.
The injective restriction proves equality on the full input bank. Consequently

\[
 CH=K\otimes I,\qquad B=O\otimes I.                 \tag{1}
\]

This conclusion does not require the nine packets to be used only as one
initial `Y+KX` preload. It does require their retained row code and the
proper-source support restriction. Mutable canonical packets that acquire
new noncanonical information, extra informative descending paths, and a
changed canonical code are outside (1).

## 2. A spanning tree and exactly 6,249 native four-cycle equations

This part works over any field and any positive bank dimension `b`. Fix an
invertible matrix `B_ij` on every edge of the native bipartite graph. Its
left vertices are the 111 receivers and its right vertices the 111 donors.
There are 6,470 edges. The exact integer-dot-product census shows that every
pair of distinct receiver neighborhoods intersects in at least 23 donors,
and every triple intersects in at least eight.

Use receiver `0` as root and call its 56 neighbors the core donors. For each
other receiver `i`, choose the least common donor `a_i` of `i` and `0`.
For each noncore donor `j`, choose the least adjacent receiver `p_j`.
The following 221 edges form a spanning tree:

1. `(0,j)` for each core donor;
2. `(i,a_i)` for each nonroot receiver;
3. `(p_j,j)` for each noncore donor.

Define invertible matrices recursively by

\[
 R_0=I,\quad C_j=B_{0j}\ (j\text{ core}),\quad
 R_i=B_{i a_i}C_{a_i}^{-1},\quad
 C_j=R_{p_j}^{-1}B_{p_jj}\ (j\text{ noncore}).
\]

Every tree edge then has normalized matrix

\[
 H_{ij}=R_i^{-1}B_{ij}C_j^{-1}=I.                  \tag{2}
\]

There are exactly `6470-221=6249` remaining edges. Each is tested by a
four-cycle with receivers `i,h` and donors `j,d`:

\[
 B_{ij} B_{hj}^{-1} B_{hd} B_{id}^{-1}=I.          \tag{3}
\]

For a non-tree edge with core donor `j`, set `h=0,d=a_i`. For a noncore
`j`, set `h=p_j` and choose `d` from the common neighborhood of `0,i,h`.
The triple-intersection bound guarantees that this donor exists.

First apply all core equations. Each uses three tree edges and forces
`H_ij=I` on its fourth edge. Next apply the noncore equations. Their other
three edges are now already fixed: `(h,j)` is a tree edge and both edges
at donor `d` are core edges. Hence they force `H_ij=I` as well. Conversely
`B_ij=R_i C_j` makes every equation (3) hold. This proves the equivalences

\[
 \begin{split}
 &\exists\,U_j,V_i\in\operatorname{GL}_b:\quad
       V_iB_{ij}U_j=I\text{ on every native edge}\\
 &\quad\Longleftrightarrow H_{ij}=I\text{ on every non-tree edge}\\
 &\quad\Longleftrightarrow\text{the 6,249 selected four-cycle identities (3).}
 \end{split}                                                    \tag{4}
\]

The ordered multiplication is essential: the blocks need not commute. These
are independent edge constraints in the triangular sense just proved; this
does not mean the scalar entries of an interior network code are independent.
The certificate lists every tree edge and every chosen four-cycle. No long
cycle search, scalar commutativity premise, or receiver-specific physical
channel is used.

## 3. The exact number of coordinates obtainable by endpoint gauges

Let `P_k` select the first `k` rows of a `b`-coordinate bank. For the same
fixed block assignment, define the common left-fixed space

\[
 \mathcal W=\{w\in F^{1\times b}:w(H_{ij}-I)=0
                 \text{ for every non-tree edge}\}.
                                                               \tag{5}
\]

**The maximum possible `k` for invertible endpoint gauges satisfying
`P_k V_i B_ij U_j=P_k` on all edges is exactly `dim W`.**

For necessity, write `L_i=P_k V_i` and `Q_j=P_k U_j^{-1}`. The edge equations
are `L_i B_ij=Q_j`. Let `W=L_0`, a matrix of row rank `k`. Propagation along
the above spanning tree gives `L_i=W R_i^{-1}` and `Q_j=W C_j`. Every
remaining edge therefore gives `W H_ij=W`. Thus all `k` rows of `W` lie in
the space (5).

Conversely take `k` independent rows in (5), assemble them as `W`, and extend
them to a basis, giving an invertible `T` with `P_k T=W`. Set

\[
 V_i=T R_i^{-1},\qquad U_j=C_j^{-1}T^{-1}.
\]

Then `P_k V_i B_ij U_j=W H_ij T^{-1}=W T^{-1}=P_k`, as required. Equivalently,
the answer is `b` minus the rank of the block matrix formed by concatenating
the columns of every `H_ij-I`. Field extension does not change this rank.
It is a finite exact linear-algebra test once the actual matrices are known.

There is a useful strict negative control. On the native graph let every
block be identity except one non-tree block. On that edge use
`diag(I_69,C)`, where `C` has 2,844 copies of a companion matrix of
`t^2+t+1` and one companion matrix of `t^3+t+1`. The complement dimension is
`2*2844+3=5691`, so the full bank dimension is 5,760. Each companion and its
difference from identity are invertible in characteristic two. Hence every
edge block is invertible and has the first 69 rows of identity, but (5) has
dimension exactly 69. No endpoint gauge can produce a seventieth common row.

This is an algebraic counterexample to an inference from the already proved
properties; it is **not asserted to be a realization of the balanced physical
network**. It leaves open a better interior coefficient choice. The finite
checker realizes the same control in dimension five with two fixed rows,
tests noncommuting positive gauges on the entire native graph, and rejects
a deliberately reordered cycle product.

As a positive corollary, if `P_k B_ij=P_k` already holds everywhere, one may
choose any receiver `r` and put `U_j=B_rj^{-1}` for its adjacent donors,
with other donor gauges identity. Since `P_k B_rj^{-1}=P_k`, the common `k`
rows persist, while every proper block at receiver `r` becomes identity.
This completes that receiver algebraically and does not align all other
receivers. Original-X restoration and arbitrary-Y normalization remain real
ordinary operations in a physical implementation.

## 4. A post-line crossover cannot realize the balanced native target

Use the actual S022 balanced routes and `b=5760` field slots. Each native
donor has 28 incident A2 planes. If a plane `H` has `m_H` native donors,
its factor `u_H` gives

\[
 x_H=12/m_H+u_H,\qquad e_H=\max(8,x_H).
\]

The actual early X bank of donor `j` sends `45 x_H` records to `H`; actual
late Y visits at its line supply `45(e_H-x_H)` further donor-dependent
departures. For a foreign pair `(i,j)`, exactly 16 of these planes lie in
`F_i`. Every proper information path from `j` to `i` must start along one
of these 16 plane branches. Its first source cut therefore has early capacity

\[
 E_{ij}=45\sum_{H\ni j,\ H\subset F_i}x_H.           \tag{6}
\]

The independent census on all 6,470 pairs gives

\[
 2880\le E_{ij}\le3600<5760.                         \tag{7}
\]

Suppose all late Y information from `j` is acquired only after the early X
records have departed their native line. Grant arbitrary early mixing,
unlimited stationary snapshots at any later proper chart, arbitrary local
recoding and all existing public trajectories. Assume there is no other
informative channel bypassing the cut (6). Then the proper transfer rank of
each pair is at most `E_ij`, or `E_ij V` at internal width `V`. Equation (1)
requires rank `5760 V`. Thus **no such post-line-only construction can
complete even one required full foreign block**. Restricting all cross-wave
reads to the D4 middle layer is a special case. The statement does not exclude
the published balanced code, which uses actual late line taps.

This impossibility also allows arbitrary deterministic processing over a
finite alphabet. Hold all neighbors of `i` except `j` fixed. Because the
canonical code restricted outside `N(i)` has rank nine, choose those outside
inputs as functions of `X_j` to make all canonical messages zero. Fix the
independent original Y values. The `i`th canonical equation now forces
`X_i` to vary bijectively with the `b` coordinates of `X_j`. Outside donor
lines cannot reach `F_i` on proper increasing routes. Therefore the desired
receiver output ranges over `|F|^b` values, but the cut (6) supplies at most
`|F|^{E_ij}` transcripts. This contradicts (7). No dimension claim is inferred
from cardinality over an infinite alphabet.

With the genuine late source-line taps restored, put
`L_ij=45 sum(e_H-x_H)` over the same 16 visible planes. The exact census is

| Total first-cut capacity | Native ordered pairs |
|---|---:|
| `E_ij+L_ij=5760` | 6,110 |
| `E_ij+L_ij=5940` | 360 |

Thus a full construction needs at least `5760-E_ij`, or 2,160 to 2,880,
additional independent source dimensions across the missing part of each
pair cut. On the 6,110 tight pairs the complete source transcript must be
bijective on the donor input; in a linear realization its source map is
square invertible. Later caches cannot repair a failure of that injectivity.
The 360 remaining pairs have 180 coordinates of source slack. These are
information requirements on already paid routes, not extra MOVE counts or a
new global lower bound obtained by adding overlapping pair demands.

## Reproduction and remaining work

Run `check.py` with `--native`, `--factor`, `--layout`, and `--out`; the source
paths are the S013 source recovery, balanced factor, and tight-atlas layout
listed in the dependency receipt. Expected status is
`PASS_NATIVE_GAUGE_CYCLES_AND_CAUSAL_INLETS`. The script independently
reconstructs all A2 planes using exact Gram determinants, checks source pins,
emits every selected four-cycle and every source cut, and uses only the
Python standard library. Its finite controls corroborate the universal
arguments above and do not materialize the large common network code.

The next constructive question is to choose actual interior/source matrices
satisfying these identities or to change the physical interface. A common
invertibility polynomial does not impose the equalities (3). The balanced
source still needs all remaining coordinates, a compatible complex supplier,
ordinary pricing, complete recursive accounting, and the five retained
framework assumptions. No new complete κ is claimed.

Credit @CubeJerry; original native, balanced-routing and canonical-code
authors; S022 partial synchronization and source-quotient work. The gauge
normal form and this independent causal audit were developed by S023 worker B
with substantial OpenAI assistance. No human or formal-kernel review is claimed.
