# Independent review: general reversible raw-pivot interface

## Accepted statement and provenance

**PASS** for the updated proof with SHA256 `71d27e20ed5041f0779f92a16fc1708f08581d330e942909fa66d57de5ffc955` at `root-research/reversible-raw-pivot-interface/PROOF.md`.

The mathematical assertions hold over every field, including characteristic two, and for every positive coefficient dimension V. They are conditional on the stated whole-field chart-transport and ordinary-operation contracts. They do not establish arbitrary-volume physical suppliers, compatible schedules for overlapping cohorts, or a new multiplication exponent.

One availability clarification was requested and is present in the accepted bytes: the raw-rowspace gate applies when using only those raw fields. Any actually cocharted owned records or other observations must be appended to the current availability matrix. Omitting them would make the claimed necessity false.

## Pivot criterion and precise information loss

Order the coordinates with the chosen m pivot indices first. The emitted raw map is

M = [[A_I,A_J],[0,I]].

An invertible transformation of its outputs subtracts A_J times the unchanged J outputs. The result is diag(A_I,I), so

rank(M) = p-m+rank(A_I),

and ker(M) consists exactly of vectors with q_J=0 and q_I in ker(A_I). The map is injective precisely when the chosen minor is nonsingular. Some m-column choice works precisely when rank(A)=m; full row rank does not validate an arbitrary choice.

For vector fields, the actual linear operator is M tensor I_V. Its rank is V(p-m+rank(A_I)) and its kernel dimension is V(m-rank(A_I)). Each extra full linear record supplies at most V dimensions, so at least m-rank(A_I) records are required. Copies of requested outputs supply no new kernel information.

The minimum is attained by actual original-coordinate records. Select a column basis of A_I and retain the pivot coordinates outside that basis before replacement. If the emitted map and these records vanish, the retained coordinates vanish, leaving a relation among the independent basis columns; every remaining coordinate therefore vanishes. There are exactly m-rank(A_I) such records. Their acquisition, storage and transport must still occur physically; this is an algebraic minimum only.

## Implementation and ordinary bounds

For nonsingular A_I, Gaussian elimination reduces it to identity by elementary row additions, nonzero scales and at most m-1 swaps. Reversing and inverting those elementary operations applies A_I to the pivot bank. The unchanged nonpivots then supply A_J q_J at the common chart. At the hub, first subtract A_J q_J and then apply the recorded reduction to recover q_I.

The in-place swap is valid over every field: x←x+y, y←y−x, x←x+y, y←−y. In characteristic two the last scale is the nonzero identity scale, and the same calculation exchanges x and y. No division by two occurs.

A Gauss-Jordan reduction uses at most m(m-1) elimination ADDs, 3(m-1) swap ADDs, and 2m-1 nonzero SCALEs including the swaps. Forward and reverse each add at most m(p-m) contributions from the nonpivot bank. Therefore the stated totals, 2m(p-1)+6(m-1) ADDs and 4m-2 SCALEs, are valid generous bounds. ADD here is the programme's weighted field addition; coefficient-service costs remain part of the separate ordinary contract.

The m delayed delivery records add their real INIT, deposition ADD, consumption ADD and CLEAR operations. The bound of m extra simultaneous records is valid for this one-group interface. No claim that different groups' live records or receiver visits compose follows from it.

## Exact raw-route invoice

Each nonpivot follows L_j→C→H, and pivot i follows L_i→C→F_i→H. Counting these actual ranks and subtracting the direct L_j→H baseline gives exactly

\[
\sum_j[(c-\ell_j)^t+(D-c)^t-(D-\ell_j)^t]
+\sum_i[(f_i-c)^t+(D-f_i)^t-(D-c)^t].
\]

The second sum replaces each pivot's C→H segment. Equal-chart segments emit no MOVE and contribute zero. The pivot ordering is arbitrary; all acquisition terms are counted once regardless of which initial dimensions belong to the chosen indices.

For 0<t<=1, each split satisfies a^t+b^t>=(a+b)^t, so the increment is nonnegative. Total rank telescopes to sum_j(D-ell_j). In the line/facet/native case this reduces to p*((c-1)^t+(9-c)^t-8^t)+m*((8-c)^t+1-(9-c)^t), as stated. Actual containment, not dimension alone, is required: incomparable charts of equal dimension cannot be treated as a zero-rank segment. Already split source routes must be compared using their actual old and new histograms.

## Current-matrix composition gate

If current raw rows are M_S and locally retained record rows are R_C, use the full availability matrix B=[M_S;R_C]. The desired original-input row a is obtainable by local weighted additions only when a lies in row(B); with a fresh charged accumulator this condition also suffices for linear acquisition. It does not by itself show that overwriting a carrier preserves information; the appropriate minor or full invertible local map must still be checked. All rows must use the same complete initial-coordinate space: an unknown common component cannot be discarded from an observation row.

For example, a current raw value q1+q2 cannot alone yield original q1. A cocharted record q2 makes q1 available. The amended proof correctly accounts for that record. Invertible changes on overlapping groups preserve total information, but their inverse must be applied in reverse chronological order and later target rows must use the current matrix. The proof makes no unsupported promise of compatible future routes or free fresh acquisitions.

## Independent controls

The standard-library checker imports no author code. It exhausts every A and pivot subset for 1<=m<=p<=3 over F2 and F3: 21,138 matrices, 22,807 matrix/pivot choices, and 599,501 input assignments. Each case checks the emitted image, exact information loss, minimum coordinate records, and equivalence between full row rank and existence of a valid choice. For every valid choice it emits actual weighted ADD/SCALE acquisition and inverse operations, verifies their symbolic maps, and checks the operation bounds. Vector-field rank scaling is separately checked at V=3.

A further 714 symbolic route profiles check the exact histogram formula, zero-length omissions, arbitrary pivot indexing and rank conservation. Concrete controls reject full-rank A with a singular selected minor, dependent overwrites without a record, incorrect overlapping inverse order, a noncontaining recipient chart, omitted acquisition legs, and an omitted final pivot leg. The complete-availability control succeeds only after its real retained record is included.

These finite controls supplement the universal proof above. Normal and optimized Python runs produce the same deterministic receipt. `MANIFEST.json` pins the checker, receipt and this review; the checker pins the accepted updated source proof.
