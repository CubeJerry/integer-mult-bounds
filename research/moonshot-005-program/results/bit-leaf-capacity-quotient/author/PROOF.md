# Actual fixed histories still require thirteen leaf-record capacities

**Status: proved in the stated information interface. No new complete κ.**

This theorem separates whole-bank coverage from simultaneously choosing a bounded number of coded records at the paid leaf ports. Even after granting the entire fixed record history and arbitrarily powerful processing of the full source banks, one independently selected record at each of the eight current ports cannot complete all111 native demands. The componentwise necessary capacities sum to13 whole records. This is an information theorem; a movement-price conclusion requires an additional physical cut hypothesis.

## Pinned source and exact interface

The baseline is the composed34 word SHA256 `e4d451886a134c648f71fadac5b7f6f8693e5495b60416d137cfe0d0e563e050`, programme commit `3057acc9311101cfedfcfacf7f68fb0866507871`. Native real roots come from `sessions/2026-11-14-S013/cloud/SOURCE-RECOVERY.json`, SHA256 `8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e`. Receiver i has native facet F_i, and sees a record at leaf L_p exactly when the real native dot product r_i·r_p vanishes.

Let H0 be the52 roles with singular mask0, E={8,9,19,20,36,37}, and H1 the53 mask1 roles outside E. Let g0 and g1 be the actual old P6 and P7 first retentions specified by `extra_source_delivery.first_retention_hex` and `higher_source_delivery.first_retention_hex`. These remain explicit fixed binary rows, not arbitrary global seeds.

The eight ports and generously allowed source spaces are:

| Port | Source information allowed to its new messages |
| --- | --- |
|7|All raw H0 coordinates and the actual g1 donor|
|11,12|All raw H0 coordinates|
|41,28,44|All raw H1 coordinates|
|19|All raw E coordinates and g0|
|27|All raw H0 coordinates and g1|

Including g1 at port7 is a deliberate relaxation of the actual cross-bank retiming: it may be carried all the way to that leaf in this information model. Thus the theorem is not obtained by ignoring the new coupled donor.

Each portal p emits a fixed-length transcript Z_p of C_p field symbols, computed from its allowed source information. Different portals may choose different recipes. A receiver obtains the transcripts of its visible ports. In addition, freely grant:

1. Every geometrically local raw X coordinate.
2. Every already completed raw X coordinate globally.
3. Every value of every record in the entire pinned source word, at that value's actual historical chart, whenever that chart lies inside the receiver's facet. The checker even grants the pure-X part of original-Y histories, eliminating all Y nuisance in this relaxation.
4. Arbitrary announcements of newly decoded raw coordinates, globally and at no cost, for as many rounds as desired.

The grant in item3 is stronger than stationary owned stock plus principal history: it includes all1,681 initial and post-INIT/ADD/MOVE record states. No changes to those historical values, new higher-chart data, arbitrary new common coded fields, changed source-bank assignments, or different ports are allowed. Those remain legitimate ways to escape the theorem.

## General quotient-capacity lemma

Fix a portal p and a receiver set J, all outside the initially granted raw points. Restrict the input to assignments supported only on J, and fix all original Y inputs to zero. Suppose every receiver in J sees p. Let S_J be the linear span of the restrictions to J of:

- all freely granted fixed historical and raw-local measurements visible to any receiver in J;
- every allowed source-bank measurement at every other portal visible to any receiver in J;
- the initially granted raw points.

Write r=dim S_J. Grant a basis of S_J globally to all receivers; this can only help. Every receiver in J can then compute all of its observations other than Z_p from that basis. Every raw coordinate outside J is zero on the restricted input family. Any newly decoded coordinate in J, when announced, is already a function of the same basis and Z_p. Induction over the actual feedback transcript therefore shows that completion of all demands in J makes the entire independent J-input a function of (S_J,Z_p).

For **linear encoders/decoders over every characteristic-two field**, including arbitrary noncommuting V×V blocks, the joint linear map must have rank |J|V. The free measurement map has rank rV, so

    C_p >= (|J| - r)V.

For **arbitrary exact deterministic fixed-length encoders/decoders over every finite characteristic-two field**, the same inequality follows by counting inputs: |F|^(|J|V) distinct restricted assignments must inject into at most |F|^(rV+C_p) transcript values. Equivalently fix the free measurements to zero and count the |F|^((|J|-r)V) points of their kernel. The proof allows all free decoded-raw-point feedback in the interface; it does not assume a particular decoding order.

The nonlinear statement is not asserted for unrestricted infinite alphabets, variable-length encodings without a worst-case symbol bound, or additional nonpoint broadcasts. The linear statement is valid for infinite characteristic-two fields.

## Eight explicit witnesses

The exact coefficient and real-geometry computations give:

| Portal | J | Projected free-information basis | r | Necessary C_p/V |
| --- | --- | --- | ---: | ---: |
|7|{18}|none|0|1|
|11|{26}|none|0|1|
|12|{53,57,85}|none|0|3|
|41|{24}|none|0|1|
|28|{45}|none|0|1|
|44|{29,62,63}|e29|1|2|
|19|{8,9,36,37}|e8+e9+e37|1|3|
|27|{42}|none|0|1|

Every old historical measurement in all eight cases has zero projection. The two nonzero free-information rows arise from the generously carried g1 donor. Each designated source bank has full coordinate rank on its J, so these are capacity constraints, not merely absence of the desired information from the source.

The port12 Gram matrix on its three receivers is

    [[4,2,-2],[2,4,-2],[-2,-2,4]],

so no one of those raw inputs is geometrically local to any of those receivers. For port19, all four pairwise native dot products are also nonzero. Its three-dimensional kernel can be written explicitly as

    span{e8+e37, e9+e37, e36}.

The donor restriction e8+e9+e37 annihilates every one of these input directions, yet all three independent records must be recovered. For port44, restricting to X29=0 leaves the two independent directions e62 and e63 invisible to every other source.

Consequently, in port order (7,11,12,41,28,44,19,27),

    (C_p/V) >= (1,1,3,1,1,2,3,1),

componentwise. The sum is13. In particular, C_p=V at every portal fails at12,44,19. This remains true while whole-source-bank visibility closes all111 demands, as the independent checker confirms. Coverage111 and eight-record simultaneous compression are different propositions.

No assertion is made that thirteen records suffice for the full problem. The matching rank of each *restricted* source-bank problem verifies that the local cut is nonvacuous; it does not provide a simultaneous all111 code or a chronological physical source.

## Source correction and boundary controls

An early scratch argument treated the donor as vanishing on {29,62,63} and {8,36}. Exact checking rejected both: g1 contains X29 and X8. Those incorrect zero-leak arguments are not admitted. The final proof explicitly includes the rank-one leaks. Enlarging the E witness to {8,9,36,37} supplies the stronger correct three-record quotient bound at port19.

The checker includes three meaningful controls. Adding a common X53 measurement invalidates the port12 rank0 premise. Giving the port44 source a new X53 direction also invalidates it. Deleting demand85 reduces the port12 floor from3 to2. These controls expose the scope of the hypotheses rather than merely perturbing an output hash.

## Transfer to the36-output terminal-reprogramming source

The separately reviewed36 word has SHA256 `af51d0d7c872dbf3fa3744b582769d4c7763e0747e57c74005d091d19b7da474`. Its new common point41, completed point46, RAW41 capture, and CAP46 source lie outside every selected witness tuple. Direct replay recomputes all historical projections and proves the same eight quotient ranks; the result is in `RESULT36.json`. Thus this precise13-capacity gate survives that concrete source change. This does **not** assert that every future common-code reprogramming preserves the gate.

## Physical costs: what is and is not established

The theorem counts informative symbol capacity at specified leaf interfaces. It does not count scratch owners, native calls, MOVE calls, erasures, or a universal number of arriving packets. Copying an existing field into several leaf owners cannot increase its information dimension; conversely a changing field can carry more than one historical value. Therefore thirteen stored records is not by itself a proof of thirteen physical arrivals.

A conditional movement corollary may be obtained only after separately proving that all new information crosses these leaf cuts in at most8 existing whole-record arrivals plus q genuinely additional positive-MOVE arrivals, with no informative leaf births, changed higher histories, new common coded information, off-portal receivers, or uncharged feedback carrying extra independent data. Under that additional cut factorization, the summed capacity bound gives q>=5 and each positive integer-rank MOVE costs at least1 at exponent199/200. An additive fixed-price continuation with room less than5 then fails its necessary movement budget. Establishing that factorization for a proposed physical class is a separate obligation, not an inference from field count alone.

## Reproduction and next questions

Run from any directory with Python and SymPy:

```bash
python check.py --repo /path/to/programme \
  --word /path/to/programme/research/moonshot-005-program/results/bit-composed-coded-source/author/output/WORD.json \
  --out /tmp/leaf-capacity-34.json
python check.py --repo /path/to/programme \
  --word /path/to/reprogram36/WORD.json \
  --expected-word-sha af51d0d7c872dbf3fa3744b582769d4c7763e0747e57c74005d091d19b7da474 \
  --out /tmp/leaf-capacity-36.json
```

The next constructive task must change one of the precise inputs to this gate: source coupling, an actually useful higher retention, common coded information touching these quotient directions, paid portal capacity, or receiver geometry. A potentially sufficient code must still be realized by legal chronological operations and a complete invoice. The global all111 supplier, strict complex supplier, complete recursion and all five foundational assumptions remain open.

Developed by `/root/delivery_audit` in @CubeJerry's persistent programme with substantial OpenAI assistance. The native source, prior actual delivery, port placement, and cross-bank constructions retain their original provenance and credit. Independent root verification is recorded separately.
