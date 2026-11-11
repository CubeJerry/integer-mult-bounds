# Independent review of the endpoint-history feedback proposition

**Accept as a universal theorem for the stated fixed-word interface.**
Reviewed by the S005 adversarial worker for @CubeJerry with OpenAI assistance.
This is independent mathematical review, not human or formal-kernel acceptance.

The reviewed draft is `s005-root/causal-feedback/PROOF-DRAFT.md`. Its conclusion
follows from an exact substitution identity, not a restriction to preselected
linear controls. For each actual execution, assign to every permitted slot
the sum of the increments actually written there. A fixed finite linear word
then has terminal and observation differences `Aw` and `Bw`, regardless of
how those realized increments were computed. If `B = L A` and `Aw = 0`,
then `Bw = 0`. Choosing `w` through feedback, arbitrary nonlinear functions,
or coordinate-mixing maps does not change that identity.

The receiver impossibility statement correctly fixes the common input and
all receiver side data independent of the required donor coordinate, then
varies that coordinate. The complete record is identical, so no deterministic
or exact randomized decoder can recover it on all inputs. Randomness, if
allowed, can be fixed in the comparison; no probabilistic lower bound is
being claimed.

The quotient-certificate reduction is also correct. Baseline-spanning decoder
rows together with a complete left-nullspace basis span the full observation
coefficient space. Each must have a response factorization. Equality of
baseline rows alone never establishes response stability; the draft explicitly
requires the missing identities instead of silently asserting them.

## Scope requirements checked

1. Native event order, MOVE routes, observation times and original field
   lifetimes are fixed. An intervention at an unlisted chart is a changed
   interface, even when its scalar cost is small.
2. An original scalar step may be replaced by an arbitrary local computation
   only when its net difference can be applied at admitted slots, preserving
   source typing and any retained guard. Added writes cannot secretly move a
   field or change the receiver's available history.
3. New local records can choose interventions. They cannot carry additional
   data to the receiver except through the modeled histories. An extra
   correlated receiver input is explicitly excluded.
4. Vector fields of any positive dimension are covered by tensoring the scalar
   response matrices with identity. The actual control functions themselves
   need not act coordinatewise.
5. Endpoint preservation is a complete hypothesis of the argument, not a
   consequence of a local decoding identity. A demonstration with nonzero
   off-terminal endpoint error does not contradict the theorem.

The source rank-one invariant, if independently authenticated, permits the
especially strong choice of A consisting only of final common role189's
perturbation. It would make every native receiver arrival insensitive when
that single endpoint is restored. No assumption about terminal recoverability,
number of encoders, or linearity of their chosen increments is then needed.

The theorem does not exclude a route with an extra chart, new receiver access,
changed unadmitted processing, or a different native word. It provides no
multiplication lower bound and no new kappa.
