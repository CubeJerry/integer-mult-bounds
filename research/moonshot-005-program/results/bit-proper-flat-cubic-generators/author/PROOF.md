# Cubic histories generated on proper rank-four source charts

**Source-bound constructive theorem and an explicit acquisition reduction.
Author certificate complete; independent review pending. No new kappa.**

## 1. Statement and retained source

Use the actual111-port BIT source with gzip SHA256
`51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78`.
Write R_j for its real root line, F_j=R_j-perpendicular, K for the canonical
binary fitting, C=row(K), and Q3 for the third Schur power of C. All value
fields below have characteristic two. The source's full120-root completion
and the preceding cubic/Koszul package identify Q3 as the rank84 cubic
evaluation code on the actual111 columns.

**Theorem.** There is an explicit binary basis of Q3 consisting of84 words
d such that the actual roots in supp(d) span a proper real subspace of
dimension4. Every word in this basis has at most8 nonzero coordinates.
These words are therefore acquirable by honest ascending reads of their
own original source records on a rank4 chart. This statement is an
availability construction, not a declaration that all84 words can be
acquired simultaneously at no additional cost.

In particular, the word

    ell = e_1 + e_56 + e_73 + e_81 + e_95                 (1)

belongs to Q3, is outside Q2, and is outside C+U, where U is the entire
36-dimensional coordinate-support/sign-parity halfclass reservoir of the
previous width-two gate. Its support has real rank4 and is orthogonal to
receiver92. Its real span D is contained in precisely the following
actual receiver facets:

    0,15,20,39,44,57,68,69,83,92,106,107.                 (2)

Thus (1) gives a concrete source mode outside both reservoirs excluded by
the quadratic and full-halfclass arguments. It does not contradict those
arguments, which deliberately retain their reservoir hypotheses.

## 2. A local difference of two global orthogonal frames

Let H and H' be two complete orthogonal eight-root frames in the full E8
completion which share exactly four lines. Let p_H and p_H' denote their
binary incidence functions, restricted to the actual111 ports. Set

    d = p_H + p_H'.                                      (3)

The full frame indicators are cubic functions on the binary quadric by
the cubic/Koszul construction. Hence d belongs to Q3 after restriction.
Let A be the real span of the four common roots. Those roots are mutually
orthogonal, so dim(A)=4. Every root in the symmetric difference is
orthogonal to A. The four roots in H minus H' already form an orthogonal
basis of A-perpendicular. Therefore the full symmetric difference has
real rank exactly4. Puncturing to the native ports cannot increase that
rank; in all source pairs used by the certificate the remaining roots
still have rank4. The full support size is8.

This is a change of global frame supported on an honest proper source
chart. Neither global frame sum itself has been assumed locally
available. Only their difference (3) is acquired there.

The exact certificate constructs the full120 real roots from the pinned
source, enumerates all2025 orthogonal frames, and identifies28350 pairs
with four common lines. Each frame has28 such neighbors. Their9450
distinct difference masks restrict to native words of weights5 through8.
Binary elimination finds rank84 and retains84 explicit independent
differences. The coefficient ranks are unchanged over any characteristic-
two extension field. Thus the finite, source-specific rank certificate,
together with (3), proves the stated all-field spanning assertion. No
claim about an unbounded family is inferred from a numerical search.

The rank computation also finds rank85 after appending one constant
coordinate to every frame indicator. Equivalently, an odd binary relation
exists among frame indicators, so their pair differences can span the
entire frame code. This last observation explains why the difference
span need not have codimension one; it is not needed as a replacement for
the emitted rank84 certificate.

## 3. The five-input mode and source coordinates

The full frame pair for (1), in the certificate's deterministic120-root
ordering, is

    H  = {0,1,96,99,108,111,113,114},
    H' = {0,69,74,87,88,99,108,113}.

Their common native roots are {0,57,83,92}. Three roots of their full
symmetric difference are among the nine omitted source roots. The five
remaining source indices are exactly those in (1). A real basis of D is
selected from those actual five roots and saved in the certificate; no
omitted input is acquired. The exact source calculation verifies

    rank(C)=9, rank(Q2)=36, rank(Q3)=84,
    rank(C+U)=39,
    rank(Q2 + <ell>)=37,
    rank(C+U+<ell>)=40.                                 (4)

All statements in (4) are binary linear algebra on the pinned source,
and hence hold after every characteristic-two scalar extension. Real
containment D subset F_i is checked with exact integer root dot products.
The real rank4 is certified by an independent nonzero rational minor and
the four common orthogonal normals.

## 4. An explicit source acquisition using the existing pivot interface

The earlier actual quadratic-history pivot proves a general masked
exchange, not an identity limited to quadratic coefficients. Here is the
complete algebra for this new mode, so its use does not depend on the
name of that predecessor package.

Every original X_k starts on R_k, every original Y_k starts at ground,
and Y_92 must eventually contain y_92+x_92 on F_92. Original inputs are
independent; no original Y value is zero. Records have arbitrary positive
whole width V. First make the same111 stationary, owned point copies
used in the predecessor construction. These are paid records.

INIT Q=0 at D. Move the five original X_k in (1) along R_k to D to Hub,
adding each to Q at D. Thus Q=ell x. Move Y_92 from ground to D, add Q,
and move Y_92 onward to F_92. There are57 canonical foreign contacts at
receiver92. Move the other52 corresponding original X_k through F_92,
add each to Y_92 there, and continue each unchanged to Hub. Move the
remaining54 originals directly to Hub. At this point all111 originals
are restored and

    Y_92 = y_92 + (K_92+e_92)x,
    Q = ell x.

INIT P at Hub and load K_92 x using the58 actual restored original reads.
Move P to F_92 and perform

    Y_92 += P;
    P += Y_92.

Now Y_92=y_92+x_92, while P=y_92+(K_92+e_92)x. Move P to D and exchange
P and Q using three ADDs. The resulting stationary cache at D retains
the dirty old history, while P=ell x. Move P from D to ground.

The word uses only the same legal INIT, same-chart ADD, nested MOVE and
owned CLEAR interface as its predecessor. This symbolic construction is
valid for every V and every characteristic-two field. A complete closure
of this partial source moves the other110 unchanged original Y records
to their terminal facets and clears every owner. Only Y_92 is completed;
the closure is not a complete multiplication supplier.

The exact movement profile of that closure is

    53[1] + 7[3] + 7[4] + 52[6] + 164[7].             (5)

Indeed the five special original X have jumps3,4; the52 other foreign
originals have jumps6,1; the other54 originals have jump7; Y_92 has
jumps4,3; P has jumps1,3,4; the other110 Y closures have jump7. Total rank
length is1562=222*7+8. Counts are113 INIT,232 ADD,283 MOVE in the closed
partial word,113 CLEAR, with113 live owners at the retained prefix. Every
owner and its actual dirty content must be included when this prefix is
extended. No zero-cost cache, original restart or extra input is used.

The literal word is an explicit specialization of the predecessor's
operation template. Its own emitted all222-column replay is retained
separately if the source-construction worker elects to integrate it. The
present certificate authenticates the new geometry and code assertions;
it does not label a not-yet-emitted source replay as independently checked.

## 5. Causal restriction and exact meaning of the escape

An adjacent frame change does not by itself complete both frames on one
descending packet. Every old-exclusive root lies in D. A chart above D
cannot lie in that root's terminal facet, because D contains that root
line. Thus a monotone receiver ending at that facet cannot receive the
old frame mode on the packet's portion above D. Below the change, that
mode has been replaced. Any proposed use of both histories must retain
and transport the displaced mode through an actual additional source or
packet interface. The local difference construction supplies no such
retention for free.

The positive result is narrower and useful: the first genuine cubic
histories outside the old two reservoirs can be acquired on a rank4
chart from as few as five native inputs, and the entire cubic code is
generated by modes with this exact proper-chart property. Shared history,
whole-system recursive cost, physical decoder, original restoration,
owned erasure, precision and uniform compiler obligations remain. The
construction supplies no completed BIT saving and no new complete kappa.

## 6. Provenance and external mathematical context

Credit @CubeJerry, the retained native E8/BIT source, the fifteen-class
target and full-halfclass reservoir authors, the cubic/Koszul investigation,
and the source-construction worker's actual masked quadratic pivot. This
package was developed with substantial OpenAI assistance.

The geometry of E8 orthogonal frames and their2025 basis table is
classical; see Waegell and Aravind, *Parity proofs of the Kochen-Specker
theorem based on the Lie algebra E8*, J. Phys. A48(2015)225301,
doi:10.1088/1751-8113/48/22/225301. The local cubic/spinor interpretation
uses Gow1997 and van Geemen-Marrani2019 as credited in the preceding
cubic package. The new source-specific claims here are the proper-chart
generation certificate, explicit five-input mode outside both previously
excluded reservoirs, and its fully costed acquisition reduction.
