# Independent asymmetric source and axis binding review

Prepared for @CubeJerry by seed78 with substantial OpenAI assistance.
**PASS**, with identical normal/optimized receipts. This executes actual
metadata/source constructors and route serialization plus exhaustive address
semantics. It runs no physical Core or halo on numerical data.

## Frozen SHA256 pins and reproduction

- source_geometry.py: `bbee918cd3492ca016d3edc668e884af6e22784a521f1102acad28e3cd2bc622`
- axis_binding_review.py: `ebd6238a6286e9ddd1d9e3d254c6b86b49d46f1e1e99e60c64fdbcc4cf09c91e`
- Both axis-binding receipts: `0df7755229622a00716f43eea7179b39978eaec6be44a5e3fc2c4c0530f389e1`

Receipts also pin retained Layout, AdmittedPartition and PreparedRoutes.

```sh
python -I -B axis_binding_review.py --package /path/to/actual-core-halo-join --output normal.json
python -I -B -O axis_binding_review.py --package /path/to/actual-core-halo-join --output optimized.json
```

Expected status: INDEPENDENT_ASYMMETRIC_AXIS_BINDING_PASS. The reviewer loads
actual source partitions and halo tables; it interprets original addresses
and source starts independently, without the author's fixture.

## Actual asymmetric witness

Original MSF periods are (16,128), with one spectator bit, local side 8,
boundary 1 and halo 0: 4096 addresses and 64 contexts. Native low-axis widths
are (7,4,1). References are (15,1,2,1,3,64) and (127,1,4,1,3,192).
Their conservative W4 archives are actually prepared.

All 4096 addresses preserve the original local MSF axes/spectator and return
exactly through the emitted route descriptors. Every context matches its
original source starts. All 1152 entries of 18 distinct windows agree at
those starts. Regenerating each window at local origin differs at 224 entries.

Support completion permutes coarse bits: naïvely reading a packed label as
the original coarse tuple gives wrong origins at 3584 addresses. The actual
retained route constructor rejects that family and a reversed-axis family.
The new producer's core_starts(c)[g-1-i] binding passes.

Deliberately unequal normalizer shifts (1,2) produce actual Count ports
(31,80,28,64,39); the drop uses sum 3, not maximum 2. Radius admission includes
all 4096 records with R0=64.

## Negative controls and scope

The new producer rejects a different Reference with the same period, reversed
sources, and an honestly packed W1 archive carrying the correct source IDs.
An identifier alone cannot certify zeros outside the stored band. The generic
producer now requires the inherited conservative band; finite sharper W2
fixtures retain their separate complete off-band check and cost.

It also rejects missing whole-field radius, missing output headroom,
insufficient lifted carrier and a coarser Core grid. These controls call the
actual producer, rather than only the reviewer's formula.

The older route constructor knows geometry and its own partitions, not the
halo's intended Reference. It accepts a structurally valid same-period foreign
source. The new family producer rejects that case against actual archive IDs.
Both observations are recorded, with no claim of wrong-source acceptance in
the new producer's declared domain.

The tested interiors are explicit admitted scalar blocks. Production carving,
native rates and growing-group absorption remain separate. Complete source
preparation, context inventory, archives and routes remain billed. These are
AI review checks, not human or proof-kernel acceptance. No selected assumption
or kappa is changed.
