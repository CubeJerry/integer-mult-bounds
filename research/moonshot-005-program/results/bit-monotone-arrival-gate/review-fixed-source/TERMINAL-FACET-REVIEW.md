# Review of the terminal-facet gate

## Finding

The last-proper-chart argument is valid for a fixed clean-X source, a fixed
canonical rank-nine terminal packet map, one monotone public-Y lineage per
output, and X-only owned caches. Its strongest safe conclusion is an
information-bearing field must arrive at each missing final facet. It need not
be a packet: a copied source cache or another X-only owned record can make the
arrival, but it must pay a distinct MOVE into that facet.

The pinned source has 111 distinct rank-seven output facets. The source lines
orthogonal to receiver `i` are exactly its off-diagonal contact support; they
all lie in its actual facet and span that facet with rank seven. The independent
X-only source has at least one history at exactly 57 facets, with history
row-ranks only one or two. I conservatively count all 57 as already served.
The other 54 facets need a new correction-bearing field at the exact endpoint.

Without branching Y-bearing owned copies, only the receiver whose endpoint is
`F_i` can be at `F_i`: distinct rank-seven facets are incomparable. A monotone
packet lineage can visit at most one rank-seven facet. Thus nine already-paid
packet lineages can cover at most nine of the 54 uncovered facets. If the
architecture allows packet cloning or source-cache delivery instead, that
changes the mechanism but not the lower bound: the remaining 45 distinct
facet destinations need at least 45 additional MOVE events. A MOVE into a
rank-seven facet from any proper subchart has rank at least one, so these cost
at least 45 units of movement moment.

The audited baseline moment is

```text
clean X-only source        289*1^t + 244*2^t
111 direct rank-seven Ys   111*7^t
9 direct rank-eight packets 9*8^t
baseline                 1616.0437246329968685...
ceiling                  1621.750880211152355...
remaining room               5.7071555781554865...
```

Nine packets split into eight rank-one moves each add
`9*(8 - 8^t) = 0.7447207381051035...`, leaving `4.962434840050383...`.
The 45 additional rank-one MOVE lower bound exceeds either remaining-room
figure by a wide margin. This keeps the price conclusion even when the strict
"nine packets cannot serve 54" wording is replaced with a cache-and-clone
allowance.

## Why the last-proper-chart step works

For a clean X history row at chart `C`, every supported input line is contained
in `C`. The future difference between a packet read at `C` and its fixed final
packet row consists only of later edits at charts `D` nested inside `C`; those
edits have source support inside `D`, hence inside `C`. Any local X-only term
added to a public-Y lineage before its last proper chart also has support
inside that chart. Public-Y ADDs can combine only co-charted rows, so they do
not enlarge this support. The terminal global packet contribution is handled
separately by the rank-nine fitting `A P`.

After the global term is fixed to `K`, the remaining correction for receiver
`i` is `F_i=(K+I)_i`. Its support is the complete off-diagonal contact set
`S_i`; the exact contact roots in `S_i` span `F_i` with rank seven. If the
last proper chart is `C < F_i`, its local rows have support in the root lines
contained in `C`, so their combined support cannot equal `S_i`. Some
correction-bearing value must therefore be present at `F_i`.

This is a first-arrival claim. If no clean source row is already at `F_i`, a
nonzero value cannot be created there by INIT alone or by ADD without another
nonzero co-chart operand. A field with that operand must MOVE into `F_i`.
Different missing facets have different destinations, so one MOVE event cannot
serve two of them. A source-cache route into `F_i` is a legitimate exception to
"packet visit," but it is still charged by this MOVE count.

## Scope and cautions

- The scalar terminal-fit premise is the pinned F2 rank-nine rigidity result:
  a rank-at-most-nine matrix with diagonal one and zeros at noncontacts is
  exactly `K`. For block volume `V`, this extends only on the reviewed
  invertible-Schur stratum. The singular noncommuting block case is not covered.
- If the decoder is changed by public-Y coding, the conclusion needed here is
  the product `A P = K`, not `A = D` individually. The fixed decoder `D`
  further pins `P` to the canonical encoder.
- A Y-bearing owned copy could branch one public-Y value through incomparable
  subcharts and recombine it at `F_i`. The review does not treat such a copy as
  an X-only cache; its own movements and lifetime need a separate invoice.
- A redesigned X-source word may create rows at additional facets. That is a
  different source and must pay its changed source itinerary. A nonmonotone
  packet tour can also revisit incomparable facets and lies outside this cut.
- The 57 exact-facet history counts are deliberately generous: their current
  source-history row-ranks are only one or two, and the separate one-chain
  cache theorem shows that a history there does not by itself complete `F_i`.

  The reason this exclusion matters is already visible in a two-dimensional
  toy chart: if `F=span(e1,e2)`, two Y-bearing branches can collect `x1` at
  `span(e1)` and `x2` at `span(e2)`, then merge at `F` to make `x1+x2`. Each
  branch's last proper chart is one-dimensional, but the union of the two
  incomparable supports spans `F`. The 111-facet argument applies to one
  monotone output lineage with X-only caches; it does not silently cover this
  branched construction.

## Independent replay

`review_terminal_facet_gate.py` reconstructs the source roots and receiver
facets from the pinned native gzip using exact rational arithmetic. It checks
all 111 contact sets, their rank-seven spans, self-exclusion, endpoint-facet
uniqueness, and the 57/54 clean-X-history count. The result is
`TERMINAL-FACET-REVIEW.json`.

```text
checker SHA256  6ce8086be058147b68ab0ea982064480bb82f3b05854acee7e61c3492ca2cb4e
result SHA256   0baefa1fba4369d848635a68f61643949a8e297de53796c0ea5a1b3848f81c91
native SHA256   51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78
```

This review narrows and repairs the event-count wording. It does not establish
a complete word or a new supplier.
