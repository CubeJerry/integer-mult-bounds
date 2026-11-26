# Independent review of the exposed star shared-sum obstruction

Disposition: **accepted as a restricted support-monotone scalar-circuit
theorem**. Reviewer: E003 routing A. This review read the complete B note
`../route-b/STAR-SHARED-SUM-OBSTRUCTION.md` and checked its proof directly;
it does not claim a separate circuit enumeration or tape execution.

Reviewed SHA-256:
`f7a992b0f438efd9521eb2ffe055a5ee3d926099ae9ca55c0fddd60c1ede3511`.

The product of two distinct hub transpositions is a three-cycle whose
orientation uniquely identifies the ordered pair. Coordinate permutations
act faithfully on injective tuples. Thus two distinct injective outputs
have at most one common input neighbor. This remains true across distinct
orbits, whose neighborhoods are disjoint.

Under the stated support-monotone gate condition, any ancestor support
is contained in the eventual output support. A gate with at least two
variables therefore serves at most one injective output. Singleton-support
gates can be contracted to scalar copies of their original variable:
their nonzero value follows from the support condition. The remaining
ancestor DAG for one output connects its m variables to the output, has
m+h vertices and at most 2h edges, and hence h>=m-1. The exclusive gate
sets prove the exact `(m-1)(Q)_(m+1)` bound with arbitrary fan-out.

The collision union bound gives density at least one half when
Q>=m(m+1). For the pair alphabet Q=2^(2f), the displayed sufficient
guard f>=ceil(log2(m+1)) is valid. The fall-off for small alphabets is
retained explicitly.

The restriction to the exposed middle cut is essential. The shared
auxiliary Fourier endpoints are dense and do not preserve this circuit
model. Likewise, the proof does not imply m separate tape interchanges,
a necessary m I(f) charge, or a lower bound on complete pencils with
signed cancellations between rectangles. B states each of these limits
correctly. The result rules out cancellation-free reuse of scalar partial
sums and leaves shared physical routing open.

Credits and scope are those of B's note and A's preceding exact star
normal form. This is independent AI-assisted written review, not formal
verification or human refereeing.
