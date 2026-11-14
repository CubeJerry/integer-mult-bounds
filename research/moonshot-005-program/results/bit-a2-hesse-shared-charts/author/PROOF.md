# Native A2/E6 folding and nine shared D4 acquisition cells

**Author proof; independent review requested. No new κ.** This package identifies an actual shared acquisition geometry in the fixed111-root BIT source. The acquisition lemma below is partial: no Y output, decoder, complete supplier, or improved multiplication bound is established.

## 1. Source recovery and classical credit

Native source SHA256: 51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78.

During the execution-environment outage the native roots were recovered from the already admitted certificate research/moonshot-005-program/results/bit-proper-flat-cubic-generators/author/RESULT.json, SHA256 4ac3933fb2393c62a96ec9e931ef4936e61d0e6c912c7ce0a94398a5f19addfc. Form each full root's84-bit membership signature in the listed frame symmetric differences, and each native index's corresponding signature in the native differences. All120 full signatures and all111 native signatures are distinct; matching them recovers the exact indexing. The checker repeats this independently, checks the frame orthogonality, and checks every polar pairing against the separately admitted quadratic/exterior certificate. This is certificate-derived recovery, **not a fresh gzip replay**.

A2+E6 and A2^4 decompositions of E8 are classical. Robert A. Wilson, *An eightfold path to E8*, version29 April2012, section3.3, describes the Eisenstein model with24 axial roots and216 three-coordinate roots: https://webspace.maths.qmul.ac.uk/r.a.wilson/pubs_files/E8notes2.pdf . The present contribution is its exact native identification, the explicit acquisition/receiver charts and their source consequences. The earlier full120 Eisenstein-cycle package is a predecessor, not an independent verification of this selected spread.

## 2. The actual carrier plane and E6 complement

Put a=r92, b=-r15, c=-r106. The integral roots satisfy a+b=c, squared norms4, and a·b=-2. Thus P=span_R(a,b) is an A2 plane and D=P-perp has dimension6. Their admitted binary labels are196,45,233, with XOR zero and mutual polar pairing1. Their binary two-space U is anisotropic. Its orthogonal complement has64 elements,36 of quadratic value1 and28 of value0, hence minus type.

Write x=u+w in U direct-sum U-perp. The full120 root lines split into36 common roots (u=0,q(w)=1), three wings of27 (u nonzero, w nonzero and q(w)=0), and three carrier exceptions (w=0). The native counts are

    32 common +25+25+26 wing +3 exceptions =111.

Common real source lines lie in D. Wing u lies in F_u and neither other carrier facet. The three carrier facets intersect pairwise in D.

The canonical fitting satisfies

    K(x,x')=1+B_U(u,u')+B_D(w,w').

Same-wing blocks are J+B_D and distinct-wing blocks are B_D. The three exception rows are common+own-wing+own-exception, and sum to the all-ones row. The canonical nine-code can therefore be expressed by three carrier totals and six E6 moments. This identity does not grant access to those values.

## 3. Twenty-seven matched triples

Define

    t_a=-(a+2b)/3, t_b=(2a+b)/3, t_c=(b-a)/3.

They sum to zero, have squared norm4/3 and pairwise inner product-2/3. Each is perpendicular to its corresponding carrier root. For each nonzero singular E6 point w, the three full wing root lines admit orientations

    r_(a,w)=t_a+v_w, r_(b,w)=t_b+v_w, r_(c,w)=t_c+v_w,

with the same v_w in D, of squared norm8/3. GEOMETRY.json records every oriented root and the integer vector3v_w; the equalities are checked exactly. The triple's acquisition chart H_w=P+span(v_w) has rank3. Two distinct such charts share P and span rank4. The puncture retains23 complete triples, three doubles and one singleton; absent values are never introduced.

The singular E6 points carry the elliptic-quadric line structure {w,z,w+z}, where B_D(w,z)=0. There are45 lines, five through every point. On each line the corresponding real weights sum to zero and span a real two-plane. These45 exact identities are finite source premises in the receipt.

## 4. An explicit nine-line spread and its D4 cells

Use four pairwise orthogonal native A2 triples:

    (92,15,106), (1,65,61), (7,55,56), (16,95,103).

The latter three split the E6 binary space into three anisotropic two-planes. Rotate each nonzero plane triple cyclically. The resulting linear map T has order3 and no nonzero fixed point. Every nonzero singular point has exactly two nonzero plane components, so w+Tw+T²w=0 and B_D(w,Tw)=0. The nine orbits are quadric lines and partition all27 points. This is a constructive proof of the spread, not an inference from a search.

For an orbit L put C_L=P+span_R{v_w:w in L}. It has rank4. Its full E8 root lines are precisely the fixed three carrier lines and the nine wing lines indexed by L, a D4 subsystem. The nine cells partition the76 native wing inputs in sizes9,9,9,8,7,9,8,8,9.

Fixing carrier u within a cell gives three mutually orthogonal wing roots. Their span is the rank3 chart S_(L,u)=C_L intersect F_u. If fewer than three inputs survive puncturing, the prescribed full rational chart is still valid, without supplying any missing input.

## 5. Hesse incidence and exact receiver access

Every pair of cells spans rank6. Of84 triples,12 span rank6 and72 span rank8. The12 proper triples form a Steiner system on9 cells: every pair is on exactly one triple. Four parallel classes each partition the9 cells into3 disjoint triples. This is AG(2,3)/Hesse incidence.

For each rank6 line-chart its orthogonal root lines are an A2 triple among the full36 common E6 roots. These12 triples partition the36 common roots;32 remain native. For example cells0,1,2 share a rank6 chart contained in facets F10,F18,F23. The receipt lists every cell, line-chart and containing receiver facet.

S_(L,u) is contained in exactly the receiver facets containing C_L, together with F_u. In particular **no wing receiver facet contains any S_(L,u)**. This restriction is checked for all27 charts.

The hierarchy

    source line -> S_(L,u) rank3 -> C_L rank4 -> chosen line-chart rank6 -> Hub

is nested. Each cell belongs to four line-charts, but an ascending original record must choose its route; incomparable rank6 visits are not free. The72 rank8 triple unions are a negative control to the proper-sharing claim.

## 6. A local ternary tensor operator

The same four-A2 decomposition splits the full roots into12 axes and four ternary27-point families. Each family uses three of the four binary planes and lies in the proper real six-space omitting the fourth plane. Its three nonzero plane labels independently take three values. Distinct roots in one family are orthogonal exactly when their labels differ in two coordinates.

Over every characteristic-two field let J be the3-by3 all-ones matrix and D=I+J. They are complementary projections of ranks1 and2. The family fitting is

    K27=I⊗I⊗I+D⊗D⊗I+D⊗I⊗D+I⊗D⊗D.

On a product using r of the D-eigenspaces its eigenvalue is 1+choose(r,2) modulo2. It is1 for r=0,1 and0 for r=2,3. Hence rank K27=1+3*2=7 over every characteristic-two field. Each row's12 foreign roots span a proper five-space. This is a local code/operator statement, not an available seven-mode broadcast. The selected native cube sizes are23,25,25,26.

## 7. Constructive acquisition lemma and exact expenses

Start from untouched original inputs. For each of the76 wing roles make an actual owned point copy at its source line, using one INIT and one ADD. These copies remain there. For each of the27 groups (L,u), INIT an owned zero cache at S_(L,u). Move each surviving original X_i of the group from its source line to that chart, and ADD X_i into the group cache. Leave the originals parked there.

All original values remain unchanged, the27 caches equal their disjoint nonempty input sums, the35 other original X remain on their source lines, and all111 Y remain unchanged at ground. The27 sums are linearly independent over every value field because their nonempty supports are disjoint. Exact costs are

    INIT103, ADD152, MOVE76, movement76[2], peak103 owned.

No downward MOVE or completed output is claimed. The direct restored variant additionally pays76[5] to move the parked wing originals to Hub. The live parked variant leaves the nested rank4/rank6 route options open. Every subsequent visit, copy, ordinary operation, ownership retirement and restoration must enter the actual continuation's invoice. Creating103 records is not zero work merely because it creates no MOVE.

This operation-by-operation prescription proves the stated partial source lemma over every characteristic-two field and block width. Worker A owns the integrated chronological implementation. Worker C separately evaluated a small reference builder on all222 independent formal columns in cloud JavaScript before that division of work; its receipts are supplementary author evidence, not independent review of A's word.

Merely restoring X endpoints and moving all Y to their final facets gives a closed-partial movement profile76[2]+76[5]+146[7], rank length1554. The Y values are still wrong for the requested transform. Its t-moment exceeds the direct baseline222[7] by76*(2^t+5^t-7^t)>0 for0<t<1. This is a partial invoice, not a feasibility certificate.

## 8. The no-point-copy control fails a76V information cut

If the76 point copies are omitted, every record carrying wing-input information lies outside the union D_wing of downsets of the76 wing receiver facets. This holds for all group caches and parked originals by section5; it also holds if the originals have already moved to Hub.

Condition on all non-wing original inputs. There is initially no wing-input information inside D_wing, but its completed receivers need76 independent own updates. Every entering width-r linear record contributes at most r information dimensions. Future entry capacity is therefore at least76V. This counts actual information crossings, not distinct lifetimes. Under monotone ascending public routes, local births cannot introduce outside information without an entry.

Retained point copies avoid this particular contradiction; they do not certify every remaining cut or a full decoder. GEOMETRY.json's acquired_cache_prefix entry is explicitly marked as the excluded no-point-copy restored control. It must not be mistaken for the retained live variant of section7.

## 9. What remains and how to reproduce

The next mathematical construction is a mixed relay on the9-cell/12-line incidence, using actual acquisitions along source->rank3->rank4->rank6 and paid descent to wing receivers. Masks, original restoration, ownership and every receiver endpoint must be solved jointly. Static rank and incidence do not provide this chronology. The parked prefix is an alternative initial source, not an automatic extension of a different prefix that has already moved those inputs.

check.mjs exports the pure function checkA2Geometry(flat,quad), where flat is the admitted flat-cubic RESULT.json and quad is the admitted bit-quadratic-exterior/author/RESULT.json. The latter has Git blob c4aff12ff1e9388962d7c635fd227b302f8e6500 at programme checkpoint12b269a9; the flat certificate has Git blob39bcf63f239b633e76628f6df5d0eb7472054734 there. Authenticate these input files before parsing them: embedded source-pin strings alone are not file authentication. The checker has no runtime package dependency and uses exact fraction-free BigInt elimination with integer gcd normalization.

A Node reproduction can import readFileSync from node:fs, parse the two pinned files, import checkA2Geometry from ./check.mjs, and serialize checkA2Geometry(flat,quad). Expected status is PASS_AUTHOR_A2_E6_D4_HESSE_SHARED_GEOMETRY. The exact function body was executed in cloud JavaScript during the outage. This is not represented as local-executor testing or as independent review.

All native compiler, precision, owned erasure, full recursive supplier and outer-theorem obligations remain open. There is no new complete κ.

Credit root for the carrier split and GQ spread question; Worker A for the live parked-source continuation and actual history-fork motivation; Worker C for this source-bound geometry, exact certificates, tensor identity, acquisition lemma and retention control. Preserve predecessor native, quadratic, flat-cubic and Eisenstein credit and classical lattice attribution. Prepared for @CubeJerry with substantial OpenAI assistance.
