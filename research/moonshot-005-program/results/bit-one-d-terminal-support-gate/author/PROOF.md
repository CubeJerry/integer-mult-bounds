# A complete target gate for terminal packets that retain one D provenance

## 1. Restricted architecture and theorem

Fix the actual native proper diagram, an original source bank F^b at every native donor, and a receiver i. The proper word is evaluated with the independent original ground input fixed to zero; its linear endpoint map is B. A separately paid replacement return bank is not included in B. The completed fitting is I+B, with native diagonal identity and zeros at nonforeign pairs, as in the admitted replacement-bank theorem.

Suppose the entire proper information arriving at F_i consists of L_i field symbols. Each arriving symbol is a deterministic function of the original inputs of at most s donors. More generally partition the arrivals into packet groups a of c_a symbols, each depending on a specified donor set S_a, with sum c_a<=L_i. Receiver processing and packet encoders may be nonlinear. Every informative arrival or bypass must be included; stationary copies of previously arrived values are not additional information.

**Support gate.** For any linear proper endpoint decoded from those arrivals,

    sum_(j foreign to i) rank B_ij
       <= sum_a |S_a intersect N(i)| c_a.              (1)

In particular the right side is at most s L_i when every group has at most s native donors.

**Proof.** Fix every donor except j. Arrivals whose support sets omit j are constant. The remaining arrivals have at most |F|^(sum_(a:j in S_a)c_a) possible tuples. The required endpoint takes |F|^(rank B_ij) values. Exact decoding therefore implies rank B_ij<=sum_(a:j in S_a)c_a. Sum this finite collection of inequalities over j and exchange the sums. No independence of packet groups is assumed, and no rank sum is interpreted as a MOVE fee. QED.

The native D4 chart contains twelve parent root lines and at most twelve native donors. Thus a word in which every incoming F_i packet still depends only on source information from one D has s=12. Arbitrary source masks and mixing inside that D are permitted. Arbitrary processing of its own packets at K is permitted. Mixing several D contributions at K can create a packet supported on their donor union and is outside this twelve-donor specialization.

The restriction concerns values and their source dependence, not the original owner's D label. A packet formed by adding values from several D charts is not a one-D packet merely because it occupies an owner whose route began at one of them.

## 2. The existing target and near-minimum fitting premise

For the S027 irreducible target B*, all foreign blocks are invertible. Receiver80 has 62 foreign donors. Therefore a complete target code in this restricted architecture requires

    62 b <= 12 L_80.                                  (2)

The pinned b=480 routes have exactly 360 original early X arrivals and 480 late Y arrivals at F80, so L_80<=840=7b/4. Their early snapshots and arbitrary local calculations cannot increase this alphabet budget. Thus the right side of (2) is at most21b, a contradiction. No number of one-D masked tiles can complete this receiver while retaining that incoming-support restriction and the same terminal invoice.

This is also an obstruction to any cheap replacement-bank completion in the class, not only to B*. The admitted `bit-near-minimum-foreign-rank` theorem covers arbitrary nonsymmetric native fittings over characteristic two, including noncommuting and singular foreign blocks. If

    rank(I+B)=9b+h,

it proves rank B_ij>=b-floor(c_ij h), with c_ij<=9/2 on all 6,470 directed foreign pairs. The zero-ground proper map and the independently paid return are precisely the interface used here; no old canonical-zero slice is assumed for a changed bank.

Combining the uniform coefficient with receiver80 gives

    62(b-floor(9h/2)) <=21b,
    h/b >=41/279.                                     (3)

At b480 this requires h>=71, already beyond the current allowance16. Formula (3) is a sufficient class obstruction; it is not a universal fitting bound or a bound on codes with shared K aggregation.

## 3. Stronger exact inherited coefficients

The admitted per-pair certificate provides more than the uniform coefficient. Receiver26 has 60 foreign donors, 360 early terminal arrivals and 480 late arrivals. Fifty-seven of its foreign blocks have c=3; donors49,86,93 have c=7/2. Hence

    57 max(0,b-3h)+3 max(0,b-floor(7h/2)) <=21b.        (4)

In particular, discarding floors in the direction that weakens the bound gives

    60b-(363/2)h <=21b,
    h/b >=26/121.                                    (5)

Receiver34 has the same profile, with exceptional donors8,40,82. Receiver80's coefficient sum is14239/72, giving h/b>=2952/14239; (5) is a slightly stronger convenient witness.

For integral copies of the pinned bank480 routes, the exact first h passing the necessary inequality (4) is:

| Bank b | Necessary h | Inherited target allowance for comparison |
| --- | ---: | ---: |
| 480 | 104 | 16 |
| 1920 | 413 | 67 |
| 5760 | 1238 | 202 |

The second and third rows describe four and twelve integral copies of these actual routes. They do not silently identify a different previously published atlas with this copied one. The ratio obstruction is invariant under these copies. The rightmost values are the programme's previously certified finite screens, not new certificates produced here.

The normalized proper movement profile of the bank480 atlas is retained. The near-minimum package bounds the limiting movement room at exponent199/200 by279/1000, while 8^(199/200)>7. The excess contribution forced by (5) is greater than7*26/121=182/121, already greater than279/1000. Thus movement alone excludes this class at the target before ordinary, storage, precision or recursive costs. No rearrangement of the ordinary invoice can repair this deficit.

## 4. Why shared K aggregation is a substantive escape

If two disjoint twelve-donor packets arrive at K, an invertible two-owner shear can replace the first value by their sum and retain the second. Sending the first to F gives one arrival depending on twenty-four donors. Its alphabet is still one field, but its support size is twenty-four. Applying s=12 to that arrival would be false.

The actual native tiles12,99,549,600,968 all have an exit through K370. Their native donor union has31 members. A common K aggregate can therefore have source support31. This verifies a genuine change in the relevant information architecture; it does not establish the entire target. Shared source coordinates, the actual K phase inverse, output decoding, all other endpoints and the complete return rank remain separate.

The new S027 frame-coded stitch deliberately uses this escape. The support gate excludes extending the preceding pass-through masked tiles as independent terminal packets. It does not exclude the new cross-D K sums or arbitrary global native codes.

## 5. Evidence, controls and status

`check.py` reconstructs native orthogonality and terminal arrivals from the immutable root and full route tables. It verifies the selected coefficient profiles against the admitted all-pair certificate, computes the exact inequalities with fractions and floors, and independently checks the five-D common-K witness. It also exhausts4,096 small binary linear packet/decoder cases, attains the abstract support bound, and exhibits a valid shared-K operation that violates an incorrectly applied twelve-donor assumption.

The general support theorem is an alphabet proof. Finite checks establish only the displayed native incidence, capacity and certificate premises and support the proof with explicit controls. This is a scoped obstruction, not a new multiplication exponent. All five foundational assumptions and the full caller remain open.

Credit @CubeJerry and the native atlas, near-minimum fitting and irreducible-target authors. Root proposed the target-first terminal support screen; Worker B supplied the full packet/decoder scope, sharper actual terminal counts, inherited-coefficient specialization, and exact controls. Worker A's five-tile K construction supplies the concrete escape witness. Substantial OpenAI assistance was used.
