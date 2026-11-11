# Independent recovery review: dirty-bus boundary and H4 planning invoice

**Recovery checkpoint; No new κ.** This is not a completed supplier package,
physical admission, or upstream PR submission. It records independently checked
algebra and conditional profile arithmetic after the execution environment became
unavailable on 2026-11-11. The reviewed design still has no H4 native word.

## Sources and exact scope

Frozen canonical base: `e54523517d0f03e58352e647c403a5af3e525a57`.
The selected conditional saving remains `363005817/100000000000`; the research
target is exactly `1/200`. Source pins are in [SOURCES.json](SOURCES.json).

The design author supplied a draft named `work-construction/BUS-PROOF.md`.
The reviewer challenged it separately using a literal integer/Fraction matrix
interpreter, a source MOVE/helper census, and integer 200th-root bounds. No
contributor scientific code is imported by the JS checks in this directory.
The final author-file bytes could not be frozen after the environment outage;
the precise claim admitted by this recovery review is the corrected statement
below. Do not treat this record as a hash-bound approval of later author edits.

## Exact conditional algebra

Let m distinct normalized sources x_i be unchanged at their nominated contacts,
let m distinct targets y_i have arbitrary independent inputs, and let H have
arbitrary dirty input h. Every actual ADD must have matching current charts,
with every intervening chart transition separately paid on its owner. In order
i=1,...,m perform y_i-=H, H+=a_i*x_i; in the same order perform
H-=a_i*x_i, y_i+=H. All 4m ADDs are literal field operations.

Before the first target contact H=h+sum_(j<i) a_j*x_j. After the second unload
H=h+sum_(j>i) a_j*x_j. Thus H returns h and y returns y+K_m diag(a)x, where K_m
has upper entries +1, lower entries -1 and zero diagonal. This is a proof for
every m, not an extrapolation of the finite m=1,...,16 matrix check. If H exits
in a different chart, its physical h-return carries that autonomous chart
operator; its moves and boundaries cannot be discarded.

For even m, with D=diag(1,-1,1,-1,...), K_m D K_m D=I: diagonal entries use
sum_i D_ii=0 and off-diagonal entries use cancellation of alternating partial
sums. For odd m the alternating vector is in the kernel and the leading even
principal minor is nonsingular, so rank is m-1. The m=2 mechanism and elementary
skew-matrix identity are prior algebra, not claimed discoveries here.

For the selected 96 paired ports, order channels A1,A2,B1,B2. Their intended
normalized transfers are +x_1,+x_2,-x_3,-x_4. Assuming an unbuilt core gives
K4 diag(1,1,-1,-1), pre-encode target pairs with B=diag(K2,K2), run the core,
then decode with B^-1. The source transfer becomes

```
1  0  1  1
0  1 -1 -1
1  1 -1  0
-1 -1 0 -1
```

Cancel the eight cross entries using unchanged returned sources. Both members
of each target pair share their boundary charts. The original X and X2 labels
agree at both boundaries, as do Y and Y2, so every opposite-orientation cross
correction uses a cochart returned source. The exact full map is
(S,D,H)->(S,D+diag(1,1,-1,-1)S,H), with arbitrary incoming targets and dirty H.
A K2 signed swap or inverse takes three ADDs; four swaps plus eight cancellations
cost 20 ADDs per paired port, hence 1920 per native. There is no wrapper scratch,
copy, new helper credit, division, or Gaussian child.

The remaining eight selected ports are **coupled** type-B blocks, with
normalized map (X-Y,(X+Y)/2). They are not A-only shear ports. The unbuilt H4
premise must preserve two independent copies of these original coupled blocks.
The 96-port boundary lemma supplies no implementation of that requirement.

## Conditional complete signed invoice

H4 must realize every corrected endpoint with two copies of main-owned paid
jobs but one copy of public-helper and owned-scratch paid jobs; all 1080
arbitrary helpers are credited only once. The selected 54 owned lifetimes,
peak 43, source accesses, phases, restorations, all-column semantics and scalar
service cap are unproved requirements of this proposed architecture.

Let H be the selected helper target profile, G the helper-plus-owned paid
profile, and T,P the complete selected caller profiles. Duplicating every
caller/root/main/QUERY/IDLE/LAMBDA term and sharing just one native core gives
T4=2T-18H and P4=2P-18G. These equations lose duplicate helper credits.
The exact complete counts are 27344 targets and 152424 paid positions,
with rank surplus 5056. There are 7904 physical main/root inputs and 19440
stage-specific helpers. Same axis labels do not alias physical owners.

At t=199/200 the independently enclosed signed moment is

`1771183385103424848/10^15 < T4_t-P4_t < 1771183385103604616/10^15`,

in particular strictly between 1771.183385 and 1771.183386. Bounds are outward,
using q^200<=r^199*10^3000<(q+1)^200 for each rank r. The JS file contains the
complete transcribed profiles and checks the integer root inequalities.

The exact favorable **predecessor source-invoice** tally is 1526544192:
native scalar 3584800, native route items 12796 priced at 1000 each, eighteen
natives 294854400, twice caller ordinary 1199210432, input conversions 3519360,
and twice LAMBDA second charge 28960000. The 16/ADD and 1000/map conventions
are not current physical bit/tape tariffs. The selected application replaces
them with fixed scalar services and elementary route records. No physical
aggregate follows before H4 supplies actual bounded scalar services, actual
route records on ambient 153, stock/setup/parking/init/erase/source work,
precision growth and fresh finite-constant substitution. The old billion
source cap is also exceeded.

## Owned-bank obstruction inside this hypothetical family

Keep all preceding counts, but share only public helpers and duplicate
the owned bank. The extra per-native paid profile is
O={1:20,2:9,3:2,4:13,5:2,6:1}. Then Pdup=P4+18O and its exact signed moment
is strictly negative, bounded by

`[-234232700993570460,-234232700993389846]/10^15`.

Thus public-helper reuse alone, with this exact doubled-owned profile and
all other stated counts fixed, fails the κ=.005 raw-moment inequality.
It does not prove that owned work must be duplicated, or that H4 is impossible.

If an alternative saves a uniform per-native paid t-moment σ from that
duplicated-owned baseline and changes no other productive/paid term, positive
raw margin requires σ>-(T4_t-Pdup_t)/18. The threshold lies in

`[234232700993389846,234232700993570460]/(18*10^15)`,

approximately 13.012927833. This is a necessary raw-moment condition for that
precisely defined profile family, not a sufficient multiplication theorem.
The construction agent separately used binary-search roots at denominator
10^18 and obtained a narrower consistent interval; the receipt here uses
the reviewer's Newton root implementation.

## Checks actually completed and reproduction

Before the outage, the reviewer directly read and hash-checked the selected
compressed source and FULL-RESULT, then executed a separate Python census:
all 1095 binary frame bases were independent; every one of 6310 MOVE pairs
was properly nested; the main/helper/owned split matched the full paid
receipt; all 1080 helper endpoints were positive nested maps; all 96 paired
ports had both required boundary-chart equalities. This finite source check
does not prove an all-width native factorization. Those inherited contracts
remain conditional as recorded in the selected application.

The earlier Fraction matrix check passed all m=1,...,16 and the four-plane
map. After the outage, the **exact JS file text included here** was executed
in the functions JavaScript engine, producing the two adjacent JSON receipts:

```sh
node exact_matrix.js
node exact_invoice.js
```

Expected markers: PASS_INDEPENDENT_INTEGER_MATRIX_REPLAY and
PASS_INDEPENDENT_EXACT_BIGINT_RECOMPUTATION. These Node commands are portable
reproduction instructions; a local Node execution was not available after
the outage. The included code was run in the tools' JS engine, not merely
written. No contributor solver or floating-point numerical root is used.

Matrix controls rejected omitted target pre-encoding, omitted cross
corrections, wrong reverse signs, and a source-version fault. In the last
control source x1 is replaced by x1+x2 during cross corrections and restored
afterward; the returned sources are correct but two target residuals are
-x2 and+x2. Returning sources eventually is insufficient if corrections
read the wrong versions. For geometry, an ordinary physical ADD from a
swap-chart source to an identity-chart target inserts the swap; cancellation
of intended source e0 leaves e0-e1. Hence matching scalar coefficients alone
does not justify a cross-chart ADD.

The partially edited local Python packet was not finalized: a new stale-source
control needed fixed prescribed cancellation coefficients instead of reading
them from evolving rows. That correction is present in exact_matrix.js.
Do not reuse the incomplete local check_bus.py as the published verifier.
The bounded K4-cohort search in the author's draft was not independently
reproduced by this reviewer and is not certified by these receipts.

## Remaining obligations, novelty, and credit

No native itinerary, chronological common-chart access proof, shared owned
bank construction, physical tariff extraction, precision envelope, outer
compiler/strictification, or ordinary BIT backend above .005 has been
provided here. The five retained foundational assumptions are unchanged:
native_all_columns, owned_erasure, compiler, precision_tape, analytic_recovery.
Positive conditional raw margin is neither a complete conditional κ=.005
assembly nor an unconditional multiplication theorem.

Credit DreamingOfClouds' CrocSwap/integer-mult-bounds#6902 two-chain native
and #6937/#7000 shared-wire lineage, and @CubeJerry's #6912 mixed-unit bridge.
The elementary dirty-bus/skew algebra is not claimed as new. The scoped
contributions are the selected opposite-chart boundary compatibility,
the complete hypothetical profile relation, and the doubled-owned-bank
threshold inside that explicit family. This review was performed by a
separate OpenAI agent for @CubeJerry; it is not human or formal-kernel review.
All selected source contributors retain their existing attribution.
