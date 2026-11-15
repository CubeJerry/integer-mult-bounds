# Actual native proper-chart covers for the full-eight axis pivots

**Proved fixed-fitting specialization of the programme's singular-pivot
theorem. No source acquisition, complete decoder or new kappa is claimed.**
The pivot with binary coordinate9 has rank15, canonical enlargement16 and
exact proper-cover charge106 on the actual111 native ports. Coordinate10
has charge110. Both use two actual native axis facets as the class-one
carriers. The result supplies a verified geometric target for Worker A's
changed full-eight acquisition investigation.

The singular-pivot code identity and two-chart mechanism were already proved
in `results/bit-singular-pivot-split/author/PROOF.md`. This contribution derives
the exact new native supports, real partner normals and charges, using an
independent implementation. It does not present that general mechanism as
new. The construction and its proof remain separate from any source scan.

## 1. Source, notation and quantifiers

The111 native integer root vectors r_i have squared norm4. Their authenticated
recovery and the120-root ambient geometry are pinned in `DEPENDENCIES.json`.
The recovery SHA256 is
`8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e`;
the full-geometry certificate SHA256 is
`4ac3933fb2393c62a96ec9e931ef4936e61d0e6c912c7ce0a94398a5f19addfc`.
Native/full indexing and every native vector are checked exactly.

Use the admitted binary polar frame with native indices
`0,1,2,4,8,14,30,59`. Write x_i for the resulting binary coordinates, B for
the nondegenerate polar form, and q for the quadratic form. All120 distinct
full-root labels satisfy q(x)=1. For distinct native roots,

    B(x_i,x_j)=0 iff the actual real roots are orthogonal.

The first eight native roots are the coordinate axes `2e_0,...,2e_7`.
Their first four independent binary labels are those at0,1,2,4. A mask s
from1 through15 here is a binary combination of those four labels; this is
the same h-coordinate convention used in the full-eight exploratory scans.
Define

    h_s(x)=B(s,x),
    K_ij=1+B(x_i,x_j),
    A^(s)_ij=K_ij[1+h_s(x_i)+h_s(x_j)].

The bracket keeps precisely the same-h class. Own coefficients equal1, and
every foreign nonzero coefficient corresponds to a real-orthogonal input.
Thus A^(s) is an explicit complete algebraic fitting. Its values do not yet
exist in an implemented source/decoder at the required charts.

Every stated row identity and rank holds over every characteristic-two
field and, after tensoring with `I_V`, every positive width V. Proper-cover
charge below refers to this fixed fitting and its nonzero foreign support,
not to all possible alternative block fittings in the same code.

## 2. Seven singular pivots and actual carrier normals

The first four independent axis labels are pairwise polar-orthogonal and
anisotropic. Consequently q(s) is the parity of the mask's bit count. The
seven nonzero singular masks are3,5,6,9,10,12,15. Each partitions the eight
actual native axes into four pairs with binary sum s. The chosen carrier
pair is the first such pair:

| Mask s | Actual carrier indices a,b | h-zero/h-one native sizes | Exact chi | One-chart receivers |
|---:|---|---|---:|---|
| 3 | 0,1 | 53,58 | 108 | 54,60,82 |
| 5 | 0,2 | 53,58 | 108 | 56,65,100 |
| 6 | 0,3 | 49,62 | 104 | 9,11,46,50,57,62,68 |
| 9 | 0,4 | 51,60 | 106 | 46,50,70,84,98 |
| 10 | 0,5 | 53,58 | 110 | 87 |
| 12 | 0,6 | 53,58 | 108 | 9,11,97 |
| 15 | 0,7 | 53,58 | 110 | 71 |

For all seven pivots the full120-root class sizes are56 and64. Mask9 is
`s=x_0+x_4`; its two carrier normals are r0 and r4. Mask10 is both
`x_1+x_4` and `x_0+x_5`, so the certificate uses actual carrier normals r0,r5.
All carriers are geometric normals already present among the native axes.
This does not assert that a needed payload is already present on their facets.

The eight odd masks are anisotropic and are explicitly excluded from this
singular theorem. Their source or covering status is not inferred from this
table. Source feasibility must also be checked independently; the smallest
chi in the table need not be the best acquisition interface.

## 3. Exact covers and their minimality

For receiver i, let S_i be the foreign support of A^(s)_i. It lies in
F_i=r_i-perp. The proof uses the already established singular-pivot cases.

### Class h_s(x_i)=0

The binary partner p=x_i+s is another anisotropic label, distinct from x_i.
Its actual120-root representative r_p is orthogonal to r_i. Every retained
foreign source j except the partner itself lies in

    F_i ∩ F_p.

The certificate checks this statement on each actual source coordinate.
If p is native, the remaining singleton is its point line L_p, which also
lies in F_i. The common chart is genuinely proper, of dimension6, and the
point chart has dimension1. If p is omitted, the common chart alone covers
the full foreign support; the omitted root is a geometric normal, not an
input or an uncharged source record.

### Class h_s(x_i)=1

Choose the actual orthogonal axis carriers a,b with x_a+x_b=s. Every retained
foreign source j satisfies

    B(x_a,x_j)+B(x_b,x_j)=h_s(x_j)=1.

Exactly one pairing vanishes. Neither j=a nor j=b occurs, because those
carriers have h_s=0. Thus the vanishing binary pairing is genuine real
orthogonality. Partition S_i according to its first vanishing pairing and
use the two actual proper charts

    F_i∩F_a,       F_i∩F_b.

Both have dimension6. This proves a two-chart cover with fully specified
supports; no exclusive-contact search or favorable source availability is
assumed.

### Exact charge

For each of the777 receiver/pivot pairs, the checker computes the rational
rank of S_i. It is6 precisely at the one-chart receivers in the table and7
at every other receiver. A rank7 support cannot lie in any proper subspace
of the rank7 receiver facet. The explicit two-chart cover therefore proves
its exact minimum cover number is2. At a rank6 support the exhibited single
proper chart proves the minimum is1. Hence the exact charge is

    chi(A^(s))=sum_i(minimum proper-chart count−1)
              =111−number of one-chart receivers.

This supplies both a lower and an upper certificate for the stated fixed
fittings. It is stronger than simply listing two possible charts.

## 4. Rank and code identity

Let C be the rank9 canonical affine evaluation code, C_s its rank8 subspace
whose linear parts annihilate s, and h_s C the rank8 filtered code. The
independent exact binary calculation checks

    row A^(s)=C_s+h_s C,       dim row A^(s)=15,
    dim(row A^(s)+C)=16,       dim(row A^(s)∩C)=8.

These are the credited singular-pivot identities specialized to the new
native puncturings. For each pivot the checker verifies the dimensions of
C_s, h_s C, their sum and their equality with the actual fitting rowspace.
Binary linear identities persist over every characteristic-two extension;
binary nonzero minors remain nonzero. Tensoring gives the stated ranks times
V and the same foreign-support geometry at every positive width.

## 5. Certificate, controls and scope

`output/PIVOT-s-COVERS.json` records every fitting row, complete foreign
support, actual partner full/native index, rational chart normals, partition,
chart dimensions, foreign-span rank and minimal charge. `output/RESULT.json`
pins every certificate and gives the summary. The checker is standalone
Python using exact integer binary elimination and Fraction-based rational
elimination; no predecessor checker or author full-eight source code is
imported.

Four rejecting controls erase an own entry, use the first carrier facet for
both h-one pieces, falsely assign zero charge to rank7 foreign support, or
apply the singular theorem to anisotropic mask4. Their failures are recorded.
The universal field/width statement follows from the explicit identities and
support proof, not from mutation rejection or a finite width experiment.

```sh
python3 -B check.py --repo /absolute/path/to/integer-mult-bounds \
  --out /absolute/path/to/pivot-cover-output
```

Expected status: `PASS_INDEPENDENT_AXIS_PIVOT_PROPER_COVERS`.

The initial full-eight `PIVOT-SCAN.json` was independently identified during
the session as invalid *seed-free feasibility evidence*: it retained donor
offsets in supposedly absent Hub seeds. Its acquisition conclusions are not
dependencies here. Correct source analysis must use actual history increments
or zero total seeds. Subsequent cache-colouring changes also need their own
literal source, endpoint, ownership and price verification.

In particular, chi106 for mask9 does not construct an all-size source or
decoder. The full-eight investigation must still realize the claimed history,
deliver all111 outputs, pay each correction and recursion, and meet both
strict suppliers. All five foundational assumptions remain. No new kappa.

Credit: @CubeJerry, the authenticated native and quadratic-geometry authors,
the programme's singular-pivot construction and reviews, and Worker A's
full-eight acquisition lead. Worker C supplied this independent exact pivot
specialization and certificates. Substantial OpenAI assistance.
