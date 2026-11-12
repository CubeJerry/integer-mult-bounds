# Independent review of the nested affine primal/dual interface

**Result: PASS**, for payload `77d2e907d74c2539b115d8ad60367ee74939cca2eda9e10bcf28fb2b4e7ee42c` and container `25b1de208efe04fa8c619c7a46b288ca38fcef7464498cf7035281788c746b27`. Worker A reviewed Worker B's source construction with no imports from the author's generator, validator, or algebra helpers. This review addresses the actual mixed-level current-row interface; Worker C's separate review covers literal full-word reconstruction and the final inverse audit.

## General affine-control invariant

Let a,b be independent hosted primal/dual banks, u independent coupled first-X controls, and d independent hosted reverse sources. At a checked macro boundary write

\[
z=Ra+Ku,\qquad R^T t=b-F_H^T d,
\]

where R is invertible, t is the actual dual bank, and accumulated forward observations have coefficients F_H on a and F_U on u. The controls u and sources d retain their original values.

An invertible cochart recoding z←Qz,t←Q^{-T}t changes R,K to QR,QK and preserves the invariant. An affine control update z←z+Lu changes K only. If receiver y observes the actual scalar λ^T z, add λ^T R to its hosted row and λ^T K to its control row. The paired update t←t−λ d_y gives

\[
R^T(t-\lambda d_y)=b-(F_H+e_y\lambda^T R)^T d.
\]

It supplies exactly the hosted transpose, without fabricating a separate coupled dual carrier. Reversing Q layers, subtracting actual control terms, and applying R^{-1} restores the primal bank. Decoding the dual by R^T leaves b−F_H^T d. These identities hold for arbitrary independent controls and inputs.

A forward observation may be stored in an owned stationary cache. Its later receiver read and lifetime still require checking. The reverse update must read the actual d_y at the same chart at that earlier time; algebra alone guarantees neither source.

## Actual source checks

The independent checker rederives the seven A3 groups: four rank-one stars of 13 donors and three rank-three cycles of 11 donors. Acquisition charts have dimension six. Hosted restrictions retain the needed ranks, and removed coupled columns occur as unchanged affine controls.

For every primitive it rederives the encoder and inverse transpose. At all three dimension-seven joins it checks the four actual primal and four actual dual rows. A star dual row already contains an earlier Y2 injection; the next recoding includes it. No original donor is substituted for an encoded row. There are 360 explicit current-row checks at these boundaries.

The prefix is independently replayed on all 1480 common inputs and 400 independent differences q=v−u. The entry transformation is literal. All 520 original E8 reads see their original donors, all 104 first-X rows restore, and all Y2 rows remain original. The common suffix is identical, with no changed-row feedback beyond final recoupling.

## Actual scope and remaining geometry

The word supplies 196 forward coefficients and 183 hosted transpose coefficients. Receivers 112,113,210 are complete; receiver 114 has 26 terms,211 and215 have 13 each. The hosted reverse residual remains rank 95. No individual reverse pair or complete target is claimed.

Each dimension-seven join is contained in exactly its two old receiver facets among all 104 active source facets. A remaining cycle mode that has already entered that join cannot reach a new receiver facet by monotone raw transport. The independent checker rejects such a proposed free delivery. This is a local route obstruction, not a global impossibility. The fourth current coordinate is untouched by the join matrix, so routing it to its new facet *before* that join is a concrete available extension; it is not part of this frozen word.

## Invoice and negative controls

A full independent type/lifetime walk gives 77262 instructions and614 raw MOVEs with rank mass3200, histogram {1:49,2:28,3:137,5:164,6:7,7:10,8:219}. Peak ownership is 43, final ownership zero. The complete pinned caller invoice includes all eight forward rank-nine packets and all raw splitting costs. A separately implemented integer-root bracket gives remaining moment/native 42.17235652100004 at exponent 199/200.

Five actual-word mutants fail: omitted coupled affine restoration, omitted early dual source term, wrong nested inverse transpose, skipped Y2 acquisition, and illegal extra delivery after a join. The normal and optimized reviewer receipts agree. This is source-specific finite verification plus the algebraic invariant above. It does not prove a new uniform supplier or complete κ.

## Reproduction

```bash
python -B check_nested_interface.py \
  --source "$REPO/research/shared-wire-split-composition/data/final.json.gz" \
  --parent "$REPO/research/moonshot-005-program/results/eight-packet-seven-corrections-fused/WORD.json.gz" \
  --word "$NESTED/output/WORD.json.gz" \
  --output /tmp/nested-review.json
```

The checker pins native, parent, candidate payload and complete caller invoice. It imports only Python standard-library modules. Exact expected status is `PASS_INDEPENDENT_NESTED_AFFINE_CURRENT_ROW_REVIEW`.

Review by the persistent @CubeJerry programme, Worker A, with substantial OpenAI AI assistance. Worker B authored the nested construction. Predecessor source and E8/fused-history credit remains in the pinned packages.
