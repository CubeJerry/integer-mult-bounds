# Open cube walks lower connector characteristic thresholds

**Scoped theorem and exact certificates; No new κ.** Closure can cost one
unit of characteristic in the balanced cube-walk route to unsigned dirty
connectors. We prove an all-dimension one-unit bracket, determine its value
at every odd prime dimension and other explicit residue classes, and supply
sharp Hamilton paths at dimensions 6, 9 and 10. Together these determine the
cube-covering-walk threshold for every dimension through 13. This answers
part of the open-path question in CrocSwap/integer-mult-bounds#6568; it is
neither an unrestricted depth-two optimality theorem nor a supplier result.

The upward/downward conversion of **open** walks is already proved in
[the merged Gray-growth package](../connector-gray-growth/README.md),
CrocSwap/integer-mult-bounds#6071. The new contribution is sharper flip-count
thresholds, explicit attaining paths outside the unique-maximum deletion
case, and complete independently implemented dirty-input checks.

```sh
python3 -B scripts/research_package.py --package research/connector-open-walk-threshold
```

The registered commands print `PASS_OPEN_PATH_THRESHOLD`,
`PASS_INDEPENDENT_OPEN_PATH_CONNECTOR` and `PASS_OPEN_PATH_REGENERATION`.
All three also run under optimized Python. Standard library only; about four
seconds for the complete registered replay on the tested Python 3.12.14 host.

## 1. Exact statement and proof

Let P(k) be the minimum, over finite walks of the binary k-cube that start
at zero and visit every vertex, of the largest coordinate-flip count.
Every step flips exactly one bit. Closure and distinctness of vertices are
not required; our finite upper-bound witnesses are Hamilton paths.

Write C(k) = 2 ceil(2^(k-1)/k), for k >= 2. The classical balanced cyclic
Gray-code theorem supplies a Hamilton cycle with each coordinate count
in {2q, 2q+2}, where 2^(k-1) = qk+r, 0 <= r < k. Exactly r coordinates
have the larger count when r > 0. See G. S. Bhat and C. D. Savage,
*Balanced Gray Codes*, Electronic Journal of Combinatorics 3 (1996), R25,
Theorem 1, [DOI:10.37236/1249](https://doi.org/10.37236/1249).
This is an inherited existence theorem, not a new proof here. Every closed
covering walk has at least 2^k edges and even coordinate counts, so its
maximum count is at least C(k). Thus C(k) is also the optimum for closed
covering walks.

**Theorem.** P(1)=1. For k >= 2,

```text
ceil((2^k-1)/k) <= P(k) <= C(k).
```

More precisely:

1. If r=0, then P(k)=2q=C(k).
2. If r>0 and 2r-1>k, then P(k)=2q+2=C(k).
3. If 0<r and 2r-1<=k, then P(k) is in {2q+1,2q+2}.
4. If r=1, then P(k)=2q+1=C(k)-1. In particular this holds
   for every odd prime k, by Fermat's theorem.

*Proof.* A covering walk visits 2^k vertices and therefore uses at least
2^k-1 edges. Summing coordinate counts gives the lower bound, including for
walks with repeated vertices. Deleting an edge of a balanced Hamilton cycle
produces an admissible path with maximum count at most C(k); translation
and a change of starting point put its first vertex at zero. Substitution
of 2^(k-1)=qk+r in the lower bound proves cases 1--3. If r=1, precisely
one coordinate of the balanced cycle has count 2q+2. Delete any edge of
that coordinate. Its count becomes 2q+1 and all other counts remain 2q,
attaining the lower bound. For odd prime k, 2^(k-1)=1 modulo k. ∎

Thus opening a walk can lower this characteristic threshold by **at most
one**, at every dimension. The theorem does not assert that the lower bound
is attainable in every one-unit-gap case. Its infinite statements use the
written proof and inherited cyclic theorem, not a finite arithmetic scan.

## 2. Sharp finite certificates beyond unique-maximum deletion

`WITNESSES.json` contains one transition sequence per row below. Starting
from zero and XOR-flipping the indicated coordinate visits every cube vertex
exactly once, with the listed counts. These are positive exact certificates,
not evidence drawn from an unsuccessful search.

| Dimension k | Flip counts | P(k) | C(k) | Endpoint Hamming weight |
|---|---|---:|---:|---:|
| 6 | 10,10,11,11,11,10 | 11 | 12 | 3 |
| 9 | 57,57,57,56,57,57,57,56,57 | 57 | 58 | 7 |
| 10 | 103,102,103,102,103,101,102,102,103,102 | 103 | 104 | 5 |

The maximum count in each row equals ceil((2^k-1)/k), proving optimality
even among covering walks with repetitions. The corresponding balanced
cycles have respectively 2, 4 and 2 maximal-count coordinates; deleting a
single edge from them cannot lower their maximum. The displayed paths have
endpoints at distance greater than one, so none is a Hamilton cycle with
one edge removed. They supply the additional cases needed for:

| k | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| P(k) | 1 | 2 | 3 | 4 | 7 | 11 | 19 | 32 | 57 | 103 | 187 | 342 | 631 |

Discovery used endpoint Pósa rotations of the reflected Gray path. The
search domain was Hamilton paths reachable by these rotations in dimensions
6, 9 and 10, with `random.Random(43)` independently reset for each dimension,
a cap of 3,000,000 iterations each, and stopping at the first path attaining
the universal length bound. It stopped after 565, 1195 and 2242 iterations.
This is not exhaustive coverage of Hamilton paths; no negative search claim
is made. `generate.py` reproduces the exact certificate objects. Its
floating-point acceptance rule is only for discovery; both proof checkers
use exact integers and do not import the search.

## 3. Conversion to the actual unsigned dirty connector

Here is the inherited construction, included to identify exactly what the
threshold controls. Fix any covering walk g_t starting at zero. Let U(t)
and D(t) count upward and downward flips coordinatewise, and let f_j be the
total count of coordinate j. For any integer characteristic c>=2 with
c>=max_j f_j, make the **positive** source-call word

```text
W = (upward labels in walk order)
    (c-f_j additional copies of each source j)
    (downward labels in reverse walk order).
```

Every source appears exactly c times. Write a(t)=sum_j U_j(t),
b(t)=kc-sum_j D_j(t). The actual prefixes of W at these two boundaries
have integer counts U(t) and c*1-D(t). The first is in the upward block;
the second leaves precisely the reversed first D(t) downward calls as its
suffix. Thus a(t)<=b(t), and their prefix sum is c*1+g_t. There is no
closure hypothesis. The arbitrary walk may revisit vertices; use its first
visit to each required mask.

In the unchanged interface, `B_j` means `z += B_j x_j` and `A_m` means
`y_m += A_m z`. At these two boundaries read output m=g_t, and give it
c-2 more reads at boundary zero. Then each A_m and B_j occurs exactly c
times. The c copies of arbitrary dirty z0 cancel; the source coefficients
sum to m modulo c; z is restored and x_j is unchanged. This implements
`y_m += sum_(j in m) A_m B_j x_j` for every nonzero mask simultaneously,
over every nonzero unital ring of characteristic c and all compatible
linear maps. It never exchanges the order of A_m and B_j, assumes an
inverse, or assumes a clean connector. P(1)=1 does not assert a nonzero
characteristic-one ring: the ring condition c>=2 remains.

By the inherited depth-block concatenation in
CrocSwap/integer-mult-bounds#4248, a k-source depth-two block yields

```text
N(c) >= k floor(c/2) + 2(c mod 2).
```

There are floor(c/2) blocks, with a two-source depth-one block if c is odd;
all blocks restore the connector, so their depths add to c. In particular
our k=9 path at c=57 gives 254 sources and our k=10 path at c=103 gives
512 sources. The balanced-closed-cycle formula in #6568 gives respectively
226 and 461 at those characteristics. These comparisons are to that
specific formula, **not** claims of the globally best known N(c). For
example the finite six-source characteristic-eight construction credited
in CrocSwap/integer-mult-bounds#6061 already dominates our k=6 block as a
characteristic threshold. That does not invalidate its sharp P(6) result:
an arbitrary depth-two block need not arise from a cube-covering walk.

The abstract floor word uses exactly c times every source and every output
operator, for c(n+2^n-1) complete calls on n sources. Any physical supplier
must still pay input access I, frame/helper work sum P_F, decoding D_W,
`c sum_j cost(B_j) + c sum_m cost(A_m)`, and every applicable inherited
restoration, storage, layout, precision, compiler and outer cost. No term
is set to zero here. There are exponentially many outputs. We supply no
physical consumer and no completed multiplication recurrence. The
(1/2+o(1)) leading coefficient for depth-at-most-two block concatenations
in CrocSwap/integer-mult-bounds#6107 is unchanged. All five selected-frontier
assumptions remain, and the selected κ=0.003125804 is unchanged.

## 4. Verification, provenance and limits

Base: `7c49fe32c55de02c2c873655c804b16e4c3fef0a`. `SOURCES.json` pins
selected-result/task provenance and the exact merged interface, Gray-growth
and bounded-depth documents. The generic runner verifies their Git blobs;
`verify.py` independently checks every live source SHA256. It rejects a
mutated copy of each source. No predecessor full scientific replay is
claimed. The task-card control was run:
`python3 -B research/universal-connector-boundary/verify.py`, yielding
`PASS_UNIVERSAL_CONNECTOR_BOUNDARY pairings=945 max_coverage=31 queries=74 leaves=182`.

Question and comparison provenance only: open #6568, head
`0c3ff8236c103c5960ef15c45b26432ad1603f8d`, file
`research/connector-balanced-walk-threshold/README.md`, blob
`1956daebfc00e0313b7a61ca08f1c57cf1fa6b27`, SHA256
`458d7b80e1a64d0fe56f2cc805162c53cb398108cbd38ecb617a136de765fb8d`.
No code or certificate from that unmerged branch is an execution dependency.
The universal proof above uses the cited classical theorem directly.

The primary checker tests all 1597 nonzero masks in the three certificates,
executes their 136798 complete calls, verifies a second characteristic for
each path, tests a repeated-vertex covering walk and dimension one, checks
the formula arithmetic through k=4096, and rejects 21 mutations. The
separately written `independent.py` imports no primary construction code;
it rebuilds the source words, executes all output calls over formal dirty
and source coefficients, preserves each arbitrary initial output, and
checks 18401 coefficients. Its 33 controls include shifted real read
boundaries and displaced dirty-cancellation reads with unchanged call
counts. See [the independent review](INDEPENDENT-REVIEW.md).
Normal and optimized Python runs passed. The checks are finite verification;
they are not kernel formalization, human review, or a proof of arbitrary
balanced-path existence. No present-literature completeness claim is made.

Prepared for and contributed by @CubeJerry, with substantial OpenAI Codex
assistance for reasoning, discovery, implementation, and separate AI review.
Credit Nick Petalas for #6568's question and balanced-cycle comparison and
#4231/#4248's interface and concatenation; apoursh (Armin Pourshafeie) for
#6071's open-walk split and growth construction; JosieElliston for #6107's
depth cap and #6061's stronger finite connector blocks; and the earlier
Ross Richardson (#934/#943) and Riquelme Soares lineage credited in these
packages. The classical balanced Gray-code result is Bhat--Savage's, with
its earlier history as recorded there. Apache-2.0, as in this repository.

## Open next questions

1. **Which remaining residue classes attain the lower endpoint?** Prove a
   max-count-balanced Hamilton path theorem or find a dimension where P(k)
   is the upper endpoint. This would finish the threshold question, but
   cannot improve on C(k) by more than one. First test a specifically chosen
   unresolved composite dimension; blocker: cyclic balance does not supply
   the needed open-path endpoint/transition distribution.
2. **Can a physical supplier benefit from these thresholds?** Name an actual
   caller and charge the full bill above, including exponentially many
   outputs. First compare its complete optimistic budget to the current
   binding supplier. Blocker: no such consumer is exhibited here. This is
   the gate before expanding this mechanism into more construction rounds.
The separate concurrent round-offset construction establishes the unrestricted
leading coefficient one using higher-depth blocks. It does not change the
sharp depth-at-most-two ceiling or the open-walk thresholds proved here;
these finite certificates and threshold statements have no dependency on
that construction.
