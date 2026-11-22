# A source-valid physical specialization of the coupled source/D family

**Positive local source/H/D construction. The original t=1 extension fails
source validity; the explicit t=26 extension passes. No fifth receiver,
complete supplier, foundational discharge or new κ.**

Baseline: programme commit44f09459f91f8c3e27fcd45f54be7d043e6493b7.
The underlying four-receiver source/H/D construction is
`bit-simultaneous-d1509-s032`. The rational interpolation equations and their
canonical fixed extension are those of `bit-source-d-interpolation-s032` and
`bit-source-d-tangent-s032`. This package does not alter either predecessor.
All field operations use GF64 with polynomial x^6+x+1.

## 1. Literal candidate and exact scope

Replace the actual35-by35 D1509 matrix T by T'=T+26E00, where26 denotes
the polynomial-basis field element0x1a (x^4+x^3+x). For every one of the44
local source/H systems, use the prescribed target

    Y' = [F C_H, M_6 S_6(T')^-1, M_9 S_9(T')^-1,
                    M_48 S_48(T')^-1, M_73 S_73(T')^-1].

Here X=[C_H,L] is the inherited96-coordinate input-generator matrix, and the
six-row source change ΔF satisfies ΔF X = Y' - F X. The deterministic extension
uses the first independent columns of X and then the first independent rows
of that column basis; all remaining coefficient positions are zero. This is
exactly the fixed extension rule used in the S032 tangent package.

`CANDIDATE.json.gz` stores T' and all44 literal6-by96 source corrections.
Only twelve corrections are nonzero: four source quotients at each of donors
0,32,35. Each has rank2. The other eight source stars and every H word retain
their literal coefficients. Source quotient rows0,1,2,15,16,17 act on source
coordinates0..47 and240..287; the other384 coordinates and24 quotient rows
are unchanged. `build.py` reconstructs these coefficients from the exact local
systems and verifies all44 relation systems and source-image equations.

The local proposition concerns the fixed eleven native donors of D1509,
receivers6,9,48,73, and the two previously admitted whole H interfaces263/642.
The source stars at the other100 native donors, further whole interfaces,
canonical return and complete recursive application remain open.

## 2. Why the t=1 local certificate was insufficient

The S032 t=1 extension satisfies every local interpolation equation, but four
complete source views are singular:

| Donor | Receiver | Protected96-view rank | Full480-view rank |
| --- | --- | --- | --- |
| 0 | 111, geometric only | 95 | 479 |
| 32 | 6 | 95 | 479 |
| 35 | 12 | 95 | 479 |
| 35 | 108 | 95 | 479 |

`output/CONTROLS.json` supplies a nonzero protected96-coordinate collision for
each case. Embedding the vector into480 coordinates makes every visible
thirty-row source quotient vanish. The unchanged384-coordinate complement is
invertible, so the full rank is exactly479. In particular, passing the local
receiver6 equations at donor32 does not prove that the proposed eight-frame
is an entire inverse fibre. This is an explicit failed realization, not a
no-go theorem for t=1 with a different extension or for the rational family.

## 3. Full source validity and genuine early preparation at t=26

Every paired source view is, up to row and column permutations, a direct sum
of its96-dimensional protected view and unchanged384-dimensional complement.
Every original quotient has zero entries in the two off-diagonal blocks;
the new changes touch only the protected block. The complementary views
inherit their nonzero determinants from the source-pinned S032 construction.

Direct exact row reduction verifies all63 protected geometric source views
at each of the eleven donors have rank96. Therefore all693 full geometric
views have rank480, including639 native views. This goes beyond the local
prescribed source images.

For each actual early owner, the new row is the appropriate row of Q[j,H]F'[j,H]
under the inherited physical owner itinerary. Each of the eleven actual
480-by480 early matrices has rank480. Late parities are the complementary
rows of the same phase-framed quotient. All owner labels and early/late quotas
are retained. No abstract interpolation basis substitutes for physical early
preparation.

## 4. Strict nonsaturation

For a donor j and distinct source planes h,k, let V range over geometric
source views containing both. Let A_V be the protected96-by96 source view in
its recorded source-plane order. The protected propagation span is

    P[j;h,k] = span_V columns_h(A_V^-1).

The block indexed by h has six columns. Every such block lies in the kernel
of the protected quotient at k. The checker forms the exact joined matrix
for each of the28·27=756 ordered pairs, with no sampled pairs or numerical
rank tolerance. It checks all2268 pairs at the three changed donors.

| Donor | Exact protected maximum | Unchanged complementary bound | Full bound | Required strict threshold |
| --- | --- | --- | --- | --- |
| 0 | 84 | 360 | 444 | 450 |
| 32 | 60 | 120 | 180 | 450 |
| 35 | 60 | 120 | 180 | 450 |

For donor0, the complementary propagation lies in the360-dimensional kernel
of the unchanged rank24 quotient. For32/35, the complement is two independent
width12 Reed–Solomon components; the inherited exact scalar propagation rank5
gives2·12·5=120. A common invertible protected input change in the predecessor
does not affect those complementary coordinates. The unchanged eight sources
retain their admitted bounds (at most444). All bounds remain strictly below
480-30=450.

The complete rank histograms are retained. Donor0 has ranks30,38,78,84 with
multiplicities1,26,81,648; donors32 and35 each have ranks52,58,60 with
multiplicities108,168,480. Exact reduction supplies both spanning relations
and nonzero minors. Hence these ranks persist over every coefficient-field
extension. Under r independent copies, direct-sum views and propagation spans
multiply each bound by r; strictness is preserved. For the existing eight
lanes at bank3840, the changed-source bounds are3552,1440,1440, below3600.
This is a theorem for the specified literal source tuple and its direct sums,
not for every point of the rational family or arbitrary coupled candidates.

## 5. Whole H and D fibres

At all72 geometric H263/H642 views (67 native), the new source maps have
exactly the old values on the full paired30-dimensional common H inverse
fibre, separately at each incident donor and every relevant central or
visible off-H quotient. Thus all off-H observations still vanish and the
central physical H readout is unchanged. The full source-view ranks establish
that the old common spaces are entire inverse fibres. The H words, including
the paid H642 complement, remain literal source-pinned dependencies.

The checker reconstructs the actual protected proper-left matrix A[j,r] from
source coefficients, phase frames, H early/late/cross matrices, real owner
labels and marked D exits. Every one of the132 geometric donor/receiver
proper-left matrices has rank96. For the44 retained donor/receiver pairs it
checks

    A[j,r] L_r = I_(D inputs) S[j,r](T')^-1,
    T'[O_r] P_j L_r = I8,

where P_j is reconstructed actual35-row ingress. The first identity proves
all off-D observations vanish on L_r. Since A[j,r] is invertible, its isolated
D1509 inverse image has dimension8, and the rank8 frame L_r is that entire
inverse image. The second identity gives a common actual identity readout.
Thus all four complete eight-dimensional receiver fibres survive at all eleven
native donors, with their same joint32-dimensional source frame.

The updated D has invertible19/16 phase blocks, zero forbidden upper-right
block, and all144 geometric8-by8 D sections invertible. These identities and
ranks persist over every field extension and fixed number of independent
lanes. No claim of a fifth entire receiver follows. The old forced four-space
response remains outside this package's positive conclusions.

## 6. Actual local implementation and cost

The changed source early matrices are compiled to binary ADD words by exact
Gauss–Jordan elimination. Reverse execution is checked on every original
binary input column; forward execution of the elimination word then restores
identity. These are2880 columns at each of the three changed sources,8640
columns total. Source late parities are formed before departure in the
inherited stationary caches and injected at their original Y-owner visits.
The cost counts every nonzero bit of the actual GF64 multiplication blocks.

The new D word uses the same35 original owners. It saves114 binary bits of
original early data, applies its114-bit early and96-bit late phases, adds the
late cross block from saved early data, and dirty-clears the cache. Symbolic
execution checks all210 original columns, including arbitrary late baselines.
Its per-base counts are6455 early ADDs per direction,4721 late ADDs per
direction,114 cache copies and4354 cross ADDs:26820 ADDs including pure
phase inverses,176 fewer than the old D word.

| Changed source | New early ADDs per direction | New late parity formation ADDs | Total base ADD change |
| --- | ---: | ---: | ---: |
| 0 | 2,445,494 | 456,797 | +5,756 |
| 32 | 263,330 | 138,310 | +30,684 |
| 35 | 253,967 | 137,753 | +35,321 |

Including the D reduction, the net base change is71585 ADDs. Eight lanes give
+572680 ADDs over the previous four-receiver physical invoice453937608.
The resulting gross local replacement bill is therefore **454510288 ADDs,
279648 INITs and279648 dirty CLEARs**, with the same16 field exports at gap6.
No MOVE is added. The eight unchanged source receipts and all280 H receipts
are explicitly reused with source pins; they are not presented as freshly
or independently recompiled in this package. The three changed source words
and D are freshly compiled and symbolically replayed. Compact deterministic
operation-stream hashes are retained; `compile.py` regenerates the streams.

These counts include the pure phase inverse words. Their placement in a
complete global restoration/preload schedule remains a separate obligation.
This is a local replacement bill, not a saving, signed supplier invoice,
canonical-return construction or complete multiplication algorithm.

## 7. Open next questions

1. Use a coupled source/D change that removes the forced fifth-fibre
   deficiency, then require these source, nonsaturation and whole-fibre checks
   before admitting a physical replacement. The canonical fixed extension is
   not automatically valid: the separate S033 q4 candidate also loses source
   ranks at several donors, as recorded without inferring impossibility.
2. Establish the missing whole interfaces and the other100 native source
   stars, then the global return, complete suppliers and recursive caller.
3. Keep native_all_columns, owned_erasure, compiler, precision_tape and
   analytic_recovery explicit. This package discharges none globally.

Credit @CubeJerry, the S031/S032 source, H, D and interpolation authors and
independent reviewers, and the inherited atlas/compiler lineage. Substantial
OpenAI assistance. Exact source-specific computational certificates and
mathematical argument; no independent human or formal-kernel proof claimed.
Apache-2.0.
