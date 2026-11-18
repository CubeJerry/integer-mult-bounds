# A paid seven-source decoder through a genuine shared rank-six chart

## Result

The seven-source native F8 construction admits a literal word that merges
two shared D4 messages at an actual rank-six chart K=A2-perpendicular,
performs an invertible two-by-two F8 decoding there, and delivers the two
decoded scalars to their actual receiver facets. The source queries are
the same simultaneous queries used in PROOF.md. All original X values
are restored unchanged at Hub, and every arbitrary Y baseline is retained.
All 42 foreign blocks are identity blocks on five F8 coordinates.

The exact binary word has

    4084 ADD, 315 INIT, 315 charged dirty CLEAR, 966 MOVE,
    movement profile 252[1]+315[2]+189[3]+210[7],
    peak 129 owned binary records.

It is checked on all 210 original binary input columns. The owned source
query records themselves are reused as the two shared plane outputs by
an explicit invertible in-place map. No original X or Y record is erased
or treated as free helper storage.

This word is a newly paid seven-source foreign-subsum fragment. Some
outputs still use explicitly charged direct D4-to-facet moves. It does
not assert the fixed full balanced path word, all native source quotient
compatibility, a complete supplier price, or a new kappa.

## 1. Geometry and joint decoding

Use the actual donor and receiver roles, field, queries and output rows
from PROOF.md and SHARED-D4-PROOF.md. For one source-pair plane H={j,k},
write its two source queries as z in F8^2 and order its five receiver
targets as a,b,c,d,e. Their five required scalar rows c_i are pairwise
nonproportional.

Choose actual D4 flats D_a,D_b,D_c with target visibility respectively

    {a,d,e},       {b,d,e},       {a,b,c}.

As before, these flats exist for every one of the 21 source-pair planes.
Let P be the actual A2 plane spanned by the native receiver roots d and e,
and put K=P-perpendicular. The selected receiver roots are pairwise
nonorthogonal and each pair belongs to an actual A2 plane. Thus K has
rank six. Since D_a and D_b are both contained in F_d and F_e, both are
contained in K. All inclusions

    H < D_a < K < F_d,
    H < D_b < K < F_e

are strict actual chart inclusions, with ranks 2,4,6,7. The certificate
records the real A2 index defining each K and verifies orthogonality
against every root of the selected D4 flats.

The two rows c_a,c_b form a basis of (F8^2)*. Define the matrix C by

    [c_d; c_e] = C [c_a; c_b].

The matrix C is invertible because both row pairs are independent.
Transmit q_a=c_a z and q_b=c_b z from H to D_a and D_b. Each D4 sends
one explicitly copied scalar to K, while its original scalar continues
to F_a or F_b. At K the in-place matrix C transforms the two copied
values into exactly q_d=c_d z and q_e=c_e z. These two physical records
then move to F_d and F_e. The third scalar q_c=c_c z travels through D_c
to F_c. Every receiver multiplies its received scalar by the same lift
vector v_(i;jk) as in the original code.

Consequently all five receiver contributions are identical to the direct
construction, jointly for all source values. This is a genuine common
K decoder on the two actual delivered records; it does not choose
incompatible receiver-specific maps on one shared field.

For source pair (0,1) in the seven-source ordering, H is actual H20.
The chosen target order is (2,3,4,5,6), and the D4 indices are 1446,2,928.
The exact H and K matrices and the A2 index defining K are recorded in
the first merge certificate. All field elements use the binary polynomial
basis of F8=F2[a]/(a^3+a+1), so there is no unspecified coefficient choice.

## 2. Literal in-place matrices and ownership

Initially form the 42 source query fields at their actual native lines
and move them to their actual pair planes. Original X is then moved
unchanged to Hub and original Y to its target facet, as in the direct
word. At each plane its two query fields are owned helpers; their values
may therefore be transformed or reused while their lifetimes are tracked.

First create one fresh helper for q_c, form it from the two query fields,
move it through D_c to F_c, decode it and clear it dirty. This is done
before the query fields are overwritten. Apply the invertible matrix

    [c_a; c_b]

in place to the two query fields at H. The fields now contain q_a,q_b.
Move each to its chosen D4. At that D4, create one fresh zero helper,
copy the value into it by three binary ADDs, and move the copy to K.
Move the original shared field to F_a or F_b, decode and clear it dirty.
When both copies have reached K, apply C in place, then move and decode
the resulting records at F_d,F_e and clear them dirty.

Every F8 two-by-two matrix is expanded to a six-by-six binary matrix.
Binary Gaussian row reduction, with swaps written as three ADDs, gives
a finite sequence of ADDs on the existing six records. Reversing the
reduction gives the actual in-place word. Both each local six-column
matrix and the whole 210-column program are replayed exactly. No field
multiply oracle, extra temporary record, or uncharged scalar operation
is used. The event word includes every local matrix ADD.

There are 42 original query-helper lifetimes and three extra field-helper
lifetimes per pair plane: one q_c and two K copies. Hence 105 field
lifetimes, or 315 binary INIT and CLEAR. Reusing the query helpers avoids
creating and later clearing redundant copies at H. Every retired helper
is a nonzero arbitrary-input linear form, so every CLEAR is charged dirty.
At peak, the 42 initial query fields and one additional field coexist,
giving 129 binary owned records.

## 3. Complete invoice

The movement counts are:

| Movement | Field records | Binary records | Rank gap |
| --- | ---: | ---: | ---: |
| Source line to pair plane | 42 | 126 | 1 |
| Pair plane to D4 | 63 | 189 | 2 |
| D4 to shared K | 42 | 126 | 2 |
| Shared K to receiver facet | 42 | 126 | 1 |
| Direct D4 to receiver facet | 63 | 189 | 3 |
| Original X to Hub and original Y to facets | 70 | 210 | 7 |

Thus the full movement profile is 252[1]+315[2]+189[3]+210[7]. All
branching is implemented by the explicitly listed D4 copies. The 42
source-query moves remain charged even though their physical records
are later reused for the H-to-D4 shared messages.

The ordinary ADD partition is 864 at source, 223 to form the third plane
outputs, 417 for in-place two-query maps at H, 126 for D4 copies, 465 for
the in-place K decoders, and 1989 at receiver facets. The total is 4084.
Every ADD is co-located, and every original record ends at its required
native boundary chart with the required exact value.

## 4. A strict local movement improvement

For the frozen movement moment d^(199/200), the direct seven-source word
has moment about 3144.14344971750, while this K-merge word has moment
about 2899.48125180586. Their exact profile difference is

    315[5] − 315[2] − 189[3] − 126[1].

The price_merged.py certificate bounds each d^(199/200) between exact
rationals using integer 200th-power comparisons. It proves a strictly
positive difference of about 244.662197911639 for these same seven-source
input/output contracts. Original X/Y movements cancel in the comparison.

This is a local movement improvement, not a complete supplier improvement.
The K word uses 151 more ordinary ADDs than the direct word (4084 versus
3933), but 126 fewer binary helper lifetimes because of explicit in-place
reuse (315 versus 441). All these costs are stated separately. The
balanced programme's global movement target and selected kappa are not
updated by this isolated fragment.

## 5. Independent verification and remaining boundary

Reproduce with

    python3 -B build_merged.py --layout LAYOUT.json.gz --out OUTPUT
    python3 -B price_merged.py --out OUTPUT/PRICE.json

The author checker replays every original input column, final original
chart, owned lifetime and charged operation. It rejects removing a K
decoder ADD and removing a D4-to-K move. The separately implemented
native-word-review checker reconstructs K as the exact rational kernel
of the real dual A2 root span, checks all strict chart inclusions by
rank, and replays all 210 columns with sets of input indices. It also
rejects a removed receiver ADD, a removed source MOVE and corruption of
an arbitrary Y baseline.

The root reviewer independently checks the word and its geometry before
admission. Extending it to the complete retained supplier requires a
compatible source quotient assignment across all native donors and
receivers, compliance with the actual shared-port capacities and fixed
route multiplicities, all canonical corrections and global inverses,
and ordinary and recursive accounting. The present paid upward helper
word belongs to the retained nested-owned model, not a stricter
descending-only helper restriction.

Credit Worker A's initial F4 construction, the native/balanced atlas
authors, @CubeJerry, root's independent review, and substantial OpenAI
assistance. The general-n and K-merge construction is Worker B's S023
work, with exact source and artifact pins in DEPENDENCIES.json.
