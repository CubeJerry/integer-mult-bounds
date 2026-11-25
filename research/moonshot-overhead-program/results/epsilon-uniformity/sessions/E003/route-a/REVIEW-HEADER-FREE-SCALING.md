# Independent Route A review of header-free affine scaling

Status: **accepted written local component**, subject only to making the
trivial Q=1 identity branch explicit. This is independent AI-agent review,
not human refereeing or formal verification. The claim remains a stream
permutation result, not a complete multiplication theorem.

Reviewed file: `../lead/header-free-affine-scaling.md` in E003; its exact
source/predecessor pins are preserved there. Reviewer read the complete
proof and complete replay script, independently rederived its count/select
and run decomposition, and ran the script with an isolated receipt path.

## Mathematical checks

1. The Euclidean recurrence is valid with Y=AN+B. After reducing A,B below
   M, v=0 contributes no lattice pair. For a pair at v>=1, the change
   `(v,z) -> (N'-z,N-v)` gives the claimed inverse bijection. If Y is an
   exact multiple of M, the apparently additional v'=0 boundary has zero
   admissible z', so no correction term is missing. A=0 can only occur in
   the terminating reduced case.
2. For residue r, `floor((r+M-R)/M)` is exactly the indicator r>=R,
   including R=0 and R=M. Equation (4) therefore counts strict prefix
   residues correctly.
3. Within a low-bit bucket, `t=b+2^k v` enumerates all eligible keys once.
   Since multiplication by lambda is a permutation modulo a, the listed
   original row positions are distinct. Searching for the least R whose
   strict-prefix count exceeds the ordinal returns exactly r=R-1, with
   no assumption that the modular progression is monotone.
4. Stable LSD partition makes bit k the next primary bit while preserving
   the previous lower-bit order. Thus the physical bucket/ordinal order
   used at the next pass agrees with its reconstruction formula. No
   original labels need remain on tape. Summing bucket counts over passes
   gives fewer than 2a examined bucket slots.
5. The scaling decomposition has run lengths q or q+1 determined by
   `t_r<s`; its output order is `a*k+t`. The inverse starts in t order
   after undoing the rectangular transpose, so the same sorter with
   multiplier lambda reconstructs original r order. Removing known dummy
   positions preserves genuine zero input symbols.

## Physical accounting

Each key reconstruction uses polynomially many actual bit operations on
O(log a)-bit registers, and log a is at most the source coefficient
height after reduction. Reconstructing a key once per whole record costs
at most V poly(h), even when a is near Q and records are tiny. The sort
retains a constant number of equal-payload arrays and no a-sized table of
keys, counts or original indices. Thus its proportional-space constant
is absolute. The fixed-degree descriptor/Euclidean scratch is additive.

Concatenation can process one prefix fiber at a time using reused regions;
the number of records with each destination bit is computable from the
complete key range [a]. Alternatively the two output streams retain the
prefix group boundaries via known counts. Neither implementation needs a
long prefix index to be reread per datum. Counter resets are paid by whole
record lengths and prefix counters are amortized. Consequently the earlier
height-priced time bound and the new absolute payload-space bound are
compatible on fixed tapes.

The general triangular-map corollary retains existing paid field
permutations and sequentially reuses its register list. It does not claim
an arbitrary succinct permutation is equally easy. The floor-sum rank/select
structure of the modular key is essential.

## Verification

Command from repository root:

```text
python3 -B research/moonshot-overhead-program/results/epsilon-uniformity/sessions/E003/lead/verify_header_free_scaling.py --max-modulus 71 --output research/moonshot-overhead-program/results/epsilon-uniformity/sessions/E003/route-a/header-free-independent-replay.json
```

The receipt records the actual completed finite cases. The replay simulates
permutation records and checks exact floor sums, key reconstruction, run
sorting, forward/inverse composition and adverse controls. It is not a
simulation of individual multitape transitions and cannot establish the
unbounded asymptotic claim without the written proof.

Open question: compose this processor with the full changing-template
field packing and source call shapes. Header elimination resolves one
space coefficient; it does not remove those other global obligations.

Credits: @CubeJerry; the E003 root proof; E002 stream predecessors; pinned
OpenAI source; classical floor sums/radix sorting; independent AI-assisted
Route A review.
