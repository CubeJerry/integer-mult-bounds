# Root independent review and closed-form fitting-distance proof

This reviews B's one-patch proof and C's sharper geometry/Hamming corollary. Scope: scalar characteristic-two fittings under the monotone generated-cache, no-Y-feedback scattering interface, including the stated upward-only local-copy extension. General block coefficients and arbitrary rank-ten classification are excluded.

Diagonal and forbidden zeros force a nonzero rank-one perturbation u v^T to have disjoint supports U,V, every U root orthogonal to every V root. After actual historical G modes are separated, the refined local-support union holds. Each original ascending source or descending packet visits at most one7-dimensional receiver facet. A fresh local copy adds a new support subspace only by a distinct arrival from a proper chart; copying at the facet adds none. These independently justify B's150/120 obstruction and C's sharper186/120 worst case. Rank4/3 root bounds use the admitted simply-laced subsystem argument on the reflected real BIT E8 configuration; no binary-chart contact graph is transferred.

## Closed form replacing the distance DP

Fix any vertex gauge K^g. Let a_i be its foreign support size and d_i the number of entries changed in actual fitting A. Each change deletes at most one canonical nonzero. The E7 bounds36 and52 force one or two incidences beyond Y_i's last proper chart whenever a_i-d_i exceeds36 or52. From baseline two visits per row, saving the first visit costs at least a_i-52 changes; saving both costs at least a_i-36. The second marginal cost is16.

All111 actual rows have a_i in55..62. Every first marginal cost3..10 is cheaper than every second marginal cost16. For at most111 required savings, an optimum using a second saving while leaving a first unused can be improved by exchanging them. Thus the exact optimistic deletion optimum is the sum of the required number of smallest a_i-52 values. This is a proof, not an extrapolation from the finite DP.

The independently reconstructed first-cost histogram is {3:1,4:11,5:16,6:36,7:28,8:13,9:5,10:1}, total698. With q packets and e extra upward-local arrivals, at most111+q+e visits exist. Required savings are111-q-e:

| q | e | Saved visits | Necessary changed entries |
|---:|---:|---:|---:|
| 9 | 0 | 102 | 619 |
| 9 | 11 | 91 | 532 |
| 8 | 0 | 103 | 627 |
| 8 | 1 | 102 | 619 |
| 8 | 3 | 100 | 603 |

These hold relative to every fixed gauge without assuming rank-one form. Relaxed deletion witnesses are not fittings or sources. e=11 and e=3 are optimistic limiting allowances; m6 q8 allows only e<=1. Every extra arrival remains paid.

## Area bound for an individually support-valid rank-one patch

The patch support is a real-orthogonality rectangle U times V. Put r=dim span U and s=dim span V; r+s<=8. For ranks<=6 the admitted simply-laced root-subsystem argument gives N_1=1,N_2=3,N_3=6,N_4=12,N_5=20,N_6=36. It applies because the full norm-four actual root set is reflection closed. Roots lying in a real subspace form a finite simply-laced root system; replace a subspace by the span of its contained roots if needed. For rank7 the harmless bound111, paired with rank1, still lies below144. Rank8 cannot have a nonempty orthogonal root support.

Maximizing N_r*N_s with r+s<=8 gives144 at r=s=4. Hence any individually fitting-preserving scalar rank-one patch changes at most144 entries. The separately checked D4-by-D4 example attains12*12=144 as an algebraic patch.

If A-K^g is a sum of p rank-one terms each individually preserving the diagonal and prescribed zeros, its changed entries lie in the union of their support rectangles. Overlaps/cancellations only reduce that union, so p>=ceil(distance/144). At q8, with zero, one or all three limiting affordable extra arrivals, at least FIVE such patches are necessary. At q9, five are necessary without extra arrivals and four with all11 optimistic arrivals.

This does NOT lower-bound the unrestricted matrix rank of A-K^g. Terms of an arbitrary low-rank factorization may violate fitting zeros and cancel only in their sum. No classification of rank-ten matrices or all q8 sources is claimed. The result excludes a construction assembled from at most four individually valid corrections of the canonical fitting at q8; it calls for coordinated zero constraints or a different fitting representation. No attainability, supplier or new kappa follows.
