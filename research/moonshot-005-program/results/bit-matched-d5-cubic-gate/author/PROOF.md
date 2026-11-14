# A fixed common chart cannot support the matched D5 cubic architecture

## Precise theorem

Use the authenticated native 111-root source, its canonical code C of dimension9, and its cubic Schur code Q3 of dimension84. Let

I = F92 intersect F54 intersect F38 intersect F4 intersect F29 intersect F35.

This real chart has dimension3 and contains exactly the native root lines23 and61. Let B be any collection of charts D=A^perp where A is an A3 root subsystem in I^perp, subject to the requirement that distinct charts have disjoint native source cohorts outside I. For each D let Z_D be the shortening of Q3 to its native source coordinates. Define

S_B = C + sum_{D in B} Z_D + span(e23,e61).

For every characteristic-two field k, every V>=1, and every native block fitting matrix whose rows lie in S_B tensor k^V, the capped proper-cover charge satisfies

chi >=197.

The statement grants all five local cubic directions at every selected bank, arbitrary common-I coordinate corrections, and all of C. It does not require that a physical source has managed to acquire them. It therefore excludes this precise architecture even under favorable acquisition assumptions: the retained complete proper-cover target requires chi<=194, and the marked eight/nine full-route variants require chi<=138/131.

This does not exclude arbitrary raw forms supported on the bank cohorts, extra noncubic modes, overlapping bank families requiring a different acquisition mechanism, another common chart, or histories outside S_B. It is not a multiplication lower bound and establishes no new kappa.

## 1. Why at most three banks can use disjoint cohorts

The five vectors
(0,0,0,0,2,0,0,0),
(-1,1,0,0,-1,1,0,0),
(1,-1,0,0,0,0,-1,-1),
(0,0,1,-1,0,0,1,1),
(-1,0,-1,0,0,-1,0,-1)

span I^perp and have twice the A5 Cartan Gram matrix: squared lengths4, adjacent products-2, and all other products0. Their consecutive sums give exactly the15 full root lines in I^perp. Thus these roots have the usual A5 edge model on six vertices, with a root line for every unordered pair of vertices.

An A3 subsystem corresponds to a four-vertex subset; its complementary pair is an edge of K6. There are exactly15 such normal subsystems and hence15 possible D5 banks. Their full source sets each have20 root lines; the native puncture leaves16,17,or18.

The common chart I has four full root lines, of which exactly23 and61 are native. Exact source incidence checks over all105 bank pairs show that two native cohorts are disjoint outside I exactly when their complementary K6 edges are disjoint. Consequently a compatible family is a matching on six vertices and has at most three banks. Every such family extends to one of the15 perfect matchings. A maximal triple covers47,48,or49 native source coordinates.

This classification is complete within the stated A3-normal bank class; it is not a search over a selected subset of banks.

## 2. The source overlap is explicitly allowed for

Each local cubic shortening has dimension5. For every maximal triple, C plus its three local shortenings has dimension24. Adding both shared coordinate directions e23,e61 raises the dimension to26.

The added two directions are essential to the scope. A genuine source may remove shared input terms from each local mode so that every outside-I original feeds only one bank, acquire the shared values once at I, and correct them when a descending packet reaches I. Such punctured modes need not remain in Q3 individually. They are nevertheless all contained in S_B, so the theorem includes this correction mechanism.

The theorem does not include arbitrary functions on all47--49 cohort coordinates. Granting those unrestricted raw coordinate directions changes the code to dimension56--58 and invalidates the present strong bound; this is an explicit scope control below.

## 3. Forced support for a fitting row

For receiver i let Z_i be its forbidden off-diagonal coordinates, the native indices j!=i with r_i dot r_j nonzero. For a candidate history code S let

L_i = {v in S : v restricted to Z_i is zero},
H_i = {v in L_i : v_i=0}.

The canonical fitting row K_i lies in L_i and has own coordinate1. Therefore every scalar fitting row in S is exactly K_i+H_i.

A foreign coordinate j is forced to remain1 when K_i(j)=1 and every vector of H_i has coordinate0 there. The checker computes these forced coordinates by exact binary elimination. It does not enumerate a convenient subset of fitting rows or assume that their coefficients are scalar in a vector implementation.

The same forced coordinates remain identity blocks for every field of characteristic two and every widthV. All the defining linear equations and nullspace bases are binary. Their ranks and identities extend to every such field, and applying the resulting affine formulas to block entries forces block I_V at each listed coordinate. No commutativity of block coefficients is assumed.

## 4. Geometric lower bounds from the forced coordinates

Every forced foreign source lies in the seven-dimensional receiver facet F_i.

If these sources have real span rank7, no single proper subchart of F_i covers them, so chi_i>=1.

If their quadratic evaluation vectors have rank28, no union of two proper subcharts covers them, so chi_i=2. Indeed, two proper subcharts would admit nonzero linear equations l1,l2 on F_i; the nonzero quadratic l1*l2 would vanish on every forced source. But rank28 is the full dimension of homogeneous quadratics on a seven-dimensional vector space, contradicting such a vanishing quadratic.

The certificate obtains rigorous lower ranks using reduction modulo103 on the integer source coordinates. A nonzero minor modulo103 is nonzero over the rationals and reals. The receiver-facet dimension gives the matching upper bounds7 and28. Ambient eight-coordinate quadratic monomials are used; their restricted evaluation rank is the same as that in any seven-coordinate basis of F_i.

The row bounds are added over all111 receivers. For the15 maximal matchings the certified sums are

199,199,199,197,197,198,197,198,200,201,200,197,199,198,199.

Thus every maximal family has chi>=197. Any smaller compatible family is contained in a maximal one, and restricting the allowed history code cannot reduce the minimum charge. The same bound follows for every family in the theorem.

This is a certified lower bound, not a claim that197 is attained.

## 5. Exact checks and scope controls

check.js reconstructs the full120 projective roots from the14 tetrad supports of the admitted native source, verifies the binary doubly-even [8,4,4] code, checks the A5 simple Gram matrix and all15 full normal roots, reconstructs all15 banks and all105 incidences, and verifies all15 maximal matchings.

It reconstructs C and Q3 from the source, verifies dimensions9 and84, derives every local shortening, and checks all1,665 forced-support rows, their binary nullspaces, and their modulo103 real/quadratic rank certificates. The shared-coordinate enlargement is included in every checked row.

Three deliberately broader controls mark the boundary of the theorem:

- Granting all15 overlapping banks gives a code of dimension64; the same forced-support lower-bound method returns0. Adding the two common coordinates gives dimension66 and still returns0.
- Granting the full Q3 code also returns0.
- Granting arbitrary raw coordinate directions on each matched triple's source union yields only62--64 from this method, not197.

A returned bound0 or62--64 is not an achievable fitting charge or a successful source. These controls show that the theorem's bank compatibility and cubic-code restrictions are real premises, not hidden universal claims.

## 6. Programme consequence

The favorable movement cost of visiting a rank-five bank is insufficient to make this construction viable. Even if all local modes and common-point corrections were available for free, the code fails the coarse complete proper-cover requirement by at least3. Repeating these matched cubic banks cannot bridge the target within this exact architecture.

A repair must change at least one substantive premise: use noncubic raw modes with an actual paid decoder, acquire overlapping banks by a new shared-source mechanism, move between different common charts with complete costs, or develop another history code. The new singular-split proposal is outside this theorem and remains a separate source-acquisition obligation.

Source data are the authenticated derived recovery, not a fresh native-gzip replay after the local environment outage. Author cloud verification passed; independent review is recorded separately.
