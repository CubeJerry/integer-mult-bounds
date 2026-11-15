# A three-head spectator source and a one-query rank-component gate

**Exact algebraic source/interface and scoped obstruction, pending independent review.** Adding an untouched spectator coordinate to every real chart preserves the source's MOVE rank differences. A three-axis ordinary cycle then gives a common head whose cube has Gaussian rank three. However, one rank-one query cannot turn one such native into endpoint ranks (3,1). The prospective one-rank-two-query inventory remains a separate construction problem. **No new kappa.**

## 1. Spectator lift and complete source price boundary

Take the actual canonical source on nine binary coordinates, with heads a,b and seven body axes. Add one fresh spectator axis c to every chart, including each initial chart, every contact chart and each endpoint. For charts U subset W, the inclusion U+<c> subset W+<c> is genuine and its rank difference is dim(W)-dim(U). Every ADD still has a real common chart. The existing all-column Gaussian source maps tensor with identity on c. No owner or copied field is added.

Thus each half retains its three MOVE ranks 1,7,8 and one ADD. The ambient field has one extra spectator coordinate per tensor column, which multiplies source and target array volumes by the same factor 2^V. The normalized rank moment remains 1+[7]+[8]; the common whole-array volume factor must be retained in any actual compilation. This is a direct-sum source identity, not a new complete supplier or a claim that enlarged arrays cost nothing. Descriptor, layout, tape and threshold constants must be updated for the fixed larger ambient dimension.

## 2. Three-axis ordinary gauge

Let S be the binary coordinate permutation a->c, b->a, c->b. In the computational index j=u_a+2u_b+4u_c its permutation is

    (0,4,1,5,2,6,3,7).

S C_b S^-1=C_a and S^3=I. Set B=C_b S and R=C_a^-1 S C_b S=S^2, an actual ordinary permutation. Preapply S to the first role and S^2 to the second; postapply S^-1 to the second. Each half adds exactly three coordinate-permutation services, without new phase passes or Gaussian calls. The exact two head maps become

    [[B,0],[I,B]],    [[B,-B^2],[0,B]],

with the native cross minus remaining a field-level scalar. These individual multiplicative coefficient identities tensor to every V. All seven body axes remain fresh and fixed by the three-head operations.

The powers obey

    B^3=C_a C_b C_c,
    B^6=X_a X_b X_c,
    B^12=I.

Their Gaussian ranks, modulo six, are (0,1,2,3,2,1). In particular B^3 is a genuine rank-three head. B^6 is an ordinary translation, not a new Gaussian query. The original two-head conservation representation does not apply after genuine ordinary mixing with c.

## 3. General one-rank-one-query component theorem

Work in any fixed finite Clifford group on at least three head coordinates, with the full monomial ordinary subgroup. At sufficiently large faithful tensor width the Gaussian-rank components pi_r are independent ordinary bimodules. Products obey r(gh)<=r(g)+r(h), by the rank inequality for the symplectic B block.

**Theorem.** For one source half N=[[A,-A^2],[0,A]], r(A)=1, and at most one rank-one in-place or distinct-bank shear query, no exact independent endpoint can have pi_2=0 but pi_3 nonzero. Arbitrary invertible ordinary interstage and boundary encodings are allowed. This includes the proposed endpoint ranks (3,1).

**Proof for a query after the native.** Absorb the outside ordinary matrices using bimodularity: they cannot hide a nonzero pi_2 or create pi_3 from zero. The remaining word has form Q C N, where C is ordinary. On its affected row the two active input columns have the form

    [L A, -L A^2+M A].                           (1)

Here L,M are an ordinary coefficient plus a rank-one query coefficient times an ordinary coefficient (in-place is the special case with no first term). Thus LA and MA are supported only on ranks 0,1,2. If pi_2 of the whole word is zero, its first active input column gives pi_2(LA)=0. LA therefore has support only at ranks 0,1. Multiplying it on the right by A gives support at most two. Hence LA^2 and MA both have no rank-three component, so neither does (1). Unaffected rows already have rank at most two. Idle input columns, if additional roles exist, involve only an ordinary coefficient or one queried ordinary coefficient and also have no rank-three component. This contradicts the proposed nonzero pi_3 endpoint.

A query before the native is handled by transposition: Clifford transpose preserves Gaussian rank, monomial ordinary maps remain monomial, and interchanging the two active role labels restores the same upper source form with A replaced by A^T. An inverse/sign orientation with rank-two cross has the same square relation using A^-1. An orientation whose cross is ordinary cannot reach rank three with one rank-one query at all. QED.

## 4. Accounting and continuation

The raw (3,1) common-body proposal has targets [10]+[8] and price 2[1]+[7]+[8], a positive planning margin [10]-[7]-2. The source embedding is valid, but the component theorem rules out its required head endpoint in the stated one-query family. This favorable arithmetic must not be promoted to a caller.

One **rank-two** query changes the component analysis and is not excluded by the theorem. Its proposed endpoint (3,2) has target [10]+[9] versus price [1]+[7]+[8]+[2]. This needs an actual source-bound identity and full ordinary/compiler accounting. Multiple native halves are also outside this one-native result.

Dependencies: pinned canonical source, general tensor-separation/rank-bimodule lemma, and the explicit direct-sum/chart argument above. Independent review should inspect enlarged-volume accounting, the field-level cross sign, active input columns in (1), and the transpose reduction. Credit @CubeJerry, the source/compiler authors, the programme's tensor-component work and S014 Worker B with OpenAI assistance. All five foundations remain retained; no new kappa.

## 5. Same-session extension: one query cannot give two high-rank jobs

The abstract compression proof in `ONE-NATIVE-QUERY-GATE.md` extends to any fixed finite Clifford head dimension with pi_low=pi_0+pi_1. Every source orientation still has invertible N_low: the diagonal rank-one heads remain, while its cross is either an ordinary triangular entry or is removed at rank two. The same two-sided ordinary-kernel compression proves

    number of endpoint jobs with rank >= 2 <= number of one-bank queries.

Query Gaussian rank does not enter this count. Thus the one-rank-two-query endpoint (3,2) is also excluded: it asks for two high-rank jobs with one query. Section 4's proposal is retained as the investigation record, not as an open case.

One rank-two query with endpoint (3,1) has no positive invoice: target [10]+[8] is smaller than price [1]+[7]+[8]+[2] for 0<t<1 by strict subadditivity of 10=1+7+2. A smallest surviving positive proposal is one native plus TWO rank-one queries, endpoints (3,2): target [10]+[9], price 3[1]+[7]+[8]. Saturating the count inequality does not construct that caller.

`check_threehead.py` verifies the lifted chart ranks, all four independent source columns at widths 1 and 2, the rank pattern and nontrivial sixth-power translation. The component/query-count arguments are universal written proofs, separate from these controls.
