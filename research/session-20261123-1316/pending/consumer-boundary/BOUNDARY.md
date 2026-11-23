# Fixed dyadic carry versus the retained quotient consumer

This is a boundary note, not a source correctness objection or a new generic
digit converter. The complete-GL identity g0*S=h0+q*C remains valid. A fixed
affine high map derived from it cannot simply replace the retained quotient
normalization. All canonical assumptions and the selected constant remain.

## Overlap decision

At canonical main e54523517d0f03e58352e647c403a5af3e525a57, #5841
`research/g20-fused-qadic-carries` already gives exact low/carry decomposition,
composition/inverse, column denominator bounds and table-free evaluation.
#5052 `research/signed-dyadic-scaling` physically routes five signed dyadic
scales. #5332 `research/bit-low-carry-lowering/offset.py` already emits a
literal binary C+1 descriptor for quarter carries with finite control and
head return. #5849 `research/runtime-quarter-carry` joins that descriptor to
a physical owner-return rotation. Later `research/bit-whole-low-carry-commit`
also handles fixed-template whole-low enumeration and commit under its ABI.

The generic recurrence a_j=p_j*D^(-1) mod q,
p_(j+1)=(p_j-D*a_j)/q for odd q and D=2^d has immediate invariants
p0/D=sum_(j<L)a_j*q^j+q^L*pL/D and
|p_(j+1)|<=max(|p_j|,D). This is no novelty claim. It does not establish
the existing physical binary-descriptor ABI, its ordering/head return, or
the quotient normalizer. We therefore do not propose another converter PR.

## Actual caller and source pins

Runtime #8042 head dfd25d553a843a946ca0b94130a5ff8943e98fdd retains #8030
head 6285dd829114705862e8d91facaedc1f31d3cfcb through its predecessor
manifest, archive SHA256
769d5a05cc1373fa22ed5956af636992fcd19d7e5c1753a32033a73c358cd31c.
The quotient_route.py blob is fc8502647a9626ffd4047cb7046b80ecc83afb5c,
SHA256 3243f45d6097a80bc8b077d8682426e4555f6c4a3097bd0a12ffd4f1f5c45ba8.
The receiver patch changes only an import and explicitly preserves that
quotient hash. The retained patch is blob 4b7db79b29b83e17e49faa981a0b7a4c4ea21a11.
Graph, caller, strong_binary and cover come byte-for-byte from the frozen
decoder-control source bindings used in the independently reviewed storage
package; ORIGINS.json records their SHA256 and Git blobs.

binary_receiver.Receiver.compiled creates OwnerBanks with a transition
closure. The inherited Receiver.transition calls quotient_right_route with
transform=compensate when direct is false. Constructors default direct=False;
weighted calls with atoms<=n^8 may instead use a direct=True small-body
receiver. This note concerns the full quotient branch, not every invocation.

canonical_right returns Y,L with g*S=L*Y, where L is lower unitriangular.
reduce_row inverts the pivots of previous canonical high rows. high_packet
enumerates previous high prefixes and passes their lifted rows to row_action.
That row's affine map therefore depends on the earlier high prefix.
affine_packet supports general local-ring unit scales. This is expected,
intentional behavior. The source does not claim one fixed affine map for the
entire quotient high packet.

## Exact source joint-port 17 witness

strong_binary.fixed_binary_charts constructs
S=transpose(frames[start[17]].B+frames[final[ports+17]].B).
The retained graph/caller give an integral invertible eight-dimensional S.
Its first three rows are (1,1,0,0,0,0,0,0), (0,0,1,0,0,0,0,0), and
(1,0,0,1,0,0,0,0). Set q=3, modulus 3^w, and
g(a,b)=I+3*a*E00+3*b*E02, a,b in {0,1}. These four valid canonical
representatives all have the same low I. Put A=1+3a, B=3b.
The first three rows of g*S are
(A+B,A,0,B,0,0,0,0), (0,0,1,0,0,0,0,0), (1,0,0,1,0,0,0,0).

The first two source pivots are columns 0 and 2. Reducing row 2 gives
Y[2,1]=-A/(A+B) modulo 3^w. Its low value is always 2, so its free high
coordinate is z=(canonical_residue(-A/(A+B),3^w)-2)/3.
The source's row-major free coordinate index is 15 (zero-based).

| (a,b) | (0,0) | (1,0) | (0,1) | (1,1) |
|---|---:|---:|---:|---:|
| z modulo 9, w=3 | 8 | 8 | 6 | 3 |

The mixed difference is 3-8-6+8=6 mod9. Every fixed affine map of the
36 free high variables over Z/9 has zero mixed difference, so none gives
this quotient high map with coefficients depending only on low and S.
More generally the rational mixed difference of Y is -9/28; the high
difference is -3/28 mod3^(w-1), nonzero for every w>=3. At w=2 the
difference vanishes. Thus first-order testing alone would miss this boundary.

At (1,1), the exact normalized rational coordinate is -4/7. The odd
denominator arises from high-prefix normalization, not the dyadic source
grammar. The fixed-denominator prefix certificate cannot be applied to
these normalization steps unchanged. Residues can of course be represented
with denominator one; this observation is not a lower bound on all encodings.
The example extends by identity blocks to higher ambient rank because later
rows do not alter earlier canonical rows. We do not identify this bare seed
with an entire native job or a full owner-return schedule.

## Replay and remaining implication

Run python -B check_boundary.py and python -B -O check_boundary.py.
The bounded checker compares 81 high pairs with an independent closed form,
checks the full g*S=L*Y identity, and checks the four corners at widths 3
through 20. The universal argument is -3/28, not the finite sweep.
Negative controls cover width-two truncation and a fixed affine counterfeit.

The next meaningful bridge must implement and fund prefix-dependent quotient
normalization, or choose a complete-GL representation with its own low-type
ordering, redundancy/compensation and owner return. A local dyadic carry
serializer alone does not settle either route. No full payload permutation,
physical time bound, or native-service storage claim is proved here.
