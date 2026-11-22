# A forced receiver-95 mismatch under source-only recoding

**Scoped obstruction. No complete supplier or new κ.** This follows the four-receiver construction in `../bit-simultaneous-d1509-s032/` and examines the most economical next rank repair, receiver 95. It allows genuine changes of the individual linear source quotients, rather than only whole-bank input changes.

## 1. Proposition and exact scope

Freeze the physical source-owner routing and the H/D phase words of the S032 four-receiver construction. Allow arbitrary new linear source records on the full 480-coordinate source banks, delivered to the same actual H input owners. Retain the following literal interfaces:

1. The complete H263/H642 inverse fibres at their 67 native views, with their existing common readouts.
2. The common complete D1509 inverse fibres at receivers 6,9,48,73, with the existing eight-parameter readouts.

Then the modified sources cannot also supply a common entire receiver-95/D1509 inverse fibre with equal donor readouts. The obstruction already involves donors 61 and 0. It does not require a source edit count bound or an assumed propagation lower bound.

The maps may change independently at different source quotients and donors. They need not be common right coordinate changes, and they may mix protected and complementary source coordinates. The proof uses linearity and fixes the specified physical H/D words, owner routing and old literal interfaces. It does not cover nonlinear source functions, changed H/D words, changed routes, changed isolation requirements, or a redesign of the four current common fibres/readouts.

## 2. Necessary values of a preserved source tuple

Write F[j,h] for a source quotient, normalized into the old paired phase frame. This normalization loses no arbitrary linear source record: the old 30-by-30 phase frame is invertible. Thus an arbitrary new tuple of 30 linear functions on the same actual phase owners can be written as the old phase frame times a new F'[j,h].

For any retained whole H-centre fibre K[c,r], if source quotient h is visible at receiver r, the new tuple must agree with the old tuple on that fibre. For h different from c, the fibre requires all other visible source information to vanish. At h=c, the actual donor section of the prescribed H readout is invertible, so keeping the same readout fixes the central quotient values. These sections are the exact full-rank donor/H interfaces of the preceding construction.

For a retained D1509 fibre Lr, every source quotient h visible at r must likewise agree on Lr. Other visible D packets are zero. The actual eight-dimensional donor section of the D word is invertible, so the eight selected ingress values are fixed by the prescribed readout. At each visible H, its complete donor section is invertible and all these proper-record values fix the original paired quotient. This uses the whole proper isolation contract; merely retaining some final endpoint values would be a weaker, different premise.

Consequently, for each (j,h), F'[j,h] agrees with F[j,h] on the span of all relevant retained native H-fibre columns and all old D-fibre columns whose receivers see h. We call that the local prescribed subspace. The condition follows from the retained interfaces, rather than being an extra assumption that source coefficients stay fixed everywhere.

## 3. One forced source-61 vector

`WITNESS.json` gives a nonzero vector v in the protected 96 coordinates, extended by zero on the remaining 384 source coordinates. It also gives its exact expression in the common rank-32 span of the four existing D1509 frames.

At donor 61, v belongs to the complete old receiver-95/D1509 inverse fibre. There are exactly sixteen source quotients visible at receiver 95. For every one, the witness gives an explicit linear decomposition of v into its local prescribed subspace from Section 2. The actual quotient labels are

    263,269,284,333,343,375,384,394,468,481,642,660,783,808,906,947.

In particular, H333 and H906 are invisible to all four retained D receivers, but the necessary H263/H642 observations still force their values on v. Choosing an off-D source quotient invisible to the four receivers therefore does not evade the witness.

Every new source-61 quotient visible at 95 must keep its old value on v. Its entire proper restriction is unchanged. All other visible proper D records remain zero, and the eight actual D1509 outputs remain

    donor61: (14,8,50,38,1,0,0,0).

Thus any proposed common entire receiver-95 fibre must contain v.

The author construction of v uses the four-dimensional intersection between the old four-frame span and donor61's receiver95 fibre. The proposition needs only the single explicit nonzero vector and its sixteen certified decompositions; it does not infer impossibility from failure of a search.

## 4. Donor 0 has a different forced readout

The four H parents by which donor 0 enters D1509 are 71,116,263,283. Because D1509 is visible to each retained receiver, all these H parents are visible at all four of them. The vector v is in the span of those four retained D fibres. Linearity and Section 2 therefore fix every one of donor0's D1509 ingress values on v, even if its other source quotients change.

The physical D word is fixed, so its actual receiver95 outputs on v remain

    donor0: (14,20,31,55,1,62,23,17).

Their difference in GF64 polynomial-basis encoding is

    (0,28,45,17,0,62,23,17),

which is nonzero. If v is not isolated to D1509 at donor0, the purported complete common inverse fibre already fails. If it is isolated, the two forced readouts differ. Either alternative contradicts the desired shared fibre/readout interface.

This proves the proposition. All coefficient identities and the nonzero difference persist under coefficient-field extensions. Repeating the frozen interface and applying arbitrary linear source recoding to the full repeated banks retains the same embedded witness. No nonlinear extension is asserted.

## 5. What this adds to the four-receiver ceiling

The preceding sharp ceiling excludes a fifth receiver through independent invertible input changes of the frozen source/H diagram. This result allows arbitrary independent linear changes of the actual source quotient tuple. For receiver95, preserving the current literal H and four-D interfaces while freezing the H/D physical words still fails.

It is not a theorem excluding every source-only redesign with other retained fibres, every possible fifth receiver, or a joint source/H/D change. It says precisely that the natural receiver95 repair requires changing at least one prescribed surrounding interface: H/D processing, routing/isolation, or one of the old common fibre/readout systems. A larger amount of source coefficient search under these fixed interfaces cannot resolve the displayed mismatch.

## 6. Evidence and next step

The author checker authenticates source pins, reconstructs all sixteen decompositions from actual geometric visibility, reconstructs the source/H/D outputs from physical owner records, verifies zero off-D response at donor61, and checks the two unequal readouts. Vector and readout mutations are rejected. The independent review uses separately reconstructed geometry and physical matrices.

```sh
python3 -B research/moonshot-005-program/results/bit-fifth-receiver-quotient-s032/check.py --repo . --out /tmp/s032-fifth-source-edit
```

Expected: `PASS_RECEIVER95_FROZEN_H_D_SOURCE_EDIT_OBSTRUCTION 16 4`.

The next concrete problem is a coupled D/H and source interpolation that changes the receiver95 response of this forced vector while retaining the four existing complete cuts. Its phase invertibility, new source-view ranks, nonsaturation, real owners, caches and changed binary costs must all be accounted for. None is supplied by this obstruction.

All five foundations, the remaining source/H/D/K/facet completion, global return, strict BIT/complex suppliers and full recursive caller remain open. No new κ.

Credit @CubeJerry, the S031/S032 source/H/D and independent-review contributors, the underlying geometry and balanced-atlas authors. Substantial OpenAI assistance. Apache-2.0.
