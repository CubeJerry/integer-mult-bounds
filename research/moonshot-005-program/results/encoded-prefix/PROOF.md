# A causal encoded prefix using the existing main fields

**Proved finite-source construction, conditional only on the retained normalized
chart semantics. No complete H4 native, supplier or new κ.**

This continues CODED-LIFT by changing the intermediate main representation, as
required by the previous frozen-prefix capacity obstruction. It constructs the
selected source prefix through cut 25728 (events 0 through 25727), including the
first two main transports. The prefix has 11 live extra owned fields and nine
extra transports with histogram `P1 +8, P2 +1`. Their added target moment is

\[
8+2^{199/200}=9.993080525655735668\ldots.
\]

This is a *spent prefix budget*, not a complete H4 invoice. Future delivery,
main rebasing, endpoint decoding, sidecar retirement, physical work, precision,
and compiler closure remain unbuilt and unpriced. In particular the 11 fields
are still live at the cut. The previous ideal H4 allowance below 98.399076951 per
native cannot be used as evidence that the remaining word fits.

## Source and model

Source: `research/shared-wire-split-composition/data/final.json.gz` at canonical
`e54523517d0f03e58352e647c403a5af3e525a57`, SHA-256
`2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883`.
Programme baseline: `091099b2d6898657b51ddadda5f9a581bacbb58b`.
There are 400 original main fields and 1080 arbitrary helper fields. Two
virtual copies have independent main inputs x and y and the same arbitrary
helper inputs h. Owned source fields begin at zero. Every linear row below
is a row on complete normalized arrays, so the algebra tensors with `I_V`
for every positive array dimension V admitted by the retained chart interface.

The source uses chart labels for invertible maps on complete arrays. A same-
chart ADD acts on normalized rows; a legal nested-frame MOVE changes the chart
and leaves the normalized coefficient row unchanged. We do not infer physical
costs from coefficient equality. Every added MOVE below is literal and uses
the source's exact entry/exit frames. New sidecar MOVEs are explicitly marked
owned; public main carriers and public helpers retain their public annotation.

## 1. Changed main representation

Let u_r and v_r be the virtual source states and write

\[
\delta_r=v_r-u_r.
\]

Run the source word once on the physical first-copy main fields and the single
arbitrary helper bank. Replace each second main holder initially by

\[
q_i=y_i-x_i
\]

using one ADD with coefficient −1 at its initial chart. There are exactly 400
such ADDs and no MOVE or allocation. A q holder is now a *difference carrier*;
it is not claimed to equal the current second-copy virtual main field.

Maintain physical observations o_j, with current chart, owner and exact linear
row on the q inputs. For each current virtual field r require a decoder

\[
\delta_r=\sum_j b_{rj}o_j
\]

using observations **currently at r's chart**. Thus the second virtual field
is `v_r=u_r+sum b_rj o_j`. The decoder is part of the explicit continuation
state. It is not permission to read a row in a past or different chart.

Source ADD and nonzero SCALE events update the virtual decoder by linearity
and execute only on the first copy. The physical observations need not change.
This is valid because both operands are already decodable at the common chart.
Zero-owned INIT/CLEAR and a legitimate COPY have their separately stated
premises; none occurs in the constructed source prefix. Coefficients and charts
are fixed source-controlled constants, not functions of the data.

### Scalar-only phase

A source interval with no MOVE cannot create a new chart-observation requirement:
the current observations' span is closed under its scalar events. Therefore
freezing the initial q carriers gives an exact representation of both virtual
copies throughout every initial scalar-only interval.

The pinned source's first 24,472 events consist of 23,108 ADDs and 1,364 SCALEs.
All SCALE coefficients are nonzero. The first source MOVE is event 24472;
all six source MOVEs before event 25489 have zero difference row. They require
only the first-copy source MOVE and no difference transport. Thus there is a
literal encoded prefix through cut 25489 with **no extra owned field and no
extra MOVE**. It does not keep the old two main-prefix banks, so the earlier
738-rank frozen-main bound does not apply to its physical main representation.

Information is not discarded: the first-copy public prefix is an invertible
linear operator on (x,h), and all 400 independent q inputs remain in their
physical carriers. Together they retain all 1880 entering array dimensions.
This is a structural invertibility proof, not a floating rank calculation.

## 2. Causal transport and rebasing rules

An auxiliary MOVE from chart f to g with current virtual difference row d
requires no new difference transport if d=0 or if d is already in the span of
current observations at g. Otherwise choose an exact cochart expression for d
at f, allocate a fresh zero owned field t at f, and add the expression into t.
Then execute the original nested-frame MOVE on t. The original first-copy
auxiliary still takes its original MOVE. The snapshot sources remain unchanged
and t is a distinct owner. The extra MOVE is charged at its actual rank.

When a source main field r moves from f to g, its existing second main carrier
is already entitled to the second main MOVE in the H4 profile. It may currently
hold a different difference code. The following safe rebase preserves its old
information and gives it the needed destination decoder:

1. Snapshot the carrier's old row into a distinct zero owned field t at f.
2. Subtract t from the carrier, making it exactly zero.
3. Form the current virtual row δ_r in the carrier using current cochart
   observations other than that now-zero carrier. The old snapshot is available.
4. Move the carrier from f to g along the source main MOVE, and retain t at f.

Every overwrite has an explicit old-version snapshot. Step 3 cannot silently
reuse the old carrier value. This is a sufficient rule, not an assertion of
optimal storage. It uses scalar work and a real parked owner, but adds no
Gaussian MOVE beyond the already-counted second main MOVE. Keeping the old
code as t also preserves all previously available source-chart observations.

Induction over the source events proves the invariant: same-chart scalar
closure handles ADD/SCALE; a difference delivery supplies the missing row at
a new chart; and main rebasing preserves the old source-chart span while
supplying δ_r at the new chart. This proves the generated prefix's exactness.
It does not assert that arbitrary future deliveries fit the target budget.

## 3. Literal source-bound construction through cut 25728

The first nonzero auxiliary delivery is event 25489:

```
MOVE 830, chart 3 -> chart 56, rank 1
δ_830 = -q_172/2.
```

q_172 is still at chart 3. The witness is one INIT, one ADD with coefficient
−1/2 and one rank-one MOVE. Dirty helper input is retained in the first-copy
helper830; the new observation stores only its homogeneous difference.

The nine delivered differences are:

| Source event | Source role | Charts | Rank | Difference row |
|---:|---:|---|---:|---|
| 25489 | 830 | 3 → 56 | 1 | −q172/2 |
| 25666 | 802 | 3 → 28 | 1 | −q142/2 |
| 25688 | 327 | 31 → 372 | 1 | q33 |
| 25711 | 328 | 101 → 369 | 1 | q108 |
| 25716 | 322 | 101 → 376 | 2 | q108 |
| 25719 | 791 | 3 → 18 | 1 | −q131/2 |
| 25721 | 332 | 102 → 372 | 1 | q109 |
| 25724 | 327 | 372 → 375 | 1 | q33+q109 |
| 25725 | 332 | 372 → 381 | 1 | (−q33+q109)/2 |

The last two rows are materialized from the already delivered, current
chart372 observations. They are not original-input rereads. At source event
25717, main108's carrier is parked at chart101 and rebased from q108 to q108/2
before its funded MOVE to chart381. At event25727 it is parked at chart381
before its funded MOVE to chart237. The two parked rows coexist with the nine
delivery fields. There are 11 live owned fields and no source-owned field at
this cut. No retirement is claimed.

The complete emitted-prefix counts are:

| Operation | Source prefix | Encoded physical prefix |
|---|---:|---:|
| ADD | 24,321 | 24,738 |
| SCALE | 1,377 | 1,377 |
| MOVE | 30 | 41 |
| INIT | 0 | 11 |
| Total | 25,728 | 26,167 |

The 11 additional MOVEs comprise two already-funded second-main MOVEs and
nine newly charged auxiliary deliveries. The 417 extra ADDs comprise 400
initial differences, 11 terms in the nine delivery snapshots, two parking
copies, two carrier subtractions and two rebasing terms. Every new coefficient
is among ±1 and ±1/2. Original source scalar work remains literally present.
Their actual physical scalar/tape tariffs and complete precision propagation
are still separate obligations.

The transcript contains exact decoders for **all 1480 live virtual source
roles**, their current charts and every observation's row. At cut 25728 the
physical second main fields are codes; direct exposure as final outputs would
be incorrect. A complete continuation must consume or change those decoders
and eventually return both virtual main endpoints and all helpers, retiring
all owned fields under the actual erasure contract.

## 4. The first old failure has a local scalar repair

This local identity illustrates why changed intermediate main rows matter.
At the entry to source events 5617–5625, let main roles a=203 and d=221 have
independent copy values, while helper roles b=498 and c=572 have equal values
between copies. Exact source replay gives δa=q203, δd=q221−q116 and δb=δc=0.
Those nine source ADDs implement

\[
(a,b,c,d)\mapsto(b,c,d,-a).
\]

A frozen-current-main scheme loses δa from the mains temporarily. At event5624
it needs δ572=q203+q221−q116, which is outside the current cochart main span.
The new frozen-input representation retains q203 and has no such failure.

There is also a 16-ADD six-holder macro with no new owner or MOVE. With first/
second mains Ua,Va,Ud,Vd and shared helpers B,C, execute:

- Va-=Ua; Vd-=Ud;
- the original nine ADDs on Ua,B,C,Ud;
- the signed swap (Va,Vd)←(Vd,−Va), implemented by three ADDs;
- Va+=Ua; Vd+=Ud.

Its final physical values are `(Ua,Va,Ud,Vd,B,C) =
(b, b−d0+d1, −a0, −a1, c, d0)` for arbitrary entering a0,a1,d0,d1,b,c.
The pair difference at a retains the helper-c difference d1−d0; the logical
second-copy main-a difference is zero and is decoded as such. All six inputs
are retained by an invertible cochart map. This macro is an illustration,
not spliced into the generated prefix, which uses the simpler initial-input
carrier representation. The two constructions must not be counted twice.

## Verification and limits

`compile_prefix.py` deterministically emits the literal transcript and its
exact decoders from pinned source bytes. `verify_prefix.py` executes that
transcript on independent formal inputs, separately executes both original
virtual prefixes, and checks every current row and cochart decoder over Q.
It checks legal nested-frame moves, ownership and source versions. Wrong
first-delivery sign, wrong owned-MOVE annotation, omitted transport and aliased
snapshot controls must fail.
Independent review is recorded separately; an author's second execution path
is not itself independent review.

All five programme assumptions remain at global scope: native_all_columns,
owned_erasure, compiler, precision_tape and analytic_recovery. The statement
proved here is an explicit finite encoded prefix and its all-column algebraic
extension under the chart contract. It is not a complete asymptotic algorithm.

## Open next question

Continue from the emitted current decoders at cut25728, choosing carriers and
retiring observations so that *all remaining* correction moment, all scalar
and ownership costs, and endpoint decoding fit the complete H4 allowance.
Blindly retaining every past observation is not a target-feasible solution;
new cochart basis choices or changed native/caller structure are needed.
The current prefix gives an exact input state for that problem, rather than
requiring future sessions to reconstruct the first causal delivery again.

Prepared for @CubeJerry with substantial OpenAI assistance. Retains credit to
the selected #7000/#7001 source authors, the shared-core recovery programme,
and the previous coded-interface and information-capacity investigations.
