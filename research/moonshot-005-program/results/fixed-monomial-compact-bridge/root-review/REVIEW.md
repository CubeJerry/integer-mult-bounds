# Independent fixed-table bridge review

Accepted conditionally under the exact retained physical primitive and
record domain of the reviewed Toffoli bridge. No new complete kappa.

The author proof pinned by `check.py` is read as a proof, not inferred from
its finite tests. The Gray construction has one earlier-control toggle at
each of the 2^g vertices and one source load/unload at each cyclic edge.
Over F2 its output is the distributive expansion of the product of the g
true source bits. Each dirty control digit is its initial value plus either
zero or its selected source bit, so excluding initial B-1 digits suffices
for every load, irrespective of the order of Gray edges. The existing
four-update toggle and exact invariant-bad-stream repair apply unchanged.
This proves 6*2^g swaps and 5*2^g rotations for the low positions, with the
highest position separately implemented after a width-one exchange.

For fixed g the guard union bound is
n*((g+1)*2^-G+8*2^(G-K)) <= (2g+3)/(128p^3).
Descriptor setup remains polynomial, full records are charged, and the
g+2 complete reserved fields only change fixed constants. All gates finish
with those fields restored, so a finite sequence reuses them. The claim
requires the stated eventual layer domain; it does not provide a new global
compiler theorem or waive any foundational assumption.

The hypercube path word is a conjugated final-edge transposition. It exchanges
only the path endpoints. Cycle decomposition therefore constructs any fixed
h-bit permutation using the stated bound. Negative controls are explicit
translations and their inverses, with no clean ancilla. The phase formula
uses input coordinates; changing to output coordinates requires composition
with the inverse permutation. The absolute one-column phase scales by f.
These facts also give the actual physical inverse without treating a table
as a primitive. All fixed recipe constants and every different bit offset
remain chargeable in the eventual source invoice.

The independent checker imports no author code. It verifies 21,844 dirty
Gray identities through seven controls, all 2,667 transpositions through six
bits, 2,346 omitted-return negative controls, and 4,096 exact rational guard
bounds. The separate author tests include literal modular states and phases;
the Toffoli bridge already has an independent modular interpreter review.
These checks corroborate the uniform proof above.

Reproduce: `python3 check.py --source AUTHOR_PROOF --out output`.
Author proof SHA256:
`71383358c9b38e91f827932dda429c165fb0bce934b14b6da83e44f30efff98d`.
