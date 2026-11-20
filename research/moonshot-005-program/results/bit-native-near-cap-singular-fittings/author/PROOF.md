# Concrete near-canonical fittings at the 34,688-symbol cap

All three constructions use b=3,840 on all 111 original roles and have the true identity on every own block. They are abstract native fitting matrices over any field of characteristic two. A physical source-to-terminal compilation remains required.

| Construction | Return rank | Directed corank | Reverse corank |
|---|---:|---:|---:|
| Concentrate on (80,96) | 34,688 | 150 | 143 |
| Concentrate on (0,1) | 34,688 | 148 | 145 |
| Spread across all 6,470 proper blocks | 34,686 | 14–21 at every directed cell | Same distribution |

For the exceptional pair, take eleven independent copies of the explicit bank-13 rank-128 fitting. Use seven individual scalar canonical slices with the directed (80,96) coefficient removed, each of true rank ten. Put a canonical scalar rank-nine fitting on each of the remaining 3,690 field coordinates. On the targeted proper block this removes 11×13+7 dimensions. All seven scalar erasures leave the reverse direction present.

For the regular pair, the realized bank-29 word uses thirteen copies omitting owner 0 and fourteen copies omitting owner 1, plus forty-three native clique sums. Both (0,1) and (1,0) vanish. Each original owner receives precisely twenty-nine coordinates. Five copies give a loss of 145 dimensions, followed by three scalar directed erasures and 3,692 canonical fields. The return rank is 34,688. The bank-29 and bank-406 examples attain the same regional ratio 29/25.

For distributed loss, use 21 explicitly listed partitions into fifteen native proper cliques and the canonical fitting on the other 3,819 fields. Each partition grade is a direct sum of fifteen independent group-sum words, so the total rank is 3,819×9+21×15=34,686. A proper coefficient is present on a partition grade exactly when its two endpoints share a clique. The published partitions put no pair together more than seven times. Across the full atlas the proper coranks 14,15,16,17,18,19,20,21 occur in respectively 44,144,334,816,1370,1722,1424,616 ordered cells. Thus every proper block is singular while the abstract target return still has two spare symbols.

The constituent block-rank calculation checks every actual scalar row, every native structural zero and the entire bank coverage. Each occurrence assigns one fresh field per active role, so each block is a partial permutation under its own local coordinate order. Its exact rank is the number of simultaneously active permitted occurrences. `check.py` records the complete proper-corank histograms and exact global ranks.

## Replay

From the results directory use `python bit-native-near-cap-singular-fittings/author/check.py --out /tmp/near-cap-replay`. The standard-library verifier finds the native root layout in the adjacent published atlas and accepts a relocated path through `--layout`. The resulting `RESULT.json` contains the full 6,470-cell corank distributions, both directed endpoints, every paid abstract return rank and the exact retained original channel counts.

Credit @CubeJerry and the original native atlas and rank-nine programme. Substantial OpenAI assistance.
