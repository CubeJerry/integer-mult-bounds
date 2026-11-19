# Independent C review of the one-star 93 target

**Accept the algebraic construction, its one-receiver optimality statement,
and the conditional movement screen.** The full-width target has fitting
rank 51,933, retained repair rank 93, all 6,470 foreign blocks invertible,
5,667 literal common correct left rows and no positive-dimensional flat
vertex-gauge input subsystem. The 1,920-width version has excess 31. Neither
version is asserted to be a physical source realization.

## Mathematical review

The native rank-nine restrictions outside receiver 80's neighborhood and
outside that receiver itself are independently reconstructed from the pinned
integer roots. They give, respectively, row and column separation for every
proper perturbation supported in that one receiver row. Thus the written
rank-addition lemma applies without symmetry or invertibility assumptions
on the perturbation. The fitting excess and retained repair rank are exactly
the rank of the perturbation.

The displayed selector table has 93 image coordinates. Its first two
restrictions to the image are the open Jordan shift J and the single closing
matrix unit E; all other restrictions vanish. Their rows jointly detect all
image coordinates. Every outside coordinate occurs once in the remaining
slots, with six final zero slots. The first selector block has full row rank
93, and the vertical selector stack has rank 5,760.

The identity (UV)^(k+1) = U(VU)^k V is correct with the stated matrix order.
Nilpotence of VU therefore proves nilpotence of UV, including its outside-image
columns. Square-zero behavior is not required. Equivalently, a kernel vector
of I+UV lies in the image of U and would give a kernel vector of I+VU; all
62 reduced matrices are independently checked invertible. This verifies the
whole foreign blocks, rather than only their restrictions to U.

Incoming identity blocks force every neighboring flat embedding to equal the
one at receiver 80. The reverse equations put that common embedding in every
selector kernel. Their injective stack makes it zero. The proof therefore
excludes arbitrary vertex-dependent injective embeddings, not only coordinate
subspaces. It remains compatible with the large common left quotient.

The optimality statement has the correct scope. For any one-receiver proper
perturbation of rank h, every changed block has rank at most h. The common
kernel of 62 such blocks has dimension at least b-62h. Any vector in that
kernel gives a constant flat family at all native roles. No nonzero flat
family therefore requires h >= ceil(b/62). Native support separation makes
this h exactly the fitting excess. The bound is 93 at width 5,760 and 31
at width 1,920, and the submitted tables attain both. The argument does not
give an unrestricted lower bound for multireceiver perturbations or other
native fittings.

## Separate controls and arithmetic

The independent checker imports no author code. It verifies every selector
at both full widths and all 62 reduced invertibility conditions. Complete
native fitting and repair matrices are checked at new widths 63 and 126,
using a different allocation order for outside-image coordinates. Every
changed complete foreign block is checked there, including its outside-image
columns. The ranks are 569 with excess 2 and 1,137 with excess 3 respectively.

Removing the closing selector leaves one undetected input direction and
restores a flat line. Merging J and E into one restriction instead gives a
cyclic permutation; adding identity is singular. These controls distinguish
the valid separate nilpotent blocks from a false closure claim about sums
of nilpotent matrices. Their additive commutator on U has rank two.

The movement comparison is recomputed from the retained paired profiles.
Integer 200th-power inequalities authenticate the rational price enclosures.
The gap is negative at m=82 and positive at m=84, with positive affine slope,
so 84 is the first passing even multiplicity. The equality
31/1920 = 93/5760 is exact. This verifies a movement ratio only; it neither
constructs the compressed source atlas nor pays its complete caller.

Reproduce with `python3 -B check.py --repo REPOSITORY --author AUTHOR --out OUT`.
Expected status: `PASS_INDEPENDENT_ONE_STAR_93_REVIEW`. Exact source and author
hashes are in `output/REVIEW-PINS.json`. This is independent agent/code review,
not human or formal-kernel certification. Credit the native authors,
@CubeJerry, S026 root and the return-bank bridge authors, with substantial
OpenAI assistance.
