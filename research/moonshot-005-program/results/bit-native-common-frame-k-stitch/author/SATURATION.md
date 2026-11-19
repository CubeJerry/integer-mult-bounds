# Exact native K saturation and the obstruction to retaining a sparse packet

**Proved necessary conditions for a complete linear proper map in the
pinned b=480 two-wave atlas. These are not sufficiency or impossibility
claims for a changed atlas.**

## 1. Model and quantified statement

Let F be any field of characteristic two, and let s be any positive
integer body width. Every field owner in the pinned b=480 atlas now
contains s F-symbols. Retain all original owner routes, chronology and
proper source support. Allow arbitrary linear local maps, paid stationary
storage, source basis changes, inter-D coding at K, and arbitrary final
linear decoding. All X-dependent information in the proper part must
reach a native receiver through its actual early X visits or late Y
terminal arrivals. No additional informative return, source read or MOVE
is permitted in this proper map.

Fix i=80 or i=1. Let K(i) be its28 incident right A2 planes. For K in
K(i), let S_K be all native source lines orthogonal to every line of K.
Let z_(i,K) be the tuple of the X-dependent coefficients of **all** actual
early and late original-owner values delivered through K to receiver i,
ordered by their actual arrival slots. The original-Y baseline is set to
zero only when defining this linear X-response map; the final algorithm
must separately preserve arbitrary original Y.

The tuple z_(i,K) has length30s. It has source support contained in S_K.
Write C_(i,K,j):F^(480s)->F^(30s) for its block at donor j. Suppose the
complete proper endpoint B has an invertible 480s-by480s block B_ij for
every native foreign donor j of receiver i. Then:

1. rank C_(i,K,j)=30s for every K in K(i) and every j in S_K.
2. For every such j, its sixteen K blocks together form an invertible
   480s-by480s source-to-boundary map.
3. Each K tuple has total X-response rank30s; projection of its row space
   to the source coordinates of any j in S_K is injective.

These statements concern actual delivered information before final
decoding. Coding among different D inputs at K is already allowed.

## 2. Exact geometry and capacity facts

`screen.py` reconstructs the authenticated root table and original routes.
For both receivers it verifies28 K planes,360 early original-X visits and
480 late original-Y arrivals. Every K has exactly30 terminal fields in
total. For every foreign donor j, exactly sixteen of these K satisfy
j in S_K. Every other K has zero j response by proper-source nesting.

For receiver80 there are62 foreign donors and each S_K has size35 or36.
For receiver1 there are60 foreign donors and each S_K has size33 through36.
The full weighted capacities are exactly

    sum_(K in K(80)) 30 |S_K| = 62*480 = 29,760,
    sum_(K in K(1))  30 |S_K| = 60*480 = 28,800.

The source pins, every K label, its actual phase counts and its full native
source set are recorded in `output/SYSTEM-SCREEN.json`. Field extension
and body replication do not change these combinatorial facts.

## 3. Proof of saturation

Fix a foreign donor j and set all other source banks to zero. Every
proper influence of X_j on receiver i passes through the sixteen actual
tuples indexed by K with j in S_K. Stacking them gives a linear map

    C_j:F^(480s) -> F^(16*30s)=F^(480s).

Any final decoder factors B_ij through C_j. Since B_ij is invertible,
rank C_j=480s. Thus C_j is square and invertible. Its480s rows are
independent; each consecutive30s-row block has rank30s. This proves1
and2. The rank of each complete K tuple is at least its rank on donor j,
namely30s, and cannot exceed its30s coordinates, proving3.

In particular, for any nonzero row a in F^(1 by30s), a C_(i,K,j) is
nonzero for every j in S_K. This is exactly the asserted injectivity of
restriction to any one supported native donor.

## 4. A retained sparse packet cannot be completed inside the same cut

Suppose a proposed partial code fixes a nonzero linear combination a of
the thirty-s actual K packet coordinates and its response to some native
j in S_K is zero. Any completion that retains that packet row, the same
thirty-s terminal capacity and the proper support has

    a C_(i,K,j)=0,  a!=0,

so rank C_(i,K,j)<30s. It cannot have an invertible B_ij. Changing the
remaining rows, adding local computation, or applying an invertible
change of basis to the same packet tuple does not remove this kernel.
The offending packet's donor response itself must change, or the
interface/capacity must change.

In the five-tile word, the actual late K370 aggregate is one of receiver1's
thirty terminal fields. It has no response to native donors15,69,70,92,107,
although all five belong to S_370. Its coefficient row is a nonzero
physical coordinate selector. Therefore it cannot be retained unchanged
in a full-rank receiver1 completion under this atlas. This is a rigorous
scope-limited obstruction, not an impossibility claim for K aggregation.
The next construction must add the missing donor dependence to this row
and check its compatibility with both receiver targets and all-source
mask cancellation. The other retained K rows require the same gate.
