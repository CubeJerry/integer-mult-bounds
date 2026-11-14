# Uniform rank gap for arrival-sparse BIT fittings

**Proved over every characteristic-two field at every block width V>=1.
No complete source, supplier or new kappa.**

Let A fit the actual111-port mask with identity diagonal V-blocks. Count each
nonzero foreign block in support_i, including singular blocks, and define
ell_i=1[support_i>36]+1[support_i>52]. If sum ell_i<=196, then

    rank(A) >= 9V+ceil(V/3) = ceil(28V/3).

This allows nonsymmetric/noncommuting blocks. It is not rank>=10V and does
not replace the scalar class-code rank16 condition. [Proof](author/PROOF.md).

## Exact premises and proof

The credited #7114 LR inequality, rederived in
[saturated-star rigidity](../bit-saturated-star-rigidity/ADMISSION.md), gives
endpoint defect g_e(a)<=3h for a complete seven-star at complement V+h.
The nonnegative summation is exact. An abstract LR assignment attains3h,
so coefficient2 cannot follow from those inequalities alone.

[The certificate](author/CERTIFICATE.json) lists275 actual eight-frames,
each with a K7 whose edges have zero factor at the omitted eighth point.
The complement stays V+h. These witnesses certify3,019 unordered contacts
whose blocks have rank>=V-3h in both directions. For h<V/3 all remain
nonzero: every row has>=41 certified contacts and86 rows have>=53, yielding
sum ell>=197. Search completeness is not a premise.

The admitted [Y-feedback normalization](../bit-y-feedback-normalization/ADMISSION.md)
counts nonzero blocks. In its monotone whole-record model, q+a<=85 therefore
forces this rank floor. For q8 with<=3 extra facet arrivals, historical kernel
total is>=V+ceil(V/3). These are necessary information conditions; no kernel
mode, endpoint or physical cost is supplied. All five foundations remain.

## Independent review

The lead separately derived the K7 summation, read the all-width arrival
bridge and reconstructed every source witness. No author implementation or
frame-search output is imported.

```bash
python3 -I -B research/moonshot-005-program/results/bit-uniform-rank-gap/review-root/check.py --native research/paired-query-only-bit/retained/inputs/BIT-NATIVE-WORD.json.gz --certificate research/moonshot-005-program/results/bit-uniform-rank-gap/author/CERTIFICATE.json --output /tmp/rank-gap-review.json
```

Expected: `PASS_INDEPENDENT_UNIFORM_BLOCK_RANK_GAP`.
[Receipt](review-root/RESULT.json) includes invalid-frame, empty-coverage,
strict-threshold and LR-coefficient controls. Universal quantifiers follow
from the written proof. Review is by an independent research agent, not a
human or formal kernel.

Credit @CubeJerry, DreamingOfClouds #7114/#6933, retained source/history authors,
Worker C and the lead's independent derivation; substantial OpenAI assistance.
Admission baseline: `ce413740299df6b1f89a67dbeeb84d5f404f9f7f`.
