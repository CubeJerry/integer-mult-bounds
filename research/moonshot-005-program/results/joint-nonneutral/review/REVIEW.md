# Independent review: joint responses at 58 prescribed helper departures

**Status: accepted within the fixed-source control class stated below. No new κ.**

This is a fresh S006 review. The checker imports no construction-author code. It
reconstructs departure payloads and historical decoder identities by a complete
1480-variable forward replay, then obtains the joint intervention matrices by a
single backward pass of timed observation and final endpoint adjoints. This is
different from the author's 58 simultaneous forward formal impulses. All
coefficients and ranks use exact rational arithmetic.

## Precise source result

Fix the pinned native instruction word and the 58 distinct `(event, helper)`
cuts in the pinned predecessor case certificate. At cut k, add an arbitrary
complete-field increment δ_k to that public helper immediately before its MOVE.
Make no other change to the common instruction word or its initial common
inputs. Let Z map these increments to the differences at the 458 public final
outputs whose final space is not the full nine-dimensional hub.

The source response matrix Z has column rank **58**. Every corresponding COPY
zero-guard response vanishes. Thus, over any characteristic-zero field and at
every block volume V, `(Z ⊗ I_V)δ = 0` implies `δ = 0`.

In particular, exact restoration of those 458 endpoints forces every selected
increment to vanish. This conclusion remains valid when the realized increments
are arbitrary functions of the common input, raw data, earlier observations, or
earlier increments: fix one execution and apply the injective linear response
map to its realized increment tuple. No assumption that the control policy itself
is linear is needed. The native processing between the selected increments must
remain the fixed pinned word, and any additional output correction is outside
this assertion.

The independently verified restricted column ranks are:

| Selected family | Number of columns | Offhub response rank |
| --- | ---: | ---: |
| All prescribed departure cuts | 58 | 58 |
| The 31 previously admitted historical observers | 31 | 31 |
| All selected cuts whose baseline payload is one active donor coordinate | 30 | 30 |
| Admitted observers with such a unit donor payload | 17 | 17 |

The 31 admitted observer donors are distinct. The 30 unit payload donor
coordinates are also distinct. The complete 58-cut list does **not** define 58
distinct donor signals: it includes repeated donors and some cuts eligible for
more than one donor. No claim of 58 independent raw demands is made.

## The chronological encoder and the old decoder mismatch

Let H_i u be the baseline helper value at selected cut i. Let L be the strictly
lower triangular matrix whose entry L_ij is the response at that helper to an
earlier unit increment at cut j. The independent backward adjoints reproduce
every entry of L, and the forward replay independently reproduces every H_i.

For the 31 selected cases, an update

\[
 h_i\leftarrow h_i+g_i(q_i-h_i)
\]

adds an increment satisfying

\[
 T\delta=q-Hu,
 \qquad T=\operatorname{diag}(1/g_i)+L.
\]

The nonzero gains are exactly the source gains 1, 2 and −2. In particular, the
pure-overwrite convention `T=I+L` cannot silently be used for this family. The
chronological T is invertible because it is triangular with nonzero diagonal.

Write B for the perturbation response of the 31 predecessor historical decoder
functionals. Each baseline functional is exactly H_i u. The checker verifies
this as a full rational row identity and verifies every listed observation as a
literal accessible initial field or post-MOVE arrival at its stated chart.
For a joint intervention, these old functionals return

\[
 Hu+B\delta=q+(B-T)\delta.
\]

The exact rank of `B−T` is **30**. Thus the previously proved individual
historical decoders do not compose unchanged on 31 independent raw donor
inputs. For any fixed common input, variation of those 31 raw inputs makes δ
range over the full 31-dimensional control space, so the mismatch is a real
uniform-input failure, not merely an incompatible choice of notation.

This statement permits alternative decoders, receiver side information, a
restricted correlated donor family, or a changed common processing word. It
does not rule them out.

The source facts in the author's separate unit-17 continuation paragraph were
also independently checked: B17 has rank 14, T17 is invertible, and
`I−B17 T17^{-1}` has rank 16 (equivalently, T17−B17 has rank 16). All 17 encoder
cuts are on their donor's initial rank-one chart, and all their offhub response
roles have original common inputs at chart 3. These facts support a new initial
precompensation investigation; they do not establish that investigation's full
physical protocol or price.

## What the rank result does and does not price

For a selected m-column family with distinct independent raw donors, the
q-dependent part of the endpoint debt has the form `Z_I T^{-1}q` and has rank m.
Invertible chronological mixing and a change among nonzero gains cannot reduce
that rank. If the entire debt must factor through r shared linear field records
and recipients have no other q-dependent information, rank factorization forces
r ≥ m. In particular, an eight-record factorization of the entire 30- or
31-dimensional debt is unavailable under that extra information restriction.

This is **not** a general m-message lower bound. Local side information,
different recipients, existing routes, broadcasts, other source controls,
initial common precompensation, or retained raw carriers can change the relevant
communication problem. The rank-17 subfamily alone does not contradict a
remaining allowance of 19 rank-one calls. No complete invoice or target exponent
is inferred from these ranks.

Initial precompensation is specifically outside the fixed-input premise above.
If a new architecture arranges `F_off V Kq + Zδ = 0`, it has added a second
endpoint response map and must be tested as that new joint construction. The
58-column injectivity result cannot be reused to discard the compensating term.

## Independent checks and negative controls

The independent checker verifies all source operation charts, ownership tags,
strict nested MOVE spaces, owned lifetimes, the baseline COPY guard, and final
charts. It compares every H, L, B and Z entry with the author certificate.
It also obtains H a second way from the final backward predeparture adjoints.
Gaussian elimination deliberately uses the largest available pivot coordinate,
unlike the author's smallest-coordinate column elimination; the resulting
independent pivot witnesses are recorded in `RESULT.json`.

Meaningful controls demonstrate that replacing `1/g_i` by 1 changes the joint
encoder, reversing a nonzero chronological response sign changes L, and a
literal mismatch column makes a retained historical decoder fail. Projecting
away every observed endpoint gives rank zero, so endpoint observability is an
essential premise. Normal and optimized Python executions produce identical
receipts; checks do not rely on removable `assert` statements.

The input pins, independent matrix digests, exact family ranks, gain counts,
rank pivots, and literal mismatch witness are in `RESULT.json`. The
`REVIEWED-FILES.json` manifest binds the reviewed author files and this review's
files. Source pins refer to compressed native bytes; JSON certificate pins refer
to their decompressed payload bytes.

## Reproduction

```sh
python check.py \
  --source /path/to/final.json.gz \
  --cases /path/to/itinerary-control-obstruction/CERTIFICATE.json \
  --observations /path/to/active-helper-observation/OBSERVATIONS.json \
  --certificate /path/to/joint-nonneutral/RESULT.json.gz \
  --output /tmp/joint58-review.json
```

Expected final line: `PASS_INDEPENDENT_JOINT58_ADJOINT_REVIEW` followed by elapsed
seconds. Expected ranks are 58, 58, 31, 30 and 17 for the five recorded families,
with joint T rank 31 and decoder mismatch rank 30.

The result is an independently verified exact finite-source linear-response
theorem, with its arbitrary-block-volume consequence established by tensoring
the injective rational map. It neither discharges the programme's foundational
assumptions nor establishes a complete multiplication bound.
