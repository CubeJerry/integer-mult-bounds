# Independent A review of C's radix and succinct executor

Reviewer: E002 Route A (a separate agent from the author). This is an
AI-assisted written audit and isolated finite replay, not human refereeing
or a full fixed-tape implementation. Source pin and predecessor scope are
those recorded in the reviewed notes.

Reviewed SHA-256 snapshots:

- `small-radix-batching.md`:
  `a2501e3f22581e148099dc8082d22c0ae34126735dd5e0fd118243b7b71b8381`
- `succinct-cyclic-executor.md`:
  `6803d8d949397b4ee6b2304098ea2fb82e997df87396a6f6c96af72f2bb3c14b`
- `verify_succinct_cyclic.py`:
  `859c4d782c252dfa3d1ecae7d942449c6704c8cbf0cddf3bd8d11ee37b47a963`

## 1. Small compatible prime

Accepted R1--R2. The p-adic valuation formula shows that the central
binomial coefficient divides lcm(1,...,N): each floor-difference term is
zero or one, and there are at most floor(log_p N) terms. The elementary
central-binomial lower bound and prime exponent upper bound then give
log2 product_(p<=N) p >= [N-log2(N+1)]/log2 N. For the chosen power of two
N this exceeds B, so the product cannot divide the complete compatibility
integer. Trial division and remainder tests through polynomially bounded
N have actual polynomial bit cost. This does not assume a prime gap theorem
or factorization oracle.

The scope of the compatibility list matters. It contains address-map
numerators, denominators, pivots and inverses of polynomial count and bit
height. It is not asserted that every coefficient of an expanded scalar
module has polynomial size. That narrower list suffices for specialization
of rational address maps modulo b^f, independently of the scalar field.

## 2. Multidigit batch block

Accepted R3--R6 with the stated concatenated-row executor interface.
The last padded group has volume inflation qW/A<=1+eta, and each independent
row has volume at most (1+eta)V/W. Consuming ell leading digits changes the
base width but leaves f<=e/m and the reserve restoration invariant intact.
Both leading chunks and remainder digits are paid directly afterwards.
The recursion coefficient is therefore (1+eta)sigma/W+2a.

I requested one correction before acceptance: a variable radix b must not
retain the source's fixed-b O(V) constant or b separate physical tapes.
The reviewed snapshot now explicitly serializes digit classes and charges
poly(b) per digit operation in C_m and the base-range bill. Because the new
b is polynomial in m, this retains the intended polynomial-m coefficient.

A concrete fixed-tape batch regrouping can use whole-row stable sorting:
pad the leading range A to qW, write r=Wg+w, then stable-sort the qW blocks
by the O(log W)-bit key w. Stability retains increasing g inside each w.
This converts [q][W] to [W][q] with polynomial(log W) work per payload
symbol; reverse regrouping sorts by r. Every padded block is charged and
removed by known index. This is the SR1 interface independently proved in
`SUCCINCT-ROW-EXECUTION.md`. It gives an implementation of the declared
concatenated representation without W tapes or W full-array scans.

The note does not establish the whole multiplier. Scalar execution,
spectral selection, precision and common-cap assembly remain separate.

## 3. Masked-translation factor decomposition

Accepted C1--C5 for the specified power-of-two addition budgets. I reread
the predecessor cyclic factorization and checked the following points.

- At a sum, the total-grade-t source is indexed by (a,u,v), so the left
  contribution increments a and uses A_a; the right retains a and uses
  B_(t-a). These are input grades. Using output grades would be incorrect.
- At a product, the current stage selects one child, never the product of
  two child matrices in the same affine stage. Consequently expanding one
  stage creates root-to-terminal paths, not exponentially many choices from
  disjoint subtrees. Each sum coordinate is visited at most once per path.
- Constant scaling affects exactly its designated local stage; padding
  contributes a guarded identity terminal. Zero factors are permitted.
- A path changes each sum coordinate by zero or one modulo its budget;
  its remaining scalar depends on input-row guards. Thus it is precisely
  an input diagonal followed by a fixed coordinate translation.
- The complete number of leaf and padding terminals is at most kS+S.
  The copied formula's actual S, rather than a shared circuit size, is the
  relevant quantity. Uniform path evaluation uses polynomial-size data.
- Cyclic coordinate increments move blocks by sequential split/merge scans.
  Their payload cost is linear; per-row mask work is polynomial in
  S,k,log D. The complete module row is arbitrary and occupied throughout.
- Summing terms uses one retained original, one reusable temporary and one
  output accumulator. This pays internal zero initialization without
  pretending those zero rows are extra independent parent inputs.

The decomposition of Aj does not execute spatial Qj once per path.
It applies Aj to the streams already routed by the source shared-pencil
construction, so it changes the scalar-row bill while preserving the
recursive-query invoice. This distinction is necessary for the claimed
component to be useful.

## 4. Isolated finite replay

Copied the inspected checker to `replay-cyclic/verify_succinct_cyclic.py`
and executed it there. Exit code zero. It checked 13 formulas, 35 complete
formal affine factors, 441 path descriptions, 9,585 path/row evaluations,
and 560 full cyclic products over F4, with maximum row dimension 64.
It rejected 24 omitted-rotation and 10 wrong-grade controls. The exact
receipt and execution output are retained in `replay-cyclic/`.

These tests corroborate finite identities and distinguish the grade and
translation failure modes. They do not prove the all-size cost bound,
execute physical tape programs or certify a multiplication theorem.

## 5. Remaining review gate

Composition must still show that recursive spatial calls can be scheduled
on the concatenated layout without reintroducing a width-many scan cost.
The natural implementation groups module rows as an ordinary prefix for
identical address operations. Source interchange accepts arbitrary prefix
ranges; endpoint/label types and query types number only polynomially
many. That grouping must appear explicitly in the complete compiler.
Expanded transition-list interpretation is not an eligible replacement
for the succinct structured executor.
