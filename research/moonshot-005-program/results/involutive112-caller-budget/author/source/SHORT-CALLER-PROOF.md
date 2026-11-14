# An E-free eight-stage, four-query caller in binary dimension eighteen

## Status and precise result

**Proved:** for each integer `a>=1`, two chains of `2a+1` arbitrary public inputs admit the E-free middle and full endpoint identity proved below. The literal `a=4` realization has 18 independent input roles, eight HOST2 stages, exactly four nonself QUERY calls and twelve whole-body idles. Its exact endpoint is diagonal over `Q(i)[Q,D_1,...,D_8]/(Q^4-1)`, with no sampled or idempotent stage symbols. The attached replay establishes the displayed finite matrix identity exactly; the argument below explains its universal parameter and operator meaning.

**Conditionally proved interface:** an h18 native satisfying the specified all-type-A HOST2 contract composes with this caller in ambient dimension 154. At all 208 legal two-tag P104 labels, every contact, target and idle has the stated whole-job geometry. The interface does not construct that native or its decoder. In particular, the favorable direct-row moment is not a supplier certificate. All compiler, uniformity, precision, ownership and framework assumptions remain explicit. **No new kappa.**

The actual source word is `a4-h18/CALLER.json.gz`. It contains 601 events: 301 ADD, 8 HOST2, 12 IDLE_ONE, 58 LAMBDA, 4 QUERY, 46 SCALE and 172 SWAP. Every public input may be arbitrary. There is no empty productive role, initial-zero role, QSELF operation or copied input. All 208 product ports are type A; no type-B saving is claimed.

## 1. Provenance and nonduplication

The chain sites and the chain-merge idle mechanism are inherited from DreamingOfClouds' `research/p104-chain-nested-root/{chain_root.py,PROOF.md}`, whose credit records Cinna Davis, Ali Romman, thu-nmrc and zxv, including thu-nmrc's whole common idles. Exact bytes and Git/SHA256 pins are in `source/PINS.json`. The earlier `root_A_efree.json` is an eighteen-stage two-chain source. The archived files named `hyb_h4`, `hyb_h6` and `hyb_h8` also each have eighteen stages: their names do not certify short callers.

The three-query four-input identity is also inherited from the @CubeJerry package `research/p104-query-only-interval/PROOF.md` (section 2); its general q^4 version specializes to the involution gadget below. We reuse that mechanism and give an explicit paired-middle factorization for the parity-uniform chains. The contribution here is the parity-uniform E-free extension, its complete literal eight-stage specialization, and the h18 whole-job interface, not the discovery of the three-query gadget. The programme's earlier four-call dyadic native-entry package is a coupled native-entry construction and is not this stage-shortening identity. The legal two-label tensor and its optimistic moment were retained in the preceding S012 preflight; this package replaces the hypothetical eight-stage caller premise by an actual formal source. Credit @CubeJerry, the inherited source authors and the programme's earlier reviewers. OpenAI assistance was used.

## 2. One chain and the parity-uniform E-free middle

Let S be any central involution over a characteristic-zero coefficient algebra. One chain has coordinates `A,F_1,...,F_a,H_1,...,H_a`. For a column x and row y, write `R(x,y)=I+(S-1)xy`.

At left site `i=1,...,a`, use

    x_i=A+F_i+2 sum(j<i) F_j,       y_i=A*−F_i*.

At right site `i=1,...,a`, in increasing order, use

    x'_i=−A+H_i+2 sum(j>i) H_j,    y'_i=A*+H_i*.

All these rank-one terms are square zero. Put `epsilon=(-1)^a` and

    w=A+sum F−sum H,              e=A*,
    v=−A+2 sum H,
    y=(1−epsilon)A*−epsilon sum(i=1..a)(−1)^i F_i*
                         −sum(j=1..a)(−1)^j H_j*.

Then `e(w)=1`, `y(v)=y(w)=0`. Insert, in chronological order,

    U_1=I+(S−1)we,                U_2=I+(S−1)vy.

**Lemma.** Right sites times `U_2 U_1` times left sites equals `S I`, for every positive integer a.

*Proof.* Use the central idempotents `(1+S)/2,(1−S)/2`. At S=1 every map is identity. At S=−1, write L and R for the left and right site products. Direct triangular substitution gives, with `Falt=sum(-1)^i F_i` and `Halt=sum(-1)^j H_j`,

    L^-1: A -> (2−epsilon)A+2Falt,   F_i -> −F_i+2A, H_j -> H_j;
    R^-1: A -> epsilon A+2Halt=:A',  H_j -> −H_j−2A', F_i -> F_i.

Thus `C=R^-1(−I)L^-1` has

    A_C=(1−2epsilon)A−2epsilon Falt−2Halt,
    F_i,C=F_i−2A,
    H_j,C=H_j−2A_C.

Multiplication of `(I−2vy)(I−2we)` gives exactly these coordinates. This is `U_2 U_1` at S=−1, so `R U_2 U_1 L=−I`. Both idempotent components prove the claim. No parity restriction on a is used. QED.

## 3. A four-query paired middle

Take two disjoint chains A and B. Subscripts identify the chain. Put `s_A=v_A+w_A=sum F_A+sum H_A`, and define SS to scale directions w_A,w_B by S while fixing their common complementary kernel. Their coordinate duals are e_A,e_B. In particular, `SS^2=I`, `y_A SS=y_A`, and `SS v_A=s_A−S w_A`.

Write `Query_A=I+S v_A y_A`. Since `y_A(s_A)=y_A(w_A)=0`,

    Query_A SS = SS (I+S s_A y_A)(I−w_A y_A).

The full paired middle is

    (I−v_B y_B)(I−v_A y_A) Query_B Query_A SS.

It suffices to apply an ordinary `(I−w_A y_A)`, then the three-query gadget below implementing `SS(I+S s_A y_A)`, then one Query_B, then the two ordinary factors `(I−v_A y_A),(I−v_B y_B)`.

Use ordinary coordinates `(a,b,c,d)` in directions `w_A,w_B,s_A,z`, where `y_A(z)=1`, `e_A(z)=e_B(z)=0`; remaining coordinates lie in the common kernel. This is an integral unimodular basis: take a nonroot coordinate p with `y_A[p]=±1`, put `z=e_p/y_A[p]`, choose another nonroot r, and complete with `e_j−y_A[j]z` for j other than p,r, plus the nonroot B coordinates. The omitted r is supplied by s_A, whose r coefficient is one.

For arbitrary input `(a,b,c,d)`, set by ordinary operations

    (w1,w2,w3,w4)=(c,a+d,b+c,d).

Apply exactly three S queries:

    w1 += S*w2;
    w2 += S*(w3−w1);
    w3 += S*(w4−w2).

Each parenthesized source is formed by an ADD and restored after its query. Replace w1 by `w1−w3`. Substitution using only `S^2=1` gives

    (S*a, S*b, c+S*d, d).

This is the required combined map. Query_B is one nonself S query in a unimodular basis completed from its square-zero column/row. All basis changes use integer ADD, SWAP and multiplication by −1. No register is assumed empty.

## 4. Fresh stage factors and whole idles

At left site i, the stage support is `M_i={A,F_1,...,F_i}` in each chain. At right site i it is `M'_i={A,H_i,...,H_a}`. Put `Delta=I+(D−1)P_M` for each fresh, commuting stage symbol D. The stage projector commutes with its site map. For an L site, the prefix is supported within M; the full root endpoint is S times identity, so P_M commutes with the remaining suffix. For an R site, every subsequent R site lies in M. Moving all Delta factors to the left therefore gives a diagonal endpoint:

- A receives every stage;
- F_i receives left stages i through a;
- H_i receives right stages 1 through i.

The same argument applies to the paired stage projector on both disjoint chains, including the middle which mixes chains only in its implementation.

At left stages i>j, the line `phi=F_j` with dual `gamma=F_j*−2A*` is killed by both sides of the site's rank-one term. At right stages i<j, use `phi=H_j`, `gamma=H_j*+2A*`. These lines are mutually dual-orthogonal and lie in every stage support they cross. Each stage support splits as the active two-plane plus these idle rank-one projectors. Their commuting stage factors telescope to a single whole idle with the product of its distinct D symbols. This is precisely the inherited chain-merge lemma, with its hypotheses verified by the displayed formulas.

Each of the two chains has a−1 left and a−1 right whole idles. Their lengths are 1,...,a−1 once per side. Consequently there are four idles of each length j=1,...,a−1, and no repeated stage axis within an idle. The productive masks give two targets of body length 2a and four targets of each length j=1,...,a.

## 5. Literal Q^4 lowering and the native macro

Let `Q^4=I` and

    lambda_±=((1±i)I+(1∓i)Q^2)/2,  S=lambda_+ Q^-1.

Then `lambda_+ lambda_-=I`, `lambda_+^2=Q^2`, and `S^2=I`. These lambda maps are ordinary operations: Q squared is the retained translation/monomial operation. They incur real finite ordinary work but no Gaussian child. They are never declared free in a complete recurrence.

One S query is the literal sequence `LAMBDA(dest,-); QUERY(dest,src,-1); LAMBDA(dest,+)`. The source and destination are distinct and are preserved as specified by an ordinary shear.

The all-type-A HOST2 contract at stage j, on four distinct arbitrary mains `(X,Y,U,V)`, is

    X -> D_j X,       Y -> D_j(Y+Q^-1 X),
    U -> D_j(U−Q V),  V -> D_j V.

Pre/post lambda_- / lambda_+ on Y gives +S in the first plane. Pre/post `−lambda_+ / −lambda_-` on U gives +S in the reverse plane. An ordinary ADD −1 after each shear gives coefficient S−1, so the macro supplies exactly the two active planes in section 4. End each public role with lambda_- to change the root's scalar S to Q^-1.

Thus the output of each of the 4a+2 roles is `Q^-1 product(j in its mask)D_j` times its own independent input, and all other input coefficients are zero. `replay.py` checks all coefficients with each D exponent retained exactly. Evaluation at Q=1,i,−1,−i is faithful because Q^4−1 is square-free and splits over Q(i); it is an exact algebraic identity check, not a numerical sample. These symbols may be replaced by arbitrary commuting operators satisfying Q^4=I. In particular, the identity holds at every dyadic width under the retained native and whole-job contracts; scalar coefficients occur once outside tensor lifts.

## 6. Whole-job geometry at all 208 two-tag labels

Take the actual 104 live P104 labels from the native source pinned by SHA256 `2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883`. The source is an input solely for those labels; its original h9 word is not presented as an h18 word. The two-tag set is `(q,0),(0,q)` in F2^18. It consists of 208 distinct odd labels spanning dimension eighteen. The two tag subspaces are orthogonal. The legal two-label factor has identity binary pairing and ordinary decoder J_2; tensoring a legal base decoder M gives `M tensor J_2`. This row identity alone does not pay for native acquisition or correction.

For each q choose an orthonormal binary basis `(q,b_1,...,b_17)` of the head space. `geometry.py` supplies and exactly checks such bases for every port. It starts with q, then selects an odd vector in the remaining orthogonal complement other than that complement's characteristic vector whenever its dimension exceeds one. This keeps the complement nonalternating. If the only odd vector in a chosen basis is the characteristic vector, adding any nonzero even basis vector supplies an eligible odd vector. At dimension one the sole odd direction finishes. Initial dimension eighteen has even characteristic vector, so the first odd q never obstructs this procedure.

At stage j put seventeen fresh orthogonal axes `E_j` beside the head and all previous fresh axes. Use the common chart

    C_j=span(b_1,...,b_17,E_1,...,E_(j−1)).

Embed the native head by fixing q and sending its orthogonal complement to E_j. The prospective boundary charts are

    X_in=C_j+<q>,       Y_in=C_j,
    X_out=C_j+<q>+E_j, Y_out=C_j+E_j.

The same applies to U,V in the reverse plane. Thus both diagonal phase differences are exactly E_j, the forward cross difference is `E_j−q`, and the reverse difference is `E_j+q`. These are the desired `D_j`, `D_j Q^-1`, and `D_j Q` coefficients, including their absolute signs.

Changing between the selected orthonormal head basis and the standard basis introduces only an explicitly computable ordinary translation. Indeed, modulo four, the difference between the sums of coordinate parities has even linear coefficients and zero quadratic coefficients: orthonormality makes every off-diagonal column inner product even and every column weight odd. Its translation mask has jth bit `(column_weight_j−1)/2 mod 2`. The same correction occurs at all four boundaries, so no new Gaussian query is hidden in this adaptation. The checker records every basis and correction and checks all 6656 absolute boundaries. It rejects a missing head term and a duplicated fresh axis.

Each productive role has a complete Gaussian job on q and its selected fresh stage blocks, of rank `1+17|mask|`. Its Q^-1 orientation differs from the positive orientation by an ordinary translation. Each whole idle has rank `17|mask|` on disjoint fresh axes. At width V the ranks multiply by V, with fixed scalar coefficients and fixed permutations. The maximum productive rank is 137 while the working ambient is 154; these are distinct quantities.

All 208 ports use four distinct native mains at each of eight calls. Map the native main `(port,plane,source/destination)` injectively into that port's active caller role. Helpers of any future h18 native must be fresh at each invocation and receive their own complete invoice. Type B is not needed and supplies no credit here.

## 7. Exact wrapper invoice and the missing native source

Per port, the literal a4 caller supplies

    T_wrapper={18:4,35:4,52:4,69:4,137:2},
    P_wrapper={1:4,17:4,34:4,51:4}.

The paid rank-one jobs are all four QUERY calls. The other paid jobs are all twelve whole idles. For n=208 ports, multiply each multiplicity by 208. If a candidate h18 native has complete native paid histogram N and helper productive histogram H, its complete assembly must use

    T=208*T_wrapper+8*H,
    P=208*P_wrapper+8*N.

N includes all four main routes per port, private acquisition and decoder paths, correction routes, erasure and every other charged recursive move. H must contain only legitimate independent helper boundary jobs. Ordinary scalar, layout and precision work remains in the full recurrence and compiler proof. This formula is an interface, not evidence that a native achieving a desired N,H exists.

At t=199/200, granting the cheapest four rank17 main routes per port, two separate eight-row decoders with rank14 per row, and zero net extra helper/ordinary/acquisition expense gives positive moment room about 0.44570691352482358 per port over all eight native invocations. This is only an optimistic necessary screen; it is not a complete conditional multiplication theorem. The actual native must fit every omitted cost in the remaining room. In particular, literal tag-subspace stops already matter at this scale; the companion budget records the exact threshold.

## 8. Verification and reproduction

Run from this directory:

    python3 -B build.py --arms 4 --body 17 --out rebuilt
    python3 -B replay.py rebuilt/CALLER.json.gz --out rebuilt/REPLAY.json
    python3 -O -B replay.py rebuilt/CALLER.json.gz --out rebuilt/REPLAY-OPTIMIZED.json
    python3 -B geometry.py PATH_TO_PINNED_NATIVE.json.gz rebuilt/CALLER.json.gz --out rebuilt

Expected formal result is `PASS_EXACT_SHORT_CALLER`; geometry is `PASS_SHORT_CALLER_BOUNDARY_GEOMETRY`. Canonical raw caller SHA256 is `44a8036075fc44a52102844828d2db15e7577d1326e3e49f5f10c13d669138c2`; deterministic gzip SHA256 is `094cb202e20f9e56cda9931f0c19801f9f9689f220d4aa3f829c262781b04111`. Source pin manifests preserve the inherited evidence. Normal and optimized replay agree. Meaningful negative controls delete an actual HOST2, QUERY, whole idle, lambda, or ordinary ADD; every altered source fails its exact endpoint.

The constructor and checker are separate implementations by the same author. They are not described as an independent mathematical review. The root orchestrator's separately produced review, if admitted, must be cited separately. The programme remains open at both the strict complex and ordinary BIT supplier obligations, and no foundational assumption is discharged by this caller alone.

### Six-stage companion

The same universal construction with a=3 is also emitted and exactly replayed in `a3-h18/`: fourteen arbitrary roles, six HOST2 calls, four QUERY calls, eight whole idles, and 403 literal events. Its ambient is 120 and its maximum productive rank is 103. The wrapper is T/n={18:4,35:4,52:4,103:2}, P/n={1:4,17:4,34:4}. Both normal and optimized formal replays and geometry receipts agree for a3 and a4. The companion source screen explains why six stages maximize the available budget per native invocation, whereas eight stages maximize the total optimistic wrapper gap.
