# Independent review of the five actual source compilers

**Accepted in the stated local, gross-cost scope.** The independent checker in this directory imports no source author executable and reconstructs the source matrices from `EARLY.json.gz` and the original X-route ownership list.

For each of sources 0, 45, 61, 62 and 100, I checked that the 480 labelled output rows contain each original owner exactly once, that each label's H destination agrees with that owner's actual X route, and that row x of the physically executed matrix is the literal row assigned to owner x. The input columns stay in their original coordinate order. Thus the physical row permutation is included in the matrix that is compiled; it is not supplied as an uncharged permutation operation.

My binary lift uses polynomial long division of each monomial product `a*t^k` by `t^6+t+1`. It does not use the author's field multiplication or NumPy block-lifting implementation. I also checked irreducibility by testing every monic divisor of degree at most three. Each field coefficient is placed on the six bit owners of the correct original field coordinate.

I independently regenerated the stated deterministic first-pivot binary elimination, including all three distinct-owner ADDs for each required row swap. The five physical matrix hashes, operation-stream hashes, ADD counts and swap counts all match the author receipt. The resulting words were replayed in both directions on the complete 2880-bit symbolic identity, so the check covers every input bit and every correlated combination of inputs, without sampling.

| Source | ADDs per direction | Paid three-ADD swaps |
|---|---:|---:|
| 0 | 2,433,642 | 2,213 |
| 45 | 2,412,700 | 2,278 |
| 61 | 2,391,802 | 2,406 |
| 62 | 2,353,561 | 2,512 |
| 100 | 2,345,849 | 2,475 |

The exact sum is 11,937,554 ADDs per direction and lane. Eight lanes and the forward/inverse pair give 191,000,864 source ADDs. Adding the previously accepted H-pair inventory of 1,509,520 gives 192,510,384 ADDs for these seven local components. The H642 complement's sixteen gap-six field exports and 96 binary INIT, MOVE and CLEAR operations of each kind remain part of that separate accepted H implementation. The source compilers themselves introduce no auxiliary owner, initialization, clear or export.

The inverse word is local only when all encoded owner values are again co-located. The proof explicitly leaves that global transport precondition open. These are the checkpoint6 early source maps, not the later prospective D1509 redesign. The bill is gross, omits the unbuilt H/D/K/F and global return work, and does not support an incremental saving, a complete supplier invoice or a new kappa.

Reproduce with `python review-b/check.py` from this package directory or any working directory. The independent exact result and hashes are retained in `review-b/output/RESULT.json`.

Reviewed by S031 worker B, 2026-11-20.
