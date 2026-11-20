# Saturated native cuts exclude the high-grade-only observer repair at κ = 1/200

## Result and exact scope

Fix the 1,289 independent input fields, 1,289 output roles and exact target of
the authenticated #7830 rational native word at
`14c74c6a67108f675ac1196a5f2415ead0920e71`. Make the four endpoint changes of
the #7833 compensated surgery. Permit any positive integer number `k` of new,
fully paid, whole-field routes from chart 3 to chart 282. Permit deletion of
any retained old route, arbitrary local linear recoding, stored histories and
retiming. Do not change any other route endpoint or the original target.

**Saturated-cut theorem.** The following six high-grade occurrences in the
eleven-element S030 cycle roster are individually mandatory:

`43, 89777, 96404, 96513, 97320, 100120`.

This is true for every positive field width and every `k >= 1`, including
simultaneous deletion attempts. Four explicit cuts also prove necessity of
the other old occurrences listed below. Together with the inherited
circulation theorem, at least **1,071 of the 1,076 retained high-grade
occurrences are mandatory**. Only

`86, 97232, 97241, 97323, 99064`

remain possible high-grade deletions. Their total profile is `{3:1, 4:4}`.
Possibility here means only that these certificates do not exclude them.

**Tariff consequence.** If the repair deletes only high-grade old
occurrences, its optimistic complete-caller saving at κ = 1/200 is at most
16.900748035042 per native use, whereas the retained 48-call caller needs at
least 23.708028821921. The shortfall exceeds **6.807280786880**, even when all
otherwise required recoding and restoration are granted free. Extra parallel
observers make this bound worse. Thus this repair class cannot fund the
target κ = 1/200 price.

The cut theorem permits low-grade deletions too. The tariff exclusion does
not: low-grade savings, other new routes, endpoint retargeting, or a changed
target require separate analysis. No new complete κ or unconditional
multiplication theorem is claimed.

## 1. Source and canonical chart graph

The native compressed word has SHA-256
`1b1b3294e86979f1f41076fb056f3c0a08ace6df7bf80f2886bc579a22962f4b`;
its decompressed payload has SHA-256
`7660985e0b618cdbee13e4190a4c6d5f91fbdf01a8f7a5186fdde8b980c19b48`.
The existing compensated constructor removes occurrence 95914, redirects
94019 and 90369, and changes the sender of 88. Its genuine fifth-channel
control adds one paid 3→282 export and restores every original target row.
The new checker authenticates those sources and replays both complete words.
It separately verifies rank 1,289 of the complete target.

Identify charts with equal binary subspaces. This yields 1,102 canonical
vertices from 1,103 listed frames. Each paid occurrence is a directed
unit-capacity whole-field arc. All original input and output roles are
retained, including the 889 independent helper identities.

For each certificate in [CUTS.json](CUTS.json), let `J` be its ordered input
axes and `C` its listed blocked old occurrences. Delete `C` temporarily and
let `A` be the set reachable from the charts containing `J` in the graph
with one paid observer. This gives a finite, unambiguous definition of the
cut. The checker verifies that its actual outgoing boundary in the
undeleted graph is exactly `C`. In all four cuts chart 3 is outside `A`.
Therefore adding any number of further 3→282 observers adds no outgoing
capacity to these cuts.

## 2. Four exact minors and saturated boundaries

The terminal lists are in the same order as their input axes.

| Cut | Input axes | Terminal slots | Complete outgoing old boundary |
| --- | --- | --- | --- |
| 1 | 16, 51 | 154896, 154931 | 97320, 98954 |
| 2 | 30, 33, 49, 60, 81 | 154910, 154913, 154929, 154940, 154961 | 43, 89777, 96404, 97315, 98077 |
| 3 | 5, 29, 84, 96, 99, 104 | 154885, 154909, 154964, 154976, 154979, 154984 | 43, 89781, 96408, 96513, 97320, 98077 |
| 4 | 29, 35, 42, 48, 53, 72, 73, 79 | 154909, 154915, 154922, 154928, 154933, 154952, 154953, 154959 | 4, 91560, 96363, 96404, 96944, 97320, 98077, 100120 |

The exact target minors for cuts 1, 3 and 4 are respectively `I_2`, `I_6`
and `I_8`. Cut 2 has diagonal

`(1/2, 1, 1, 1/2, 1)`

and determinant `1/4`. Its halves are retained explicitly; using integer
row numerators alone would conceal them. Each chosen input is inside its
cut, and every chosen output is outside. The four minor ranks are thus
2, 5, 6 and 8, exactly their outgoing capacities.

### Rank-cut lemma

Let `A` be any set of physical charts. Suppose `r` independent original
input field directions inside `A` have an invertible scalar `r`-by-`r`
target minor at output fields outside `A`. At field width `V`, set all other
original inputs to zero. The outside responses have rank `rV` on those
selected inputs. If only `c` whole-field messages leave `A`, their aggregate
rank is at most `cV`. All later outside operations factor through those
messages and the fixed outside inputs. Consequently `c >= r`.

This remains true with arbitrary local linear operators, arbitrary stored
histories and arbitrary retiming. A fixed chart change is invertible and
does not change rank. At any column multiplicity, each scalar minor becomes
its tensor product with `I_V`; its rank scales by `V`. No one-column price
is substituted for a whole-field transfer.

Apply the lemma to each listed cut. Deleting even one member of its
boundary leaves at most `r-1` whole-field exports. Other old deletions can
only reduce that capacity. New parallel observers cannot increase it,
because their source is outside. Each listed boundary occurrence is
therefore mandatory in the stated route contract.

The union comprises 15 occurrences. Its intersection with S030's eleven
high-grade cycle candidates is exactly

`{43, 89777, 96404, 96513, 97320, 100120}`.

Seven other newly constrained cycle occurrences have grade one or two;
two further high-grade boundary occurrences were already forced by the
earlier circulation argument. This package does not claim that its four
cuts exhaust all saturated boundaries.

## 3. Combining with the existing circulation theorem

The S030 [paid-export sieve](../complex-native-paid-export-sieve/PROOF.md)
proves a necessary flow condition from the invertibility of the complete
target. The new checker reconstructs its relevant finite premises.

Every canonical chart of the original word is balanced after counting
input and output ports. For the compensated graph with `k` observer
exports, unused route capacity in any full 1,289-field flow has divergence

`k delta_3 - (k-1) delta_282 - delta_278`.

It decomposes into directed cycles and paths from 3 to 278 or 282. Chart 3
has no incoming route, and 282 cannot reach 278. Neither path region
contains an old route of grade at least three. Consequently every deleted
old high-grade occurrence must lie on a directed cycle. There are exactly
eleven such occurrences; this count is reconstructed from the canonical
route graph rather than read only from a receipt.

Six are excluded by Section 2. Therefore only the five listed remaining
occurrences can contribute high-grade deletion savings. Granting all five
simultaneously is an optimistic upper bound; no code realizing those
deletions has been constructed.

## 4. Complete cost comparison

Put `t = 1-kappa`. The literal four-channel endpoint surgery saves

`3^t + 5^t - 7^t`

relative to the original native. Each genuine added observer costs `3^t`.
The maximum remaining high-grade deletion moment is bounded by

`4*4^t + 3^t`.

Thus with `k >= 1` observers the optimistic net saving is at most

`G_k(t) = 4*4^t + 3^t + 5^t - 7^t - (k-1)*3^t`.

The retained caller's required gain per native use is computed from its
actual complete invoice:

`R(t) = M(native,t) - M(helpers,t) + [M(fixed_paid,t)-M(fixed_root,t)]/48`,

where `M(profile,t) = sum count_r*r^t`. This retains the productive helper
fields, all 48 native calls, and every fixed caller charge. It is not a
component-only comparison.

| κ | Maximum optimistic net gain, `k=1` | Required complete-caller gain | Remaining margin |
| --- | --- | --- | --- |
| 0.0043 | [16.914612057142, 16.914612057143] | [8.901591739208, 8.901591739209] | [8.013020317933, 8.013020317934] |
| 0.005 | [16.900748035041, 16.900748035042] | [23.708028821921, 23.708028821922] | [-6.807280786881, -6.807280786880] |

The exact rational outward bounds are retained in the receipt. The
inherited dyadic square-root power engine bounds every exponentiation;
displayed decimals are outward rounded. At κ = 0.005 each additional
observer costs more than 2.983565993496, so `k > 1` cannot repair the
negative margin in this class.

At κ = 0.0043 the optimistic screen leaves about 8.013 units for other
costs. This is a necessary budget, not a source construction, supplier
admission or complete multiplication result. Even the five remaining
deletions may prove impossible.

## 5. Verification and classification

Run from the repository root with Python 3 and the standard library:

```sh
python -I -B research/moonshot-005-program/results/complex-paid-export-s031-repair/author/check.py --repo . --out /tmp/s031-complex-rank-cuts
```

Expected marker:

```text
PASS_S031_SATURATED_COMPLEX_CUTS_AND_HIGH_GRADE_SCREEN 4 6 5
```

The verifier authenticates sources, replays the original and genuine
fifth-channel target, verifies full rank, constructs each cut from its
small seed certificate, checks every actual outgoing route, and tests the
exact nonzero diagonal minors with their denominators. It reconstructs
the circulation roster and evaluates both complete tariffs. Mutations of
a terminal and a boundary occurrence are rejected. Actual removal of each
mandatory export is checked against its capacity deficit.

A mixed-integer search suggested the cuts. Its time limits and numerical
bounds are not proof evidence and are not imported by the checker. The
final verification uses no optimizer, search routine or floating point.
The theorem concerns the fixed source atlas at all field widths; the
finite graph/minor certificate is not being extrapolated to a different
atlas. Independent review is required before programme admission.

## Open next questions

1. Which of the five remaining high-grade cycle occurrences, or the
   remaining low-grade cycles, also lie on saturated multi-source cuts?
   Start with a cut containing an occurrence's tail but not its head, and
   seek a full-rank outside minor of the same boundary size.
2. Can low-grade cycle/path deletions fund the remaining .005 shortfall
   while preserving every independent helper output? Their full paid
   profile and the actual observer count must be included.
3. If a cut is repaired by another new route or an endpoint change, does
   that paid route fit a legal nested native interface, carry the needed
   independent information, and preserve every downstream target? A
   restored cut capacity alone answers none of those questions.

Credit the Clear1nsight #7830/#7833 source lineage, the S030 paid-export
circulation sieve, the retained P104 caller and their notices. Prepared
for @CubeJerry with substantial OpenAI assistance. No new κ.
