# Fixed-tape child dispatch for the radix-three amplitude corrector

Status: **proved physical scheduling supplier; independent review requested**.
This supplies the explicit head discipline for Route B's
`bounded-amplitude-residual-repair.md`, rather than inferring cheap motion
from a geometric memory estimate alone.

## 1. Fixed tapes and current-frame suffixes

Use one fixed finite set of tapes sufficient for the local radix-three
FFT's three partner streams, result streams, operand arrays and arithmetic
buffers. An additional fixed tape holds recursion descriptors. No tape is
assigned to a recursion level.

On every working tape, a call owns only the suffix above its current-frame
boundary marker. Ancestor data lie below that marker and are never read
or crossed during the call. Local passes rewind only to the current marker,
not to the physical origin. A finite descriptor records n,m,k,a, logical
array lengths and suffix roles. Before a recursive call, all relevant
heads are placed at their current stack tops.

Record separators and frame markers use separate fixed alphabet symbols.
Frame markers nest in ordinary stack order; descriptors identify the
current frame. Return erases temporary suffixes and restores the preceding
frame marker or record separator. There is no unbounded collection of
marker colors.

## 2. Consume parent frequency operands from their ends

After the two forward FFTs, discard arrays no longer needed and arrange
the transformed operands as stacks of canonical 2m-coefficient ring
records. A constant number of whole-array copies/reversals can arrange
these stacks in O(na) time. Process frequency j from 3k-1 down to zero.

The current operand pair is already at the two stack tops. A frame marker
immediately before each record marks the child's input suffix; remaining
unprocessed parent records lie below it. R_m multiplication starts with
its two actual blocks in place. An optional copy through a buffer costs
O(ma), and no O(na)-bit parent prefix is traversed.

The child may consume its input records. It stores all of its FFT work,
arrays and nested child regions above the respective markers on the same
fixed tapes. Return erases the child's input/scratch suffixes and restores
heads at the ends of the remaining parent operand stacks. This clears only
O(ma) visited cells, in addition to the child's own charged running time;
it does not scan remaining parent data.

A third designated stack accumulates pointwise products. The child's output
boundary is just after the completed parent product records. The child
leaves its canonical 2m-coefficient result there and changes its frame
marker to the next parent record separator on return. If its internal
algorithm finishes on another tape, transferring that one record still
costs O(ma). All other child work is cleared. For j divisible by three,
append the proved zero record in O(ma) scans and make no recursive call.

Total child transfer and cleanup is O(kma)=O(na), not O(kna). The two
input stacks are consumed in one direction and the output stack grows in
one direction. These costs belong to the local term of A4.

## 3. Restore inverse-transform order once

Products were appended in descending frequency order. Reverse their record
order once before the inverse FFT. Read the last record, locate its start,
copy its bits in canonical internal order to a new array, and move to the
preceding record. Each location/copy/head-return costs O(ma), and output
appending is monotone. A reusable one-record buffer and fixed tapes suffice
for total O(kma) time. Coefficient bits are not reversed internally.

The inverse FFT then uses the author's local stage layout. Its partner
reads, three-stream merges and optional ternary digit reversal remain inside
the current suffixes. Each complete pass costs O(na), for O(log k)
stages. Divisions by three and twiddle rotations retain their O(ma)
record bills.

## 4. Time and all visited cells

A child has m<=n/3. At one active depth, each parent retains a constant
number of arrays with total volume O(na). A child works in suffixes above
those parent stack tops. As inputs are consumed and outputs appended, each
parent top stays inside its O(na) interval. Siblings revisit overlapping
suffix regions; they do not each allocate a fresh parent-sized workspace.

The maximum rightward extent on any physical tape is bounded by a fixed
constant times

    a(n+m+m_next+...) <= (3/2)na.

The constant includes the fixed FFT arrays and record buffers and does
not multiply at every depth. This bounds the union of visited cells.
Logarithmic descriptor sizes decrease geometrically along the chain;
repeated descriptions of a also fit O(na). The fixed n=1,3 bases are
handled separately.

Every call returns heads to its own boundaries/top records. Thus the exact
physical recurrence and space estimate are

    T(n,a)<=2k T(m,a)+O(na(1+log k)),
    visited(n,a)=O(na),

with a fixed alphabet and tape count. Full parent scans occur only in
its charged local FFT/reordering stages, never once per recursive child.
An implementation that instead placed every child's work after a parent
prefix and crossed that prefix on every return would fail this interface.

This is an explicit schedule for the already proved algebraic recursion.
It supplies no new convolution identity or unpriced random-access oracle.
