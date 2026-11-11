# Exact dual obstructions to 103 proposed itinerary-controlled helper pulses

**Classification: proved for the explicitly certified source/case family under the retained linear typed-field model. No new κ.**

This result excludes a particular way of completing candidate helper loans.
It does not exclude all helper encodings, all historical decoders, jointly
designed initial pulses, or controls at additional charts.

## Source and quantified contract

Use the native word `research/shared-wire-split-composition/data/final.json.gz`,
compressed SHA256
`2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883`.
Identify frame aliases by their binary span. Let H be full chart127.
Every public common input is arbitrary, and a field has arbitrary admitted
volume V over a characteristic-zero coefficient field.

The certificate contains 103 distinct pairs `(departure event, raw donor)`
at 58 native public-helper MOVE occurrences. For each pair, let j be the
departing helper, X the donor, and A→B its actual source MOVE. The source
chart A lies on X's original main itinerary, whose endpoint is H. Let
P_X be the suffix of that itinerary beginning at A, including A and H.

Immediately before this MOVE, change the helper by an independent field
perturbation δ, or by any nonzero fixed scalar multiple of δ. Keep the
remaining common computation equal to the original native word, except
that at every later cut the implementation may add arbitrary field values
to any live common role whose chart is in P_X. It may use stationary δ
snapshots at every such chart, unlimited local storage and additions,
arbitrary coordinate mixing, feedback, and arbitrary terminal corrections
at H. These are deliberately generous grants. Existing common values may
also be used in the added controls; restriction to zero common input leaves
an arbitrary linear δ-dependent control field at each permitted position.

**For each certified pair, no such continuation restores all common
endpoints outside H for every δ.** Therefore it cannot complete the full
common-restoration contract, independently of which receiver decoder is
chosen.

The controls need not be individually neutral. The theorem permits their
joint cancellation across all future source cuts. The initial departing
helper pulse remains prescribed; admitting a compensating pulse on that
same helper before its departure would remove the signal before it is
exported and is not the proposed loan. Other same-chart compensators at
that cut are covered: after the helper departs, those roles remain at A
with the same suffix response.

## Three-term-or-shorter dual witnesses

For each case, `CERTIFICATE.json` gives a linear functional ℓ of at most
three final public common fields outside H. All coefficients are exact
rationals. Reverse propagation of ℓ through the actual suffix has two
properties:

1. Its coefficient on every live common role at every permitted future
   station/control cut is zero.
2. Immediately after the selected MOVE, its coefficient on the departing
   helper is exactly one.

Neither property uses a COPY-zero guard as an output observable. The
certificate therefore remains valid in the stronger relaxed linear model
that lets native COPY overwrite a nonzero destination. Enforcing the real
COPY-zero rule cannot create a solution.

Let Y be the final common output of any candidate continuation, and E(u)
the required native output for the original common input u. By linearity
and the standard impulse-response identity, the initial pulse contributes
δ to ℓ(Y−E(u)). Every later added control contributes zero, by property1.
Thus

\[
\ell\bigl(Y-E(u)\bigr)=\delta.
\]

For nonzero δ, some common endpoint outside H is incorrect. A terminal
correction at H cannot alter ℓ, since ℓ is supported entirely outside H.
For a pulse cδ the residual is cδ, so rescaling a historical decoder's
nonzero sensitivity does not cure the obstruction.

The argument holds for all V: tensor the scalar source adjoints with the
identity on the V field coordinates. Each allowed control may itself use
an arbitrary V-by-V linear map, because its scalar adjoint coefficient is
zero. It also covers linear feedback: whatever field the controller adds
at a permitted cut, its contribution to ℓ is zero. No finite input sample
or asymptotic extrapolation is used.

## Why the verifier covers every future control cut

The verifier starts at the final state with the displayed ℓ and checks
that every live role in P_X has adjoint zero. It then walks backwards
through every instruction after the selected departure. An ADD can change
only the adjoint on its source; SCALE changes only its destination;
COPY changes its source and destination; MOVE changes one role's chart;
INIT/CLEAR change one role's lifetime. The verifier checks every changed
adjoint or location. By induction, all unchanged permitted roles retain
zero adjoint too. This is an exhaustive symbolic check of all future
control positions, not a search over a selected finite set of controllers.

At the cut immediately after departure, the helper has chart B and
adjoint one. Its location is checked against the literal source MOVE.
The verifier also authenticates donor access to A, the remaining donor
itinerary, final chart H, public-helper ownership, and the source hash.
It imports no search code or predecessor verifier.

## Exact scope of the selected cases

The 103 cases are the union of two session screens: 89 donor/loan pairs
from 44 hub-observable direct-relay candidates, and the 31 cases whose
particular source-derived historical decoder has nonzero pulse response.
Seventeen pairs overlap. The certificate's explicit case list, rather
than a claim of global completeness for either exploratory screen, is
the theorem's domain. All31 chosen nonzero-decoder cases are included.

The result does not rule out alternative initial pulses designed jointly
across different cuts, arbitrary changes to the native common operations
away from P_X, acquisition of δ at additional destination stations, new
geometric routes, or another decoder/caller interface. In particular,
fully joint additive modulation from time0 is a different problem. The
separate same-cut neutral-kernel investigation also has different premises.

## Controls and credit

Granting a new stationary δ cache at the selected destination B breaks
the adjoint-zero premise: the departing helper's coefficient there is
one. A control that erases the initial pulse likewise fails the certified
nonzero-response premise. These controls identify actual ways to change
the interface, without declaring them free physical services.

The source and earlier endpoint/quiet-route work are credited to the
native authors and @CubeJerry's persistent programme. The S004 bridge
worker supplied the nonzero historical-decoder candidates; the
construction worker searched the control spans, extracted these short
duals, and wrote the separate exhaustive adjoint verifier. OpenAI
assistance is disclosed. Independent review, when completed, is recorded
separately. This establishes no complete multiplication bound and removes
none of the foundational assumptions.
