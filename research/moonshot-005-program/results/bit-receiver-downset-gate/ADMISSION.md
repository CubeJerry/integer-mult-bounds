# Receiver-downset obstruction for canonical class extensions

**Proved within the stated all-history code and monotone route contract.
No new kappa.** Over every characteristic-two field and width V, a complete
source whose actual historical X code lies in
W_c tensor F^V, W_c=U+span(K_i), i in class c, needs q>=14 packets.
This excludes all15 previously proposed rank16 canonical candidates.

More generally, a scalar W containing U and contained in U+C, with added
quotient dimension h, needs q>=16-2^h: 15,14,12,8,0 for h=0,1,2,3,4.
The same holds for a fixed scalar code tensored across V. Arbitrary non-tensor
block codes are not assigned an18V dimension bound by this argument.

[Proof and certificate](author/PROOF.md) use the exact native pin
51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78,
the admitted class/coset geometry and arbitrary-Y historical normalization.
In the outside-class receiver downset W has zero local intersection; actual
first entries carry at most qV unique W projections, while14V independent
class endpoint rows are required. The scalar hierarchy counts nonzero binary
quotient labels in a field-linear h-space. No local codeword is assumed free.

[Worker C review](review-c/REVIEW.md) and [lead review](review-root/REVIEW.md)
are separate proof/source checks. Reproduce from repository root:

```bash
python3 -I -B research/moonshot-005-program/results/bit-receiver-downset-gate/review-c/check.py --native research/paired-query-only-bit/retained/inputs/BIT-NATIVE-WORD.json.gz --output /tmp/downset-c.json
python3 -I -B research/moonshot-005-program/results/bit-receiver-downset-gate/review-root/check_geometry.py --native research/paired-query-only-bit/retained/inputs/BIT-NATIVE-WORD.json.gz --partition research/moonshot-005-program/results/bit-fifteen-class-target/author/RESULT.json --output /tmp/downset-root.json
```

Expected lead status: PASS_INDEPENDENT_RECEIVER_AND_CUT_GEOMETRY. Receipts
include all111 restrictions, all67 quotient subspaces and nonzero-shortening
controls. The original rank16 family is closed; richer codes remain open.
The separate operator-shortening theorem subsequently excludes q8 throughout
the full fixed C+U tensor code, but not q9/10 or arbitrary codes.

Credit @CubeJerry, retained BIT/E8, class/coset and history authors, Worker A,
Worker C and lead; substantial OpenAI assistance. Baseline
4b7eff5a9d0abee84824a74c67133ee7546ecfff. All five foundations retained.
