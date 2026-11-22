# A bounded coupled D1509 repair

**A physical one-vector repair and an exact frozen-ingress rank gate. No complete fifth receiver or new κ.**

The saved 35-owner D1509 word changes six output rows and makes the forced receiver-95 witness vector have the same readout at all eleven native donors. It preserves the four existing whole receiver fibres for receivers 6, 9, 48 and 73, their identity readouts, the 19/16 early/late split, and all 144 geometric D section ranks. Source and H coefficients are unchanged.

The homogeneous space of phase-legal changes preserving the four actual readouts has dimension 360 over GF64. The saved matrix gives the common witness response `(14,5,63,1,1,49,6,27)`.

This is a necessary-interface repair. The witness still has off-D leakage at ten donors, and the donor-0/donor-61 receiver-95 whole fibres have join dimension 14. On the complete forced four-space, the unchanged donor ingress contrasts have rank 30, common-row dimension 5 and induced common-response rank 2. Thus no common linear D readout can be injective on that four-space at the frozen ingress, even with phase restrictions relaxed. With the same space and coordinate labels, at least two actual ingress coordinate functions must change to reach rank 4. This counts changed functions, not paid MOVEs or fields.

## Evidence and verification

[PROOF.md](PROOF.md) gives the construction, exact gate, support corollary and scope. The [independent review](../bit-d1509-coupled-repair-s032-independent/REVIEW.md) reconstructs the actual ingress maps, checks all retained whole fibres and geometric sections, and independently compiles the changed physical word. It imports no executable from the new author packages. Its saved result is [output/RESULT.json](../bit-d1509-coupled-repair-s032-independent/output/RESULT.json).

From the repository root:

```sh
python3 -B research/moonshot-005-program/results/bit-d1509-coupled-repair-s032-independent/check.py --out /tmp/s032-coupled-independent
```

Expected status: `PASS_INDEPENDENT_BOUNDED_COUPLED_D_REPAIR`.

Negative controls reject the unmodified D word as an all-donor witness repair and reject a mutation on an actually retained output row. `VERIFY-RECEIPT.json` binds the independent check and result. Inputs are pinned in `SOURCE-PINS.json`; this package's bytes and decompressed payload hashes are in `MANIFEST.json`.

## Literal data and generation

| File | Content |
| --- | --- |
| `DATA.json.gz`, `RESULT.json` | Actual ingress, homogeneous constraints and first rank-one pair repair |
| `ALL-DONOR-VECTOR.json` | Saved phase-legal matrix, inverse and section checks |
| `D-WORD.json.gz` | Actual owners, matrix and literal binary ADD lists |
| `COMPILER-RESULT.json` | Local compiler increment and inherited totals |
| `FULL-COLLISION-CERTIFICATE.json.gz` | Forced frame, contrasts, annihilator and common response |
| `FULL-COLLISION-GATE.json` | Exact rank-gate summary |

Generation order: `phase_freedom.py`, `all_donor_vector.py`, `full_collision_gate.py`, then `compile_d.py`, each run with the repository root as current directory. The scripts write beside themselves. To regenerate without changing frozen evidence, copy these four scripts into an empty temporary directory before running them; they continue reading predecessors from the repository root.

## Local price

The new D word costs 27,259 ADDs including pure phase inverses, compared with 26,996 previously. Across eight lanes this adds 2,104 ADDs, giving **453,939,712 ADDs** for the inherited eleven-source/280-H/one-D local word. INIT and dirty CLEAR remain **279,648 each**, and the **16 gap-six field exports** are unchanged. No new MOVE is introduced. The full supplier invoice, inverse placement and canonical return remain open.

## Open next questions

The next construction is simultaneous source/D interpolation that changes the relevant ingress functions or the forced fifth-receiver space while preserving the literal H interfaces and all four existing whole D fibres. A candidate needs fresh source ranks, nonsaturation, off-D isolation, retained readouts, chronology and costs. The present gate fixes ingress and the forced space; it is not a general source/H/D impossibility theorem.

Predecessors: S031 native D1509, S032 four-receiver construction and S032 receiver-95 quotient obstruction. Credit @CubeJerry, inherited geometry and compiler contributors, and independent reviewers. Substantial OpenAI assistance. Apache-2.0.
