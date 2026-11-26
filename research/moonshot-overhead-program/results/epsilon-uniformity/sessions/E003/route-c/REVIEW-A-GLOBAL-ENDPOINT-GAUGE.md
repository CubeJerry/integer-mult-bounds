# Independent review of the one-gauge endpoint obstruction

Status: **accepted in its declared partial-Fourier, monomial-middle model**.
Reviewed `../route-a/ROUTING-GLOBAL-ENDPOINT-GAUGE.md`, SHA-256
`5b2755bf746faf5ed041f91f1cfd1a1d3dc084a1adf315008a8110d0a887ed06`.
The source pin is OpenAI math `3344da59991ed94f9ba711217b29c1d760badfa6`.
Both complete `build/kernel.tex` and `build/binary.tex` were read from
the Fourier preprint, including the full endpoint proof. Exact hashes
and an unchanged verifier replay are in `review-a-endpoint-gauge-replay/`.

## Partial-basis criterion and source compatibility

For a character supported on an affine coset of U, the character sum in
the full normalized Fourier transform vanishes off one coset of U-perp
and is nonzero at every point of that coset. A vector in B(V) has a
V-coset as its support. Equality up to nonzero scalar therefore requires
`V=U-perp`; the same character sum proves sufficiency. This does not use
nondegeneracy of the pairing restricted to U.

The actual source first removes its initial and final quadratic phases.
Its remaining common kernel is paired full Fourier on the two halves.
The auxiliary phase stays in the endpoint, while the distinguished phase
is constant on the auxiliary cosets and stays in the middle. The source
explicitly describes changes of coset representatives as coordinate
permutations and character signs. Consequently A's declared pair of
partial bases has the asserted condition `V_w=U_v-perp` for an individual
retained cross-kernel route to have a monomial middle. Tensoring both
halves changes call counts but not this subspace condition.

The scope is important: each retained cross-kernel route is required to
be individually monomial between the fixed endpoint gauges. The proof
does not rule out expressing one cross-kernel as a sum of several
different monomial paths, using more than one gauge, or using general
nonmonomial bases. Those are additional mechanisms, not consequences of
this basis criterion.

## Triangle and exceptional binary alphabet

With all six directed edges on three labels present, their shared
destinations force all three input subspaces to agree, and their shared
sources force the output subspaces to be the common orthogonal
complement. The auxiliary restrictions then put each norm-one label
direction in `U intersect U-perp`, an impossibility because every vector
in that intersection has self-pairing zero. This checks the necessity
even when input and output gauges are separately chosen and dimensions
are unrestricted within the stated range.

For q>=4, three distinct letters in one coordinate of a native label
give precisely a Gram identity matrix on those three directions.
The characteristic-zero free coefficient at distance one is nonzero:
every factor `1-1/(2h)` is nonzero. Thus the actual retained free graph
contains the required six directed edges. The rational coefficient is
not being interpreted in the binary Gram field.

For q=2 the two parity classes give two orthogonal norm-one directions
and a complete bipartite free graph. Choosing both endpoint subspaces as
the corresponding auxiliary lines satisfies the complement equations.
The exception is therefore real rather than an omitted boundary case.

## Rank statement and the exact invoice boundary

If `I=C+F` and F vanishes within each parity class, a diagonal half-size
block of C is an identity matrix. Thus its rank is at least N/2 over
every field. The paired-square construction has blocks `[[I,I],[I,I]]`
and attains that rank; the free negative cross entries restore the
identity. This verifies both the lower bound and sharpness, including
characteristic two.

The source states an implementation with 2D axis calls for a charged
rectangle, using D calls on each half. A's conclusion uses this *retained
routine as the declared invoice*: at D=2, at least N/2 charged rectangles
across m queries bill at least `2D*m*(N/2)/N=2m` calls per original label
row. It does not infer an implementation lower bound from the source's
upper bound, or exclude a different charged/free implementation.

## Finite replay and disposition

The unchanged checker passed 4,774 subspace pairs, 1,165,984 exact matrix
entries, 4,221 input-gauge triples, four native label triangles, and ten
sharp parity-rank examples. Its norm-zero counterexample correctly
rejects extending the triangle claim without the norm-one assumption.

I found no gap in the algebraic result or its stated source-model
application. Acceptance is confined to G1--G3 and the retained charged
invoice. It is not a review of every destination-sharing or state-walk
optimization, a general Clifford-circuit obstruction, a physical runtime
lower bound, or a new complete multiplication result.

Review: E003 route C, 2026-11-26; substantial AI assistance.
