# Third overlap, a disproved invariant, and the overlap method's exact ceiling

## Exact new point

The S033 construction worker added a third row-space overlap at retained
receivers 48 and 73. Its common row has zero profile on the four fixed input
coordinates F={4,5,7,8}. The projection identity proved in the parent package
therefore makes that row annihilate every donor image B(j), not merely their
contrasts. Its restriction to the 32 native input coordinates is nonzero.

The independently rechecked exact matrix has

    rank span_j B(j) = 31,
    rank Z = 27,
    rank[Z B(61)] - rank Z = 4.

This is a counterexample to the conjecture that the native donor images must
always span all 32 coordinates in the admissible affine D family. The saved
matrix has both invertible phase blocks and all 44 exact local interpolation
conditions. The author verifies all 144 geometric sections; the independent
wave-two checker separately verifies all 132 sections involving an actual
native donor and any geometric receiver, using the inherited labelled section
lists and independently written GF(64) arithmetic.

The five shared native rows comprise the original two shared outputs, the
two previous extra profiles, and the new zero-profile row. They are independent
as native row functions, annihilate Z, and give a rank-four common response.
The actual eight receiver-95 outputs still have nonzero contrast response of
rank six. The necessary physical gate rank Z<=24 is not met: three further
contrast ranks remain to be removed.

## A rigorous ceiling for the row-overlap construction

This is a method-specific ceiling, not a universal lower bound on Z.

The full physical T is invertible. The union of O(48) and O(73) contains
14 distinct rows, so those rows have rank 14 on all 35 input coordinates.
Restricting to the native union V deletes exactly three columns. Therefore

    rank T[O(48) union O(73),V] >= 11.

Each of the two separate receiver row spaces on V has dimension eight,
because it contains an invertible native eight-column section. Consequently

    dim(row T[O(48),V] intersect row T[O(73),V]) <= 8+8-11 = 5.

The new matrix attains equality: the join has rank 11 and the intersection
has dimension five. The displayed two-receiver overlap mechanism is therefore
sharp within this contract. Adding further independent row overlaps cannot
preserve full-word invertibility and all native section ranks.

A complete receiver-95 response requires eight independent native rows
annihilating Z. Since at most five can belong to this two-receiver intersection,
at least three independent rows of a successful actual receiver must lie
outside it. Equivalently, a successful continuation needs a mechanism that
produces common rows beyond the current overlap construction.

It would be invalid to infer rank Z>=27 from this statement. The intersection
is a proved subspace of the annihilator of Z, but equality with that
annihilator has not been established for every admissible matrix. Exceptional
common rows outside the intersection remain open.

## Independent review of the full source-gauge theorem

The root's [global gauge theorem](../../bit-global-gauge-lift-s033/PROOF.md)
is sound. Its exact full-H intersection identity shows that the desired
automorphism of the four-frame span fixes its overlap with the full retained
H core pointwise. Combining it with identity on that H core and identity on
a complement gives an invertible source map G(j). Composing every source
quotient on the right by the same G(j) preserves all source restriction ranks
and propagation dimensions exactly. This justifies source-view invertibility,
strict nonsaturation and genuine early preparation by a linear-algebra proof,
without relying on the failed arbitrary 44-map extension.

The independently checked third-overlap lift has eleven rank-96 gauges.
For each donor the reviewer reconstructs the full H core from the pinned
whole-H fibre columns, checks the exact intersection dimension, verifies
G(j)H(j)=H(j), and verifies the four oriented frame equations and their inverses.
At donor 61 it also checks G(61)K=K. Recomputing actual ingress as P(j)G(j)K
agrees exactly with the section-inverse formula used in the rank calculation.
This establishes a valid full-source extension for the new rank-27 point.

These are algebraic source-validity statements. The full-source ranks and
nonsaturation are inherited by the proved composition, rather than being
claimed as a fresh exhaustive replay of all predecessor views. A changed
source compiler invoice remains a separate dependency. Source right-gauges
and invertible D section changes cannot repair the previously unequal joined
whole-fibre diagrams; the gauge lift itself does not supply a fifth receiver.

## Next obligation and limits

The immediate necessary condition remains rank Z<=24 together with equal
actual receiver-95 outputs and full whole-fibre validity. The current point
has rank 27, so a new mechanism is required. No finite search failure or
generic-rank observation is promoted into a no-go theorem. Both strict
suppliers, complete paid return and caller, and all five foundational
assumptions remain open. No new complete kappa.

## Reproduction

From the repository root:

```sh
python3 -B research/moonshot-005-program/results/bit-coupled-fifth-review-s033/wave2/check.py \
  --repo . --out /tmp/s033-three-overlap-review \
  --candidate research/moonshot-005-program/results/bit-coupled-fifth-s033/THREE-OVERLAP-CANDIDATE.json.gz \
  --gauges research/moonshot-005-program/results/bit-global-gauge-lift-s033/output-three-overlap/GAUGES.json.gz
```

Expected status: `PASS_INDEPENDENT_THREE_OVERLAP_REVIEW`. Source hashes,
the five common rows, the zero-profile annihilator, the eleven gauge review
records, and the exact ranks are retained beside this review. This checker
does not execute the author's constructor or the root's gauge verifier.

Credit @CubeJerry, the retained S031/S032 sources and reviewers, the S033
construction worker and root gauge proof. Substantial OpenAI assistance;
independent agent proof and arithmetic review, not human/kernel certification.
Apache-2.0.
