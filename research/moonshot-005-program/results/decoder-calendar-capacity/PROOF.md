# A source-calendar capacity obstruction to all-live local decoding

**Source-bound linear theorem with an exact finite-source rank certificate.
No new kappa and no universal shared-core impossibility.** Independent review is
recorded separately. The source is the selected 71,261-event native word at
canonical `e54523517d0f03e58352e647c403a5af3e525a57`, compressed SHA-256
`2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883`.
The programme baseline for this investigation is
`2b725ad5cb2661e93e50fd28cdf0a495fa7f710c`.

## 1. Precise interface and permitted freedom

Take two virtual executions of that word, with independent 400-field main
inputs x and y and the same arbitrary 1080-field helper input h. Every complete
field contains V coordinates over a characteristic-zero scalar field F
(in particular F=C), for any positive dimension admitted by the retained chart
interface. Normalize each chart by its specified invertible
coordinate map. Write the first execution's normalized row as c_r(x,h), and
the second minus first as d_r(q), where q=y-x. These are independent input
blocks of dimensions 1480V and 400V. Source-owned fields begin at zero.

The **all-live current decoder contract** requires that, after every source
event, both current virtual values of every live source role can be recovered
by linear operations from physical fields CURRENTLY in its chart. This is
equivalent to recovering c_r and d_r. The physical main and helper fields may
hold arbitrary linear codes. They need not equal either virtual prefix, and
the proof does not fix their actual MOVE payloads.

The funded transport calendar is nevertheless fixed: at each source main MOVE,
grant two arbitrary incoming complete fields at its destination; at each source
helper MOVE, grant one; at each source-owned MOVE, grant a fields, where a is
either 1 (the optimistic H4 profile) or 2 (duplicated owned work). Every other
cross-chart arrival is extra. Grant even impossible acquisition and arbitrary
teleportation for each funded field: only its destination and arrival time are
fixed. Earlier or differently routed arrivals require a different calendar and
are outside this theorem. Initial main inputs and helper inputs enter their
specified initial charts, and zero initialization brings no information.

Local work, exact coefficient services, arbitrary additional memory, snapshots,
erasure and immutable retention of all past local rows are free. Equal-span
charts 1091 and 1092 are identified for free. These grants strengthen a proposed
implementation. There are no free input rereads or cross-chart services. A
complete field still has V coordinates; it cannot contain two independent
complete fields at the same physical size. The argument applies to arbitrary
linear coding within those V coordinates, not only scalar combinations of
normalized rows.

## 2. General calendar-capacity lemma

For each chart f, let B_f(t) be the span over F of all required normalized rows
that have appeared there through event t, including its initial rows. Because
all past recovered values may be retained, their full coordinate space
`B_f(t) tensor F^V` lies in the actual historical information space K_f(t).
Let A_f(t) be the number of funded field arrivals by that event, and E_f(t)
the number of extra field arrivals. Local linear operations add no independent
input information; a field arriving at f adds at most V dimensions. Thus

    dim_F B_f(t) * V <= dim_F K_f(t)
                   <= dim B_f(0) * V + (A_f(t)+E_f(t))*V.

Consequently every successful implementation has

    E_total >= sum_f max(0, max_t [dim B_f(t)-dim B_f(0)-A_f(t)]).

This includes arbitrary proactive coding, unused funded capacity saved for
future demands, and arbitrary owned storage. It is the maximum cumulative
deficit per chart, not the sum of positive single-event deficits: a funded
arrival may prefetch a future independent row. Conversely a later funded
arrival cannot pay an earlier deficit. No assumption about literal main MOVE
payloads is used. The earlier 984-arrival theorem and this theorem therefore
have different scopes; their lower bounds must not be added.

All source coefficients are rational, so the ranks over F equal the ranks
computed over Q. This removes any dependence on the implementation's complex
block coefficients. The statement does not transfer this characteristic-zero
source or its half coefficients to the BIT interface.

The required row space splits as the direct sum of common rows on (x,h) and
difference rows on q. Its dimension can be computed by independent exact
elimination in the two blocks. Initially all required rows are initial input
coordinates in their prescribed charts. A cochart ADD, nonzero SCALE, zero
INIT or valid COPY cannot enlarge historical local knowledge once both operands
are already recoverable. CLEAR introduces no new row. Only a source MOVE can
add new required common and difference rows at its destination. Each of those
two insertions raises rank by zero or one. The source program and coefficient
domain are checked literally, including all owned flags and lifecycle guards.

## 3. Exact selected-source result

The source has 1710 main, 4553 helper and 47 owned MOVEs. Exact rational replay
and canonical-frame elimination give the following necessary arrival counts.
Cut k means events 0 through k-1 have executed.

| Cut | One funded owned arrival | Two funded owned arrivals |
|---:|---:|---:|
| 25489 | 0 | 0 |
| 25490 | 1 | 1 |
| 25728 | 9 | 9 |
| 26226 | 92 | 92 |
| 36961 | 1686 | 1667 |
| 71261 | **3144** | **3111** |

The certificate records every source MOVE's common/difference rank increments,
each chart's maximum deficit and the event attaining it. The exact source
calculation is finite, while the information inequality above holds for every
admitted V and every implementation in the stated linear/calendar grammar.
It is not an extrapolation from random inputs or a finite-size algorithm test.

## 4. Consequence for the evolving construction

At t=199/200, every extra positive-integer-rank Gaussian MOVE costs at least
one unit of paid moment. With the unchanged H4 caller and targets, the inherited
exact receipt allows less than

    221397923137950577 / 2250000000000000 < 98.399076951

per native for all added paid work. The all-live contract needs at least 3144
arrivals under precisely that funded calendar, even before their higher ranks
or ordinary work are priced. It therefore cannot complete that H4 profile.
Giving all original owned routes a second free payload still leaves 3111; it
does not repair the decoder obstruction, and its actual duplicated-owned bill
must in any case be charged separately.

This rules out the interface, not merely the author's eager implementation.
The exact early counts 9 and 92 also explain the eager prefix's transport
growth. A new full construction must relax at least one premise: require only
particular causally needed virtual values, change arrival times/destinations,
alter the complete target/paid invoice, or use a different physical model with
its own justified costs. Changed physical main encodings alone do not evade the
theorem if every virtual helper is still decoded at every source event.

The ten owned-difference identities from the companion package remain valid:
they require particular physical cochart observations only at their ten named
events. They do not require this overstrong all-live contract. Their remaining
observation construction and full tariff are still open.

## 5. Verification and limits

`scan.py` propagates exact rational source rows, keeps separate canonical-chart
bases, and computes cumulative deficits for both owned calendars. Its result
is reproducible from the pinned source. Independent review uses a distinct
implementation and separately verifies the capacity argument. Negative controls
include granting two arrivals for every source MOVE (zero deficit), a single
copy (zero deficit), prefetch slack, and the impossibility of paying an earlier
deficit with a later arrival. Source drift and ownership mismatches are rejected.

All five foundational assumptions remain unresolved. This package establishes
a scoped obstruction and motivates demand-driven coding; it supplies no native,
supplier, compiler admission, BIT supplier or complete multiplication exponent.

Prepared for @CubeJerry with substantial OpenAI assistance. Credit the selected
native and the programme's preceding capacity, causal-arrival and changed-main
construction packages. This is a continuation of that shared proof programme.
