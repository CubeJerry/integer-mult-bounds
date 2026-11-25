# Independent review of height-priced affine streams and address interface

Reviewer: S003 Route C. Status: **HS/HA accepted as stated; AR accepted
as a conditional composition of its explicit local contracts**. This is
not an independent claim of a complete multiplier.

Read in full: imported E002 Route A `HEIGHT-PRICED-AFFINE-STREAMS.md`
and `ADDRESS-RADIX-INTERFACE.md`, at concurrent programme checkpoint
`9d5abf18ff741ff6f8b9f82790e0475fc662b4fe`. Also compared against the actual
OpenAI November tape `build/interchange.tex` elementary-scaling discussion
at math `3344da59991ed94f9ba711217b29c1d760badfa6`.

## HS genuinely avoids a numeric-magnitude charge

The original increasing-piece implementation makes a=|c| mod Q runs.
That number is not small merely because c has small binary height. HS does
not pretend otherwise: after reduction 1<=a<Q, every run has q or q+1
blocks, Q=a*q+s. The exact run key is t_r=-rQ mod a, and

    a*(ceil(rQ/a)+k) mod Q=a*k+t_r.

Thus sorting complete runs by t gives one row for each output residue.
Padding a to the next binary power and each run to q+1 blocks expands
payload by less than four. Transposing only ceil(log2 a) binary row
digits yields increasing a*k+t order; known positions remove the extra
rows and last-column padding. Genuine zero data are not inspected.

Each binary digit move across an arbitrary complete intervening range is
a linear scan with two temporary streams: split by that bit and interleave
the equal suffix blocks. These are constant-digit operations, not recursive
interchanges of the entire log(Q)-bit field. The process needs logarithmically
many passes in a, not a tapes or a passes over the entire input.

The inverse inserts the same dummy positions, reverses those digit moves,
and sorts rows by -t*(Q mod a)^(-1) mod a. Its inverse modulus is a and has
only O(log a) bits. It never asks the increasing-piece routine to scale by
the potentially huge inverse residue modulo Q. The reduction and negative
sign cases are correctly separated in HS.

## Physical work and occupied data

Run headers occupy O(a log a) per prefix and are moved with complete
payloads. Since a<=Q, the stable radix passes cost Q*poly(h) volume, h the
binary coefficient height. The nontrivial descriptor estimate is justified
by log Q<=h+log(q+1): a fixed polynomial in the per-run descriptor width
is paid by q*B*poly(h), not by rereading a long prefix per datum. Prefix
counters must use the source amortized convention, as explicitly stated.
One fixed collection of reusable work regions covers payload, headers and
arithmetic registers, yielding visited-space rather than merely live-space
control. No empty source address coordinate is assumed.

HA then applies O(D^2) one-control shifts and D scalings in descending
target-field order. Their earlier controls remain unchanged, and complete
target fibres pay for fixed-degree arithmetic in log Q. General maps retain
the source's Bruhat field-permutation calls. The new short-row transpose
inside HS does not add a recursive large-field interchange call. Thus the
height-priced routine is a substantive improvement to ordinary work while
retaining that call invoice.

## Address/radix contract

AR's theorem correctly keeps polynomial-height endpoint maps, compact
scalar-row execution, grouped call types and a strict maximum child-volume
fraction as hypotheses. It does not infer compact row execution merely
from symbolic sparsity. Small compatible radix selection is a separate
supplier. Multidigit batching permits exponentially many rows with only
polynomial-bit row keys, and stable whole-block sorting moves occupied
payload, not per-symbol long address tags.

The corrected grouped-volume bound is a fixed gamma<1, such as 2/N_label,
not 2/W. The summed call mass and the largest child's volume are different
quantities and are kept separate. Full-volume reserve children run after
main arrays are cleared. The algebra is encoded once and reused through
recursion; temporary role/frequency tags are removed before child calls.
Those conditions are necessary and explicitly retained.

## Independent finite replay

Route C separately wrote `verify_height_priced_scaling.py`. It implements
the actual padded run records, stable binary key passes, individual binary
row-digit moves, known-position deletion, and the inverse. It checked
9,886 coprime forward/inverse cases for 2<=Q<=64, 1<=c<=129 and suffix
lengths 1 and3, involving 652,616 record positions and 8,854 nontrivial
run transposes. Payloads include genuine zero values. Every permutation
matched direct multiplication modulo Q and returned exactly under inverse.
The receipt is `height-priced-scaling-replay.json`.

This corroborates the permutation identities. The asymptotic fixed-tape
and visited-space conclusions rest on the scan proof, not the finite test.
No human refereeing, Lean build or complete multiplier execution occurred.
E002 owns this independent height-priced route; S003 B's explicit small
dyadic geometry is a different sufficient construction and does not rely
on HS/HA.
