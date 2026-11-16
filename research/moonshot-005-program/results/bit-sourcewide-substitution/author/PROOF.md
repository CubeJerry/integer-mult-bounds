# Source-wide substitutions and three actual lower triples

## What is proved

Starting from the actual 43-output word after root's raw2/BACK2 replacement,
three successive source changes add outputs 8, 9 and 36. All old outputs and
all original records are preserved. The final word therefore completes
**46 of 111 outputs**, including every member of the previously obstructed
set `{8,9,36,37}`.

The construction is a source-valid escape from the fixed-history and
late-injection obstructions. Its source caches and matching Hub reads change
together. It is not an endpoint-cost optimum: root has subsequently found
cheaper paid direct-return alternatives after removing narrow point services.
The reusable result here is the exact source-substitution mechanism and its
physical realization, with all cost and lost source contracts stated.

The initial word is pinned by
`0fa6fd43de9e1782168ed811f39110cfd58f8035f5e90fc81c92c859fd2df96c`.
The native source remains pinned by
`8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e`.

| Stage | New output | Word SHA256 |
|---|---:|---|
| 44 outputs | 8 | `f4a27a72484db22126f93cd7d8544e60b26bf5d6138f734bc66985a5e8c8a75f` |
| 45 outputs | 9 | `6427be84494f45664aa3312ade2955b6d694e7eab475804c4262faf05a4af01a` |
| 46 outputs | 36 | `45479de20faad9d9cd4ace9493057b82fb2c8b6f8baa4ac67134571f2e5cca84` |

## Source-wide substitution lemma

Let a linear characteristic-two record word have independent original columns
`X_i` and arbitrary original `Y_i` columns. Suppose original `X_b` is never a
destination of ADD, so it is an immutable raw donor. Define the invertible
column substitution

\[
T(X_b)=X_b+X_c,\qquad T(X_i)=X_i\ (i\ne b),\qquad T(Y_i)=Y_i.
\]

Suppose every old use of the raw donor `X_b` can be replaced by a chronological,
co-located read of the actual row `X_b+X_c`. This may use an actual coded cache
at a lower chart or two actual raw reads at a common upper chart. Require that
all other operations receive their transformed input rows, and that any
retimed cache writes have completed before their first dependent read.

Then every computed record other than the deliberately untouched original
`X_b` is transformed by `T`. This follows by induction: zero initialization and
ADD commute with `T`, and MOVE does not change a row. At a use of the exceptional
raw donor, the stipulated actual replacement supplies its transformed row.
The original donor itself remains restored automatically because it was never
modified. Every other restored original remains its same original column.

Consequently, among the old diagonal output equations, only the completed
output `Y_b` changes: its increment becomes `X_b+X_c`. Every other old completed
output remains correct. A physical decoder can repair `Y_b` and add `Y_c`
using this coupled direction. The lemma does not grant the coded source or its
transport: source availability, legal chronology, chart geometry, scratch
ownership and all movements remain separate sufficient hypotheses.

The argument works for all characteristic-two fields and every positive
whole-record width. The concrete construction below uses only literal binary
coefficients. It does not assert a general arbitrary-field minrank optimum.

## Three literal substitutions

| Packet | Old terminal `a` | Old retained point `b` | New point `c` | Substitution |
|---|---:|---:|---:|---|
| `P2` | 12 | 39 | 8 | `X39→X39+X8` |
| `P1` | 11 | 38 | 9 | `X38→X38+X9` |
| `P0` | 7 | 30 | 36 | `X30→X30+X36` |

In each row the three native roots are pairwise orthogonal. The old retained
point and terminal formed an actual lower pair: the packet loaded raw `X_b`
at its rank-four chart `J`, descended to `L_a`, retained `X_b`, reset, and
loaded raw `X_a` for its ground terminal.

The old imports `IMPORT_E8`, `IMPORT_E9`, and `IMPORT_E36` are **consumed and
repositioned**. They no longer hold the old pure E rows at `M1`. Their new
values are the three coded pairs, and their new endpoints are the corresponding
rank-four charts `J22`, `J23`, and `J16`. Claiming that the original three M1
source contracts survived would be false.

## Actual coded source and cache repair

Write `H=Extra6` (rank six), `S=M0` (rank five), and let `J` be the packet's
rank-four chart. Introduce planes

\[
K=\operatorname{span}(L_a,L_b),\quad
A=\operatorname{span}(L_c,L_b),\quad
B=\operatorname{span}(L_c,L_a).
\]

All three planes lie in `H`; `K⊂J⊂S⊂H`. The new original routes are

* `X_b: L_b→A→H→Hub`;
* `X_c: L_c→B→H→Hub`.

At `A` and `B`, actual raw correction rows are captured in stationary owners.
Native-line raw captures of `X_b` and `X_c` are also made before departure.
At `H`, first the actual original `X_b` and later the actual original `X_c`
are added into the existing import owner. Thus its actual row is `X_b+X_c`.
The import then moves `H→S→J`, with both owned rank-one moves counted.

At `S`, the actual coded import contributes to every cache that previously
received raw `X_b`. The complete cache lists and actual matching Hub loads are
recorded in each stage's result. `PRIVATE22` and `PRIVATE23` are retimed to
`M0`: their other actual originals already visit M0, and their packet query
moves to immediately before its descent to J. `PRIVATE16` was already at M0
after the source50 repair and remains there.

Every old Hub use of `X_b` also adds the actual original `X_c`, at Hub. This
is essential. Replacing only lower caches, or only the late common payload,
does not implement the column substitution and fails the endpoint equations.

The old private/cached sums need not retain their old literal values. Their
values are exactly `T(old value)`. This is the difference from the earlier
raw50 repair, which paid a separate import to preserve every old cache row.
Here the consistent substitution avoids that second import.

Before `P7` is born, the builder checks every inherited field against the
literal substitution. The only declared exceptions are the removed old raw-J
owner, the repurposed import owner, and the untouched raw original `X_b`.
There are no unmatched inherited-field values. This check covers the actual
source inventory, including temporarily modified original records, not merely
the intended final common codes.

## Actual lower triple decoder

At J, the packet reads the actual coded import `X_b+X_c`. It descends to K,
retains that row in its existing lower-memory owner, descends to `L_a`, adds
the actual raw `X_a`, and continues to ground. The old reset is removed.
After subtracting any actual existing ground mask, the terminal code is

\[
C=X_a+X_b+X_c.
\]

The P2 terminal retains the existing mask `E77`; P1 and P0 need no such mask.
All mask reads are explicit in the word.

| Receiver | Ground preload | Actual subsequent reads | Nested route |
|---|---|---|---|
| `Y_a` | C | native raw `X_c`, then raw `X_b` at A | `zero→L_c→A→F_a` |
| `Y_b` | C | existing raw `X_a`, then raw `X_c` at B | `zero→L_a→B→F_b` |
| `Y_c` | none | native raw `X_b`, then retained `X_b+X_c` at K | `zero→L_b→K→F_c` |

The chart inclusions follow from pairwise orthogonality and are checked over
the exact rational native roots. Every source correction copy is chronological
and co-located. The coded import is already at J before the packet reads it.
No arbitrary source bank, free raw local, cloned original or uncounted descent
is used.

This is a two-source-chart extension of the nested-retention triple lemma.
The native line `L_c` need not lie in J: the actual coded pair is formed higher
at H, and its paid import supplies it to J. Correction source routes remain
inside H.

## Complete movement and ordinary counts

For each of the three upgrades, the signed movement changes are:

| Changed path | Increment, with `[d]=d^(199/200)` |
|---|---|
| Original b: old `L_b→J→S→Hub`, new `L_b→A→H→Hub` | `[4]+[2]-2[3]` |
| Original c: insert B before H | `[1]+[4]-[5]` |
| Existing import: old `H→M1`, new `H→S→J` | `[1]` |
| Packet: insert K before `L_a` | `[2]+[1]-[3]` |
| Y_a decoder | `2[1]+[5]-[7]` |
| Y_b decoder | `[1]+[5]-[6]` |
| New Y_c decoder | `2[1]+[5]-[7]` |

The exact total is

\[
\Delta=8[1]+2[2]-3[3]+2[4]+2[5]-[6]-2[7].
\]

Its linear rank-volume is one. Its concave movement moment is enclosed by

`[1.08911998477517025298152011762527,`
` 1.08911998477517025298152011762539]`.

| Targets | INIT | ADD | MOVE | Dirty CLEAR | Movement moment, approximate | Necessary room, approximate |
|---:|---:|---:|---:|---:|---:|---:|
| 43, root raw2 base | 130 | 834 | 490 | 130 | 1617.19769371800701 | 4.55318649314534 |
| 44 | 133 | 846 | 498 | 133 | 1618.28681370278218 | 3.46406650837017 |
| 45 | 136 | 858 | 506 | 136 | 1619.37593368755735 | 2.37494652359500 |
| 46 | 139 | 869 | 514 | 139 | 1620.46505367233252 | 1.28582653881983 |

The final complete movement profile is

`{1:217, 2:46, 3:49, 4:18, 5:82, 6:20, 7:82}`.

The exact final movement interval is

`[1620.46505367233252109368552844601349,`
` 1620.46505367233252109368552844601646]`.

The corresponding necessary limiting room is at least
`1.285826538819834152560621920977415`.

All ordinary INIT, ADD, MOVE and dirty CLEAR counts are reported. The fixed
integer-200th-root method gives rigorous directed movement intervals, but this
does not supply a complete ordinary or recursive supplier invoice.

## Scope controls

At every stage the independent interpreter replays all 222 arbitrary initial
columns and all chart directions, co-locations, original restorations,
requested output increments and owner retirements. Eleven single omissions
and a collective deletion of all matching Hub substitution reads are rejected.
The collective test is a negative control for the claimed coupling mechanism:
the actual coded lower source alone is insufficient.

The finite proof does not complete the remaining 65 outputs, solve unrestricted
source/decoder fitting, prove the selected exponent, discharge the five
foundations, or imply optimality. Root's later cheaper point-service variants
are separate actual source interfaces and must be compared by their retained
information and costs, not by target counts alone.

## Reproduction and next questions

```sh
python3 -B workers/coded/build_encoded_lower_triples.py \
  --repo programme --base workers/coded/extra43-raw2/WORD.json \
  --engine workers/audit/leaf-capacity-gate/check.py \
  --price-engine workers/audit/review36/check.py \
  --out workers/coded/encoded-lower-triples --stages 3
```

The source loader is `workers/coded/source_loader.py`. Stage words and results
are written under `outputs44`, `outputs45`, and `outputs46`; `CHAIN.json`
records the authenticated dependencies.

Next work should compare this changed source/common interface with the cheaper
actual raw-return alternative, determine which retained rows are indispensable
for a larger simultaneous code, and use source-wide substitution only when it
gains source or delivery capacity at a competitive complete cost. Further
local triples alone are not a proof of a complete supplier.

Predecessor construction, source-recovery, root cost repairs, and independent
audit work retain their attribution. Substantial AI assistance was used in this
source construction and finite evidence.
