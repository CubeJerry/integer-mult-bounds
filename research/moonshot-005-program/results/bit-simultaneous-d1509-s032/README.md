# Four simultaneous whole D1509 receiver cuts

S032 changes the actual source maps to serve native receivers **6, 9, 48, 73** simultaneously at D1509 on all eleven native donors. It preserves both whole H263/H642 interfaces and literal H/D words. Each common entire fibre has dimension 8 per 480-field source, or 64 at bank 3840. The fixed source/H diagram has a sharp maximum of four receivers under independent invertible source input changes: all 462 five-receiver subsets have unequal donor join ranks.

Read [PROOF.md](PROOF.md) for the exact hypotheses, constrained extension lemma, local accounting and next source-edit obligation. This is a local source/H/D theorem and scoped sharpness result, not a completed supplier or new κ.

## Reproduce

From the repository root:

```sh
python3 -B research/moonshot-005-program/results/bit-simultaneous-d1509-s032/verify.py --repo . --out /tmp/s032-four-receiver-verify
```

Expected:

```text
PASS_FOUR_RECEIVER_D1509_AND_SHARP_FIXED_INPUT_GAUGE_GATE 4 11 132 462
```

The author checker authenticates predecessor pins, 132 proper restrictions, eleven gauges, materialized source/early/late compositions, whole paired H preservation, unchanged H/D data, every five-subset and three negative controls. The separate package `../bit-simultaneous-d1509-s032-independent/` independently reconstructs physical atlas interfaces and finite certificates.

Recompile actual source/H/D phase words and cache operations:

```sh
python3 -B research/moonshot-005-program/results/bit-shared-h-s031-construction/native-d1509-all-native/compile_prefix.py --repo . --package research/moonshot-005-program/results/bit-simultaneous-d1509-s032 --out /tmp/s032-four-receiver-compile
```

Expected final counts: **453937608 ADD, 279648 INIT/CLEAR each, 16 gap-6 field exports**. These are gross local replacement costs for eight lanes, with pure phase inverses. Global inverse placement and full supplier invoice remain open.

## Evidence

- `output/FRAMES.json.gz`, `PROPER.json.gz`, `READOUTS.json.gz`: owner-bound inverse restrictions for twelve geometric receivers and eleven native donors.
- `output/CONSTRAINED-GAUGES.json.gz`: common four-receiver frame, H cores, fixed spaces and actual input maps.
- `output/SOURCES.json.gz`, `EARLY.json.gz`: changed physical source maps, phase frames, late parities and actual early owner matrices.
- `output/H-PHYSICAL.json.gz`, `D-WORD.json.gz`: unchanged predecessor H/D data.
- `output/FIVE-RECEIVER-CENSUS.json`: all 462 native rank mismatches. Smaller-set exploration is in `CENSUS.json`.
- `output/PHASE-COMPILER-RECEIPTS.json.gz`, `COMPILER-RESULT.json`: actual binary words and full local inventory.
- `verification/VERIFY-RESULT.json`: fresh author verification.
- `SOURCE-PINS.json`: immutable predecessor dependencies.

`explore.py`, `protected_gauge.py`, `solve_gauges.py`, `build.py` and `five_receiver_gate.py` preserve the construction path. Their finite searches imply no impossibility outside the fixed diagram. Decompressed gzip payload equality is mathematical; byte hashes additionally identify committed containers.

## Open next questions

Change the source quotient/H-map diagram so its joined-fibre dimensions can agree, while retaining whole H interfaces and source validity. Complete remaining D receivers, other sources, H/D/K/facet maps, global restoration and affordable return before admission of either strict supplier. All five foundations remain explicit.

@CubeJerry with substantial OpenAI assistance. Predecessor and independent-review credits are in the proof. Apache-2.0.
