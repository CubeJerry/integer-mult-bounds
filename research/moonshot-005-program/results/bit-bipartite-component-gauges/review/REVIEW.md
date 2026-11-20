# Independent check of the bipartite gauge and split-target claims

I independently reconstructed the 111-root foreign graph, the two ordered
stars, the central generators and the ranks after deletion of the cross maps.
The verifier imports no author or predecessor checker. It reads three
pinned data files. The native identity edges form a single bipartite
component on 220 vertices with 6,347 edges. Identities therefore identify
all ordinary input and output spaces without assuming that the two roles
at one native root start in the same gauge.

Write F_l=E_(0,l) and R_l=E_(l,0) on bank labels with identity on each
64-dimensional block. Comparing the exceptional row via I+F_1 identifies
F_1+F_l, and comparing the exceptional column via I+R_1 identifies R_1+R_l.
The product for l=2 on the row and l=3 on the column is E_(0,0). Using l=2
on both sides produces zero in characteristic two. Compressing the relative
maps for internal operators by E_(0,0) isolates the internal generators:
the tail term vanishes on the double-sided compression. This puts
F_1,R_1 and every F_l,R_l in the relative algebra.

The checker built new independent words in the three 32-square matrices,
starting from the empty word and retaining an independent span at each breadth
step. Their rank reaches 1,024 by degree ten. It never reads the predecessor
list of 1,024 words to establish that rank. The two internal scalar arrows
supply all 2-by-2 units; the three other arrows supply T,W,U in their
respective corners. Products then give all 64-by-64 central units and
transport through the tails gives M_3840(F). These binary rank and product
identities hold over every field of characteristic two.

The ordinary space W at multiplicity s is stable under all E_ab tensor I.
Each E_aa extracts one coordinate fibre and E_ab identifies every fibre
with one subspace Z of F^s, proving W=F^3840 tensor Z. Both exceptional
gauges are then also W. The converse is immediate by direct action. The
768s-dimensional small component fits exactly when 5 divides s. These
are field-linear statements about the fixed B; they neither invoke a
physical 1+4 routing at s=5 nor exclude nonlinear representations.

On a single body the reviewer independently used tails 1 through 48 and
right coordinate zero. In the row star the 48 incoming spinor spaces
land in one 16-dimensional central space. In the column star one
16-dimensional central input is injected at 48 distinct receiver vertices.
The two native supports and the two component directions are disjoint, so
the assembled crossing rank is 32 across 96 edges. Alternating two distinct
right coordinates on the same 48 tails makes *both* ranks 32 instead of
16. The alignment used in the result is essential.

After deleting the two crossings, every retained tail map still has square
zero and the five internal maps have square zero on the central bank. Their
common component projections commute with any repeated spinor action. The
remaining row and column perturbation ranks are separately 64, directly
computed by accumulating their image and row bases. The native baseline
rank is 9; its two restrictions outside the appropriate row and column star
supports both have rank 9. Thus the canonical and residual column and row
spaces intersect trivially, giving rank(I+B_diag)=9*3840+128 and additional
canonical repair rank 128. The small component is exactly canonical since
all its possible perturbations joined it to the central large component.
This is a different fitting target with physical construction still open.

Run check.py with `--repo REPO --out FRESH`. RESULT.json records the
complete role lists, finite ranks and controls. Outcome: the author's
stated claims hold in the specified scope. This is separate model-assisted
mathematical and computational review, not external human review.
