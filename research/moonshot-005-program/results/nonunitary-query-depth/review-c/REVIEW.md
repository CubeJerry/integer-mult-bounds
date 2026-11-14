# Independent review: nonunitary paid-layer support bound

**Accepted for the exact linear, sublinear-ordinary-branching model stated by the author. No new κ.** The reviewed author package is `root-work/nonunitary-query-depth`, manifest `89fb25c61c3a17c48900f2e7d05f719c502b6f37cdc0525eb13fb5918bbb6c09`, proof `bd121f3c3e864ee65fd545346dd70458bebf0573d4080ad811ccb145ea590f55`.

## Universal argument and scope

For any composable finite matrices A,B, a row of AB is supported in the union of at most s(A) supports of rows of B. Therefore s(AB)<=s(A)s(B), including rectangular, singular and nonunitary maps over any field. Cancellations only reduce that union. A Gaussian rank-r layer has degree2^(rV), while an additive nonself query layer retains a disjoint destination baseline and has degree1+2^(rV). Parallel grouping is valid only for the declared disjoint layer; consuming a previous query result creates a later layer.

Multiplying all factors gives the displayed logarithmic bound, with every ordinary factor's actual row degree charged in L_V. Initialization, copying and selection have degree at most one. Restricting to originally independent input columns cannot increase support, so clean or discarded zero workspace does not evade the bound. Arbitrary spatial coordinate permutations are permitted. No unitarity or bounded scalar coefficient assumption is needed.

The actual N premise gives slope2 and exact row degree2^(2V+2). Consequently one rank-one direct layer or query layer requires a linear-in-V ordinary branching allowance. The exact two-Gaussian circuit Q,R0,Q^-1 is a sharp support-depth control. The C conclusion uses its separately reviewed actual support premise and the positive good-row fraction for V>=2. The present reviewer checked the inheritance and scope of that source review; the C collision enumeration was not rerun here.

This theorem constrains layer depth and ordinary branching, not aggregate paid rank mass. In particular, a maximum support bound cannot by itself require112 paid queries per layer. The224 price consequence is correct only after separately restricting the repair to two complete112-port rank-one query banks. Productive-helper subtraction, arbitrary sparse higher-rank repairs, redesigned source interleavings or width-growing ordinary decoders are not excluded by this lemma.

## Composition with the actual three-half endpoint

The independently reviewed `worker-a/three-half-endpoint-ranks` package gives the joint endpoint bound4·2^(23V) for V>=2. Its review is at `worker-c/three-half-rank-review`. Equation(1) therefore implies that any subsequent exact linear correction with L_V=o(V) and only one rank-one paid layer has final support slope at most24. It cannot expose even one rank25 Gaussian output. A depth of at least two is necessary in this specific postprocessing model. Cross-bank mixing is already allowed by using the common maximum23; claiming four layers from separate per-bank bounds would be unjustified.

The source-to-endpoint chronology remains a separate construction obligation, and no Gaussian productivity follows merely because the coded endpoint was realized exactly.

## Independent checks and provenance

`check.py` imports no author checker. It exhausts4096 binary rectangular matrix products, including568 zero products and3129 strict support inequalities; verifies the448 authentic N translation blocks have four distinct translations; checks exact one-query inequalities at32 finite widths without floating-point logarithms; and constructs eight width-growing nonunitary ordinary butterfly controls with support2^V and L_V=V. The latter confirms why the sublinear ordinary premise is necessary.

```bash
python check.py --output RESULT.json
python -O check.py --output RESULT-OPTIMIZED.json
cmp RESULT.json RESULT-OPTIMIZED.json
```

Receipts are byte-identical. The universal theorem is established by the row-union proof, not extrapolated from these controls. Source N was separately proved and reviewed in the preceding programme; source C is inherited from the pinned Worker B independent review. Root authored the paid-layer extension; Worker C supplied this independent proof and composition review for @CubeJerry with OpenAI assistance.
