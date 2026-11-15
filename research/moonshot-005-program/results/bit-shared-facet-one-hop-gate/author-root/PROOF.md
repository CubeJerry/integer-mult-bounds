# A source-spreading requirement for shared-facet chart coding

**Proved under the precise one-hop source interface below; independently checked geometry and matrix controls; separate adversarial
review pending. No new κ.** The local MDS code does not solve simultaneous global
source formation. If banks are recoded only at their original root lines,
and each encoded bank then goes to one E6 chart, actual global information
has rank at least ceil(111b/4)V. A fixed rank9bV canonical supply cannot suffice.
This identifies a missing coefficient-spreading mechanism, not a lower bound
on arbitrary shared-facet coding or multiplication.

## 1. Exact source interface

Fix the111 authenticated native real lines L_j and facets F_j. Let b>=1 be
fixed, V>=1 and k any field. There are b independent width-V input banks per
root, n=111b in total, partitioned into111 root cohorts.

An arbitrary pre-encoder P_j acts on the b banks at L_j, including arbitrary
noncommuting V-by-V coefficients. Thus P=diag(P_j) is cohort block diagonal.
It may be invertible, but the lower bound does not need that. No cross-root
coefficient mixing has yet occurred.

Each encoded bank ascends directly from L_j to one proper chart C annihilating
an A2 plane of full E8 root normals: one of the28 E6 charts in a receiver's
atlas. Local operations may mix every carrier at C. Upward continuations can
serve any native facet containing C, then continue to Hub for restoration.
Banks at the same final facet can mix arbitrarily.

The local continuation does not gain access to a different lower chart or a
facet not containing C. This excludes additional descending local helpers,
public excursions and cross-root recoding below E6. Those are possible paid
escapes, not silently allowed operations. Additional nonlocal histories must
belong to the separately counted global space.

Grant arbitrary global X information with actual row-space dimension at most
gV, arbitrary availability and arbitrary output mixing. This favorable grant
counts coefficient modes, not packet identities. A changing packet may have
more history modes than lifetimes. Original Y inputs remain independent and
their coefficient equations are additional requirements.

Completion of all111b outputs implies, by linearity,

    I = G + U P,       rank G <= gV.                     (1)

U describes encoded-bank influence through the local E6/facet continuation.
Exact native geometry shows each E6 chart belongs to at most three native
final facets. A chart containing L_j cannot belong to F_j because L_j is not
contained in F_j. Therefore each column block of U reaches at most three
OTHER receiver cohorts, and U has zero diagonal cohort blocks.

Mixing within the first E6 chart preserves this facet set under the declared
continuation. Within-line pre-encoding can spread an input among banks, so P
must remain explicit: physical bank supports cannot be substituted for the
columns of UP. Arbitrary source/receiver operations are accounted for through
this factorization, not an assumption that actual input banks stay pure.

## 2. Transposed cohort filtration

Transpose (1): G^T=I-P^T U^T. Here P^T is cohort block diagonal, and every
acquisition row of U^T reads at most three other cohorts and none of its own.
The admitted cohort-order filtration theorem gives

    rank G >= V*ceil(111b/4).                            (2)

Briefly, order the cohorts and filter ker(I-P^T U^T) by prefix support. A row
is good when its cohort precedes all cohorts it reads. Good acquisition rows
vanish on that prefix, so its dimension increment is at most the number of
bad rows times V, even for singular P_j. Some order has at least the ceiling
of sum_alpha 1/(s_alpha+1) good rows. With s_alpha<=3, (2) follows over every
field and block width, without a commuting coefficient assumption.

Because111/4>9, rank9bV canonical global information is insufficient for every
b. At b16 the bounds are444V versus144V; after the fully paid five-bank binary
expansion b80 they are2220V versus720V. Increasing a fixed batch cannot fix
this source interface. Local MDS identities and one-receiver literal words
remain valid: they do not claim the full identity (1) on all111b outputs.

## 3. Quantitative condition on an escaping source

Retain cohort-diagonal P and the zero diagonal cohort blocks of U, but allow
encoded bank alpha to reach s_alpha OTHER receiver cohorts through its actual
continuation. Own-cohort support remains excluded throughout this relaxation. The same theorem and
Cauchy--Schwarz, for g=9b, imply

    sum_alpha 1/(s_alpha+1) <= 9b,
    sum_alpha s_alpha >= (111b)^2/(9b)-111b = 1258b.

Some bank must reach at least12 receiver cohorts; otherwise all s<=11 would
force rank G>=V*ceil(111b/12)>9bV. The strict one-E6-hop model supplies at most
333b incidences. These are necessary coefficient-support conditions, not an
unpaid routing recipe. Cross-root recoding at lower common charts, mixed or
nonlocal descending histories, several paid effective cells, or another
larger global space may change the premises. Actual formation, restoration,
ownership and the complete invoice must then be established.

The favorable shared-facet movement envelope near1614.675 is consequently
conditional on a stronger source. Its strict one-hop interpretation cannot
complete with only canonical global modes. A more powerful source can retain
the MDS local decoder; this is a continuation constraint, not its dismissal.

## 4. Geometry, dependencies and status

The geometric checker starts from the authenticated111 roots, closes their
exact reflections to the120 full E8 root lines, and identifies each A2 normal
plane by its three root lines. Each native facet has28 proper rank-six charts,
each native foreign root lies in16, and each chart belongs to at most three
native facets. Containment is checked by exact rational-span equations. The
application only needs the last bound and own-facet exclusion;16-fold coverage
is a compatible positive control, not global source formation.

The underlying matrix/aggregate theorems are already proved in
results/cohort-acquisition-rank/author/PROOF.md and COROLLARIES.md, with
independent C review. This package contributes their source-faithful shared-
facet application, not a renamed claim of novelty for the old theorem.
Small finite arbitrary-block and changed-support controls supplement the
universal proof. Credit @CubeJerry, native/filtration predecessors and the
established acyclic index-coding method, root's source-spreading reduction,
and C's local coding construction, with OpenAI assistance. No complete
supplier or foundational discharge is claimed.
