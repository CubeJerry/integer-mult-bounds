# Independent review of the recoverable-encoder criterion

**Decision: ACCEPT after the explicit distinct-carrier and route-preparation clarifications. No source feasibility or new κ.** Reviewed author SHA256: `4c716975ebad0a89f49886f0c3bf770f1aa832143636f5dc4775e7e73f8474c0`.

The bridge reviewer independently checked the universal algebra, normalization, physical lowering and fee formula. The five small matrix controls use a separate exact elimination implementation; no author checker is imported. This is independent agent review, not formal-kernel verification or human peer review.

## Algebra and equivalence

The encoder changes only the raw donor, producing δ=q−ru while the common state remains at its actual original cut. Because all considered controls occur later, their response matrices apply to this same δ. A candidate observation evaluates to

\[
dF_0u+(dBc)(q-ru).
\]

Comparing coefficients of independent u and q gives exactly dBc=1 and dF₀=r. Neutrality Ac=0 is a separate retained premise, including every stated source guard. The local encoder and terminal recovery both exist precisely when r belongs to row(E)∩row(W_T); replacing intersection by a sum would be invalid.

With L spanning the annihilator of this intersection, the double-annihilator theorem gives dF₀∈R iff dF₀L=0. Thus all admissible d lie in the row span of Z_R, while all neutral c lie in the column span of K. Existence is equivalent to Z_RBK≠0. The stated block-rank excess identity follows by quotienting the observation space by im(F₀L), then restricting the control map to ker A. Matrix shapes must be preserved for zero-dimensional spaces; the exact controls cover those cases.

For a nonzero entry β, selecting d=Z_R's corresponding row and c=K's corresponding column divided by β gives unit signal. The resulting r=dF₀ has both required row representations. This avoids circularly assuming an encoder exists before the decoder is selected. The necessity and sufficiency are exact for this fixed one-encoder, one-donor, finite linear interface.

## Physical implementation and costs

The revised author explicitly requires distinct donor and receiver carriers, a still-unused receiver collection route, and separately charged preparation of the donor at the encoder. The donor's stationary δ records may use only its remaining funded itinerary; earlier consumed routes cannot be reused. The cochart encoder changes no common input, and receiver accumulators read each historical field only when it actually exists.

After common execution the endpoint response is supported at T. Correcting those endpoints with unchanged δ first and only then adding λ times the restored outputs into Q yields q. No γ condition or matrix inverse is needed. Owned records require real labels, storage, lifetimes and CLEARs. A zero-COPY guard belongs in A, while owned retirement is retained under the original contract.

The fee e+c₀+d₀+s+J+t+l counts encoder, controls, observations, donor snapshot copies, receiver collection, terminal corrections and donor recovery respectively. There are s+J INITs and CLEARs, no added MOVE in the displayed lowering, and separately charged input conversions and final recoupling. Fixed coefficients, including β⁻¹, require physical admission. The algebra does not establish a uniform supplier, precision theorem or recursive bound.

## Exact controls

The independent checker verifies five cases: the scalar example that is encoded-visible but additive-invisible; an encoder mode absent at the terminal; a recoverable sum requiring the nontrivial normalization β=2,c=1/2; a forbidden nonneutral pulse; and a zero-response observation. It checks row-space intersection membership, the projected rank identity and the actual normalized equations. Negative controls identify the false union-of-row-spaces replacement, omission of Ac=0, zero signal, wrong normalization and the additive scalar case.

Normal and optimized runs agree. These finite controls support the reviewed universal proof; they are not extrapolated native feasibility tests. No generalized-R source search has been performed or certified by this review.

Credit: S004 orchestrator as author; S004 bridge worker as independent reviewer for @CubeJerry; OpenAI assistance disclosed.
