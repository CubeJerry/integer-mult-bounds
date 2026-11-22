# The entire K remains forced under variable D and arbitrary full source recoding

**An interface lemma. All source quotient rows may change. H processing,
owner routing and the four literal retained fibre/readout systems remain fixed.**

Consider the old four-dimensional K inside donor61's entire receiver95/D1509
fibre. Let the physical D word change arbitrarily, retaining invertible donor
sections and the four literal common frames/readouts at6,9,48,73. Allow arbitrary
separate linear source quotient maps on each full480-coordinate source bank,
including all30 quotient output rows and mixing the96 protected coordinates
with the remaining384. Retain the literal native whole-H263/H642 interfaces.

Then all source/H proper records at donor61 and receiver95 have exactly their
old values on K. In particular the off-D records vanish, D ingress has rank4,
and K remains contained in donor61's entire receiver95 fibre. Consequently any
common entire receiver95 fibre must contain this K. This does not assume source
changes come from one invertible input gauge or from the44 protected local maps.

## Why D variation cannot remove this forced subspace

There are16 source quotients visible at95 for donor61. Four are D1509 parents:
263,481,642,947. For each, the entire K is contained in its prescribed native H
observation span alone. Those observations fix the whole30-entry quotient tuple
on K, independently of the proposed D matrix.

For each of the other12 quotients, K lies in the span of its prescribed native
H observations and whichever retained D frames are visible there. Because this
quotient is not a D1509 parent, its entire source tuple on each such retained
frame must be zero: all of its proper records are outside the allowed D1509
packet. The relevant complete H donor section is invertible, so zero proper
records force that zero tuple. These required values do not depend on D.

Hence changing D does not change any of the images used in the16 decompositions
of K. Linearity forces the old quotient values on every column of K. With the
H word and owners unchanged, every resulting proper record is old as well.

The original full H/interface argument in the S032 source-only obstruction
allows an arbitrary30-row source tuple: the old source phase frame is an
invertible normalization, and the actual complete H sections are invertible.
The present lemma removes its frozen-D premise for this particular forced K,
because the only D observations used away from the four parents are zero.
It does not relax whole-proper isolation into agreement of a few final outputs.

## Exact evidence

`forced_K.py` uses the own GF64 arithmetic from the parent package. It obtains
native H frames from S032's independent physical reconstruction and source
quotients from the admitted four-receiver word. It supplies an explicit
coefficient matrix for the full96-by-4 K at each of the16 visible quotients.
At the four parents the generators are H observations only. At each nonparent
it verifies the entire old30-row quotient is zero on every retained D-frame
column used. Thus the calculation does not silently fix only the six protected
output rows.

H333 and H906 see none of the four retained D receivers. Their decompositions
use native H observations alone. Removing those H observations leaves no
prescribed generator at these sites, showing why they cannot be omitted.
The checker also reconstructs the old protected proper restriction at95 and
checks zero on all88 off-D rows and rank4 on the eight D ingress rows. Its full
whole-fibre interpretation inherits the admitted S032 source/H interface.

```sh
python3 -B research/moonshot-005-program/results/bit-coupled-fifth-s033/wave3/forced_K.py \
  --repo . --out /tmp/s033-full-source-forced-K
```

Expected status: `PASS_FULL_SOURCE_VARIABLE_D_FORCED_FOUR_SPACE`.
Source pins and all16 decompositions are retained with the verification output.
The linear identities persist over coefficient extensions and after tensoring
with I_k; arbitrary separate full-bank linear lane mixing does not alter the
prescribed values on the embedded K tensor lane space.

## Consequence for the coupled continuation

This lemma combines with a universal off95 parent obstruction for the fixed
H/four-frame system: if some other donor necessarily has a nonzero proper
record outside D1509 on K, common entire receiver95 fibres are impossible.
That implication is valid even when all source quotient coefficients are
allowed to change, because K cannot be removed from donor61's fibre by those
changes under the retained literal interfaces. The off95 lower bound and its
independent review are recorded separately by the orchestrator and adversarial
worker; this file proves the forced-K premise.

The result does not exclude changed H words, changed owner routes, redesigned
retained common frames/readouts, cross-donor source coding, nonlinear maps or a
different isolation contract. Such changes require fresh mathematical and cost
accounting. No new complete exponent or foundational discharge.

Credit @CubeJerry, S031/S032 source/H and forced-collision contributors and
independent reviewers. Substantial OpenAI assistance. Apache-2.0.
