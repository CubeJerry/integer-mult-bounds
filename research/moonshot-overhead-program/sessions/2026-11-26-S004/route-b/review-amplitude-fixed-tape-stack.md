# Independent review of the triadic child-stack schedule

Reviewer: S004 Route B. Reviewed Route A's full
`amplitude-fixed-tape-stack-supplier.md` against the A1 ring recursion.

**Verdict: the schedule supplies the stated recurrence and uniform
visited-space bound.** The important ingredient is consuming the parent
frequency stacks from their current ends, rather than returning across
a parked parent array for each recursive product.

The two next operand records lie at their respective stack tops. Their
preceding separators can become the child boundary markers using only
O(ma) motion. The child owns those records and the suffixes to their
right; it may overwrite or consume them. Unprocessed parent records
remain to the left of the markers. On the output tape the marker lies
after the already accumulated products. Child output is therefore
appended directly, while unrelated parent prefixes on every remaining
tape are protected by their own markers. A fixed permutation of tape
roles or a constant number of local copies suffices to arrange the same
interface at every depth; neither extra tapes per depth nor a global
origin rewind is needed.

On return, temporary child work occupies O(ma) cells beyond the current
markers and can be erased within the child invoice plus O(ma). Removing
its input records restores the parent input heads to the remaining
stack tops. Leaving one canonical output record and replacing the child
marker by a parent separator restores the output interface. A zero
frequency consumes its two records and appends its zero result in the
same O(ma) bound without a recursive call.

Record-order reversal before the inverse FFT is also O(na): locate one
record's beginning, copy it in canonical internal order, return across
that record only, and repeat backwards through the array while appending
forward on the destination tape. Each record has O(ma) bits. Thus input
dispatch, return, skipped frequencies and the final reorder total O(na)
at a parent call. The remaining O(na log k) local invoice is exactly
the already described FFT stages and digit-reversal passes.

All parent stack tops move within fixed O(na) intervals during sibling
processing. A single child adds O(ma) suffix extent, with m<=n/3. The
maximum physical extent of any working tape is bounded by a fixed
constant times a(n+m+...), so O(na) bounds all cells ever visited.
The constant number of stream/buffer roles is independent of depth.
Recursion descriptors and repeated a descriptions fit this bound.
The constant-size base algorithm can use the same marked-origin
convention; shifting that finite tape routine into the current suffix
does not require traversing the ancestor prefixes.

This proof concerns the schedule and interfaces. The exact algebraic
identity, ordered coefficient lift, root orthogonality and base integer
arithmetic remain separately charged by A1; the schedule does not add
an algebraic oracle. The resulting time recurrence is precisely
`T(n,a)<=2k T(m,a)+O(na(1+log k))`.

Prepared for @CubeJerry with substantial ChatGPT assistance.
