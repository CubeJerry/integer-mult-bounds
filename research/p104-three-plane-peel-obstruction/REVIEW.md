# Independent review: fixed-core endpoint peeling

Reviewed source contribution: commit
`d2d605f90619776a35276c45fb11f184d52d26f2`, package
`research/p104-three-plane-peel-obstruction`. The native source gzip is
SHA256 `ab5c1c05383a8d3a84995f1a8368e08173e776608d635ff06871651d9e494590`.
The review is by a separate research agent for @CubeJerry, with substantial
OpenAI assistance; it is not independent human or proof-kernel acceptance.

## Mathematical decision

The frame-block argument is valid in the stated fixed-core class. If
`U=BKA`, with A and B block diagonal in the new initial and final frame
partitions, then every corresponding block is multiplied on its two sides
by invertible matrices. Each forward block rank is invariant. Since the
public core is invertible, the inverse block is independently constrained
by `U^-1=A^-1 K^-1 B^-1`. The direction and order of these factors are
correct. Rational nonzero minors remain nonzero over Q(i), so enlarging
the scalar field does not remove the obstruction.

The preliminary zero-block elimination is also sound. The allowed output
groups include full, because an existing span(q) input has a full output;
therefore a forbidden output row is not the newly promoted g. Dually the
allowed input groups include zero, so a forbidden input column is not the
newly promoted h. Moving g out of full or h out of zero cannot remove the
stored forbidden entry. A nonzero coefficient obstructs an entire zero
block even when arbitrary bases within the two frame groups are allowed.
The author's complete witness census remains the finite exclusion evidence
for the nonresidual pairs; this review does not describe a repeated
independent check of every one of those coefficients.

For both residual pairs, the independently reconstructed full input/output
groups are `[47,819,h]` and `[159,931,1352]`, with h793 or h1202. Their exact
core block is `diag(1,0,0)` and their exact inverse block is
`[[0,0,0],[0,1,1/2],[0,0,0]]`. Both have rank1. The forward target requires
the additional independent [2,2] entry in the forward block, hence ranks
(2,1); the reverse target instead requires it in the inverse block, hence
(1,2). This rules out both target orientations. Merely testing the forward
block would miss the two reverse candidates.

An identity field cannot contribute an additional entry to this crossing
block: under public ascent, its input subspace is contained in its output
subspace, while anisotropic q cannot be contained in q-perp. The claimed
target ranks therefore include all relevant identities and original planes.

## Independent computation

`review.py` imports none of the author's code. The author computes forward
full matrices; this review propagates exact rational scalar functionals
backward through the opcode stream. It reconstructs the three required
forward rows and the four required inverse rows. Pulling each inverse row
back through the core gives the corresponding coordinate functional on all
1375 public inputs, independently checking factor order and inverse-row
semantics. Altering each inverse functional is rejected. Ranks of the two
3-by-3 blocks are checked using direct nonzero minors, without the author's
Gaussian elimination routine.

A separate literal first/last-MOVE census finds363 eligible initial helpers,
295 eligible final helpers and984 distinct equal-port pairs. No helper can
occupy both endpoint roles for an anisotropic port. Normal and optimized
Python executions give the identical receipt in `RECEIPT.json`.

The conclusion remains source-bound: one promoted pair, unchanged interior
scalar word, arbitrary invertible endpoint matrices only inside the new
frame groups, and the original two-plane endpoint preserved elsewhere. It
does not exclude new interior contacts, several simultaneous promotions,
operator-valued endpoint transforms outside this scalar class, or another
native source. The favorable rank-surplus calculation is only motivation;
there is no new kappa or positive supplier claim here.
