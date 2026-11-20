# Five closures require the old inverse fibres to move

## Precisely scoped proposition

Retain the 101 native common inverse-fibre subspaces of the hybrid
H263/H642/H135 word in this directory, in the same original input
coordinates. Allow arbitrary new **linear** source maps on the seven
existing donors, including arbitrary mixing of all 3840 fields across the
marked/unmarked components and all spinor lanes. Require each actual
native source cut to remain invertible. Central source maps, the four
flexible quotient maps, and all new H/D/K/facet maps may be changed freely
subject to these retained fibres and source cuts.

Then no fourth native centre containing at least two of these seven donors
can have the required common 240-dimensional source inverse fibre. All
five possible new centres are excluded. This proposition does not retain
whole point-table equality as a premise. It does retain the 101 named
native inverse fibres. Moving those fibres is outside its scope.

## 1. Saturated observations are forced

For a source flag (j,Q), take the span S_(j,Q) of the retained native
K_(H,i) whenever j belongs to H, Q differs from H, and receiver i sees
both Q and H. Every row of any new quotient F'_(j,Q) must annihilate this
span: it is among the observations that vanish on each retained inverse
fibre.

For every flag used by the witnesses below, the exact component ranks
give

\[
\dim S_{j,Q}=15k,\qquad
\dim S_{j,Q}^{\perp}=k.
\]

Thus, over the full bank, the annihilator has dimension

\[
16(3+12)=240.
\]

The quotient is visible in a required native source cut, so that cut's
full rank forces its quotient rank to be 240. Its row space must
therefore equal the entire 240-dimensional annihilator. This remains true
when the replacement mixes all bank coordinates: it is a dimension
argument on the full original bank, not a restriction to the displayed
component decomposition.

Only the 101 native fibres are used to compute these annihilators.
Nonnative completion receivers are not needed for this proposition.

## 2. Sixteen forced quotients leave no common direction

There are exactly five native H planes, other than the designated three,
containing at least two of the seven existing donors. For each, the saved
certificate lists 16 forced off-centre source flags seen by one actual
native receiver. None of the listed flags is a designated central plane
or one of the four flexible flags. Their quotient row spaces have the
following stacked ranks.

| Proposed H | Existing donors in H | Witness receiver | Marked scalar rank | Unmarked scalar rank | Full-bank rank |
| ---: | --- | ---: | ---: | ---: | ---: |
| 44 | 0, 25 | 2 | 48 | 192 | 3840 |
| 116 | 0, 45 | 1 | 48 | 192 | 3840 |
| 394 | 25, 61 | 5 | 48 | 192 | 3840 |
| 643 | 62, 100 | 18 | 48 | 192 | 3840 |
| 652 | 47, 100 | 0 | 48 | 192 | 3840 |

Any common inverse fibre for the proposed centre and this receiver must
vanish on the off-centre observations of every existing donor in the
centre. In particular it must lie in the kernel of these 16 forced
quotients. Their stacked rank is the whole bank, so this kernel is zero.
It cannot contain the required 240-dimensional common inverse fibre.

The argument ignores all central and flexible rows. Changing them,
changing the H coding word, and changing downstream words cannot remove
this contradiction while the named old fibres and source cut ranks are
retained. The construction of a fourth centre must move at least one of
those fibres, or change some other stated premise.

## Exact certificate and replay

`output/CLOSING-WITNESSES.json` contains the five lists of 16 actual
(donor,plane) flags. `check_closing.py` reconstructs the old hybrid fibres
and their native-only annihilators, checks every flag's saturation and
receiver incidence, exhausts the native H list for other candidates, and
replays both full component ranks. The full-bank statement follows by
the displayed direct-sum dimension calculation and then applies to
arbitrary full-bank replacement maps.

As a negative control, removing one block from any saved witness lowers
its component ranks to 45 and 180, giving full-bank rank 3600. This is a
check of the rank witness, not a claim that removing one block repairs
the complete model, which has additional observations.

Run from the repository root:

```sh
python -B research/moonshot-005-program/results/bit-coupled-native-three-chain-source/fibre-only/check_closing.py --repo . --out /tmp/fibre-only-closing
```

The positive donor-dependent source, its original-owner invoice and its
common-fibre verification are separate claims in `PROOF.md` and
`check.py`. No general impossibility for four-centre constructions or
for the native target is asserted.
