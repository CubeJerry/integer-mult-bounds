# Independent compiler and accounting review of the native D1509 prefix

**Accepted in the stated local scope.** The independent replay passes with **313,198,856 binary ADDs, 134,928 INITs, 134,928 dirty CLEARs, and the retained sixteen gap-six field exports**. It does not establish the unbuilt global transport or a supplier invoice.

The review covers PROOF sections 3, 4, 7 and 8 and the physical accounting in `compile_prefix.py`. The separate source/H/D geometric and common-fibre proof is reviewed by worker C. My checker imports no author executable. It reads the frozen literals and the raw atlas routes, implements its own polynomial arithmetic and binary lift, regenerates every phase ADD stream, and replays the circuits on all independent input bits.

## Source owners and late parity holders

For all five supplied sources I reconstructed every paired thirty-row quotient from the literal fifteen-row source map and thirty-by-thirty phase frame using an independently computed multiplication table for GF64. The multiplication table uses polynomial multiplication followed by long division by `t^6+t+1`.

I assigned each early row to its actual original X owner using the raw route list and checked equality with both the labelled and physical 480-by-480 early matrices. Every original owner 0 through 479 appears exactly once. Thus the source owner permutation is included in the compiled matrix.

The remaining rows of each paired quotient agree exactly with the stored late parity rows. Their counts equal the raw Y visits at that source and H, in actual Y-owner order. There are 360 parity fields per supplied source and 1,800 in total. I verified all 1,800 cache-to-Y bindings and their uniqueness. The binary formation replay starts each additional holder at zero, adds the specified original source bits, then injects the resulting parity into its actual Y owner while retaining an independent arbitrary Y baseline. The cache clear acts on the additional holder, not on that original Y owner.

The five new source phase compilers have the following exact counts. Both their physical matrix roles and their deterministic word hashes agree with the frozen receipt.

| Source | ADDs per direction and lane | Parity formation ADDs per lane |
|---|---:|---:|
| 0 | 2,438,764 | 424,342 |
| 45 | 2,418,579 | 431,101 |
| 61 | 2,392,569 | 434,920 |
| 62 | 2,352,169 | 426,528 |
| 100 | 2,348,503 | 430,986 |

These are the current native-D1509 source matrices. The earlier checkpoint6 source compiler word is not substituted for them.

## All 136 physical H modules

For every H module I reconstructed the sorted original X and Y owner lists directly from the raw atlas and matched them to the physical matrix order. I independently regenerated and replayed the early and late phase words. Required row swaps cost three distinct-owner ADDs; no permutation is supplied for free. All phase operation counts and uint32 little-endian stream hashes agree with the frozen phase receipts.

For an ordinary H module with a cross block, the replay copies its original early input bits before the early transform, transforms the arbitrary late input bits when they arrive, then adds the binary cross block from the stationary copies. The complete result equals the full block matrix on every independent early and late input bit. There are exactly 22 nonzero-cross modules, each with 45 original early fields, for 990 H cache fields. Their copies cost 5,940 ADDs and 5,940 INIT/CLEAR operations of each kind per base lane. The exact cross-block bill is 168,500 ADDs per base lane.

At H642 I checked that the actual ninety-owner word and input-owner order are the retained ones, and compiled the same 92-by-92 extension. With the two additional field inputs initialized to zero, its first ninety outputs equal the specified word and its last two outputs equal the retained information complement. The inverse restores all ninety original fields and the two initialized zeros when all extension outputs are supplied. This preserves the accepted two-field complement per lane and its existing gap-six export contract; it does not create another free complement.

## Chronological D1509 word

The raw routes give exactly nineteen early X owners followed by sixteen late Y owners at D1509. I checked the literal owner order, the 35-by-35 phase matrix, every cache label, and the complete early, late and cross ADD lists. The independent replay begins with 210 unrelated original input bits. It copies the 114 early bits into additional holders, applies the early word to the actual early owners, applies the late word to the arbitrary late owners, and adds the cross block from the copies.

The resulting symbolic rows equal the complete binary lift of the D matrix. In particular the sixteen late original baselines remain present. There is no initialization of an original Y record and no access to a departed original X record through an uncharged alias.

| D operation per base lane | Binary ADDs |
|---|---:|
| Early phase forward | 6,543 |
| Late phase forward | 4,721 |
| Copy nineteen early fields | 114 |
| Cross block from stationary copies | 4,354 |
| Forward total | 15,732 |
| Forward plus both pure phase inverses | 26,996 |

The D holders require 114 INITs and 114 dirty CLEARs per base lane, and no extra MOVE. At eight lanes this gives 215,968 ADDs and 912 INIT/CLEAR operations of each kind.

## Gross invoice reconciliation

Every additional holder has a distinct typed label. The base instance has 1,800 source parity holders, 990 H early holders, nineteen D early holders and two H642 complement holders: 2,811 fields or 16,866 bits. Eight lanes give 134,928 INITs and the same number of dirty CLEARs. The sum is a conservative simultaneous-holder count when lifetimes overlap; individual lifetimes are tied to their actual copy, visit and last-use events.

| Component | Base binary ADDs | Eight-lane binary ADDs |
|---|---:|---:|
| Five source and 136 H phase words, with pure inverses | 36,789,744 | 294,317,952 |
| Source parity formation | 2,147,877 | 17,183,016 |
| Source parity injection into actual Y owners | 10,800 | 86,400 |
| H early copies | 5,940 | 47,520 |
| H late cross blocks | 168,500 | 1,348,000 |
| D word, copies and both pure inverses | 26,996 | 215,968 |
| **Total** | **39,149,857** | **313,198,856** |

The retained H642 complement contributes sixteen full-bank field exports, or 96 binary MOVE records, at gap six. Source parity, H early and D early caches are stationary and introduce no additional MOVE in these local modules.

## The inverse boundary and admission limit

The exact replay verifies each pure early and pure late inverse as a local circuit. The pair of pure inverses is not, by itself, the inverse of a complete block matrix with a nonzero cross term. The proof correctly leaves their global Hub restoration and actual-Y preload placement conditional on the later transport construction. My review supplies no K/facet word, global return replay or complete supplier invoice.

The totals are gross replacement costs for the supplied components, including their stated pure inverse words. They do not subtract an old implementation, price other sources or D modules, or establish a kappa improvement. Within this boundary, the physical ownership, stationary-copy chronology, full symbolic local maps and operation inventory are independently verified.

Reproduce with `python review-b-compiler/check.py` from this package or any working directory. The complete independent receipt and all input hashes are in `review-b-compiler/output/RESULT.json`.

Reviewed by S031 worker B, 2026-11-20.
