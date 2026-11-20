# Independent review: shared-node Hermite3 cannot align the native fibres

**Accepted within the stated source and target contract.** The frozen shared-node Hermite3 information systems at donors0 and61 cannot satisfy the 33 native H263 inverse-fibre requirements after independent invertible binary-linear changes of their input banks. This remains true for arbitrary positive repetitions, finite extensions of GF64, Frobenius-conjugate copies and arbitrary binary-linear mixing between those copies. In particular, it covers the stated Hermite3+Hermite12 source at bank3840.

This is an obstruction to this fixed quotient information. It is not an obstruction to arbitrary nonlinear bank bijections, changed off-H quotients, feedback families, changed nodes, larger informative cuts, inter-source coupling or changed targets. It certifies no new kappa.

## Frozen inputs and independent replay

The author manifest is

```text
8da45eb4c1e098747f9a2ab4d6ddfb1de56407955123ffe08f366577b4a0322c
```

The final author proof, implementation, source pins, result and compact witnesses are hash-bound by `SOURCE-PINS.json`. The review additionally binds the literal native layout, original-owner routes, exact lattice basis, shared-node table, the prior independent bilinear review, and the already reviewed tight-cut theorem. The author manifest's own listed hashes are checked on every replay.

Reproduce from the repository root:

```sh
OPENBLAS_NUM_THREADS=1 python -I -B research/moonshot-005-program/results/bit-global-hermite-fibre-obstruction/review-c/check.py --repo . --out FRESH
```

Expected output:

```text
PASS_INDEPENDENT_HERMITE3_BINARY_INTERTWINER_OBSTRUCTION 3024 297 6 33 264
```

The review imports no author or predecessor code. It reuses, by copying, the arithmetic and exact root-coordinate methods of this reviewer's previously frozen independent cycle checker. Multiplication uses carryless polynomial convolution modulo X^6+X+1. Rank uses forward elimination with the last eligible pivot row; nullspaces use back substitution. None of the author's compressed core bases, relation bases, equation rows or selected minors is used to construct the review matrices.

## Native binding and necessary alignment

The independently reconstructed native geometry gives H263={0,61,62}, global node49 and exactly33 native receivers perpendicular to H263. Receiver80 is not among them, and neither compared donor is donor10. Thus the identity target blocks used by the reviewed tight-cut argument are the actual original-coordinate S028 blocks; the bilinear parameter identity is not substituted for the target.

Each donor star has 28 distinct shared nodes. For every one of these33 receiver views, exactly16 actual H labels are visible, including H263. The off-H node set has15 distinct elements. At donors0 and61 the two off-node sets intersect in9 nodes. The checker determines these sets from the literal native chart labels and polar adjacency.

The complete original-owner route stream gives30 native X slots at each of donors0,61,62 through H263. Expanding each slot into its eight actual lanes gives720 original X fields and no Y fields at the centre. There are45 native D exits with16 fields each, and every relevant receiver sees15 exits, hence240 fields. Original owner equals source on each counted early route. This is the actual fully early H263 cut.

The retained tight-cut proof applies because the source observations are separated, the target contributions are identities, and no additional informative path is granted. Fixing the other sources and the fifteen off-H observations leaves one full quotient-width uncertainty fibre at each compared donor. Their independent variations must be transmitted through one quotient-width shared H cut. The finite additive sumset argument forces equality of the whole original-input coset directions. For the linear sources after binary-linear bank gauges, those directions are additive subspaces. Arbitrary H and downstream functions do not relax this necessary equality, and bijective output relabelings do not change the source partitions.

## Literal polynomial kernels

For width k, the source domain is the coefficient space of polynomials of degree less than16k. Its plane observation consists of the first k Hasse derivatives at that plane's node. At15 distinct off-H nodes with monic product g(z), vanishing of those observations is equivalent to divisibility by g(z)^k. The whole inverse fibre is therefore

```text
L = g(z)^k · {polynomials of degree less than k}.
```

The checker independently multiplies the15 linear factors, constructs each shifted-power basis, and evaluates its Hasse observations directly from the binary binomial-coefficient criterion. Every off-H matrix has rank15k, every proposed kernel basis has rank k and is annihilated by that matrix, and its central-node observation has rank k. Thus the full16-node source view is also invertible. These tests cover tensor scalar, tensor width3, Hermite2 and Hermite3 controls, and the literal Hermite12 decomposition.

For Hermite3, each donor's33 three-dimensional fibres span36 dimensions. The two spans are equal, as stated in the author proof. At each receiver, the first two fibres have union rank6 and all three donor fibres have union rank9. The ungauged directions therefore differ. The stronger gauge obstruction below does not rely on this difference alone.

## Full compatibility equations in the original48 coordinates

The independent construction deliberately avoids the author's36-coordinate compression. Order the33 receivers by their actual native indices, and let A_i and B_i be the respective48 by3 polynomial coefficient bases at donors0 and61. Concatenate the source bases as

```text
A = [A_1 ... A_33],  shape48 by99, rank36.
```

Solve its full relation space directly, obtaining R of shape99 by63 with AR=0. A field-linear map from the source span taking each fibre into its corresponding target fibre has matrices M_i of shape3 by3 satisfying

```text
T A_i = B_i M_i.
```

Such prescribed images extend to a linear map precisely when every source relation is respected:

```text
[B_1 M_1 ... B_33 M_33] R = 0.
```

This condition is necessary and sufficient on the source span. It makes no invertibility, scalar, diagonal or common-matrix assumption on the33 matrices M_i.

For each s from0 through5, replace B_i by its coefficientwise 2^s power. Expanding the48 by63 relation matrix yields an independent3024 by297 homogeneous system. All six have rank297. The author's equivalent compression gives2268 rows; the larger review system uses the original polynomial coordinates and reaches the same full column rank without assuming any supplied core coordinate map. It follows that every M_i vanishes, so every corresponding linear intertwiner vanishes on the entire nonzero source span.

The review emits its own selected297-row square minor for each system, verifies each has rank297 and records its coefficient hash. `MINORS.json` contains those row indices and hashes; `FIBRES-AND-RELATIONS.json.gz` contains the independently generated polynomial fibre and relation bases. Duplicating the last row of one selected minor drops its rank to296, providing an explicit negative control.

Positive controls distinguish this obstruction from a faulty universal rejection. The scalar tensor system has nullity1 and a rank6 core map; tensor width3 has nullity9 and a rank18 core map; Hermite2 has nullity4 and a rank12 core map. The checker constructs actual coefficient solutions, tests every relation and verifies the full displayed core rank. These are local transport controls only.

## Why six field-linear systems exclude binary-linear bank gauges

Every binary-linear map on GF64^48 has a unique linearized-polynomial expression

```text
T(x) = sum from s=0 to5 of T_s x^(2^s),
```

with GF64 matrices T_s. Suppose T maps each source fibre L_i into the corresponding target fibre M_i. Fix x in L_i. Since L_i is a GF64 subspace, lambda*x belongs to it for every lambda in GF64. Project T(lambda*x) to the quotient by M_i. The resulting vector polynomial in lambda has degree at most32 and vanishes at all64 field elements. Each coefficient is therefore zero. Hence each T_s separately maps L_i^(2^s) into M_i.

Applying inverse Frobenius to this inclusion yields a field-linear map from L_i into one of the six Frobenius-conjugate target diagrams tested above. Every such map vanishes on the source span. Thus T_s annihilates its conjugate source span for every s, and T annihilates the original36-dimensional source span. T cannot be invertible.

If independently invertible binary-linear source gauges aligned the two original-input fibre arrangements, their composition would be an invertible transport between the ungauged arrangements, with direction depending only on the chosen coordinate convention. The tested direction is impossible, and an invertible transport in the reverse direction would have an invertible inverse. This proves the claimed obstruction to independent gauges, without assuming them equal or block diagonal.

## Copies, extensions and the literal Hermite12 reduction

For direct sums, write a candidate binary-linear bank map in blocks between copies. Input vectors supported in one source copy and projection onto one target copy show that every block must transport the corresponding pair of fibre diagrams. The preceding proof forces each block to vanish on its source core. The full map therefore vanishes on a direct sum of nonzero cores and cannot be invertible. This allows unrestricted mixing between the copies.

The same argument applies to Frobenius-conjugate copies: conjugating a hypothetical transport by the corresponding coefficientwise Frobenius bijections reduces it to a binary-linear transport between the original diagrams. Over a finite extension K of GF64, fixed GF64 coefficient matrices act as repeated copies after choosing a GF64 basis of K. The arbitrary binary-linear map may mix these copies, which is already covered. This justifies the full finite-extension claim rather than merely extension of the rank computation.

The Hermite12 reduction is exact in one fixed polynomial coordinate permutation. Write an exponent ell as4q+r, where0<=q<3 and0<=r<4. Then

```text
z^ell g(z)^12 = z^r · [z^q g(z)^3]^4.
```

The four residues r modulo4 have disjoint coefficient coordinates. Each residue block is the Frobenius-square image of the Hermite3 kernel basis. The checker tests all four diagonal blocks and all off-residue zero blocks for both donors at all33 receivers:264 diagonal identities in total. This is a simultaneous diagram decomposition, independent of the receiver.

Consequently sixteen copies of Hermite3 plus Hermite12 give a3840-coordinate bank and240-dimensional inverse fibres, with80 Hermite3 or Frobenius-conjugate components. The arbitrary-copy argument excludes all binary-linear bank recodings mixing these components. Altering only the central H263 observation leaves the fifteen off-H kernels unchanged and cannot repair their incompatibility while the source cuts remain tight.

## Scope of admission

The final author proof's tight-cut use, complete relation-system equivalence, Frobenius decomposition, repetition argument, finite-extension argument and Hermite12 reduction are accepted. The exact finite statements are independently reproduced in a different coordinate construction and with independent arithmetic.

No step converts an arbitrary nonlinear bank bijection into a binary-linear one. No inference is made about the separate feedback construction, a redesign of off-H quotient information, other node assignments, an enlarged informative cut, early inter-source information exchange, arbitrary native fitting targets or a general lower bound for every source architecture. The result excludes this fixed source family under its explicit gauges and routing/target contract. All remaining multiplication-programme and foundational obligations remain open.
