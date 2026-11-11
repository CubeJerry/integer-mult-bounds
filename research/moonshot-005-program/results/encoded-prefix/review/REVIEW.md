# Independent review of the changed-main prefix and safe retirement

**Outcome:** the corrected 25,728-event prefix and 26,226-event retirement
extension pass a separately implemented exact typed replay on all1,880 inputs.
The retirement criterion is sufficient. No H4 native or new kappa is proved;
all five global assumptions remain.

`review_prefix.py` imports no author compiler/verifier. It interprets every
physical instruction on1,480 independent first-copy inputs and400 independent
second-main inputs. Both virtual copies use the SAME arbitrary1,080 entering
helpers; the physical verification does not set helpers to zero. It independently
checks each first-copy source instruction and replays the original prefix,
comparing all1,531 first-copy roles (including51 owned labels). At the cut it
checks all current physical observations and every one of the1,480 virtual
decoders as exact1,880-column rational rows. All live/cochart/INIT/COPY/SCALE/
CLEAR/MOVE guards, including actual private/public ownership, are checked.

| Result | Primary | Retirement extension |
|---|---:|---:|
| Source cut |25728|26226|
| Physical operations |26167|27312|
| Current observations |411|487|
| Extra paid profile |8rank1+1rank2|86rank1+6rank2|
| Combined active owned peak |11|87|
| Owned lifetimes |11|120|
| Independently checked dirty CLEARs |0|33|

Primary decompressed JSON SHA256:
`e019602e31b3913d30b2688b4e841d34faf89faff0a9ce932327abeb78698d5e`.
Retirement decompressed JSON SHA256:
`c39e2429da49be9654407fbe89fcded1b3306aa18ca974e74bfe1124ac642ab1`.
The mathematical receipt does not depend on gzip header/library details.

## Ownership correction found during review

The initial compiler incorrectly copied an original PUBLIC helper MOVE's
ownership flag to its new PRIVATE difference carrier. Selected-source grammar
requires the flag to agree with the actual physical owner's private/public
status. The author fixed new difference-delivery flags to private, added the
guard, and regenerated both transcripts and receipts. The corrected payloads
above pass the independent checker. Child ranks/moments are unchanged, but
private rising routes still require a fresh physical tariff. The earlier
untyped transcripts are not the reviewed scientific artifacts.

## Retirement proof and independent checking

At chart f, let V_f span current virtual differences of ALL live source roles,
and O_f span actual live physical difference observations. The invariant is
V_f contained in O_f, with the first-copy source state preserved separately.
Deleting an observation is sufficient when all of V_f remains spanned by the
other current observations. Every virtual state remains cochart-decodable;
future scalar updates stay in the chart's span, while future MOVEs must satisfy
the independently charged delivery/rebase rule. The removed value need not be
zero. Decoders must be recomputed, not truncated blindly.

Checking only mains would be unsound: all main differences can be zero while a
live helper still needs a nonzero row. Source-owned roles likewise count. The
reviewer reconstructs the actual physical matrix BEFORE each of33 CLEARs, forms
the remaining observation span using primitive-integer maximum-pivot elimination,
and checks EVERY current virtual row at that chart. No author safe/unsafe label
is trusted. The complete retirement timeline agrees with the author; each row's
receipt records the source event, owner, chart and number of checked virtual
roles. The active peak counts actual owned lifetimes including temporary
snapshots and source-owned fields, not only persistent cache entries.

Dirty CLEAR still inherits `owned_erasure`. No zero-CLEAR implementation or
free physical erasure is inferred. Sufficiency does not imply necessity or an
optimal retirement rule.

## Cost, continuation, and scope

The independent physical interpretation reproduces both added MOVE histograms.
The extension spends approximately97.9584831539344; its next rank-one payment
under the same chosen history exceeds the exact H4 allowance below98.399076951.
That is a valid stopping test for THIS constructed rule, not for all changed
main codes or other payload choices. Its87-live geometry also cannot inherit
the original43-live compiler. The primitive-integer rank checks prove exact
source facts; normalized identities tensor with I_V under the inherited chart
semantics, not a newly proved native all-column or precision/tape theorem.

Neither prefix completes its endpoint decode, retirement, physical tariff,
source/control movement, uniform compiler or BIT supplier. They remain useful
positive finite prefixes. A weaker demand-only continuation need not retain
all current virtual roles and is a different, unreviewed invariant here.

## Reproduce

Run `review_prefix.py --source SOURCE --transcript PREFIX --author-receipt RESULT`.
The same command passes under Python `-O`; guards use explicit exceptions.
`PREFIX-REVIEW.json` and `RETIRED-PREFIX-REVIEW.json` retain all counts and every
retirement record. Source SHA256:
`2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883`.

Prepared for @CubeJerry with substantial OpenAI assistance. Independent model-
assisted reconstruction is not human or proof-assistant acceptance. Credit the
retained selected native and the author of the changed-main construction.
