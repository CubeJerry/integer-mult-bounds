# Canonical histories plus four coordinate innovations still miss the target

**Proved source-bound code theorem and conditional target exclusion. This does
not exclude arbitrary rank13 fittings, useful partial pivot prefixes, or later
noncoordinate history. No new kappa.**

Let K be the pinned111-port binary canonical fitting: K_ii=1 and K_ij=1 exactly
at real-orthogonal foreign source contacts. Let C be its nine-dimensional
row space, with basis rows0,1,2,4,8,9,14,30,59. For receiver i, let N_i be its
forbidden/noncontact source columns, excluding its diagonal. The actual
restriction C|N_i has binary dimension8. Its only canonical kernel is span K_i.

## 1. Uniform deletion robustness of the forbidden constraints

Exact enumeration of all512 binary canonical words gives256 distinct
restrictions at each N_i. The smallest nonzero restricted weights are:

| minimum weight | receivers |
|---|---:|
|18|7|
|19|24|
|20|52|
|21|16|
|22|11|
|23|1|

Thus for EVERY source subset S of size at most17 and every receiver i,
restriction to N_i minus S still has rank8. Otherwise a new nonzero restricted
codeword would be supported on at most17 deleted coordinates, contradicting
the exhaustive minimum-distance certificate. The rank statement remains true
over every characteristic-two field: a nonzero binary rank minor is still
nonzero, and the binary dependencies still hold. It does not require that
arbitrary extension-field words have been finitely enumerated.

Consequently the canonical rows vanishing on N_i minus S form exactly the
one-dimensional space span K_i, over any such field. The threshold17 is sharp
for this constraint-robustness statement: the checker provides an actual
weight18 restricted word, deletes precisely its support, and checks that the
rank then drops from8 to7. This sharpness is not a physical target construction.

## 2. All-width fittings in the coordinate-extended history space

Fix any such S and V>=1. Consider a block fitting A whose row blocks lie in

    W_S=(C+span{e_s:s in S}) tensor k^V.

Equivalently, each V-row block is an arbitrary matrix-valued linear combination
of the nine canonical rows and the unit rows indexed by S. All V-by-V
coefficients may be singular or noncommuting. This is a restriction on the
actual history ROW SPACE, not merely on its dimension or on packet count.

Write a row block as R_i plus a correction supported on S, with R_i canonical.
The fitting's forbidden zeros force R_i to vanish on N_i minus S. Applying
Section1 entrywise to its operator coefficients gives

    R_i=T_i K_i

for one V-by-V matrix T_i. If i is outside S, the identity diagonal A_ii=I_V
forces T_i=I_V. Therefore every column outside S in every row i outside S
has exactly its canonical block: K_ij I_V. Only columns in S can change.
No reordering or inversion of the unknown coefficient matrices occurs.

For i in S the diagonal can instead be supplied by its unit row. Such a row
can be localized to e_i. It would be incorrect to force its canonical part
to remain K_i; this distinction is included in the count below.

## 3. Arrival count and the target consequence

The actual canonical FOREIGN degrees have census

    55:1, 56:11, 57:16, 58:36, 59:28, 60:13, 61:5, 62:1.

For an arbitrary fitting use the admitted native support statistic

    ell_i=1[foreign support>36]+1[foreign support>52].

If |S|=s<=4, every row outside S still has foreign support at least f_i-s>36.
All but at most F_s=#{i:f_i<=52+s} of those rows also have support>52.
The rows inside S are optimistically granted ell_i=0. Hence

    sum ell_i >= 2(111-s)-F_s.

For s=0,1,2,3,4 the resulting lower bounds are respectively

    222, 220, 218, 215, 202.

In particular every such fitting has sum ell>=202. The admitted all-route
retained-caller theorem requires sum ell<=194 for a complete target-profitable
source, with all public/owned turns and actual history equations charged.
Therefore no complete source meeting that theorem's hypotheses can have its
entire relevant history X-row space contained in W_S with |S|<=4.

This is stronger than the dimension-only floor ceil(28V/3), and answers a
specific constructive question: replacing one canonical mode K_i by the
retained pivot mode K_i+e_i is a legitimate partial mechanism, but its future
histories cannot remain solely in C+span e_i. At least five coordinate
directions are necessary if coordinate extensions are the only innovations;
five are not shown sufficient. Other genuinely noncoordinate histories
remain possible and require their own exact source and budget.

## Evidence, scope and credit

The checker derives K from rational native root coordinates and enumerates
only the fixed finite9-code. The argument above supplies the all-subset,
all-field and all-width quantifiers. A source-code test is not used as an
unbounded algorithm proof. The complete-caller implication retains its exact
source, cost and foundational premises from bit-all-route-rank-gap.

Native SHA256:
`51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78`.
Credit the native canonical code, all-route support theorem, Worker A's
retained-pivot construction motivating this check, root's deletion-distance
and support argument, independent review recorded separately, and @CubeJerry.
OpenAI assistance. Both strict suppliers and all five foundations remain open.
