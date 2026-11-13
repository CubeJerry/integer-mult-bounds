# Independent audit of the binary four-quotient obstruction

PASS on frozen root manifest1c727243747e684b7d633fe4d76bc723c823909d4a221cfdb66fbe38565897e7 and proof0f37573476c75cbd8d27364c8e883ca747fb9bffc149340a9f5942b0eab0a578. The proof, exhaustive catalogue coverage, and dangerous-cap screen pass independent review and different implementations. No correction of the claimed theorem is needed. The four-representative weight32 argument, implicit in the frozen text, is made explicit below.

Scope remains scalar F2, the specified q8 unit-refined Q={1:1618} movement profile with at most three extra upward-local arrivals, and the generated-cache monotone interface WITHOUT Y feedback. This is a quotient-dimension lower bound, not arbitrary fitting rank13 or a completed supplier.

## Complete catalogue coverage

A class with gamma>=13 has at least seven positively improved rows, since each row saves at most two. Their binary normals span rank at least three. The reviewed gluing lemma provides a BINARY representative g and the exact fitting formula. The17 theorem's envelope therefore applies to this actual group of improved rows. Our independent enumeration evaluates ALL569 legal parameter triples and explicitly emits every case whose upper bound is at least13:

| r | s | j values | Complete generated family |
|---:|---:|---|---|
|3|4|1|rank-three flat subset|
|3|5,6|0|rank-three flat subset|
|4|4|1,2,3,4|four-subset with isolated root|
|4|5|1,2|isolated root plus rank-three subset|
|4|6,7|1|isolated root plus rank-three subset|
|5|5|4,5|orthogonal clique|
|6|6|5,6|orthogonal clique|
|7|7|6,7|orthogonal clique|
|8|8|7,8|orthogonal clique|

There are19 cases in this table. In particular the newly threshold-relevant (6,6,5) and (7,7,6) are included: if all but one of the independent support roots are orthogonal to every other support root, the whole support is mutually orthogonal. For r4 with isolated root, removing that root leaves rank three and support size4..6; thus the rank-three-extension generator is exhaustive. All representatives have support at most eight. Low-normal-rank groups have at most three rows and cannot reach gain13.

Our primary-source generator uses the full120 perpendicular-mask/F257 closure method from our independent17 audit, not the author's numpy Gram-adjugate membership. It then generates each listed support family and uses a bitset orthogonal-clique recursion. It makes6329841 candidate calls, independently split as146521 rank-three supports,2577100 isolated extensions,3483013 isolated quads and123207 orthogonal cliques. It reproduces all clique counts and all38324 classes, with exactly the gain histogram13:20290,14:9988,15:6912,16:1122,17:12. Every class mask, gain and one-/two-saving row mask agrees with the frozen author catalogue; comparison is semantic and does not assume the author's support-list ordering.

We separately enumerate all512 binary codewords and verify distance48. We also compute all111 zero-restriction images, each of size256, with minimum nonzero weight at least18. This provides an additional independent exactness argument for the row masks: for a representative of weight<=8, any restriction outside its closed neighborhood would have nonzero weight<=8 and cannot be a restricted codeword. Thus availability is exactly M(V). The changed fitting row is unique, giving two savings on J and one on eligible U, exactly as catalogued. This corroborates the author's enlargement-and-uniqueness argument and rules out omitted improving rows in a high class.

## Small-representative XOR and disjointness checks

Distinct representatives of weight<=8 cannot differ by a nonzero C word: their difference has weight<=16<48. If a sum of two high classes had gamma>=13, its catalogue representative c would satisfy a+b+c in C, of weight<=24<48. Therefore c must equal the literal XOR a^b. We independently test all162603561 distinct pairs of18034 high classes against our rebuilt full38324 catalogue, and find none. Their sums have gamma<=12; in particular high classes are sum-free in the quotient.

For a dangerous FOUR-class cap, quotient sum zero gives a+b+c+d in C with weight<=32<48. Hence the four literal small representatives XOR to ZERO. This separate four-representative argument is necessary for cap coverage; the earlier24 bound on three representatives alone would not justify it.

The twelve gamma17 one-saving masks each have17 rows and pairwise intersection at least five in our independent data. To attain17 that direction must receive every one of its improving rows. Row direction groups in a fitting are disjoint, so at most one direction can actually attain17; all others save at most16. The proof uses attained disjoint assignments, not a mistaken global reduction of the individual catalogue gains.

## Different exhaustive cap algorithm

Our C++ checker does NOT build the root top-pair XOR table and scan every high pair against it. Instead it splits all dangerous caps by the number of top classes (gain>=16):

- With at least three top classes, enumerate ALL242403084 triples of1134 top classes, compute the fourth literal XOR, and look it up in the independent catalogue. Retain a distinct fourth high class and potential>=64.
- With exactly two top classes, potential>=64 forces BOTH gains to be17 and both remaining gains to be15. Enumerate all456192 choices of a pair of the twelve17 classes and one6912-element15 class; lookup of the fourth covers this entire remaining case.

With at most one top class, potential is at most17+15+15+15=62, so no dangerous cap is omitted. Sorted four-class keys deduplicate the enumerations. The indices belong to the full38324 catalogue and fit16 bits; four such indices fit the64-bit key exactly. Mask arithmetic uses unsigned128-bit values;111-bit fields cannot overflow it. Hash collisions are resolved by exact key equality.

This different decomposition yields the same3989 dangerous caps. For each, our best disjoint-row upper bound is popcount(one UNION two)+popcount(two), equal to the per-row maximum contribution across the four directions. It never sums incompatible per-direction maxima. The exact maximum is46; the complete histogram matches32:3935,41:12,42:14,43:4,44:3,45:18,46:3. The C++ source explicitly fails compilation under NDEBUG and contains exact assertions.

## Final proof and boundaries

The Fano-plane argument is sound. In a binary quotient of dimension at most three there are at most seven nonzero directions. Sum-free high subsets have at most four elements; a four-element one is an affine plane, with literal cap relation justified above. With at most two high directions, at most one attained17 gives total saving<=17+16+5*13=98. Three high directions are independent; their three pair sums save at most12 each, giving<=17+16+16+3*12+13=98. Four high directions with potential<=63 give<=63+36=99; dangerous caps instead give<=46+36=82. Thus total saving is at most99 and ell sum is at least123.

The declared q8 path/profile supplies at most111+8+3=122 arrivals, so it cannot complete in this interface. Therefore dim((row(A)+C)/C)>=4. If a historical code actually contains C, its dimension is at least13; arbitrary rank-ten spaces with smaller intersection with C remain unclassified. The proof does not establish this four-dimensional conclusion for q9's looser arrival allowance, for larger scalar fields, arbitrary blocks, Y feedback, nonmonotone paths or a different paid profile. Initial Hub modes are not automatically retained in the normalized historical code.

The catalogue and cap computations are exact fixed-source finite statements; fitting and proxy savings do not supply a physical word. All222 endpoints, causal acquisition, original X restoration, ordinary work, physical maps, owned erasure, compiler and strict suppliers/five foundations remain. No new complete kappa is inferred.

Reproduction uses explicit paths: run generate.py with --repo, --root-bundle and --output; compile check_caps.cpp with a normal C++17 compiler and assertions; run it on generated catalog-input.txt, saving stdout to CAP-REVIEW.json; then run finalize_checks.py with --review and --root-bundle. The compiled executable and regenerated plain-text input are runtime products, not frozen source artifacts. The generator output binds the input by SHA. All source/hash comparisons and substantive finite computations completed successfully in this audit.
