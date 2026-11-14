# Independent review of the 27-role wing obstruction

Reviewer: S013 adversarial mathematics worker, separate from the construction worker who authored the source package. This is a mathematical and separately implemented exact-geometry review, not a human review or formal proof-kernel verification.

## Exact reviewed inputs

- Wing proof: Git blob 01f0c19a354b7aab7c7234664291a3072b0c11d7.
- Wing receipt: b981225c500cb654701be80c296e5af019673ac5.
- Saturated-star proof: f9f0b56e2a06231fba611ab248819ab2543a480b.
- Root recovery: 8eba43d142c819c206dce5df87ea4571aaead287.
- Native gzip provenance: SHA-256 51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78.
- Recovery certificate: SHA-256 4ac3933fb2393c62a96ec9e931ef4936e61d0e6c912c7ce0a94398a5f19addfc.

## Findings

The seven-point identity frame, nineteen actual edge roles, degree pattern (5,6,6,5,5,6,5), and all required shared-endpoint zeros were reconstructed directly from the recovered integer roots. The reconstruction code in check.mjs was written separately and does not call or import the construction worker's checker.

The common factor normalization in saturated-star Theorem A is adequate. At rank8V, the sum of LR inequalities forces every gamma rank to vanish and every intrinsic Schur block to equal -I. Ordered edge gauges and the common factor-basis change normalize both row and column factors. Thus the role3 anchors constrain the same bilinear coordinate pairing. There is no illicit assumption that independently chosen row and column gauges coincide.

The seven role3 noncontacts have normalized vectors (16,32,64,224,140,131,133). Independent binary elimination gives rank seven and common annihilator (1,1,1,1,0,0,0,0). This vector has zero self-pairing in characteristic two. Both role3 factors lie in that line tensored with the V-dimensional block space, so their diagonal product is zero, contradicting I_V. The proof neither commutes matrices nor needs the remaining V-by-V factors to be invertible.

Dropping the first anchor leaves rank six; substituting frame role0 is invalid because it is an actual contact. These exact controls were independently checked. The canonical wing fitting has binary rank nine.

**Review conclusion: the strict bound rank>8V over all characteristic-two fields and all widths is correct under the stated derived-source premise. Scalar minimum nine follows. A universal9V lower bound does not follow from this argument.**

The new weighted augmented-star proof is a separate result authored by this reviewer. Its verification by this checker is not independent review of that new theorem; root's separate review must be recorded separately. No fresh gzip replay during the execution outage is claimed.
