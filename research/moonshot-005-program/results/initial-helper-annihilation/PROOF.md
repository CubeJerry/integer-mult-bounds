# Initial helper modes are invisible on every required receiver itinerary

**Proved source-specific obstruction. No new κ.** This result tests the
initial-helper substitution repair proposed after the terminal and static
history obstructions. It does not apply to midrun helper-state replacement.

## 1. Exact statement

Use the native word
`research/shared-wire-split-composition/data/final.json.gz`, SHA256
`2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883`.
Identify chart aliases by their full binary spans. The word has 1,480 public
inputs, 400 main roles, 1,080 public helpers and 71,261 instructions. A
nonentry main starts outside the zero chart 3; an entry main starts at 3.
There are 200 of each. Every occurrence and index below is source-specific.

For a main role i, let I_i be every chart on its entire original main MOVE
itinerary, including its initial and final charts. For each nonentry donor X,
define

\[
H_X=\{h:\ h\text{ is a public helper},\quad
       \operatorname{initial}(h)\in I_X,\quad
       \operatorname{final}(h)=127\}.
\]

Thus H_X includes all helpers initially accessible anywhere on the donor's
route, not only helpers starting at the donor's initial chart. The final
chart condition is the proposed zero-extra-MOVE restoration interface.
There are 45 helper inputs in the union of these sets. Eighty-eight donors
have nonempty sets, of size at most nine.

Let W be the native linear map from all 1,480 independent public inputs to
its public endpoints. A *required pair* (X,Y) consists of a nonentry donor X
and entry receiver Y with W[Y,X] nonzero. Exact source adjoints give 104
required pairs. Fifty-eight have H_X empty. The other 46 are the nontrivial
cases below; these are not 88 nontrivial receiver tests.

Let L_Y be the linear span of **all** actual native field rows observed at
**any** chart in I_Y, over the whole execution and on all public or live
owned roles. The histories are granted simultaneously, with all observation
clocks, donor/receiver route ordering, storage and decoder costs waived.
The common native's own instruction order and chart itinerary stay fixed;
the theorem does not assert invariance under reordering its operations.

**Theorem.** For every required pair (X,Y), every row in L_Y has zero
coefficient on every input in H_X. In particular,

\[
L_Y\big|_{H_X}=0,
\qquad
L_Y\cap\operatorname{span}\{e_h:h\in H_X\}=\{0\}.
\]

The first assertion is stronger than the second: there is no hidden helper
signal that might be separated by cancelling common-input noise. None of
these particular helper input columns appears in the receiver history.

Consequently, for every admitted complete-field volume V and arbitrary
independent common input, changing only the helper inputs in H_X leaves every
native history observable on I_Y unchanged. Arbitrary initial helper
encodings of a new independent q_X therefore cannot communicate q_X to Y
through this observation interface. This remains true if the receiver
accumulates observations while moving along its whole itinerary: granting
every historical observation without time restrictions is already stronger.

## 2. Source certificate

`CERTIFICATE.json` records all 200 donor helper sets, all 104 actual endpoint
dependencies, and the original donor/receiver itineraries and checked state
counts for the 46 nonempty cases. All comparisons use canonical chart
spaces, while the file retains source chart representatives for inspection.

The verifier identifies the endpoint dependencies by fresh exact reverse
adjoints. It independently propagates the 45 eligible initial helper columns
forward through the entire native word. Each field row is an exact sparse
rational vector on those 45 inputs. At initialization, row h is e_h for an
eligible helper, and every other row is zero on these columns. Each ADD,
SCALE and COPY applies its exact coefficient; INIT produces zero; CLEAR
retires the owned row; MOVE changes the chart and preserves the represented
linear value. COPY is assignment, not addition.

Every initial field state and every new destination state after a source
instruction is checked. When a state is at a chart on I_Y, all its H_X
coefficients must vanish for every relevant required pair. Values persisting
between instructions do not produce new rows or chart locations, so this
checks every actual historical field row. The verifier also checks source
MOVE positions, cochart ADDs and final public charts.

The fifty-eight empty-H_X cases are immediate. Exact propagation verifies
the other 46 cases. Linear combinations of rows with zero H_X projection
also have zero projection, proving both displayed identities for L_Y. This
is an exhaustive certificate of a finite pinned source statement, not an
inference from a sample of inputs or a failed parameter search.

## 3. All field volumes and the substitution interface

For an admitted field volume V, the same source coefficients act on complete
fields. A source coefficient zero becomes the zero map on all V coordinates.
Changing initial helper fields by arbitrary coordinate vectors therefore
changes none of the receiver's native historical fields. Arbitrary mixing of
those observations, caching, donor/receiver access retiming and linear
decoding cannot recover an
independent donor value that has no effect on the observations. The argument
does not require an estimate of the decoder's arithmetic cost.

The proposed initial-helper primitive encodes q_X by signed swaps and local
subtractions into one or more helpers initially accessible along I_X, runs
the original common native, decodes a helper-input form on I_Y, and restores
all changed helpers and the donor at chart127. The theorem grants the
initial encoding and final restoration for free. Its necessary decoding
condition still fails, even when every helper in H_X is available and every
historical receiver row is granted simultaneously. It therefore rules out
this entire stated initial-helper channel family for all 104 required pairs.

The claim concerns information supplied by that channel. Other independent
raw donor access, a change to native operations, additional receiver chart
access, or a helper mode first injected **during** the native execution are
different interfaces. In particular a midrun unit perturbation of a helper
state need not be the forward image of its initial helper input. Such a
perturbation can have a different later response, so this theorem does not
rule out the proposed midrun endpoint-restored swap.

## 4. Two concrete controls

**Actual main-input perturbation.** For the first nontrivial required pair,
the verifier identifies the nonzero native coefficient from X to Y, while
the eligible helper coefficients remain zero. Treating the common main
input as a freely replaceable helper would change a required common endpoint
and invalidate the theorem's helper-only premise. This control verifies that
the observed zero columns are specific to the eligible helper modes, not a
claim that the receiver is independent of all source data.

**Changed geometric access.** Donor41/receiver153 has nine eligible helper
inputs. Exact full-input adjoints show that each of their final helper rows
is its original input coordinate, all at chart127. Granting those final rows
to the receiver exposes nine independent helper modes. Chart127 is absent
from the receiver's itinerary; giving it that access is an actual change of
geometry, not a free decoder implementation. This control makes the claimed
access restriction testable and demonstrates the boundary of the result.

## 5. Programme consequence and limitations

The static history theorem requires at least 36 informative nonquiet helper
crossing units from original operations if no more than eight new paid
complete fields fit the current optimistic price. The construction explored
here sought to supply such traffic by encoding q into initial dirty helpers
and restoring them at the terminal hub. The zero-column result closes this
particular escape, including multi-helper initial forms and itinerant
receiver decoders.

The next viable question is whether a midrun helper-state replacement can
deliver useful information and have its entire common-state disturbance
repaired at the hub. That has a different suffix response and a causal
restoration obligation. Neither an informative route nor a restoration
construction is supplied by this negative theorem. The
subsequent two-ADD difference escrow stores each perturbation directly and
permits reverse chronological donor restoration; it does not require an
invertible repair matrix.

No Gaussian saving, complete native, uniform supplier, foundational
assumption, or new multiplication exponent is established. Credit belongs
to the predecessor endpoint and initial-loan investigations and the S004
bridge worker for the candidate substitution interface. The all-history
initial-column annihilation theorem and exact certificate were prepared for
@CubeJerry by the S004 adversarial worker with OpenAI assistance. Independent
review is recorded separately before programme admission.
