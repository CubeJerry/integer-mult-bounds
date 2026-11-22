# Receiver87 phase audit: early rank one remains possible

**The proposed phase argument does not exclude receiver87 with arbitrary
common invertible readouts.** Its donor0 premise is false: donor0 has five
early inputs and three late inputs, not four of each. The exact necessary
condition is that the physical pinned profile have early rank one. A small
abstract code satisfies all eleven native pair tests at that rank.

Author: @CubeJerry, with substantial OpenAI assistance. This is a new frozen
review. The receiver54/74 package remains unchanged. No search or compiler
was run, and no whole receiver87 construction is claimed.

## Literal chronology and the corrected bound

The D phase split is19 early and16 late coordinates. Both retained output
sets O9 and O73 contain four early and four late rows. The only native donors
containing the pinned pair4,5 are:

| Donor | Early inputs | Late inputs | Required lower bound on profile early rank |
| --- | ---: | ---: | ---: |
| 0 | 5 | 3 | 1 |
| 61 | 6 | 2 | 0 |
| 62 | 5 | 3 | 1 |

In particular I0=[0,3,4,5,15,19,20,22]. Let P be the two-dimensional physical
span of receiver columns4,5, and let p be its early projection rank. If a
section has e early inputs including those two, its four early output rows
have rank at most (e-2)+p. Invertibility therefore requires p>=6-e, giving
only p>=1 from donors0 and62.

The previous exact union calculation puts input27 in the constrained input
span. Hence the physical column27 lies in P. It is late, so its early
projection is zero. Native donors35 and45 contain input27; retained section
invertibility requires that column to be nonzero. Therefore P has a nonzero
purely late vector and p<=1. Combining the bounds gives exactly p=1.

The same reasoning applies to late input31. No native input set contains
both27 and31, so their required proportionality within the one-dimensional
late part of P does not itself force a native section singular.

With literal readouts Q_r=I, the old pinned profiles have early rank two;
the checker verifies this for both r9 andr73. That narrower phase-preserving
literal-readout subfamily is excluded. Arbitrary common Q_r can move the
physical profile to early rank one, so that conclusion does not extend to
the requested common-readout family.

## Exact abstract U-code positive control

The constrained input union has coordinates
U={2,4,5,14,16,17,27,31}. Use a two-dimensional profile with first basis vector
early and second basis vector late, and assign:

| Input columns | Image |
| --- | --- |
| 2,4,14,16 | e1 |
| 5,17 | e1+e2 |
| 27,31 | e2 |

Its early projection is (a,b)->a and has rank one. Every native intersection
with U is one of {4,5}, {16,17}, {2,27}, {14,31}. Each pair has rank two.
The checker verifies all eleven native pairs explicitly. This is an
abstract U-code and supplies no D word or source extension.

## Counterexample to the disputed section inference

For additional direct verification, the certificate embeds e1 in an early
output row and e2 in a late output row, and extends the above U-code to a
partial8-by35 physical receiver-row map. Its donor0,32,35 sections are each
invertible, all late-to-early entries vanish, and columns27 and31 are
nonzero. The donor0 pinned columns have full rank two but early rank one.
Thus invertibility and phase compatibility do not imply the proposed early
rank-two premise, even while the relevant late-column donor sections pass.

For each of r9 andr73, an explicit invertible common Q_r is also saved,
mapping the old pinned columns4,5 to this profile. Columns7,8 are assigned
so that all four normalized fixed-column identities hold. Every constrained
union column maps into the profile. These are separate partial receiver
row models: they do not check all native sections, shared physical rows,
the complete D phase blocks, H/source feasibility or cost.

## Field, lanes and reproduction

The audit uses exact GF(64) arithmetic; the abstract U-code itself uses only
zero andone. The counterexample and rank reasoning persist under field
extension. For k repeated lanes, the corresponding necessary early profile
rank is k, and the positive control tensors with the identity on those
lanes. No inference from random failures is involved.

From the repository root:

```sh
python3 -B research/moonshot-005-program/results/bit-coupled-fifth-review-s033/target87-phase-gate/check.py --repo . --out /tmp/s033-receiver87-phase-audit
```

Expected status: PASS_RECEIVER87_PHASE_PREMISE_AUDIT. The output contains
the complete phase census, all eleven pair checks, explicit partial maps,
common readouts and normalized pin checks. Input hashes and the verification
receipt are included. Receiver87 remains unexcluded in the common-readout
model and is only a next investigation target.

## Open next questions

A receiver87 construction would need compatible shared physical rows,
all required phase and section determinants, actual whole source isolation,
full source ranks and cost. The abstract rank-one early profile is a concrete
starting constraint, not a solution of those obligations.
