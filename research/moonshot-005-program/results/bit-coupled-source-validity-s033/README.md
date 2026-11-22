# Source-valid t=26 coupled source/D specialization

The original S032 t=1 fixed extension fails four complete source views.
The explicit t=26 specialization preserves all693 geometric/639 native source
views, all11 actual early bases, strict nonsaturation, all72 geometric/67 native
whole H interfaces and all44 retained whole D identity readouts. It is an
actual source-valid member of the coupled family, with a priced local physical
implementation. No fifth receiver, complete supplier or new κ.

Read [PROOF.md](PROOF.md) for the full proposition, its scope, uniform extension
argument, exact cost accounting and open next questions. `CANDIDATE.json.gz`
contains the exact changed D and source coefficients. `output/` records every
source view, all2268 changed-source propagation ranks, full H/D interfaces,
four explicit t=1 collisions and compiler receipts.

From the repository root:

```sh
python3 -B research/moonshot-005-program/results/bit-coupled-source-validity-s033/reproduce.py --repo . --out /tmp/s033-source-valid-t26
```

Expected: `PASS_SOURCE_VALID_T26_COUPLED_LOCAL_CONSTRUCTION`. It reconstructs
the exact candidate, checks full sources and interfaces, runs collision and
mutation controls, and compiles/replays the changed source/D words. It writes
only to the requested output directory. `--skip-compile` omits the binary
compiler replay and labels that omission explicitly.

The gross local bill is454510288 ADD,279648 INIT/CLEAR each and16 gap6 field
exports. The whole-system invoice, global restoration and both strict
suppliers remain open. All five foundational assumptions remain explicit.

@CubeJerry with substantial OpenAI assistance. Apache-2.0. Predecessor credit
and independent-review boundaries are in the proof and programme admission.

## Full-gauge implementations and independent review

[GLOBAL-GAUGE-REVIEW.md](GLOBAL-GAUGE-REVIEW.md) reviews the separate
`bit-global-gauge-lift-s033` theorem and binds both overlap realizations to
actual source and D implementations. Their unchanged H costs are explicitly
reused; every source phase is freshly compiled for each realization.

| Local realization | Gross ADD bill | Increase over S032 | Extra field exports |
| --- | ---: | ---: | ---: |
| t=26 fixed extension | 454510288 | 572680 | 16 |
| Two-overlap q4 gauge | 454470648 | 533040 | 16 |
| Three-overlap q4 gauge | 454540232 | 602624 | 16 |

Each retains279648 INIT/CLEAR operations and gap6 exports. These are local
replacement bills; none is a complete supplier invoice or a κ improvement.
The three-overlap case has stronger geometry but a slightly greater local cost.

For either gauge subdirectory, compile its saved literal candidate and
independently review its full source-gauge binding:

```sh
python3 -B research/moonshot-005-program/results/bit-coupled-source-validity-s033/compile.py --repo . --candidate research/moonshot-005-program/results/bit-coupled-source-validity-s033/global-gauge-three-overlap/CANDIDATE.json.gz --out /tmp/s033-three-overlap-compile
python3 -B research/moonshot-005-program/results/bit-coupled-source-validity-s033/review_global_gauge.py --repo . --gauges research/moonshot-005-program/results/bit-coupled-source-validity-s033/global-gauge-three-overlap/GAUGES.json.gz --candidate research/moonshot-005-program/results/bit-coupled-source-validity-s033/global-gauge-three-overlap/CANDIDATE.json.gz --out /tmp/s033-three-overlap-source-review
```

`materialize_gauges.py` rebuilds the protected source corrections from any
saved full gauge certificate. The exact mathematical fields of the result
are `D_matrix` and `source_protected_delta`; the descriptive `kind` value does
not enter the mathematics or compiler.
