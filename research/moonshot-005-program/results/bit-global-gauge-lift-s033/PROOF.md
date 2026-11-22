# Every admissible D rectangle has a full source-gauge lift

**Proved local algebraic construction. This is a source validity theorem and
an explicit rank-four common-response example, not a fifth whole receiver or
a complete supplier.** Source-dependent compiler prices are recorded separately.

## 1. Fixed data and scope

Work over GF(64), with polynomial x^6+x+1, or any coefficient-field extension.
The eleven native donors, actual H words, owner routes, retained whole H263/H642
interfaces and four common D1509 frames at receivers R=(6,9,48,73) are those of
S032. The protected source summand has dimension96; the other384 coordinates
are unchanged. Let L=[L_6,L_9,L_48,L_73] have rank32. Let H_j be the span of the
protected portions of every retained H263/H642 fibre applicable to donor j.
These are full H cores, not the smaller individual-quotient observation spaces.
The H_j dimensions are44 at j=0,62;36 at45,100;60 at61;0 otherwise.

Let T be the original35-owner D word. I_j are its eight input indices at donor j,
O_r its eight output indices at retained receiver r, S_jr=T[O_r,I_j], and
U=union_r O_r (22 positions). Let B={4,5,7,8}, B_j=B intersect I_j.
All index sets and matrices are literal pinned data. There is no unpriced
identification of different physical owners.

The new D word T' must be phase-legal with the same19/16 split, have invertible
phase blocks and retained sections S'_jr, and satisfy

    T'[U,B] = T[U,B].                                      (1)

For every such T', there exist invertible96-dimensional source maps G_j which
fix H_j pointwise and make all four old common source frames L_r retain their
identity D readouts under T'. Full source-view ranks, true early preparation,
whole H fibres and strict source nonsaturation then hold by composition.
This existence theorem allows changes to all source quotients at a donor.
It is broader than the earlier44-map family that edits only four D parents.
No claim says its price equals that family's price.

## 2. Exact intersection certificate

The new independently computed identity is

    H_j intersect im(L)
      = span { L_r T[O_r,B_j] : r in R }.                   (2)

The right side has dimension4|B_j|:8 for j=0,45,62,100;
16 for j=61;0 for the other donors. The verifier reconstructs H_j from the
pinned whole-H fibre columns, independently computes its rank and its
intersection dimension with L, and checks that the displayed columns lie
in H_j with exactly that rank. These three facts prove equality, rather than
only inclusion or a finite search assertion. Source matrices and incidence
bindings are inherited from the independently reviewed S032 construction;
the new finite-field elimination is separately implemented, with opposite
pivot selection and no imported author executable.

## 3. Extension theorem

Define the target image of L_r by

    V_jr = L_r S_jr (S'_jr)^(-1),  V_j=[V_j6,V_j9,V_j48,V_j73]. (3)

Each block factor is invertible, so the map L_r x -> V_jr x is an automorphism
of im(L), which is the direct sum of the four rank-eight frames.
For the intersection generator L_r T[O_r,B_j], condition(1) gives

    (S'_jr)^(-1) T[O_r,B_j] = E_Bj,

where E_Bj is the coordinate insertion for B_j within I_j. Therefore the
map in(3) fixes that generator. By(2), it fixes all H_j intersect im(L).
Combine this automorphism on im(L) with the identity on H_j. They agree on
the intersection, so they define an automorphism of H_j+im(L). Extend it by
any isomorphism between complements, or by identity on one fixed common
complement, to an invertible G_j on the96-dimensional source summand.

The implementation explicitly verifies

    G_j H_j=H_j,   G_j L=V_j,   rank(G_j)=96.

Its deterministic basis-extension construction is one possible physical
source map. Existence does not depend on this choice of complement.

## 4. Full source and whole-fibre consequences

Replace EVERY source quotient F_jh by F_jh G_j on protected columns and use
identity on the other384 columns. Every source-view matrix and true early
matrix is right-composed by the same invertible480-dimensional map. Thus all
693 geometric/639 native source views and all eleven early matrices remain
invertible. Every source inverse fibre is carried by G_j^(-1), so every joined
propagation dimension is identical to the reviewed original. The previous
bounds444<450 at five structured sources and150<450 at the other six are
retained exactly; there is no generic-rank or small-perturbation argument.

Every retained H fibre is fixed pointwise on the protected part and unchanged
on the complementary part. Since whole source observations agree on these
fibres and the H words are unchanged, all72 geometric/67 native whole-H
interfaces and their literal readouts survive. Whole inverse-fibre equality,
not just prescribed images, follows from the invertibility of the full source
restrictions, together with the inherited exact section dimensions.

Let A_jr be the original complete proper restriction, and let J_jr insert the
eight D ingress rows. The reviewed S032 identity is

    A_jr L_r = J_jr S_jr^(-1).

Right-composition by G_j and(3) gives

    A_jr G_j L_r = J_jr (S'_jr)^(-1).

Consequently the off-D proper records vanish, the new D readout is I_8, and
the entire isolated inverse fibre is im(L_r), because A_jr G_j is invertible.
This is one source system supplying all44 donor/retained-receiver interfaces.
All actual owners and routing remain inherited. Changed source preparation
must be compiled and charged, and global inverse placement remains open.

## 5. Extensions, limits, and the rank-four example

All identities persist under coefficient extensions. Tensoring the fixed data
with I_k also proves the statement for every positive repetition k, even when
T' has arbitrary matrix blocks mixing copies: (1) is then a block identity,
(2) tensors exactly, and the proof uses matrix multiplication and inverses,
not commutativity of the variable blocks. Physical finite-word prices for
changed repetitions are not supplied by this algebraic statement.

For the separately constructed overlap candidate, the saved G_j give a valid
full source lift. Direct multiplication of the literal old ingress P_j by
G_j, restricted to the forced four-space K, gives contrast rank28 and augmented
rank32. Thus the space of common linear responses has rank4, improving the
previous2. This uses independently recomputed physical ingress; it is not
inferred merely from the creator's rational section formula.

This still does not build receiver95. The actual eight receiver95 output rows
would have to annihilate the contrast on the32 native ingress coordinates,
while their restriction has rank8 by any invertible native section. Rank-nullity
therefore requires contrast rank at most24;28 does not suffice. Additionally,
source right-gauges preserve the previously proved mismatch of joined whole
fibres for every five-subset. This gauge lift alone cannot complete a fifth
whole receiver even with a changed invertible D section. A useful fifth-fibre
construction must change the source/H information diagram beyond this
coordinate-change lift and satisfy the actual eight-output equation.

The failed canonical t=1 and q4 local extensions in the separate source-validity
package are consistent with this theorem: they are different source extensions.
The theorem guarantees existence in the broader all-quotient gauge class,
not validity of every arbitrary extension of prescribed local images.

## 6. Reproduction and next question

Run verify.py from this directory with --repo, --candidate and a fresh --out.
It reads only pinned JSON inputs, emits the eleven gauges and exact result,
checks multiplication and whole-frame identities, and rejects a corrupted gauge.
The full source-rank and propagation conclusions are proved by composition;
they are not presented as new exhaustive replays of all old source matrices.

The next useful construction must make contrast rank at most24, satisfy the
actual receiver95 rows and common whole isolation, and preserve source ranks
and nonsaturation in a source family that can change the joined-fibre diagram.
The remaining100 source stars, other H/D/K/facet interfaces, affordable global
return, both strict suppliers and full recursive caller remain open. All five
foundational assumptions remain explicit. No new complete kappa.

Credit @CubeJerry, S031/S032 source/H/D constructors and independent reviewers,
S033 construction/bridge/adversarial workers, and the retained geometry/compiler
lineage. Substantial OpenAI assistance. Independent agent verification is not
independent human review or a formal-kernel proof. Apache-2.0.
