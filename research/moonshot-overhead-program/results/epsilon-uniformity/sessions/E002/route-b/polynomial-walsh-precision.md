# Polynomial precision and exact rational scaling for the Walsh branch

Status: **source-specific numerical component, awaiting independent review**.
This proves numerical precision and rational record-processing bills. It
does not by itself prove cheap physical routing, module-index movement or
a complete multiplication envelope.

Pins: OpenAI `math@3344da59991ed94f9ba711217b29c1d760badfa6`, tape
`build/walsh.tex` and `build/uniformity.tex`; programme predecessor
`0607d044d1d09489580da0e5828588820e1a6775`, Route B
`pairwise-newton-division.md`, `polynomial-auxiliary-cost-audit.md`, and
`growing-arity-circuit-candidate.md`.

## 1. A fixed-tape rational scaling primitive

**Lemma W1.** Let a signed rational coefficient `a/b`, `b>0`, have
numerator and denominator bit length at most `h>=1`. Let `X` be a signed
integer represented in at most `k` bits. A fixed finite-alphabet multitape
machine computes

\[
Y=\lfloor aX/b\rfloor
\]

in `O((k+h+1)(h+1))` actual steps and `O(k+h)` visited cells, plus fixed
constant changes for the output sign convention. Constants do not depend
on `a,b,h,k`. Coefficients and inputs are supplied on separate tapes.

**Proof.** Multiply the long integer `|X|` by the short integer `|a|`
using at most `h` shifted-addition passes. Each pass traverses at most
`k+h+1` bits, including head returns; it uses a fixed number of tapes and
costs `O(k+h+1)`. The intermediate product fits `k+h+1` bits.

Divide that product by `b` from its high bit toward its low bit. Maintain
an `h+1`-bit remainder. On each incoming bit, shift the remainder, compare
to `b`, optionally subtract, and emit one quotient bit. Each iteration
costs `O(h+1)` physical steps including scanning and returning the remainder
head. The quotient has at most `k+h+1` bits. This is ordinary restoring
binary long division, with no random-access arithmetic. If `aX<0` and
the unsigned division has nonzero remainder, negate the quotient and
subtract one; otherwise only negate. A final scan supplies canonical
output. Reuse the same remainder/product regions throughout. ∎

Consequently, if a numerical record represents `X/2^p`, W1 returns the
same-grid rounding of `(a/b)(X/2^p)` with absolute error less than `2^-p`.
The rational coefficient is used exactly; no coefficient-approximation
error or preparation at `p` fractional bits is needed for this operation.
The numerator may be zero and `b=1` causes no exceptional case.

When `h<=m^C` and `k>=h`, this costs `m^{O(1)}k` per record and uses
`O(k)` temporary space. It therefore has a polynomial-in-m coefficient
per encoded bit volume. This is distinct from arbitrary multiplication
of two `k`-bit values, for which the source still uses its fixed short
`O(k log k)` multiplier. Norm growth from a large rational numerator is
handled in the precision proof below, not ignored.

## 2. On-demand rational check-space coefficients

Use the preceding rational Walsh construction. It has odd `m`,
`W=2^ceil(log_2(m+1))=O(m)` binary shifts, a degree `D=O(sqrt m)`
Newton predictor and `s=W/16` check rows. For a spectral tuple
`k=(k_1,...,k_m)` in `{0,1}^m`, its shift count is

\[
c_t=\sum_j(k_j+\beta_j(t)\bmod2),\quad
p_t=(-1)^{u-\sum_j\beta_j(t)}
       \sum_{h=0}^{D}(-2)^h\binom{c_t-u}{h},\quad
z=(-1)^{\sum_j k_j}.                                  \tag{W1}
\]

**Lemma W2.** From the `m` spectral bits, one fixed multitape machine
computes the actual defect set `J={t:p_t!=z}` and emits the exact coefficient
matrix of the entire `2s`-by-`2s` rational check-space table in polynomial-
in-m bit operations and cells. Every entry has polynomial-in-m bit height.
No `2^m` table enumeration or lookup is required.

**Proof.** Enumerate the `W=O(m)` seeds and compute the `m` parities by
ordinary binary dot products. The count is an `O(log m)`-bit integer.
Evaluate generalized binomials by the exact integer recurrence
`B_0=1`, `B_h=B_(h-1)(c_t-u-h+1)/h`; integrality holds for every integer
`c_t-u`, including negative values. Numerator and denominator bounds give
bit length `O(D log(m+D+2))` for `B_h` and the predictor partial sums.
All `W D` operations therefore have polynomial bit cost. Select the
actual defect set; outside-window counts that accidentally predict
correctly are excluded, so no zero gap is inverted.

The check nodes are `x_t=t/W`. Restrict the first `ell=|J|` Vandermonde
rows to J to get `V_J`. Construct its entries exactly and solve by
fraction-free elimination with tested pivots (or by the explicit Lagrange
formula). Its determinant is a product of nonzero rational node gaps, so
the procedure terminates. Recover the error vector from the two input
check vectors, divide its entries by the known nonzero integer gaps
`p_t-z`, solve with `V_J^T`, zero-pad to s and return `(a,za)`.
The `ell=0` case returns zero and performs no division.

The common-denominator bound in the predecessor proof is

\[
O(s^2\log(W+2)+sD\log(m+D+2))                         \tag{W2}
\]

bits for table entries: use the squared Vandermonde determinant and the
product of the nonzero integer gaps. This is polynomial in m. Fraction-free
intermediates are minors of polynomial-dimensional matrices of such
entries and have polynomial bit height as well. Even a sequential scan
through the entire stored polynomial-size matrix for every access adds
only a fixed polynomial factor. Thus the implementation is on actual
fixed tapes, not an arithmetic model with random access. ∎

The existing two-predictor repair identity and its small phase volume are
unchanged. The table is still sandwiched between the paid forward/inverse
conversions. This lemma never moves a spectral mask through an unperformed
converter. The fields used for these numerical rational coefficients are
not reduced into the characteristic-two interchange field.

If physical rows are aligned in the converter's spectral-address order,
the selected table acts identically at every spectator/module coordinate.
At most polynomially many serial role scans suffice to apply its dense
small row map. Compute a coefficient using W2 and apply it to a `k`-bit
record by W1. The total is `m^{O(1)}V` actual work for encoded bit volume V,
once the m spectral bits are supplied by the source column-parity scans.
Those scans examine `O(k)` address bits per numerical record, already paid
by its `Theta(k)` record width. Reused coefficient and accumulator regions
have polynomial-in-m proportional space. This physical statement includes
the aligned-row/available-spectral-bits interface explicitly.

## 3. Expanded spectral cardinality does not control norm growth

For sufficiently large admissible m, the predecessor source-map audit gives
an absolute `K` with all of the following:

* arity `2m<=A_m<=4m`, batch width and recursive branch count at most `m^K`;
* at most `m^K` local rational row operations per numerical coordinate;
* row-block dimensions, simultaneously held row roles and coefficient bit
  heights at most `m^K`;
* polynomial-in-m ordinary operations and coefficient heights after the
  finite depth-`O(log m)` contraction is fully unrolled.

These are precisely the rational branch of
`polynomial-auxiliary-cost-audit.md`; they do not include a claim about
physical routing cost. A data-dependent spectral table is block diagonal
over the spatial addresses. Its operator norm is the maximum norm of a
small block, not the sum over the `2^m` possible cases.

In particular a block of side at most `m^K`, with entries bounded by
`2^(m^K)`, has Euclidean operator norm at most `m^K 2^(m^K)`. Applying
one at each address has the same norm bound. W2 supplies the actually
selected block. Alternatively a literal exhaustive lookup could copy its
coefficient exactly before W1; the slow lookup adds time, but no numerical
rounding events and no factor `2^m` in the ideal block-diagonal norm.

Copies, masks and accumulations have polynomial dimension and the same
coarse bound. Permutations are isometries. Completed normalized child
transforms are unitary. Therefore, for a larger absolute `K_1`, a product
of all nonchild operations at one node has

\[
\log_2 C_{\rm level}\le m^{K_1}.                      \tag{W3}
\]

This includes intermediate partial sums; it is not merely the norm of the
completed predictor. Matrix entries may be much larger than one, and their
full bit heights are in W3.

## 4. Uniform working precision above a polynomial threshold

**Theorem W3.** Fix absolute input norm and desired output-error exponents
`B,D>=1`. There are absolute `C,K_2` and a fixed numerical evaluator for
the rational Walsh template such that, for `N=2^k` and

\[
k\ge m^{K_2},                                        \tag{W4}
\]

inputs of Euclidean norm at most `2^(Bk)` are transformed with every
completed boundary error at most `2^(-Dk)`, using at most `Ck` signed
integer and fractional bits per real component. The precision calculation
does not depend exponentially on the number of spectral cases. Constants
depend only on B, D and the fixed source-operation bounds, not m or k.

**Proof.** A spatial recursion path has depth at most
`1+log_(A_m)(k+1)<=C log_2(k+2)`. For two instructions, follow their paths
to the first common ancestor, as in `uniformity.tex`. W3 bounds the
propagated-error gain by

\[
G_{m,k}\le2^{C m^{K_1}\log_2(k+2)}.                   \tag{W5}
\]

Completed intervening pieces are unitary. Padding/restriction have norm
at most one; fixed copies and masks are included in W3.

Because branching is at most `m^K` and `A_m>=m`, a full recursion tree
has at most `m^{K+1}(k+2)^{K+1}` nodes after increasing K. There are at
most `O(m log(k+2))` base-A pieces. Counting their local arithmetic gives
at most `m^{K_3}(k+2)^{K_3}` whole-array arithmetic events, for an absolute
K3. The number of live/padded numerical coordinates per event is at most
`m^{K_3}2^k`. No factor `2^m` appears: a table selection is exact and one
block is used at each address.

At precision p, W1 introduces coordinate error less than `2^-p` on each
rational scalar update. A whole-array rounding error is consequently at
most `m^{K_3}2^{k/2}2^-p`. The one fixed irrational butterfly coefficient
and the source's root/phase arithmetic may instead introduce a coefficient
error times the current input norm. With an allowed bootstrap norm cap
`2^((B+2)k)`, the same argument bounds every fault by
`m^{K_3}2^((B+3)k)2^-p`. Existing fixed-degree phase preparation computes
those coefficients to p bits; its actual cost is separate from this error
bound and remains charged by the source compiler.

Freeze each fault and propagate it through exact linear maps. Summing
their number and W5 shows that the total error at any intermediate or
completed boundary is at most

\[
2^{-p+(B+3)k+C' m^{K_4}\log_2(k+2)}.                 \tag{W6}
\]

Choose a larger `K_2` so that, whenever W4 holds,
`C' m^{K_4}log_2(k+2)<=k`. Such an absolute choice exists: for `k>=2`,
`log_2(k+2)<=3sqrt(k)`, and `k>=m^{2K_4+C_0}` with a sufficiently large
absolute C0 makes `3C' m^{K_4}sqrt(k)<=k` for all m>=2. Take
`p=ceil((B+D+5)k)`. W6 is then smaller than `2^(-Dk)`.

Ideal intermediate norm is at most `G_{m,k}2^(Bk)<=2^((B+1)k)` under
the same threshold. Adding the just-bounded numerical error preserves
the bootstrap cap `2^((B+2)k)`, by induction through instructions.
This justifies `O(k)` integer width as well as fractional width. Temporary
exact products in W1 have width at most `Ck+m^K=O(k)`. The source's
general short products have at most twice the record width. ∎

The source final convolution/carry proof needs fixed absolute norm and
error exponents. It can therefore use W3 with corresponding fixed B,D.
No approximate output or probabilistic correctness is introduced.

## 5. Preparation and remaining physical interfaces

The elementary exact coefficient work in W2 is polynomial m and may be
performed on demand. A full optional spectral-table archive can still have
`2^(m^C)` size. Merely creating that archive does not require per-volume
scans through it. Any implementation that does scan it per record must
charge that time, although W3's precision bound remains valid.

Computing a complete finite rational template and all remaining source
phase tables at precision O(k) has conservative additive bill
`2^(m^C)(1+k)^{m^C}`. Lemma S1 in `separated-setup-transfer.md` absorbs
such work above a polynomial-in-m logarithmic-input guard. Numerical
template dimensions, norm amplification and scalar arithmetic therefore do
not force the previous expanded-table threshold `k>=P_m^C`.

Still separate: all physical endpoint/address rearrangements; the succinct
characteristic-two module executor; radix and leading-row padding; unchanged
recursive-call coefficients; and uniform visited-space composition. This
note supplies no new unconditional multiplication bound on its own.

Open next questions: independently audit W1's actual record layout and W2's
height bound; compose W3 with the final fixed macro executor and its precise
branch trace; replay exact signed rational rounding and zero-gap controls.

Credits: @CubeJerry; the pinned OpenAI precision argument and its sources;
S002 rational predictor, check inverse and source-operation audit; ordinary
binary multiplication/division; substantial ChatGPT multi-agent assistance.
