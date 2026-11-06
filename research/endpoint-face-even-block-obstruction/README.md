# An endpoint-face obstruction to a third minimal query fragment

Three ordered adjacent query pairs cannot all have rank-four common banks
while retaining the left/right endpoint-face architecture of the two-fragment
root in CrocSwap/integer-mult-bounds#6726. At least one bank must have rank
five or higher, or the architecture must change. **No new κ.**

The stronger theorem in [PROOF.md](PROOF.md) applies to arbitrary positive
even group sizes m: an ordered collection of pairwise commuting banks of
minimum rank m+2 contains at most one left-face group and at most one
right-face group, in that order. It holds over every field of characteristic
different from two, in every even ambient dimension and for every nonzero
endpoint parameter. Independent adversarial review further extends the
one-per-face bound to all positive group sizes; the order conclusion holds
for all sizes in characteristic different from two and three, including
characteristic zero. A characteristic-three odd-group support-and-commutation
counterexample explains that boundary; it is not a native caller. These are written algebraic proofs with exact checks,
not finite-search impossibility claims.

## Why this matters and what is new

The complex supplier binds the pinned selected result. Additional fragments
can earn useful independent outputs only if their native banks coexist.
CrocSwap/integer-mult-bounds#6726 explored a ten-field three-pair pilot and
found a rank-six middle pair within 20 tested placements. That does not prove
a universal barrier. This package proves the precise lower obstruction for
the existing two endpoint faces, without a dimension, coefficient-height,
placement-search or endpoint-parameter bound. It does **not** promote the
pilot's observed rank-six cost to a theorem.

The endpoint chart and the rank-three, one-dimensional predecessor come from
Ali Romman's CrocSwap/integer-mult-bounds#6398. The new mechanism first treats arbitrary even-dimensional common-kernel
projections: their forced matrices have zero triple products but at least one
nonzero double product, so they cannot commute. An independent review then
uses the trace of the rank-one product to include odd dimensions. The proof covers the exceptional parameters ±1 explicitly.
The coupled three-stage rank-budget work in CrocSwap/integer-mult-bounds#6717
is relevant context, not a dependency on its proposed supplier.

## Exact scope

The model is the canonical scalar shortest-query word. Endpoint banks are
distinct commuting rank-two idempotents. Each group bank commutes with the
endpoints, supports every group query on both sides, and uses exactly one
endpoint face ab or ac plus its common-kernel subspace. Groups are ordered
and do not interleave. Minimum rank m+2 is a proved necessary floor in this
class and an explicit hypothesis for the noncommutation theorem.

The result does not exclude rank-five pair banks, the other endpoint faces,
equal or larger endpoint banks, interleaved groups, or genuinely coupled
ports. The original even-size theorem has the wider characteristic range;
the extension and its characteristic-three order exception are explicit in
PROOF.md section 7. It does not construct a supplier, verify an arbitrary caller,
discharge the five inherited framework assumptions, or change the selected
certificate. Prefix commutation is unnecessary for the obstruction; the
source positive control nevertheless checks every actual full-stage prefix.

The original optimistic third-fragment plan assumed another pair at the same
rank-four common-bank cost as the existing two. The theorem rules out this
necessary algebraic premise before a complete new invoice exists. Higher-rank
or changed-face proposals still need complete productive/paid, physical,
ownership, restoration, native and outer accounting.

## Reproduction and executed checks

From the repository root, with Python 3.12 and only the standard library:

```sh
python3 -B research/endpoint-face-even-block-obstruction/verify.py
```

Expected status: `PASS_ENDPOINT_FACE_EVEN_BLOCK_OBSTRUCTION`; the full output
is [RESULT.json](RESULT.json). The verifier completes in about two seconds
on the author environment, Python 3.12.14.

Executed normal and optimized runs check:

- Every polynomial coefficient of the even-block inverse identity at sizes
  2,4,...,16, without sampling its scalar parameter.
- 108 exact pairs of individually idempotent but noncommuting projections,
  at group sizes 2,4,6 and parameters -3,-1,-1/2,1/2,1,3, including reversed
  left/right order. At ±1 exactly one double product vanishes; one-sided
  zero-product checks are insufficient.
- The exact eight-field source queries: independent rank-one factorization,
  canonical similarity reconstruction, all stage support and prefix
  commutators, central endpoint -I, endpoint parameter -1, and both forced
  rank-two common-kernel projections with zero cross-pairings.
- Rejection of a deleted query, a deleted bank coordinate, an odd block
  substituted into the even inverse identity, and an inverse-sign error.

The independent implementation in [review_endpoint.py](review_endpoint.py)
imports no author code. Its finite-field Gaussian elimination checks 448
Gram cases, 550 same-face and 550 reversed-face products; a second rational
normalization checks all nine source queries. Six additional failure/scope
controls include an actual mutated source file and the characteristic-three
reversed-order witness, whose native prefix checks fail at sites 1 and 2.
Both normal and optimized runs passed with identical receipts; see
[INDEPENDENT.txt](INDEPENDENT.txt) and the mathematical [review](REVIEW.md).

These finite checks support the derivation and source applicability. The
written proof supplies the unbounded quantifiers. Neither run is formal-kernel
verification or independent human scientific acceptance. Registered replay:

```sh
python3 -B scripts/research_package.py --package research/endpoint-face-even-block-obstruction
```

## Provenance and reproducibility boundary

Base: `7c49fe32c55de02c2c873655c804b16e4c3fef0a`. Its selected κ is
0.003125804; pending proposals are not treated as accepted replacements.
[SOURCES.json](SOURCES.json) pins the base catalogue and selected record,
plus exact predecessor paths, heads and available content hashes.

The positive fixture is the unmodified `ROOT.json` from
`research/p104-paid-idle-fragmentation/frozen/two-fragment/` at the
CrocSwap/integer-mult-bounds#6726 source head
`435bbe91fb28cb1d7a569ca70c6c4e9eb302d486` in `zxv/integer-mult-bounds`.
Its Git blob is `d153188cc7bdc96d80f3f3bdae8e88865ef1d437`; its SHA256 is
`b31151c36e39c9267bcc81ec3e13d9d29df9d0c0b404830a9cfb01e21a5b8fc2`.
The verifier authenticates these retained bytes locally. No unmerged Git
object, network retrieval or predecessor executable is needed to replay.
Only the root algebra is checked here; the predecessor's larger physical
caller, price, native and compiler packages are not replayed.

The theorem is stated directly in canonical coordinates; the inherited
normal form is documented in
`research/five-call-projector-rigidity/PROOF.md` at the base. The source
application does not merely assume that result: its simultaneous similarity
is reconstructed and checked against every retained query matrix.

## Open next questions

- Can three ordered pair banks have ranks 4,5,4 on these same endpoint faces?
  The first step is to add one excess common-kernel direction and solve its
  projector equations jointly with the actual prefix commutators. This could
  distinguish a genuine rank-five escape from the predecessor's rank-six
  pilot, but a legal root and complete invoice remain missing.
- Can a different endpoint face or interleaving produce a useful third
  fragment? First derive its forced row/column pairings; do not reuse the
  all-ones cross matrix outside the ordered-face assumptions. Native
  chronology, physical unit retirement and complete accounting remain open.

The structured versions and their blockers are in [TASK.json](TASK.json).

## Attribution

Prepared for @CubeJerry with substantial OpenAI Codex assistance. The new
proof and exact verifier were developed in a coordinated research session;
a separate review agent independently reconstructed the proof, derived the
all-size extension, and supplied a distinct exact implementation.
Ali Romman retains credit for the endpoint chart and one-dimensional
predecessor; thu-nmrc, zxv and all retained predecessors retain credit for
the actual common-idle root, paid-idle construction and its provenance.
See the unmodified [source notice](inputs/NOTICE). New material and the
retained source are Apache-2.0. No selected-frontier update is requested.
