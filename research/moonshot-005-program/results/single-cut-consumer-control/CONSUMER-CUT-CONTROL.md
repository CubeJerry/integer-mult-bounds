# Single-cut consumer access is tight; global continuation is separate

## Proposition / negative control

Fix the pinned S010 native source (gzip SHA-256 `2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883`), a characteristic-zero field, and any whole-field volume `V>0`. Use the hosted orthogonal frame

`B = (5, 56, 65, 69, 77, 96, 100, 103)`.

The complete-target cut theorem gives `Z_B=B`, `|Z_B|=8`, and zero fixed outward credits for this cut. Therefore at least `8V` dimensions of additional private-innovative outward transport are required across `D_B`.

This one-cut demand can be met at an **actual target consumer** for exactly the same eight rank-one calls. For each `i in B`, let `D_i=d_i` be the restored original D field at its endpoint facet `F_i`, and let `B_i=b_i` be its authentic Hub row before the required correction. Create one owned lifetime `q_i` at `F_i`, perform `q_i += D_i`, make a new owned MOVE `F_i -> W` to the Hub, then perform `B_i -= q_i` and clear `q_i`. The Hub row is now the prescribed `b_i-d_i`; `D_i` itself was copied and remains restored at `F_i`.

The exact pinned-source check reconstructs `B`'s Gram block as `I_8`; the eight D endpoints are charts `(132,179,187,191,198,216,220,223)`, each dimension 8, and Hub is chart 127, dimension 9. Each `F_i -> 127` chart pair occurs in the native MOVE list. Every **new invocation** is still charged as a separate owned rank-one MOVE, so the added Gaussian price is exactly `8*1^(199/200)=8`. The local additions, eight INITs, eight clears, and lifetime/peak constraints remain ordinary/source accounting; they are not hidden in the MOVE price. This construction uses no pre-existing pure Gram Hub premise: it explicitly transports the needed `d_i` values to the actual B-row consumer.

Thus any strengthening that treats “this exit must eventually be consumed by an original target” as an automatic positive surcharge beyond the single-cut demand is false. For this cut, the complete-target lower bound is sharp even with actual Hub consumption and D-endpoint restoration.

## Negative controls and scope

A second independently reconstructed hosted orthogonal frame is `J'=(0,7,20,27,36,46,57,111)`, with `J'∩B=∅`. The same eight `F_i -> W` messages contribute zero to the `D_{J'}` cut: independent GF(2) span reconstruction verifies all 96 facet spaces are distinct, and none of the eight selected facets is contained in any `J'` facet. Since `D_{J'}` is the union of the chart downsets `↓F_j`, a chart `F_i` belongs to it exactly when `F_i⊆F_j` for at least one `j∈J'`; here that test fails for all eight sources. Thus these messages do not cross this cut, which still demands 8. The eight-message local construction is **not** a witness for the full family of cuts and not a complete network code. It is a negative control against overpromoting one-cut consumer contact.

The Gram calculation is exact over `Q`: each root inner product is divided by 8 as a rational number. A negative arithmetic control uses hosted roles `(0,1)`, whose root inner product is `+4`; their normalized inner product is `1/2`, while floor division by 8 would incorrectly return zero.

The LP edge `0 -> span(511)` still has no actual target at its endpoint; this note does not legalize it or prove the global consumer-constrained optimum. The result is static in the original source charts and rows. If a candidate changes current fitting rows or moves the target consumer, recompute the causal rank at those actual live versions. No shared/common transport is credited, and no existing raw MOVE occurrence is reused as free capacity; if a construction claims a funded occurrence, subtract only its genuinely remaining capacity at the specific time/version. The proposition leaves all other first-family outputs and the full 400-path restoration schedule open.

## Independent check

`consumer_cut_check.py --repo /path/to/programme` reads the pinned native payload, reconstructs the source E8 root vectors from the hosted role charts, checks both 8-by-8 Gram identities and disjointness, rejects the `+4` nonorthogonal pair control, verifies every D endpoint dimension and every native `F_i -> 127` chart-pair occurrence, and checks all 96 facet spans and the cross-frame noncontainment control. `consumer_cut_check.json` is its compact receipt. Checks use explicit exceptions and remain enabled under `python -O`. The algebra scales by `I_V`, so the result holds for every allowed positive volume, not only the scalar run.
