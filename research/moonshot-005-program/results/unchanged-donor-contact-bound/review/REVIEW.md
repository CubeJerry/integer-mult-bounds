# Independent review of the all-chart unchanged-donor obstruction

## Review conclusion and precise scope

The root argument in `root-research/contact-capacity/PROOF.md` is correct with its final restrictions. The analytic 2,786 bound is independent of the all-chart census. This review adds a source-bound decoder uniqueness lemma and an exact finite integer refinement to 2,768. Neither number is a lower bound on paid MOVEs or coded operations. No new kappa is established.

The grammar has one monotone nested-subspace path for each of 104 unchanged original X values and one path for each of 104 Y accumulators. Donor-only stationary caches at visited charts are allowed. A receiver-written record later read by another receiver is a relay and is excluded. Moving additional copies, recoding donor values, changing the eight-packet span, and exporting encoded receiver information are excluded. Local linear operations and arbitrary retiming are otherwise granted. Each receiver may use the eight original E8 packet rows and its own accumulator.

For a dimension-d chart, each path contributes to at most one chart of that dimension. Counting every cochart donor/receiver pair, including repeated pairs across dimensions, overestimates actual distinct usable pairs. Odd-line and odd-normal capacities give the six outer dimension bounds 104, 208, 416, 416, 208, 104. This remains true for stationary donor caches: the cached value exists only at a chart already counted for its original path.

## The middle-dimensional analytic inequality

I independently checked the signs in the root Fourier argument. On the even eight-dimensional subspace E of F2^9, the quadratic form q(v)=sum(i<j) v_i v_j has polar form the ordinary binary dot product and Gauss sum +16. The translation identity gives

\[
\sum_{e\in E}(-1)^{q(e)+B(e,z)}=16(-1)^{q(z)}.
\]

Let w be the all-one vector. For a four-space C having odd vectors, write C=span(w+h,U), where U=C intersect E has dimension three. If h belongs to U, then w belongs to C and C-perp has no odd vectors, so its contact product is zero. Otherwise the odd normals in C-perp correspond to

\[
e\in U^\perp,\qquad B(e,h)=1.
\]

This affine set has 16 elements. Writing S_U=sum(u in U)(-1)^q(u) and S_D=sum(u in U)(-1)^q(h+u), insertion of the two character indicators gives its character sum **S_U-S_D**, with no missing factor. Thus

\[
D=(8-S_D)/2,\qquad R=12-D-S_U/2.
\]

The restriction of the alternating polar form to U has rank zero or two. At rank zero, S_U is 0 or 8, while S_D is 0 or plus/minus 8. At rank two, both belong to {0,4,-4}. These 15 overgranted cases imply

\[
5DR\le 8D+24R.
\]

The inequality also holds for any selected subpopulations a<=D and b<=R. The bilinear expression 5ab-8a-24b achieves a maximum at a rectangle corner; all four corners are nonpositive. Summing over dimension-four charts and using both resource totals at most 104 gives 665 contacts after integer rounding. Duality gives the same bound in dimension five. The total is 2,786. The checker corroborates every Fourier sign on E and every Gauss case; these finite checks supplement the analytic derivation.

## New source-bound lemma: eight-packet decoder uniqueness

**Proposition.** For the pinned 104 ports, over every coefficient field of characteristic other than two, and at every positive coordinate volume V, any field-linear receiver decoder using the eight E8 packet values and directly meeting unchanged original donors is forced to use the standard E8 coefficient row. Consequently all 48 geometrically accessible off-diagonal donor terms are necessary at every receiver within this grammar.

Let A_j be the integer eight-coordinate E8 row of port j, normalized by A_i dot A_i=8. The packet rows are s_k=sum_j A_(j,k) X_j. For receiver i, let B_i contain the 55 other ports j with binary port dot product v_i dot v_j=1. No monotone donor/receiver paths can meet for such j, since their initial line is not contained in the receiver's final facet. The coefficient of every X_j, j in B_i, therefore must vanish in the packet decoder.

The source checker constructs a seven-by-seven minor among the rows A_j, j in B_i, for every i. Its determinant is one of plus/minus 64, 128, or 256. All 55 rows are orthogonal to A_i. Hence these rows have rank exactly seven over every field of characteristic other than two, and their annihilator is the line spanned by A_i. Scalar packet weights must therefore be lambda*A_i. The own donor i also cannot meet its receiver because its port is odd. Its target coefficient one, together with A_i dot A_i=8, forces lambda=1/8.

For V-coordinate fields, replace each scalar packet weight by an arbitrary V-by-V matrix. Apply the same seven independent equations separately to every matrix entry. All eight coefficient matrices are A_(i,k) times a common matrix. The required own coefficient identity fixes the common matrix to I_V/8. Thus arbitrary cross-coordinate linear decoding does not escape this conclusion.

The remaining 48 port rows have binary dot product zero and E8 inner product plus/minus four. Their forced packet coefficients are plus/minus one-half and are nonzero over every admitted coefficient field. A correct decoder must acquire each such original donor directly, because no other information carrying it is permitted by the grammar. This proves the 104*48=4,992 demand count, rather than assuming a historically chosen decoder is uniquely relevant.

The source-minor claim is exact finite source verification, with all witnesses published in `output/RESULT.json`; its arbitrary-field and tensor implications follow mathematically. The complete argument remains specific to the stated packet span and receiver source contract. In particular, changing the packet span is a legitimate open escape.

## Exact integer sharpening, with a proved finite recurrence

The positive population pairs from the analytic Gauss cases are dominated by

\[
(2,12),\quad (4,10),\quad (6,8),\quad (8,4).
\]

Let P contain every positive integer subrectangle (a,b) dominated by at least one of these four pairs. Any actual chart profile with positive contact count belongs to P. Discarding zero-contact profiles only releases resources.

Define F(A,B) as the maximum total contact product over finite multisets of profiles in P with donor resource at most A and receiver resource at most B. Empty multisets give zero. Removing one profile from a nonempty multiset proves, in both directions, the exact recurrence

\[
F(A,B)=\max\left(0,\max_{(a,b)\in P,\ a\le A,\ b\le B}
       \{ab+F(A-a,B-b)\}\right).
\]

Every recursive term has smaller nonnegative resources, so induction determines every state. Evaluating all 105-by-105 states gives F(104,104)=656. The code independently evaluates an exact-resource forward recurrence and the above at-most-resource backward recurrence, checking agreement at the final and adversarial boundary states. One abstract attaining multiset is ten copies of (6,8), five of (8,4), and one of (4,4): both resources equal 104 and its value is 656. This witness proves only attainment of the integer relaxation, not feasibility as actual chart paths.

Dimension-five profiles transpose dimension-four profiles, so the same optimum applies. Substituting 656 for 665 in both middle levels gives

\[
104+208+416+656+656+416+208+104=2768.
\]

At least 2,224 of the 4,992 required distinct pairs therefore need mechanisms outside this unchanged-donor grammar. A single coded operation can address several pairs, so this is not a count of required operations or a recursive-cost lower bound.

The coarse N-donor-trajectory extension in the root proof is also valid: its level bound is sum(d=1 to 8) min(N*2^(8-d),104*2^(d-1)), equal to 4,988 at N=252 and 4,995 at N=253. Thus 253 trajectories are necessary in that overgranted direct-copy extension. Additional trajectories are not synonymous with paid MOVEs.

## Reproduction and independence

Source: `research/shared-wire-split-composition/data/final.json.gz`, compressed SHA256 `2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883`.

```sh
python3 -B check.py --source /path/to/final.json.gz --output output
python3 -B -O check.py --source /path/to/final.json.gz --output optimized
```

Expected marker: `PASS_INDEPENDENT_CONTACT_AND_UNIQUE_DECODER_AUDIT`. The script uses explicit rejecting gates, no author module imports, no all-chart enumeration, and independently written integer E8 coordinates. Normal and assertion-disabled receipts agree exactly. Root developed the analytic population proof and census; this bridge-worker review independently checks the proof, supplies decoder-rank witnesses, and adds the integer recurrence. Re-executing either script is reproduction rather than an additional independent review.

Prepared for @CubeJerry with substantial OpenAI assistance. Retain the native/E8 predecessor authors' credit and Apache-2.0 provenance. All five foundations, compatible uniform suppliers, and the global current-row encoding construction remain open.
