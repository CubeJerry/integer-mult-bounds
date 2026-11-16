# The current eight-seed programme has a seventeen-receiver point-feedback closure

**Proved scoped information obstruction for the fixed native source. No general multiplication lower bound and no new kappa.** Even granting all seventeen compatible raw outputs at ground for free, together with every receiver's entire raw geometric side information for free, the current S8 code cannot complete an eighteenth receiver by iterating only completed-point feedback. Ninety-four explicit dual witnesses certify this statement. Therefore another isolated raw output, or a feedback mechanism whose only new global X information is already completed raw outputs, does not by itself create a route from this source to all111 endpoints.

## Exact model and proposition

Use the programme's pinned111 native roots r_j, L_j=span(r_j), F_i=r_i-perp and singular fitting A with h mask189. The native source SHA256 is `8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e`. Let S be the eight-dimensional span of the A rows indexed1,3,4,6,73,74,77,78; this is precisely the D4-compatible seed space retained by the current twelve- and fifteen-output words.

The actual early point set is P0={1,6,73,75,77,79}. For a set P define

    G(P)=S+span{e_j:j in P},
    L(F_i)=span{e_j:r_j is orthogonal to r_i}.

Define the optimistic fitting closure map

    Phi(P)={i:e_i belongs to G(P)+L(F_i)}.

This grants the receiver all local raw coordinates, regardless of whether the real source retained or routed them there. It also grants every point in P as shared global information at zero transport cost. These grants are deliberately stronger than the actual source.

For every characteristic-two field and positive whole-record width, the exact source satisfies

    Phi(P0)=Z,
    Phi(Z)=Z,
    Z={1,3,4,6,18,21,61,64,65,73,74,75,76,77,78,79,80},
    dim G(P0)=14,       dim G(Z)=25.

Consequently any exact decoding programme starting with S and P0, allowing arbitrary computation on these global values and each receiver's proper raw side information, and adding only raw values of already decoded receivers to its global information, remains inside Z. Unlimited rounds and zero-cost point feedback do not complete the other94 receivers. The statement does not permit a new nonpoint global measurement or a genuinely nonlocal receiver observation and then pretend it is only point feedback.

## Exact primal and dual certificates

For each i in Z the certificate supplies an explicit row of G(P0) with own coefficient1 and zero at every noncontact. Its difference from e_i lies in L(F_i), proving i in Phi(P0). The exact binary rank of S is8; its direct sums with the six and seventeen point spaces have ranks14 and25.

For every i outside Z the certificate supplies a binary vector u_i such that

    (u_i)_i=1,
    support(u_i) is disjoint from Z,
    support(u_i) is contained in {j:<r_i,r_j> !=0},
    <u_i,s>=0 for every s in S.

The ordinary coefficient pairing is used here, independently of the real chart inner product. The vector annihilates G(Z) because it annihilates S and is zero on Z. It annihilates L(F_i) because its support consists only of noncontacts. But its pairing with e_i is1. Thus e_i is outside G(Z)+L(F_i).

All94 witnesses are explicit and short: their weights are1 through5, with histogram{1:2,2:57,3:24,4:6,5:5}. The verifier reconstructs S from the raw roots, checks every coefficient pairing, every real noncontact and every excluded point, and checks each primal fitting witness. This is an exact certificate of a finite-source proposition, not a failed search or numerical rank extrapolation.

## Arbitrary fields, widths and computation

The witness argument persists over every field of characteristic two. More directly, fix any nonzero record t in K^V and compare two input assignments: all X zero, and X_j=(u_i)_j t. Every S measurement agrees in the two assignments. Every granted raw point from Z agrees, and every raw coordinate geometrically inside F_i agrees. The desired X_i differs by t. The original Y inputs can be held identical and arbitrary in both assignments.

Therefore no exact function of the granted observations can recover X_i. This proves the local impossibility even if the receiver performs nonlinear processing. Inductively, a point-feedback programme that has only decoded members of Z can add no distinguishable observation capable of decoding a member outside Z. Arbitrary block operations and record widths do not evade the information restriction.

## Meaning for the full111 budget

The current actual full-history fifteen-output word has about7.746 normalized movement room in the retained necessary native comparison. The point-feedback-only architecture fails even if every additional point return and every proper local source observation is priced at zero. Improving their constants or adding more rounds cannot turn it into a complete111-output construction.

A scalable continuation must instead introduce new nonpoint global information, genuinely nonlocal receiver information, a changed code, or another interface outside the stated grants. A downward-moved cache whose payload is not supported in the destination receiver's facet is one possible escape; this theorem does not exclude it. The actual seventeen-compatible receiver set still leaves18 and61 uncompleted by the current source. Completing those two can establish reusable source mechanisms, but cannot alone defeat this closed information boundary.

## Reproduction, controls and credit

    python3 check.py --repo REPO --out output

Expected PASS_EXACT_S8_POINT_FEEDBACK_CLOSURE, closed set size17, ground rank25 and94 dual witnesses. Removing a witness's target coordinate destroys its required nonzero target pairing. Explicitly granting any excluded raw coordinate defeats its witness, demonstrating the intended scope boundary. No physical implementation or cost is claimed for the optimistic grants.

Credit @CubeJerry, the native/singular/S8 source predecessors, `bit_bridge` for the target-compatible seed construction, `bit_construction` for the exact feedback closure and dual certificates, and root for programme direction and independent review. Substantial OpenAI assistance. All complete supplier and foundational obligations remain; no new kappa.
