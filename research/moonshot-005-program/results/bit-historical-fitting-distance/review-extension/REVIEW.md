# Independent audit: closed-form patch distance and rectangle count

Status: **accepted within the stated scalar interface and decomposition class**. I independently reproduced the closed-form Hamming lower bounds from the already frozen exact support histogram and checked the rank-one rectangle area bound using the admitted E8 low-rank root-flat counts. I found no arithmetic or logical gap in the extension.

## Closed-form visit-distance calculation

Using the support histogram from my earlier exact source review, the canonical row supports (a_i) lie in 55 through 62 with counts

\[
1,11,16,36,28,13,5,1.
\]

To reduce a row's visit requirement from two to one, it must delete at least (a_i-52) contacts. These first marginal costs range from 3 to 10. A second saved visit costs another (52-36=16) deletions for every row. Thus every first marginal is strictly cheaper than every second marginal. For any required number of savings up to 111, an exchange argument shows an optimum uses only first marginals, sorted increasingly. This directly gives the lower bounds and replaces the small DP without relying on solver behavior.

| Packets (q) | Extra arrivals (e) | Required saved visits (111-q-e) | Minimum changed entries | Patches if each area is at most 144 |
|---:|---:|---:|---:|---:|
| 9 | 0 | 102 | 619 | 5 |
| 9 | 11 | 91 | 532 | 4 |
| 8 | 0 | 103 | 627 | 5 |
| 8 | 1 | 102 | 619 | 5 |
| 8 | 3 | 100 | 603 | 5 |

For example, the 102 cheapest first marginals comprise costs (3, 4^{\times11},5^{\times16},6^{\times36},7^{\times28},8^{\times10}), totaling619. For the q8 limiting case, the 100 cheapest comprise (3,4^{\times11},5^{\times16},6^{\times36},7^{\times28},8^{\times8}), totaling603. No second marginal is selected because its cost is at least19 while every unused first marginal is at most10.

The relaxed deletion model is one-sided: it assumes each changed entry can remove one support incidence, even though many changes will not do so and the row choices may not form any fitting. Therefore its minimum changed-entry total is a necessary lower bound, not an attainable matrix or source schedule.

## Support-valid rank-one patch area

For a nonzero scalar rank-one term (uv^T), let (U) and (W) be the source-root sets indexed by the supports of (u) and (v). If that term individually preserves the diagonal and every prescribed zero, (U\cap W=\emptyset) and every root in (U) is real-orthogonal to every root in (W). Their real spans are orthogonal, so their dimensions (r,s) obey (r+s\le8).

The admitted E8 root-subsystem proof bounds root lines in ranks 1 through 6 by (1,3,6,12,20,36). For rank7, the trivial bound111 is already enough; a nonempty orthogonal companion has rank at least1. Enumerating the dimension pairs under (r+s\le8) yields maximum rectangle area 144 at ((4,4)): (12\cdot12=144). The rank7/1 case is at most111. The (r=s=4) D4-by-D4 patch is an algebraic sharpness witness, but it is not a physical word.

If a final fitting difference from a fixed canonical gauge is a sum of (p) rank-one terms that each individually preserve all fitting zeros and the diagonal, changed entries lie in the union of those (p) support rectangles. Cancellations and overlaps only shrink the changed set. Thus (p\ge\lceil d_H/144\rceil). In the q8 movement-allowed cases (d_H\ge603), so at least five such patches are necessary. At fixed (m=6), the budget permits at most one extra unit arrival, and the bound strengthens to (d_H\ge619), still five patches.

## Scope checks

This does **not** bound the unrestricted matrix rank of (A-K^g). In an arbitrary rank-(p) factorization, individual terms can violate diagonal or forbidden-zero constraints and cancel only after summation. It also does not classify rank-ten fittings, prove any distance bound attainable, or rule out a different fitting representation. The five-patch conclusion applies only when every rank-one summand itself respects every fitting constraint.

The source support histogram was not re-enumerated here; it is pinned in the earlier independent review `worker-c/rank-one-patch-review/RESULT.json`. The q8 extra-arrival allowances (three in the limiting all-finite-(m) budget, one at fixed (m=6)) agree with the pinned independent q8 budget receipt. Every movement comparison remains an optimistic movement-only necessity: extra ordinary work, arithmetic, and source acquisition are separate costs.

## Pins and replay

Independent arithmetic replay: `replay_arithmetic.py`; output: `RESULT.json`.

- Root extension: `root-work/patch-distance-review/REVIEW.md`, SHA256 `a503084a154c3383ba1e5ae75f5299573556850f31339eb95d25cb2c89379765`.
- Root arithmetic/source receipt: `root-work/patch-distance-review/RESULT.json`, SHA256 `b2dab00e3a816644b516a5bf10d8db1729da3eb5796f80d2246c741faebaa6de`.
- Prior independent support census: `worker-c/rank-one-patch-review/RESULT.json`, SHA256 `3a4bf899025257c5faeff8873edab410735957cda5a881415993ddce1d88fb7b`.
- Admitted low-rank E8 geometry: `programme/research/moonshot-005-program/results/coordinate-return-optimum/PROOF.md`, SHA256 `d0d4d4c6153453861bcf931353fcdb700deb44f4d380a0b39bf6ba2779d0ccac`.
- q8 movement budget receipt: `root-work/final-path-q8-budget/RESULT.json`, SHA256 `f1ec7b16a986c7b7ce7d9a3788bbea2943810cfd70386e554bd14a21759e07e2`.
