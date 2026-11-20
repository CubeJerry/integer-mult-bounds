# A single global rank defect beneath the five pinned defects

**Accepted after independent worker-B reconstruction and proof review.** Keep the frozen baseline
and coordinates of the adjacent proof. The full response to the909 independent
source-export controls and381 external inputs has

    rank [C N] = 1288.

The direct rational checker obtains this by extending its full1289-dimensional
column-space basis for C with every external-input response column. A second
small-matrix explanation is useful. In inverse target coordinates,

    R [C N] has the same column span as [Id - T P, h].

Here the natural source basis plus the external original inputs together supply
all1289 original input directions. A row vector y annihilating this last matrix
satisfies y=yTP and yh=0. Put z=yT. Then

    z (Id_7 - P T)=0,  z P h=0,  y=zP.

Conversely these equations produce every such y; the map z to zP is injective
on this kernel, since zP=0 implies z=zPT=0. Consequently the left nullity equals
7-rank[J], where J=[Id_7-PT | Ph]. The exact J is

$$
J=\begin{pmatrix}
0&0&0&0&0&0&0&0\\
0&1&0&0&0&0&0&0\\
0&0&1&0&0&0&0&0\\
0&0&0&1&0&0&0&0\\
0&0&0&0&2&-1/4&0&0\\
0&0&0&0&-4&1&0&0\\
0&-1/4&0&0&0&0&1&0
\end{pmatrix}.
$$

The last six rows have rank six: use columns1,...,6, with central2-by2
minor determinant1. The zero first row leaves exactly one left-null direction.
Thus rank[C N]=1289-1=1288, independently agreeing with the direct column
elimination. Its null functional in inverse coordinates is the original
payload at deleted slot86.

This is different from the rank-five pinned obstruction. Global rank alone
leaves only one missing information direction, while the specified source and
outside-output interface imposes five independent alignment conditions.
Changing only linear preprocessing of the original input banks while keeping
the surrounding forms fixed does not enlarge col[C N]. One new scalar response
may remove the global rank defect; this calculation does not claim that it
also repairs the pinned conditions or realizes the target. Changes to original
input coefficients inside arbitrary existing local forms are surrounding-form
changes and are outside the fixed-preprocessing statement.

The complete replay is `total_rank.py --repo . --out <temporary-directory>`.
It reruns the adjacent independent full rational reconstruction, then computes
both ranks. No repaired circuit or new kappa follows.
