# Three rank-one queries for pure (3,3) must lie on one side of the inverse-native base

**Proved scoped necessary condition, pending independent review. No caller is constructed. No new kappa.** The surviving one-native/three-rank-one/two-role proposal cannot put one query before and two after the native, or vice versa. All three must lie on the same side after choosing the source or inverse-source F_1 orientation.

## 1. Setting

Use the exact Gaussian rank bimodules, product upper/lower rank triangle, ordinary inverses and independent two-role source of `INVERSE-NATIVE-TWO-QUERY-GATE.md` and `MIXED-QUERY-PURE-ENDPOINT-GATE.md`. The base L has every coefficient in F_1. Three one-bank query coefficients and their inverses belong to F_1. The asserted final M is invertible and pure E_3, as required by independent endpoints (3,3) with arbitrary ordinary boundary encodings.

## 2. One query before and two after

Absorb outer ordinary factors and write

    W=Q_2 C L D Q_1,           M=Q_3 E W,

where C,D,E are invertible ordinary matrices. Let i be the affected row of Q_2 and j the source column of Q_1.

Since W=E^{-1}Q_3^{-1}M, the lower Gaussian rank triangle implies W has no rank component below two. Its upper rank bound is three. Hence

    W=B+A,          B=pi_2(W), A=pi_3(W).

Every degree-three term uses both Q_1 and Q_2, so A is supported only in block (i,j). The final query Q_3 leaves its other output row unchanged. That row of E W is pure E_3 because M is pure E_3. Consequently E B has at most one nonzero block row, and

    rank(B)<=d.

Let i',j' be the other row and column. The block W_{i'j'} is untouched by Q_1,Q_2, so it is an ordinary compression of L and belongs to F_1. It is also a block of W, which has no component below two. Therefore

    W_{i'j'}=0.                                      (1)

But (1) is incompatible with W invertible, A supported in one block, and rank(B)<=d. Indeed W restricted to input role j' equals B restricted to that role, so this restriction has full column rank d. Also output row i' of W is row i' of B and has full row rank d. Thus rank(B)=d. The image of B is d-dimensional, its projection onto output role i' is an isomorphism, and its restriction from input role j' is an isomorphism onto that image. Their composition is exactly B_{i'j'}=W_{i'j'}, which must be invertible. This contradicts (1).

## 3. Two queries before and one after

Transpose the identity and apply Section 2 in the transposed graded algebra. The source and query ranks and ordinary invertibility conditions are unchanged. This handles the reversed distribution without an unstated scalar or phase specialization.

## 4. Remaining exact caller problem

The one-native/three-rank-one inventory is therefore reduced to a single placement up to transpose:

    M=Q_3 O_3 Q_2 O_2 Q_1 O_1 L,

with all three queries after the F_1 base and invertible ordinary O_j, and target M=U diag(G_3,H_3)V for independent rank-three Gaussian transforms. All ordinary zero divisors and role mixing remain allowed. The theorem does not exclude this same-side word; it requires a separate construction or obstruction.

The complete optimistic moment invoice remains target 2[10] versus price 4[1]+[7]+[8]. A solution must still preserve the actual seven-axis body source, all physical field volumes, uniformity, paid ordinary routing, complete recursive calls and all five retained foundational assumptions. The placement reduction is source-bound mathematical progress, not a supplier admission or a new complete multiplication exponent.

## 5. Necessary intermediate interface in the surviving same-side word

Let W=Q_2 O_2 Q_1 O_1 L and M=Q_3 O_3 W be a prospective surviving caller. Removing Q_3 from pure E_3 gives W supported only in E_2+E_3. Its E_3 part lies in the second query's affected row and has rank at most d. Its E_2 part, after multiplication by O_3, lies in the last query's affected row and also has rank at most d. Since W is invertible, both parts have rank exactly d, and their physical image and input row-spaces are complementary. Their images are ordinary one-role submodules. Thus an invertible ordinary output change can separate W into one pure E_3 row and one pure E_2 row.

The full-rank pure E_2 row R_2 cannot admit a factorization

    R_2=H V_2,

with H an invertible E_2 operator and V_2 an ordinary unimodular input row. If it did, the shared-input-row-space proof in Section 3 of the inverse-native gate would force the E_3 row through the same V_2. Then W would have rank at most d, a contradiction. This uses no assumption that H is a single Gaussian group element.

Therefore the concrete remaining construction must first produce two independent high-rank rows whose rank-two row cannot already be identified with an independent role through an ordinary input change, and must then use the third rank-one query to complete the independent rank-three endpoints. This is a precise structural requirement on the intermediate representation. It is not a proof that such a representation exists, nor a claim that every ordinary kernel projector necessarily admits a free one-role basis.
