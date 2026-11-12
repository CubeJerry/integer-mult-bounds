# Independent review: physical unit17 precompensation word

**Decision: accepted within the stated partial-construction scope. No new kappa and no saving over direct17-channel delivery.**

The reviewer imported no author code. `review.py` independently interprets the frozen 80,774-instruction word over all 1880 formal input variables, reconstructs the expected native endpoint map from the source port/main data, and checks every final symbolic row and chart.

Pinned native compressed SHA256: `2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883`. Reviewed word compressed SHA256: `c75f595393d32f0ddefed906e9dab02e6e09b764730684541375d6979c6c349c`; decompressed payload SHA256: `ee6a4bb6c9e9873a518f84ab8e007851e43bd770c11d01b1e3e2ea96f1b5c901`.

## Verified content

The full 1480-input first-copy common computation returns exactly the original native map F(u). Exactly 17 second-copy Y fields become vY+vX; the other 383 second-copy input values remain unchanged. All 1880 public fields end at their specified native final charts. These are complete symbolic identities over characteristic zero, hence apply to every positive field volume under the retained chart contracts; they are not numerical input tests.

All 71,261 original native instructions occur in their original order after the required owned-label remapping. The 1,710 original main MOVE reservations are used exactly once each, with the correct logical role, physical field, source chart and target chart. The only additional MOVEs are 17 owned rank1 moves from donor lines to empty chart3. At each such move the actual formal payload is exactly q_j=v_j−u_j for the declared donor. This verifies physical information acquisition, not merely an oracle for a debt packet.

The interpreter checks active labels, INIT freshness, owned-only CLEAR, cochart scalar operations, nonzero SCALE, nested MOVE direction and ownership flags, and the actual zero target of the sole native COPY. Peak live owned storage is 121 fields; all owned lifetimes close. There are 8,037 MOVEs total: 6,310 common, 1,710 funded raw, 17 new.

The functional negative control deletes one nonzero raw initial gain correction and detects a wrong final output row. A separate negative control duplicates a claimed funded reservation and is rejected by the source-lineage audit. Normal and optimized runs use explicit exceptions and must reproduce the same receipt.

## Limits and assumptions

This is a real restored partial word, not a complete second-copy supplier. It completes 17 of 208 required cross dependencies; 191 remain. Its 17 new rank1 calls match the direct information price for those17 channels, so the result does not establish a price improvement. The 1,710 raw reservations are already consumed in this partial word and cannot be spent again in its continuation.

The review establishes exact rational typed-word correctness. It does not discharge scalar-admission/precision costs: the word contains non-dyadic rational coefficients inherited from the source and historical decoders. It also does not discharge the native, erasure, compiler, precision or analytic-recovery foundations. Ordinary operation and owned-storage counts are retained in the receipt; no zero-cost implementation is assumed.

Reproduce using `python review.py --source /path/to/final.json.gz --word /path/to/WORD.json.gz --output RESULT.json`, then the same command with `python -O`. The reader should compare `RESULT.json` and `RESULT-OPTIMIZED.json`.

Independent review prepared for @CubeJerry with OpenAI assistance. Credit the source authors, the programme's historical observation packages and the bridge worker's actual-value/precompensation construction.
