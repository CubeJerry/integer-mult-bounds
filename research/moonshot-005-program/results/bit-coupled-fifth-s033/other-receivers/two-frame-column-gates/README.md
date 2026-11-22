# Common-readout column obstructions for receivers54 and74

The two-frame targets54 and74 are excluded under fixed literal H actions/owners and the four retained common frame spaces, allowing arbitrary common invertible readout changes at the retained receivers and arbitrary full linear source recodings. No phase assumption or consistency between shared D output rows is used in the final column contradiction. Target87 survives this particular necessary-condition test.

## Normalization from fixed H observations

Let L_r be a retained frame. At source0, the two-column profile X_r=L_r T_old[O_r,{4,5}] lies in the native H observation span at each of the four D parents. The checker saves all sixteen exact decompositions, for all four retained receivers. The old D ingress on X_r is the coordinate inclusion of inputs4 and5. Fixed H observations preserve this ingress even under full source edits. If the common retained readout is an invertible Q_r, then

T'[O_r,{4,5}] = Q_r T_old[O_r,{4,5}].

Therefore A_r=Q_r^(-1) T'[O_r,:] has the old fixed columns4,5. The source0 physical ingress identity is also checked in the independent rebased receiver54 review; its normalization applies to every retained r.

## Tight parent kernels imply column dependencies

For an anchored forced K=L W with two nonzero blocks, suppose a donor has joint parent off-target kernel dimension4 and each block kernel dimension2. The joint kernel is their direct sum. For each active retained r, isolation then implies

A_r[:,I_j] V_jr is contained in im W_r,

where V_jr=S_old,jr^(-1) ker(M_jr). If a coordinate unit at p lies in V_jr, column A_r[:,p] must lie in im W_r. The checker verifies that im W_r=span(A_r[:,4],A_r[:,5]) using the fixed normalization and exact profile factors. Any donor input set containing4,5,p then yields a singular retained section.

For receiver54, one small witness is tight donor32, retained receiver9, dependent column22, and violated section donor0. Receiver48 gives another witness. For receiver74, a small witness is tight donor38, retained receiver6, dependent column19, and violated section donor0. Receiver73 gives another witness. Exact kernel coefficients and all matrices are saved; the checker records16 coordinate witnesses for54 and20 for74. A single witness for either target suffices.

## What remains for receiver87

Receiver87 uses retained frames9 and73. For each of those frames, the sum of every tight-donor embedded input kernel is exactly the coordinate subspace on

{2,4,5,14,16,17,27,31}.

Its dimension is8, but each native donor input section intersects it in dimension exactly2. Mapping this entire subspace into the fixed two-plane therefore does not force a retained section singular by this test. The checker stores the exact union bases and eleven intersection dimensions for each frame. This is a specific surviving interface condition, not an existence theorem, determinant-feasibility result, full source realization or whole fifth receiver.

The next receiver87 design must arrange that both normalized retained row blocks map those eight input coordinates into their fixed two-plane while keeping every native section invertible, respecting shared actual rows and physical phases, and supplying a common whole target fibre. The old five-fibre joined-span obstruction still excludes a solution obtained solely by invertible source gauges preserving the old arrangement.

## Replay

```sh
python research/moonshot-005-program/results/bit-coupled-fifth-s033/other-receivers/two-frame-column-gates/check.py --repo . --out /tmp/s033-column-gates
```

SOURCE-PINS.json authenticates the inputs. output/CERTIFICATE.json.gz contains the target gates and H decompositions. No new kappa or compiler invoice is claimed.

Authorship: @CubeJerry, with substantial OpenAI assistance. Apache-2.0.
