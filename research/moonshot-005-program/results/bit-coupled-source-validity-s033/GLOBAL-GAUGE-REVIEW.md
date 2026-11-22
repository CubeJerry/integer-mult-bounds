# Independent review of the full source-gauge lift

**Accepted within its stated local scope.** This review checks the mathematical
argument in `../bit-global-gauge-lift-s033/PROOF.md`, especially sections2–5,
and separately reconstructs its source/early/H bindings. It does not assert a
fifth receiver, full supplier or new κ. The reviewer did not import the new
lift constructor. Its field routines are the earlier source implementation,
separate from the lift author's reverse-pivot implementation; inherited S032
source admissibility remains an explicit dependency.

## Intersection and extension argument

The intersection identity is sufficient in its stated form. The displayed
columns lie in im(L) by construction; the root's exact dimension/inclusion
certificate proves they span H_j intersect im(L). Defining the map on each
rank-eight retained frame by S_old S_new^-1 preserves that frame's span.
Since all four frame spans are independent, this gives an automorphism of
im(L), not merely a rank-preserving list of individual images.

For b in B intersect I_j, the fixed retained-output/input rectangle gives
S_new E_b = T[O_r,b]. Thus S_new^-1 T[O_r,b]=E_b in the correct multiplication
order, and the specified source map fixes L_r T[O_r,b]. It therefore fixes the
whole intersection. The identity on H_j and this automorphism on im(L) agree
on their intersection and give an automorphism of their sum. Extension by
identity on a vector-space complement is valid. This also explains why the
construction does not need a probabilistic completion argument.

This theorem permits changing all28 quotients at each source. The earlier
canonical44-map extension is a smaller and different choice; its singular
source views do not contradict existence of this broader gauge lift.

## Source, H and D inheritance

A common invertible right composition of EVERY source quotient gives the same
right composition of each full source view and true early matrix. Hence all
view ranks remain full. The inverse image of every quotient coordinate block
is carried by the same inverse gauge, so the dimension of every joined
propagation span is preserved exactly. This supports strict nonsaturation
without assuming that upper rank bounds survive generic perturbation.

The full paired H fibres are fixed pointwise: the protected constituent lies
in the fixed H core, and the complementary constituent is unchanged. Since
H operations and owners are unchanged, every observation and common H readout
on those spaces is unchanged. Full source invertibility turns the inherited
contained spaces into entire inverse fibres. For D, the exact formula
A_old G L_r = J S_new^-1 follows by multiplying the original proper-restriction
identity on the right by S_old S_new^-1. The new phase word therefore supplies
the same actual identity outputs on the same complete common frame.

`review_global_gauge.py` checks all eleven gauge ranks, all308 composed source
quotients, physical early-owner row reconstruction, all applicable full paired
H fibres and all44 oriented D source-frame equations. These exact checks pass.
The claimed693/639 source-view counts and nonsaturation inherit from the
source-pinned S032 theorem by the proved composition; this review does not
present them as a fresh full replay of that predecessor.

## Arbitrary repetitions and the remaining geometric barrier

The block-valued extension is valid when understood as a statement about
finite-dimensional vector spaces: tensor the fixed spaces with the repetition
space, treat each S_new as an invertible8k-by8k matrix, and repeat the same
intersection argument. No interchange of noncommuting variable blocks occurs.
Physical compiler costs of arbitrary block-valued candidates are not provided
by this algebraic existence theorem.

A source gauge transports every isolated proper D subspace by one invertible
map per donor. Changing an invertible D section changes the orientation of its
readout, but not that isolated source subspace. Thus the previous unequal
five-fibre join ranks persist. The rank-four forced-space response example
removes a specific rank-two common-response defect but still cannot construct
receiver95 in this gauge class. The actual eight-output rank condition also
requires contrast at most24; the candidate's contrast28 fails it.

## Physical specialization and separate D checks

The q4 gauge realization is actually compiled, not only declared admissible
by linear algebra. `global-gauge-q4/COMPILER-RESULT.json` reports fresh binary
replay of all31680 source original columns and all210 D columns, including
pure phase inverses. All11 source phases change. The280 unchanged H receipts
are reused; no source receipt is counted as unchanged. The gross local bill is
454470648 ADD,279648 INIT/CLEAR each and16 gap6 field exports. It is533040 ADD
above the old four-receiver local bill and adds no MOVE. Global inverse
placement and the complete supplier bill remain open.

The separate `Q4-D-SECTIONS.json` reconstructs every geometric section directly
from the35 owners and atlas incidence: all144 rank-eight sections and both
19/16 phase ranks pass. This is separate from the root's retained-section
check and from the candidate author's generator.

Credit @CubeJerry, S033 root and construction workers, and predecessor
source/H/D, atlas and compiler authors. Substantial OpenAI assistance.
Independent agent review, not independent human or formal-kernel review.
Apache-2.0.

## Three-overlap refinement

The same complete composition review and binary compiler checks also pass
for the later three-overlap realization, saved in `global-gauge-three-overlap/`.
Its source/D realization has contrast27 and augmented rank31 in the separate
construction/review certificates, hence common-response rank4. The review
here independently checks its full source-gauge bindings, all whole H and
retained D frame equations and all144 geometric D sections. It does not
independently recalculate the contrast ranks in this checker.

The later realization costs454540232 ADDs,602624 above the S032 physical
baseline and69584 above the preceding two-overlap q4 realization. INIT/CLEAR
remain279648 each; the16 gap6 field exports remain. All11 source phases are
freshly compiled and replayed on31680 original binary columns; all210 D
columns and pure inverse words pass. Its D cost is26644 ADDs per base instance
including phase inverses. A smaller D-only cost does not imply a smaller full
source/D bill: the new source preparations account for the net increase.

This is the stronger geometric checkpoint, with a slightly higher local
physical bill. Neither realization meets the necessary contrast≤24 condition
or changes the excluded five-fibre join-rank geometry of the gauge class.
