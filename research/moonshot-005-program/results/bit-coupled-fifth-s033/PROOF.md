# The exact protected source/D family

**Source-specific algebraic theorem. No full source word, fifth whole receiver,
supplier, new exponent or foundational discharge.**

Baseline `44f09459f91f8c3e27fcd45f54be7d043e6493b7`. Inputs are the literal
44 local systems from `bit-source-d-interpolation-s032`, independently
reconstructed in its separate review, and the actual original D1509 word.

## Proposition

Work over any field extension of GF(64). Retain receivers R=(6,9,48,73), the
eleven native donors, their actual four H parents, owner incidence and H words.
Let I_j be donor j's eight actual D inputs, O_r receiver r's eight D outputs,
T the old 35-by-35 D matrix, and U the union of O_r (22 positions).

Let T' be any matrix with the same 19/16 phase pattern and with all44 retained
sections S'(j,r)=T'[O_r,I_j] invertible. Permit independent new 6-by-96 protected
source quotient maps at the44 parent locations, holding all other source
coefficients fixed, with exactly the old prescribed H images and four common
D frames/identity readouts. Such local maps exist if and only if

    T'[U,{4,5,7,8}] = T[U,{4,5,7,8}].                    (1)

Thus the D solution set is a determinant-open subset of an833-dimensional
affine coordinate space:921 phase-legal entries minus88 fixed entries.
Requiring both phase blocks invertible removes more determinant-zero sets.
The old matrix satisfies all these determinants, so the open set is nonempty.
These are algebraic dimensions, not a count of finite-field points.

For each D, all source extensions have13,368 independent scalar parameters.
The complete local joint family has dimension14,201. This is a statement
about the specified local equations, before complete source validity.

The same iff holds for arbitrary k-by-k coefficient blocks mixing repeated
lanes, with old scalars replaced by scalar multiples of I_k. The88 fixed
positions become fixed blocks, and all retained8k-by-8k sections must be
invertible. The two parameter counts become833k^2 and13,368k^2. No commutation
of variable blocks is required.

## Exact intersection identities

Let C(j,h) be the independent-column matrix of prescribed H observations,
L=[L_6,L_9,L_48,L_73] the common96-by-32 four-frame matrix, F(j,h) the old6-by-96
source map, and M(j,h,r) the actual6-by-8 ingress-to-quotient map. The pinned
physical identity is

    F(j,h)L_r = M(j,h,r)S(j,r)^(-1),
    S(j,r) = T[O_r,I_j].

Put B_j=I_j intersect {4,5,7,8}. The decisive identities are

    col C(j,h) intersect col L
      = span{ L_r T[O_r,B_j] : r in R }.                 (2)

Every displayed column on the right is independent, so its dimension is4|B_j|.

| Donors | B_j | Dimension |
| --- | --- | --- |
| 0,62 | {4,5} | 8 |
| 45,100 | {7,8} | 8 |
| 61 | {4,5,7,8} | 16 |
| 32,35,38,68,69,90 | empty | 0 |

For all44 systems the certificate supplies the exact coordinates of these
columns in C. Direct multiplication proves containment. Independence and
rank(C)+32-rank[C,L] prove equality. It also verifies the original relation
kernels. For each donor/receiver, stacking the four actual maps M over its H
parents has rank8;44 exact left inverses certify this second fact.

## Necessity and donor61 reduction

A valid new source map satisfies F'C=FC and F'L_r=M S'^(-1). For p in B_j,
the vector L_r T[O_r,p] belongs to the H space by(2). Evaluating its image in
the two ways gives

    M(j,h,r)S'(j,r)^(-1)T[O_r,p] = M(j,h,r)e_(j,p),

where e_(j,p) is the unit vector at p's position in I_j. Stack the four parent
equations and apply the certified left inverse. Then

    S'(j,r)^(-1)T[O_r,p] = e_(j,p),

and multiplication by S' yields T'[O_r,p]=T[O_r,p]. Donor61 contains all four
special inputs. Its four parent systems therefore force the whole88-entry
rectangle(1). The other40 systems impose no additional condition on D.

## Sufficiency and source freedom

Conversely(1) gives S'^(-1)T[O_r,p]=e_(j,p) for every relevant j,r,p. Hence the
requested images on L agree with the old H images on the right side of(2).
Equality(2) says these are all compatibility conditions. They define a linear
map on col[C,L], which can be extended to the full96-dimensional source space.
Do this independently for all44 quotients.

For an explicit extension choose independent columns X_0 of X=[C,L] and a
nonsingular square row minor. Its inverse supplies the required map on X_0;
choose its values on a complementary basis freely. Every other solution differs
by a map annihilating X, a space of dimension6(96-rank X). The44 dimensions sum
to13,368. A fixed extension operator applied to the rational section inverses
identifies the joint family with the D open set times this affine source space.
Thus its dimension is833+13,368=14,201.

All identities survive coefficient extensions. Tensor the source intersections
and parent left inverses with I_k and use actual block-section inverses. The
same proof works without moving blocks past one another; source extension
freedom is6k(96k-k rank X), proving the repeated-lane assertion.

## Verification and scope

`check.py` has its own GF64 multiplication and elimination and imports no
constructor or tangent executable. It authenticates the two literal inputs,
checks all intersection witnesses, parent left inverses and dimensions.
The original D word is a positive control. A deterministic dense positive
point changes820 free entries and passes all local equations and phases.
Each of the88 fixed entries has its own nonzero mutation with all retained
section ranks intact; each fails a donor61 equation. These controls supplement
the structural proof, rather than extrapolating from a finite sample.

```sh
python3 -B research/moonshot-005-program/results/bit-coupled-fifth-s033/check.py \
  --repo . --out /tmp/s033-exact-local-D
```

Expected status: `PASS_EXACT_833_PARAMETER_LOCAL_D_FAMILY`.

Full source views, strict nonsaturation, whole fibres, actual early source
preparation, compilation and global costs are separate. The canonical S032 t=1
extension actually fails some full source ranks in S033's separate review.
The theorem also does not assert a universal fixed-K rank2 obstruction: the
separate coupled overlap candidate raises the unrestricted common response to4.
The actual receiver95 output and whole-fibre conditions are stronger.

## Open next questions

The old projected tangent has no remaining finite integrability obligation:
its coordinate directions parameterize the whole local solution set. Choose
free D coefficients and source extensions that pass complete source/fifth-fibre
contracts, or prove which further interface must change. Both suppliers,
return, full recursive caller and all five foundations remain open. No newκ.

Credit @CubeJerry, S031/S032 source/H/D authors and independent reviewers, and
inherited geometry/atlas/compiler contributors. Substantial OpenAI assistance;
agent review is distinct from independent human or proof-kernel verification.
Apache-2.0.
