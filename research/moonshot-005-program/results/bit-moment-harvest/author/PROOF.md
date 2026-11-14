# Acquiring a common-section history on the same completed staircase lifetime

**Proved symbolic construction; fixed native words author-verified. Independent source review pending. No complete source or new kappa.**

This is a constructive extension of the programme's existing masked orthogonal staircase. A packet can complete its selected orthogonal targets and, on the same physical descending lifetime, carry one actually acquired proper-section mode to ground. The cache retains the packet's old original-Y mask at the section. Cubic section modes can be acquired in this way; they are not inferred from a static polynomial-code table.

## 1. General source lemma

Let S=(s_1,...,s_a) be a nonempty ordered set of pairwise orthogonal, nonzero real source vectors in R^d, a<=d. Let F_t=r_t^perp and C_b=intersection_(h<=b) F_(s_h), so dim C_b=d-b. Original X_t carries independent x_t from its source line to Hub; original Y_t carries independent y_t from ground to F_t and must end with y_t+x_t. Values have any positive whole-record width V over any characteristic-two field.

Let h be the sum of any subset of other original X inputs whose real source lines lie in C_a. No selected source s_b belongs to this support, because its nonzero norm excludes its line from C_a. Zero INIT, same-chart coefficient-I_V ADD, nested MOVE and explicitly charged owned CLEAR are the only primitives used.

**Lemma.** The existing a-target orthogonal staircase can be extended to leave one pure ground history h while completing every selected Y and restoring every original X, using the same single descending Hub-to-ground lifetime and one stationary owned cache Q at C_a. The only extra operations beyond genuine source acquisition and the old staircase are one Q INIT and a three-ADD exchange. Q ends with sum_(s in S)y_s at C_a; the packet ends with h at ground.

To prove it, INIT Q at C_a. Before moving the packet, send every source original contributing to h along its actual nested path

    source line subset C_a subset Hub,

ADD it into Q at the common chart, and continue it unchanged to Hub. All these originals are disjoint from S. Other unselected originals can go directly to Hub. Thus Q=h is genuinely acquired without a source restart, downward original path, or additional moving owner.

Now run the previously proved orthogonal staircase on S. At ground, prefix-code its original Y values. Acquire the X tail preloads through the actual borrowed final original X, using the nested C_b charts and restoring that original at Hub before the descending packet is born. The packet starts with sum_(s in S)x_s. At each C_b, the exact two-ADD exchange

    Y_(s_b) += P; P += Y_(s_b)

completes the receiver and replaces the packet by the old preloaded receiver. After the last target, P=sum_(s in S)y_s at C_a. All selected receivers ascend to their prescribed facets. At C_a perform

    P += Q; Q += P; P += Q.

This swaps the genuine records. P now contains pure h and descends the remaining distance to ground; Q retains the old Y mask at C_a. Every operation is chronological and cocharted. The identity holds componentwise for every V and every characteristic-two field. The construction does not make arbitrary support-local forms available without acquisition; that acquisition was the first part of the proof.

The unselected original Y records may remain at ground for a later source continuation. A closed partial word can instead move them to their own facets unchanged and clear all owned histories, paying their actual nonzero contents. Neither option completes those targets.

## 2. Low-degree section modes

For the native canonical code K, define

    h_S = product_(s in S) K_s + sum_(s in S) e_s,     (1)

where product is coordinatewise multiplication. Pairwise real orthogonality makes every selected own coordinate of the product equal1. Removing those coordinates leaves exactly the other source roots orthogonal to every selected normal. Hence h_S is a genuine common-section mode and satisfies the lemma.

For |S|=3, this is a cubic codeword corrected by the three selected coordinates. It need not itself lie in the cubic reservoir without those corrections. The exact claim below is that it lies outside the quadratic reservoir even after all completed-coordinate corrections and the eight coordinate-root patches are granted. No degree label is substituted for a physical acquisition.

## 3. Actual native cubic and D4 examples

The source is authenticated by gzip SHA256

`51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78`.

The builder first creates111 actual pure source-line copies to preserve later source access. It then applies the lemma literally, with a stationary cache333 and one descending packet334. All222 original input columns, exact rational charts, original restorations and owned lifetimes are tracked.

### Cubic section

For S=(8,10,12), the common chart has rank5. The13 source indices in h_S are

    0,3,5,6,13,103,104,105,106,107,108,109,110.

The prefix completes Y8,Y10,Y12, restores every original X, retains h_S at ground and y8+y10+y12 at the actual common chart. Its113 owners,142 ADD and136 MOVE events are explicit. Closing the other108Y and all owners gives244 MOVE events and

    7[1]+[2]+13[3]+13[4]+3[5]+2[6]+205[7].           (2)

The rank length is1562=222*7+8: only one full descending lifetime has been added to original endpoints.

Let Q2 be the binary span of canonical rows and their coordinatewise quadratic products. Its exact rank is36. Adjoin the coordinate unit rows e0,...,e7 and the three selected units e8,e10,e12; this has rank47. Adjoining the actual h_S raises rank to48. Thus this retained history is outside Q2 plus all those patches. The finite source ranks persist under characteristic-two field extension and componentwise whole-width lifting.

### Four completed roots and the twelve-point D4 section

For S=(8,10,12,13), all four selected roots are pairwise orthogonal and the common chart has rank4. The product of its four K rows equals the previous three-row product on this exact source; the fourth completed-coordinate correction removes index13. The resulting h_S has12 inputs,

    0,3,5,6,103,104,105,106,107,108,109,110.

In the rank4 coordinate section these are the12 unoriented D4 root lines: the four coordinate axes and eight sign-root lines. Their real orthogonality components are three complete four-sets,

    {0,3,5,6}, {103,106,108,109}, {104,105,107,110}.

The exact prefix completes four original targets, retains that D4 section sum at ground, retains y8+y10+y12+y13 at the rank4 section, and restores all original X. There are113 INIT,148 ADD and140 MOVE events. The closed partial word has247 MOVE events and

    9[1]+2[2]+13[3]+15[4]+2[5]+2[6]+204[7].          (3)

Its rank length is again1562. Q2 plus the eight coordinate units and all four selected units has rank48; the actual harvested history raises it to49. Thus this also escapes the quadratic-plus-coordinate reservoir. It is a cubic-section history modulo completed coordinates, not evidence of an independent degree-four term.

## 4. Exact accounting and limits

Every original traverses its required total d-1 ranks; the single packet traverses d. The source-support inputs are split at C_a, rather than charged as direct jumps through a chart they actually read. The packet's descending stages and all selected-Y outgoing moves are literal. For a>=2, with c source inputs in h, the native ADD count including111 point copies is

    111+c+3+(7a-6)=108+7a+c.

This gives142 and148 in the two examples. The cache and packet, together with the111 source copies, give113 owners. Every closure explicitly lists all113 clears, including arbitrary nonzero masks. No generic statement about the exceptional a=1 count is inferred from the a>=2 formula.

No target price or complete continuation is inferred from the constant rank length. Different real-rank jumps have different t-moments, and a continued source must supply its own exact full movement profile, decoder access, restoration and ownership invoice. The eleven-dimensional/forty-eight-dimensional algebraic spans are not paid packet counts. The actual source words contain only the displayed one retained mode at ground and one dirty original-Y mask at its real section.

At t=199/200, rigorous176-bit integer-root intervals give moments1547.298795763430166156... for(2) and1547.344467343235477321... for(3). Adding eight hypothetical bare[8] routes leaves limiting caller room11.114058437148947797... and11.068386857343636633... respectively. BUDGET.json records the exact rational enclosures. This is an optimistic whole-caller movement screen of a partial word; it supplies no actual eight-route continuation or uncharged decoder.

The higher-degree reservoir therefore has at least one real source interface. It still needs a joint chronological mechanism capable of using such histories within the full caller budget. Repeating isolated orthogonal modules remains subject to the existing14-packet lower bound and cannot reach the target by itself. This construction does not evade that theorem, provide a7/8/9-packet continuation, or discharge any compiler, uniformity, precision, erasure, ordinary BIT, complex-supplier or foundational assumption.

## 5. Verification and credit

build.py emits deterministic compressed PREFIX and CLOSED-PARTIAL words and exact RESULT receipts. It authenticates the native, constructs rational nested charts, verifies every cochart read and monotone path, tracks all222 original columns, and checks the full retained and closed partial maps. It rejects deletion of section acquisition, Y prefix coding, tail preload, original restoration, packet loading, masked completion or the final exchange. Normal and Python-O reproduction is author verification, not an independent review.

The full masked orthogonal staircase and its accounting are prior programme results at results/bit-orthogonal-staircase/author/PROOF.md. The new contribution is the general acquired-section harvest interface and these source-bound cubic/D4 words. The companion finite-geometry worker's Q2/Q3 reservoir analysis motivated the examples. @CubeJerry, native E8/BIT and all staircase/source authors retain credit. Substantial OpenAI assistance is disclosed.
