# Independent review of the auxiliary-only common-layout obstruction

Reviewer: E002 Route C. Status: **PASS within its stated algebraic model**.

Reviewed artifact: Route B, `query-representative-obstruction.md`, SHA-256
`13bf30caed3d6c791da2ae6e48101a28432a7083a39ff75a752490b66f93ffba`.
Source audit: OpenAI math commit
`3344da59991ed94f9ba711217b29c1d760badfa6`, Fourier preprint
`build/kernel.tex`, especially the free-rectangle construction and the
subsection “The endpoint Fourier transforms.”

## 1. Source applicability

The source identifies each distinguished-plus-auxiliary address vector
with the same nondegenerate bilinear space, using `d_v` for the
distinguished coordinate and a basis of `d_v^perp` for the auxiliary
coordinates. The identity `<d_v,d_v>=1` makes this a direct sum. Thus its
physical distinguished value really is `<d_v,x>`; this is not an arbitrary
choice of coordinate functional added by the proposed obstruction.

For a free rectangle, the source sets
`H=span{d_w:w in J}` and uses `H subset d_v^perp` to perform the first
partial transform using only auxiliary axes. Its surviving spatial
coordinate is the actual coset `x+H`. The source's change to the common
complement `C` changes the representative of that same coset and adds a
Fourier phase. It does not independently relabel the abstract quotient
for each source. Consequently the proposed common distinguished
coordinate must be one function of `x+H`, shared by every source.

The source uses a paired dual basis in the other half. The contradiction
in either one of these halves already precludes the proposed replacement
of the full two-half map; no additional symmetry hypothesis is required.

## 2. The linear obstruction

Since `H subset d_v^perp`, the formula
`ell_v(x+H)=<d_v,x>` is well-defined. If each source's conversion preserves
its distinguished coordinate and gives a common layout with distinguished
coordinate `tau`, then `tau=ell_v` for every source. Equality on all cosets
implies equality on all vectors of the original space. Nondegeneracy then
implies `d_v=d_v'` for all source pairs. This argument allows arbitrary
auxiliary permutations: it uses only preservation of the distinguished
coordinate and of the intrinsic coset being represented.

The distinction between a vector class in `D/H` and a functional on `D/H`
is essential. The condition `d_v-d_v' in H` need not make the two
functionals equal. QR1 correctly demands equality against every original
vector, which implies the difference is zero in the already
nondegenerate source quotient.

## 3. Distinctness and the canonical witness

For `Gamma(v,w)=1-HammingDistance(v,w)` over `F_2` and `q>=3`, QR2's
probe construction is valid coordinate by coordinate. A probe letter
different from both labels contributes one disagreement to each. Changing
one such letter to the corresponding letter of `v` changes exactly one
of the two distances. Their Gram rows therefore differ, so their generator
images in the actual radical quotient differ. This checks the real source
space, rather than an unnecessarily larger formal label space.

For `q=2^t>=4`, the rectangle with first-coordinate source set `{0,1}`
and destination set `{2,3}` is a genuine first-differing-bit rectangle:
its common prefix has `t-2` zero bits, its next bit differs, and its final
bit is free. Fixing all other coordinates to the common value zero gives
distance exactly one on every cross pair. The source polynomial has
`p(1)!=0`, so this is an actual nonzero free rectangle, not merely a
rectangle contained in the zero set of the Gram form. Its two source
directions are distinct, and the concrete choice `x=d_(0,0,...)` gives
the conflicting distinguished values one and zero exactly as claimed.

The `q=2` exclusion is correct: the Gram row then depends only on word
parity, so distinct labels can collapse in the radical quotient.

## 4. Scope of the acceptance

The result excludes phases and auxiliary-only reindexing as a complete
replacement for all query-slot-dependent common-coset maps in this
retained endpoint schedule. It does not establish a lower bound on tape
passes, on actual run time, or on the number of maps after a new sharing
construction. It permits query-touching coordinate changes, shared
multi-query executions, a larger endpoint transform, and a different
kernel or rectangle architecture. These limitations are correctly stated
in the reviewed note and are needed for the conclusion.

This gives a useful concrete falsifier for a proposed rectangle-volume
executor: if its common-layout step claims to preserve every physical
query slot using auxiliary maps alone, QR3 disproves that step. A valid
executor must explain how it implements or avoids the surviving
query-slot-dependent shear.

Credits: @CubeJerry; the pinned Fourier endpoint construction; Route B's
obstruction; substantial ChatGPT multi-agent assistance. This is a written
algebraic and source-interface audit, not formal verification or a
physical lower bound.
