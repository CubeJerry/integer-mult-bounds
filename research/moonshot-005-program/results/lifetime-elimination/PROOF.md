# Late reconstruction removes whole owned dependency lifetimes

**Proved typed-word elimination theorem, exact conditional source constructions,
and full provisional paid profiles. No new kappa.**

The construction replaces a terminal owned observation and then removes its
unused preparation, including upstream owned lifetimes whose only consumers
were that preparation. It preserves every public endpoint. This changes the
intermediate observation interface, so a theorem requiring a deleted return
value at its former clock does not automatically apply to the new word.

## 1. Whole-lifetime elimination theorem

Consider any finite well-typed word using public and owned fields with INIT,
CLEAR, ADD, COPY, nonzero SCALE and nested MOVE operations. A lifetime runs from
one INIT of an owned label to its matching CLEAR. An external read is an ADD or
COPY using that owned field as source and writing a distinct field. Writes to
the owned field, its MOVEs and its lifecycle instructions are internal.

**Lemma.** If an owned lifetime has no external read, removing every operation
whose destination belongs to that lifetime preserves all other fields and
every public endpoint, for every legal input and permitted field size. The
result remains well typed and returns the same owned labels dead.

**Proof.** Each removed operation affects only the specified owned field. No
retained operation reads it during the lifetime. Its INIT starts from a dead
label and its CLEAR returns the label dead. Other fields and chart states
therefore evolve identically while the deleted label remains dead. Subsequent
uses begin with a fresh INIT and are unaffected. This operational proof is
independent of row rank, input distribution and finite simulation. It includes
the removal of allocation, erasure and MOVE operations. QED.

Deletion may remove another lifetime's last reader. Repetition is valid by
induction and terminates because instructions decrease. Alternatively, mark
owned lifetimes backward from their public uses, following dependencies from
an owned consumer to its owned sources. Every lifetime outside the marked set
is an unobserved owned subgraph, including any internal cycles. The certificates
check that the three-wave rule removes exactly this full unmarked set. No dead
owned-only strongly connected component remains. Maximality here concerns this
whole-lifetime dependency criterion, not all algebraic or physical optimizations.

## 2. Why terminal reconstruction changes upstream dependencies

For a current identity `delta_r=sum_j a_j delta_observer_j` at the destination,
the predecessor lowering retires r at its source, initializes it as zero at the
destination and adds actual cochart observers. The new destination lifetime has
the source row. If the old lifetime has no earlier external read, its entire
preparation is now unused and the lemma deletes it. Its owned sources may then
lose their last consumers too.

The current identities require the400 independent main-difference domain with
arbitrary equal entering helpers in the two executions. The deletion lemma
holds for every input to the expanded word; it does not enlarge the domain of
the inserted identities. Actual observer fields, acquisition and backing remain
conditional premises unless constructed below. No externally required read is
silently skipped: every deleted lifetime is certified to have no reader in its
deletion wave, and every survivor has a dependency path to a public use.

## 3. Exact source cascade

Start with seven current reconstructions at
28169,33558,34479,39217,40094,40096,41758. Three waves delete8,3,3 lifetimes.
One first-wave lifetime was already unread in the source and contains no MOVE;
the other deletions are exposed by reconstruction.

* Owned1510 has only writes until its final public update41760. Reconstruction
  at41758 removes its earlier MOVEs39546(rank4) and41756(rank1).
* The intermediate1512 lifetime reconstructed at40094 is updated only internally
  by40095 and retired by40096. Deleting it removes all four40094 observer terms,
  agreeing with the independently proved two-return fusion.
* Child-prefix deletion removes the last consumers of owned1515,1514,1513.
  Their deletion removes the last consumers of owned1526,1524,1522. Those three
  lifetimes contain historical returns28141,33554,34467. The historical returns
  disappear without preloads or before-return decoding obligations.

Thus seven-current removes12 original owned MOVEs and leaves22 terms, with
saved histogram `S7life={1:5,2:3,3:1,4:2,6:1}`.

Adding current37606 deletes the unread source lifetime of1511, including its
historical37597 return(rank5). Its first external read is37608. Eight-current
therefore removes14 MOVEs, including all four historical returns, and uses26
terms:4main,20helper,2owned. The four37606 helpers are228,913,992,1444; their
physical availability is not replaced by free main/owned history. Its histogram
is `S8life={1:6,2:3,3:1,4:2,5:1,6:1}`.

All ten current identities additionally remove33272(rank2) and33281(rank1),
leaving28 terms and `S10life={1:7,2:4,3:1,4:2,5:1,6:1}`.

No public MOVE is removed or reordered. All surviving owned operations are
included in the exact word and invoice. Fresh destination accumulators remain
where needed, and an endpoint recipient occurring in its reconstruction is
read before update. No SCALE0 or unpriced destructive public overwrite is used.

## 4. Constructed optional entry preloads

The33272 and33281 target rows use44 and52 original chart3 input directions.
`ten_preloaded` constructs them at entry with two fresh owned accumulators,
96ADDs and two paid owned MOVEs from chart3 to260 and1091, of ranks3 and4.
Each accumulator is retained until its reconstruction, used once and cleared.
The full emitted word includes all allocation, transport, storage and cleanup.

These two particular helper-observation premises are thereby discharged on
the declared physical input-difference rail. There are26 remaining external
terms and two constructed internal preload observations. Formation of the q
inputs from the multiplication copies, the full joint native and ordinary
tariffs remain separate obligations.

The earlier rank4 fresh-preload exclusion was tied to a smaller fixed margin.
The new savings make both preloads affordable. However, the optional variant
has a worse paid moment than eight-current at the same26 remaining terms. It
is a verified module, not preferred solely because its preloads now fit.

## 5. Complete provisional paid accounting

Let T4,P4 be the pinned H4 profiles and
`O={1:20,2:9,3:2,4:13,5:2,6:1}`. The builder derives the actual owned-MOVE
histogram from each emitted word. Its whole profile is

    T=T4,    P=P4+18(O-S),

with18 additional rank3 and18 additional rank4 positions for `ten_preloaded`.
Every removed historical route, new entry route and repeated native is counted.

|Variant|Removed original owned MOVEs|Extra preloads/native|External terms|Paid positions|Rank surplus|Remaining paid moment/native, strict upper|
|---|---:|---:|---:|---:|---:|---:|
|seven|12|0|22|153054|3544|14.841106979641|
|eight|14|0|26|153018|3652|20.801032491590|
|ten|16|0|28|152982|3706|23.794113017246|
|ten_preloaded|16|2|26|153018|3580|16.838177042001|

All have27344 target positions. The exact following bounds, divided by18*10^15,
are the remaining paid moment/native at exponent199/200:

|Variant|Lower numerator|Upper numerator|
|---|---:|---:|
|seven|267139925633455462|267139925633527118|
|eight|374418584848544536|374418584848616174|
|ten|428294034310347784|428294034310419404|
|ten_preloaded|303087186755941834|303087186756013490|

Exact integer inequalities for200th roots prove these intervals. With all other
terms fixed, at most14,20,23,16 additional positive-integer-rank fields fit,
respectively. A margin is not evidence that a supplier or physical observer
exists; every new acquisition, recursion and ordinary fee must still be charged.

Preloaded-ten costs between3962855449589037/10^15 and3962855449589040/10^15 more
paid moment/native than eight-current. No complete ordinary/compiler/precision
dominance theorem or completed multiplication exponent follows.

## 6. Actual reference word and ownership

|Quantity|Source|seven|eight|ten|ten_preloaded|
|---|---:|---:|---:|---:|---:|
|Instructions|71261|71208|71201|71194|71296|
|ADD|61180|61156|61151|61146|61242|
|MOVE|6310|6298|6296|6294|6296|
|INIT / CLEAR|54 /54|47 /47|47 /47|47 /47|49 /49|
|SCALE|3662|3659|3659|3659|3659|
|COPY|1|1|1|1|1|
|Declared owned labels|51|51|51|51|53|
|Owned lifetimes|54|47|47|47|49|
|Peak owned fields|43|34|33|33|33|
|Final owned fields|0|0|0|0|0|

These are actual full-word counts, not sums of independently priced modules.
The certificate records every deleted operation by source index, all surviving
lifetimes and external readers, and all remaining observation versions.

Other original helper-difference MOVEs remain in these reference words. The
words establish equivalence and provisional paid feasibility; they do not
implement the H4 helper-sharing premise. A400-input homogeneous reference is
not an1880-input joint native.

## 7. Verification and remaining scope

The builder freshly checks all ten inherited target rows, every expanded
reconstruction, and all1480 public endpoints after deletion for each variant.
All400 independent input coefficients are exact. Typed ownership/chart guards,
cleanup, source MOVE maps, lifetime dependencies, backward public closure,
whole invoices and exact moment bounds are checked. The all-size result comes
from the operational lemma and inherited linear identities tensoring across
every permitted field size, not a bounded collection of numerical experiments.

Controls change a surviving observation coefficient and alter public endpoints;
remove an externally read lifetime and reject the word; and give helper400 an
independent difference, changing94 public endpoints relative to the original
source replayed on that enlarged domain. The preload word also rejects a
noncochart raw input. Normal/-O receipts, certificates and transcripts agree.

The new intermediate interface legitimately removes historical before-return
obligations. Earlier obstructions remain valid for their stated interfaces.
An actual joint helper/main/owned representation, compatible uniform complex
and covered BIT suppliers, full ordinary/precision/compiler/recursive costs
and the five foundations remain open. No new kappa. Prepared for @CubeJerry
with OpenAI assistance; credit source/H4 authors, S002 identities, S003 quotient
and fusion work, and the separate independent reviewer.
