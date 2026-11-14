# Acquired payloads let the same two packets execute two nested forks

**Proved finite native constructions with explicit arbitrary-input words; author replay complete. Independent review is separate. No new kappa.**

## 1. Result and scope

On the source-pinned 111-role BIT native, there is an actual characteristic-two word completing the eight targets

    92, 36, 54, 38, 55, 23, 1, 18

using the SAME two Hub-born descending packet lifetimes through two successive coupled forks. Every other owned record is stationary. All 222 original input columns are retained in the verification. The eight original X records are restored at Hub before either descending packet is born. The other 103 X records remain on their original source lines and their Y records remain at ground, so this is a continuable partial construction.

The nested word uses 14 INIT, 69 ADD, 56 MOVE and 14 CLEAR, with peak14 owned records. Closing the remaining original paths without changing their values gives the complete partial invoice

    31[1] + 5[2] + 11[3] + 3[5] + 3[6] + 209[7],

of rank length1570, with262 MOVEs. This closure is an accounting/control variant, not a continuation that preserves original access for the unserved103 targets.

A second, alternative word attaches two three-target orthogonal staircases to a payload fork. It completes nine targets with the same two full descending lifetimes, nine owned records,67 ADD and closed profile

    33[1] + 4[2] + 12[3] + 2[4] + 4[5] + 5[6] + 205[7].

Its rank length is also1570. These are alternative source words. Their cost credits are not added.

The new mathematical mechanism is actual future-input acquisition before a fork, followed by reuse of the live packet values at a common proper chart. The nested word's second fork needs an old source coordinate at a new correction chart. A decoder chart outside the common five-dimensional ambient space permits the original ascending X record to supply that coordinate; no extra descending helper is needed.

Nothing here completes all111 targets, constructs a uniform supplier, changes an accepted exponent, or discharges a foundational assumption.

## 2. Model, coordinates and arbitrary inputs

Write x_i,y_i for independent V-dimensional vectors over any field of characteristic two. Let L_i be the real source line spanned by the normalized native root r_i, let F_i=r_i-perp, let Hub=R^8 and let ground=0. Original X and Y records move monotonically upward. Owned records are initialized to zero and may move monotonically downward. An ADD is executed only when its two records occupy the same actual chart. Every owned record is eventually explicitly cleared, including nonzero records.

The words use only additions with coefficient1. Thus the exact 222-column binary replay proves the displayed finite linear map, and the same algebra applies componentwise for every V and every characteristic-two field. No scalar finite test is substituted for the geometric or universal algebraic argument.

All normalized roots are read from recovered geometry blob

    8eba43d142c819c206dce5df87ea4571aaead287

in CubeJerry/integer-mult-bounds. This is the exact signature reconstruction from the admitted flat-cubic certificate, SHA256

    4ac3933fb2393c62a96ec9e931ef4936e61d0e6c912c7ce0a94398a5f19addfc,

ultimately pinned to the native gzip SHA256

    51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78.

The execution-environment outage prevented a new gzip replay. The qualification is derived recovery from an authenticated admitted certificate. The word checker independently verifies every chart rank and inclusion from those recovered integer roots by exact integer elimination.

## 3. Payload fork identity

First use the native pentagon in cyclic order

    (v0,v1,v2,v3,v4)=(92,36,54,38,55).

Consecutive roots are orthogonal. Set

    E_A = F_v0 intersect F_v2,       rank6,
    E_B = F_v0 intersect F_v3,       rank6,
    D   = F_v0 intersect F_v2 intersect F_v3, rank5.

Let a,b be two genuinely acquired fresh X forms supported on D, and put

    p=a+b,
    h=x_v0+x_v1+x_v4,
    H=x_v0+x_v1+x_v2+x_v3+x_v4,
    u=x_v2+x_v3,
    W=x_v1+x_v4+p.

The required stationary records before the fork are:

| Record | Chart | Actual value |
|---|---|---|
| H-cache | F_v0 | zero, then filled from the actual Q packet |
| W-cache | F_v0 | W |
| p-cache | D | p |
| S1 | E_A | x_v1+a |
| S4 | E_B | x_v4+b |
| S3 | F_v2 | x_v3 |
| S2 | F_v3 | x_v2 |

Original Y_v2 and Y_v3 visit D and each add the p-cache, then continue to E_A and E_B respectively. Y_v0 waits at E_A. These are actual visits and ADDs.

At Hub load P=h+p and Q=H from restored originals. Move both to F_v0 and execute

    H-cache += Q
    P += Q
    Q += H-cache
    Q += P.

After this, P=Q=u+p and H-cache=H. Move P to E_A and exchange it with S1 using three ADDs. Move Q to E_B and exchange it with S4. Thus

    P=x_v1+a at E_A,       Q=x_v4+b at E_B,
    S1=S4=u+p.

Now finish three original Y records:

    Y_v0 reads S1 at E_A, then H-cache and W-cache at F_v0;
    Y_v2 reads S1 at E_A, then S3 at F_v2;
    Y_v3 reads S4 at E_B, then S2 at F_v3.

Their X contributions are respectively

    (u+p)+H+W = x_v0,
    p+(u+p)+x_v3 = x_v2,
    p+(u+p)+x_v2 = x_v3.

All arbitrary original y masks remain exactly once. The other two base targets have not yet been completed. The two packets are still alive and now carry the fresh forms a,b. Merely reusing old H/u histories would not have introduced those fresh coefficients; their actual acquisition below is essential.

This identity is a conditional interface when its actual cache values are premises. The following two source words establish those premises without free reads.

## 4. Native acquisition for the nested word

Choose

    a=x23+x18,   b=x1,   p=x23+x18+x1.

All three fresh source lines lie in D. The intended second pentagon is

    (w0,w1,w2,w3,w4)=(36,23,55,1,18).

Its ordinary consecutive orthogonality relations all hold. Define

    N0  = D intersect F36,             rank4,
    N2  = D intersect F55,             rank4,
    N02 = D intersect F36 intersect F55, rank3,
    N03 = D intersect F36 intersect F1,  rank3.

The second-fork correction for Y1 needs x55. For that correction use

    G3 = span(N03,L55), rank4.

Its exact normal basis is

    r92, r38, r1, r54-r36.

Consequently

    L55 subset G3 subset F92 intersect F38 = E_B,
    N03 subset G3 subset F1.

These inclusions are the source-alignment step. The convenient chart D intersect F1 would exclude L55, so original X55 could not ascend there. Replacing G3 by that chart is an explicit rejected geometry control.

Before either packet is born, prepare the future caches

    NS1=x23 at N02,
    NS4=x18 at N03,
    NS3=x1 at N2,
    NS2=x55 at G3,
    NH=0 at N0.

Every cache is acquired on an original ascending route:

* X23 ascends L23 -> N02 -> D, supplying NS1. X18 ascends L18 -> N03 -> D, supplying NS4. At D temporarily replace X18 by X18+X23=a. This accumulator supplies p at D, S1 at E_A and W at F92, then reaches Hub. X23 has continued unchanged to Hub; add it once more to restore X18=x18.
* X1 ascends L1 -> N2 -> D -> E_B -> F92 -> Hub. It supplies NS3, the b part of p, the b part of S4, and the b part of W.
* X36 ascends L36 -> E_A -> F92 -> Hub and supplies the x36 terms of S1 and W.
* X55 ascends L55 -> G3 -> E_B -> F92 -> Hub. It first supplies the future NS2 correction, then the x55 terms of S4 and W.
* X54 ascends through F38 and supplies S2=x54. X38 ascends through F54 and supplies S3=x38. Both continue unchanged to Hub. X92 ascends directly to Hub.

All selected X values are restored before the Hub loads. No unserved original input outside these eight targets is moved or borrowed. Every step of these paths is nested and every supplied value is present at the receiving cache's actual chart.

Execute Section3. After its three outputs are complete, clear the seven old stationary caches. Move P and Q down one rank from E_A,E_B to their common D. At operation108 the literal word has

    P=x36+x23+x18 = h' at D,
    Q=x55+x1 = u' at D,

with the five future caches above already in place. Y36,Y23,Y55,Y1,Y18 still carry their untouched original y values at ground. This is a stronger continuation interface than a static sum-space membership assertion.

## 5. The second fork uses the same lifetimes

At D execute Q+=P. Then Q=H'=h'+u', the total of the five second-pentagon inputs. Move the same P,Q records to N0, and execute the four-ADD fork operation with NH:

    NH+=Q;  P+=Q;  Q+=NH;  Q+=P.

Both packets now carry u'=x55+x1. Move P to N02 and exchange it with NS1; move Q to N03 and exchange it with NS4. P=x23 and Q=x18 then descend to ground.

Complete the five second-pentagon outputs:

* Y23 reads P at ground and ascends to F23.
* Y18 reads Q at ground and ascends to F18.
* Y36 reads P+Q at ground, then NS4=u' at N03, then NH=H' at N0, and continues to F36.
* Y55 reads NS1=u' at N02, then NS3=x1 at N2, and continues to F55.
* Y1 reads NS4=u' at N03, then NS2=x55 at the off-D chart G3, and continues to F1.

The X contributions are x23,x18,x36,x55,x1 respectively. The five original y coefficients remain unchanged. Clear P,Q and the five remaining stationary owners. All fourteen clears are explicit and paid; none is justified by assuming a record is zero.

There is no second Hub initialization and no other descending MOVE. Both packet rank paths are

    8 -> 7 -> 6 -> 5 -> 4 -> 3 -> 0.

Their initial X coefficient space has dimension2. The span of their actually carried X projections AFTER leaving Hub has dimension6, with a possible basis

    x92, x36, x23, x18, x55+x1, x54+x38+x1.

The receipt excludes intermediate loading sums at Hub from this count. Thus the increase is a genuine chronological history increase. It is not a claim about six independent final packets, nor a full111-role fitting.

## 6. Alternative nine-target continuation

For the alternative word choose a=x10+x49 and b=x1+x41. The native classes

    (36,10,49),   (55,1,41)

are mutually orthogonal triples. Their payload source lines lie in D, and are also orthogonal to their class's first target.

For one class (f,s,t), build the original-y prefix masks at ground:

    Y_f=y_f, Y_s=y_f+y_s, Y_t=y_f+y_s+y_t.

Before X_t leaves L_t, let Y_s visit L_t and read x_t. At Q=span(L_s,L_t), temporarily replace X_t by X_t+X_s and let Y_f read that actual sum. The aggregate can then follow Q -> D -> E_A or E_B -> F92 -> Hub, supplying the p/S/W records on the same ascent. Restore X_t at Hub using the unchanged X_s.

The original Y values wait on the three nested class-flag charts. Once the payload fork has produced packet x_f+x_s+x_t, the two-ADD staircase exchange

    Y_i += packet; packet += Y_i

successively completes the three targets. The packet ends as the actual sum of their original y masks and is explicitly cleared. The second branch is identical.

This proves the nine-target word on all222 input columns. Its post-Hub carried X space has dimension8, while its initial packet space still has dimension2. The two alternatives have different payload values, source routes and Y preloads, so one cannot switch between them after their acquisitions without a newly costed conversion.

## 7. Exact accounting, controls and limits

The exact closed profiles and arithmetic certificates are in RESULT.json. At t=199/200 their moments are enclosed by verified rational intervals:

| Alternative | Moment, rounded for display |
|---|---:|
| Nine targets, then close unserved paths | 1555.397788895561080324553876232857 |
| Two nested forks, then close unserved paths | 1555.338556984570100653389065498788 |

Every bound is obtained using integer200th-root inequalities a^200 <= r^199 S^200 < (a+1)^200 with S=10^40. The interval endpoints are retained, not inferred from floating point.

Any partition into isolated one-packet modules in the retained Hub-born full-route grammar requires at least three packets on either target subset, because each includes an induced pentagon and an isolated one-packet module can serve only mutually orthogonal roots. Against the optimistic lower invoice 222[7]+3[8], the nested word saves more than7.366796991599802719702522833870 in movement moment. This comparison does not apply to arbitrary proper-born alternatives and does not price their ordinary/ownership costs as zero.

For the nested partial word, the limiting complete-caller allowance leaves optimistic movement margins10.991550467330668... after seven further bare full routes, or3.074297216009013... after eight. These are necessary budget screens only. No completion of the remaining103 targets within either allowance is supplied. The remaining original X access is preserved in NESTED.json; NESTED-CLOSED.json deliberately removes it only for the closed accounting control.

Negative controls delete essential p reads, source captures, restoration, payload acquisition and the inter-fork basis change. All are rejected. Replacing G3 by D intersect F1 fails the actual original-X route. The finite replay does not prove a uniform native compiler, precision or storage bound. All five foundational premises remain explicit.

The highest-priority continuation is another compatible shared-history handoff that uses the remaining live original inputs and charges every changed source route. The nested word proves that a second fork is possible; it does not prove arbitrary iteration. See CONTINUATION.md for the exact remaining geometric issue.

Prepared for @CubeJerry with substantial OpenAI-assisted research. Credit the programme's admitted pentagon fork and orthogonal staircase, Worker C for the off-D correction chart and independent finite-geometric insight, the lead construction worker for the acquired-payload identity and both literal words, and all source/native/caller predecessors. The storage-code papers in SOURCES.json motivated attention to acquired piggyback values and coupled decoding; none is used as an unproved source-availability premise.
