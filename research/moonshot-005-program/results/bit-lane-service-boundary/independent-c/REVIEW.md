# Independent review of the local lane-service boundary

**PASS at the stated scope. No new κ.** Reviewed root/lane-interface/PROOF.md,
SHA256 `c5eb472260fb3d42f786e7268b4dcab5e1fb00ed0131e82ca79e8f53ea5d0952`.
This is independent proof review and separately written algebraic controls,
not a rerun of the author's verifier.

The constant-record invariant follows directly for every field and every
width from the listed fixed scalar operations, within-record permutations,
role permutations and zero initialization/clear. On constant inputs r output
records have rank at most r. The prescribed two-run block projection has
restriction rank at least3, because its second half contains three independent
cohort forms. Consequently two full records in this restricted local grammar
cannot realize that prescribed packed subspace. The proof correctly avoids
claiming a lower bound for all physical compiler programs or native moves.

The streaming claim is a sufficient conditional interface. Under synchronized
complete streams, paid layout/return operations, and the stated same-record
bank support, each selected-bank XOR preserves its source and all untouched
banks. It has exactly s value additions at width2s and O(s) symbol accesses,
with constant buffering. This is a uniform algebraic/streaming statement;
it does not establish that the proposed BIT layouts satisfy those premises.
Field-symbol access and any physical value/precision costs remain to be
charged in the relevant source service.

A material clarification was requested and incorporated before approval.
Commutation with diagonal lane projectors alone is insufficient for a
cross-bank update. The required matrix unit E_ba, including the identification
between the two banks, must commute with the chart action, or its conjugated
implementation must be paid. The final proof explicitly assumes identical
I2 tensor T actions and records the diag(A,B) counterexample. Our independent
control uses T=diag(I2,swap2): both projectors commute but E10 does not.
Same-record calls between distinct banks are now explicit in the stream
premise as well.

I read and hash-checked both supplied retained compiler sources:
FINITE-PRECOMPILATION SHA256
`4cb32f6b8e388ecf6ed41b5bbdeeb4539cb40c8424f194974afea58f7e0921e8`
and SPECIALIZATION SHA256
`70430114f744108223bc1d44b98bc25b696c4b408b7b044c2a8bbdfdb434ac5c`.
They retain all-column words, arbitrary spectators, permitted whole-job
adapters, complete owner costs and updated finite constants. Their fixed
scalar/monomial specializations do not, merely from these statements,
constitute an admission of arbitrary normalized local block maps. This
review does not exclude a separately demonstrated implementation using a
richer permitted service.

The fresh checker tests912 constant-record generator instances,17472 distinct
record streaming cases and680 same-record distinct-bank cases. It also gives
the explicit projector-only commutation countercontrol. These finite checks
corroborate the general operation-wise and rank arguments; they do not replace
them or certify a tape-layout implementation.

The subsequent two-copy representation repair is compatible with this review.
Expanding every lane into a separate fully paid physical record increases the
number of output records; the two-record rank bound is no longer the claimed
physical interface. Such expansion must count every doubled record, MOVE,
productive target and caller term. It does not make masking free and does not
invalidate the invariant for its original fixed-record grammar.

Reproduce with `python3 check.py --proof /path/to/lane-interface/PROOF.md
--out /path/to/RESULT.json`. Expected status is
`PASS_INDEPENDENT_LANE_INTERFACE_CONTROLS`. All source/proof/checker pins are
in MANIFEST.json. Credit remains with the root proof, Worker C's block source,
retained compiler contributors and @CubeJerry, with OpenAI assistance.
