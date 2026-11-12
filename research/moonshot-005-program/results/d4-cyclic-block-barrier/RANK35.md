# Rank at least 35 from the complete full-block packing census

**Status: proved for the stated finite D4 partition interface, independently reproduced by the orchestrator. No new κ.**

This is a strengthening of the preserved rank-at-least-34 theorem in PROOF.md. Its earlier complete orthoframe catalogue and rank-33 cover proof remain valid. This note adds a stronger global packing certificate; it does not replace the physical scope or the accounting assumptions of that proof.

## 1. Source and complete catalogue

Use the same authenticated native source, compressed SHA256
`2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883`.
The 96 hosted normals are all nine-bit weight-three/weight-seven vectors after deleting the published 16 omitted normals and eight coupled normals. The pure-JS catalogue regenerates all 122,850 orthogonal quadruples, not only XOR-zero quadruples, and yields exactly 3,150 real D4 root spans. Exactly 90 contain twelve hosted root directions.

The original regeneration is in `verify-core.js`; `CATALOGUE.json` contains all spans and their three orthogonal families. Root subsequently authenticated the pinned gzip (SHA256, CRC and length), matched the 104/96 inventories, every hosted initial line/final facet and the full raw MOVE histogram. Those are root source-binding checks, not a claim that this reviewer recovered the unavailable old filesystem bytes.

Root also independently regenerated the 3,150 sets with an eight-coordinate half-sign closure, different from this reviewer's nine-coordinate orthoframe projection. Both catalogues agree.

## 2. At most four pairwise disjoint full hosted D4 blocks

Order the 90 full hosted blocks lexicographically by their sorted binary-normal lists. For a partial increasing-index packing, the next candidates are precisely the larger indices disjoint from every chosen block. Recurse over every such candidate. There is no heuristic pruning or numerical optimization.

The complete counts by packing size are

| Size | Number |
|---:|---:|
| 0 | 1 |
| 1 | 90 |
| 2 | 847 |
| 3 | 604 |
| 4 | 43 |
| 5 or larger | 0 |

The traversal has 1,585 nodes. Every packing occurs exactly once, because it has a unique increasing index order. The certificate lists every tuple. Every child retains exactly the larger disjoint candidates; an empty candidate list certifies that its branch has no extension. Thus the maximum size is exactly four.

One actual four-block packing is:

- 11,13,19,21,138,140,146,148,352,382,487,505
- 26,69,100,191,193,224,261,292,379,385,416,478
- 49,50,73,74,133,134,253,254,304,328,388,508
- 56,88,112,152,176,208,319,351,375,415,439,471

The checker rejects a duplicated full block and a deleted full block. The positive four-block witness prevents the vacuous assertion that all extensions were suppressed.

This is a complete finite combinatorial certificate for the pinned source. It is not an inference of asymptotic impossibility from a failed finite search.

## 3. Rank-density consequence

Partition all 96 hosted root directions into disjoint subsets of the D4 catalogue. Let a,b,c,d count blocks of real ranks 4,3,2,1. The root-subset bounds proved in PROOF.md are respectively 12,6,3,1. Every rank-four block that is not a full twelve-root block has size at most eleven. At most four full blocks can occur in a partition.

Consequently, for total rank R,

\[
 R=4a+3b+2c+d,\qquad
 96\le 11a+\min(a,4)+6b+3c+d.
\]

Suppose R is at most 34. If a is at most seven, the right side is at most

\[
 11a+\min(a,4)+2(34-4a)
 =68+3a+\min(a,4)\le93.
\]

If a is eight, the remaining rank is at most two, so the lower-rank blocks contribute at most three directions. The size is therefore at most

\[
 8\cdot11+4+3=95.
\]

No larger a is possible. Both cases contradict the required size 96. Therefore

\[
 \boxed{R\ge35.}
\]

This argument is stronger than enumerating only the possible rank-34 deficit shapes. It does not assert that rank 35 is achievable; the relaxed size bound at rank 35 is 98.

## 4. Consequence for the retained cyclic block architecture

Retain all physical restrictions of PROOF.md: disjoint D4 blocks; independent fresh full-field Gram return views priced at least their block ranks; genuine b/d routes in the cyclic family-chart schedule; all other assembly costs granted free. Shared mixed/current observations, joint returns across blocks, another route architecture and a different forward interface remain outside this obstruction.

For compatible enlarged family charts, put t=199/200 and

\[
 \beta=2+2\,2^t+2\,5^t-2\,8^t.
\]

The prior route theorem gives combined return and mandatory cyclic raw cost at least

\[
 R+3\beta(96-2R).
\]

It increases with R because \(\beta<1/6\). The new rank bound yields

\[
 \boxed{35+78\beta>40.5774346602217}
\]

per native word. For minimal family charts the stronger floor is
\(35+78\delta>40.8059697961141\), with
\(\delta=2+2^t+3^t+4^t+5^t-2\,8^t\).

The complete optimistic source headroom is 39.07974274338085 for the original eight rank-nine forward packets plus eight coupled corrections. For the actual late-two forward source word, including its mandatory first-bank raw refinements, it is 39.49812968891777. Hence the compatible enlarged-chart floor exceeds that implemented late-two allowance by more than 1.0793049713039.

All signs are certified by 160-bit integer power intervals in RANK35-BUDGET.json. The core was rerun with rankLower=35; this is not a floating-point feasibility decision.

Other forward architectures may have larger headroom. In particular this does not exclude the broader interleaved-forward allowance, approximately 41.2695 after the coupled corrections. Do not promote this fixed-interface result to a universal D4 or multiplication lower bound.

## 5. Reproduction and provenance

Run:

    node verify-packing.mjs CATALOGUE.json

The pure combinatorial function was executed in the available JavaScript engine. The thin Node standard-library file-reading wrapper was written after the filesystem outage and was not itself executed in that unavailable runtime. The function and exact receipt are the verified computation.

The rank-35 budget uses the unchanged pinned H4 invoice and native raw histogram documented in PROOF.md. The original rank-34 receipt remains historical evidence; use RANK35-BUDGET.json for the strengthened final gate.

Credit: @CubeJerry programme. The root orchestrator discovered the full-packing strengthening and independently generated the catalogue/packing census. The global-adversary worker independently reconstructed the census, supplied the direct rank-density argument, and regenerated the exact rank-35 budget. AI-assisted research and verification.
