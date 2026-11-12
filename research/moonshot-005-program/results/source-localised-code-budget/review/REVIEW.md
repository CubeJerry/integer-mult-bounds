# Independent review: fully newly paid source-localised packet codes

**Accepted with the explicit requirement that every transport leg of each coded packet is newly charged. This does not exclude hybrid paid/funded transit.**

Reviewed author proof SHA256: `0ec235610b82756a60b4518323a48235f14499c5ad391aa3127322147e64ee6c`.
Reviewed certificate SHA256: `3c1c70f7e5435d2103d2052729cfa4c039d31994f27cdb0e1ecebb860fd29c16`.
The immutable native SHA256 is `2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883`.

## Mathematical proof

The acyclic fitting-matrix argument is valid. After restricting the five granted self-delivered coordinates to zero, every acyclic active vertex set U has a topological ordering making its principal block of I-K triangular with I_V on the diagonal. It therefore has rank |U|V over any field. Each packet contribution factors through one V-dimensional field, so its restricted rank is at most V, regardless of arbitrary V-by-V coordinate maps, cancellations or interactions among final packet contributions. A contribution vanishes on U unless both its donor and recipient chart sets meet U. Rank subadditivity gives the claimed acyclic inequality.

If an entire encoder/decoder rectangle lies in S, its matrix contribution can be absorbed into K. The new K remains supported on S, so the acyclic triangular argument is preserved. The remaining packet inequalities must use nonnegative weights; the supplied74 weights have positive integer numerators and positive common denominator10^6.

The chart price g(U,W) is correct for wholly paid paths. Projection modulo W bounds total downward rank by dim(U)-dim(U intersect W); projection modulo U bounds total upward rank analogously. Subadditivity of r^t for0<t<=1 gives the two-term lower price. A path through the intersection attains this lower price in the enlarged chart geometry. No dimension difference between incomparable charts is treated as a single nested MOVE.

The all-leg payment premise is essential. If A is a proper subspace of B and B of C, with both rank differences1, a funded A→B leg followed by one new B→C leg has newly paid cost1 although g(A,C)=2^t>1. Receiver side information S is an observation grant; it does not authorize free transport of an arbitrary new coded packet on the graph that supplied S. The narrowed author statement now makes this distinction explicit.

## Independent certificate check

`check_budget.py` imports no author code. It authenticates the native, the base routing payload `58186c21...`, the expanded routing payload `0df1ceb9...`, and the complete H4 invoice `b8adae35...`. The side-information matrix is specifically `main_reuse_retimed47`:1746 entries, self-delivered roles22,44,72,89,109, and99 remaining coordinates. Its underlying expanded routing scope retains original neutral-helper event times, while main routes and all47 owned edges are retimed/reused as information overgrants. These are not H4 reservation credits.

The checker reconstructs all208 raw itineraries directly from the native. It uses canonical binary Gaussian bases and union ranks for intersections, rather than the author's enumerated subspace intersections. It checks all74 acyclic sets by an independent topological deletion algorithm, reconstructs352 encoder and283 decoder chart sets, and verifies all99,616 chart pairs:12,537 absorbed rectangles and87,079 paid inequalities. The minimum certified slack is exactly1/200000 at the review precision. The weighted objective is exactly98.992356.

All1,268 mutual-information cliques are independently enumerated. Their size histogram is99,346,319,280,176,48 for sizes1 through6. The only strict discount is pair{67,80}, uniquely using chart749→105 with downward rank2. The source spaces have dimensions3 and1 and are nested. Every one of the99 singleton demands has an explicit rank1 chart-pair witness, establishing the claimed upper construction rather than merely its lower bound. Thus the relaxed fractional and integral clique-cover optimum is97+2^(199/200). The exceptional clique dual is nonnegative because1<2^(199/200)<2.

Directed powers are enclosed by an independent integer binary-search engine at denominator2^128. Complete T4 and P4 give27344 target and152424 paid positions, with18 native repetitions. The reviewed conditional allowance is below98.399076950198. The new98.992356 lower bound therefore exceeds the full H4 allowance by more than0.593279049802. No reverse duties or extra ordinary costs were needed to force this scoped exclusion, and no S8 funded reservations were imported.

Controls reject the cyclic pair{67,80} as an acyclic set and reject doubled dual weights on an actual rank1 singleton route. The receipt includes an authenticated digest of the exact S matrix, source pins, all count summaries, the exceptional geometry and each singleton upper witness.

## Scope and next obligation

The rank proof holds uniformly at every block volume and permits arbitrary linear packet encoders and decoders. The geometric price, however, applies only to one encoding chart, one decoding chart and wholly newly paid transport for each packet. It excludes neither a packet acquiring new input contributions later, different packet versions serving distinct stops, physically retained dirty-common records, nor a hybrid using available funded routes. General linear network coding can have more than rank V across a changing packet's full lifetime, so the one-packet factorization cannot simply be imposed on such a lifetime.

`HYBRID-CUTS.md` gives two sound extensions: replace geometric g by the actual newly-paid shortest-path tariff in a declared timed funded graph, or use information-rank cuts with the funded crossing capacities explicitly deducted. Neither extension inherits98.992356 without a new certificate.

Prepared by an independent review worker with substantial OpenAI assistance. Native, source-side-information, H4 and author weighted-certificate lineage retain their attribution. No complete multiplication supplier or new kappa is claimed.
