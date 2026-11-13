# Independent review: scalar one-rank patch obstruction

## Verdict

I find B's one-rank patch obstruction sound under the stated scalar,
characteristic-two fitting and monotone no-Y-feedback interface. The
diagonal/noncontact argument is exact over a field, the E7 proper-flat bound
is applied to a genuinely proper intersection, and the 150-versus-120 count
follows from the refined support union. The upward-copy extension is also
sound with the declared local-copy premise: a copy born at a facet is already
covered by that cell's existing support union; a new local support subspace
outside it must arrive at that facet on its own upward record. A lower-chart
cache read on a Y path is contained in that Y path's last proper chart.

I additionally found a stronger visit bound for a single support-valid
rectangle, and a fitting-distance statement that does not assume any
rank-one or rank-ten factorization. These do not classify arbitrary rank-ten
fittings or arbitrary sums of rank-one matrices.

## Independent source and patch review

I rebuilt the 111 source root directions from the pinned native's rational
line charts, normalized them to integer norm-four E8 roots, and reconstructed
the scalar fitting by exact dot products: diagonal one and an off-diagonal
one exactly for real-orthogonal source roots. The exact rank is nine; foreign
row supports range from 55 to 62, with histogram

| Foreign contacts | Rows |
|---:|---:|
| 55 | 1 |
| 56 | 11 |
| 57 | 16 |
| 58 | 36 |
| 59 | 28 |
| 60 | 13 |
| 61 | 5 |
| 62 | 1 |

For a scalar patch `A=K^g+u v^T`, diagonal preservation gives
`supp(u)∩supp(v)=empty`. If `i∈supp(u)` and `j∈supp(v)`, then
`u_i v_j` is nonzero. A prescribed noncontact zero at `(i,j)` cannot be
changed, so that pair must be a real-orthogonality contact. Thus every root
in U is orthogonal to every root in V. This uses the no-zero-divisors property
of scalar fields; it is not asserted for block maps.

When `|V|>=3`, choose two distinct projective V roots v,w. U lies in
`v^perp ∩ w^perp`, which is a proper subspace of the E7 facet `v^perp`;
the admitted universal proper-flat maximum is 36. Therefore `|U|<=36`, so
at least 75 rows are unpatched. Each has at least 55 canonical contacts and
still needs `r_i+s_i>=2`. This proves at least150 required visits against
the 111 original X plus nine packet paths (120). If `|V|<=2`, no row loses
more than two support entries, leaving at least53; all111 rows need two
visits, or222 total. These are the frozen 150/120 and small-V cases.

The source rectangle rank-ten example is a useful negative control: its
12-by-12 support is cross-orthogonal, diagonal-safe, changes144 contact
entries, and has rank10. It is an algebraic fit, not a source word. It
illustrates why the theorem must not be described as excluding arbitrary
rank-ten matrices.

## Sharper single-rectangle arrival accounting

Use the same scalar patch assumptions and support bounds.

| Patch width `|V|` | Bound on affected rows | Residual contacts per affected row | Minimum required visits | Extra upward arrivals beyond q=9's 120 |
|---:|---:|---:|---:|---:|
| 0 | 0 | at least 55 on every row | 222 | 102 |
| 1–2 | no row loses more than 2 contacts | at least 53 on every row | 222 | 102 |
| 3–18 | at most 36 | at least `55-|V| >= 37`; at least one visit | at least 186 | 66 |
| 19 or more | at most 6 | unchanged rows alone force `2*105=210` | at least 210 | 90 |

For the last row, the admitted E8 root-flat count gives at most12 roots in
rank four and at most6 in rank three. Nineteen projective V roots cannot
span rank at most four, so `dim(span V)>=5`. Then U lies in a subspace of
dimension at most three and has at most six roots. This is the E8 flat
premise in the admitted coordinate-return proof; it is not an unproved
external ADE assumption.

The `3..18` row uses two different support thresholds. At least37 residual
contacts cannot lie in the one proper chart contributed by Y_i, since a
proper subspace has at most36 roots. For unchanged rows, more than52 contacts
cannot lie in the union of only two proper subspaces. The cell-local support
union is the Y_i last proper chart plus the X predecessor and packet
successor charts, so these force respectively one and two path incidences.

The q=8 version has at most119 original path visits. The corresponding
single-patch extra-arrival requirements are 103, 67, and 91. The original
31-arrival q=8 bound in B's proof is valid but not sharp.

## Additional ascending local copies

An upward copy adds no independent source input. At a chart where it is
created, its local remainder is already inside the existing cell's union of
X predecessor and packet successor charts. If it is read by Y_i at an
earlier chart on that Y route, its support is contained in Y_i's last proper
chart. A genuinely new subspace contribution to the facet union must be
carried by an additional record into that facet from a proper chart; one
monotone upward record can visit at most one of the pairwise incomparable
seven-dimensional target facets. Each such extra arrival therefore uses at
least one positive-rank MOVE, whose `r^(199/200)` price is at least one.
This accounts for extra pure-X upward records only; it does not cover
downward nonlocal copies, packet-family expansion, Y movers, or restarted
paths.

Using directed movement bounds, the optimistic q=9 direct-route base
`222*7^(199/200)+9*8^(199/200)` has less than 11.5420067271 left under the
limiting allowance. The sharper 66- and 90-arrival cases exceed that room by
more than54.4579932729 and78.4579932729 respectively; the `|V|<=2` case
exceeds it by more than90.4579932729. For q=8, the all-unit target costs1618
and leaves less than3.7508802112 even at the infinite-m limit. The 67- and
91-arrival cases exceed it by more than63.2491197888 and87.2491197888. These
are optimistic movement-only contradictions; ADD/INIT/cache costs and any
extra route refinements have not been charged.

## General scalar fitting-distance corollary

The local support proof also yields a statement without a low-rank
perturbation representation. Fix any vertex-gauge canonical fit `K^g`, and
for each row let `a_i` be its foreign support and
`d_i=|{j:A_ij != K^g_ij}|` for the actual scalar fitting A. Since both
fittings have the same prescribed zeros and diagonal, every changed position
lies among the canonical contacts. Thus A still has at least `a_i-d_i`
foreign nonzeros. The support theorem forces two visits if this count is at
least53, one visit if it is at least37, and gives no required visit when it
could be at most36.

To lower a row's demand from two to one requires at least `a_i-52` changed
entries; to lower it to zero requires at least `a_i-36`. The exact source
support histogram above and a small dynamic program minimize total changed
positions while allowing these optimistic row-by-row support deletions. The
result is a necessary Hamming distance from **every fixed** vertex-gauge
canonical matrix:

| Interface | Available original visits | Extra arrivals allowed in the movement comparison | Minimum changed matrix entries |
|---|---:|---:|---:|
| q=9, no extra copies | 120 | 0 | 619 |
| q=9, all affordable extra rank-one arrivals | 120 | at most 11 | 532 |
| q=8, no extra copies | 119 | 0 | 627 |
| q=8, limiting all-unit budget | 119 | at most 3 | 603 |
| q=8, fixed m=6 budget | 119 | at most 1 | 619 |

The DP is a relaxation: it permits every changed coefficient to delete one
contact and ignores fitting, chronology, and chart constraints. Consequently
the resulting distances are necessary lower bounds. This statement applies
to any scalar fitting used by a completed execution in the interface; it
does not say every rank-ten fit has rank-one form.

For a sum of separately support-valid rank-one patches, the final changed
positions are a subset of the union of their support rectangles. The union
must be counted once: overlapping patches and cancellations do not multiply
the Hamming distance. The distance bound therefore requires a rectangle
union of at least the displayed size in the no-extra-arrival cases. I do not
extend this rectangle decomposition to arbitrary rank-two perturbations,
whose individual terms may violate fitting zeros and cancel only in their
sum.

## Limits and pins

This proof excludes one support-valid scalar rank-one patch and gives a
separate final-matrix distance condition. It does not classify all rank-ten
fittings, show the lower bounds attainable, or construct a source word. The
all-V singular-Schur stratum and other transport/source architectures remain
outside the scalar one-patch statement. All source and dependency bytes are
pinned in `MANIFEST.json`.
