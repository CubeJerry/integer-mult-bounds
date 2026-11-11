# Independent full-input review of initial-helper annihilation

**Verdict: accept the precise source-specific statement. No new kappa.**
The S004 orchestrator reviewed the adversarial worker's revised proof and exact
certificate. Their hashes are fixed in REVIEWED-FILES.json and in review.py.
The common native chronology remains fixed; the generous retiming applies to
donor/receiver access and decoder observations, not to an arbitrary changed
common word. This clarification was requested before admission.

## Independent reconstruction

The reviewer wrote a fresh implementation using all 1,480 independent public
input coordinates, rather than the author's 45 selected helper columns and
reverse endpoint adjoints. It executes every source ADD/SCALE/COPY exactly,
checks the unique COPY destination is zero on all inputs, tracks physical
charts and owned lifetimes, and verifies all 1,080 arbitrary helper inputs are
restored and all main endpoints are independent of them. Binary chart spaces
are compared as explicit span sets rather than reduced basis representatives.

For each chart the implementation unions the supports of every actual field
row ever observed there. No Gaussian elimination or author/predecessor verifier
is imported. This stronger support check independently establishes that the
eligible helper columns never occur in any relevant receiver history. It
reconstructs and matches all 200 donor helper sets and all 104 exact required
endpoint dependencies in the proposed certificate. There are 45 eligible helper
inputs in total and 88 nonempty donor sets, but only 46 required pairs with
nonempty helper sets; the other 58 required pairs have empty sets.

Both normal and optimized executions agree byte for byte. The three controls
show that the actual required main-input signal is present, adding the terminal
chart to receiver access exposes every eligible helper input, and one artificial
helper-column injection destroys the claimed annihilation.

## Mathematical argument and scope

An exact zero coefficient in every native history row stays zero in every
linear combination of those rows. Thus the claimed local-history subspace has
zero projection onto the donor's eligible initial-helper subspace. For every
admitted field volume V, the same coefficients act on all coordinates, so the
zero map remains zero. Indeed an arbitrary change confined to those helper
inputs cannot affect these observations; the conclusion does not depend on a
finite random input test or on failure of a decoder search.

Granting all histories simultaneously over the receiver's whole original
itinerary is stronger than any causal observation schedule on that route.
Consequently no initial-helper-only substitution in this specified interface
can deliver the required independent donor signal. Unpriced raw-input access,
new receiver charts, changes to the common native or injections into helper
states during execution are outside the theorem. Its conclusion must not be
used as a global obstruction to active-helper coding.

The theorem closes the initial-helper proposal. It does not invalidate the
newer two-ADD difference-carrier construction interface. That later interface
stores q-h in the raw donor and uses midrun injections; its endpoint restoration
and possible source witnesses require separate proofs. No new supplier,
compiled price or complete multiplication bound follows from this review.

## Reproduction

From repository root:

```sh
P=research/moonshot-005-program/results/initial-helper-annihilation
python -B "$P/review/review.py" --repository . --packet "$P" --output /tmp/helper-annihilation-review.json
python -O -B "$P/review/review.py" --repository . --packet "$P" --output /tmp/helper-annihilation-review-opt.json
cmp /tmp/helper-annihilation-review.json /tmp/helper-annihilation-review-opt.json
```

Expected PASS_INDEPENDENT_FULL_INPUT_HELPER_ANNIHILATION. The separate agent
review and exact full-input computation are not formal-kernel checking or
human peer review. Prepared for @CubeJerry by the S004 orchestrator with
OpenAI assistance; the author and predecessor constructions retain credit.
