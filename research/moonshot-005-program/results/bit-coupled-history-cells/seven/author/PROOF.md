# Reuse the two reflected-cell packets for two more actual input points

**Proved seven-target partial source. No complete supplier and no new kappa.** This is a continuation of the same five-target reflected cell, not an independent decoder architecture. Its predecessor proof and exact word remain unchanged in `braided-pentagon`.

Use the same pinned native source and point-prefix builder. The five cycle labels1..5 remain actual indices92,36,54,38,55. Add targets a=110 and b=23. Exact real inner products show that both new source lines are contained in D12345, the rank-three common perpendicular chart of the five cycle roots. The complete native point list in this common chart is {23,41,49,61,110}; the construction uses only110 and23 and grants no other local values.

At zero, normalize these two original Y fields as well by their actual B caches. They require three extra ADDs, giving14 normalization ADDs for all seven. Before changing any of the five cycle y components, precode

    Y_a = y_a+y1+y2+y5,
    Y_b = y_b+y2+y3+y4.

These are six extra actual cocharted ADDs at zero. The earlier seven ADDs then prepare the five-cycle fields exactly as before. Neither new field moves before its final ground read.

After the five-cycle computation has completed Y5 at D1345 but before Y5 leaves, ADD Y5 into P1. At that point P1=y1+x2+x5 and Y5=y5+x5, so P1 becomes y1+y5+x2. Move P1 down one rank to D12345. Complete Y2 there using P2 exactly as before, then ADD this actual completed Y2 into BOTH packets before Y2 leaves. Thus

    P1=y1+y2+y5=:U1,
    P2=y2+y3+y4=:U2.

All five completed Y values remain unchanged. No pure y value was looked up; these Y-only packet masks were obtained by actual completed-output feedback at matching charts. They are arbitrary independent-input expressions, not zero.

Now P1 descends from D12345 to the actual source line of input110, ADDs its stationary pure point copy, and descends to zero. The actual ground ADD Y_a+=P1 gives y_a+x_a. P1 is retired and Y_a ascends to its native facet. P2 similarly visits the actual source line23, reads its real point copy, descends to zero, completes Y_b, and retires. Both point copies remain unchanged. Each path from rank3 to its rank1 point and then zero still has total rank length3, so neither packet needs an additional MOVE relative to its old remaining descending flag.

The new work consists of three core-normalization ADDs, six initial Y precoding ADDs, three completed-output feedback ADDs, two point reads and two target ADDs: exactly16 further ADDs. It uses no additional owned lifetime, no higher owned peak, and no additional total MOVE length. No original X beyond the earlier five restored pivots is needed at Hub by this continuation.

The cumulative unfinished invoice is122 INIT,571 ADD,770 unit MOVE,8 CLEAR, peak117 owned. Seven Y fields are correct at their native facets,104 Y fields remain y+E at zero,23 original pivots remain dirty halfbanks, and the same114 point/core caches remain live. The extra14 moves compared with the earlier unfinished word are the newly completed two original Y paths, which were still pending there.

The closed partial word restores every X, moves every Y to its native facet, and retires every owned field. It has122 INIT,632 ADD,1598 unit MOVE,122 CLEAR, peak117. Its exact map is

    X_i=x_i for all111;
    Y_i=y_i+x_i for i in {92,36,54,38,55,110,23};
    Y_i=y_i+E_i x for the remaining104 targets.

All222 original input columns and all actual chart/ownership conditions are checked. Five new semantic mutants remove each feedback or point-read operation; together with the earlier controls,15 mutants are rejected. Normal/optimized execution agrees. The linear source identity tensors over every characteristic-two field and every positive V; compiler/physical and nonzero-erasure assumptions remain separate.

The actual remaining receiver cut S={8,9,14,15,30,31,59} still has deficit6. Both new completed facets are outside that union, and all point/core observations remain unchanged there. Therefore retiring these two packets still cannot simply consume two of the six or seven global slots first. This is an improved terminal cell or a local reuse interface, not a complete global composition. The earlier cheaper one-pointdrop control for the isolated C5 subproblem remains valid.

Known required Y stops are: Y1,Y3,Y4 each have rank jumps1,1,5; Y2,Y5 have jumps3,4; the two new targets need only a final jump7 after their ground read. P1 has rank jumps1,1,2,1,2,1, while P2 has jumps1,2,1,1,2,1; both have four unit jumps and two rank-two jumps. Their actual permitted coalescings therefore support a whole-cell movement analysis without assuming all Y moves remain unit-refined. Any future decoder adds its own required stops.

Credit @CubeJerry and the native/point-prefix predecessors; Worker C's cycle algebra and independent review; root's coupled-exit guidance; Worker A's completed-Y feedback and actual point refill. OpenAI assistance. No new kappa.
