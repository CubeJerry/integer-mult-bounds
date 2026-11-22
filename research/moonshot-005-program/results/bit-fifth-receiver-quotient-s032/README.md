# The receiver95 source-edit obstruction

Arbitrary independent linear source-quotient changes cannot add receiver95 while retaining the S032 literal whole H263/H642 and four D1509 interfaces and freezing the physical H/D words. This is a source-only obstruction beyond the preceding independent-input-change ceiling. It is not an obstruction to a coupled source/H/D redesign or to every possible fifth receiver.

[PROOF.md](PROOF.md) states the exact domain and argument. `WITNESS.json` supplies one nonzero vector, sixteen local native-H/D decompositions and two unequal owner-bound readouts. It uses only native H receiver constraints.

From the repository root:

```sh
python3 -B research/moonshot-005-program/results/bit-fifth-receiver-quotient-s032/check.py --repo . --out /tmp/s032-fifth-source-edit
```

Expected: `PASS_RECEIVER95_FROZEN_H_D_SOURCE_EDIT_OBSTRUCTION 16 4`.

The checker reconstructs the actual source/H/D response of the vector, checks all sixteen prescribed subspaces, zero off-D response at donor61, both different readouts, real D parent incidence, and mutation controls. The separate sibling `../bit-fifth-receiver-quotient-s032-independent/` supplies independent evidence.

`forced_collision.py` retains the construction and exact finite screen. Earlier exploratory visibility screens are isolated under `exploration/`; they are not needed for the theorem. `SOURCE-PINS.json` binds the four-receiver and predecessor sources. Generated compressed payload identity is compared after decompression where relevant.

## Open next question

Construct a simultaneous source/H/D change that repairs the displayed receiver95 readout mismatch while retaining four complete receiver cuts, full source validity and nonsaturation. Physical phase invertibility, source costs, global return and both strict suppliers remain open. No new complete κ.

@CubeJerry with substantial OpenAI assistance. Attribution and scope are in the proof. Apache-2.0.
