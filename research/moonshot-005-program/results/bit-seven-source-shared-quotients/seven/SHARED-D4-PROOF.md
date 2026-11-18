# Three shared native D4 ports per pair plane

## Constructive statement

The seven-source F8 construction in PROOF.md can be compiled through
actual shared native D4 flats. For each of its 21 source-pair planes,
three scalar H-to-D4 ports suffice to realize all five distinct required
receiver output rows. Two of the shared messages each serve three native
receivers, including two receivers that decode from both messages. The
third message serves the remaining receiver. Every copy is explicitly
created, moved and retired in the literal word.

The resulting full seven-source word still realizes all 42 required
identity blocks, preserves all arbitrary Y baselines, and restores all
original X. Its exact binary invoice is

    4684 ADD, 567 INIT, 567 dirty CLEAR, 966 MOVE,
    movement profile 126[1]+189[2]+441[3]+210[7],
    peak 132 owned binary records.

There are 42 field source-to-plane queries, 63 field plane-to-D4 ports,
and 147 field D4-to-facet deliveries. This is an explicit shared-middle
realization with genuine native charts. It is a new paid fragment, not
the fixed balanced atlas word, and it does not imply a lower complete
native price or a new kappa. Its additional copies and deliveries remain
in the invoice.

## 1. Exact incidence used

Keep the seven real source and receiver labels from PROOF.md. For each
source-pair plane H={j,k}, its five target receivers are the labels i
outside {j,k}. Among the 45 actual D4 flats containing H, exact native
dot products give the following visibility histogram on these targets:

| Number of these targets containing D4 | Number of D4 flats |
| --- | --- |
| 0 | 10 |
| 1 | 15 |
| 3 | 20 |

Every one of the ten three-element target subsets is seen by exactly two
of these D4 flats. In particular, no available D4 reaches four of the
five receivers. These facts are checked for all 21 actual pair planes;
the word records the selected D4 indices and every selected incidence.

This is a property of the pinned seven-source embedding. It is not a
claim that a D4 has only three receivers in the full native problem.

## 2. Three-port construction

Fix H and denote its two independent source queries by z in F8^2. The
five requested output scalars are c_i z, where the five nonzero two-entry
rows c_i are pairwise nonproportional, as proved in PROOF.md.

Order the five receivers as a,b,c,d,e. Select actual D4 flats D_a, D_b,
D_c whose target visibility sets are respectively

    {a,d,e},       {b,d,e},       {a,b,c}.

Send c_a z to D_a, c_b z to D_b and c_c z to D_c, each in one F8 field
port. The first two rows form a basis of (F8^2)*. Hence unique coefficients
lambda_i,mu_i satisfy

    c_i = lambda_i c_a + mu_i c_b,       i=d,e.

Both coefficients are nonzero because all five target rows are distinct
projective lines. D_a delivers its one scalar to a,d,e. D_b delivers its
one scalar to b,d,e. D_c delivers its scalar only to c. Receiver a, b or c
therefore gets its desired scalar directly; receiver d or e gets it from
the displayed two-message combination. Multiplying these scalar messages
by the original lift v_(i;jk) yields exactly the same plane contributions
as the direct private-output construction.

All three H-to-D4 messages are actual functions of the same two source
queries, chosen once at H. The messages carried by D_a and D_b are shared
unchanged among their receivers; no receiver-specific map is silently
substituted on one shared field. The only receiver-specific operations
are ordinary scalar decoding after the delivered records reach that
receiver's facet.

For the first pair, source indices 0 and 1 in the seven-source ordering,
the actual plane is H20. Its five targets have local indices 2,3,4,5,6.
One certified choice is D1446 for {2,5,6}, D2 for {3,5,6}, and D928 for
{2,3,4}. Their messages have coefficient rows (1,5), (7,2), and (3,1)
over the fixed binary representation of F8. Receiver 5 uses coefficients
(6,7) on the first two messages; receiver 6 uses (5,4). The other twenty
pair planes have equally explicit entries in the word certificate.

## 3. Exact local port bounds

The following bounds concern the isolated interface of one pair plane:
its two queries may vary independently, and its five prescribed scalar
outputs must be supplied using messages whose only dependence on those
queries enters through H-to-D4 ports. Each such port contains one F8
element. Further processing can be arbitrary; no extra side information
about the two queries is supplied. These are local interface bounds,
not lower bounds on the unrestricted full native network, where other
plane queries are correlated with the same original source banks.

**At least three H-to-D4 ports are necessary.** Suppose two suffice. Each
port can reach at most three of the five targets because every subsequent
nested chart containing D4 is still contained in a receiving facet only
when that facet contains D4. If the two sets do not cover all five, the
interface already fails. Otherwise at most one receiver sees both ports,
so at least one port is the sole query-dependent information for two
different target receivers. From that single F8 element one could then
recover two independent linear forms of z. Those two forms distinguish
all 64 values of z, while the port has only eight values, a contradiction.
This argument allows nonlinear port encodings and decoding.

**With three H-to-D4 ports, at least seven scalar D4-to-facet deliveries
are necessary in the direct-delivery model.** A feasible three-port
solution must place its ports at three distinct D4 flats. If two ports
were placed at one flat, its visibility covers at most three targets;
the remaining single port would be the sole information for at least two
different targets and fail by the preceding cardinality argument.

Each D4 thus has only one query-dependent F8 value. A target receiving
one scalar delivery must obtain its full prescribed form from that value.
One D4 value cannot alone support two different target forms. Consequently
at most three of the five targets can receive just one scalar delivery;
the other two require at least two. At least 3+2*2=7 deliveries are needed.
The explicit construction attains both bounds. This second count assumes
the three D4 ports are followed by direct D4-to-facet scalar deliveries;
it does not price alternative merging charts or array-valued encodings.

## 4. Literal schedule and invoice

The source-query stage and original X/Y moves are identical to the direct
seven-source word. This contributes 864 source ADDs and movement profile
126[1]+210[7]. For each plane, form its three shared messages in fresh
owned field records and move each from the rank-two plane to its chosen
rank-four D4 flat, contributing 189 binary moves of rank gap two overall.

At D_a and D_b, create and send two copies one at a time, then move the
original shared message itself to the third target. At D_c, move the
original message to its sole target. All seven delivered field values
are decoded into the five coordinates of Y at their genuine facets and
cleared dirty. The 147 field D4-to-facet deliveries contribute 441 binary
moves of rank gap three. Every D4 copy is made by explicit ADD into an
initialized helper; no fanout is free.

The ADD partition is 864 at source, 645 at pair planes, 252 for D4 copies,
and 2923 at receivers, totaling 4684. There are 42 query-helper lifetimes
and 147 delivered-message lifetimes, hence 189*3=567 binary INIT and CLEAR.
Every retirement is dirty. At peak, 42 source query fields, one shared
D4 message and one copy coexist: 44*3=132 binary records.

The compiler is build_shared.py. It imports the direct compiler's finite
field arithmetic and constants, but has a separate literal schedule and
event replay. The companion native-word-review checker imports neither
compiler and uses exact rational span inclusion for all D4 moves. Both
replayers check all 210 original columns, arbitrary Y baselines, complete
original-X restoration, and every owned lifetime. The independent output
is in native-word-review/seven-shared/RESULT.json.

## 5. Boundary of the constructive result

This word establishes real joint source-query and shared-D4 consistency
on seven actual sources and seven actual receivers, with an exact local
three-port construction at every pair plane. It does not use the existing
balanced source multiplicities or its fixed D4-to-rank-six-to-facet word.
In particular, the direct rank-three D4-to-facet deliveries and fresh
helpers are all newly paid. Extending it across all native source/receiver
roles still requires compatible source coordinates, capacity allocation,
ordinary compilation, and the full retained native boundary contract.

Credit Worker A's initial four-source construction, the native atlas
authors, @CubeJerry, and substantial OpenAI assistance. Constructed by
Worker B during S023; baseline and pins are in DEPENDENCIES.json.
