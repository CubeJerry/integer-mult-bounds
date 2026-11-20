# Actual five-source binary compilers and a gross local invoice

## Exact scope

This result compiles the five **checkpoint6** early source maps, for sources
0,45,61,62,100, onto their actual original owners. It does not compile the later
source redesign used by a prospective D1509 decoder. It supplements the accepted
full45 H263/H642 compiler with the previously unpriced source preparation and
its local inverse. All costs below are gross operation counts; no deduction of
the replaced construction and no completed supplier inequality is asserted.

## Actual owner order

For each source j, the raw route list partitions the original field coordinates
0,...,479 into its H destinations. The accepted EARLY literal gives a480-by480
matrix E_j with each output row labelled (H,x), where x is its actual owner.
The input columns already refer to the original coordinates0,...,479. Define
A_j by placing the row with label(H,x) at row x. The checker verifies every label
against the raw route list, with every original owner present exactly once.

Thus A_j is the matrix that must actually be executed in place on the original
source owners. Sorting the row labels without moving their matrix rows would
implement the wrong map. The compiler includes this row assignment in A_j; it
does not take an owner permutation for free.

## Explicit binary word

Use the polynomial basis1,t,...,t^5 for GF(64), with t^6+t+1=0. A field
coefficient a is replaced by its6-by6 multiplication matrix, whose column k is
the polynomial coefficient vector of a*t^k. The resulting binary matrix has
2880 actual owners, indexed6*x+bit. The checker constructs each coefficient by
polynomial multiplication and reduction, independently of the source author's
field arithmetic.

The deterministic elimination scans columns in increasing order. It selects the
first pivot at or below the diagonal. A required swap is performed by the three
ADDs (j,k),(k,j),(j,k), and is charged three times. It then clears that column
from every other row by a distinct-owner ADD. Elimination reaches the exact
2880-by2880 identity. Every recorded operation is an involution, so reversing the
recorded list implements A_j. Executing the list in its recorded order implements
A_j inverse. The checker independently replays both directions on the complete
symbolic binary identity, rather than on sampled inputs.

All owners are at source j when its preparation executes. The inverse is legal
at any point where all480 encoded original owners are co-located, in particular
at the Hub after a completed transport has restored those encoded owner values.
This local statement does not assert that the presently incomplete transport
supplies that global precondition. The source word needs no auxiliary owners,
initializations, clears, or added exports.

The complete words are reproducibly specified by the literal matrix, pivot rule,
and checker. Their SHA256 digests encode the elimination stream as consecutive
unsigned16 little-endian(target,source) pairs; the script regenerates and verifies
the streams without retaining large redundant operation lists.

## Exact gross cost

| Source | Binary ADDs per direction | Paid three-ADD swaps |
|---|---:|---:|
|0|2,433,642|2,213|
|45|2,412,700|2,278|
|61|2,391,802|2,406|
|62|2,353,561|2,512|
|100|2,345,849|2,475|

There are eight lanes and two directions. The five source compilers therefore
cost191,000,864 binary ADDs. The already accepted two-H forward/inverse words
cost1,509,520 binary ADDs, so these seven local components together cost
**192,510,384 binary ADDs**, plus the H642 complement's16 field exports at gap6
and96 binary INIT, MOVE, and CLEAR operations each. This is an exact inventory
for the stated components. It omits all unbuilt H,D,K,F and global return work;
it is not an end-to-end invoice and does not establish a new kappa.

Block repetition applies the same explicit word independently to each repeated
copy, with cost scaling linearly. This extension is an algebraic construction,
not an extrapolation from sampled input vectors.

## Reproduction

From the repository root:

```
python -B research/moonshot-005-program/results/bit-shared-h-s031-construction/d-aligned-full45-pair/source-compilation/author/check.py --repo . --out /tmp/s031-source-compiler-replay
```

Expected status:`PASS_ACTUAL_FIVE_SOURCE_BINARY_COMPILERS` with source total
191000864 and known-component total192510384. An independent review is required
before admission.
