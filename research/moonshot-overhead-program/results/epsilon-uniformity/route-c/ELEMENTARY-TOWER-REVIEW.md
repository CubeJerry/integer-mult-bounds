# Independent audit of the proposed elementary-height extraction

Status: **compiler and threshold audit passes with the explicit implementation
reading below**. This audits `../route-a/elementary-tower-extraction.md` and
`../route-a/compiler-invoice.md`, as read on 2026-11-25. It is not a second
independent multiplication construction or an endpoint result.

The review tested for an omitted exponential, a parameter-dependent
arithmetic degree on streamed data, a multiplied child volume, or an
uncharged visited-space term. No substantive obstruction was found. The
aggregate setup clock and scratch caps in the invoice are material to the
all-length claim.

## 1. Source audit and finite-description budget

At OpenAI `math` commit `3344da59991ed94f9ba711217b29c1d760badfa6`, the review
inspected the relevant November `interchange.tex`, `permutations.tex`,
`walsh.tex`, `integers.tex`, and `uniformity.tex`, and the original Fourier
predictor, matrix-root, Hermite repair, routing and normalization proofs.
The September predecessor's `build/sections/02-streams.tex` and `04-swap.tex`
were read for the actual counter, scaling, descriptor, triangular-factorization
and parking algorithms. S002's label and threshold estimates were checked
against these interfaces. Unspecified fixed-parameter constants were not
assumed to be polynomial in the new budget.

After a fixed power enlargement, `S` must dominate total binary description
length, total instruction count, role counts, radix and integer scaling
values, numerical coefficient bit lengths, and generator work and space.
Individual-entry bounds alone would not suffice. The proposed extraction
bounds both entries and their counts, allowing this enlargement without
changing `S<=E_3(CZ)`.

The address geometry has polynomially many labels and rectangles in `m`:
`N<=m^4`, and a disjoint partition has at most `N^2` nonempty rectangles.
The rational matrices have polynomial dimension. Even bit-length doubling
at every rational operation gives heights `2^(poly(m))`, hence absolute
values `E_3(O(Z))`. Products of polynomially many such values stay at this
height. Trial division for a prime above that product and the batch width
costs a fixed polynomial in their values, so adds no fourth exponential.

The original predictor has raw row count `R_0=2^m b_0^H`, with
`H<=(m+1)^(d+1)` and `d=O(sqrt(m log m))`; hence `R_0<=E_3(O(Z))`.
The cyclotomic extension is represented by its basis, not by all its
elements. Lagrange product formulas and geometric-sum inverses of root
differences use polynomially many operations on arrays of polynomial
length in `R_0`. In characteristic zero, multiplying such arrays adds
operand coefficient heights and a logarithm of the convolution length.
Products of polynomially many factors therefore have polynomial bit
lengths. This verifies the place most likely to create an additional
alphabet or coefficient tower.

## 2. Stream compilation and counter access

One fixed interpreter of binary instruction data, with a common finite
alphabet and tape count, suffices. No Cartesian product of all logical
roles' control states is needed. Complete sequential scans of the finite
instruction and scalar lists already cost only `poly(S)`.

A split into at most `S^2` classes can use polynomially many full scans.
Scaling by an integer of absolute value at most `S` has at most `S`
monotone pieces, with a polynomial-length selector. Inverse scaling
reverses the same split and merge. At a width-`f` target, offsets and
rational units use arithmetic on `O(f log b+log S)`-bit words. Its
degree is absolute, while the number of terms is an outer `poly(S)` loop.
A fixed power of `f` is absorbed by the complete `b^f` target range.
If suffix lengths enter the calculation, their bit costs are absorbed
by the complete suffix range as in the invoice.

An implementation clarification matters for this argument: decompose a
triangular sum `y <- y + sum_i a_i x_i` into its single-control updates.
They commute and leave the control fields unchanged. Each update then
uses an absolute fixed number of collapsed formal fields and counters,
as in the predecessor's elementary-stream lemma. This realizes the
factor `poly(S)` as an outer loop. It avoids assuming constant-time
access to one of `S` binary counters stored at different tape locations.
The numerical Walsh selector may instead scan all its fields per record,
because its record already has width at least the top address width `k`.

With these collapsed fields, the source's local counter resets and ripple
analysis avoid rereading full spectator descriptions per data bit.
Initial descriptor work is `poly(S)(1+log V)^c` for absolute `c`, and
is `poly(S)V`. Coordinate changes use polynomially many triangular
updates and at most dimension-minus-one exchanges. Extraction, parking,
restoration and interpretation are parent charges. They do not replace
a child's logical data volume by the larger serialized workspace volume.

The packed-XOR guards also retain absolute polynomial degree. Controls
are selected bits, fixed binary column maps, or tables on the source's
fixed-power short blocks. Their parameter-dependent coefficient remains
`poly(S)`. The exceptional fraction `O(k 2^-G)` absorbs the power of
`k` for an absolute guard coefficient; it need not absorb the `S`
coefficient. Narrow chunks use direct bit moves. No factor
`k^(poly(S))` is introduced on every data record.

## 3. Descendant count, setup and threshold

After enlarging `S`, one node has at most `S` calls and fixed-list
instructions. Address widths contract by at least two, so depth is
`O(log(2+k))` with an absolute constant. One tree has at most
`S^(C log_2(2+k))=(2+k)^(C log_2 S)` nodes. A Walsh node may invoke
interchange trees; interchange recurses only into interchange. Their
product, times top-level pieces and layers, remains a polynomial in `k`
with exponent `O(log S)` plus an absolute constant. This is below the
invoice's conservative `G(S)(1+k)^E(S)`, with `G,E<=S^c`.

This is additive setup. The supplied inequality

\[
 k\ge64(E+H+1)^2
 \quad\Longrightarrow\quad
 2^H(1+k)^E\le2^{k/4}
\]

absorbs it into the full `2^k` record volume above a threshold which is a
fixed power of `S`. It also handles row padding, whose exponent is at
most `log_A W<=S`. Accepted integer shapes have `Nk=Theta(u)` with
absolute constants. Their prime-box threshold is an absolute source
constant and may remain separate as `U_0`.

The fixed one-half interchange and one-quarter binary contraction margins
give absolute geometric denominators. Thus summing the volume recurrences
preserves `poly(S)` constants and the displayed powers of the width.

## 4. Precision and short arithmetic

With at most `S` roles and instructions and coefficients of at most `S`
bits, a one-level pointwise operator has norm at most `S^C 2^S`.
A complete node's product bound therefore has binary logarithm at most
`S^C` for absolute `C`. Completed children, address permutations and
complete intervening pieces have unit norm at the relevant boundaries.

The common-ancestor argument gives gain logarithm
`S^C log(2+k)`. Counting faults adds the same type of term. Digit norms,
the sole coordinatewise product and the final scale have logarithms
`O(k)` with absolute coefficients; fixed coefficient storage adds at
most `S`. Thus signed and fractional widths `S^c(1+k)` suffice. This
bounds bit lengths without enumerating coefficient magnitudes. The
source's computed majorant makes the precision choice effective, without
needing the analyst's smallest exponent `c`.

An interchange subroutine permutes the bits of the numerical record
exactly. Its temporary arithmetic over a finite field contributes no
floating-point errors and has norm one at its returned boundary. It
must not be included as a nonunit numerical gain at every inner stage.
Conversely, the pointwise dyadic maps of the Walsh template are included
in the one-node norm product above.

Phase orders and block dimensions are fixed powers of `k`. Their source
preparation routines have absolute polynomial degree in precision.
Replacing precision by `P<=S^c(1+k)` introduces only `poly(S)`.
The independent short multiplier costs `O(P log(2+P))`, at most
`poly(S)k log(2+k)` above the threshold. Its scratch is bounded by its
own time; only one such multiplication is active at once. The resulting
`poly(S)poly(k)` scratch charge is additive and eventually absorbed by
the top volume. A linear-space theorem for the short multiplier is not
being assumed.

## 5. Visited space and the actual fallback

An interchange main descent has relative volume at most `2/W<=2/3`,
and a Walsh descent has ratio at most one half. Their polynomially many
local roles therefore give a geometric sum of parked data volumes.
Full-volume reserve descents clear numerical work and park only
descriptors. Total descriptor and word workspace along a path is
`poly(S)poly(k)`. Siblings, pieces and subroutine invocations reuse
marked regions, so this reasoning concerns visited cells.

The invoice's additional all-length mechanism is appropriate. Preserve
the original operands, put one aggregate `u`-step clock around all
non-volume setup, and mark `u+O(1)` auxiliary cells on each fixed scratch
tape. On exhaustion, erase tentative data and use schoolbook on the
preserved operands. The clock must not be reset per node. Its amortized
counter overhead is charged, and physical interpretation multiplies
its permitted work by only `poly(S)`.

The numerical stream allocation still requires the source's shape tests
before allocating a padded layout. On an accepted shape it has
`poly(S)u` volume; finite code adds `poly(S)`. The auxiliary cap handles
the otherwise troublesome short lengths where a high-degree polynomial
in `k` could exceed `u`. Cleanup traverses only previously charged
regions. This proves `poly(S)(u+1)` visited space at every length,
including a late abort after some correct numerical layers have run.

For the sufficiently large regime, total setup and scratch are bounded
by `2^(k/4)`, while `u=Theta(2^k k)`. Therefore neither cap fires. The
asymptotic threshold follows without the machine receiving an unknown
absolute constant or the prime-gap cutoff as advice.

## 6. Chunking, scheduling and conclusion

A power-of-two chunk count between `4S^c` and `8S^c` gives the common
linear cap at sufficiently large input lengths. Gathering, chunk
products, carry propagation, generation and cleanup add fixed powers
of `S` to the attempt constant. After a power enlargement, a sufficient
threshold is `log_2 N_j<=S^c+O(log S)+log_2 U_0`.

For an explicitly specified nondecreasing-sum diagonal order, the pair
index is `O((j+log S)^2)`. Therefore `S<=E_3(CZ)` gives the proposed
double-exponential logarithmic bounds `(T)`. The arbitrary phrase
“computable diagonal order” alone would not fix this quantitative bound;
the invoice correctly specifies an order and a particular generator.

The final optimization is consistent. With
`y=log_2 log_2(x+16)`, choosing `j` of order
`(y/log(y+2))^(1/3)` makes the penalty and feasibility bills at most
`sqrt(x)` and leaves residual exponent cost `x/(j+2)`. This gives the
stated explicit but very weak subpower certificate.

Every required expense in this particular compiler can thus be bounded
by a fixed power of `S`; no additional exponential was found. The
single-control decomposition in Section 2 is a useful explicit detail
for the implementation proof. It does not change the claimed tower.

This is a mathematical source audit. The enormous finite templates were
not physically generated, and no numerical experiment or formal-proof
build certifies this global claim. The component verification script
checks separate identities only. The extraction quantifies the original
source construction; it does not settle the square-root endpoint or
show that realistic inputs reach its fast regime.
