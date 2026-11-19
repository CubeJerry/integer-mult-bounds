# Completing saturated middle messages with genuine X closures and Y births

## Native local interface

At D, let u in F^nE be its genuine early X values and v in F^nL the proper source contributions on genuine incoming late Y owners. Assume(u,v) ranges over the full product on the proper slice. There are aE continuing early X slots and s=nE-aE>=0 genuine X closures to Hub. The atlas supplies exactly s genuine Y births from ground, so aL=nL+s late Y slots leave D.

The early map is bijective on its nE actual X owners. The late map can read retained u and is bijective on its nL+s actual Y owners for every fixed u. On the proper source slice born Y values vanish and incoming late values equal v. Their arbitrary original baselines are retained in the implemented word.

Receiver i sees a specified continuing-slot collection A_i and demands T_i(u,v) of rank |A_i|. A slot is shared by the native receivers of its one K flag, at most three. Put V_i=row(T_i), let E be the early-coordinate row space, and let pi_L project row vectors to incoming-late coordinates. Define

    Q_a=E intersect(intersection_(i seeing a)V_i), for early slots;
    Q_a=intersection_(i seeing a)V_i, for late slots.

An empty audience gives the full proper input dual before the early restriction. All demands use one common real D input.

## Theorem

Let d be the maximum audience size. The following are necessary for arbitrary deterministic proper-message encoders with the stated two phase bijections:

(H) For every receiver i and subset S of A_i, dim(sum_(a in S)Q_a)>=|S|.

(E) For every subset S of continuing early slots, dim(sum_(a in S)Q_a)>=|S|.

(L) For every subset S of late slots, dim(sum_(a in S)pi_L Q_a)+s>=|S|.

Conversely, if(H),(E),(L) hold and |F|>d+1, a simultaneous linear D word meets every proper demand, preserves an invertible genuine early phase, and has an invertible genuine late phase on arbitrary Y baselines. The literal finite binary invoice is given below. Exactly the retained movements, closures and births are used.

For native d<=3, existing GF16/GF32 suffice. This is a physical D-stage completion conditional on the supplied source/demand spaces, not a solution of source gluing or K delivery.

## Necessity

On the proper slice, saturated common-information makes every slot a function of Q_a. Each receiver tuple has full product range, giving(H). Early bijectivity gives full product range to any subset of continuing early outputs, giving(E).

For(L), fix u=0. The late pure bijection maps the born-Y-zero slice of size |F|^nL injectively into its aL outputs. Any S-projection fibre has at most |F|^(aL-|S|) points, so its projected range has at least |F|^(|S|-s) values. On that proper slice these outputs are functions of sum pi_L Q_a, proving(L). This cardinality argument permits nonlinear encoders; for |S|<=s the inequality is simply weak.

## Simultaneous linear construction

Choose q_a in Q_a for each continuing slot, with independent coefficient variables. Choose s free early closure rows in E and s free born-Y coefficients for each late output. Receiver determinants are nonzero by(H) and independent representatives. Condition(E) supplies independent representatives for all aE continuing early rows, then s free rows complete the nE-by-nE early determinant. Thus that determinant is a nonzero polynomial.

Each pure-late row can be any vector(pi_L q_a,b_a) in(pi_L Q_a) direct-sum F^s. The sum of these allowed spaces over a nonempty slot subset S has dimension dim(sum pi_L Q_a)+s. Condition(L) is precisely the independent-representatives criterion for an invertible aL-by-aL late matrix. Any projected choice lifts to q_a in Q_a. Therefore the pure-late determinant is also a nonzero polynomial.

Multiply all receiver determinants and both phase determinants. Each q coefficient occurs in at most d receiver determinants and one phase determinant, linearly in each. Closure and born-Y variables occur only in one phase determinant. Individual degree is at most d+1, so the finite-grid lemma gives a simultaneous assignment whenever |F|>d+1.

Before the early map, retain a local raw snapshot of u. Apply the invertible early map to actual X owners and use their continuing and closing routes. In the late phase apply the invertible late matrix to genuine incoming/born Y owners, then add q_(a,E)u from snapshots. On the proper slice the continuing values are q_a(u,v), giving all demands. For arbitrary Y values the late map is still invertible and the cross additions are translations for fixed u.

This supplies the phase form used by the retained whole-word restore/preload construction. All other stages, end-to-end identities and source conditions still need their own proofs.

## Explicit finite ordinary invoice

For F=GF(2^w), expand every field value in a fixed binary basis and perform the same binary linear map at every positive whole-record body width. Put M=w*nE and N=w*aL. An invertible binary matrix of order m uses at most m^2+3m ADDs by elimination and three-ADD swaps. Its inverse has the same bound. A dense cross matrix from M cached X records to N late Y records uses at most MN ADDs.

Keeping all early inputs as snapshots costs M INIT, M ADD and M charged dirty CLEAR, with extra local ownership peak M. Include the inverse early block at Hub and inverse late block in the ground preload, as required by the retained global restore/preload word. The corresponding local contribution is bounded by

    ADD <= 2(M^2+3M)+2(N^2+3N)+MN+M;
    INIT = dirty CLEAR = M; extra owned peak = M.

The direct-ground Y births and X closures are genuine public originals already present in the atlas. They are not initialized helpers. This word adds no MOVE. The inverse placements assume the rest of the complete pure phases is composed and inverted as in the existing compiler; the invoice is a local contribution, not a replacement for its entire bill. No compiler, erasure, precision or recursive foundation is discharged.

For the balanced atlas, nE is its left early count, aE is its right early count, and s is the certified middle surplus. For bank480 the identities are nE=l_D, aE=32-l_(Dperp), s=l_D+l_(Dperp)-32 and aL=l_(Dperp), matching the actual original-owner routing. The theorem does not change any of those counts.

## Why all three tests are needed

Receiver tests alone do not force a pure early inverse. Two separate saturated receivers may each demand the same early coordinate from two distinct early slots: their individual tests pass, but those rows cannot be an invertible two-owner early map. Condition(E) catches the duplication.

Likewise, proper late messages can all depend only on early data. If nL=1 and s=1, two such late rows have zero incoming-Y projection, and one born-Y column cannot make the2-by2 pure-late map invertible. Condition(L) rejects this despite successful proper-message tests. Checking only the total projected span is also insufficient: every late subset must have enough projected dimensions after the s birth dimensions are added.

A positive three-input example has nE=2,nL=1,aE=1,s=1. Send u1 early and close u2. Send v on one late owner and u2 on the other proper output; the second has one genuine born-Y baseline. Targets(u1,v) and(u1,u2) are both reconstructed. The early and late pure maps can be identities; one paid u2 snapshot supplies the late cross addition. Arbitrary incoming and born Y values remain in the two independent late owners.

## Verification and next step

`check.py` independently checks all three local rank conditions on exact small examples, exhausts a family of target-plane pairs, replays the positive example on all independent X/Y columns and ordinary binary states, and includes early/late phase failures which the previous information-only receiver tests miss. The written determinant and alphabet proofs cover arbitrary finite dimensions; finite tests are supporting evidence.

The next construction is a complete compatible source/target arrangement satisfying these conditions at every D and the separate K compression tests. Successful local phase completion does not synchronize foreign blocks or establish a low-rank return bank.

Credit @CubeJerry and the native/atlas and restore/preload authors. This extends S027's saturated common-information bridge using the programme's independent-representatives and finite-grid methods. S027 Worker B developed the phase-completion theorem and finite invoice with substantial OpenAI assistance. No new complete kappa or foundational discharge is claimed.
