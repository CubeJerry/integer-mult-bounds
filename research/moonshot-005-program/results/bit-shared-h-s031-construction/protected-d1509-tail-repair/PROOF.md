# Two central tails repair the protected shared-D obstruction

**Positive width3 source/H theorem and exact known partial-D four-space certificate. Independent admission pending. No complete D decoder, full return or new kappa.**

The admitted rank-one-overlap pair has centres H263 and H642, with donors0,61,62 and45,61,100. Its protected physical ports have exactly one common D chart, D1509. The old literal fails a necessary proper-D continuation condition: an H263 fibre direction isolated to D1509 can affect an H642 output to another visible D. This result changes only the source quotients at (45,H642) and (100,H642), removes that interference at every native D1509 view, and retains all complete source/H properties.

Work over GF64 with modulus x^6+x+1. Each source bank has dimension48 and each of its28 quotients has width3. Both physical nine-port H words are unchanged: H263 has rank9 and H642 has rank8. The second word still requires its one separately paid information complement. All assertions concern the five supplied sources, their two supplied H words, and the explicitly enumerated known observations. They do not assume any unbuilt H word.

## 1. Exact finite result

The source literal passes all315 geometric and291 native full source cuts. At both centres the entire three-dimensional off-H inverse fibre is common to all three donors and has the same invertible three-port readout. All72 geometric and67 native H views pass. The whole H263 fibre core remains22-dimensional; the whole H642 core remains18-dimensional. Each of the five actual96-by96 two-copy early source bases remains invertible at seed0.

The native receivers seeing D1509 are

    6,9,48,52,54,73,74,85,87,95,98.

At each of these eleven views, the common kernel of all known outside-D source observations and all known wrong-D H outputs has dimension exactly4. It contains both independent whole-H directions isolated to D1509, one from each centre. Thus neither isolated direction produces an output at any other visible port of either built H. The result includes all five donors' outside-D source observations, rather than only those at the shared donor.

The two changed source quotients are still single edited geometric quotients at donors45 and100. The uniform propagation bounds are therefore27<45 there. The three other source tuples are unchanged and retain the two-edit bound36<45. These are the admitted arbitrary-edit bounds, applied after checking every full source cut; the changed tails introduce no further edited planes.

## 2. Preserve the entire second-centre fibre core

Write C_j for the three-row central quotient at H642 and C_j^old for its admitted value. Let S_B be a48-by18 matrix spanning all36 geometric H642 fibres. We require

    C_j S_B = C_j^old S_B.                              (1)

The shared donor61 is left literally unchanged. For donors45 and100, equation(1) permits arbitrary linear tails annihilating the entire core. Every off-H642 quotient is unchanged, so its whole inverse fibre is unchanged. Equation(1) preserves the full central pencil and hence the original common H642 readout on every such fibre. H263 uses donors0,61,62 only; all their source matrices are unchanged. Thus its full fibre diagram and readouts are unchanged as well.

Equation(1) alone does not ensure the other source views remain invertible or that any D continuation condition holds. Those are separately imposed and checked below.

## 3. A canonical four-space from fixed observations

Fix one of the eleven native receivers i and set D=D1509. Every one of the five donors belongs to D. Let Z_i be the common kernel of all their visible source quotients at planes not contained in D. There are twelve such planes at each donor. Direct exact elimination gives

    dim Z_i = 12.

Add the contribution rows of H263 leading to every other visible protected D port, separately for each of its three donors. The common kernel has dimension6. Add the shared donor61 contribution rows of H642 to its other two visible protected ports. The resulting common kernel L_i has dimension4.

These observations are fixed before either tail is chosen. None involves the variable C_45 or C_100: their central H642 plane is contained in D and was excluded from the source observations, and their H642 contribution rows have not yet been added. `SOURCE-COEFFICIENTS.json.gz` stores a canonical column basis of every L_i. The checker independently reconstructs it by exact elimination.

For each j in {45,100}, impose

    P_B[E,j] C_j L_i = 0                               (2)

for every native i seeing D and each of the other two visible protected H642 ports E. Here P_B[E,j] is the actual one-by-three donor block in the fixed physical H642 word. This equation uses the actual D label; no receiver-dependent output permutation is allowed.

By construction all fixed observations annihilate L_i. Equation(2) makes the remaining known wrong-D rows annihilate it too. Adding rows cannot increase a kernel, so the complete known kernel is exactly L_i and has dimension4, not merely at least4.

## 4. Exact affine systems and literal source tails

Flatten C_j into144 unknown field coefficients. Equation(1) gives54 scalar equations. Equation(2) gives88 equations: eleven receivers times two wrong-D ports times four basis columns. The resulting affine system has142 rows and144 columns.

For each of the three H642 donors, its coefficient matrix and augmented matrix both have rank110. Hence it is consistent with a34-dimensional space of homogeneous tails. For donors45 and100 the literal is a fixed solution plus a deterministic nullspace combination with tags `protected-full-D-tail/45/0` and `protected-full-D-tail/100/0`. For donor61 use the old map, which also satisfies every equation. The checker stores the complete coefficient matrix, right side and34-column kernel basis for each system, and checks the literal maps directly against every equation.

The chosen coefficients additionally pass all full source cuts and all five actual early bases. This is a finite exact witness, not a genericity assertion about every member of the affine family. No claim is made that an arbitrary free-tail choice is source-invertible.

The independent isolated H directions are reconstructed from the entire three-dimensional H fibre and the inverse of its actual common receiver readout. They are normalized to1 at D and0 at the other visible ports. For each i their two columns have rank2 and lie in L_i. This verifies both directions of the repaired cross-H condition and all outside-D source conditions for these directions.

## 5. Extensions and scope

All coefficients, source determinants, readout determinants and affine identities lie in GF64. They persist in every finite coefficient-field extension. Repeating r copies gives a4r-dimensional known partial-D space at each of these eleven views, full H readouts of dimension3r, and the same one-dimensional-per-copy H642 loss. The result changes actual source matrices and rebuilds actual early bases; no linear transformation is treated as free.

This is a width3 component. Its direct sum with a complementary width12 pair needs its own literal source, early and all45-port checks. Even the exact four-dimensional known partial-D kernel does not construct a D word: the remaining native H parents, their sources, the physical D input owners, phase constraints, common output maps and later K/facet continuation remain obligations. Other observations introduced by such a continuation might shrink the present kernel and must be checked. No return or movement advantage follows from the present rank count alone.

Replay:

```sh
python -B research/moonshot-005-program/results/bit-shared-h-s031-construction/protected-d1509-tail-repair/check.py --repo . --out /tmp/s031-protected-D-tail
```

Expected receipt:

    PASS_PROTECTED_D1509_FOUR_SPACE_TAIL_REPAIR 315 291 72 67 11 4 110

Credit @CubeJerry, the retained geometric source and native atlas, the admitted rank-one-overlap and four-edit protection results, and agent C's exact frozen-prefix D witness. Substantial OpenAI assistance. No new complete kappa.
