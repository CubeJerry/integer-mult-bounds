# Independent review: calendar capacity and weaker decoder obligations

**Accepted within the stated linear, source-calendar scope. No new kappa.**
This review was performed by the bridge worker independently of the root
worker's rational replay. It includes proof review and a distinct modular
implementation; it is not a second execution of the author's verifier.

## Mathematical review

The dimension inequality is valid over any characteristic-zero field F,
including C. A normalized required scalar row b means all V coordinate forms
in b tensor F^V must be recoverable. Immutable snapshots may be granted for
free, so every past requirement remains in the historical knowledge space.
Local linear work adds no independent input information, and each complete
incoming field contributes at most V dimensions. The initial fields are
independent unit input coordinates, hence their initial ranks are exact.
The maximum cumulative deficit in each chart is a necessary count of its
extra arrivals; adding chart maxima is valid because one arrival has one
physical destination. Prefetch credits are retained. Future arrivals cannot
repair an earlier deficit.

Arbitrary physical codes and arbitrary linear mixing within V coordinates do
not break this argument. Rational source row ranks agree after base extension
to F. The initial row model has independent common (1480) and difference (400)
input blocks; sharing the arbitrary helper input is exactly the reason its
contribution cancels in the difference block. Equal-span chart aliases are
identified. No nonzero initialization, input reread or unpriced cross-chart
service is allowed. Changing the funded destinations or arrival times leaves
the theorem's scope.

The weaker-interface extension uses the same lemma with a smaller demand
calendar. Source main departure demands must precede that MOVE's destination
funding. Endpoint demands are additional terminal requirements. Common state
remains recoverable after every source event throughout these variants.
Removing one scalar demand in one chart can lower any later history rank and
therefore its maximum deficit by at most one; the stated necessary reductions
of 8 or 99 rank units follow. They do not identify sufficient demand deletions.
Monotonicity between the one-owned and two-owned calendars proves that every
mixed owned calendar also has the common 106 departure lower bound.

## Independent calculation

`independent.py` uses sparse finite-field maximum-pivot elimination modulo
1000003, whose primality is checked by trial division. It independently derives
GF(2) RREF chart keys. The author's elimination is rational and uses a different
pivot convention. Source denominators are checked invertible modulo the prime.
Initial unit-row ranks are exact. A modular nonzero minor is a rational
nonzero minor; thus modular history ranks certify rational lower bounds.
This reasoning uses cumulative rank, not an invalid assumption that modular
span membership by itself proves rational membership.

All 6310 MOVE innovation records, every chart maximum and maximizing event,
and all six prefix cuts agree. The final lower bounds are 3144 (one funded
owned arrival) and 3111 (two). `weaker_independent.py` separately builds demand
histories and funded calendars, then merges them with ordered event phases
and a second chronological pass. All 22098 demand records and all chart
maxima/argmaxes agree across the three weaker interfaces: 913/902 for current
mains, 106/106 for departure plus endpoint, and 0/0 for endpoint only.

The endpoint-only zero means this relaxation gives no obstruction. It proves
no realizability, source-side payload acquisition, tariff or precision bound.
The positive bounds likewise do not rule out demand-driven code with deferred
common state, alternate transport calendars, or a different justified invoice.
All five foundational assumptions remain open. The source and frozen author
file pins are in the adjacent review receipts and REVIEWED-FILES.json.
