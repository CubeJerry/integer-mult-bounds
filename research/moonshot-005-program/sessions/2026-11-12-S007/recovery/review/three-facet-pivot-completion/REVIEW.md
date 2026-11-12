# Independent review: three-facet completion with real raw pivots

## Verdict

**PASS.** The frozen 75,085-instruction word completes the ordinary private blocks (56,168), (77,189), and (100,212). The three selected private Y outputs are respectively v168+v56, v189+v77, and v212+v100, while their X outputs remain the original vX. All 1,480 common outputs, the seven previous history corrections, and the other 4,841 foreign residual coefficients are preserved. The complete private difference map is invertible.

This is one compatible rewrite of the independently reviewed fused seven-correction parent. The checker reconstructs the entire new word independently; it does not combine the one- and two-facet schedules. It imports no construction-author code. It reuses our pinned source-root, prefix, type-walk, and integer-root helpers, plus the retained independent signed-Pauli/global-phase verifier for physical map recipes.

## Actual acquisition geometry

The three final facets are 179, 198 and 220. Their actual pairwise intersection charts are 955, 904 and 957, each dimension seven. Chart 1095 is explicitly declared with basis [3,25,41,72,132,260]. Its dimension-six span is exactly the triple intersection. All original 1,095 chart frames remain unchanged.

The checker derives the Gram coefficients from the original port vectors. Each receiver needs 48 foreign coefficients of magnitude one half. Partitioning by precisely which receivers need each donor gives:

| Receiver support | Donors | Acquisition chart |
|---|---:|---:|
| 168 | 14 | 179 |
| 189 | 14 | 198 |
| 212 | 16 | 220 |
| 168,189 | 16 | 955 |
| 168,212 | 14 | 904 |
| 189,212 | 14 | 957 |
| 168,189,212 | 4 | 1095 |

There are 92 distinct donors, 144 receiver/donor coefficients, and 12 actual stationary owners. The four triple donors are 12,17,31,38. Every original donor line is contained in its acquisition chart. Each shared donor makes one compatible ascending journey. The three receiver routes are 3→1095→955→179, 3→1095→957→198, and 3→1095→904→220.

## Reversible pivots and original-value recovery

The original parent has 104 consecutive donor MOVEs at events 410–513 with no arithmetic between them. The new schedule holds pivots 10,0,6 on their initial lines while all other donors make their acquisition routes and reach the hub. The pivot cohorts are disjoint exact-pair classes. None of the pivots is one of the five initial-line controller donors.

| Pivot | Pair chart | Delivered receiver | Facet | Pivot coefficient |
|---:|---:|---:|---:|---:|
| 10 | 955 | 189 | 198 | −1/2 |
| 0 | 904 | 168 | 179 | +1/2 |
| 6 | 957 | 212 | 220 | −1/2 |

For one cohort D, pivot j and delivered receiver y, the real pair accumulator holds A=sum over d≠j of a_d q_d. At the pair chart the original q_j first contributes to the receiver that visits this chart. Then the pivot becomes S=a_j q_j+A. It carries S to the missing receiver's facet, adds S to the actual stationary facet collector, and continues to the hub. The pair accumulator is retired; no independent record of q_j is assumed.

At the hub every other q_d in that cohort is present on its original carrier. The actual inverse subtracts each a_d q_d and scales by 1/a_j. Since a_j is nonzero, this is an invertible triangular change of coordinates. The 41 recovery sources were checked individually as exact original q rows at the actual hub. The three delivered full aggregate rows and each immediate inverse-SCALE result were also checked on all 1,880 formal initial coordinates.

After event 817, boundary 818 has all 104 original qX rows simultaneously at hub 127. All 520 subsequent retained E8 ADD source reads were individually checked to read the correct original donor at that chart. This checks the source reads themselves, not merely the later packet MOVE times.

## Whole-word equivalence and invertibility

Every parent instruction is accounted for. The only moved parent operations are the donor MOVEs in that consecutive block; all parent arithmetic stays in order, every native instruction retains its literal bytes, and every old raw arithmetic access retains its physical chart. All 12 new owners are retired before common processing starts.

A separate exact prefix interpretation starts with independent common u and private v=u+q coordinates. At common entry the new word differs from the reviewed parent in exactly three raw receiver rows, each now qY+qX. Every common row, other raw row, and retained controller cache is identical. After that boundary each selected raw receiver participates only in its final common recoupling. Thus the parent's common restoration, COPY guard, previous seven corrections, and other rows carry over through an identical suffix; a second dense full-native replay is unnecessary.

The checker independently reconstructs the final 400-by-400 private difference map from the source Gram matrix and actual correction rows. Exactly 144 new foreign coefficients vanish, and all other 4,841 residual coefficients stay unchanged. All X rows are original qX; each first-Y row has nonzero own-Y diagonal and only X terms elsewhere. Subtracting those X rows and dividing by the diagonal gives an explicit inverse, checked for every one of the 400 rows. The full common map Tu is invertible by the reviewed native contract, so the joint endpoint map recovers u, then q, then v=u+q. Erasing derived accumulators loses no independent initial coordinate.

## Physical chart maps and negative controls

The complete type walk checks every arithmetic cochart, strict nested MOVE, owner lifetime, endpoint chart and rank. It verifies zero collector MOVEs and peak ownership 43. The new chart basis and all acquisition/receiver inclusions are authenticated directly from binary spans.

All 99 newly introduced ordered chart pairs are present exactly once in the recipe certificate. This review freshly executes the retained independent signed-Pauli/global-phase verifier on every recipe against the actual old or new chart frame. Recursive ranks agree with dimension differences. The existing exact compiler is credited as inherited; this is not a newly authored chart engine or an independent all-column supplier construction.

Six negative controls reject: doubling an inverse scale leaves 2q10; omitting one hub cancellation leaves an extra q11 in donor10; reversing a facet delivery sign creates 16 erroneous receiver coefficients; omitting the pivot facet stop breaks cochart arithmetic; changing the new chart breaks actual nesting; changing a recipe's global phase fails exact physical equality.

## Complete bill and remaining scope

| Quantity | Actual | Increment over fused parent |
|---|---:|---:|
| Instructions | 75,085 | 328 |
| ADD | 64,424 | 197 |
| SCALE | 3,676 | 6 |
| MOVE | 6,826 | 101 |
| INIT / CLEAR | 79 / 79 | 12 / 12 |
| COPY | 1 | 0 |
| Peak owned | 43 | 0 |

The 197 added ADDs cover 144 acquisitions/encodings, three facet deliveries, 41 hub recovery operations and nine receiver reads. The actual raw profile is {1:61,2:43,3:4,5:5,6:48,7:48,8:299}: 508 calls and total rank 3,200. All eight original rank-nine packet calls remain present and charged.

The complete conditional H4 profile is independently rebuilt from the pinned source invoice and actual MOVE counts. It has 130,932 paid positions, 27,344 target positions and rank surplus 3,760. Exact directed integer-power enclosures confirm extra raw moment approximately 1.8539402799956353 and remaining conditional moment per native approximately 45.10785453981816.

The word still has 4,841 foreign coefficients and the private reverse duties open. This is a verified partial native, not a complete multiplication bound, and no free composition with another cohort schedule is implied.

## Reproduction

Run `python check_three_pivots.py` or `python -O check_three_pivots.py`. The deterministic receipts agree. All review rejection conditions use explicit exceptions. `MANIFEST.json` pins the checker, receipt and this report. The source, parent word and independent receipt, construction word/proof, and reused helpers are separately pinned in the checker.
