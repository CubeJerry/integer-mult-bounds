# Rectangle tests limit whole canonical blocks after both marked stars are exact

Consider the fixed native mixed physical word from `bit-global-source-facet-row-column`, with arbitrary separate bijections on each complete original donor input and each receiver output. The 220-edge endpoint word is one such choice. If all 123 whole nonidentity S028 edges are exact, a new pair of canonical edges may conflict even when every single constituent transfer is invertible. We certify these conflicts on the original 3,840-dimensional source space and allow arbitrary nonlinear endpoint bijections.

First fix all 62 incoming targets at receiver 80. For any other receiver \(i\) and two of its native donors \(j,k\) also reaching receiver 80, both \(B_{ij}\) and \(B_{ik}\) have canonical targets. If both are exact after endpoint bijections, the two maps

    B_ij B_80j^(-1)   and   B_ik B_80k^(-1)

are jointly left/right equivalent by the same two bijections to \(T_{80j}^{-1}\) and \(T_{80k}^{-1}\). Therefore the two pairs have exactly the same number of agreeing inputs. The target difference has rank at most 64. Indeed, the two nonidentity increments have their entire image in the same physical 64-field original bank, and taking the difference of inverses of invertible matrices preserves difference rank. The native difference, however, has rank at least 79. Apply it to 80 common, explicitly specified original inputs and then select 80 actual output rows in a true native copy. Every one of the 55,395 distinct choices across the other 110 receivers gives rank 79 or 80. Thus the native maps agree on at most \(64^{3840-79}\) inputs while the target maps agree on at least \(64^{3840-64}\). Local bijections cannot reconcile them.

Dually, when all 61 outgoing targets of donor 10 are exact, any other donor can supply at most one complete canonical edge to these 61 receivers. For two native receivers \(i,k\) of that donor, use the differences of \(B_{i,10}^{-1}B_{ij}\) and \(B_{k,10}^{-1}B_{kj}\). All target increments now read from the same original 64-field bank, so the same rank upper applies. We test the transpose of the native matrix difference to measure its GF64 rank. The proof of the agreement-count invariant still concerns the original maps and arbitrary endpoint bijections. Every one of 53,806 distinct choices gives projected native rank 79 or 80.

The first census covers 3,531 canonical edges and the second covers 3,480. The two overlap on the native edges between the 61 outgoing leaf facets and the 62 incoming leaf donors. The marked-row and marked-column requirements permit at most one complete canonical edge at each of the 49 other output sites and the 48 other input sites respectively. The overlap can contain only an ordinary bipartite matching, of cardinality at most 61. Hence at most 158 entire canonical targets can be correct in the union under these two necessary tests. The exact union size and induced minimum number of failures are in `output/RESULT.json`.

The checker starts from the actual paid source programming and the physically expanded H, D, K and F. It verifies the normalization of each chosen test vector through the full 480-component Schur system in the eight coupled copies, then projects the true composed words. Seven direct full transfer controls per direction audit the reduced computation. Each ordered rank census has a fixed digest. This obstruction fixes the internal bilateral word; it does not exclude changing H, D, K, the early or late source programming, or the underlying facet before the endpoint recalibration.

    python -B PATH/author/check.py --repo REPOSITORY --out FRESH

Python, NumPy and a C compiler are required. Optional `--cache-dir`, `--late-cache` and `--source-cache` reuse checked physical inputs. Credit @CubeJerry and the native construction and target authors. Substantial OpenAI assistance.

## Sharp optimum across the 5,055 canonical edges touching either star

The 1,956 canonical edges joining a leaf receiver of donor 10 to a leaf donor of receiver 80 permit at most **one** exact edge in total. To prove this stronger restriction, for every such edge form the map

    M_ij = B_i,10^(-1) B_ij B_80,j^(-1).

Write \(T_i=T_{i,10}\) and \(T_j=T_{80,j}\). When this edge and both its incident marked stars are realized, substitution in the three target equations gives

    M_ij = G_10 (T_i^(-1) T_j^(-1)) H_80.

Here \(G_{10}\) and \(H_{80}\) are the same arbitrary bijections for every prospective bridge. Two bridges could therefore both be exact only if the pair of native maps has the same number of inputs on which they agree as the pair of target maps. For edges \((i,j),(k,l)\), the target difference \(T_i^{-1}T_j^{-1}-T_k^{-1}T_l^{-1}\) has rank at most 128. This follows by adding and subtracting \(T_k^{-1}T_j^{-1}\). The two outgoing perturbations read the same original 64-field source bank, while the two incoming perturbations write the same original 64-field output bank. Inversion of the individual invertible factors preserves each corresponding difference rank.

`check_double.py` constructs one common 130-column original input probe and one common 134-row original output probe. It pulls the latter back through every actual \(B_{i,10}^{-1}\), pushes the former through every actual \(B_{80,j}^{-1}\), and evaluates their sandwich on each complete native mixed transfer. It checks these projected matrices against direct native multiplication at five spaced edges. For **all 1,911,990 unordered pairs of the 1,956 candidate bridges**, the projected native difference has rank 130. Their native agreement sets therefore contain at most \(64^{3710}\) inputs, while the target maps agree on at least \(64^{3712}\). This inequality excludes even two bridges with distinct donors and receivers, independently of whether either endpoint recalibration is linear.

Combining the two one-sided results and this two-sided result permits at most 49 outside-row edges, 48 outside-column edges and **one inter-star bridge**. The independently compiled 221-edge connected spanning-tree word realizes all 123 marked matrices plus 98 such canonical edges. Consequently the exact optimum on the union of 5,055 applicable canonical edges is **98** under arbitrary endpoint bijections fixing this native internal word and realizing every marked target. At least 4,957 of the original 6,470 target blocks must fail, leaving at most 1,513 complete original target blocks globally under these hypotheses. This proves no unconditional global block count for words with different internal coefficients.

    python -B PATH/author/check_double.py --repo REPOSITORY --out FRESH

The optional probe cache is authenticated against the full ordered native 134 × 130 matrices. The 35 MB array is generated from the input word when absent. `output/DOUBLE-RESULT.json` and `output/DOUBLE-INPUT.json` include the exact census and content digests. The common-arithmetic definition uses the same GF64 polynomial and physical owner order as the bilateral construction.

## Canonical targets independent of either marked star

For four canonical edges \((i,j),(i,l),(k,j),(k,l)\), exact identity after arbitrary local endpoint bijections would give \(B_{ij}B_{kj}^{-1}=B_{il}B_{kl}^{-1}\) as maps on the entire original field space. These four physical maps are invertible linear maps, so their original \(2\times2\) block matrix would have rank exactly 3,840. Restrict it to the seven ordinary copies on all selected original inputs and outputs. The resulting submatrix is the direct sum of seven copies of the native 480-field rim rectangle, of rank

    7 [480 + rank(R_ij R_kj^(-1) − R_il R_kl^(-1))].

A projected native difference of rank at least 69 already forces the full two-by-two rank above 3,840. `check_flat.py` tests every all-canonical rectangle using 76 genuine rim output rows and 71 genuine input directions. Its finite receipt records the complete census and field-array hashes. Its proof fixes the same internal native operator and allows every marked target to be sacrificed.

Consequently the bipartite graph of complete correct **canonical** edges of this native word after any endpoint bijections is four-cycle-free. Each unordered pair of donors shares at most one exact receiver. If receiver degrees are \(d_i\), double counting gives \(\sum_i \binom{d_i}{2}\le\binom{111}{2}=6105\). Among integer degree lists of given sum the minimum is attained by balancing. At 1,221 total incidences, all 111 degrees can be 11 and this lower bound already equals \(111\binom{11}{2}=6105\). Every larger sum violates the inequality. Thus at most 1,221 of 6,347 complete canonical matrices can be correct and at least **5,126 canonical matrices fail** for every such endpoint choice. Even granting all 123 nonidentity matrices, at most 1,344 of the 6,470 complete targets can be correct. The conclusion concerns this fixed internal physical word, with arbitrary endpoint bijections.

    python -B PATH/author/check_flat.py --repo REPOSITORY --out FRESH

### Sharpening the global count when the marked edges may be sacrificed

The canonical graph in fact has only 110 possible nonisolated donors and 110 possible nonisolated receivers, since every proper block at donor 10 or receiver 80 is nonflat. The same integer degree balancing bounds its edge count by 1,204. The two star censuses strengthen the total count even when an arbitrary subset of the 123 marked edges is kept.

Suppose \(u\) incoming marked edges and \(v\) outgoing marked edges are exactly realized, where \(0\le u\le62\) and \(0\le v\le61\). Let \(m\) be the number of correct whole canonical edges. No receiver is incident to two of the \(u\) corresponding donors, and no donor is incident to two of the \(v\) corresponding receivers. When both sets are nonempty, their mutual rectangle contains at most one correct edge by the two-star pair test. Thus the total degrees of these \(v\) receivers is at most \(110-u+1\), and that of these \(u\) donors at most \(110-v+1\). Without the opposite set the appropriate cap is 110. Moreover the usual four-cycle pair count on the receiver degrees has at most \(\binom{110}{2}-\binom u2\) available donor pairs, and the transpose has the corresponding bound with \(v\).

For each allowed \((u,v)\), `extremal.py` independently minimizes the degree-pair count by balancing the degrees within each of the two groups, enumerating every possible group degree sum up to the applicable cap. It also imposes the four-cycle bound on the outside \((110-v)\times(110-u)\) rectangle. All 3,906 integer cases then give \(m+u+v\le1220\). Consequently **at least 5,250 of all 6,470 original target matrices fail under every choice of endpoint bijections** with the internal word fixed, independently of whether any particular marked block is required. Without charging marked successes, at least 5,143 of the canonical blocks themselves must fail.

If all 123 marked edges are retained, the outside 49 × 48 canonical rectangle admits at most 357 edges by the same degree bound. Together with the sharp 98-edge cap on the 5,055-edge touching union, the entire word can realize at most **578 of the 6,470 original target blocks**. At least 5,892 fail in this fully marked regime. The lower bound of 221 exact blocks is realized by the connected two-star word. The separate higher-girth audit of the remaining 49 × 48 rectangle in `bit-global-two-star-target/review` improves its upper bound from 357 to 158. Combining that result with the sharp anchored 98 gives the stronger overall interval **[221, 379]** when all 123 marked blocks are required.

    python -B PATH/author/extremal.py --out FRESH
