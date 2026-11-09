# Worker A independent review of union transport cost and backing

Reviewed 2026-11-09. **Scoped pass; no blocking defect found** in the targeted
long-stream/short-metadata and local-retirement invariants. This is independent
AI-assisted review by worker A, not a numerical Gaussian review, proof-assistant
certificate, or admission of the full analytic assumption. No C file was edited.

## Reviewed source and scope

The reviewer read PROOF sections6–8, union_bits.py, union_catalogue.py,
union_fields.py and physical_router.py, and the authenticated inherited Tape,
Count, local pool and boundary-origin implementations. Exact before/after
source hashes are in `a_review_union.normal.log`; the files stayed unchanged
during both runs. In particular:

* physical_router.py: `ed725d25219c583c31937854e35c921283c2155a38cea2b257189f1ff29a12ce`;
* union_bits.py: `70fa20367d5ffea06518c2459bcf431d333d42a92eb3dbb40ff67625d5e41edc`;
* union_catalogue.py: `684fd2c3dcc1021c1ddd3c934e1324de8666b1dec92a620c6d525de860203974`;
* union_fields.py: `e50d8a9b89cf4b33b875387bf71b1aed402227e443c7b8aa5f87e63ca467f3b4`;
* PROOF.md: `a365685c67a890933c73a7f7098bd61987a07f853809ae656042880f0a617f30`.

The decisive question was whether a long context, record population, suffix
length or coordinate-prefix value becomes a Count, or whether local retirement
silently revisits old retained backing. Either fault could invalidate the
displayed polylogarithmic overhead without changing a finite output oracle.

## Independent experiments

The reviewer script imports the routines under review, but no C fixture,
encoder, expected-value oracle or Tape class. It uses a separate sparse
absolute-coordinate hardware object with independent primitive-action counts,
hard protected-prefix bounds and preserved old blank tails. Normal and
optimized commands both pass with byte-identical logs:

```sh
python -B review/a_review_union.py
python -O -B review/a_review_union.py
```

The registered result is `PASS_A_INDEPENDENT_LOCAL_SCANS_AND_PREFIX_BOUNDARY`.

1. **Sixteen local-block cases.** Parent block bodies have lengths
   0,17,8191,65537; current bodies have lengths0,1,9,257, with additional retained
   blank tails. A hard guard forbids even reading the parent while finding or
   popping the current block. Independent exact bills are
   `top_block(n)=3n+7` and `pop_block(n)=4n+5`. The previous block is unchanged,
   all current symbols are erased, and the head ends exactly at that block's
   former append origin. The empty-block case passes too. The bill contains
   neither the older prefix length nor warm capacity.
2. **Four complete raw-context cases.** Key lengths0,17,4097,65537 are copied
   and compared literally, with the Count name replaced by a rejecting
   sentinel. Independent bills are `same_context(q)=8q+8` including output,
   and `skip_context(q)=3q+3`. Full key bits and delimiter are preserved.
   Warm target capacity131071 introduces no extra traversal.
3. **Three long coordinate-prefix cases.** Independently constructed valid
   headers use all-one coordinate/ordinal words. Prefix lengths112,448,2304
   are saved and compared raw. Only the active ordinal is returned as a Count;
   source heads return exactly. A one-bit raw-prefix change flips equality.
   The maximum retained Count-tape cell counts are11,12,15 respectively, with
   observed pool peak13. These are actual retained extents of the leased
   metadata tapes, not a host estimate of their numerical values.
4. **Discriminating bad conversion.** Deliberately interpreting an all-one
   448-bit raw prefix with `big` grows a Count tape to450 cells and violates
   the short-metadata criterion. Thus the positive prefix experiment would
   detect the rejected representation change; it does not merely restate an
   identity result.

These experiments check specific implementation invariants. Their all-size
content rests on the following source argument.

## Source cost and retained-backing argument

The only long context operations are same_context/skip_context: binary scans
until PART_END. The context value and its length never enter Count arithmetic.
The output receives its full key once. Catalogue rewinds and repeated context
traversals are explicitly inside `(R+1)C`, not discarded as constant setup.

Geometry.key copies/compares an axis-coordinate prefix raw, skips the remaining
bounded header fields, reads only h ordinal bits into a Count, then reverses
the known local offset. Prefix length `axis*h` is itself a short encoded
integer, bounded by g*h; it is not the exponentially large integer represented
by those prefix bits. Header offsets and record widths are O(g*h+g+t+w).
Page extents are products of local a,n,b,w with a,n<=L; for example
`ceil(a/b)*b^2*w <= (a+b)*b*w`. Balanced-tree ranges are bounded by a<=L.
Consequently every arithmetic operand is polynomial in the displayed local
parameters and has O(ell) bits. There is no arithmetic operand D=L^g, U, S,
live stream length, suffix-row length, context value or global stack offset.

Each Geometry.key comparison scans O(H) raw bits with short counters.
It does not introduce H-bit integer arithmetic or an H-squared key comparison.
The balanced range query halves its encoded range, closes each old Count and
uses O(log L) iterations; it constructs no host tree. Every record and each
boundary lookahead is visited a constant number of times per zip level.
Combining O(log a) levels with the short arithmetic costs is consistent with
the explicit `SB(1+t+log a_max)*ell^5` transport bound. This checks the decisive
parameter separation, not the optimality of exponent5.

Radix inversion locates one locally delimited decision block and performs its
three forward decision scans, then erases that same block backward. The two
record partitions are consumed by decisions, without N0 or N counters.
Keep/final restoration has the same local-block discipline. Every finished
record is stored only once. Hence total keep bits are S, final-record backing
is O(UB+g), and radix backing is O(Ut+t), with no sum over completed rounds.
The tested local-pop bills justify why an older block is not traversed to
retire its successor.

The inherited borrowed-port origin function is a four-action **validation**
of the immediately preceding LEFT marker, not a rewind through arbitrary old
backing. Legal run inputs therefore enter at their actual local origins.
Ordinary work-tape clear/rewind crosses the present body, whose retired suffix
is already blank; it does not search for a historical extent. Caller movement
of a protected return beyond its live end is separately acknowledged in the
proof and contributes caller backing/rewind cost.

The odometer's exceptional movement also fits the stated invoice. A carry
through j trailing axes costs O(jL(h+2)poly(ell)) and occurs at most D/L^j
times, besides the final carry. Since sum(j/L^(j-1))<=4 for L>=2, this totals
O(D(h+2)poly(ell)); the final gL(h+2) is absorbed by DH. Header generation
already scans O(H) per dense point. A noncarry step has no O(L) catalogue seek.

Finally S<=gU<=UH, Ut<=UB and U<=D. With h>=1,
H=2+2gh+g+2t >= g(h+2), and D>=L, so
M=g[L(h+2)+2]=O(DH). These justify simplifying the transport backing to
O(q+DB+C_max+ell^2), without an added sparsity premise. The numerical child,
borrowed source/bank, production setup and caches remain added, as the proof
states. Historical backing is a sum of per-role historical maxima, including
visited cells; it is not reset by erasure and is not a maximum of total sizes.

## Limits

This review did not reprove the retained nonlinear line consumer, its rounding,
source factorization or numerical radius bound. It did not execute the large
numerical fixture or prove production delivery of complete contexts, global
page amortization, broad forward transport, core/halo assembly or FFT/CRT
recovery. The exact preparation and numerical bills must remain additional.
The complete-context specialization retains its lower group-size, full-box
delivery and uniform source-height premises. No whole selected assumption is
discharged by this targeted runtime review.
