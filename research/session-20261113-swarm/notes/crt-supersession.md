# Two-axis CRT payload lift preflight

**Status: the d=2 row shear is source-verified and its payload mechanism is already covered by #4024; outer-caller integration and tariff remain unresolved. No κ and no PR.**

This is a bounded preflight for the d=2 forward address map in #7351. It asks whether its exact padded permutation has a direct payload realization. It does not claim the #7351 compact endpoint already transports payload.

## Exact source-bound map

Pinned forward source: CrocSwap/integer-mult-bounds #7351, head d2ed3959c30528b0b85fc6d815d4ad4f94f6be86, research/encoded-balanced-crt-endpoint/PROOF.md, §2. SHA-256 a20c90aada4ea2d9141a465b10bd1d54a1047b52608bb19c88efa7fd98eeacf3.

Use u=s_0 and q=s_1 for the two pairwise-coprime source moduli. Let complete padded coordinate extents be P=2^h0, Q=2^h1, with u<P, q<Q, as allowed by #7351. For a valid left coordinate 0<=i<u, its singleton reconstruction is k_A=i. The right-node offset from the pinned formula is

    b(i) = i * u^(-1) mod q.

Thus the complete padded address map is

    Phi(i,j) = (i, j+b(i) mod q)   if 0<=i<u and 0<=j<q,
               (i,j)               otherwise.

There is no multiplier on j: the coefficient of j is exactly one. In the source coordinate convention no fixed relabeling is needed. Each valid row is a cyclic right shift of its first q cells; the tail j>=q is fixed. Every row i>=u is fixed, including all its valid-looking right coordinates, because #7351 sets the left reconstruction to zero when the left coordinate is padded. This is a permutation of the full P-by-Q padded rectangle. Its inverse rotates each valid row by -b(i) modulo q.

The formula is not for fixed q. #7351 quantifies over arbitrary admitted pairwise-coprime moduli u,q, with their declared widths. In particular, h0,h1∈{ell-1,ell}, ell>=2, with both h0,h1>=2, and u,q>=2. A runtime implementation must read q and u and compute u^(-1) mod q; a constant table or fixed-ROM assumption is outside this source contract.

## Bounded payload-mechanism check

The candidate three-reversal row rotor is not a new payload mechanism. #4024, `research/crt-address-streams`, head `e99297be6749518a1b5b85cd129ecaf204d26c63`, already gives complete payload fibers for the general triangular shifts. Its physical-composition proof splits each target into the first `s_i-offset` cells, the remaining `offset` cells, and the invalid tail on a sequential pass; then emits the second bucket, first bucket, and invalid bucket while carrying the complete spectator suffix. The inverse uses the inverse split. The implementation in `crt_shear.py` does these bucket copies, checks full stream exhaustion, restores heads, and clears temporary buckets. `crt_offsets.py` compiles the actual encoded offsets for every lower prefix, with zero offset on an invalid prefix. This supplies the row rotation here as the d=2 specialization, including arbitrary payload values in padded tails and inverse ownership.

The #4024 proof explicitly charges each shear `O(V)` movement, including bucket copy and erasure, full suffixes, offset copying, and counter restoration, with `V=CTR` for its complete tensor payload. It also states a full conversion invoice that includes a full-support global router, `D` shifts, two padding passes, offset preparation, setup, return, and cleanup. Under its stated conditional caller laws and inherited router theorem premises, the proof derives a complete conversion cost `O(V p^Phi log p)`. That conclusion is conditional on the theorem's physical tensor interface, router, and caller hypotheses; it does not automatically place the converter in the selected caller of the current project.

The #4024 source supplies a broader physical construction than this proposed row rotor, so I stop the row-rotor construction here. The candidate rotor's data movement would also be `O(V)`: split a valid row at `q-b_i`, rotate its two pieces, and preserve the padded tail. But an independent three-reversal implementation would duplicate the already-covered complete payload movement without discharging the unresolved source/caller integration or tariff gate.

## Corrected balanced-width setup bound

Let H=max(h0,h1). The balanced source contract gives `|h0-h1|<=1` and both widths at least two, so `PQ>=2^(2H-1)`. For H=2,3, `H^4/2^(2H-1)` is at most 3; for H>=3 its successive ratio is `((H+1)/H)^4/4<1`. Hence `H^4<=3PQ`. Also `Q>=2^(H-1)>=H`, so `PH<=PQ`.

One call to the pinned #7351 endpoint on a private geometry probe with input coordinates `(1,0)` returns the second coordinate `u^(-1) mod q`: `1<u` because the source requires `u>=2`, and the offset formula is `0+1*u^(-1) mod q`. Its declared-address cost is `O(A^4)` with `A=h0+h1<=2H`, hence `O(H^4)=O(PQ)` on this balanced source domain. Repeatedly updating the row guide by `b_(i+1)=b_i+u^(-1) mod q` over at most P rows costs `O(PH)=O(PQ)` in fixed-width arithmetic. Thus inverse setup and a sequential offset guide can fit within `O(V)` for `V=PQL`, `L>=1`, without an additional Euclid oracle. These are optimistic absorbed setup bounds; they do not replace #4024's more general offset compiler or prove the selected caller pays for the full conversion.

These bounds correct the earlier draft's use of `ceil(log2(max(u,q)+1))`, which can understate declared widths when moduli sit below their width ceilings. Geometry-sensitive controls must be bounded with H, the actual declared width. They show only that setup is not an asymptotic obstacle relative to V on this balanced source domain.

## Supersession and remaining gate

Root supplied two directly overlapping payload results to credit: #7388 head `d6f4a69202ad0bba4a915f4d4f3eaba1fe431c86` (`encoded-crt-leaf-payload`) and #7390 head `cf62e701f52adf2196923ab7356539e69713d55b` (`encoded-crt-two-target-payload`), reported as finite payload fibers via radix. I did not inspect those packages. Together with #4024, this closes the proposed row-lift as an independent contribution; this preflight does not claim global novelty.

The #4024 proof's `O(V p^Phi log p)` complete conversion bound is conditional. The current preflight does not establish that its inherited router and physical tensor premises refine the selected caller, that the actual serialized cell width and geometry match, or that the enclosing caller's budget admits all conversion stages. The older `research/crt-transported-key-tape/README.md` at canonical `e54523517d0f03e58352e647c403a5af3e525a57` remains a fixed exceptional-key result; it is not needed to establish the supersession and adds no caller integration evidence.

**No caller-cost admission follows.** The actual next theorem must bind the complete #4024 conversion to one selected caller, including its layout, cell width L, extents, ownership, inherited router/tensor premises, call count, returns, scratch/history, and outer tariff. In particular, if a caller requires staged result ownership, its full staging and commit cost must remain explicit. #4024's complete converter invoices one router and D shifts per conversion; multiplication's two forward and one inverse conversions retain three router calls and corresponding setup costs.

This is a bounded source-bound supersession check, not an implementation or a κ contribution.
