# Independent review: five receivers exclude nonlinear geometric/gap15 gauges

**ACCEPT within the exact retained separated-source, identity-target, tight
H263 contract.** Both BINARY-PROOF.md and NONLINEAR-PROOF.md are correct.
The latter proves an affine restriction on selected core cosets; it does not
assume or conclude that a full bank bijection is globally additive.

This review uses a smaller witness than the author's complete 33-direction
argument. It independently reconstructs fifteen scalar fibres by multiplying
their fifteen actual off-centre node factors. It does not import either S031
gate checker, the new author's arithmetic, or any saved fibre/readout array.
The only executable dependency is the authenticated S030 geometric-cycle
review's field and native-geometry primitives. The all-width gap15 theorem
remains an explicitly reviewed analytic predecessor, not a computational
conclusion from these scalar examples.

## 1. Exact native witness and source information

The centres and ports are read from the native atlas. H263 has donors
0, 61, 62 and shared source node 49. The following five native receivers
suffice:

| Receiver | Donor-0 parameter | Role in the core |
| ---: | ---: | --- |
| 5 | 3 | first axis |
| 76 | 39 | second axis |
| 52 | 5 | third axis |
| 56 | 6 | first plus third |
| 97 | 34 | second plus third |

For each donor and receiver, the independent checker forms

    U_(j,i)(z) = v_(j,i)^2 product_(a in actual off-H nodes) (z+a).

There are fifteen distinct off-H factors and one distinct central node.
The polynomial vanishes at every actual off-H observation and has nonzero
central evaluation, so it generates the entire scalar inverse fibre. The
three axis polynomials are independent at every donor. The two displayed
additive relations hold coefficient by coefficient at every donor. This
reconstructs the required core geometry directly from native source views.

The reviewed gap15 source theorem replaces these polynomials by an injective
core embedding E_j for every allowed matrix width and finite extension, and
preserves their central scalar readouts. Thus the same three-axis and two
mixed-direction pattern applies to A^3, where A is the full additive amplitude
space. The literal scalar check authenticates this theorem's native inputs.

## 2. Why arbitrary inverse gauges become affine on this smaller core

At a tight receiver cut, each separate original-input fibre has M elements.
The target is the sum of three such fibres, while the remaining transcript has
at most M values. Hence the sumset has exactly M elements. The finite equality
case forces all three fibres to be cosets of one additive subgroup. Keeping
one donor fibre fixed and varying the others shows that this subgroup depends
only on the receiver, not on the donor or fibre values. This step requires
the stated separated-source cut and identity target; it is not a statement
about an arbitrary communication protocol with extra informative paths.

Choose one affine core coset at each donor. Joins of the three axis partition
relations show that its inverse-gauge image is exactly a coset of the same
subgroup W at all donors. The three axis subgroup sizes multiply to the size
of W, so their sum is direct. After translating base points, each restricted
bijection consequently has coordinate form

    f(x,y,z) = f_1(x) + f_2(y) + f_3(z).

The first-plus-third partition is mapped to cosets of a fixed subgroup.
Projection of that subgroup onto either participating axis is an additive
isomorphism. Therefore increments of f_1 at any base point are a fixed
additive transform of increments of f_3 at an independently variable base
point. Fixing the latter point to zero makes the former increment independent
of its base point. Evaluating again at zero proves additivity of f_1; the
same argument proves additivity of f_3. The second-plus-third direction then
proves additivity of f_2. Every restricted f is additive after translation.

The relative map between two donors preserves the five corresponding
direction subspaces. Additivity and the first triangle force the first and
third axis amplitude maps to coincide. The second triangle forces the second
and third to coincide. Hence one arbitrary invertible binary amplitude map
per donor serves both collision receivers. No field-scalar commutation or
blockwise restriction is needed. The argument permits arbitrary mixing of
extension coordinates and repeated source components.

## 3. The shared-port contradiction uses one common input domain

Use the same fixed source-coordinate base point for all five receiver
restrictions at each donor. The central quotient on each residual fibre is
its fixed base value plus d_(j,i)A. Each d is nonzero, so these fibres exhaust
the same full three-input H alphabet for every receiver. This is the key
domain check: a different decoder's fixed observations do not change the
encoder function or restrict it to a disjoint input subset.

The independently reconstructed derivative triples at receivers 5 and 76 are
(30,18,12) and (38,18,52), respectively. After removing constant offsets and
normalizing the first aggregate block, the second blocks differ by

    D(30) M_1 D(18)^(-1) + D(38) M_1 D(18)^(-1)
      = D(56) M_1 D(18)^(-1).

Every factor is invertible as a binary operator. Thus the two aggregate row
spaces have zero intersection, regardless of the third block or amplitude
dimension. A function of both aggregates is invariant under the sum of their
kernels, which is the full H input space, and must be constant.

The actual D108 packet is seen by both receivers. Reconstructing original
owners gives 45 H exits of sixteen fields each, and a 240-field visible cut
at each of the five receivers, at bank 3840. Exact recovery at this capacity
makes the visible transcript a bijection of its aggregate. Its full product
alphabet is attained, so every constituent packet, including D108, has its
full positive alphabet. It cannot be constant. This establishes the claimed
contradiction even with nonlinear H functions, output relabelings and
downstream decoding.

## 4. Controls, limits and verdict

The author's checker was replayed independently and passed its noncommuting
binary matrix controls and finite nonlinear controls. These are sanity
checks, not the proof of the universal functional equation. Its explicit
globally nonlinear map that is additive on separate core cosets correctly
guards against an overstrong global-linearity claim.

The result excludes the fixed scalar/single-gap15 quotient family after
arbitrary separate full-bank bijections. It allows every admissible width,
finite coefficient extension and matrix feedback parameter. It does not
exclude changed quotient information, multiple-gap feedback, inter-source
preprocessing, larger informative cuts, changed target blocks, or a complete
construction obtained by a different source family. No return-excess price
or complete exponent follows from this obstruction.

Replay:

    python -I -B research/moonshot-005-program/results/bit-shared-h-s031-review/binary-gap15-port-gate/root-review/check.py --repo . --out FRESH

Expected marker: PASS_ROOT_FIVE_RECEIVER_NONLINEAR_GAP15_REVIEW 15 3 56.

Root review, S031. Model-assisted independent mathematical review and a
separate native reconstruction; not human peer review or formal-kernel proof.
