# Deferring common state still leaves a106-arrival departure obstruction

**Proved source-bound linear lower bound, supported by a modular rank
certificate. No new kappa.** The common-state interface here is weaker than
the preceding all-live decoder contract. It permits the quiet helper449 loan
between source events28048 and30653.

## 1. Source and observation contract

Use the71,261-event native at canonical
`e54523517d0f03e58352e647c403a5af3e525a57`, compressed SHA256
`2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883`.
There are1480 common input arrays (400 main and1080 arbitrary dirty helpers)
and400 independent difference arrays q=y-x. Source-owned fields start at zero.
Each array has V coordinates over a characteristic-zero field F. Source rows
are rational, and chart maps are the retained invertible maps.

Require these virtual values to be recoverable from physical information
currently in the specified chart at these times:

* Before each source ADD or COPY, both current common operand values.
* Before each source SCALE, its current common operand value.
* At the endpoint, all1480 common public values in their final charts.
* Before each source main MOVE, that main's current difference value in its
  SOURCE chart; at the endpoint, all400 main difference values.

A MOVE alone imposes NO common observation requirement. An owned CLEAR imposes
none either. Common values may be encoded or unavailable in their virtual
chart between read deadlines. The contract still exceeds endpoint-only block
correctness: algebraically fusing source operations without separately decoding
their listed operands may leave its scope.

The funded destination/time calendar grants two arbitrary incoming fields per
source main MOVE, one per helper MOVE, and a=1 or a=2 per source-owned MOVE.
Funded payloads have arbitrary acquisition and teleportation. Allow unlimited
free local immutable snapshots, scalar work, linear coding within allV
coordinates, precision, memory, parking and cleanup. Initial inputs enter only
their pinned charts; no extra input rereads or cross-chart services are free.

## 2. Capacity argument

For each chart f, retain the span B_f(t) of its initial input rows and every
common or difference row required through time t. The independent input blocks
have additive ranks. Let A_f(t) be funded arrivals and E_f(t) extra arrivals.
All required full-array forms lie in historical knowledge K_f(t), hence

    dim_F B_f(t) * V <= dim_F K_f(t)
                   <= dim_F B_f(0) * V + (A_f(t)+E_f(t))*V.

Taking each chart's maximum nonnegative prefix deficit gives

    E_total >= sum_f max(0, max_t[dim B_f(t)-dim B_f(0)-A_f(t)]).

Departure observations precede that MOVE's destination funding; read demands
precede their scalar event; endpoints come last. Prefetch credits remain, but
later arrivals cannot pay an earlier deficit. Arbitrary main payload codes do
not bypass a demand that the virtual main difference itself be decoded before
departure.

Compute lower ranks modulo p=1000003, whose primality is checked. All source
coefficient denominators are invertible modulo p. A nonzero modular minor is
a rational nonzero minor, and rational rank persists over F. Initial unit-row
ranks are exact. Modular historical ranks therefore give a rigorous lower
bound for everyV andF. No inference of rational span membership from modular
membership is used.

The implementation skips re-inserting a current common row already known in
its chart. Initially each input is known. A MOVE invalidates this flag; its
first actual read inserts the current row. Once both operands are inserted,
their ADD/COPY result lies in the same local span; SCALE likewise preserves
membership. INIT produces known zero. This induction makes the optimization
identical to inserting every listed read demand, including repeated reads.

## 3. Certificate and consequence

| Common observations | Difference observations | Owned a=1 | Owned a=2 |
|---|---|---:|---:|
| Every current value | Main departure and endpoint |106|106|
| Actual scalar reads and all public endpoints | Main departure and endpoint |**106**|**106**|
| Actual scalar reads and all public endpoints | Main endpoint only |0|0|
| No common observations after initial input | Main departure and endpoint |0|0|

The second row is new. Its104 contributing charts are90 and98 with2 each and
102 others with1 each. Deferral moves the first maximizing event later in eight
charts without reducing their maxima. For example chart38 moves from main814's
departure at27202 to common411's SCALE read at27590.

Common449's arrival at28048 creates no read-deadline demand at594 until its
actual target read at30837. The quiet loan closes at30653, before that demand.
This explicit guard demonstrates that the new replay permits the actual common
state freedom exercised by the seven-ADD construction.

The H4 invoice allows less than98.399076951 extra paid moment per native at
t=199/200. Each extra positive-integer-rank Gaussian MOVE costs at least1.
Thus106 necessary arrivals exceed the allowance before higher ranks or ordinary
operations are priced. Giving both payloads on every source-owned route does
not lower106. Monotonicity gives the same106 for every mixed one/two-owned
funded calendar.

At least eight scalar-row units of this observation burden must be removed to
reach a98-arrival ceiling with all else fixed. Under the ten-owned-skip
invoice's remaining seven-arrival ceiling, at least99 units must be removed or
the invoice changed. These are necessary changes, not constructed sufficient
ones. A next source architecture must defer some virtual main departures too,
fuse common scalar operations without individual operand demands, alter paid
arrival timing/destinations, or obtain other justified budget savings.

A zero modular result supplies no obstruction. It does not establish that the
full rational calendar bound is zero, that payloads can actually be acquired,
or that a physical implementation fits the target. All five foundational
assumptions, native/caller admission and the complete target theorem remain
open. The preceding984, all-live3144 and departure106 lower bounds have
different premises and must not be added together.

Prepared for @CubeJerry with substantial OpenAI assistance. Credit the selected
native, the shared-core H4 invoice, the prior calendar-capacity argument and
the complementary quiet-helper loan construction.
