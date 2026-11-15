# Independent review of the paid two-copy principal-bank movement invoice

**Status: PASS for the stated movement-only interface. No new κ.**

Worker A independently reviewed `root/two-copy-budget/check.py` and its frozen
`RESULT.json`; exact file hashes are in this review's receipt. The reviewer
reassembled the full physical coefficients and used a separate integer-root
implementation with denominator `2^160`, rather than the author's decimal
`10^50` denominator. Every interval and every sampled sign agrees with the
independent enclosure.

For `p=16,...,21` ordinary principal banks in a complete two-copy caller,
the physical movement profile is

`380[1]+24[2]+238[3]+142[4]+218[7]+(p-16)[8]`.

The two additional ascending Y routes are actually priced as
`14[1]-2[7]`; the paid extra principal lifetimes each contribute `[8]`.
Every native, target, productive and recursive caller term is duplicated
before normalization. Thus the normalized source moment is exactly half
of this full physical profile. The coefficientwise duplication identity
is valid for any finite caller parameter, and does not invoke fractional
physical records or free concurrency.

The first certified even caller parameters for `p=16,17,18,19` are
respectively `2,4,4,6`. In each case the finite margin is affine in `m`
with strictly positive slope `18` times the limiting room, so positivity
persists for every later even `m`. At `p=19` the normalized limiting room
is enclosed about `3.26306177977597658`; `p=20` has negative room about
`-0.695564845884850999`. For `p>=20`, the margin is already negative at
`m=2` and decreases with `m`; adding further `[8]` lifetimes only decreases
it. Thus this particular optimistic movement interface excludes all
`p>=20`.

This is an exact budget lemma. It does not provide a decoder, admit an
unconstructed source, establish a supplier, or translate scalar cover
charging to repeated physical banks sharing the same native facet. The
latter rank-weighted charging interface is a separate open obligation.

Reproduce with `python worker-a/review-two-copy-budget/check.py` from the
session workspace. The checker imports only the reviewer's prior binary
root arithmetic helpers, not the author's arithmetic or result generator.
