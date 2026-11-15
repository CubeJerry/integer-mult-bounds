# Four frame deficits exclude a common-ground broadcast completion

**Proved obstruction for a stated continuation grammar. No new κ.** The
retained two-output source cannot be completed by independently exporting
locally formed handoff payloads to ground, even when their receiver access and
local receiver corrections are granted for free. The conclusion holds for both
the coupled and uncoupled source, with an additional free global grant of all
seven donor coordinates. It is not a lower bound for changed source chronology,
intermediate acquisition or arbitrary physical receiver networks.

## 1. Exact model and quantifiers

Fix either open two-output source word from S014 at its recorded handoff. The
native 111-root geometry and its exact source bytes are pinned in RESULT.json.
For every characteristic-two field F and positive integer V, each original
record contains an arbitrary independent V-vector. Existing complete output
roles are 17 and 34. Every other receiver must finally acquire its own x_i while
preserving its original y_i.

The following optimistic continuation is allowed:

1. Every existing ground X-row, namely the eight actual terminal packet rows,
   is globally available. In addition, grant the seven coordinates
   `x16,x19,x38,x49,x50,x56,x57` globally without charging their transport.
   Call their joint rowspace G. This is deliberately stronger than the actual
   two-output handoff; these seven coordinates are not already ground sources.
2. At any actual nonzero handoff cell H, permit arbitrary linear recoding,
   fresh owned copies, and arbitrary use of the actual records at that cell.
   Allow even noninvertible local processing for the lower-bound argument.
   Original X values at Hub are included, with Hub's full rank-eight tariff.
   Adding globally granted G rows to a local payload is harmless and may also
   be allowed. There is no free cross-chart recoding or use of a value that
   exists only in an earlier source snapshot.
3. Each exported whole-V record is formed from that local information and
   sent directly to ground, paying `[dim H]=(dim H)^(199/200)`. A subdivision
   of the same descent with no new information acquisition is also allowed:
   concavity cannot make it cheaper than the direct tariff. Source cells do
   not exchange payloads or acquire new intermediate information before this
   ground broadcast.
4. Once at ground, grant every export to every receiver for free. Grant each
   receiver every original coordinate local to its final facet, free linear
   decoding and free ordinary operations. Each unavoidable baseline Y ascent
   is already charged exactly once in Q2 and remains charged here; impose no
   additional fragmentation or access cost on that ascent. This relaxation
   does not remove a baseline cost and then compare against the old allowance.

All omissions in this model make completion easier. Erasure, precision,
compilation and complete recursion remain outside this necessary movement
test and cannot rescue a movement deficit. This theorem changes none of the
programme's five foundational assumptions.

**Claim.** Any such completion incurs additional normalized descent rank at
least 10 and movement moment at least 9.89. The source's limiting movement
allowance is less than 9.25, so this continuation class cannot reach the retained
target invoice at `t=199/200`, for any fixed even caller multiplicity.

## 2. Four simultaneous identity restrictions

Use the following native role sets:

| Cut | Nonorthogonal frame | Rank of G on frame | Deficit |
|---|---|---:|---:|
| A | 0,14,18,30,69,70,107 | 4 | 3 |
| B | 2,8,9,14,21,46,88,92 | 5 | 3 |
| C | 4,11,12,16,36,37,74,78 | 6 | 2 |
| D | 4,32,35,55,56,89,93 | 5 | 2 |

Within each frame, every root pairing, including the diagonal, is nonzero.
No frame contains a completed role. Thus a receiver in the frame has no local
coordinate from that same frame: every allowed local correction restricts to
zero there. The completed receiver map therefore restricts to the frame
identity. Its required rank is `|frame|V`, whereas G supplies only the stated
rank times V. The four missing ranks sum to

    (3+3+2+2)V = 10V.

The ranks are the same for coupled and uncoupled words. They are calculated
from a literal 222-column replay of the source, not from a proposed terminal
row assignment. Omitting the free donor grant makes the deficits `(3,3,3,3)`;
the theorem retains the stronger grant and the weaker sufficient bound 10V.

For a handoff cell H, let `a(H)` count frames on which at least one actual local
X-row survives modulo the restriction of G. Any locally recoded V-record can
increase total rank across the four frame restrictions by at most `a(H)V`.
This remains true with arbitrary F-linear block coefficients: if every local
scalar row lies in the binary rowspace G on a frame, all its block-linear
combinations lie in `G tensor F^V` there. If the local space is not contained,
one V-record can add at most V dimensions.

After any collection of exports, rank subadditivity therefore gives

    10V <= sum_exports a(H) V.

Subsequent receiver mixing cannot create an additional X-row outside the
span of supplied information and local corrections, so it does not avoid
this requirement. Projecting away the arbitrary original y-columns only
strengthens the continuation and is legitimate for this necessary X-rank test.

## 3. Every handoff cell has a(H) <= dim H

The exact source has only three relevant cell types:

- **Point cells, dimension one.** Their actual records are the original point
  copies `Rj=x_j`. Their active point sets in cuts A–D are respectively

      A: {0,30,69,70,107}
      B: {2,8,9,21,46,88,92}
      C: {4,11,12,37,74,78}
      D: {32,35,89,93}.

  These sets are disjoint. Even where the displayed frames share a role
  (14 or 4), that coordinate is already in G on one of the two restrictions.
  Hence each point cell can contribute to at most one cut.
- **The dimension-three cell D31.** Its actual nonzero local raw information
  is the row `x72+x77`; all other retained raw-cache rows there vanish. This
  row restricts to zero on all four frames, so `a(D31)=0`.
- **All other nonzero handoff cells have dimension at least four.** There are
  only four frame restrictions, so `a(H)<=4<=dim H` even if arbitrary payloads
  were granted at those cells. Hub and its actual original X values are among
  these cells and retain dimension eight.

There is no nonzero dimension-two handoff cell. The complete exact cell
inventory and activity matrix appear in RESULT.json. Ground contributes only
the already granted G and therefore has no new activity.

Combining the activity bound with the four required rank increments yields

    sum_exports dim H >= 10.

This is a universal inequality for the stated fixed-source grammar, not an
inference from a failed finite search. The finite work checks the explicit
geometric and linear-algebraic premises of that inequality.

## 4. Exact movement comparison

For every integer `1<=d<=8`, the exact integer inequality

    8 * 989^200 < 1000^200

implies `d^(199/200) > (989/1000)d`. Consequently the added movement is
strictly greater than 9.89. The frozen directed price certificate for Q2 gives

    additional limiting room
    <= 3697537037616963921386505817509494970999509789
       /400000000000000000000000000000000000000000000
    = 9.24384259404240980346626454377… < 9.25.

The deficit is at least `9.89−9.243842594… > 0.6461574059…`, before any new
ordinary, storage, initialization/erasure, compiler or precision expenses.
Finite even caller multiplicity has a smaller allowable source moment than
the limiting invoice, so it cannot remove this contradiction.

## 5. Verification, controls and constructive consequence

```sh
python3 -B check.py --repo /absolute/path/to/integer-mult-bounds
```

Expected status: `PASS_FOUR_FRAME_GROUND_BROADCAST_OBSTRUCTION`.
The standard-library checker derives actual rows by source replay, verifies
the geometry blob, reconstructs rational cell equivalence, checks all four
frame Gram restrictions and all local-cell activity bounds for both variants,
and checks the exact integer price inequality. It preserves the qualification
that native-gzip reconstruction and full source MOVE legality are inherited
from the admitted predecessor, rather than claiming a new full native replay.

Negative controls inject an uncharged cross-chart row into a point cell,
inject a four-cut row into D31, and place an already completed role in a frame.
Each is rejected. Removing one cut lowers the certified deficit to seven;
the complete point-coordinate broadcast spans the identity as a positive
high-cost control. Independent review must rederive the proof and witness,
not merely rerun this author checker.

The remaining constructive direction is now more specific: a successful
decoder must use destination-sensitive delivery, further source chronology,
or genuine intermediate interaction that changes the flat broadcast premise.
Merely selecting different existing cache rows, granting arbitrary local
recoding, or adding a cheap common-ground broadcasting suffix cannot suffice.
This theorem does not exclude those changed mechanisms and does not assert
a general lower bound for multiplication.

Credit: @CubeJerry; S014's retained two-output source, actual chart geometry,
shared-export and fixed-frame source-cut authors; S015 construction worker's
four-cut composition and exact tariff certificate. Substantial OpenAI
assistance. No new complete supplier or κ.
