# Independent review of the canonical source-side basis obstruction

Verdict: **PASS for precisely the stated one-sided simultaneous-coordinate
strategy**. Reviewed Route C source-side-basis-obstruction.md at SHA-256
d88feb7e5e334e89ad6f271a42955a0a982fbbd851d482c9e61019cfaafdd2a0.
This is neither a tape lower bound nor an obstruction to coordinating
the larger full endpoint spaces.

The four proposed two-label source sides are canonical. At the selected
inner varying coordinate, the first-differing-bit partition contains
source {0,1}, destination {2,3} for every q=2^t>=4, with leading
zero prefix when t>2. Fixing (0,1) at the first selected position and
using d-2 singleton last-bit rectangles leaves exactly that edge.
The other last coordinate can be kept unselected: there are 2d-4
available preceding positions for the d-2 needed ones. This includes
the d=2 boundary case. At the outer level the product construction
with singleton source words at d-1 further positions gives exactly
the claimed two-element outer side.

The Gram-quotient step is essential and is correct. Every x_v+y_v
has the same pairing, namely one, with each x_w and y_w. Their
differences therefore lie in the radical and vanish in the actual
quotient. Thus y-differences are negatives of x-differences.
For the selected probes, the inner distance is precisely
d-2+[a!=r]+[b!=s]. It equals d only at the opposite binary corner;
all other outer coordinates are equal. Pairing a zero-sum corner
combination with all four probes returns its coefficients individually,
up to the nonzero rational scale -1/d and a permutation.
Consequently its three corner differences really are independent
in the quotient, not just in an auxiliary representation.

The resulting four variation lines have representatives
p, r-q, q, r-p in a three-dimensional space. They are pairwise
distinct and satisfy the displayed four-cycle dependence. Four
different coordinate lines in one basis would correspond to four
independent basis vectors, contradicting that dependence. The
argument uses rational address arithmetic and remains valid when
the unrelated data algebra has characteristic two.

The written scope is appropriately narrow. The full endpoint space
contains differences from both oriented sides and can be larger;
its coordinatization would not automatically coordinatize these
subspaces. Two-sparse descriptions, alternative bases, simultaneous
delivery and different rectangle families all remain possible.
No lower running-time claim follows.

I replayed the author's exact checker in this directory as
verify_source_basis_obstruction_replay.py. All 15 (d,q) pairs passed,
including 60 canonical sides, 60 rank-three edge triples, and 15
rejected wrong-probe offsets. The replay receipt is
source-basis-verification.json. This reuses the author's checker;
the independent part is the written proof audit above.

Credits: @CubeJerry, the pinned rational Gram geometry, Route C's
construction, and substantial ChatGPT multi-agent assistance.
