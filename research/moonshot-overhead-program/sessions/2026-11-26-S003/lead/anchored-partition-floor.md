# A floor for the anchored product-placement invoice

Status: **accepted after independent A proof review and isolated finite replay**; see `../route-a/review-anchored-partition-floor.md`. This concerns the retained two-level placement and its declared sufficient rank guard. It is not a lower bound on all rectangle geometries, physical routing, or integer multiplication. The general density estimate below is elementary; no priority claim is made for it. The concurrent stronger E002 result is credited in Section5.

## 1. A two-sided density estimate

Let `C(q,k)` be the directed relation on two copies of `[q]^k` in which every corresponding coordinate differs. For any finite rectangle cover by nonempty `A_r x B_r`, set

    S_L=sum_r |A_r|, S_R=sum_r |B_r|,
    alpha_L=S_L/q^k, alpha_R=S_R/q^k,
    rho=2(q-1)/q.

The sides may be arbitrary correlated subsets. Exact disjointness is not required for this lemma.

**Lemma AP1.** `sqrt(alpha_L alpha_R)>=rho^k`.

For every coordinate i, the projections of A and B are disjoint. Hence

    |A||B| <= product_i |proj_i A||proj_i B|
           <= (q/2)^(2k).

Writing `E=[q(q-1)]^k`, coverage, that area bound and Cauchy--Schwarz give

    E <= sum_r |A_r||B_r|
      <= (q/2)^k sum_r sqrt(|A_r||B_r|)
      <= (q/2)^k sqrt(S_L S_R).

Division proves AP1. In particular maximum per-side incidence is at least rho^k. A bound of the form `c^k poly(log q)` valid for every k and power-of-two q must have c>=2: otherwise fix q with rho>c and let k grow. This is a necessary condition consistent with JR, not a refutation of it.

## 2. Anchored inner cells and outer products

Use the actual S004 anchored scheme: `d>=2`, `h=2d-1`, inner words `U=[q]^h`; an inner far pair differs in exactly d positions. Partition the relation separately by its d-position set, common outside letters, and ordered unequal letters at its first changed position. Inside each such cell use any exact rectangle partition of `C(q,d-1)`. It may differ between cells. Do not merge rectangles across these cells.

Let alpha_L^0 and alpha_R^0 be the average source and destination incidences of the resulting inner partition. There are

    M=binom(h,d) q^(h-d) q(q-1)

cells, each with q^(d-1) vertices on each side. Applying AP1 within each cell, then Cauchy--Schwarz across cells, gives

    sqrt(alpha_L^0 alpha_R^0)
       >= binom(h,d)(q-1) rho^(d-1).                    (AP2)

Now use this inner partition in the source outer construction: outer words are in `U^h`; partition their d changed positions and common outside words, and take products of the d inner rectangle families. The averaging factors exactly:

    alpha_L=binom(h,d)(alpha_L^0)^d,
    alpha_R=binom(h,d)(alpha_R^0)^d.

Consequently its maximum endpoint load lambda satisfies

    lambda >= sqrt(alpha_L alpha_R)
      >= binom(h,d)^(d+1)(q-1)^d rho^[d(d-1)].           (AP3)

This statement permits arbitrary correlated sides in each JR cell. It retains the outer product placement and the separate position/anchor cells. It makes no assertion about partitions that combine those cells or replace the outer architecture. The same bound holds for separately chosen inner families in the d outer coordinates by applying AP2 to each factor.

Already `binom(2d-1,d)>=2^(d-1)`: its product representation has d-1 factors `(d+j)/j>=2`, for `1<=j<=d-1`. Since q>=2 and rho>=1, AP3 implies

    log2(1+lambda) >= d^2-1 >= 3d^2/4.                 (AP4)

Thus even perfect inner partitions cannot remove the quadratic distance term from this particular placement.

## 3. The declared rank guard and explicit dimension

Retain precisely the sufficient rank guard used by S004 and the explicit S003 star realization:

    q^(d^2) >= 2^(2d^2-2) m,
    D=2(2+h q^h),          x=log2 m>0.                 (AP5)

These are premises of this certificate calculation. AP5 is not claimed necessary for a different rank estimate or realization. Since h>=d, AP5 gives

    log2 D >= h log2 q >= x/d.

Combining with AP4,

    log2[D(1+lambda)] >= max(x/d,3d^2/4)
                      >= (3/4)^(1/3) x^(2/3).         (AP6)

The last inequality follows by cubing: the maximum cubed dominates `(x/d)^2(3d^2/4)`.

**Theorem AP.** Arbitrary replacements of the inner first-difference partitions by exact correlated-side partitions, while retaining these cells, outer products, dimension and sufficient rank guard, cannot certify an `exp(o((log m)^(2/3)))` geometric invoice. Under JR, S004's matching upper invoice is `exp(O((log m)^(2/3)))`. This matching statement is conditional on JR and concerns this declared invoice only.

This is a sharper continuation gate than the earlier literal-partition `x^(2/3)(log x)^(1/3)` floor: correlated JR pieces may remove its logarithm, but this retained placement still has a two-thirds power. It does not show that the invoice is a lower bound on actual executed time. A different sharing method, smaller representation, improved rank estimate, or partition crossing the fixed cells remains outside the theorem.

## 4. Dependencies and verification scope

Actual dependencies read: S004 `lead/joint-rectangle-transfer.md`, Sections1--4; S004 `route-a/joint-rectangle-two-scale-transfer.md`; S003 `route-b/explicit-dyadic-geometry.md`, especially its exact dimension and shared-pencil statement. Programme source pin is `af5d7983`; the OpenAI source pin remains `3344da59991ed94f9ba711217b29c1d760badfa6`.

The companion checker tests exact finite covers, correlated-side refinements, the anchored incidence identities and rational parameter inequalities. It cannot prove JR, the unbounded theorem, physical time lower bounds, or whole multiplication. Independent review is recorded separately when completed.

Prepared for Jerry Chen (@CubeJerry), with substantial ChatGPT assistance. Credits: the original OpenAI label/endpoint construction, S004's anchored JR scheme and S003's explicit star realization.

## 5. Stronger concurrent incidence theorem

After this derivation, the lead fetched E002 checkpoint `a8dd6c24` and read its complete `route-a/NONCANONICAL-RECTANGLE-INCIDENCE-BARRIER.md`. E002 proves a stronger two-thirds incidence floor for **every cover satisfying the retained zero-Gram-side condition**, without the fixed cell/product partition restriction of AP. Its constant-weight binary rank argument bounds the size of a rectangle side near each source; its q-ary companion gives `log2 rho_v >= (d^2+d log2 q)/32`, and the same sufficient rank guard yields `Omega((log m)^(2/3))`.

AP remains a short independent elementary confirmation in a narrower class, not the programme's strongest incidence theorem. The lead checked E002's polynomial-rank identity, neighbor-counting step and binomial estimate, but has not replayed its finite checker in S003. Both results remain scoped to positive incidence invoices and a retained sufficient rank guard. Neither lower-bounds general tape runtime or resolves JR. Credits for the stronger noncanonical result remain with E002.
