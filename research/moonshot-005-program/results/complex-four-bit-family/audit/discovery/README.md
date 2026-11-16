# Bounded caller discovery archive

This is finite exploratory evidence, separate from all proved source, trace and obstruction claims. Read `SCOPE.json` before interpreting any result. In particular, the script samples three modular nullspace vectors per linear system; it does not exhaust the invertible locus, prove a complex unit criterion, or construct an all-width caller.

The current final script and its shared prefix are preserved byte for byte. A small relocation wrapper substitutes only the recorded checkout path and keeps the options and algebra unchanged. From the repository root, the three finite modes are:

```sh
python <this directory>/replay.py --repo . --profile 421 --sourcegauges --coupled --orientation 010
python <this directory>/replay.py --repo . --profile 421 --sourcegauges --coupled --orientation 010 --loose
python <this directory>/replay.py --repo . --profile 421 --sourcegauges --coupled --orientation 010 --mixed
```

Each run took approximately four minutes in the original environment. The first two recorded no sampled modular units under their row restrictions. The mixed mode retained 92 sampled modular units, none with the desired width-one component-rank census. The final script's optional loose-mode flag was added after the other runs, and their start-of-run script bytes were not pinned; this archive therefore preserves the exact observed output files and a fully specified final generator, without claiming an independently reproduced historic script version.

No additional full run was launched during protected review. `replay.py --repo . --help` checks relocation and option loading without launching the scan. Exact path products, field `65537`, quarter phase `256`, width residue `1`, basis tables, first-interstage templates and random seed are given in `SCOPE.json` and the script. The compact mixed census omits candidate vectors that have no proved endpoint interpretation; the deterministic generator can reproduce them.
