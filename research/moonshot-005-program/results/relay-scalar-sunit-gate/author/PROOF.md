# A scalar Gram rescaling cannot repair the twenty-port relay over Z[1/30]

**Source-specific theorem, independent review pending. No new kappa.**

This result excludes every nonzero rational scalar rescaling, not just a
finite coefficient search. It uses the established complete solution of
the {2,3,5}-unit equation. The companion anisotropic matrix construction
lies outside the excluded family and supplies a meaningful boundary control.

## 1. Exact scope and source

Use `results/proper-chart-relay/author/20/WORD.json.gz`, gzip SHA256
`0edf81ca8f6a7e60e5a01d4acdcaefdb74882180b8d12c408513bc91cd625b1c`,
and `research/shared-wire-split-composition/data/final.json.gz`, SHA256
`2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883`.
The actual relay construction, phase audits and smooth-ring continuation
theorem remain explicit predecessors in `results/proper-chart-relay/` and
`results/proper-chart-relay-smooth-ring/`.

Let H be its96 hosted ports, T the20 restored ports, and S=H\T the76
remaining ports. These are the historical native labels, converted to compact
source indices by `source_role_map`. Let g_h be the normalized root
coefficients in the recorded omitted orthogonal frame
Z=[7,25,42,52,76,82,97,127]. The normalization is the predecessor's: squared
root norm18, inner products divided by18. Every g_hi is dyadic.

Write R=Z[1/30]. For any lambda in R, replace the acquired preload by

    q = sum_(h in H) g_h^T d_h,
    r_h = -d_h + lambda g_h q      (h in H),
    r_u = lambda g_u q            (mode ports u).

Keep the same relay geometry, permutation, restored set and endpoint
formula. This is an algebraic relaxation: a particular lambda might require
more literal gates or violate the old magnitude restriction. The identity
d_h=-r_h+sum_u beta_hu r_u persists because g_h=sum_u beta_hu g_u.

**Theorem.** For every nonzero lambda in R, this terminal public map has no
exact R[i]-linear continuation restoring all original D inputs for arbitrary
original data, after all previous owners retire and with no separate
correlated original-input record. Fresh zero records and independent inputs
do not help. The claim holds at every whole-field width V>=1. It permits
neither changing the geometry nor importing additional correlated state.
It does not address new arithmetic primitives or an independently justified
approximate/rounding interface.

The zero boundary is excluded deliberately: lambda=0 gives an invertible
signed permutation on the remaining D coordinates. That degenerate unmixed
preload does not by itself provide the missing physical restoration or
forward correction schedule.

## 2. Source-bound determinant

After using D_T and undoing the recorded permutation, the unknown D_S block
is -I_76+lambda g_S g_S^T. Its determinant is

    D(lambda)=det(I_8-lambda B),    B=g_S^T g_S.

Other outputs give no additional independent D information: every B output
has its arbitrary independent original b coordinate, while X/Y undergo only
the unchanged invertible coupled shear. Thus the full400-input determinant,
up to sign, is D(lambda).

Exact reconstruction from the pinned geometry gives

    char_B(x)=(x-13)(x-8)(x-10)(x-9)(x^2-18x+161/2)^2,

so

    D(lambda)=(1-13lambda)(1-8lambda)(1-10lambda)(1-9lambda)
              * ((1-9lambda)^2-lambda^2/2)^2.             (1)

RESULT.json records the exact8-by8 matrix. The checker independently
reconstructs it from literal source root lines and checks (1) at nine distinct
rational points. Both sides have degree at most eight, so these exact
equalities certify a polynomial identity. They are not a numerical
extrapolation. At lambda=1 they recover the admitted determinant24387048.

## 3. Complete S-unit reduction

If a product in a commutative ring is a unit, each factor is a unit. Suppose
D(lambda) is an R-unit. Put u=1-8lambda, v=1-9lambda, w=1-10lambda. These
are nonzero units, and u+w=2v. Therefore

    x=u/(2v),  1-x=w/(2v)

are R-units. Rearrangement gives

    lambda=(1-2x)/(8-18x).                               (2)

The exceptional x=4/9 has no finite lambda, since the rearranged equation
would assert0=1/9.

The required external result is the complete classification of
x+(1-x)=1 in R-units. Rafael von Kaenel and Benjamin Matschke,
*Solving S-unit, Mordell, Thue, Thue--Mahler and generalized Ramanujan--Nagell
equations via Shimura--Taniyama conjecture*, arXiv:1605.06079v1, Theorem A,
states that the {2,3,5} case has exactly17 symmetry orbits and99 ordered
solutions. They credit this small-prime case to de Weger, Theorem5.4.
The paper title refers to the now-proved modularity theorem; it does not
introduce an unproved conjecture into this application.

Primary source: https://arxiv.org/pdf/1605.06079, Theorem A, manuscript p.7.
The six transforms of z are

    z, 1-z, 1/z, 1/(1-z), z/(z-1), (z-1)/z.

The following independently generated positive coprime triples a+b=c,
with z=a/c, give17 distinct orbits:

    (1,1,2), (1,2,3), (1,3,4), (1,4,5), (2,3,5),
    (1,5,6), (3,5,8), (1,8,9), (4,5,9), (1,9,10),
    (1,15,16), (1,24,25), (9,16,25), (2,25,27),
    (5,27,32), (1,80,81), (3,125,128).

Each triple has prime support in{2,3,5}; orbit distinctness is exactly
checkable. The published upper bound17 makes this witness list exhaustive.
The checker enumerates witnesses with c<=128 but does not treat that cutoff
as a completeness argument. No external software or licensed data file was
copied into this package.

Applying (2), discarding its one infinite value, retaining nonzero lambda
in R, and imposing all four linear unit conditions in (1), leaves precisely
the following five candidates. Write Q(lambda)=(1-9lambda)^2-lambda^2/2.

|lambda|1-13lambda|1-8lambda|1-10lambda|1-9lambda|Q(lambda)|
|---|---|---|---|---|---|
|1/18|5/18|5/9|4/9|1/2|161/648|
|1/12|-1/12|1/3|1/6|1/4|17/288|
|7/64|-27/64|1/8|-3/32|1/64|-47/8192|
|1/5|-8/5|-3/5|-1|-4/5|31/50|
|1/4|-9/4|-1|-3/2|-5/4|49/32|

The numerator obstructions are respectively7*23,17,47,31,7^2, so no
quadratic factor is an R-unit. This contradicts the supposed unit determinant.
The candidate7/64 is essential: lambda was never assumed itself to be a unit.

## 4. Exact continuation consequence

For every nonzero lambda, D(lambda) is zero or a nonunit of R. If zero, the
remaining D matrix has a nonzero rational kernel. If nonzero but a nonunit,
some prime p outside{2,3,5} divides its reduced numerator, yielding a nonzero
kernel over F_p. Extend this residue field to contain a root of X^2+1;
this gives a homomorphism from R[i]. Because the restored coordinates are
an identity block, the kernel has a nonzero D_S component and zero D_T
component. Cancel its B-output effect using the independent original b
coordinates, and set the other independent input components to zero.

This constructs a kernel of the full public map with a nonzero original D
component. Every subsequent exact R[i]-linear instruction still annihilates
it, while exact D restoration would not. Independent helper inputs have
zero components on this kernel direction. Tensor with I_V for any V.
This proves the stated source-specific obstruction.

## 5. Constructive boundary and programme effect

Let Lambda=(1/4)I_8+(1/24)E, where E has blocks[[1,-1],[-1,1]] on coordinate
pairs(0,2),(1,3) and is zero elsewhere. Independent reconstruction gives

    det(I_8-Lambda B)=3375/128,

an R-unit. This explicitly refutes extending the scalar obstruction to
arbitrary matrix preloads. The companion source implements Lambda at the
existing ground bank with22 additional scalar gates and no new MOVE or
owner lifetime. Its separate proof and precision qualifications remain.

Thus scalar rescaling cannot remove the original arithmetic defect, whereas
anisotropic matrix adjustment can. Neither result restores the remaining76
D fields or supplies the104 missing forward outputs. Both strict target
suppliers remain unproved, the selected conditional multiplication bound
is unchanged, and all five foundational assumptions remain.

## 6. Verification and attribution

Run this package's `check.py --repo . --output RESULT.json` from the repository
root, adjusting the script/output paths. It uses Python's standard library
and exact fractions. Expected: PASS_EXACT_SOURCE_AND_S_UNIT_REDUCTION,
17 orbits,99 solutions, five nonzero linear-factor candidates and no unit
determinant. The external complete S-unit theorem is an explicit dependency,
not purportedly reproved by this checker.

Prepared for @CubeJerry with substantial OpenAI assistance. Credit the
original relay and its independent ring audits, de Weger's complete
classification, von Kaenel--Matschke's theorem and exposition, and the
companion worker's anisotropic construction. The new contribution is this
source-specific application and certificate, not the classical number theory.
