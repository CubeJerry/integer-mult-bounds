# Bounded next numerical-result seam audit

Feasibility only; no new construction, tested theorem, package or PR.
Audit started 2026-11-14 07:26 UTC; stop within the requested ten minutes.
Canonical base: e54523517d0f03e58352e647c403a5af3e525a57.

## Prior work already closes the semantic and source-operation parts

The actual producer is `research/encoded-current-crt/producer.py`, blob
a327b0161eca57a1cc44ec2aa8e3defed2167ddc, SHA256
88dab4ca02a92164a67826db361214fa1405e4b4a588f8c4279a21bcee95ab76.
Merged #5053, live head ef9da0a9ac29cf86610a52e3a183bdb28508aa74, already
proves current-coordinate reconstruction for arbitrary finite nonempty
left/right groups, pairwise coprime moduli above one, complete product
below 2^(P-1), padded/invalid coordinate semantics, borrowed restoration,
successful/admitted rejecting ownership, at most 32 live slots in a fixed
64-slot arena, and the complete source-operation bound 2^20(P+2)^4.
Reproving CRT, Euclid, the numerical margin or bounded-slot existence would
duplicate it.

Merged #5219, head 15edd6b658f14ae981cedf24507bb957a9e4e174, supplies the
guide-driven Entry, genuine encoded >=4 guard, canonical padding, exact
original allocator-event correspondence and complete 60-owner lifecycle,
with extra source-operation cost 2^16(P+2)^2. Merged #5353, head
07a135eee3a8da9392c4a1e01d4b89db05b4ac03, supplies actual padded-axis
source-to-guide/descriptor RowEntry. The canonical persistent numerical
owner then reuses 63 physical backings across different guides and proves
rolewise historical maxima. It explicitly leaves full binary arithmetic
lowering open. These are proved implications, not gaps merely because an
instruction table has not been materialized.

The canonical `crt-complete-binary-refinement` proof refines the different
fixed PR5105 repair program: 8242 source instructions, 31 roles, one fixed
geometry and supplied ROM; 557123 target instructions and
101391*T+29679 bound. Its program and inputs are not this numeric producer.
It supplies compiler techniques, not an unchanged-grammar substitution.

## Exact remaining boundary

`Entry.invoke` pads into actual bank roles 60/61, then executes unchanged
`produce`. Runtime arithmetic is `words.py`, blob
8d4ba37e2778acb35b34e0719df2caf138fbeb50. Unsigned.divmod is called by
remainders and each Euclid step; modular multiplication/product add other
marker-driven loops. Source control contains only finite role identities,
flags, carry bits and a bounded allocator, with no width decode.

The full producer receives the actual P guide, padded current left/right
streams, eight protected words, 56 inactive private words, the numerical
template and output port. It returns owned lower/left-product words, the
current offset/updated-right stream and validity flag, clearing all other
word bodies and returning borrowed heads. Literal lowering must additionally
implement the primitive loops, finite slot selection, variable numerical
role references, continuations, serialization and cleanup. Generic finite
compilability alone would not be new work.

## Narrow candidate with an honest owner boundary

The smallest substantive numerical primitive not found already lowered in
this bounded audit is a source-bound literal restoring divmod matching
`Unsigned.divmod` lines 253--279 on the actual P-bit word ABI.

Proposed input: four fixed physical roles, borrowed numerator N/denominator D
and granted inactive owned quotient Q/remainder R. Inputs are LEFT bits_P
RIGHT at first-body heads; Q/R have owned LEFT guards and blank P+1 bodies.
Require P>=4, 0<=N<2^P, 0<D<2^(P-1), disjoint roles and retained old blank
histories. These are explicit physical premises, not a new allocator.

A finite graph could initialize Q/R from the read word extent, scan numerator
bits high to low, update R in place by 2R+bit, compare with D, conditionally
subtract in place, and emit Q's corresponding bit. The invariant R<D proves
the high-margin shift cannot overflow. It would return floor(N/D) and N mod D,
preserve borrowed bytes, return all first-body heads and provide a separate
Q/R retirement entry. Finite carry/comparison/borrow control suffices.

Complete optimistic bill: O(P^2) literal instructions for P full shift,
compare, optional subtraction and return iterations, plus O(P) initialization
and retirement. Four P+2 word windows and their older per-role unions cover
history; no source-prefix transport, inverse, modular product or free encoding
conversion is hidden. This is a physical implementation and verification
advance, not a new division algorithm or asymptotic arithmetic result.

The actual caller join is a material remaining check: old divmod allocates
scan and alternating remainder temporaries and leaves a specific free-stack
order. A fixed Q/R implementation changes that trace. A real substitution
must preserve the original events or prove an explicit live/free-role
renaming relation and charge physical selection/binding. #5219's original
allocator coupling cannot silently be reused for changed calls. A local
four-role primitive does not by itself lower the numeric producer.

The stronger possible target is the exact one-left/one-right leaf kernel
with actual persistent-bank output/lifecycle. Its optimistic bill remains
O(P^3) for inverse and O(P^2) for division/products, plus all stream and
ownership work. Several blocks and that owner interface make it unsuitable
as an unbudgeted extension of the completed header package.

## Overlap and recommendation

Read exact current-producer, Entry, persistent-owner and fixed binary
refinement proofs and the actual divmod body. Live searches for
encoded-current-crt/literal, #5053/compiler/arithmetic, restoring-division/
literal and divmod/literal returned the predecessor producer/entry and
unrelated packages, without an exact current literal division implementation.
#5098's one-inverse cache still assumes an inverse provider. The first-node
numerical allocation-prefix package concerns a different complex Node.
This is bounded text coverage, not exhaustive novelty certification.

If another wave stays on this branch, allocate the four-role divmod **and
the actual-call ownership/binding audit together**, stopping at a precise
unresolved allocation-trace seam. If only a generic standalone divider can
be completed and it removes no useful actual-call premise, stop rather than
publish a generic arithmetic exercise. Do not reprove existing CRT/Euclid,
generic compiler or historical-allocation lemmas. No construction is
authorized by this note, and neither candidate implies a new kappa.

Credit JoyboyBrian #5053/#5219 and persistent ownership, Ali Romman #5353,
the exact current #7388/#7352 caller and original Word/record authors.
Prepared for @CubeJerry with substantial OpenAI assistance.
