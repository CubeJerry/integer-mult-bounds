# Independent review of scaling isolation and repair slack

The written proofs of the fixed-space identity, scaling isolation and sharp
shared-repair inequality are valid within their stated linear scopes. Root
reviewed the arguments and implemented separate GF(4) and binary-subspace
controls, without importing the author checker. This is AI-assisted review,
not human or formal-kernel verification.

## Scaling and the actual source family

On the canonical nullspace, the native orthogonality map acts as identity.
Restricting the defect there therefore gives the exact quotient repair rank.
On the further unselected-coordinate subspace U, the changed donor input map
acts as scalar t. Each zero-defect subspace is an eigenspace of one fixed B
with eigenvalue inverse(t). Distinct such subspaces form a direct sum even
when B does not preserve U. Their dimensions sum to at most dim U, proving
the isolation inequality without a diagonalizability premise.

The generic-defect argument uses a nonzero minor at t=0 only as an algebraic
witness. Zero is explicitly excluded from physical source changes. At each
nonzero t, all early source maps and foreign blocks remain invertible, the
seventy corrected rows persist, and the retained whole-record compiler pays
for the changed coefficients. No new MOVE is silently omitted. The result
does not rule out the exceptional low-defect code.

## Shared repair and saturation

For each receiver, target dimension is at least the visible tuple dimension.
Inside U+R, its target therefore has an intersection of dimension at least
dim U. Intersecting s such spaces gives the precise loss
`(s-1)(dim R-dim(U intersect R))`, and hence the advertised `(s-1)r` bound.
The graph examples attain that loss with one genuinely shared repair symbol.
The independent controls reproduce the three-receiver counterexample to a
loss of only r and the sharp examples through eight receivers.

This validates the correction to the tempting 48,876 shortcut. That earlier
scalar plane ceiling depended on exact saturation with no repair channel.
Adding a channel changes the premise; subtracting its dimension once from the
old total does not constitute a proof. No repaired scalar-source exclusion
is admitted here, and no nonlinear extension of the new subspace lemma is
claimed.

## Remaining question

The fixed-space criterion is a construction target, not a construction. A
physical low-defect code, complete ordinary/caller accounting, the complex
supplier and all five foundations remain open. The pooled-cut search is
exploratory evidence only. Credit @CubeJerry, predecessor native and atlas
authors, and S026 Worker C. Substantial OpenAI assistance is disclosed.
