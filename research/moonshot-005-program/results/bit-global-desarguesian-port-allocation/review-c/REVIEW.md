# Independent review of the global Desarguesian port allocation

**Accepted within the geometric scope.** The supplied witness marks 630 of the actual 3,150 D charts, is invariant under the actual perpendicular involution, and induces a Desarguesian nine-line singular spread at every one of the 1,120 actual H charts. It extends the nine actual ports of the new H263 component. All 30,240 point reservations, 40,320 parent/receiver views and 37,800 D/donor profiles pass exact independent checks.

This review certifies a global allocation and its local finite-field geometry. It does not certify a source word, a shared D/K/facet word, literal original-owner timing, an invoice, or a larger κ.

## Independence of the computation

The reviewer imports no author implementation and no preceding geometry implementation. `check.py` reads only the pinned atlas, quadratic-basis data, submitted marking/field-operator witness, old marking and the new H263 component parameters. The component parameter file is checked against its frozen manifest.

The proof kernels differ from the author implementation in three substantive ways:

1. The native roots are reconstructed by exact integer back-substitution in the supplied triangular lattice basis. For all 256 binary coordinate vectors, the reviewer also checks the physical lattice identity `q(v)=||v||²/4 mod 2`. Thus the hyperbolic coordinate convention is verified against actual lattice representatives rather than assumed.
2. The complete A2 and D4 atlases are regenerated from the quadratic space. The reviewer enumerates all anisotropic planes directly. For each of the 1,575 totally singular radical lines, its perpendicular contains 24 nonsingular vectors; the graph joining vectors of polar product one has two components of size 12. Those components are precisely the two native D4 charts with that radical. Their union over every radical equals the supplied 3,150-chart atlas.
3. Local endomorphisms use a row-major 6-by-6 unknown matrix and least-pivot binary elimination. Maximal singular subspaces are enumerated independently through their unique reduced row-echelon bases, rather than by the author's iterative subspace extension.

All arithmetic is integer or binary arithmetic. No floating point, optimization package, author code or accelerator is used.

## Actual atlas, duality and receiver checks

The 120 root coordinates are distinct and are exactly the nonsingular vectors of the 8-dimensional plus quadratic space. The regenerated atlas has exactly 1,120 anisotropic planes and 3,150 D4 charts. The native perpendicular table agrees with direct bilinear orthogonality on all 256 points.

The 630 selected D labels correspond to exactly 315 distinct singular radical lines, with both perpendicular D charts selected together. Every D has exactly 16 parent H planes, and each of its 12 root donors lies in exactly four of those parents. This independently establishes all 37,800 D/donor flag counts.

For each actual H, its perpendicular has 64 vectors, of which 27 are nonzero singular vectors and 36 are nonsingular vectors. Its 45 native D ports contain exactly nine selected ports. The nine selected radicals partition all 27 singular vectors once each. For each of its 36 nonsingular receiver vectors, exactly 15 ports are visible and exactly three of those ports are selected. The aggregate counts are 30,240 point checks and 40,320 receiver checks; the first 111 native receivers account for 37,296 of those views.

## Desarguesian structure is checked directly

The supplied six-vector coordinate basis spans the literal H-perpendicular space in every case. Each packed field operator is range-checked, is an invertible binary linear map, preserves the actual quadratic form, and satisfies

\[
J^2+J+I=0
\]

on all 64 vectors. The irreducible polynomial gives a faithful scalar action of F4 on the 6-dimensional binary space.

The reviewer reconstructs all 21 nonzero F4 orbit lines

\[
\{0,x,Jx,J^2x\}.
\]

These lines partition all 63 nonzero vectors. Exactly nine are singular for the quadratic form, and those nine are exactly the selected native D radicals. This checks the full Desarguesian spread and its singular nine-line part, rather than inferring the claim solely from point counts or line preservation. Across all H charts, 23,520 orbit lines are checked.

The space of binary endomorphisms preserving each of the nine marked lines has dimension exactly two in all 1,120 cases. The identity and the supplied J are independent elements of it, so the complete endomorphism algebra is exactly

\[
\{0,I,J,I+J\}\cong\mathbf F_4.
\]

Its two nontrivial field generators are J and J². The reviewer checks the conjugate generator as a positive control at every H and verifies that it produces the same 21 orbit lines. This establishes uniqueness of the local field action up to its two conjugate generators. It does not assert that the local J operators glue to a single operator on the whole 8-dimensional space.

## Binding to the new component and separation from old allocations

The selected ports at H263 are exactly

```
110, 132, 720, 810, 1509, 1735, 1994, 2621, 2836.
```

They agree with the actual frozen `component/output/PARAMETERS.json`, not only with a literal list in the author's checker. The new global selection differs from the preceding orthogonal-spread selection in exactly 840 D labels.

Unique RREF enumeration gives the complete counts of totally singular subspaces in dimensions one through four:

| Dimension | Number of subspaces |
| --- | ---: |
|1|135|
|2|1,575|
|3|2,025|
|4|270|

Every maximal singular four-space contains 35 singular lines. Its intersection with the new set of 315 marked lines has the following distribution:

| Marked lines in the four-space | Number of four-spaces |
| --- | ---: |
|0|72|
|7|135|
|15|63|

No maximal singular four-space has all 35 lines marked. An allocation induced by any orthogonal spread would include all 35 lines of each of its nine spread members. Therefore this marking is not induced by any orthogonal spread, including orthogonal spreads not present in the older witness.

## Adversarial controls

Toggling one marked D label breaks exactly 16 H quotas. Toggling that label together with its perpendicular partner preserves global dual covariance but still breaks exactly 32 H quotas. These distinguish the point/allocation constraints from duality alone.

The identity endomorphism preserves all marked lines and the quadratic form, but fails the irreducible polynomial relation. This checks that the field-structure conclusion depends on more than line invariance. Conversely, replacing J by J² passes the full field and orbit checks at all H charts, as required.

## Reproduction and accepted boundary

From the repository root:

```sh
python -I -B research/moonshot-005-program/results/bit-global-desarguesian-port-allocation/review-c/check.py --repo . --out /tmp/global-desarguesian-independent
```

The final line is

```
PASS_INDEPENDENT_GLOBAL_DESARGUESIAN_PORT_ALLOCATION 1120 630 30240 40320
```

The complete receipt is in `output/RESULT.json`, including all file hashes, the witness payload hash, native atlas checks, endomorphism dimensions, orbit counts, singular-subspace counts and negative controls. The review ran in approximately two seconds in this environment.

The result removes the global port-allocation obstruction for this particular family of local Desarguesian components. It supplies a coherent choice of nine actual ports at every H with all required geometric 3/12 and point-reservation counts. Compatibility of actual source maps, phases, the shared later maps, global endpoints, ownership and the complete price remains separate work.
