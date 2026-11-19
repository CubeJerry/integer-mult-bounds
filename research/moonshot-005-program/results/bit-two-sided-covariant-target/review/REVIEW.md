# Separate review of the two-sided covariant target

**Accepted in its stated algebraic scope. No complete physical realization
or new kappa.** S028 worker C separately reconstructed the native gamma
matrices, native graph, adapted basis, all five internal block identities
and the 1,024-word algebra certificate. The author checker was read for
scope but was not imported or executed by this review.

## Mathematical argument checked

The adapted generators gamma80+I and gamma10+I are the upper and lower
two-by-two matrix units tensored with I8. At a foreign neighbour of 80,
the upper-block form of gamma forces E01 tensor T to commute exactly
when T commutes with the repeated diagonal block P. The lower version
at donor10 is identical. Each of the five actual edges satisfies both
commutators, and each entire perturbation squares to zero regardless
of whether the secondary matrix is nilpotent.

The submitted words are 1,024 independent 32-by-32 binary matrices.
Their determinant is one in F2 and remains nonzero over every
characteristic-two field. This finite exact certificate establishes the
full secondary matrix algebra; a finite random search was not used as a
proof of a generic or asymptotic claim. Combining E01/E10 with each
secondary generator produces I2 tensor that generator, and the two
off-diagonal units then give all 64-by-64 units inside bank0. The 59
whole-bank transfers in each direction transport those units to all
60-by-60 bank positions. Thus the generated algebra is M3840.

Every altered foreign edge has an identity reverse orientation.
Invertibility in both directions first forces invariant subspaces to
have equal dimensions, and the identity edge then identifies them.
Native connectivity makes one common invariant space; the full matrix
algebra leaves only zero and the whole bank. Flat embeddings and
quotients are excluded separately by the explicit common-kernel and
image arguments. Those arguments survive body replication; irreducibility
after replication is correctly not claimed.

The row-star image and column-star input each have dimension64. Their
native input supports and output supports are disjoint, so rankDelta=128.
Both relevant native rank-9 restrictions are independently verified.
They exclude intersections with the canonical row and column spaces,
giving rank(I+B)=9*3840+128=34688 and retained repair rank128. This is
the complete algebraic return rank, not the smaller proper-response rank.

The tensor-coordinate permutation identifies the bank with End(F16)^15
while retaining the same left spinor factor. The movement profile is
unchanged; the existing m870 test is inherited arithmetic, not a new
supplier result. Source coefficients, H inverse fibres, D/K matching,
physical phase normalization, ordinary work and every foundational
assumption remain outside this acceptance.

## Controls and precise predecessor diagnosis

Replacing one word in the submitted basis by a duplicate lowers rank
from1024 to1023. A wrong secondary matrix unit retains receiver covariance
but fails the actual donor action. A diagonal unit makes I+N singular.
Omitting both E10 generators leaves the first spinor half invariant.

The previous receiver-covariant target really does fail the proposed
mirrored interface: its row80/donor0 and row80/donor2 internal blocks have
donor commutator ranks16 and4 while receiver commutators vanish. This was
checked at s=1,4,12, including the prior b3840 case. The new target repairs
that algebraic compatibility issue. Two-sided commutation is an extra
requirement of the mirrored covariant interface, not a universal condition
on every possible physical implementation.

Reproduce with Python's standard library:

```sh
python -B check.py --repo REPOSITORY --author AUTHOR_PACKAGE --out /tmp/two-sided-review
```

Expected marker: `PASS_SEPARATE_TWO_SIDED_TARGET_REVIEW`. Exact reviewed
source hashes and diagnostics are in output/RESULT.json. Credit the
orchestrator's construction, @CubeJerry, all pinned native/target authors
and substantial OpenAI assistance. This is separate model-assisted review,
not human acceptance or formal-kernel verification.
