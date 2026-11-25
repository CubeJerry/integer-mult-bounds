# Source-by-source invoice for the elementary-height compiler

Status: **proved mathematical implementation ledger**. Independently
reviewed by the lead and Route C; see `../route-c/ELEMENTARY-TOWER-REVIEW.md`.
This expands Section 4 of `elementary-tower-extraction.md`. It is a
written proof, not a Lean certificate or an astronomical-template replay.

All manuscript references below are to OpenAI `math` commit
`3344da59991ed94f9ba711217b29c1d760badfa6`. `T/` means the November tape
paper's `build/`, `F/` the November Fourier paper's `build/`, and `Old/`
the September tape paper's `build/sections/`.

## 1. Implementation being bounded

This is a specified implementation of the source scheme. For the requested
rational exponent, choose a prime in the proved Bertrand interval, double
the integer label parameter until the explicitly counted call/reserve
inequalities have a fixed strict margin, and use the stated literal
matrix-root and basis-expansion algorithms. Use standard diagonal pairing
for `(j,log_2 r_chunk)`. An arbitrary merely computable generator or arbitrary
enumeration order is **not** asserted to obey the bound.

Let `S>=2` dominate the finite data from the extraction, enlarged by a
fixed power when needed: arities, row/role counts, instruction-list length,
integer radix value, absolute integer numerators/denominators in address
maps, bit lengths of numerical dyadic coefficients, generated scalar
tables, and the generator's actual time and visited space. All remain
`E_3(C j^3 log(j+2))` under a fixed power enlargement.

Use a fixed finite binary instruction engine, not a universal simulation
of a machine with an unbounded number of heads. The engine serializes
aligned roles exactly as `T/uniformity.tex`, common-tapes subsection.
Row and role numbers live in binary data, not in a cross-product of
control states. A candidate can be the fixed engine plus a literal
printer for its `poly(S)`-bit tables. Such a printer has `poly(S)` states;
with a fixed tape count and alphabet, its transition list has `poly(S)`
bits. A fixed outer interpreter scans that list and maintains one head
per candidate tape, adding `poly(S)` time per transition and additive
`poly(S)` code storage. It adds no `log n` overhead.

Finite generation may also be performed by a fixed tape program from
`j`. Matrix computations do not assume random access: scanning a stored
array for one requested entry costs at most its polynomially bounded
description length, introducing another fixed polynomial factor. This
preserves all elementary heights. The generator prints a validated
finite list and all retained data are counted.

Write `k` for the top binary address width and `V` for a node's logical
bit volume at its current numerical width. Factors polynomial in `S`
are always kept. The following claims have input-width exponents
independent of `S`.

## 2. Exact stream and address primitives

| Primitive | Source proof | Quantitative implementation |
|---|---|---|
| Digit split, digit move, merge | `Old/02-streams.tex`, `lem:elementary-streams` | At most `b^2<=S^2` role streams; serial scans and class counters cost `poly(S)V`, with polynomial descriptor setup. |
| Fixed aligned row map | same; `T/uniformity.tex` | At most `S` inputs/outputs; scan out one role, compute and merge. A dense map costs a polynomial number of full scans, all charged. |
| Nested counters and returns | `Old/02-streams.tex`, counter paragraph | A range counter costs `O(L+w)` over `L` ticks. Each reset is charged to its range scan; at most `S` ranges add `poly(S)`, not a power of `k`. Unrelated prefix counters are not reread per entry. |
| Controlled rotation | `Old/02-streams.tex`, `lem:ordered-affine-streams` | Offset arithmetic has an absolute polynomial degree in `f log b+log B+log S`, with `poly(S)` terms. The full target fibre has `b^f B` positions, which absorbs that polynomial with `poly(S)` coefficient. |
| Rational scaling | same lemma | Integer scaling uses exactly `|a|` monotone pieces; `|a|<=S` by definition. Its inverse reverses the split/merge. Numerator and denominator values, not just their bit lengths, are included. |
| General rational coordinate map | `Old/04-swap.tex`, `lem:lower-lower`; `T/interchange.tex` | Elimination gives two triangular factors and a permutation. Dimension at most `S` means polynomially many updates and at most dimension-minus-one recursive exchanges. |
| Scalar field arithmetic | `F/repair.tex`, `cor:swap-repair` | Expand the cyclotomic extension into independent `F_p` rows. Scalar maps become finite base-field matrices. Only `O(log p)` bits encode a data symbol; no table over all extension elements is built. |

The offset calculation can be implemented with schoolbook multiplication,
division and Euclidean elimination on its binary integers. Its bit exponent
is an absolute constant; the number of fields and terms only multiplies
the cost by `poly(S)`. For any fixed integer `a`,
`(1+w)^a<=C_a 2^w`; applying this to
`w=f log_2 b+log_2 B` proves the fibre absorption uniformly. A long
unrelated prefix contributes only an amortized counter advance, exactly
as the source requires.

Instruction lookup can scan the entire finite list, and row lookup can
scan the aligned role record. Each contributes at most another polynomial
in `S`. This conservative choice avoids every uncharged random-access
assumption.

For clarity, a triangular update `y += sum_i a_i x_i` is implemented as
successive **single-control** rotations `y += a_i x_i`. The controls stay
unchanged, so their composition is the required update. Each elementary
call has an absolute fixed number of collapsed prefix/control/target/gap/
suffix fields and counters. The `S` terms are an outer loop with charged
table scans; no constant-time access among `S` counters is presumed.

## 3. Recursive movement and stack space

The new interchange recurrence has a fixed margin
`2m^gamma+2a <= m^rho/2`. Its non-call node work is `poly(S)V`, plus
`poly(S)(1+k)^a` descriptor work for one absolute `a`. The latter can
be bounded globally as setup, rather than hidden separately at every
small descendant. The main child receives its original fraction of
logical volume; no serialized workspace is substituted for that volume.

Before a main call, park the other roles and descriptor at an end-access
stack. Restore from the same end. Copy, erase, head returns and repeated
instruction lookup cost a polynomial in `S` times the parent's volume.
There are at most `S` calls after a fixed power enlargement, so all this
is a parent non-call coefficient. Main descents shrink volume by at most
`2/W`, with `W>2`. Full-volume reserve descents occur after merging and
clearing work streams; they park only descriptors. Parked arrays therefore
sum geometrically, with coefficient `poly(S)`. This follows the explicit
schedule in `Old/04-swap.tex`, fixed-tape parking paragraph, and its
reserve adaptation in `T/interchange.tex`.

The radix conversion pads volume by less than `b^2<=S^2`; single-digit
base cases use polynomially many digit streams and at most `poly(S)`
passes. All root and child descriptors are finite lists of at most `S`
binary integers with `O(k+log S)` bits. Products, splits and collapsed
lengths use `poly(S)(1+k)^a` arithmetic of absolute degree. Descriptor
storage on an active stack has depth `O(log(2+k))`.

The normalized Walsh recurrence has its own fixed strict margin, and
each child receives `1/W` of its parent volume. Its occupied spectator
rows and padding are precisely those of `T/walsh.tex`; parking does not
alter the `sigma/W` coefficient. Both recursive algorithms use the
same finite engine and flat descriptor stacks. There is no interpreter
slowdown multiplied once per recursion depth.

## 4. Packed XOR and controlled-block permutations

`T/permutations.tex`, `lem:packed-xor`, performs a bounded number of
controlled rotations per guard pass, an exact exceptional-record sort,
and `O(log(2+k))` guard passes. Its controls in this application are either
selected address bits, fixed binary column maps, or the CRT block tables.
They admit algorithms with an absolute polynomial degree in `k` and
coefficient `poly(S)`:

- A binary matrix acts column by column, using at most `S^2` XORs per
  column. Parity selectors inspect at most `S` functions of each column.
  Scanning all columns costs `poly(S)k`.
- A CRT table has at most a fixed power of `k` entries: the source's
  short axes have width `20 ceil(log_2 k)`, and blocks have at most seven
  axes. Schoolbook arithmetic on `O(k)`-bit ranks has absolute degree.
- Exceptional destinations are computed by reversing eight rotations
  and applying the prescribed flips. The number of rotations is
  absolute; address calculations again have absolute polynomial degree.

Choose one sufficiently large absolute guard coefficient `C_guard`.
The exceptional fraction is at most `80k 2^(-G)`, with
`G=C_guard ceil(log_2(2k))`. Multiplying this fraction by the polynomial
rank-calculation and `O(k)` radix-sort expenses leaves `poly(S)V`.
The parameter-dependent coefficient does not require a guard length
proportional to `S`; it stays in the time coefficient. A scan of the
whole address costs `O(k)` per record and is paid by record width at
least `k`. Stable sort passes, temporary keyed records and cleanup are
all included, and their space is linear in the record volume.

`cor:bit-positions` uses a bounded number of packed-XOR operations.
`lem:controlled-blocks` uses `O(log k)` block batches and `O(log k)`
Beneš stages. Its application has a uniform positive free-address
fraction: no controls for synchronized local permutations, and at most
`k/2+O(log k)` controls for CRT. For large `k` one can take `delta=1/3`,
independent of the template. Thus the source bounds become

\[
 \operatorname{poly}(S)V(1+k)^\rho(1+\log(2+k))^3
       +\operatorname{poly}(S)(1+k)^a,
\]

for an absolute setup degree `a`. Small widths use direct splits, whose
cost remains `poly(S)` times volume under the same accounting.

## 5. Precision and numerical work

Use the original dyadic normalized Walsh template (`F/binary.tex`), not
the changed real-root construction. If one node has at most `S` entries
and instructions, its fixed coefficients have at most `S` bits. The
product of its instruction norm bounds is at most
`C_node=2^(S^a)` for some absolute `a`. Copies, merges and retained
register identities are included.

An exact completed child is unitary. The source's common-ancestor
argument (`T/uniformity.tex`, precision subsection) therefore bounds a
fault gain by `C_node^(2d+1)` with `d=O(log(2+k))`, rather than by a
product over all completed children. The logarithm of the gain is
`poly(S) log(2+k)`. Counting the array faults adds a polynomial term of
the same form. Boundary digit, product and final-scale bounds in
`T/integers.tex` have absolute exponents in `k`. Thus its explicitly
computed error majorant is bounded by

\[
 \log_2 H_j(k)\le Ck+S^a\log_2(2+k)+S^a
                   \le S^{a'}(1+k).
\]

The published precision algorithm computes that majorant and takes enough
bits for `2^P>8H_j(k)+2k`, also storing fixed dyadic coefficients exactly.
It need not know the smallest absolute exponent `a'` in this analysis.
Integer magnitude caps have the same bit-length bound. Temporary exact
sums/products before rounding enlarge it only by a fixed factor.

Interchange is an exact permutation of the *bits* of a numerical record.
Its temporary finite-field combinations are not floating-point numbers;
they introduce no numerical faults. At its return boundary every record
is restored at the required address. It therefore has norm one for the
Walsh error argument regardless of its internal finite-field workspace.

For `P<=S^a(1+k)`, the source's fixed short multiplier costs
`O(P log(2+P))<=poly(S)(1+k)(1+log(2+k))`. Its visited workspace is at
most its time. Only one such word multiplication is active at once, and
its marked scratch region is erased and reused, so the space charge is
**additive** `poly(S)(1+k)^2`, not this amount for every record. A linear
space theorem for that short multiplier is unnecessary here. The primitive
is the independently established Harvey--van der Hoeven multiplier cited
by the manuscript, avoiding circular use of the desired near-root bound.

The short roots, trigonometric phases, square roots and positive divisions
in `T/integers.tex` involve fixed powers of `k`, uniformly separated
denominators and `P` precision bits. The explicit series, bisection and
integer algorithms have an absolute polynomial degree in `(k,P)`.
Substituting `P=poly(S)(1+k)` gives `poly(S)(1+k)^a` setup with absolute
`a`. Prefix coefficient streaming writes fewer than `2N` products per
diagonal, including table rewinds. This is `poly(S)Nk log(2+k)` work
and `poly(S)Nk` storage plus the additive word scratch above.

The selected-bit Walsh layer has `poly(S)Nk(1+k)^rho log(2+k)` volume
work after summing its strict recurrence. The outer convolution has
`O(log(2+k))` layers and controlled-block permutations have the third
logarithmic power. Three transforms, pointwise products, all full-stream
copies/rewinds, CRT, final rounding and carry recovery are therefore
bounded by

\[
 \operatorname{poly}(S)Nk(1+k)^\rho(1+\log(2+k))^4
 +\text{setup},
\]

with `Nk=Theta(u)` at a valid input length. All scalar record widths and
storage multipliers remain polynomial in `S`.

## 6. Aggregate setup, fallbacks and all-length space

One Walsh tree has depth `O(log(2+k))` and branching at most `S`.
One local interchange tree has the same coarse bounds. Interchange
recurses only into interchange; Walsh can invoke those trees at its
nodes. A product of these two geometric-tree bounds, times the outer
pieces/layers, bounds total nodes by
`S^a(1+k)^(a log_2 S+a)` for an absolute `a`. Every node's non-volume
preparation has absolute polynomial degree in `k` and polynomial
coefficient in `S`. Thus all setup is bounded by

\[
 G(S)(1+k)^{E(S)},\qquad G(S),E(S)\le S^a. \tag{1}
\]

This includes on-demand descriptors and instruction enumeration. Walsh
row-padding exponent `log_A W<=S` fits the same bound.

Add two explicit fallbacks after finite template generation. Retain the
original operands. Give the **aggregate** non-volume setup routines a
clock of `u` engine steps across the whole execution; do not reset this
clock per node. Mark `u+O(1)` cells on each auxiliary scratch/descriptor
tape. If the clock expires or auxiliary workspace crosses its mark,
erase tentative work and run the fixed schoolbook multiplier on the
retained operands. Stream storage is separate and has the proved
`poly(S)u` bound; retained finite code costs `poly(S)` cells.

An engine step here is one elementary read/write/head-movement transition
of the serialized binary engine, not an unbounded opcode. A setup scan,
matrix calculation or integer multiplication requires its full number of
microsteps. Clock maintenance has the separate amortized constant cost.
Input scans and copies, per-record work and fibre-offset computations
already charged to volume in Sections 2--5 are outside this **non-volume**
clock; they are not silently placed in (1).

Before materializing a padded array, compute and check its source shape
conditions within the capped auxiliary workspace. In particular require
the Walsh row padding `q'<=2q`, verify the borrowed-coordinate capacity,
the cyclic-box volume and coprimality, and the digit-width test `b<=4k`.
If any test fails, take schoolbook fallback. Thus a small input never
allocates a `W^J` row extension whose ratio to its actual rows is
unbounded. These are the finite preflight checks specified in the
candidate-generation subsection of `T/uniformity.tex`.

Each engine step has at most `poly(S)` physical interpretation cost, so
the setup clock permits at most `poly(S)u` physical work. Its amortized
binary counting and returns are those of `uniformity.tex`. Scratch
regions are reused from marked origins. Cleanup visits only previously
charged stream/scratch cells. The fallback therefore proves an
all-length visited-space bound `poly(S)(u+1)` without absorbing a
high-degree polynomial in `k` into `2^k` at small lengths.

Neither check fires in the sufficiently large regime. Put
`H=ceil(log_2 G(S))` and take `k>=64(E(S)+H+1)^2`. Then

\[
 G(S)(1+k)^{E(S)}\le2^{k/4}.
\]

Since `u=Theta(2^k k)`, this fits both the setup clock and scratch marks.
Coefficient storage, root preparation, word-multiplier scratch and stack
descriptors obey (1) or smaller polynomial bounds. A sufficient condition
is `log_2u>=S^c` after enlarging an absolute exponent; the relation
between `k` and `log_2u` is included. The source shape tests handle the
absolute prime threshold, independent of `j`.

The fallback checks are actual operations. `S^c` is an analytical bound
on their eventually successful range: the machine need not receive an
uncomputed value of `c` or the prime-gap cutoff. Numerical precision
uses the source's computed majorant rather than an unknown constant.

## 7. Assembled candidate estimate

Above the sufficient threshold the fast computation returns the exact
full product. Volume, interpretation, precision and movement cost

\[
 T_j(u)\le S^c u(1+\log_2u)^\rho
                    (1+\log_2(2+\log_2u))^4.
\]

For `eta=theta_j-rho=1/(2(j+2))`, maximizing
`(1+x)^4 2^(-eta x)` gives prefactor `O(eta^-4)`, below a fixed power
of `S`. Thus time is `S^c u(1+log_2u)^theta_j` above the stated
threshold; visited space is `S^c(u+1)` at every length, and generation
costs `S^c`. These are the candidate profiles used by the tower note.

The proof and separate review verify that each routine in this chosen
implementation is one of the priced types and uses the specified engine.
A different universal compiler, a table over the entire extension
alphabet, or an arbitrarily slow generator can invalidate the elementary
height; none is being silently treated as equivalent here.

### Verification scope

This is a mathematical implementation and cost proof. The astronomical
templates have not been generated or benchmarked; no Lean build certifies
the compiler. `verify_route_a.py` checks separate interpolation and
parameter identities, not this global theorem. The parent and independent
Route C review checked the compilation, threshold and space interfaces;
the explicit single-control, setup-clock and array-preflight clarifications
have been incorporated.

Credits: OpenAI source constructions and cited earlier algorithms;
@CubeJerry; concurrent S002 label/threshold work. The invoice was
developed with GPT-6 Astra Pro assistance.
