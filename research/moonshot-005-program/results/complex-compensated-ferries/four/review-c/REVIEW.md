# Independent review: four funded cross pairs

## Result

I independently replayed the frozen rank-54 partial word on all 400 public input directions, checked its eight causal ferries and suffix transfers, independently checked all 23 new chart recipes including global phase, and replayed the three-copy lift on all 2,280 input directions with its complete pinned invoice. All checks passed. I found no correctness blocker in the construction or its stated scope.

The result is a partial source advance. It preserves the parent's first-X, first-Y, and D outputs, all 24 already completed reverse outputs, and the 4,920 original-coordinate first-Y debt. It lowers the reverse residual rank from 58 to 54 by four exact dependencies. It does not finish either source endpoint or establish a complete kappa supplier.

## Immutable source pins

| Object | SHA256 |
| --- | --- |
| Author manifest | `a5310b300948784844ebca3bf6d55bc2fb44a9e04da937f0d2ae044b061469d5` |
| Candidate word | `20a5c2c3eccd000b757f65e2cd6bed7f8a9ec39f0b8f88a66716e4b818a2521f` |
| Parent Q | `a235a7e58f9eb96c6d409a88095fd6b59c977977baabb8735c76b2b820dcbedc` |
| Native 1,880-input source | `2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883` |
| Three-copy word | `3df717ae5d6081ed8c19de677751426597b26473169a8f072f92aac22f39a741` |
| Three-copy caller result | `d9ba709fa5dcefffe3f3abdcf34600ce188224703cfd743e6db8b58ba4816cb7` |
| 23-map chart certificate | `b9ab7c0384f0e4a48d4ee9ed609ae981f76585a90bed7cdced90735d8ae596d2` |

The 400-direction and m=3 replays use the separately written Worker C exact `Fraction` interpreter. The m=3 replay independently composes the pinned native common source with two literal private copies, checks all common and private final maps, checks all final charts, then recomputes the integer T/P invoice and its rational 199/200 movement-moment enclosure. The phase checker reconstructs frame circuits itself; it does not import the author's compiler or map checker.

## Causal and endpoint checks

The four undirected port pairs are `(1,106)`, `(2,4)`, `(11,15)`, and `(23,24)`. Their directed handoffs use eight actual original Gram fields and eight D donors. I re-extracted each parent's eight packet encoder/decoder maps from the operation stream and checked them against the packet records. The candidate's 520-term Y precode is exactly the sum of the eight negative decoder-weighted D contributions. Each D donor has one source use in the parent: its literal MOVE to its selected facet. The candidate preserves and hoists each of those eight MOVE events.

Each packet handoff follows the actual nested route `Hub -> D facet -> recipient B line -> Hub`, adds the unchanged D donor at its facet, uses the stated pair coefficient at the recipient line, and replaces only that packet's original Hub-to-zero descent. The candidate lineage retains every other parent event byte-for-byte. The full 400-direction linear replay finds exactly eight changed outputs, each an advertised B row with its advertised coefficient times its unchanged D output. Thus all X, Y, and D endpoints remain exactly the parent maps.

I seeded eight independent tags into the initial B rows immediately before the first old B use and propagated them through all later parent instructions, including intermediate owned records, snapshots, scales, and clears. All 329 tag-bearing events were processed. Each tag reaches only its own final B row with coefficient one. This verifies the full suffix transfer needed by the ferry argument.

The four advertised paired residual rows are exactly proportional and the independent rank calculation gives 58 before and 54 after. The zero residual rows are unchanged and remain the same 24 completed hosted ports. Recomputed original-coordinate first-Y debt is 4,920. All 104 designated first-X rows and all 104 designated first-Y rows match the parent exactly. Public raw MOVE calls are unchanged.

## Resource and phase checks

The private word has 6,314 instructions, 856 MOVE calls, 402 owner lifetimes, and peak 29. Relative to the parent it adds 1,056 ADDs and 16 MOVE calls while replacing eight rank-nine descents; the exact profile delta is `{1:+16, 7:+8, 9:-8}`. Total MOVE-rank mass is unchanged. There is no increase in owner count, peak, SCALE, or COPY count. The three-copy word has 85,489 instructions, 8,022 MOVE calls, 858 owner lifetimes, and peak 43.

The independent frame checker found exactly the 23 new ordered MOVE chart pairs listed in the author certificate. For each it reconstructed the signed Pauli tableau and exact Gaussian vacuum state of the certified recipe, verifying exact global phase. A phase-only mutation retained the tableau but changed the vacuum state and was rejected for each of the 23 pairs.

For the pinned m=3 invoice, independent replay obtains productive count 31,296, paid count 156,492, rank surplus 4,380, and per-rail moment lower bound

`60491953236701923665779004485461/6000000000000000000000000000000`

(approximately `10.081992206116988`). The exact rational enclosure is narrower than, and contained within, the published enclosure. This verifies the complete invoice for this partial word only.

## Scope limits

This is one actual word on the exact pinned source and all its 400 directions, together with its exact three-copy fixed-multiplicity lift. It does not imply an unlimited-m theorem, arbitrary-source extension, free reset, extra source credit, or complete endpoint. The remaining reverse response has rank 54; the original-coordinate forward debt remains 4,920. The accompanying general ferry/terminal obstruction must be applied separately to any completion claim.

## Reproduction

From the repository work root:

```bash
python worker-c/funded-cross-four-review/replay_four.py \
  --package worker-a/next/funded-cross-four \
  --source programme \
  --out worker-c/funded-cross-four-review/RESULT.json

python worker-c/funded-cross-four-review/phase_check_four.py \
  --package worker-a/next/funded-cross-four \
  --out worker-c/funded-cross-four-review/PHASE-RESULT.json

python worker-c/funded-cross-four-review/replay_m3_four.py \
  --package worker-a/next/funded-cross-four \
  --source programme \
  --out worker-c/funded-cross-four-review/M3-RESULT.json
```
