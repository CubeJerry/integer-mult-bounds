# Two-query minimum-rank gate for independent pure endpoints

**Proved scoped extension, pending independent review. No new kappa.** This closes the proposed one-native query-ranks (2,1) endpoint (3,3), with arbitrary ordinary encodings and every query placement. The genuinely open next inventory has three paid rank-one queries.

## 1. Rank band and statement

Use the same finite Gaussian rank bimodules as `INVERSE-NATIVE-TWO-QUERY-GATE.md`. In addition to the upper rank inequality, Gaussian products satisfy

    |r(g)-r(h)| <= r(gh) <= r(g)+r(h).

The lower bound follows by applying the upper bound to g=(gh)h^{-1} and h=g^{-1}(gh), using r(g^{-1})=r(g). Consequently multiplying a pure E_h element by a coefficient in F_b on either side produces no component below h-b. Ordinary factors preserve every rank component.

Let the two-role invertible base L have all entries in F_s. There are two invertible one-bank queries with Gaussian ranks a>=b, arbitrary invertible ordinary interstage/boundary matrices, and endpoint

    M=U diag(G_h,H_h) V,

where G_h,H_h are invertible in E_h and U,V are invertible ordinary matrices. Thus M is invertible and pure E_h, with physical rank 2d.

**Theorem.** Necessarily h<=s+b. Equivalently, both paid query ranks must be at least h-s to obtain two independent pure-rank-h endpoints from an F_s base.

## 2. Proof for all placements

Suppose h>s+b. If the rank-a query is at an outer end of the three nonordinary factors (L and the two queries), absorb the outer ordinary boundary matrix. Expanding that query as I+e_i q e_j^T, every term omitting it has rank at most s+b<h. Thus all of pi_h(M) lies in the rank-a query's single affected row if it is at the output end, or its single source column if it is at the input end. Its physical rank is at most d. This contradicts pi_h(M)=M having rank 2d.

The only remaining placements put the rank-a query between L and the rank-b query. The rank-b query is then at the outer end. Remove it from the asserted identity by multiplying by its inverse, together with the adjacent ordinary factor. Since M is pure E_h and the inverse query has coefficients in F_b, the remaining word has no rank component below h-b>s.

That remaining word contains L and just one rank-a one-bank query, separated by ordinary matrices. At the end adjacent to that query, an unaffected output row (or fixed input column) equals an ordinary compression of L, hence belongs to F_s. It must therefore vanish. The remaining word is invertible, so it cannot have a zero full row or column. This contradiction handles the remaining placements. QED.

No ordinary coefficient is divided by; no absence of ordinary zero divisors is assumed. The argument does not require a scalar augmentation or a special phase residue.

## 3. Native application and mixed-query invoice

Every source orientation has either itself or its inverse in F_1, as established in the inverse-native gate. Inverting the whole caller preserves query ranks and endpoint Gaussian ranks. For h=3 and s=1, the theorem requires both queries to have rank at least two. It excludes query ranks (2,1), (3,1), and any other two-query inventory with a rank-one query from producing independent endpoints (3,3).

The hopeful (2,1) invoice was target 2[10] versus price 2[1]+[2]+[7]+[8]. That arithmetic is favorable near t=1, but the required caller is excluded. The theorem does not say that a rank-two query is interchangeable with two rank-one calls or that any source call can be inverted for free in an actual algorithm; inversion is solely a proof transformation of a supposed exact identity.

## 4. Complete one-native/at-most-two-query exclusion on three heads

Together with the inverse-native gate and the existing one-native high-job query count, the theorem rules out a positive common-body invoice for **any** one-native, at-most-two-query, two-retained-role inventory on three heads. Query Gaussian ranks are at most three. Let x=[2] and a=[8]-[7]. Strict concavity gives

    0<a<x-1<1,        x<2.

Every target with total head rank H has moment at most 2[7]+a H. The complete native source price is 1+2[7]+a, plus every query moment.

- No query: the native or its inverse is in F_1, so H<=2 and the deficit is at least 1-a>0.
- One rank-one query: the inverse-base maximum rank is two and at most one endpoint has rank at least two, so H<=3. The deficit is at least 2-2a>0.
- One query of rank at least two: the high-job count still gives H<=4. The deficit is at least 1+x-3a>4-2x>0.
- Two rank-one queries: H<=4 by the inverse-native gate. The deficit is at least 3(1-a)>0.
- Two queries, one rank one and the other at least two: the pure-(3,3) theorem gives H<=5. The deficit is at least 2+x-4a>6-3x>0.
- Both queries have rank at least two: H<=6 by the three-head dimension. The deficit is at least 1+2x-5a>6-3x>0.

These are rigorous moment inequalities for every 0<t<1, including t=199/200. Ordinary costs were optimistically set to zero, so paying them cannot rescue the excluded inventories. A zero-rank query is ordinary and can be absorbed without weakening these bounds.

The next smallest still-open optimistic inventory in this same three-head construction is one native with **three rank-one queries**, endpoint (3,3): target 2[10], price 4[1]+[7]+[8]. The present two-query proof does not extend to three merely by counting factors. A source-bound identity, full uniformity and ordinary cost admission remain missing.

Dependencies and scope are those of the inverse-native gate, plus the lower Gaussian rank triangle and the already proved one-native bound on the number of rank-at-least-two endpoint jobs. Finite marked columns can be included only after the separately stated bulk-rank algebra admission. No complete supplier, complete kappa or foundational assumption is newly discharged.
