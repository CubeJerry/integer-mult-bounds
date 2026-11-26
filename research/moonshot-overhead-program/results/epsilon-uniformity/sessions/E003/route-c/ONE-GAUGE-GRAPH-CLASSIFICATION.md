# Complete graph criterion for one partial-Fourier gauge per endpoint

Status: **proved within A's monomial-cross-kernel model; independent
review pending**. This extends the triangle test to arbitrary directed
retained route graphs. It does not exclude multi-path synthesis, multiple
gauges or general nonmonomial endpoint bases.

## 1. Exact model

Let D be a finite-dimensional nondegenerate paired binary space with
norm-one directions d_v. Let E be any set of directed retained routes.
Choose one input subspace `U_v subset d_v-perp` and one output subspace
`V_v subset d_v-perp` per label. They may differ. A's reviewed partial-basis
criterion says that an individual retained cross-kernel has monomial
middle precisely when

    V_w=U_v-perp                  for every (v,w) in E.                 (GC1)

The phase separation, paired two-half kernel and exact source scope are
those checked in `REVIEW-A-GLOBAL-ENDPOINT-GAUGE.md`. Each route must be
individually monomial. Synthesizing a kernel from a sum of several distinct
monomial paths is a different mechanism.

## 2. Directed component-completion criterion

Form a bipartite graph with an input copy v_in and output copy v_out of
each label, and an edge v_in--w_out for every (v,w) in E. For each
nontrivial connected component let A be its input labels and B its output
labels. A and B can overlap as sets of original labels.

**Theorem GC.** The gauges exist if and only if every component satisfies

    <d_v,d_w>=0                   for all v in A, w in B.                (GC2)

All assignments on that component are obtained by choosing a subspace W
in the interval

    span{d_w:w in B} subset W subset span{d_v:v in A}-perp,              (GC3)

and setting `U_v=W` for v in A and `V_w=W-perp` for w in B. Isolated
endpoint copies impose only their individual auxiliary-space restriction.

Proof. Assign U_v to input v_in and V_w-perp to output w_out. GC1 makes
the assigned subspaces equal along each edge, hence constant W throughout
each component. Input restrictions give `W subset span(A)-perp`.
Output restrictions give `W-perp subset d_w-perp`, equivalently `d_w in W`.
These are precisely GC3. Such an interval is nonempty exactly when GC2
holds, and W=span(B) supplies a constructive solution. Nondegeneracy
justifies taking the orthogonal complement twice. QED.

On a component containing an edge, norm-one directions ensure
`1<=dim W<=dim D-1`. Thus the constructed gauges have dimensions allowed
by A's model. Repeated directions cause no exception. The criterion is
computable by graph traversal and binary linear algebra. It must check
the cross Gram entries on the component's completion, not only its edges.

## 3. Bidirected graphs and a triangle-free obstruction

Suppose E consists of both orientations of an undirected graph G. Within
a connected component, two-edge walks identify the input gauges of their
endpoints. An odd cycle makes the endpoint-copy graph connected with the
same label set on both sides. GC2 would then require self-pairing zero,
contradicting norm one. Hence each nontrivial component must be bipartite.

If a component has color classes A,B, its endpoint-copy graph has exactly
two components, A_in--B_out and B_in--A_out. Feasibility is equivalent to
orthogonality of all cross pairs in A x B, even when a cross pair is not
a retained edge. One explicit solution is

    U_v=span(B), V_v=span(A)-perp       for v in A,
    U_w=span(A), V_w=span(B)-perp       for w in B.                       (GC4)

Bipartiteness alone is therefore insufficient. In F2^4 with ordinary dot
product, the norm-one directions with bit encodings

    d_1=1, d_2=2, d_3=13, d_4=7

have orthogonality graph exactly the path 1--2--3--4. Its color classes
are {1,3} and {2,4}, but `<d_1,d_4>=1`. The gauge model fails despite
the absence of triangles and odd cycles.

**Corollary GC-full.** When every orthogonal pair is retained, the gauges
exist exactly when the full orthogonality graph is a disjoint union of
complete bipartite graphs and isolated vertices.

Indeed GC2 completes each connected bipartite component to a biclique;
all of those edges are present under the full-retention assumption.
Conversely each such biclique satisfies GC2. A's q=2 native labels give
one complete bipartite parity component; the native q>=4 triangle fails.

## 4. Scope and evidence

This classifies algebraic feasibility in the specified model. It does not
bill physical routing, coordinate changes or control. It allows isolated
vertices, separate input/output choices and degenerate restricted forms.
It does not prohibit a different charged matrix, residual transforms,
multiple gauges or multi-path kernel synthesis. Destination-only sharing
remains possible because it retains residual transforms.

`verify_one_gauge_graph.py` compares GC2 with direct input-subspace
assignment search on finite directed graph families, including the P4,
triangle and complete-bipartite controls. The receipt records coverage.
The component argument above is the universal proof.

Dependency: A's `ROUTING-GLOBAL-ENDPOINT-GAUGE.md` and the pinned source
endpoint factorization independently reviewed by C. The component criterion
and P4 example were derived during that review. No literature priority,
general circuit lower bound, formalization or human refereeing is claimed.

Credits: @CubeJerry; E003 A's gauge model; pinned OpenAI source;
substantial AI-assisted derivation.
