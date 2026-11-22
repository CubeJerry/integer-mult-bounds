# Independent alternative fifth-receiver screen

**Accepted as an exact necessary-condition screen.** Targets 52, 54, 74,
85, 87 and 98 are not excluded. This is not an existence certificate,
a source-feasibility proof, or a new complete multiplication bound.

Author: @CubeJerry, with substantial OpenAI assistance. The review checks
`bit-coupled-fifth-s033/other-receivers` independently. It imports only the
independently written GF(64) arithmetic from the parent review directory,
and does not import or execute the construction screen.

## Exact result

The four retained spaces are the eight-column blocks of the fixed matrix
L, ordered 6, 9, 48, 73. Within this reduction, anchors 0, 61 and 62 force
the same two-dimensional space for each of the six targets. Anchors 45 and
100 contribute zero for those targets.

| Target | Active retained blocks | Joined forced dimension | Screen |
| --- | --- | ---: | --- |
| 52 | 6, 9, 48 | 2 | Not excluded |
| 54 | 9, 48 | 2 | Not excluded |
| 74 | 6, 73 | 2 | Not excluded |
| 85 | 6, 9, 73 | 2 | Not excluded |
| 87 | 9, 73 | 2 | Not excluded |
| 98 | 6, 9, 48, 73 | 2 | Not excluded |
| 95, negative control | 48, 73 | 4 | Excluded at eight donors |
| 6, retained positive control | 6 | 4 | Not excluded |

The dimension two is the output of this intersection reduction. It does
not assert completeness of all consequences of the fixed interfaces.
The seven native fifth candidates are independently enumerated from the
literal roots, D1509 chart and receiver indices below 111.

## Forced-space construction and hypotheses

H words, actual route owners and literal retained H interface actions are
fixed. The four retained D fibre subspaces im(L_r) are fixed. Compatible
D coefficients and arbitrary full linear source tuples may change; common
invertible D readout changes are allowed. The necessary argument does not
require the fixed 88-coefficient interpolation rectangle.

The verifier reconstructs each old whole target fibre U(a,t) by solving
its actual 96-row proper system, using the eight literal D inputs and the
old D section. Native retained H fibres are reconstructed from the old
source maps. Their visible spans define C(a,h) at each source quotient.

Intersect im(L) with C(a,h) at all four D1509 parents and with U(a,t).
At each of the sixteen target-visible source quotients, intersect again
with C(a,h), augmented, for non-D1509 parents only, by those L_r on which
retained whole D isolation prescribes zero source action. The resulting
K(a,t) has unchanged source action at every target-visible quotient under
the stated hypotheses. Every actual old off-target output vanishes on K,
including outputs outside the protected 96-row view; this is checked.
Any proposed common whole target fibre must therefore contain K.

The independent code computes the all-parent fixed intersections at all
eleven donors; only the five listed anchors have nonzero intersections.
Equality of column spaces is checked against the author's certificates;
no particular basis of K or the H cores is assumed.

## Necessary block-subset inequality

Write K=L W with eight-row blocks W_r. For every donor j, each of its four
D1509 parents h and each retained receiver r, reconstruct the full 30-by-30
H section B(j,h,r). All 176 sections are invertible and satisfy

\[
B(j,h,r)F_{old}(j,h)L_r S_{old}(j,r)=E(j,h,r),
\]

where E inserts the actual D inputs. Retained isolation thus forces

\[
F_{new}(j,h)L_r
=F_{old}(j,h)L_r S_{old}(j,r)S_{new}(j,r)^{-1}Q_r.
\]

The common readout Q_r may be any allowed invertible matrix. This uses all
thirty source rows and allows changes outside the old protected six rows.

Let M(j,t) be the old target off-output map on the active retained blocks
at the four parents. Whole target isolation on K necessarily requires

\[
M(j,t)X_j=0,\qquad
(X_j)_r=S_{old}(j,r)S_{new}(j,r)^{-1}Q_r W_r.
\]

For every nonempty subset A of active receiver blocks, invertible block
diagonal left multiplication preserves the rank of the stacked W_A. Hence

\[
\operatorname{rank}W_A\leq\dim\pi_A\ker M(j,t).
\]

All 1,474 such inequalities are checked across the nonzero anchor cases
and all native donors. A violation is an obstruction. Passing does not
supply compatible X_j, D sections, common readouts, source extensions,
full source rank verification, or a cost certificate.

## Actual off-output audit

For all 88 donor/target pairs (seven new targets plus retained target6),
the four parents have 120 distinct actual output owners. Eight are D1509
input owners. The independent map includes all remaining 112 outputs.

The author's sixteen off-output rows from the protected proper view have
exactly the same row space on the entire im(L) as these 112 actual rows,
in every one of the 88 cases. Including the other outputs therefore adds
no projection obstruction for the six targets.

The verifier reconstructs 201 native retained H fibres, all forty anchor
cases and 1,000 invertible full H sections. The latter include retained
sections, non-parent zero restrictions and forced-space output checks.
All literal geometry, matrices and author outputs are pinned.

## Controls, field and scope

Receiver95 at anchor61 reproduces the rejection at donors 32, 35, 38, 45,
68, 69, 90 and 100: required block rank four exceeds available projected
kernel dimension two. Retained receiver6 passes. A one-entry mutation of
a computed receiver95 kernel fails its exact annihilation identity.

Arithmetic is exact over GF(64), with polynomial x^6+x+1. Rank identities
persist under coefficient-field extension. Tensoring all maps and spaces
with k lanes scales ranks and dimensions by k. The necessary inequality
also applies when invertible changes mix lanes within retained blocks.
A passing scalar screen proves no existence at one or repeated lanes.

Changed H words, changed literal H interface actions and changed retained
spaces are outside the hypotheses. No compiler, instruction count or
complete source-feasibility replay was run in this review.

## Reproduction

From the repository root:

```sh
python3 -B research/moonshot-005-program/results/bit-coupled-fifth-review-s033/alternative-receiver-screen/check.py --repo . --out /tmp/s033-independent-other-receiver-screen
```

Expected: `PASS_INDEPENDENT_ALTERNATIVE_RECEIVER_NECESSARY_SCREEN`.
The output records all subset ranks and partition profiles. Exact input
hashes are in SOURCE-PINS.json. Prior review waves and the abstract
rank-two repair package remain unchanged.

## Open next questions

Construct compatible actual D sections and full source maps for one of
the six targets, or derive an obstruction beyond these inequalities.
Receiver54 has a separate continuation. A physical candidate still needs
whole isolation, every retained interface, full source ranks and cost.
