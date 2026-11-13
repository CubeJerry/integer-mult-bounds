# Independent review: the E7 two-subspace bound

**Geometry review: pass.** The exact real-root geometry in the pinned BIT
source supports the sharp bound of 52. This review does not admit the separate
monotone event-accounting theorem, its price corollaries, a supplier, or a new
value of kappa.

## Independent reconstruction

I rebuilt the line system from the authenticated native input at SHA-256
`51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78`. Starting
from its 111 actual source lines, I recovered the 14 weight-four supports,
completed their eight sign classes, added the eight coordinate lines, and
checked exact norm, spanning rank, reflection closure, and transitivity on all
120 lines. Fixing the coordinate root `2e_0` leaves 63 lines in its orthogonal
seven-dimensional subsystem.

The orbit computation is independent of the author's coordinate method. I
selected a different generic positive orientation, found its indecomposable
positive roots, solved the seven fundamental weights as rational vectors in
the ambient eight coordinates, and generated their Weyl orbits by reflecting
those ambient vectors. The seven orbit sizes, root counts in the normal
hyperplanes, and pair maxima agree exactly with the submitted certificate:

| Fundamental-weight orbit | Normal lines | Root lines in one hyperplane | Maximum union with any parabolic flat |
|---:|---:|---:|---:|
| 0 | 378 | 21 | 46 |
| 1 | 5,040 | 10 | 41 |
| 2 | 63 | 30 | 51 |
| 3 | 1,008 | 16 | 45 |
| 4 | 288 | 21 | 46 |
| 5 | 2,016 | 13 | 42 |
| 6 | 28 | 36 | 52 |

The 8,821 parabolic root masks are distinct. For each first orbit I fixed one
normal and checked its union with every normal mask in all seven orbits;
Weyl transitivity makes that exhaustive for arbitrary ordered pairs.

## Universal real-subspace reduction

The chamber argument correctly extends the finite hyperplane calculation to
all real subspaces. If `C` is any proper subspace of the fixed E7 space, choose
a nonzero normal `w` with `C` contained in `w^perp`. The finite Weyl group acts
on this space and has a vector `rho` strictly positive on the simple roots.
Choose a Weyl image of `w` maximizing its inner product with `rho`. Every
simple-root pairing is then nonnegative: a negative pairing could be
reflected to increase the objective. At least one pairing is positive.

Every positive root has nonnegative simple-root coefficients. If it is
orthogonal to this dominant normal, its coefficients must vanish at each node
with positive pairing. In particular, its line belongs to the maximal
parabolic root set obtained by omitting any one such node. Thus the roots in
`C` are contained in one of the enumerated maximal-parabolic sets. Applying
this to each of two proper subspaces reduces their union to one of the checked
pairs of parabolic root masks. The finite search is not being used to infer
the unbounded real-subspace quantifier; the chamber reduction supplies that
step.

This reasoning also handles subspaces of dimension below six: their root
support is still contained in a maximal parabolic set. The condition is on
root lines *contained in the subspace*, not on the dimension of a span formed
after taking a union.

## Sharpness and the 51 control

The bound is sharp. My independent ambient-coordinate witness has two E6
hyperplanes with normal vectors

`(0,1,1,-1,0,0,0,0)` and `(0,0,0,1,0,-1,-1,0)`.

Each contains 36 of the 63 E7 root lines; their intersection contains 20, so
their union contains `36 + 36 - 20 = 52`. This is an explicit negative
control against a proposed bound of 51. The submitted witness and mine agree
on the 36/36/20/52 counts.

The actual source contact sets have 55 through 62 lines. Therefore no two
proper real subspaces cover an actual contact set. At least three proper
subspaces are necessary in any argument whose local contributions are each
supported in one such subspace. This geometric statement does not establish
that three-subspace coverage is impossible.

## Scope boundary

The geometric certificate is valid. The downstream arrival count still needs
its stated trajectory/locality premises: monotone source paths and packet
paths, no Y-bearing movers, no nonlocal payload carried back down after an
upturn, and terminal fitting rigidity in the asserted block stratum. In
particular, the 52-line result alone cannot be applied to an arbitrary
nonmonotone packet whose later payload includes source data acquired at a
larger chart.

The independent checker is
[`review_e7_subspace_union.py`](review_e7_subspace_union.py), and its replay is
[`RESULT.json`](RESULT.json). The exact reviewed author and proof bytes are
pinned in [`MANIFEST.json`](MANIFEST.json).
