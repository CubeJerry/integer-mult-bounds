# Fresh frozen-stock closure of proper-birth41

## Pinned input and exact result

The input is the endpoint-preserving proper-birth41 word, SHA256
`6c76a836322483cc11888ae214379a27adbb8f638ac3a049584f75953c5185a9`,
with native source SHA256
`8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e`.
This audit derives its observations from that word afresh. It does not inherit
an inventory, milestone, source bank, or dual from the unreduced clique41 word.

Independent exact replay checks all 222 original input columns, real-rational
chart geometry, custody, restorations, endpoint identities, and owned erasures.
The counts are 118 INIT, 798 ADD, 450 MOVE, and 118 dirty CLEAR. There are 1,588
record-state observations, including the 222 original input states.

The first cut at which the eight principals are at the zero chart and all 111
original X records have their raw values at Hub is step 1,196. The actual pure-X
records at the zero chart have binary rank 17. No history row is used to obtain
this current-cut rank.

## Three separately computed observation models

At receiver i, a record at real chart C is geometrically visible when C is
contained in F_i. A raw point X_j is geometrically local when the native real
inner product of roots i and j is zero. Every model below is an information
upper envelope: it ignores chronological and nested-route obstacles. It is not
an unpriced physical decoding construction.

1. **Current stock plus raw locals.** Use the actual pure-X fields retained at
   the fresh cut, at their actual current charts, and grant all geometric raw
   locals.
2. **Pure-X history plus raw locals.** Use every pure-X state that actually
   occurred, at its actual chart, and the same raw-local grant. Different
   historical states may not be simultaneously retained; this model grants
   them simultaneously for an obstruction calculation.
3. **All record X parts plus raw locals.** Additionally strip off all original-Y
   components of every actual record state. This is a larger information grant,
   equivalent to making those independent original-Y values available for
   subtraction. It cannot underestimate a receiver's X information.

Each model has exactly the same 41 directly fitting receivers as the completed
word. Granting all 41 completed raw points globally and then iterating free
feedback of newly decoded raw points yields no further point. Each closure is
exactly 41, and each has 70 explicit outsider dual vectors in RESULT.json.
The actual retained pure-X stock without the raw-local grant fits 35 of the
completed targets. The other six are 3, 21, 64, 65, 76, and 80. This distinction
is expected: actual decoding may have read records or raw values earlier than
the selected common cut. It does not invalidate the completed word.

In particular, deleting unused additions and moving the births did not create
an unmasked historical point-decoding opportunity outside the completed set.
There is no new target to route from these frozen observations.

## Checkable dual argument and field scope

For each outsider i, the checker supplies a binary column z with z_i=1 such
that every granted local observation row a satisfies a dot z=0 and z_j=0 for
every one of the 41 globally granted completed points j. The checker obtains
these vectors by exact binary elimination and verifies both conditions.
Consequently e_i is outside the local observation span even after all feedback
points in the closure have been added. The dual rows are derived independently
for each of the three models; the strongest model alone suffices to exclude a
new frozen-history decoder.

The same witness works over every field of characteristic two: its entries and
the observation rows are binary, and the displayed dot products remain zero.
For a positive whole-record width V, tensoring the witness by any nonzero record
vector preserves every observation and changes X_i. Thus even arbitrary local
computation cannot distinguish the two inputs. For a causal protocol whose only
cross-receiver feedback consists of already decoded raw points, no first new
outsider can be decoded, so iteration cannot enlarge the 41-point closure.
This argument does not grant arbitrary exchange of coded local observations.
It does not cover a changed source word, changed chart placement, newly captured
information, a new common code, or a different delivery transcript.

No movement lower bound, source-completeness theorem, or kappa improvement is
claimed by this diagnostic. Prices and the actual 41 endpoints are certified
separately in birth-localized41.

## Reproduction

Run `check.py` with `--repo` pointing to the pinned programme checkout,
`--word` to birth-localized41/WORD.json, `--engine` to
leaf-capacity-gate/check.py, and `--out` to this directory. RESULT.json contains
the three closures and all duals; CURRENT-STOCK.json records the full fresh cut;
ALL-HISTORIES.json records the complete actual observation ledger.
