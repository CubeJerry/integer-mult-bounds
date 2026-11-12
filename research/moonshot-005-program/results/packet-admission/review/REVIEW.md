# Independent review of stacked packet admission and exact-gain corollaries

**Accepted as conditional linear-interface theorems. No source sufficiency or
new κ is established by these matrix statements.**

I independently checked `PROOF.md` and `COROLLARIES.md`. Their quantifiers are
essential: finite-dimensional spaces over a fixed characteristic-zero field,
independent unrestricted common and private input vectors, fixed linear packet
maps, and the stated physical availability contracts. A field-rank argument is
not an integer residue-encoding or general bit-complexity lower bound.

## Main criterion

The chronological scaled encoder must use

\[
 T=\operatorname{diag}(1/g_i)+L,
 \quad J=Z_oT^{-1}D,
 \quad K=-VJ.
\]

With the fixed pre-correction target cache `b=Hu+Dq`, actual increments satisfy
`TΔ=Dq−HKq`. The assumed identity `HV=0` makes this precisely `Δ=T^{-1}Dq`.
The offhub right-inverse property then cancels the common endpoint error:
`F_oK+Z_oT^{-1}D=−J+J=0`.

Because snapshots are taken after correction, the historical output is

\[
 Au-A VJq+B T^{-1}Dq.
\]

Thus the required raw initial correction is exactly

\[
 E=R-BT^{-1}D+A VJ.
\]

The plus sign on `AVJ` is necessary. Omitting that term is justified only when
its actual product is zero; the convenient sufficient condition `AV=0` is
explicitly distinguished in the author theorem.

For the prescribed corrections, `K=-VJ` and `F_oK=-J` imply both row-space
inclusions, hence `row(K)=row(J)`. It follows that

\[
 \operatorname{row}[K;E]=\operatorname{row}[J;E].
\]

Both corrections can be recovered from packets `Cq` exactly when this space
lies in `row(C)`. Necessity is robust to nonlinear local decoding of those
linear observations: a missing row direction produces two private vectors with
the same `Cq` but different required corrections. Common or local data that are
independent of q can be fixed equal in this argument. Additional q-dependent
local information must instead be included explicitly; it changes the test.
Sufficiency is constructive by row combinations. A row basis realizes the
minimum `rank([J;E])` within this fixed interface.

## Corollaries

If `row(J)=row(D)`, then `E−R` has rows in that same space. Therefore
`row([J;E])=row([D;R])`. Injectivity of Z_o on `im(T^{-1}D)` is a valid
sufficient condition, since it gives `ker(J)=ker(D)`. If R has full column
rank m, the packet minimum is exactly m. The source-specific unit-17 claim uses
the separately admitted independent rank-17 debt result; it is not a newly
replayed source computation in this review.

For invertible square R, put `G=R^{-1}BT^{-1}D`. On `ker J`, the AVJ term
vanishes. Thus

\[
 \ker[J;E]=\ker J\cap\ker(I-G),\qquad
 \operatorname{rank}[J;E]=m-\dim(\ker J\cap\ker(I-G)).
\]

The formula does not require AV=0. For a full 104-coordinate first-Y target it
requires an exact-gain, zero-debt subspace of dimension at least 94 for ten
packets, or 96 for eight. These are exact algebraic conditions inside the
stated interface, with all physical and budget obligations still separate.
They must be adjusted when additional directly delivered donor information or
a different target dimension is granted.

## Meaningful checks and remaining contracts

The independently written rational checker gives a two-control example with
nontrivial chronology, gain two, and nonzero AVJ. It verifies complete offhub
restoration and the desired decoder output, then shows failure when AVJ is
omitted. Further explicit examples demonstrate failure of `Δ=T^{-1}Dq` when
HV is nonzero, ambiguity from one missing packet direction, the effect of
extra q-dependent side information, and a nonzero COPY guard despite terminal
offhub cancellation. A two-dimensional exact-gain example verifies the kernel
corollary. These controls illustrate hypotheses; the universal proofs are the
row-space and rank-nullity arguments above.

The guard equation, literal local access, cached b values, fixed pre-correction
V, chronological snapshots, retained original q, receiver route use, raw
restoration and scalar/precision services remain explicit premises. Forming a
packet basis algebraically does not pay for routing or erase owned records.
Rank does not determine ordinary-operation counts, rational denominator cost,
precision growth, peak ownership, or recursive savings. This review admits no
numerical H4 budget assertion beyond the separate source/invoice packages.

`REVIEWED-FILES.json` pins the author's unchanged proof and corollaries plus
this review and its independently written exact controls.

```sh
python check.py --output /tmp/packet-admission-controls.json
```

Expected status: `PASS_INDEPENDENT_PACKET_INTERFACE_CONTROLS`.
