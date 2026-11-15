# Constant-record invariant and an explicit lane-service boundary

**Proved for the grammar below; conditional streaming bridge; no new κ.**
This result separates the new algebraic block capacity from physical source
admission. It does not claim a lower bound for every retained compiler program.

## 1. Restricted full-record grammar

Fix any field k and width V>=2. A record is an element of k^V. Permit arbitrary
finite full-record scalar ADD and SCALE, arbitrary coordinate permutations
within any single record, whole-record role permutations, zero INIT, and
CLEAR. Scalar coefficients are the same on every coordinate of a record.
All active records may be used; auxiliary zero records are permitted.

The subspace in which every record is constant across its V coordinates is
invariant under this grammar. Each listed operation preserves it directly,
so induction over the finite word proves the claim. On this input subspace,
r output records carry at most r independent field values. In particular,
any prescribed output-row space U must have restriction rank at most r on
constant inputs if it is to be packed into r records by this grammar.

This includes arbitrary within-record permutations, not merely affine ones.
It excludes coordinate-dependent coefficients, nonmonomial transforms,
cross-bank conditional routes and incoming nonconstant auxiliary data.
Actual native moves need not preserve constants; the statement concerns the
local formation/restoration stage before carriers leave their common chart.

## 2. Application to the optimal two-lane cohort

At a constrained two-run cohort in the new capacity construction, the first
lane has projected rank1 and the second has projected rank3. For V=2s the
second-lane row space alone restricts to rank3 on constant input records:
choose any fixed coordinate in that lane and its three independent original
cohort forms. The row space of all packed outputs therefore has restriction
rank at least3. Two full constant records have restriction rank at most2.
Thus no basis choice can realize this prescribed packed subspace using only
the grammar in section1. The obstruction is to that local implementation,
not to the algebraic optimum9V+floor(V/2), the scalar W9 word, or a richer
explicitly paid ordinary service.

The elementary V=2 example packs four forms u_left,u_right,v_right,w_right
into two records. On constant inputs u=(u,u),v=(v,v),w=(w,w), these forms have
rank3. Two outputs of the restricted grammar have rank at most2. A conditional
cross-bank swap or lane-selective ADD breaks the invariant and lies outside
the proved grammar.

## 3. Sufficient streaming service, with its premises retained

Suppose cocharted physical records are available on synchronized complete
streams with a fixed two-lane layout. Assume each chart acts identically on both lane banks, as I_2 tensor T,
so the full lane matrix units commute with it. Assume source and target
records can be scanned in a common lane/coordinate order with all
required layout conversion and return paid, including same-record calls
between distinct banks. Then

    ADD_LANE X[a] -> Y[b]

can be performed by a streaming pass: for each coordinate of the half-record,
read its source value, XOR/add it into the corresponding target value, retain
the source, and return both streams in their declared layouts. With one
symbol buffer this uses V/2 value additions and O(V) symbol accesses, plus
the explicitly charged layout passes. It introduces no new full-record owner
and does not erase arbitrary data. Reversing a binary lane CNOT undoes it;
a swap takes three such CNOTs. A fixed finite lane circuit therefore has
finite explicit ordinary work and restoration, uniformly in half-width s.

The untouched-spectator premise is substantive. If normalized input x at
chart C is physically T_C x, a desired normalized block map B is physically
T_C B T_C^-1. It agrees with an ordinary lane operation only when the chosen
full matrix unit E_ba tensor I_s commutes with T_C, or a separately paid
conjugated realization
is supplied. Commutation with the two diagonal lane projectors alone does
not suffice: diag(A,B) commutes with those projectors but fails to commute
with cross-bank transfer when A differs from B. Arbitrary block matrices in a lower-bound model do not prove
this property.

## 4. Relationship to retained compiler sources

The retained finite-precompilation contract requires an all-column native
word, complete arbitrary spectators, priced whole-job adapters and finite
program closure. Its specialization proves fixed scalar words and monomial
address maps in the retained physical grammar. Neither source alone licenses
silently replacing full-record ADD by an arbitrary normalized block map.

The lane service above is a concrete sufficient interface, not an assertion
that its layout and spectator premises already hold for the proposed word.
Admission requires binding it to actual BIT cover/tape layouts, counting its
ordinary passes, ensuring all-column uniformity, preserving source/target
adapters and substituting the new full operation/ownership/precision constants.
No movement saving may be claimed by omitting these checks. The current
conditional two-lane word lists every ADD_LANE and keeps compiler admission
false; it is an exact target for this remaining bridge.

Source pins: FINITE-PRECOMPILATION git blob
4badb40f0919c515823cb07e44c6470d4d6469ca, SHA256
4cb32f6b8e388ecf6ed41b5bbdeeb4539cb40c8424f194974afea58f7e0921e8;
SPECIALIZATION git blob7ee84b30892f7354e1c36611f1a5e9b082dc6147,
SHA25670430114f744108223bc1d44b98bc25b696c4b408b7b044c2a8bbdfdb434ac5c.
The exact retained provenance is in
research/p104-shared-native-helper-splits/retained/compiler/RETAINED.json.

Credit @CubeJerry, retained compiler contributors, Worker C's cohort capacity
and explicit lane circuit, and root's invariant/interface review. OpenAI
assistance. The five foundational assumptions remain retained.
