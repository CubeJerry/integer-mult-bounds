# Independent audit of the eight actual seed packets

**PASS for the stated acquisition and handoff. No Y output is completed by
this word. No complete supplier and no new kappa.**

The independently replayed source extends the three-mode source reviewed in
`TRIPLE-REVIEW.md` by adding five literal seed packets. All 111 originals are
restored at Hub before any packet birth, and all 111 actual point copies are
retained. The eight starting rows are K1,K3,K5,K10,K11,K15,K30,hK0. Their rank
is eight. The first three packets make the previously proved cyclic
8->7->6->5->0 paths; the other five make actual 8->0 paths. All seed terms
are loaded from live, restored originals at Hub.

The terminal code has rank eight. The span of every actual packet value
after leaving Hub has rank 18, intersection with W of dimension 11, and
seven directions outside W. In particular, historical dimension is not a
terminal packet count. The checker does not identify those two interfaces.

The complete owned handoff consists of 111 point copies, ten local caches
and eight packets. All X values are restored and all Y values remain y_i.
The closed partial word has 129 INIT, 655 ADD, 300 MOVE and 129 CLEAR
operations, peak 129 owners, no live owners and rank length 1618. Its exact
movement profile is

    41[1]+21[2]+8[3]+11[4]+24[5]+23[6]+167[7]+5[8].

At t=199/200, the independently computed integer-root bracket gives
1603.494282103596485... . This is a movement moment, not a complete recursive
supplier price. The other cost contracts and the unserved Y outputs remain.
Dirty CLEAR relies on the retained owned-erasure premise.

The replay checks all 222 independent input columns and exact rational
chart inclusions. It uses only independently authored utilities and derives
every handoff value from the root geometry. Tensoring the verified 0/1
formal identity with I_V proves it for arbitrary positive width and
characteristic-two field. Five focused additional mutants reject a missing
term in either a canonical or filtered extra seed, an extra packet ending
at the wrong chart, birth before original restoration and a restarted owned
packet lifetime.

The separate full-history closure screen in `EIGHT-RESULT.json` grants all
historical rows free global availability. It fits 38 of 111 receivers; the
terminal eight rows fit 14. Neither count is a delivered-output claim.
The accompanying history-bridge proof makes the scope and remaining
information/transport obligations explicit.

```sh
python research/moonshot-005-program/work-in-progress/2026-11-15-S014/worker-c/review-a/eight_check.py --source research/moonshot-005-program/sessions/2026-11-14-S013/cloud/SOURCE-RECOVERY.json --words research/moonshot-005-program/work-in-progress/2026-11-15-S014/worker-a/eight-output --output /tmp/eight-independent.json
python research/moonshot-005-program/work-in-progress/2026-11-15-S014/worker-c/review-a/eight_negative_check.py --source research/moonshot-005-program/sessions/2026-11-14-S013/cloud/SOURCE-RECOVERY.json --word research/moonshot-005-program/work-in-progress/2026-11-15-S014/worker-a/eight-output/WORD.json --output /tmp/eight-negative-independent.json
```

Expected statuses are `PASS_INDEPENDENT_EIGHT_PACKET_AND_HISTORY_REVIEW` and
`PASS_INDEPENDENT_EIGHT_PACKET_NEGATIVE_CONTROLS`.
