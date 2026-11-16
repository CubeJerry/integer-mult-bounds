# Actual Extra6 triple with a repaired original-source itinerary

## Result and authenticated inputs

The word completes **43 outputs**, preserving the entire cyclic41 target set
and adding 37 and 50. It retains the three actual `M1` imports of 8, 9 and 36.
Its new common code, after subtracting already-present ground masks, is

\[
C_6=P6+E75+E77+E79=X_{19}+X_{37}+X_{50}.
\]

The three roots are pairwise orthogonal. The code is built from actual
chronological source captures, not from an optimistic Extra6 source bank.

The immediate 42-output source has SHA256
`d5726e001270e007209507c8eb9f385167a7d304a9f09c194381296b569f293f`.
The new 43-output word has SHA256
`3483fb4abac2f71bf266df368c97fcf5a624fee89ef82b55ca8238e56e74b1b8`.
Both pin the native source by
`8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e`.
The cyclic-import construction, proper-birth optimization, prior clique codes
and source-recovery certificate retain their predecessor attribution.

## The source obstruction and its paid repair

The native `X50` original used to follow

`L50→J16→C0(=M0)→Hub`.

At `J16` it contributed to `PRIVATE16`; at `M0` it contributed to
`H1_1`, `H1_2`, `Hnew1_0` and `Q0`. The desired new correction plane
`B=span(L50,L19)` is incomparable with `J16`. Appending that new stop to the old
route is illegal, and an explicit negative control rejects it.

Move the birth of `PRIVATE16` to `M0`. Its exact source sum is unchanged:

\[
\mathrm{PRIVATE16}=X_7+X_{30}+X_{31}+X_{49}+X_{50}.
\]

The first four actual originals already visit `M0` after their old `J16`
visits. Capture them into `PRIVATE16` at `M0` instead. For `X50`, use this new
public itinerary:

`L50→B→Extra6→Hub`.

At `Extra6`, capture raw `X50` into a fresh owner `IMPORT_RAW50` and move that
owner to `M0`. This is one paid rank-one owned move. At `M0`, add this actual
import into `PRIVATE16` and into each of the four old M0 caches listed above.
The independent formal replay and a before/after cut comparison check that all
five cache rows are exactly their old values.

The `P0` query of `PRIVATE16` moves from immediately after its `M0→J16` descent
to immediately before that descent. Its earlier `KEEP_C0` retention/reset has
already occurred. Thus the packet arrives at `J16` with precisely its old
value, and all lower `P0` services are preserved. The added import is real,
present at the queried chart, and ultimately cleared. No copied row is granted
for free.

## Three actual source and receiver paths

Use the following rank-two planes, all contained in rank-six `Extra6`:

| Name | Plane | Receiver whose facet contains it |
|---|---|---|
| `P6_K` | `span(L19,L37)` | `F50` |
| `P6_A` | `span(L50,L37)` | `F19` |
| `P6_B` | `span(L50,L19)` | `F37` |

The actual `X37` original visits `P6_A` before `Extra6`. At that first plane it
is captured into stationary `P6_RAW37A`; at `Extra6` it contributes to
`EXTRA_AFF`. The rerouted actual `X50` is captured into `P6_RAW50B` at `P6_B`
and also contributes to `EXTRA_AFF` at `Extra6`. Therefore the real source row
is

\[
\mathrm{EXTRA\_AFF}=X_{37}+X_{50}.
\]

Raw native-line captures `P6_RAW37L=X37` and `P6_RAW50L=X50` are made before
the corresponding originals move. Their stationary births, captures and
retirements are included in the word and invoice.

`P6` is born at `Extra6`, reads the actual row above, and descends through
`P6_K`. It copies `X37+X50` into stationary `P6_RET`, descends to `L19`, adds
the existing actual raw `HRAW19=X19`, and continues to ground. Its existing
three ground masks are still added, giving the stated common code after
mask correction. The former `HKEEP_L19` owner and reset are removed.

The exact decoder equations and nested paths are:

| Receiver | Ground preload | Subsequent actual reads | Ascending path |
|---|---|---|---|
| `Y19` | `C6` | raw `X50`, then raw `X37` | `zero→L50→P6_A→F19` |
| `Y37` | `C6` | raw `X19`, then raw `X50` | `zero→L19→P6_B→F37` |
| `Y50` | none | raw `X37`, then `X37+X50` | `zero→L37→P6_K→F50` |

The previous 42-output construction already preserved the old output20 by a
paid raw native-line-to-ground copy. That repair is retained. Every old 42
endpoint remains exact, and output50 is added. The three genuine M1 imports
of 8, 9 and 36 remain unchanged at the programmable source cut.

## Complete invoice

From the immediate 42-output source, the new counts are

| Operation | Before | After | Change |
|---|---:|---:|---:|
| INIT | 125 | 130 | +5 |
| ADD | 830 | 844 | +14 |
| MOVE | 484 | 492 | +8 |
| Dirty CLEAR | 125 | 130 | +5 |

Peak ownership is 130. All scratch fields are retired. Let
`[d]=d^(199/200)`. The exact signed movement changes are

| Changed path | Signed increment |
|---|---|
| Actual original50 itinerary | `[4]+[2]-2[3]` |
| New actual raw50 import | `[1]` |
| Actual original37 correction stop | `[1]+[4]-[5]` |
| P6 rank-two retention stop | `[1]+[4]-[5]` |
| Y19 triple decoder | `2[1]+[5]-[7]` |
| Y37 triple decoder | `[1]+[5]-[6]` |
| New Y50 decoder | `2[1]+[5]-[7]` |

Their sum is

\[
8[1]+[2]-2[3]+3[4]+[5]-[6]-2[7].
\]

The linear rank-volume increases by exactly one. The movement moment
increment is enclosed by

`[1.09204992241481661960591661170799,`
` 1.09204992241481661960591661170809]`.

The full new movement profile is

`{1:194, 2:40, 3:59, 4:12, 5:77, 6:23, 7:87}`.

Its moment is enclosed by

`[1619.20896182605571357585390598070092,`
` 1619.20896182605571357585390598070390]`,

leaving necessary limiting room at least
`2.541918385096641670392244386289975`.

Root's separate raw2/BACK2 exchange may commute with this construction, but
that additional optimization is not included in this pinned word or invoice.

## Verification and negative controls

The retained independent interpreter checks all 222 independent formal input
columns; exact rational chart containments; each chronological co-location;
public ascent and owned descent; all original-X restoration; all 111 original-Y
endpoints; and complete scratch retirement. It also verifies the three common
code roots are pairwise orthogonal, the retimed M0 rows are unchanged, and the
three M1 imports are still actual raw values at the correct chart.

Fourteen omitted captures, import movements, decoder reads, decoder stops or
retirements fail the replay. A fifteenth control restores original50's old
`J16` stop before its new plane and is rejected for an illegal route. These
checks do not rely on inherited source-cut metadata. Literal binary equations
lift to every characteristic-two field and positive whole-record width.

## A reusable sufficient source-repair pattern

Suppose an actual original supplies several linear caches at a lower chart
`S`, and a desired new public itinerary instead reaches an upper chart `H`
containing `S`. Capture its actual row at `H`, pay an owned descent from `H`
to `S`, and replace every old contribution at `S` by that imported row.
If a separate private cache was born below `S`, it can be retimed to `S`
provided every other contributing original already visits `S` with the same
value, and its sole owned query can move to the preceding `S` visit without
changing any intervening retained values. All these conditions are checked in
this concrete instance. The general pattern requires its own chronological
and chart-compatibility checks on each use.

The cost of the paid `H→S` import must be retained. In this instance it is one
rank-one move and removes the source-path incompatibility that would otherwise
invalidate the clique decoder.

## Reproduction and open questions

```sh
python3 -B workers/coded/build_extra43.py \
  --repo programme --base workers/coded/extra42/WORD.json \
  --engine workers/audit/leaf-capacity-gate/check.py \
  --price-engine workers/audit/review36/check.py \
  --out workers/coded/extra43
```

This word is source-valid partial progress. It does not complete the remaining
68 outputs, provide ordinary/recursive supplier bounds, discharge the five
foundations, or prove a new kappa. Further work must physically use the real M1
imports, find broader simultaneous codes, and preserve the source and decoder
costs after any higher-cache changes. A separate source-level review is still
required before admission. Substantial AI assistance was used in the current
construction and finite certificate.
