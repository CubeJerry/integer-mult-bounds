# Independent review of mixed retained swap records

**The proposed algebraic criterion is correct over any field. Physical record availability and raw-return prices remain separate obligations.**

This reviews the root worker's stated proposition; no formal author draft hash had yet been supplied when this review was written. The independent controls are `check_mixed_swap.py` and `MIXED-SWAP-REVIEW.json`.

## Exact interface and identities

Let k chronological swaps have actual differences delta satisfying

    T delta=q-Hu,    T=I+L,
    Y=Wu+Z delta.

Each original raw donor q_i must still hold its original value when its swap occurs. The displaced pre-swap value is retained in its donor carrier, so the actual retained vector is

    R=q-delta=L delta+Hu.

All components of R and Y are available at the decoder at the stated versions. They must not be treated as separately supplied common records Nu. Choose H=Lambda W+Gamma N with [W;N] row-independent, but do not supply Nu. Define

    B=Lambda Z-L,
    K a row basis of the left nullspace of Gamma,
    C=KB.

Substituting Wu=Y-Z delta gives

    R=Lambda Y-B delta+Gamma Nu,
    C delta=K(Lambda Y-R).                             (1)

Thus the observed mixed records supply exactly the displayed delta combinations. Additional actual raw returns Aq supply

    A delta=Aq-AR.                                    (2)

## Recovery criterion, necessity sign and optimal count

Full recovery of Wu and every q_i is equivalent to

    rank([C;A])=k.                                    (3)

Sufficiency follows by solving delta from (1)-(2), then Wu=Y-Z delta and q=R+delta.

For necessity, choose a nonzero t in ker C intersect ker A. Since KBt=0 and K spans the left annihilator of Gamma, there exists eta with

    Gamma eta=B t.

Row independence gives a common displacement v with Wv=-Zt and Nv=eta. Set dq=t. The actual difference change is t because

    dq-Hv=t+Lambda Zt-Gamma eta
         =t+Lambda Zt-(Lambda Z-L)t
         =(I+L)t=Tt.

Both observed Y and R remain unchanged, and A dq=0. The wanted raw vector changes by the nonzero t. This excludes arbitrary decoders of the stated linear data. The sign of eta is positive in Gamma eta=B t; replacing it with -B t does not give this ambiguity.

Every additional row adds at most one rank, so the sharp return dimension is k-rank(C). Standard coordinate rows extending row(C) attain it. In particular mixtures of original raw coordinates cannot improve the minimum number of returns, though they may change their acquisition and transport costs. A coordinate q_i can be captured while its actual swapped helper holds q_i only if the source word supplies the required cache/lifetime and route.

## Intrinsic rank form

The result does not depend on a particular hidden-complement basis. The identity

    rank(KB)=rank([Gamma B])-rank(Gamma)

follows by quotienting the image of [Gamma B] by the image of Gamma. Hence

    min returns = rank(Gamma) + k-rank([Gamma B])
                >= rank(Gamma)
                 = rank([W;H])-rank(W).

The final equality uses the independence of [W;N]. Thus the raw-return requirement splits into the common payload rank outside the hub target space and any further degeneracy of the chronology/response matrix. This is a rank statement, not an additive paid-call lower bound across separately modeled swap families.

Equivalently, the known rows C arise from combinations a of swap equations whose baseline payload aH lies in row(W). For such a, aGamma=0, and aLambda is the unique coefficient row representing aH through independent W. The corresponding observable difference row is aLambda Z-aL. This description makes complement independence explicit.

## Independent controls and scope

The checker constructs the observation and target matrices directly in the independent original inputs (u,q), rather than implementing the claimed decoder. For48 exact rational instances it checks every coordinate-return subset, compares the full observation-row condition with (3), verifies optimal coordinates and tests additional arbitrary linear return matrices. It also constructs129 explicit indistinguishable input pairs using the necessity formula.

Directed controls distinguish the hub-recoverable single swap, requiring no new raw return, from a single swap whose displaced payload lies outside the hub row space, requiring one. They reject replacing Lambda Z-L by Lambda Z+L: one fixture would then falsely claim zero returns where one is necessary. A separate control rejects the wrong eta sign. Finally, W=N=[1], Lambda=0, Gamma=[1], Z=[1] gives Y=q,R=u and shows why common-row independence cannot simply be dropped from the unqualified criterion.

No source-specific joint swap family has been supplied by this algebra. All actual swap cuts, chronological L entries, common response Z, availability of every R_i, receiver effects, guards, common endpoints, raw caller duties, return routes, scalar services and complete costs remain to be authenticated. In particular, a retained R_i cannot be cleared or overwritten before its uses in (1)-(2).

Prepared by an independent review worker with substantial OpenAI assistance. The mixed-record proposition belongs to the root worker; the prior difference-carrier, joint-restoration and retained-difference theorem lineage is preserved.
