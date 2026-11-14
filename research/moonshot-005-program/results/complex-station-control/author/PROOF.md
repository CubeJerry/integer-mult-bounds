# Original-D station controls cannot repair the stripped source

**Exact finite-source and all-volume linear-interface theorem. No new κ.**
This package concerns the stripped parent and stripped four-ferry words,
not the whole class of complex algorithms. It changes neither frozen
S011 package `history-frozen` nor `target-relation-frozen`.

## 1. Interface and claimed result

Use the pinned 400-input standalone parent (compressed SHA256
`a235a7e58f9eb96c6d409a88095fd6b59c977977baabb8735c76b2b820dcbedc`),
with its 31 coordinate returns removed by ending at parent event 4779.
Alternatively use the four-ferry word (compressed SHA256
`20a5c2c3eccd000b757f65e2cd6bed7f8a9ec39f0b8f88a66716e4b818a2521f`),
retaining exactly the operations whose parent event is absent or below 4779.
The resulting words have 4779 and 5851 operations, respectively. Their
actual hosted residual ranks are both 82. Their original forward coefficient
debt remains 4920; no result here completes it.

The original independent hosted donor fields are `D=304,...,399`; the hosted
Hub receiver roles are `B=208,...,303`. These role sets are authenticated
against the native source gzip SHA256
`2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883`.
Every original D field keeps its value throughout the selected word.
For each D role j, let S_j be all chart IDs it visits in that word, including
its initial and final charts.

Grant original d_j at every chart of S_j from the beginning, even before the
actual raw D field arrives. This grants permanent stationary caches and
future-station access without any cost. At every source cut, one may add to
any live **non-D** field at chart C an arbitrary fixed linear form

    sum_(j:C in S_j) L_(cut,field,j) d_j.

For any V>=1 over a characteristic-zero field, each L may be an arbitrary
V-by-V operator. Operators need not commute. The old operations, coefficients,
charts, routes and lifetimes are otherwise retained. Writing to original D
fields, newly mixing independent unknown non-D inputs, adding travelling
relays, and changing chart routes are outside this interface. Consequently,
this theorem must not be presented as an obstruction to transient D recoding.

The exact results are:

| Source | D columns invisible to all allowed B controls | Other columns | Actual residual before controls |
|---|---:|---:|---:|
| Stripped parent | 74 | 22 | 82 |
| Stripped four-ferry | 66 | 30 | 82 |

For the protected set J, every allowed control has zero final B response in
every original d_j column with j in J. The current reverse error therefore
has an identity principal block on J, before any new informative transport:

    rank(E) >= |J| V.

This conclusion permits all other D columns to be changed arbitrarily and
does not assume that the residual is a Gram code or any other chosen fitting.
Requiring every first-X, first-Y and original-D endpoint to be restored can
only restrict the control family further. No un-restored endpoint is offered
as a free completed output.

## 2. Direct adjoint proof

For a unit additive increment in a current field, its final B response is
computed by the fixed remaining source operations. Propagate all 96 B output
coordinate functionals backwards. For an old `ADD dst += c src`, add c times
the destination adjoint to the source adjoint. A nonzero `SCALE` scales its
adjoint. A `MOVE` changes the current chart; `CLEAR` introduces a zero adjoint
for the old owned field; reversing `INIT` retires it. The selected words contain
no `COPY`, and the checker explicitly rejects any unsupported opcode.

At every interval on which a field's adjoint and chart remain fixed, its
response is unchanged. It therefore suffices to check initial terminal states
and each event at which an adjoint, chart or lifetime changes. The exact
checker checks 4360 such non-D field states in the parent and 4904 in the
four-ferry word. It also compares every backwards original-input adjoint with
the independently replayed full endpoint map on all 400 original inputs.

Let U be the charts on which some live non-D field has a nonzero final B
adjoint at some source cut. The exact U sets have 131 and 139 charts. The
protected columns are exactly those original D roles satisfying

    S_j intersect U = empty.

There are respectively 74 and 66. Hence an allowed insertion of L d_j for a
protected j has final B response zero, for any operator L. Summing over all
insertions proves the statement for arbitrarily many controls. Tensoring the
old scalar response with I_V proves it for every volume and arbitrary
operator-valued inserted forms. This argument uses an exact zero identity,
not a modular rank upper bound or a failed finite search.

The original unmodified B outputs also have coefficient zero on every
protected d_j. The actual target is b_i-d_i. Restricting the residual columns
to J and its receiver rows to the matching B roles therefore gives exactly
I_|J| (up to choosing the sign convention for target minus current). This is
the displayed all-volume rank lower bound. The checker's exact certificate
lists every protected role, source port, station set, and matching receiver.

## 3. Why earlier Hub snapshots provide no hidden extra channel here

It is insufficient to inspect only final B rows if older Hub histories could
contain information subsequently discarded. The selected source has a stronger
structural property, checked independently of the D-control adjoints:

* Exactly 200 fields arrive at Hub 127, each a public field.
* There is no owned arrival and no public departure at the Hub.
* No public field starts at the Hub.
* All 200 final Hub fields are the 104 first-X roles and the 96 B roles.
* Treating the 200 actual arrival values as 200 formal independent variables,
  the unchanged Hub-only circuit has an invertible 200-by-200 map K from
  arrivals to final Hub values.

The checker constructs and ranks K over the rationals. This does not merely
reuse a baseline statement that historical rows happen to be in the final
span. Since no D station is Hub, the granted source controls do not intervene
in that Hub circuit. Thus, for every controlled execution, every historical
Hub observation is a linear function of its final Hub vector. Local owned
copies and departures do not change this: there are no later owned arrivals,
and all Hub operations are already included in K.

If new messages are consumed at the Hub and feed known linear forms into old
operations, all historical Hub values are instead functions of the final Hub
vector and those messages. Their past use does not create a further independent
record. An independent unknown-input replacement of old Hub operations is
not granted by this argument.

## 4. A return-information consequence, with its scope stated

Suppose the above controlled old word is augmented by q newly acquired
whole-V observation fields delivered to the Hub. Grant arbitrary mixed
observations, any acquisition chronology, free local storage, arbitrary Hub
linear decoding, and feedback linear in earlier messages. The newly acquired
fields may read actual old-source fields and earlier messages. They do not
make additional unknown-input-dependent deposits at intermediate charts; a
travelling accumulator that distributes several different innovations before
its final arrival is a different interface and must be accounted for
separately.

Then completion of the exact B outputs together with restoration of the
first-X Hub outputs requires

    q >= 74  (parent),           q >= 66  (four-ferry).

Here q counts whole-field information dimensions: for fragmented messages,
the statement is sum of their independent scalar capacities >= |J| V. It
is not |J|V separate MOVE events.

To prove it, remove all message-driven perturbations from the linear execution
by superposition and call the remaining final Hub vector H'. Its coefficients
on the 104 independent original first-X inputs and 96 independent original B
inputs form an invertible matrix (the inserted forms involve only original D).
Thus the pure original-D space intersects row(H') trivially. The target Hub
vector differs from H' by a pure-D matrix whose protected B minor is I_|J|.
Its quotient demand modulo H' therefore has dimension at least |J|V.

Every actual old Hub history lies in row(H', messages), by the formal K
identity above and linear superposition. Exactly q V-dimensional messages
can add at most qV quotient dimensions. This gives the inequality. Feedback
causality affects which messages are realizable, but cannot increase the
span of their entire recorded tuple. Restoring first-Y and every other public
output is an additional duty and is not discarded.

This is an information lower bound only for capture-and-return observations
and the explicitly retained old-source control grammar. It does not count a
multiphase travelling field as one independent history row, does not cover
recoded D carriers, and does not prohibit changing the old B processing rules.

## 5. Exact retained price

The source-specific price checker retains the full selected caller and the
actual stripped MOVE profiles. With t=199/200, its per-rail limiting room for
additional paid MOVE moment is

    57.096340268441956...                 (parent),
    56.851881389659691...                 (four-ferry).

The finite fixed-m room is the displayed limit minus
31.539778367085413.../(m-1), for every integer m>=2. Since every nontrivial
whole-field return has MOVE rank at least one, 74 or 66 whole-field returns
cost at least 74 or 66 moment units, even granting one rank1 MOVE per record
and every other new duty free. Both strict deficits persist for every finite
m. The information dimension bound also applies to fragmented records, but
this price conclusion retains whole-field calls; fragments need their own
complete invoice. The price argument must not be used for zero-transport information carried
by a changed source: that possibility lies outside the old-word interface.

All ordinary scalar work, lifetimes, physical placement, compiler, precision,
complete forward endpoints, compatible BIT supplier, and the five foundations
remain required. No new κ or complete complex supplier is established.

## 6. Controls and next source construction

Each nonprotected D column has a stored actual nonzero B-response witness
at an admitted station. Thus the checker distinguishes zero and nonzero
controllability. A separate scope-changing control adds a protected original
D value into a different live original-D carrier at the ground chart. The actual prefixed ADD is replayed on all400 inputs: its B change is the
certified carrier column and its borrowed D endpoint is left as d_k+d_j.
This shows directly why
writing to D carriers must not be smuggled into the proved interface. That
control does not restore the borrowed carrier at its final facet and is not
a complete construction.

The most concrete remaining escape is now transient recoding of original D
or a travelling mixed field that deposits several independent historical
forms before terminal restoration. Both change the old source's protected
column calculation. Their global endpoint restoration and full movement bill
must be proved, not inferred from this scope limitation.

Credit: @CubeJerry persistent programme; the pinned native and S010 source
construction authors; the S005/S006 source-adjoint methodology; S011 source
and price analysis prepared with substantial OpenAI assistance. This author
checker is newly written and does not import either earlier frozen producer
engine. Independent review is still required before programme admission.
