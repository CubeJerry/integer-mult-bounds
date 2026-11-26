# Independent review of the complete one-gauge graph criterion

Disposition: **accepted within the declared individual-route monomial
model**. Reviewer: E003 routing A. Read and checked the full C note
`../route-c/ONE-GAUGE-GRAPH-CLASSIFICATION.md`, SHA-256
`975bfd042b9956564ced3758146f5cec059a7fe72430c1265ec5b12050a8a397`.
No independent replay of C's finite graph search is claimed here.

Assigning U_v to an input endpoint and V_w^perp to an output endpoint
makes the edge constraint equality of subspaces. Hence a connected
component has one common W. The two endpoint auxiliary restrictions
are exactly `span(B) subset W subset span(A)^perp`, proving necessity,
sufficiency and the full interval of assignments. Separate input/output
copies correctly permit one label's two gauges to lie in different
components. If a label occurs on both sides of the same component,
the norm-one condition correctly makes its cross completion impossible.

For a connected bidirected graph, the bipartite double cover has one
component when an odd cycle is present and two when the graph is
bipartite. The norm-one diagonal rules out the first case. In the second,
cross orthogonality of the entire color-class completion is necessary
and sufficient; merely checking the retained edges is insufficient.
The explicit gauges in GC4 satisfy both auxiliary restrictions and
the edge-complement identities.

The four listed directions 1,2,13,7 each have odd weight. Their zero
pairings are exactly 1--2, 2--3 and 3--4, while 1 pairs nontrivially
with 4. Thus the P4 counterexample to bipartiteness alone is correct.
Under full orthogonality retention, GC2 forces each connected component
to be a complete bipartite graph, giving the stated exact classification.

The result includes degenerate restricted subspaces but does not enlarge
the underlying source-compatible partial-Fourier model. It does not
exclude several gauges, residual transforms, sums of paths or general
nonmonomial endpoint bases. In particular it is consistent with the
destination sharing and state-walk/tree constructions.

This is independent AI-assisted written review, not a physical routing
cost proof, formal-kernel check or human refereeing.
