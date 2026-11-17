# Actual four-arrival repair of the binary complementary-frame circuit

**Positive source-aware receiver service, subject to independent admission.**
This word changes the no-additional-arrival premise of the three-round gate.
It captures two actual pure pair sums early, then pays four owned ascents
from their rank2 capture planes to rank5 service charts. Eight receivers gain
five native correction terms each. The eight already-complete coordinate Ys
stay at ground. No new diagonal output, complete supplier, or cost dominance
is claimed.

## Source and actual pair captures

Parent: the admitted full-half reservoir, SHA256
`6f1bd8465c7a4fa5b7b59888fb5dbd9bbbb88dc3306c984bd71497fd4be7d980`.
Use A=[14,17,19,20] and B=[96,101,99,102], with indices modulo four.
The extra modes are x_B0+x_B2=x96+x99 and x_B1+x_B3=x101+x102.
The first pair lies in the parent's direct proper half H12_0; the second
lies in H12_1. Before either pair's originals leave their native lines,
move both to their rank2 span, add one original into the other, initialize
two zero-owned copies and load them from that actual sum, then repeat the
original ADD to restore both originals. Continue the parent's literal source
word. Each original's new rank2 stop lies inside its already-planned rank3
half chart. No past read, hypothetical grant, or lost X restoration is used.

There are four new owners, two per mode. Their complete birth, load, movement,
service and retirement are present. All111 original X records finish raw at
Hub, and all parent code/half/axis fields are retained at the actual cut.

## Binary network and arbitrary baselines

Let B^A_i and B^B_j denote the actual pre-service Y baselines, including all
independent original Y variables and existing axis corrections. The forward
Y network has twelve ADDs:

    Round1: Y_Ai += Y_B(i+1), for i=0,1,2,3.
    Round2: Y_B(i+2) += Y_Ai, for i=0,1,2,3.
    Round3: Y_Ai += Y_B(i+3), for i=0,1,2,3.

Apply the exact reverse twelve ADDs while all eight records are still at
ground. Next seed Y_Ai from actual NATIVE_Bi at L_Bi, and Y_Bi from actual
NATIVE_Ai at L_Ai. Every forward meeting is an actual common chart, of ranks
2,4,6 in the three rounds.

Before round3, inject R_j=x_B(j-1)+x_B(j+1) into Y_Bj. Direct propagation
then gives

    Y_Ai = B^A_i + sum_(k!=i) x_Ak + x_B(i+1)+x_B(i+2),
    Y_Bj = B^B_j + sum_(k!=j) x_Bk + x_Aj+x_A(j-1).

The injected terms are X-only and do not alter the Y matrix. The reverse
ground network and forward network compose to identity on all arbitrary Y
baselines. Every displayed new X term is native to its receiver: the eight
frame lines form an orthogonal basis and the own line never occurs.

## Proper geometry and paid upward service

After round2, Y_Bj occupies the rank4 span of

    A_(j-1), A_j, B_(j-2), B_(j-1).

Adjoining the pair plane of R_j gives the rank5 chart E_j spanned by these
lines and B_(j+1). This chart is contained in F_Bj and in the final rank6
rendezvous with A_(j+1). Its rank2 pair owner moves upward to E_j, paying
gap3, and Y_Bj moves rank4 to E_j and reads that actual owner. Both public
records then reach their final common rank6 chart. Thus the information
arrival occurs before round3 and is not retrospectively commuted through it.

The interpreter uses the already reviewed paid nested-owner contract:
owned moves may go in either nested direction, each charged by the absolute
rank gap to exponent199/200. All public moves remain upward. Exactly four
new owned upward moves occur; the parent's36 downward unit moves are unchanged.

## Complete invoice and endpoint checks

Relative to the parent, the movement difference is

    40[1] +8[2] +4[3] -8[7].

Its parts are: the four original pair-capture stops add8[1]-4[2]; the eight
public paths through ranks0,1,2,4,6,7 add24[1]+16[2]-8[7]; the four additional
rank5 stops add8[1]-4[2]; the four owned ascents add4[3].

The complete profile is179[1]+111[2]+4[3]+103[4]+111[7]. The complete primitive
counts are188 INIT,1400 ADD,508 MOVE,188 CLEAR, with peak188 owners. The moment
is1590.79710755293444199481533912544866150194031 to the certified outward
interval in RESULT. The increment is12.42112100005385144756701655205117119621302;
necessary limiting room is30.953772658217913251430811241546324945974811 to the
recorded outward interval. Every owned retirement is included.

At cut1985 there are410 live fields. Exactly103 public Ys remain at ground,
including all eight completed axes; the eight serviced Ys are at rank6.
The new native foreign terms number40, giving452 across the103 unknown
receivers. The all222-column replay verifies arbitrary-Y identity, all original
X restorations, all ADD coincidences, all route containment and complete
endpoints. Seven omission controls reject missing capture, source inverse,
ground inverse, native seed read, forward network ADD, owned ascent, or pair
service. This is not a claim that452 terms finish the receivers or that the
remaining room suffices for their continuation.

Reproduce with:

    python workers/A/build_four_arrival_frame_repair.py --repo source \
      --parent workers/A/full-half-reservoir/WORD.json --out /tmp/frame-repair

The builder depends on the pinned native geometry and interval helper, A's
existing all-column interpreter, and its reviewed explicit nested-owner
extension in review_owned_upward_rebase.py. The new word's source, service,
cleanup and complete invoice are all concrete. Independent review determines
admission; absent review this package remains a precisely specified WIP.

Worker A, S020, 2026-11-17. Credit root's complementary-frame proposal,
Worker C's independent algebra check, retained source authors and reviewers,
and substantial OpenAI assistance.
