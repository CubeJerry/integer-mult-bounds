# Independent adversarial review of the signed-permutation caller gate

**Reviewer:** Worker C, S013, for @CubeJerry, with OpenAI assistance.  
**Disposition:** accept the stated fixed-algebra theorem and the separately qualified ordinary source normalization. No caller is constructed and no new kappa is established.

This review was written after reading the author proofs and the actual pinned common-cubic source. The finite reconstruction below was written separately and does not import or invoke the author checkers. It ran in the cloud JavaScript runtime after the local executor became unavailable. A later parity-kernel investigation is a separate result; the inventory described as surviving *this rank gate* is not thereby claimed to survive every subsequent obstruction.

## 1. Exact materials reviewed

The repository is CubeJerry/integer-mult-bounds. The common-cubic source is at commit
`4bf5bc1f28c87fe6120bd053d8202e40b425d6fb`,
path `research/moonshot-005-program/results/complex-common-cubic-head/author/PROOF.md`,
Git blob `04bbc16a5076cb2306c3f98aa1ecf171da1d6d01`.

Author materials:

- Signed-permutation proof: `a1ac2256f8a7b3ab467c9eb22abb1c6787bf889e`.
- Ordinary lambda normalization: `92943f0fda91920931bcfe1f7cab866b39e79b91`.
- Author checker: `ce1e13f62b32e646fe2a4ac0f9185ede6cc26e77`.
- Author receipt: `58c620fca4f7608ddfef7923b5b00efc1fffd9f8`.
- Tensor-separation proof: `fa2e3d3c1e0a112bd3306213021e23f861cdb799`.
- Tensor checker: `c638ba381ec3e624e80a2f4a4fd969cb6b5e1a7e`.
- Tensor receipt: `04dc60df2eaac7647f8c6b9256308b0dd09a41cb`.

The canonical literal control remains pinned by that source to blob
`8cddb0aff69b91ae648422f2cd5e77a12883ebe7`.
This review checks the common-cubic source interface as published; it does not reopen every earlier compiler, precision, or native-source theorem.

## 2. Universal proof audit

### Faithfulness at all sufficiently large widths

The tensor-separation proof is valid. For finitely many pairwise nonproportional unitary matrices, the normalized Gram entries have strict off-diagonal modulus below one. The displayed diagonal-dominance argument proves eventual tensor independence even for scalar coefficients that depend on the width. Exact scalar cocycles must be retained in a projective version.

For the concrete group, every element fixes the same zero-frequency vector. Consequently a relation at width V+1 contracts to a relation with exactly the same coefficients at width V. A nonzero width-six Gram determinant therefore implies independence at every V at least six.

I reconstructed the width-six Gram matrix independently and obtained determinant **32 modulo 137**, using i=37 modulo 137. This differs from both the author's prime101 witness and root's reported prime109 witness. The rank is192. Since 37 squared is -1 modulo137, this is a legitimate Gaussian-integer determinant specialization. It proves a nonzero characteristic-zero determinant; it is not an empirical extrapolation from widths one through six.

The finite-dimensional ordinary algebra inverse argument is also correct. An actually invertible element of its faithful matrix image has its inverse in the image by its minimal polynomial. Thus invertible ordinary boundary encodings remain invertible after either abstract representation. This does not supply a physical implementation of an arbitrary mathematical inverse; the obstruction only needs its existence.

### The two representation maps

The four translations form the kernel of the phase-to-three-sign map. Instead of assuming the author's closed formula, the independent checker constructs all eight cosets as products of Qa,Qb,Qc modulo the actual four translations. It obtains each phase element's unique sign word from these cosets, derives the permutation action by conjugating the three generators, and only then checks agreement with the published formula.

The resulting unsigned and signed permutation matrices obey both multiplication laws on all192 squared ordered pairs. They coincide on all24 ordinary elements and therefore on their entire complex linear span. The difference rank is the number of changed signs.

I independently checked the physical rank census using support counts of the actual four-by-four Fourier-conjugated monomial operators. Thus the classification does not merely reuse the author's formula for the binary Gaussian rank. The census is exactly:

| Physical Gaussian rank | Representation difference rank | Count |
| --- | --- | --- |
|0|0|24|
|1|1|72|
|2|2|72|
|2|3|24|

The last class is the central-Z ordinary double coset. Difference rank is an algebraic potential, not a physical MOVE tariff.

### Native half and endpoint inequality

For any compatible matrices, the difference of the two representations of a product splits into two terms. Matrix-rank subadditivity proves D(MN) at most D(M)+D(N). Left and right multiplication by an invertible ordinary matrix preserve D exactly.

For the actual common-cubic half, let X=B1-B0. It has rank one. When the off-diagonal power is zero its difference vanishes. Otherwise the identity

`B1^2-B0^2 = B0 X + X B1`

holds without requiring B0 and B1 to commute. The two invertible block-triangular eliminations in the author proof reduce the native difference to diag(X,X). This proves exact native potential two for every baseline orientation and coupling sign. My checker reconstructs and checks all eight reductions over the integers, then verifies a rank-two modular witness.

An in-place Gaussian query and a distinct-bank Gaussian shear both have difference rank d(g). In particular, the latter is not incorrectly treated as a free query merely because its determinant is one. Independent endpoint jobs give a block-diagonal difference, whose ranks add. The stated inequality and both closed inventories follow.

The proof correctly permits arbitrary invertible ordinary matrix mixing inside C[H24]. It does not prove a physical obstruction for quadratic coordinate phases outside H24, column-dependent operators, a changing unbounded one-column family, limiting approximate identities, additional source types, or discarded inputs. Those exclusions are essential.

## 3. Ordinary lambda normalization audit

Let T=Q squared and let alpha=(1+i)/2, beta=(1-i)/2. The algebraic identities lambda=alpha I+beta T, lambda squared=T, and lambda inverse=beta I+alpha T are exact because T squared=I. The normalized S=lambda Q inverse is an involution, and Q=lambda S.

The independent checker works in the abstract commuting phase group with exact Gaussian-dyadic coefficients. It checks all16 entries of the four-input source after the stated pre- and post-normalizations. This is a collective-operator calculation, so it proves the identity at every tensor width without replacing a collective sum by a tensor power of a one-column sum.

The five in-place scalar operations produce exactly

`(u,v) -> (alpha u+beta v, beta u+alpha v)`.

They require three scalar additions and two scalar multiplications per pair, no helper field and no erasure. The two inverse scale constants are nonzero fixed Gaussian dyadics. The normalization uses eight lambda services for the four-role source, four per half. Thus six D scalar additions and four D scalar multiplications per half are the correct counts when D is the number of scalar coordinates in a field. Pairing/unpairing layout operations and the final two swap gauges remain paid ordinary work.

The local coefficient bound is finite and independent of precision. This supports the claimed fixed-circuit normalization, but does not discharge the full ordinary tape/bit compiler. I found no basis for deleting those inherited costs, and the author does not delete them.

A negative control compares the actual two-column eigenvalue i squared=-1 with the false collective expansion alpha+beta=1. This demonstrates why the admitted collective lambda service is different from pretending the tensor Gaussian itself is an ordinary linear combination.

## 4. Optimistic changed-query arithmetic

Independently computed integer200th-root brackets at scale10^25 place

`3*9^(199/200) - 2 - 2*7^(199/200) - 8^(199/200) - 2^(199/200)`

between

`9302175408765793434332219 / 10^25`

and

`9302175408765793434332226 / 10^25`.

The raw Gaussian margin is positive. Its inventory includes one actual native half, one rank-seven idle, and both the rank-two and rank-one queries. It is a conditional cost calculation for a missing circuit, not a supplier or an accepted multiplication bound. The distinction remains necessary even if a later theorem excludes this inventory.

## 5. Reproduction and disposition

Run `node check.mjs` in this review directory. No author module is imported. The checker independently reconstructs the finite group, cosets, actual Fourier support ranks, both representation homomorphisms, native triangular reductions, width-six Gram determinant, lambda normalization, and exact optimistic price bracket.

The finite checks authenticate this concrete source and these concrete representations. The universal statements follow from the proofs audited above: tensor-independence propagation, representation linearity, matrix-rank identities, and the exact source normalizations.

**Accepted within the explicit scope.** The closed three-half inventories should be recorded as contradicted under the fixed G192/H24 interface. The changed-query inventory remains only a candidate relative to this rank gate. The larger-ordinary and changed-source possibilities remain separate proof obligations. No new kappa.
