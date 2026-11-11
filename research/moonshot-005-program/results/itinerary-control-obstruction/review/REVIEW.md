# Independent review of the 103 prescribed-pulse obstructions

The S004 orchestrator independently checked the proof and wrote `review.py`
without importing the author verifier or any exploratory search routine.
The source SHA256 and the exact reviewed proof/certificate are pinned.

## Mathematical review

Each certificate supplies an off-terminal endpoint functional with pulse
response one and zero response at every permitted subsequent control position.
The resulting identity is `ell(endpoint error)=delta`, or `c delta` for a
nonzero rescaling. Thus restoration for all inputs is impossible in precisely
the stated interface. Tensoring by the identity covers arbitrary field volume;
zero scalar adjoints also annihilate arbitrary coordinate-linear controls and
linear feedback. Ignoring COPY's zero-destination guard enlarges the model and
does not weaken the negative result. The argument is complete for the explicit
103 cases, and is not a claim of completeness of either exploratory screen.

The initial pulse is prescribed. Controls on other fields at that cut can be
commuted past the departing MOVE, while cancelling the pulse on the departing
helper itself would remove the proposed signal. Jointly selected earlier
pulses, additional stations, and changes to the native common operations are
outside the theorem. The positive control below verifies one such boundary.

## Independent source check

The author checks changed adjoints/locations while walking backward. This
review instead first builds all forward location/lifetime intervals, then
builds piecewise-constant reverse adjoint intervals for the 33 distinct final
functionals. A separate offline interval join tests every future cut of every
live common role at every permitted donor station. It checks all 103 distinct
event/donor pairs at 58 helper departures, authentic source geometry, off-hub
endpoint support, and unit pulse response. Binary frames are identified by
explicit spans, not frame indices.

For every case, adding the actual departure destination to the station set
creates a nonzero adjoint intersection. This is a meaningful negative control
for the allowed-station premise. Source and author pins are checked before any
calculation. Normal and optimized Python receipts agree byte for byte; explicit
exceptions, rather than assertions, enforce the checks.

From the repository root:

```sh
python3 -B research/moonshot-005-program/results/itinerary-control-obstruction/review/review.py --repository . --packet research/moonshot-005-program/results/itinerary-control-obstruction --output /tmp/itinerary-review.json
python3 -O -B research/moonshot-005-program/results/itinerary-control-obstruction/review/review.py --repository . --packet research/moonshot-005-program/results/itinerary-control-obstruction --output /tmp/itinerary-review-opt.json
```

Expected status: `PASS_INDEPENDENT_INTERVAL_JOIN_103_PULSE_DUALS`.
This is independent model-assisted mathematical and implementation review,
not human peer review or formal-kernel certification. No new kappa.
