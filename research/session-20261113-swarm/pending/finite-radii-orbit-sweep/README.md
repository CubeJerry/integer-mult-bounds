# Bounded W(D4) orbit-flow sweep

This package records exact finite matching evidence for (U=H_4/2), error
cap one, on only the Gaussian integer balls (S_R) with (R=6,7,9,11).
The script constructs sorted-absolute-coordinate/product-sign orbit
representatives and their exact (W(D_4)) capacities; it never enumerates all
points and then applies 192 group elements.

## Results

| Radius | Tested threshold | Threshold feasible? | Exact finite optimum | Strict lower-cut deficit |
|---:|---|:---:|---|---:|
| 6 | (sqrt{21}-sqrt{19}) (inherited (eta_2)) | no | (sqrt{31}-sqrt{28}) | 32 |
| 7 | (sqrt{43}-sqrt{39}) ((eta_3)) | yes | (sqrt{31}-sqrt{28}) | 32 |
| 9 | (sqrt{73}-sqrt{67}) ((eta_4)) | yes | (sqrt{78}-sqrt{73}) | 64 |
| 11 | (sqrt{111}-sqrt{103}) ((eta_5)) | yes | (sqrt{78}-sqrt{73}) | 64 |

The exact orbit-flow and Hall-cut receipts, including every orbit capacity,
positive quotient flow, and complete cut neighborhood, are in
[`RESULT.json`](RESULT.json). A quotient matching lifts to a full finite
injection by distributing each orbit-pair flow uniformly over its
biregular edge set and applying Hall's theorem; the proof is in
[`PROOF.md`](PROOF.md).

## Replay

From this directory, run:

```sh
python3 -B sweep.py > RESULT.json
python3 -B verify.py
python3 -O -B verify.py
```

`verify.py` checks flow conservation, orbit capacities, target and optimum
cuts, exact complete neighborhoods, and two deliberately corrupted
certificates. Its default behavior reads the saved receipt and emits a
summary; the sweep itself is deterministic and the result is byte-identical
under normal and optimized Python execution.

No PR is proposed from these bounded radius checks alone. The results are
finite evidence only and do not establish a pattern for other radii or a
global construction.
