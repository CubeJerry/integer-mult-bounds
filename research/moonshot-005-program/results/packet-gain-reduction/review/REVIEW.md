# Independent review of packet/private/native-history gain criteria

**Accepted as derived interface theorems with explicitly retained source
dependencies. No new κ or complete source construction.**

This review covers the frozen `PROOF.md` and `GENERAL-INTERFACE.md`. The source
facts are inherited from the already admitted complete history-nullspace and
stable endpoint packages. Every dependency byte hash in `SOURCES.json` was
checked. Their source verifiers were not rerun here; this is independent review
of the new mathematical deductions, not a new claim of independent source
reproduction.

## Restored endpoint with packet-dependent initial correction

Write the actual registered histories as

\[
 y=Ou+(OVC+B)q.
\]

The admitted complete nine-relation certificate implies `NB=0` for all
columns of B when **every control column** is supported at the same admitted
220 stations. The certificate concerns every allowed station and source cut,
so its annihilation extends coordinatewise from one private input to any
finite collection of linear private inputs, subject to that common station
restriction.

The stable decoder D0 is the actual final-role-189 minus initial-role-189
history functional. The control stations do not meet the receiver itinerary;
therefore local native operations still express that actual final field by
the same registered histories. Restoring the final field gives

\[
 D_0y=u_{77}-(e_{189}V)Cq.
\]

The negative sign and the modified initial observation are essential. The
initial read is `u189+(e189 V)Cq`, not the old value u189. Initial corrections
at receiver chart 3 are legitimately outside the later control-station set,
and their effect is fully included in OVC.

Any history coefficient D with `DO=e77` differs from D0 by a left-null row of
O. It therefore has the same private gain, since it annihilates both B and
OVC. The receiver can obtain `u77+q77` precisely when the desired private
coordinate belongs to `row(C,S)`. This proves the displayed linear criterion.

The nonlinear strengthening in the author proof is also valid. If the desired
coordinate is outside `row(C,S)`, choose q0 in their common kernel with a
nonzero desired coordinate. Complete nullspace annihilation places Bq0 in
`im O`; choose v with `Ov=Bq0`. The two inputs `(0,q0)` and `(v,0)` produce
identical full records. Endpoint restoration and `Cq0=0` imply
`e77 v=D0Bq0=0`, so the targets differ. This uses arbitrary independent field
inputs; it is not a bounded-bit or integer residue-decoding lower bound.

## General criterion with foreign control columns

For arbitrary actual records `y=Ou+Rq`, choose a baseline decoder D0 with
`D0O=h`, and let N span the complete left nullspace of O. All compatible
history coefficients are exactly `D0+tN`. Their private gains are
`D0R+tNR`. Thus recovery of `hu+eq` from histories and `Cq,Sq` is equivalent
to

\[
 e-D_0R\in\operatorname{row}(C,S,NR).
\]

If the actual stable endpoint relation places D0R in `row(C)`, this reduces
to `e in row(C,S,NR)`. For `R=OVC+B`, the extra native-history information is
exactly `row(NB)`, since NO=0.

Under the same unrestricted finite-dimensional field assumptions, this
criterion is necessary even for nonlinear decoding of these particular
linear records. If it fails, the target row `[h,e]` is outside the row space
of the full observation matrix `[[O,R],[0,C],[0,S]]`. Its kernel therefore
contains a displacement on which the target changes. The complete records
coincide for the two displaced inputs, excluding every decoder. This is a
direct linear-algebra strengthening, not a statement about nonlinear source
encoders or finite input domains.

The supplement correctly avoids a serious scope error: annihilation of only
the q77 column does not establish NB=0 for foreign controls outside the 220
stations. A concrete example has

\[
 y_1=u,\qquad y_2=u+q_2,\qquad p=q_1+q_2.
\]

The q1 history-response column is zero, yet `2y1−y2+p=u+q1`. The history
relation reveals q2 and combines with the packet to recover q1. Fixing q2 to
zero would destroy the relevant packet-kernel ambiguity. The independent
checker verifies this example and its row spaces exactly.

## Controls and remaining scope

Further exact examples check the changed initial189 observation, a nonzero
private history response hidden by a common-input displacement, and failure
of the no-gain conclusion when endpoint restoration is dropped. These are
hypothesis controls; the universal argument is the proof above.

The one-receiver theorem does not grant physical packet delivery, arbitrary
history snapshots, owned capacity, local scalar services, raw restoration or
price savings. Common-dependent replacement can change the baseline common
matrix O, and new carrier observations change the observation interface; the
old nullspace cannot be silently reused. Controls at receiver stations may
also invalidate the asserted stable endpoint representation.

Donor 77 is already handled in the separately proved 17-channel partial
construction. The one-receiver theorem alone says nothing conclusive about
the other 87 first-pair channels or a general multi-donor packet code. Such a
code needs its actual joint NB, stable gain, endpoint response, and physical
side information. The general criterion is the appropriate next interface
test.

`REVIEWED-FILES.json` pins both author proofs, their source manifest and this
review. `RESULT.json` records the inherited dependency hashes and exact
controls.

```sh
python check.py \
  --author /path/to/packet-gain-reduction \
  --programme /path/to/research/moonshot-005-program \
  --output /tmp/packet-gain-controls.json
```

Expected status: `PASS_INDEPENDENT_PACKET_GAIN_ALGEBRA_AND_PINS`.
