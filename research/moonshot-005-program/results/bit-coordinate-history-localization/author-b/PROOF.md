# Properly supported nonclass words of the coordinate extension

PASS, exact scalar F2 statement for the actual111-source partition. Put W0=U+span(K0), where U is the fifteen-class indicator code and class0 consists of coordinate indices0 through7. The nonzero words of W0 outside U whose real root support lies in ANY proper real subspace are exactly

    l_i=K_i+u0,  i=0,...,7.

Each such support spans its actual coordinate terminal facet F_i. This is a universal real-support classification, not merely a census of hosted chart IDs. It grants no availability of those forms at their support charts.

Every nonclass word has the unique form K0+sum_c b_c u_c. K0 is1 on all eight members of coordinate class0. Unless b0=1, those eight roots remain in the support and span Hub. A proper word must therefore cancel class0.

Among the other classes there are eight full classes of eight roots and six short classes. Direct primary-source checks show that in every class K0 and K0+u_c select complementary nonempty support halves. Each half has one fixed four-coordinate support. In a full class each half consists of four nonzero orthogonal roots, so it spans exactly that coordinate four-plane. This real-span argument is independent of any reduction of root coordinates into F2.

After coordinate-class cancellation, there are256 choices of the eight full-class bits. The certificate records every choice and the union of its selected coordinate supports. Exactly eight unions are proper; each misses exactly one coordinate p, with each p occurring once. All other unions span Hub already and cannot become proper after adding short-class support: classes are disjoint, so no short-class bit cancels a full-class coordinate.

In a proper full-class pattern, those selected roots already span the seven-coordinate hyperplane x_p=0. Any proper real subspace containing the entire word must be that hyperplane. Both halves of each short class are nonempty and have complementary coordinate supports. Exactly one short-class bit selects the half omitting p. Consequently each proper full-class pattern has a unique completion by all six short-class bits. The resulting word is checked exactly to be K_p+u0. Its support spans x_p=0, which is the actual native F_p. This proves completeness for all32768 nonclass words without a general word search.

In coordinate order0 through7 the eight support sizes are49,53,53,51,51,51,51,53. Independent binary elimination gives rank(T_short)=6, rank(span(l_0,...,l_7))=4 and rank(T_short+span(l_i))=10. Since rank(W0)=16, its quotient by this joined space has dimension6.

For completeness, a properly supported class word cannot contain any full-class indicator, because that class alone spans Hub and disjoint indicators cannot cancel it. Thus every properly supported class word lies in T_short. Each individual short-class indicator is itself properly supported (at most seven independent orthogonal roots). It follows that the linear span of ALL properly supported W0 words is exactly T_short+span(l_i), of rank10. This statement concerns the span of the supported words; it does not say every vector in that rank10 space is properly supported.

The checker authenticates the original native bytes and exact partition, derives rational roots directly, verifies every half and its real-span premise, enumerates the256 full choices, and checks the unique short completions and eight identities. It imports no author checker. Exact class/support choices and all patterns are preserved in CERTIFICATE.json. Python optimized mode is explicitly rejected.

This small algebraic classification does not initialize a row, provide a cache, schedule a visit, restore an unknown input, or pay for any physical transport. It supplies no source word, cost claim, compiler, completed supplier or kappa. All earlier endpoint, image, chronology, ownership, erasure, precision and strict-supplier obligations remain.

Reproduce: `python -I -B check.py --repo REPO --workspace WORKSPACE --output OUTDIR`.
