# Independent review of the operator invariant-filtration theorem

**Accepted as a universal characteristic-two code theorem under the stated
common invariant-filtration premise. No physical source or new kappa.**

The proof checked is pinned by `author_proof_sha256` in `RESULT.json`.
This review is by the programme orchestrator, independently of Worker C's
author argument and implementation, for @CubeJerry with OpenAI assistance.
No human or formal-kernel verification is claimed.

## Universal argument

The essential matrix is the vertical stack of the fitting with a basis of
the canonical tensor code. Its rank is `9V+d`, not merely the fitting rank.
A single basis adapted to a common value-space flag triangularizes every
coefficient block, and also the identity coefficients of that canonical
basis. Reordering by value layer makes this entire rectangular stack block
upper triangular. Each diagonal stack is exactly the corresponding smaller
fitting stacked with its own canonical code.

For a block upper-triangular rectangular matrix, independently chosen
nonsingular diagonal minors combine into a nonsingular square minor: the
selected matrix is square block upper triangular and its determinant is
the product of the diagonal determinants. This proves the needed rank
inequality even though a layer has more rows than columns. No false rank
equality, subtraction of separate lower bounds, or assumption that off-
diagonal blocks vanish is used.

A diagonal-layer foreign block can be nonzero only if its original block
was nonzero. Thus every layer separately has arrival charge at most 194.
Apply the already admitted proportional quotient theorem to each layer,
then sum the resulting quotient lower bounds using the stacked-rank
inequality. This gives `d >= V + sum ceil(v_a/17)`. Each layer has at least
as many double-saving rows as the original fitting, so the weighted
denominator `17-min(b,9)` transfers in the stated direction. The bounded-
layer and complete-flag corollaries follow from integer ceiling bounds.

Field extension preserves ranks of all the finite matrices involved, by
the nonzero-minor characterization. Over an algebraic closure, a finite
commuting family has a common eigenvector: successive eigenspaces remain
invariant under the other commuting operators. Repeating on the quotient
constructs a complete invariant flag. This proof works in characteristic
two, without diagonalizability or a characteristic-zero Lie theorem.
Consequently commuting coefficients force `d>=2V` at the target arrival
threshold, even with nilpotent parts or nonsplit initial coefficients.

Noncommutativity alone does not evade the conclusion. Noncommuting upper-
triangular families still have a complete flag. Conversely opposite
nilpotent matrix units have different one-dimensional kernels and cannot
have a common invariant line over any extension, so the argument does not
silently triangularize arbitrary operator families.

## Independent native controls

`check.py` imports no author code. It reconstructs real orthogonality and
the binary canonical fitting directly from the pinned rational native
word. It constructs the two declared six-root patches from their explicit
sets, recovers both seventeen-receiver eligible sets and their overlap of
five, and reproduces the exact fitting with charge 193, rank eleven, and
canonical quotient dimension two. It compares all 111 reconstructed rows
with the frozen scalar fitting. Identity tensor lifts at widths 1,2,3,5,8
attain `d=2V`, confirming algebraic sharpness for every width via the
universal tensor-rank argument.

Additional fitting controls perturb extant blocks by noncommuting upper-
triangular operators and by a common two-plus-three-dimensional invariant
filtration. The stacked quotient is computed directly and compared with
the sum of its layer quotients. Three hundred exact binary rectangular
matrices test unequal row/column layer sizes. A nonzero lower-block example
violates the claimed inequality if triangularity is removed; duplicate
rows guard the elimination routine. These are finite corroboration of the
proof, not a finite-domain replacement for it.

## Scope

The theorem measures innovation relative to the nine-dimensional canonical
code. It does not imply `rank(A)>=11V` without an additional relationship
between the actual historical span and that code, and it does not count
physical packets. The explicit sharp code is not an acquisition schedule
or a decoder. Its eleven-port supported innovation, or twelve ports after
including the retained pivot, is still excluded by the separately reviewed
point-retained handoff theorem under that theorem's premises.

The proportional quotient theorem and its pinned native seventeen-savings
geometry are inherited dependencies, not independently re-proved here.
Both strict suppliers, complete recursive accounting, and all five
foundations remain open. Any useful fractional-width proposal must now
identify a coefficient family without a complete common invariant flag;
this is a necessary structural condition, not evidence of existence.

## Reproduction

```bash
python3 -I -B research/moonshot-005-program/results/bit-operator-invariant-filtration/review-root/check.py \
  --native research/paired-query-only-bit/retained/inputs/BIT-NATIVE-WORD.json.gz \
  --author research/moonshot-005-program/results/bit-operator-invariant-filtration/author \
  --output /tmp/operator-filtration-review.json
```

Expected status: `PASS_INDEPENDENT_INVARIANT_FILTRATION_REVIEW`.
