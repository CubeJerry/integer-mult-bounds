# Root review of the unitary normalizer entropy theorem

**Accepted in the explicit unitary model. No new kappa.** The theorem applies to independently specified arbitrary N banks, with clean restored ancillary fields, sublinear ordinary port-mixing entropy allowance, and no productive helper subtraction. It does not constrain arbitrary nonunitary arithmetic or the changed caller now under construction.

Reviewed author proof SHA256: `e35f396d7ceea64cde50fe03351609c9fb54ed3e073721ebf2edcc30ca6cd523`. Author manifest SHA256: `e2bb67b0e6cafb63980c93d07a842c73bbfd80a65d210ce88343f395d3855412`. Worker C developed the proof after root proposed the entropy question. Root supplied the cap-free concavity strengthening. This is a critical proof review and separately implemented source/arithmetic verification, not a claim that the shared idea was independently rediscovered.

## Universal proof review

The potential must be evaluated on the complete unitary matrix, including columns corresponding to hypothetical nonzero ancillary inputs. With one field dimension K, define Phi as the total entrywise Shannon entropy divided by K. Each row is normalized because the complete intermediate map is unitary. Coordinate monomials preserve this potential.

The group lemma is correct in both directions. For a fixed column and a row group B of size m, the group's probability mass p is preserved. Its entropy is `-p log p + p H(conditional probabilities)`. Only the conditional term changes, by at most `p log m`. Summing columns gives total mass m because all intermediate rows have norm one. Summing groups and dividing by K gives the claimed bound. No monotonicity of entropy is presumed: inverse gates can decrease it.

A p-port unitary has K groups of size p, costing at most p log2 p potential. A rank-r tensor Gaussian on one field has K/2^(rV) groups of size2^(rV), costing at most rV. These statements are unchanged by arbitrary unitary coordinate monomials around a gate. They also hold when the total number of fields or ambient dimension varies with V. Ordinary coordinate permutations have zero potential cost, but repeated port mixing is explicitly counted.

For the actual source, each target row has four input-port blocks; in each block the two distinct nonzero binary normals give four translations per column. The whole-bank scalar coefficient is applied once. Hence each row has4^(V+1) equally weighted entries and entropy2V+2. Extra ambient axes are spectators. This is a tensor-product proof from source-bound facts, not extrapolation from small widths.

Correct main behavior and clean ancillary restoration force the first block column of the final unitary to be `(N^direct_sum_b,0)`. Because that upper block is already a square unitary, orthogonality forces the other upper block to vanish. The final operator is therefore block diagonal with a unitary ancillary block. Its additional entropy cannot lower the main contribution. This establishes the finite inequality

    V sum r + C_port(V) >= 224b(V+1).

The assumption C_port=o(V) then gives liminf rank mass at least224b. Since rank mass is an integer, it is at least224b eventually; no fixed profile or uniform bound on the number of calls is needed. For0<t<1, subadditivity gives `sum r^t >= (sum r)^t`. Therefore the cap-free liminf moment is at least `(224b)^t`. The proof takes a bound on each complete sum, rather than exchanging a limit with an unbounded sum. An optional fixed rank cap yields the stronger linear refinement. Neither statement subtracts any helper target credit.

The rank-mass sharpness control is sound in the relaxed circuit model:112 rank-one calls for Q,28 actual four-port unitary factors for R0, and112 rank-one inverse calls. It has mass224 and port allowance224, attaining the finite entropy inequality. This is not a claim of cheap cochart availability or a sharp concave-moment optimum.

The clean-ancilla countercontrol establishes why the ordinary restriction is essential. Its two-field matrix J is unitary despite its Gaussian-dyadic entries. Conjugating a controlled translation by J gives the displayed projector-valued involution W. Applying W, a phase, and W implements C_q on the main field and restores a zero ancillary field. Iterating over columns uses linear-in-V ordinary port work. This circuit falls outside the sublinear allowance and is consistent with the theorem; it prevents an overbroad assertion that unitarity alone forces Gaussian calls.

## Separately implemented exact checks

The accompanying root checker imports no author code. It authenticates the frozen source and geometry, reconstructs R0 from the actual integer real roots and class Gram matrices, verifies all112 four-neighbor rows, and checks all28 four-port orthogonal factors. It expands the one-column C_h inverse times C_j as exact Gaussian rational translation coefficients and checks the uniform quarter probabilities.

An independently written integer200th-power bisection computes interval bounds for x^(199/200). The checker derives the twelve-stage source allowance directly from W_6 and the actual minimal source profile, rather than reading the author's budget output. It proves that218.0202223577... exceeds75.7857962575... for one bank and434.5318593803... exceeds151.5715925151... for two banks.

The clean-ancilla control is independently multiplied as a literal4-by4 Gaussian rational matrix. The checker verifies the full unitary and its zero lower-left block, then rejects omission of the final W. A nonunitary rescaling control explicitly violates the unitary premise. Incorrectly tensoring the whole-bank scalar coefficient has width-two row norm1/4 rather than1.

Reproduce from the session root, or substitute the committed paths after relocation:

```sh
python -B root-work/unitary-normalizer-review/check.py --author worker-c/unitary-normalizer-entropy/author --source programme/research/moonshot-005-program/results/logical-involution-112/author/output/R0-minimal/WORD.json.gz --geometry programme/research/moonshot-005-program/results/logical-involution-112/author/dependencies/GEOMETRY.json --output /tmp/entropy-review.json
```

The theorem's use is confined to ruling out that unitary/no-productive-credit implementation class for the already proved modular N repair. Nonunitary arithmetic interleaved with Gaussian calls, genuinely productive helper targets, larger ordinary-work budgets, or changed complete caller endpoints require separate arguments. The selected multiplication exponent and all global foundational assumptions remain unchanged.

Credit Worker C's proof and controls, root's original question and cap-free refinement, Worker B's R0 source, Worker A/root's physical reduction, pinned predecessors, @CubeJerry and OpenAI assistance.
