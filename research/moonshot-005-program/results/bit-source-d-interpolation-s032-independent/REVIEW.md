# Independent source/D interpolation review

Session `2026-11-22-S032`. The exact local interpolation reduction and the recorded bounded screen are accepted. The screen is not a general impossibility result.

## Actual family and reconstructed matrices

The allowed source changes replace only six protected rows of each selected paired source quotient, on the 96 protected source coordinates. There are four actual D1509 parent quotients for each of eleven native donors: **44 independent local systems**. All remaining source coefficients, physical H maps, ownership, the four common source frames, and the native retained H interfaces are fixed.

The independent checker reconstructs the donor/receiver sets from integer root orthogonality and the actual A2/D4 incidence. It obtains each local six-by-six H-to-proper map directly from the literal source local frame, physical early/late/cross H matrices and raw owner routes. It uses the canonical selected-D allocation. It does not import the new author executable or its saved `PROPER` matrices.

The native H constraint spaces come from the earlier independently reconstructed whole protected H fibres, retaining receivers below 111 only. The checker verifies that the four-receiver gauges fix these generators pointwise, so the inherited H vectors are in the correct current source coordinates. All **176** local six-by-six maps (44 systems times four receivers) are invertible. Their output-owner ordering is explicitly retained in the receipt.

## Exact criterion and orientation

For donor \(j\), source quotient \(h\), and retained receiver \(r\), let \(B_{jhr}\) map the six protected quotient values to the six proper H outputs visible at \(r\). Let \(E_{jhr}\) place the relevant D1509 input coordinates into those six output-owner positions. For a proposed physical D word \(T'\), its actual eight-by-eight section is

\[
C'_{jr}=T'[O_r,I_j].
\]

Assume these retained sections are invertible. Whole isolation plus the literal identity D readout requires the local protected quotient map \(F'_{jh}\) to satisfy

\[
F'_{jh}L_r=B_{jhr}^{-1}E_{jhr}(C'_{jr})^{-1}.
\]

This orientation follows by first inverting the actual D readout section to prescribe ingress, then placing that ingress at the actual owner rows, then inverting the local H restriction. The independent checker reconstructs these maps without using the author's inversion-through-old-gauge calculation.

Let the columns of \(C_H\) span the literal native H source vectors whose quotient values must remain fixed. Set

\[
X=[C_H\;L_6\;L_9\;L_{48}\;L_{73}],
\]

and let \(Y\) concatenate the unchanged values \(F_{jh}C_H\) with the four required images above. A linear protected map \(F'_{jh}\) exists **if and only if**

\[
\ker X\subseteq\ker Y,
\qquad\text{equivalently}\qquad YN=0
\]

for a basis matrix \(N\) of \(\ker X\). Necessity follows from \(Y=F'_{jh}X\). For sufficiency, define the map on \(\operatorname{im}X\) by \(Xc\mapsto Yc\); the kernel condition makes this well-defined, and a linear map on a subspace extends to the 96-dimensional source space. Kernel **containment** is the appropriate criterion: these local maps are not required to be invertible gauges.

An explicit extension can preserve the old map on an arbitrary complementary choice. Put \(\Delta=Y-F_{jh}X\), choose independent columns \(Q\) of \(X\), and choose rows \(A\) making \(X[A,Q]\) invertible. Set the change to zero outside columns \(A\), and set

\[
D[:,A]=\Delta[:,Q]X[A,Q]^{-1},\qquad F'_{jh}=F_{jh}+D.
\]

Then \(DX=\Delta\) by the same relation condition. This proves sufficiency for the specified interpolation equations. It does not prove full source-view ranks, source-phase legality, preservation of every other required circuit interface, a compiler invoice, or a common fifth whole fibre.

## Positive controls and bounded negative evidence

Two actual words pass all 44 independently reconstructed systems:

1. The original four-receiver D word.
2. The admitted six-free-row D word from `bit-d1509-coupled-repair-s032`.

In both cases the unchanged source map itself is an exact solution: \(Y=F_{jh}X\). Thus the checker accepts the known admitted D modification and does not impose an unintended freeze of every D output row.

The checker also verifies \(\operatorname{rank}L=32\). If the H constraints are removed, the interpolation domain is just \(L\) and its relation kernel is zero; arbitrary prescribed images on those 32 columns extend linearly. This identifies the role of the retained H constraints in the local equations, without asserting full source admissibility after releasing them.

The checker regenerates the exact deterministic list of 128 elementary output shears with coefficient one. Each is phase-legal, invertible as a 35-coordinate word, and changes an actual retained D section. It independently reproduces:

| Rejection | Number |
|---|---:|
| Singular retained eight-by-eight D section | 19 |
| Nonzero exact H/source interpolation relation | 109 |
| Feasible candidate in this list | 0 |

Every saved interpolation rejection is independently checked at its claimed donor/quotient, donor 0 and H116, including the exact nonzero residual rank. The singular-section checks independently reproduce the first failing section. The saved trial witnesses describe these 128 candidates only. They exclude neither different shear coefficients, longer words, general simultaneous D changes, nor source families outside the protected six-row edits.

## Evidence and reproduction

`SOURCE-PINS.json` binds the exact consumed artifacts. `output/RECONSTRUCTED-MATRICES.json.gz` saves the independently recovered source maps, native H spans, relation bases and target maps for all 44 systems. `output/TRIAL-WITNESSES.json` and `output/RESULT.json` save the bounded checks and both positive controls.

From the repository root:

```sh
python3 -B research/moonshot-005-program/results/bit-source-d-interpolation-s032-independent/check.py --out /tmp/s032-interpolation-independent
```

Expected status: `PASS_INDEPENDENT_SOURCE_D_INTERPOLATION_REDUCTION`. No new author executable is imported. The recorded arithmetic pass takes approximately four seconds in this environment.
