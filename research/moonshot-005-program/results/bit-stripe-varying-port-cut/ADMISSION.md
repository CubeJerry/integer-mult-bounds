# Aligned scalar stripes require more information than the balanced ports carry

**Admitted S023 checkpoint 2.** The fixed balanced native atlas cannot be
completed by scalar quotient rows acting separately on common aligned
stripes, even when every row varies independently with donor, plane and
stripe. Arbitrary nonlinear downstream processing is permitted. General
array maps that mix source stripes remain open.

This strengthens the [identically repeated-row gate](../bit-replicated-scalar-port-cut/ADMISSION.md).
At one stripe, each receiver's plane target defines a projective line.
A shared port can carry that stripe only when its receivers share the
line. Recoverability forces each receiver to belong to a monochromatic
port neighborhood. Thus the target lines form a partition into classes
that each have enough internal ports to cover all their vertices.

The [proof](author/PROOF.md) reduces the all-field, arbitrary-width claim
to exact finite partition decisions on the authenticated native incidence.
An exhaustive deterministic search has no timeout or numerical unknowns.
The [independent reviewer](review/REVIEW.md) uses a different color-domain
support solver, checks all111 receiver prerequisites, and reproduces every
one of1108 capped rank decisions:

| Native donors per plane | Maximum rank allowed by the port partition bound | Planes |
| ---: | ---: | ---: |
| 2 | 1 | 204 |
| 2 | 2 | 23 |
| 3 | 1 | 630 |
| 3 | 2 | 249 |
| 3 | 3 | 2 |

Granting every uncovered port and singleton source its full capacity,
all plane outputs together have at most538644r field dimensions. Correct
native recovery on the canonical-zero input slice requires587520r.
The strict information deficit is48876r for every positive r. This is
not a MOVE lower bound or a statement that all balanced array codes fail.

[The decisions](author/output/DECISIONS.json.gz) contain all finite caps and
positive color assignments. Independent controls cover small hypergraphs,
all four-vertex graphs,1225 common-function quotient pairs and81 aligned
stripe intersections. The nonlinear factorization and global cardinality
arguments are proved separately from these finite controls.

The common stripe indexing in actual source coordinates is an explicit
hypothesis. Arbitrary donor basis changes can leave this class. The next
source construction therefore needs genuine cross-stripe mixing or a
changed paid architecture, together with all source timing and global
compatibility equations. No new κ, supplier or foundation discharge.
Credit @CubeJerry, retained geometry/source authors, Worker A's scalar
port argument, root's extension and Worker B's independent review, with
substantial OpenAI assistance.
