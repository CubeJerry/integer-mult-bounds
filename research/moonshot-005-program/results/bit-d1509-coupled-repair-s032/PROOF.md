# A legal D1509 witness repair and the remaining four-space obstruction

**Positive local D word plus a scoped exact rank gate. No complete fifth receiver, supplier, or new κ.**

This package follows the four-receiver S032 construction and receiver95 source-edit obstruction. It changes actual D1509 coefficients while keeping the source/H word fixed. One forced witness vector now has equal D readouts across all eleven native donors. The complete forced four-space still requires a changed source-to-D interface.

## 1. Actual ingress and retained interfaces

Let Pj be the actual 35-by-96 protected-source ingress matrix at D1509 for native donor j. These matrices are reconstructed from the changed S032 source coefficients, actual phase owners and complete H early/late/cross words. They include the effects of the explicitly saved original-early caches. Each has rank 8 and is supported on the eight real D inputs reached through the donor's four H parents.

Let Lr be the existing common eight-frame for r in R=(6,9,48,73), and Or its eight actual D output indices. The old D word T satisfies

    T[Or] Pj Lr = I8

for every j and r. We seek a new physical word T'=T+DeltaT with the same 19/16 early/late split. The upper-right 19-by-16 block must stay zero. Preserving the four existing readouts imposes exactly

    DeltaT[Or] Pj Lr = 0.

It does not impose zero change at every output of the full D packet. Such a stronger condition would unnecessarily forbid the intended changes at other receivers.

The exact homogeneous phase-legal matrix space has dimension 360. Receiver95 uses output rows 10,13,16,18,30,31,32,33. Rows10/30 occur at retained receivers48/73 and already have zero witness discrepancy. Rows13/16/18/31/32/33 occur at none of the four retained receivers. They carry every nonzero coordinate of the preceding source0/61 discrepancy.

## 2. A genuine phase-legal D repair

The first literal repair is rank one and cancels the old source0/61 witness discrepancy. It preserves both phase-block ranks and all geometric donor/receiver section ranks. A stronger deterministic construction chooses the six free output rows to give a common readout of the same nonzero vector v at all eleven native donors.

For this vector, the donor contrast matrix

    Zv = [(Pj-P61)v] for j != 61

has rank10 both on the first19 rows and on all35 rows. The three changed early rows are chosen in the nine-dimensional annihilator of the early contrast; the three changed late rows lie in the 25-dimensional annihilator of the full contrast. The literal seed1 matrix passes every required finite rank check. These coefficient choices are an exact certificate; no probabilistic existence premise is retained.

The resulting35-by35 matrix T' differs from T in exactly rows13,16,18,31,32,33 and has delta rank6. Its early and late diagonal blocks have ranks19 and16. All144 geometric D sections are invertible8-by8 matrices, including all121 native sections. Every one of the44 old donor/receiver identity readouts remains exact. The source/H word and all old proper inverse restrictions are unchanged, so the four old whole inverse fibres are retained.

At receiver95, all eleven donors now give v the same actual output

    (14,5,63,1,1,49,6,27).

This closes the displayed **one-vector readout discrepancy** under a changed physical D word. It does not make v isolated at the other donors: their off-D source/H responses are unchanged. It also does not align the whole eight-dimensional receiver95 fibres.

## 3. Chronological binary word and paid local cost

The new word is compiled on the same35 actual owners. Before early owners depart, their19 original fields are copied into the same114 stationary binary cache bits. The early block is applied to the114 early original bits, the late block to the96 late original bits, and the new cross block is added from those saved early originals. Direct symbolic evaluation checks every one of the210 original binary columns, including arbitrary late baselines.

The exact base-instance operation counts are:

| Component | ADD count |
| --- | ---: |
| Early block, per direction | 6,672 |
| Late block, per direction | 4,732 |
| Original-early cache copies | 114 |
| Late cross block from caches | 4,337 |
| Total including pure phase inverses | 27,259 |

The previous D total was26996, so this change adds263 ADDs per base instance and2104 over eight lanes. The gross eleven-source/280-H/one-D count becomes **453939712 ADDs**. INIT and dirty CLEAR remain279648 each; the16 gap6 field exports are unchanged; no MOVE is added. Pure phase inverse placement in the global restoration/preload schedule remains a separate dependency. This is a local replacement invoice, not a complete supplier price.

## 4. The whole forced four-space cannot be repaired at frozen ingress

Let K be the96-by4 forced collision frame from the receiver95 source-edit package. Its columns are independent and P61 K has rank4. Form

    Z = [(Pj-P61)K] for j != 61,       B = P61 K.

The exact35-by40 contrast matrix has rank30. Its row annihilator has dimension5. A basis N for that annihilator satisfies

    N Z = 0,
    rank(N B) = 2,
    rank([Z B]) = 32.

These are explicit finite matrix identities and ranks, independently checked.

For any linear D readout A, with any number of rows and with all phase constraints relaxed, equal donor readouts on all of K require A Z=0. Thus every row of A lies in the row span of N. Its common response A B can have rank at most2. It cannot be injective on the four-dimensional K.

This is an exact impossibility theorem for **frozen donor ingress on the whole forced K**, not a failed search. In particular, a D-only coefficient change cannot complete the required common four-space readout. The positive one-vector word does not contradict it: an injective readout of one vector requires only rank1.

The gate does not exclude jointly changing donor ingress, changing the forced subspace, changing isolation or other interfaces, or nonlinear D functions. It does not prove that any particular number of paid routes is needed.

## 5. A precise coordinate-change requirement

For arbitrary matrices Z and B with the same row labels, define

    q(Z,B) = rank([Z B]) - rank(Z).

This equals the rank of the common response induced by the annihilator of Z. If k coordinate-row positions are replaced in both matrices, q can increase by at most k.

To prove this, delete those k rows first. Re-adding one row increases the two ranks by either0 or1. If rank(Z) increases, the augmented rank also increases. Hence q increases by0 or1 per re-added row. Both the old and new q lie between the deleted-row value and that value+k, proving the claim.

Here q=32-30=2. If the same K is to have an injective rank4 common response, at least **two distinct actual D input coordinate positions** must change across the family of donor ingress functions. One arbitrary coordinate-row replacement cannot suffice. A single source or H edit could affect multiple such rows; this is not a lower bound of two new fields, calls, routes or MOVEs. Changing K or the prescribed isolation requirement leaves the corollary's scope.

## 6. Next construction

A complete receiver95 continuation requires source/H changes that alter the relevant ingress subspaces together with a compatible D word. Retuning only the six previously unused output rows repairs v but leaves the rank2 whole-K obstruction and off-D leakage. A next attempt should modify at least the needed ingress functions or redesign K while preserving the complete four existing receiver interfaces through a simultaneous source/D interpolation.

Every such change needs fresh source-view ranks, nonsaturation, whole-H checks, phase invertibility, owner/cache binding and cost accounting. The other native source stars, whole H interfaces, K/facet word, canonical return, both strict suppliers, full caller and all five foundations remain open. No new complete κ.

Credit @CubeJerry, the S031/S032 source/H/D constructions and independent reviewers, inherited atlas/geometry and compiler contributors. Substantial OpenAI assistance. Apache-2.0.
