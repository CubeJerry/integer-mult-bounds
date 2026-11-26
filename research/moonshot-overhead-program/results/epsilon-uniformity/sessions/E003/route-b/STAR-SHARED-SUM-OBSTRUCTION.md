# Shared partial sums for the exposed star kernel need cancellation

Status: **proved restricted linear-circuit obstruction; independent review
pending**. This refines E003 A's `ROUTING-STAR-TRANSPOSE-NORMAL-FORM.md`.
It does not lower-bound general linear circuits, tape running time or
integer multiplication.

A exposes the middle operator `S_b=sum_j b_j P_j`, where P_j exchanges
auxiliary pair register 0 with pair register j, and all b_j are nonzero.
Its monomial-sum theorem needs at least m summands. The theorem here
permits arbitrary directed-acyclic reuse of scalar partial sums.
It applies at that middle boundary. The shared auxiliary Fourier
endpoints are nonmonomial, so support arguments do not automatically
transfer through them.

## 1. Circuit model and statement

Let Omega have Q letters, m>=2, and X=Omega^(m+1). Give each coordinate
v an independent input variable x_v over any field K. The requested
output at u is

```
y_u=sum_(j=1)^m b_j x_(P_j u),   every b_j!=0.          (S1)
```

A linear circuit may freely copy wires, rename coordinates, and multiply
by arbitrary nonzero scalars. Binary gates form `alpha F+beta G` with
alpha,beta nonzero. It is **support-monotone** if every gate satisfies

```
support(alpha F+beta G)=support(F) union support(G).    (S2)
```

Thus negative coefficients and arbitrary fan-out are permitted, but a
gate cannot cancel a variable completely. Discard all unused wires and
gates. Let X_inj contain the tuples with pairwise distinct letters, and
put `M=Q(Q-1)...(Q-m)` (zero if Q<m+1).

**Theorem S1.** Any support-monotone binary linear circuit computing
the outputs S1 indexed by X_inj uses at least `(m-1)M` addition gates.
Direct separate summation attains that count for these outputs. If
`Q>=m(m+1)`, then `M>=Q^(m+1)/2`, giving at least
`(m-1)Q^(m+1)/2` scalar additions.

This is a scalar-addition count, not a bit-operation or tape-movement
lower bound. A wider fan-in gate may be charged by its fan-in minus one;
the same statement then applies to that charge.

## 2. Exact support geometry

For u in X_inj set `N(u)={P_1u,...,P_mu}`. These m neighbors are
distinct and injective. Coordinate permutations act faithfully on u,
because its letters are pairwise distinct.

**Lemma S2.** Distinct u,v in X_inj have at most one common neighbor.

Indeed, `P_i u=P_j v` implies `v=P_j P_i u`. Since u!=v, i!=j.
The product of distinct hub transpositions is a 3-cycle on `{0,i,j}`;
its direction uniquely determines the ordered pair (j,i). Two common
neighbors would give different ordered pairs inducing the same
coordinate permutation on u. Faithfulness makes those permutations
equal, contradicting uniqueness. This proves the lemma.

Equivalently, the bipartite support graph has no four-cycle. The proof
works on each orbit of a fixed letter set and therefore on their union.

## 3. Why shared partial sums cannot reduce the count

Support is nondecreasing along every used circuit path. Hence a gate
feeding an output has support contained in that output's neighborhood.
A gate involving at least two variables cannot feed two distinct
injective outputs: its support would lie in their neighborhood
intersection, which Lemma S2 bounds by one.

One output depends on m independent variables. Contract singleton-support
gates and unary scalings. A binary fan-in graph connecting those m input
vertices to the output requires at least m-1 gates: with h gates its
underlying connected graph has m+h vertices and at most 2h edges, so
`2h>=m+h-1`. This remains valid with directed-acyclic reuse within that
output's graph. Thus every output requires at least m-1 gates of support
at least two. Their sets are disjoint across the M outputs, proving S1.

Variables outside X_inj cannot help: once introduced, support monotonicity
would preserve them to an output where their coefficient must be zero.
The same argument handles arbitrary mixing between independent seed
rows when the target is block diagonal on those rows.

## 4. The injective sector has constant density when fields are wide

A union bound over equality of coordinate pairs gives exactly

```
M/Q^(m+1) >= 1-binom(m+1,2)/Q.                        (S3)
```

Thus Q>=m(m+1) gives density at least one half. In A's paired-register
normal form, `Q=2^(2f)`; already `f>=ceil(log2(m+1))` suffices.
The guarded nonstationary executor eventually has much larger f.
For a small alphabet this density conclusion is unavailable, and the
theorem deliberately retains its exact falling-factorial size.

Invertible monomial gauges preserve support intersections and this
circuit model. Dense Fourier gauges do not. The input to the exposed
middle is arbitrary because the endpoint transform is invertible, but
a different algorithm for the composed operator may avoid that cut.

## 5. Consequences and limits

The theorem rules out extensive cancellation-free partial-sum reuse,
not merely a short list of monomial terms. A scalar sharing mechanism
must use cancellation, additional nonmonomial transforms, or a different
model. It can still be possible to share **physical routing** while
performing O(m) scalar additions per coordinate. S1 does not imply m
separate interchanges or a necessary charge `m I(f)` per volume. Such
a router could change the positive toll in the coupled Walsh invoice
barrier and is not excluded here.

Nor may these bounds be summed over all source rectangles as a lower
bound for a complete pencil. The source uses signed cancellation between
rectangles; no global support-monotonicity assumption is made.

Repeated letters destroy faithfulness and can produce several common
neighbors. Non-hub transpositions destroy the unique 3-cycle product.
A zero b_j reduces the required row support. The finite checker
`verify_star_shared_sums.py` records all three negative controls,
alongside exact orbit and density checks. It does not enumerate circuits
or run a tape algorithm; Section 3 is the unbounded circuit proof.

Open next questions: can structured seed signs support a useful
cancellation-based transform, and can the weighted terms share physical
routing with a fixed number of payload arrays? Any individual-pair
mechanism must then lift to full rectangles without losing endpoint
sharing.

Credits: @CubeJerry; pinned OpenAI endpoint construction; E003 A's star
normal form; elementary support and graph arguments; substantial ChatGPT
assistance. No general circuit/tape lower bound, formal-kernel check or
human review is claimed.
