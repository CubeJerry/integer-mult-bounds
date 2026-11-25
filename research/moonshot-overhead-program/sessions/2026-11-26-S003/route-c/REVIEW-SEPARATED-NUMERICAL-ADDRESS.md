# Independent review of the numerical query-address invoice

Status: **accepted in the stated source-operation and local-support scope**. Reviewed `../route-a/separated-numerical-address-audit.md`, its exact checker, and the actual November 24 source at pin `3344da59991ed94f9ba711217b29c1d760badfa6`. This accepts SN-A1–SN-A9 as written; it does not establish SN or any machine lower bound. The admitted AQ envelope is unchanged.

## 1. Source operation count

I reread the Fourier `build/kernel.tex` product, shared-pencil, endpoint and finite-recursion sections, and tape `build/permutations.tex` through the packed-XOR proof. The source explicitly keeps m distinguished axes and D-1 shared auxiliary axes in each half. For a fixed j, its coordinate maps act on that distinguished axis and the auxiliary axes; the other distinguished axes are complete spectators. Binary elimination on this 2D-dimensional support consequently uses O((D+1)^2) complete width-f exchanges/additions. This smaller support is legitimate and does not mean a unit-cost address-word operation.

The free source endpoint and destination endpoint transforms are independent of j. Their intervening representative changes remain indexed by j in the source operation list. Summing over endpoint incidences gives O(m(D+1)^2 lambda V) field-move volume per pencil. On charged rectangles the number of common rows is bounded by the same incidence count, and their extra Fourier calls remain in the recursive invoice. Pointwise row mixing does not create another spatial call.

The complete query-product correction uses one exchange of the two full halves; its price J(a) should indeed appear once at that boundary. It is unnecessary to implement this particular map by m separate small exchanges. The check/lift tables are pointwise in the spatial index and are covered by CW's ordinary work. Each of the two repair branches has volume V/8, so the repeated nonrecursive invoice is multiplied by the convergent sum of 4^(-h). This establishes the displayed SN-A2 with the existing NW constant-array schedule and additive descriptor allowance.

The generalized packed-XOR price is valid under the stated physical supplier: its source proof uses a bounded number of width-f interchanges per guarded pass, plus ordinary rotations and exceptional-set work. The restored third chunk is an occupied, paid spectator. The absolute setup polynomial and guard constant are fixed before choosing the varying arity. The record width is Theta(k), so reading address counters remains charged to payload scans, as required by the actual source lemma.

## 2. Cancellation and what remains

For J(u)=sqrt(1+u)L(u), with L increasing, f>=2 and A>=2m give

    sqrt(m) J(f) <= sqrt(3/4) J(a).

The inequality uses 1+f<=3f/2, f<=a/(2m), and sqrt(a)<=sqrt(1+a). Since J(f)>=1, the extra 1 in 1+J(f) changes only an absolute constant. Thus the predictor degree O(sqrt(m)) is removed from the multiplicative address bill. The separate m query count remains. SN-A5 follows, and its m E_addr J(a) term is not the E_addr J(a) term requested by SN.

This is a statement about the evaluated operation list and its retained positive majorant. It is not a lower bound on any joint algorithm for the query sum. The note keeps that distinction explicit.

## 3. Exact endpoint example

For d_v=e_1 and d_w=e_2 in the binary two-dimensional dot-product space, the stated source and destination frames are orthonormal and H=<e_2> is contained in d_v-perp. The factorization therefore falls within the source's free-rectangle argument, including its pairing and spectator conventions.

Expanding the exponent in SN-A6 yields the initial phase x_j z_j+x_0 z_0, the final phase s_j t_j+s_0 t_0, and the cross terms

    x_j t_0+x_0 t_j+z_j s_0+z_0 s_j.

Those cross terms are precisely the normalized Walsh matrix followed by the two exchanges X_j<->Z_0 and Z_j<->X_0. Since D_j commutes with H_aux and D_aux and H_aux P_j=P_j H_main, the claimed E_dest D_j P_j D_j E_source factorization follows with the stated order. The scalar normalization is 1/4 in one column. The two endpoints are mutual inverses; no unnormalized transform or missing phase is hidden here.

An address with only X_j nonzero witnesses P_j!=P_l for j!=l. Multiplying a monomial matrix by invertible diagonal matrices cannot change its support permutation. Hence the shared endpoint argument alone cannot turn all the middle operators into one common permutation with query-dependent pointwise phases. Tensoring columns and retaining unused query axes preserves this witness. A joint sum algorithm remains a separate possible mechanism.

## 4. Independent replay and scope

Copied the checker into `replays/separated-numerical-address/` and ran it independently with `python3 -I -B`. It passed 256 exact rational kernel entries, 217,872 complete global query outputs, 32 distinct-support witnesses, 80 regular-price cancellation checks and 35 negative controls. The source script hash is `d4395f18c420d151bea1372b84093495352a0458bbd8d2aadf20ee6b1e850228`; the replay and receipt are preserved in that directory.

These tests support the explicit local identities and support distinction. They do not execute the asymptotic tape supplier or prove that joint aggregation is impossible. The independent S004 JR-alone conditional transfer improves the binary rectangle family by another route and is compatible with this audit. This is an AI-assisted written review, not a formal-kernel or human-referee certificate.
