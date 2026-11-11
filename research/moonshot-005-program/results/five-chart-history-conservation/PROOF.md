# A rank-one endpoint law for every receiver history

**Proved for the pinned finite source and the stated all-volume control
interface. No new multiplication exponent.** This excludes a larger class
than the preceding single-encoder and unchanged-q tests.

## Statement

Fix `research/shared-wire-split-composition/data/final.json.gz`, compressed
SHA256 `2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883`.
The native has 71,261 scalar instructions and 1,480 arbitrary common input
fields. Charts are identified by their complete binary spans.

Let C be the five original donor77 station spaces, represented by frame
IDs 71,312,324,232,127. Let R be the receiver189 itinerary, with frame IDs
3,307,901,198. These space sets are disjoint. Retain the native MOVE
calendar and all native common instructions, but allow any finite collection
of extra increments to any live common field at a chart in C, at any cut.
Each increment may be any field value, chosen jointly or from previous
common values, raw differences, local records or feedback. No independence,
linearity or unchanged-q-zero baseline is required of the controller.

Give the receiver its entire native history: every initially present field,
every native MOVE arrival at any chart in R, and all intermediate local
values. Do not give it a new controller-produced transport or an additional
q-bearing side channel. Outside C the common computation remains the native.

Compare this execution with the original native execution on the same
common inputs. For each of the 19 native MOVE arrivals, let Delta h_i be
its changed value. Let Delta y be the change in final common field189.
The source certificate proves

`Delta h_i = rho_i Delta y`

for every field volume V and all allowed increments. The coefficients are
zero for 16 arrivals and -1,-1/4,1/2 for the remaining three. The exact
event/role/chart mapping is `CERTIFICATE.json`.

Consequently **restoring common endpoint189 alone forces the receiver's
entire native history to be unchanged**. This includes all 1,046 initial
observations and all intermediate local values. Requiring the other common
endpoints, COPY guards, ownership and cost contracts only restricts the
candidate executions further.

## Direct timed adjoint certificate

For each arrival i, form the timed output functional

`L_i = arrival_i - rho_i * final_common189`.

Propagate this functional backwards through the original common word,
adding the arrival's unit impulse at its actual post-MOVE cut. The verifier
checks that at every cut its coefficient on every live common field in C
is zero. It checks actual role locations and compares chart spaces, so a
frame alias is not treated as a new source of access.

An ADD changes only the adjoint on its source. SCALE changes its
destination. COPY changes source and destination, MOVE changes location,
and INIT/CLEAR change the owned lifetime. Checking every changed entry
therefore maintains the all-stations-zero invariant across every cut.
The proof is not a finite search over controller choices: the symbolic
adjoint vanishes at every possible intervention position.

Adding any vector v at a permitted position changes L_i by zero times v.
By superposition of the native linear evolution, every finite set of
increments leaves L_i unchanged. This proves Delta h_i=rho_i Delta y.
The baseline value of L_i need not be zero and is not assumed to be zero.

The certificate is scalar, but the native acts coordinatewise. Tensoring
with the V-dimensional identity proves the same statement for all admitted
field volumes and for arbitrary coordinate-mixing controller increments.
The source COPY-zero restriction is not needed for this obstruction:
linear overwrite semantics only enlarge the permitted trajectories.

## Feedback and replacement encoders

An increment may depend on all earlier perturbed states. For any completed
trajectory, its actual sequence of increment values is still a finite
sequence to which the preceding identity applies. The zero adjoint does
not require those values to be selected in advance or to be independent
of the common input. A locally replaced update can also be represented by
the difference between its actual new value and the original update,
provided the replacement changes only a live field at a permitted chart
and retains the outside native chronology and lifetimes.

This covers single or multiple common-mode encoders and arbitrary local
feedback within the stated access set. It does not cover recoding the
outside native, moving controls or helper fields along new routes,
introducing an observed extra carrier, or changing the receiver access.

## Complete histories and indistinguishability

Initial receiver observations are unaffected, because the two chart sets
are disjoint. Between arrivals, native ADD/COPY/SCALE operations combine
fields already at the receiver chart, INIT adds zero and CLEAR removes a
field. There are no permitted controllers there. Induction therefore
extends equality of the initial/arrival records to every intermediate
native receiver value.

If endpoint189 is restored, choose two executions with the same common
input u and same receiver-private data but different raw donor q77. Both
receiver histories equal the native history on u. They are identical,
so no decoder using this interface can recover the independently varying
q77. This remains true for nonlinear decoders. The conclusion is a scoped
information obstruction, not a global lower bound on multiplication.

## Verification and controls

The author verifier authenticates the source, every donor/receiver chart,
the complete observation census, all 19 timed adjoints and a source-input77
positive control. This input perturbation produces unit final189 response
and the three nonzero listed arrival responses, demonstrating why endpoint
restoration is a necessary premise.

Changing a nonzero rho coefficient is rejected. Adding controls at chart8
also breaks the adjoint invariant. A separate exploratory unit pulse into
role1139 immediately before event35613 at chart8 changes arrival
(37192,1145,901) while leaving final common189 unchanged; its required
physical access and encodable/recoverable common mode are not supplied by
this obstruction package.

Independent source/adjoint review is recorded separately. It does not
import the author extractor. No human or formal-kernel acceptance is claimed.

## Implication and next questions

The first encoder cut and later quotient-surviving cuts are all excluded
within the original five donor stations, without separately testing their
local mode intersections. Any successful repair must change access,
outside processing, the observation interface or the native geometry.
Expanded 220-station algebraic searches do have nonzero neutral gains;
they are not excluded by this theorem and are not physical constructions.

The next useful task is an actual source mode and complete paid access
schedule for such a broader channel, with arbitrary dirty-input
restoration and all ordinary/lifetime costs. One channel alone would not
meet the whole shared-native, supplier or outer theorem obligations.

Prepared for @CubeJerry by the persistent programme's S005 mathematical
bridge worker with substantial OpenAI assistance. Credit the native and
shared-wire construction lineage, prior additive-history and stable-history
packages, and the construction and adversarial workers' source reductions.
The retained five foundational assumptions are unchanged.
