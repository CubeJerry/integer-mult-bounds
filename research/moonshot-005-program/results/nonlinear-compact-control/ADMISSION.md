# A paid columnwise nonlinear control from retained primitives

**Conditionally proved physical construction; independently reviewed. No new kappa.**

At each selected bit position of one fixed offset rho, the construction
implements y <- y XOR(xz) on arbitrary complete records. It uses existing
dirty coordinate fields,24 compact swaps and20 rotations for the low positions,
an exact highest-bit operation, and paid exceptional-stream repair. Every
reserved coordinate is restored. The inverse uses the current inverse controls.

With G=4 ceil(log2 p)+6 and K>=G+4 ceil(log2 p)+10, the exceptional fraction
is at most7/(128p^3). Under the retained record domain and movement tariff the
complete cost is O(V*((f log p)^tau+1)); V is physical payload volume, not
tensor width. Complete addresses/descriptors have O(A) bits, A=O(p), and
records dominate fixed powers of p. The changed coordinate reservation is
explicit and eventually fits the same recurrence regime. A fixed cubic Z4
phase is a paid O(V) pass. Different bit offsets require separate accounting.

This is a derived specialization of pinned canonical movement, layout and
guard interfaces, not a new free monomial primitive or a discharge of the
global compiler assumption. Finite recipe constants, source gauges, whole
native bodies, precision and recursive callers remain separately charged.

[Proof](author/PROOF.md), [dependency pins](author/DEPENDENCIES.json),
[independent modular and source review](independent-c/REVIEW.md).
The independent checker covers arbitrary dirty states, all six slot orders,
actual inverses, invariant bad streams, exact repair and omission controls.
Author parameter tests separately cover reservations, highest-bit handling
and lifted phases. These checks corroborate the parameter-uniform proof.

Run `python3 author/check.py --out OUT` and
`python3 independent-c/check.py --out REVIEW_OUT` from this directory.
Credit @CubeJerry, root, bit_bridge and the pinned canonical source authors;
OpenAI assistance. All five foundational assumptions remain explicit.
