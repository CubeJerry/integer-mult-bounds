# Complete polynomial proportional profile and the first fixed-beta envelope

Status: **accepted complete written algorithm/profile composition**, after
independent global reviews by Routes A and C and lead source/component
audit. See `ADMISSION-P.md` for the reviewed snapshot and verification limits.

All logarithms are binary. Put L(n)=1+log2 n and x(n)=log2 L(n).
The pinned tape source is OpenAI
`math@3344da59991ed94f9ba711217b29c1d760badfa6`, November 24 build,
especially `interchange.tex`, `permutations.tex`, `walsh.tex`,
`integers.tex` and `uniformity.tex`. The predecessor programme pin is
`0607d044d1d09489580da0e5828588820e1a6775`. Its accepted Theorem Q,
rational-address height proof, source-operation classification and exact
integer assembly are inputs, with the expanded physical implementation
replaced below. The new construction is credited to the source authors,
Jerry Chen (@CubeJerry), prior programme work and substantial AI-assisted
E002 derivation/review. It is not a priority certification.

## 1. Statement and dependencies

**Theorem P.** There is one fixed deterministic finite-alphabet
multitape machine computing the exact full product of every pair of n-bit
nonnegative integers, with contiguous input/output and all head movement
charged, whose worst-case time and cells ever visited satisfy

    T(n) = O(n sqrt(L(n)) 2^{O(x(n)^(3/4) (log2(x(n)+2))^(1/4))}),
    visited cells = O(n).                                      (P1)

The constants are absolute and the displayed envelope is eventual. A
fixed exact fallback handles every other length. In particular every
fixed beta>3/4 satisfies H(n)<=2^{O(x(n)^beta)}. P1 does not assert the
beta=3/4 bound without its logarithmic factor, a polynomial-x overhead,
or the constant-overhead endpoint.

The following E002 written components supply the changed operations:

| Interface | Supplier |
|---|---|
| Rational affine address maps priced by bit height | Route A, `HEIGHT-PRICED-AFFINE-STREAMS.md` (HS/HA) |
| Whole-row short-key permutations | Route A, `SUCCINCT-ROW-EXECUTION.md` |
| Compatible small radix and multidigit leading batches | Route C, `small-radix-batching.md` (R1 and its batching lemma) |
| Full-rate factor coefficient slices | Route C, `succinct-cyclic-executor.md` (C1--C5) |
| Characteristic-two check coefficients and aligned application | Lead, `on-demand-spectral-repair.md` (SR1--SR4) |
| Complete physical binary interchange | Route C, `polynomial-interchange-invoice.md` (I1--I7), and A's address/radix interface |
| Exact rational record scaling and on-demand numerical repair | Route B, `polynomial-walsh-precision.md` (W1--W2) |
| Absolute numerical record width above polynomial threshold | Route B, same note (W3) |
| Setup absorption and actual direct selector | Route B, `separated-setup-transfer.md` (S1--S3) |

The theorem does not replace a numerical rational coefficient by a
characteristic-two coefficient. The exact finite-field processor implements
address permutations; the numerical Walsh processor acts on complex
fixed-point records, using a separate rational finite template.

## 2. A single compact family constructor

For a dyadic J>=4 let

    rho_J = 1/2 + 1/(2J),     theta_J = 1/2 + 1/J.

Retain Theorem Q's geometric parameter families. Use a power-of-two
characteristic-two distance d in [100J,200J), a rational Walsh distance
in [100J,202J], and odd m=2^u+1 with u tried through powers of two.
Increase the sufficient threshold to log2 m>=2^42 J^3 log2 J. The exact
integer guards in I5 and predecessor Q2--Q7 give

    J<=m,     log2 m<=C J^3 log2(J+2),
    Lambda_I <= m^rho_J/2,
    sigma_F/W_F <= A_F^rho_J/4,     2m<=A_F<=4m.        (P2)

The larger characteristic-two window D_pred<=24sqrt(m) and its complete
finite-conversion invoice are included in Lambda_I. No smaller old window
constant is reused. Arbitrary numerical leading padding by at most two
still leaves a contraction of at most 1/2 in the normalized Walsh bill.

The complete rational address maps, inverses, endpoints and Bruhat factors
have polynomial-m count, dimension and bit height by the predecessor
minor-height argument. Its list includes every nonzero numerator and
denominator that must be a unit. The small-radix construction chooses an
odd b<=m^C avoiding this complete list. It does not need b>W_I. Instead
ell=ceil(log_b W_I) leading digits supply a batch with padding at most two;
log W_I and ell are polynomial m. The binary exterior padding costs less
than b^2 and is therefore polynomial m.

The copied predictor formulas have polynomial size and degree O(sqrt m).
All shift versions retain the same unpruned formula shape and degree
budgets. Their cyclic module width w may be 2^{m^C}, but log w, the number
of coordinate types and every path evaluator description are polynomial
m. The finite unrolling has height ceil(log2(m)/4) and at most polynomially
many control types. Numerical Walsh batches, role matrices and their
rational heights are polynomial m, rather than merely having polynomial
logarithms. The binary and characteristic-two label sets are polynomial m.

A fixed constructor emits these compact descriptions. All data access in
that constructor can be sequential; scanning polynomial arrays for every
matrix access still has polynomial cost. The constructor may additionally
perform exact exhaustive finite checks of the finite algebraic identities.
Even allowing all frequency cases and the expanded cyclic module gives a
conservative time/space envelope 2^{m^C}; this is **additive preparation**.
No expanded verification archive is consulted while processing input
symbols. Discard it after validation and retain only compact plans. The
visited-cell allowance for preparation is still charged when discarded.

The processor has a fixed finite set of stream/arithmetic/control opcodes.
The current opcode's data are found by scans of the polynomial compact
plan, not by searching a 2^{m^C}-entry transition table. A polynomial
number of compact scans per local operation changes only an absolute
power of m. Module rows are driven by bounded-width counters and stream
lengths; iterating over occupied rows is charged to their payload volume.
This is a uniform fixed interpreter with variable data, not a growing
alphabet, growing number of physical tapes or free machine advice.

## 3. The complete interchange supplier

The local physical proof I1--I7 applies to arbitrary positive spectator
ranges and arbitrary occupied payload. Its coefficient slices are sums
of polynomially many input masks followed by fixed coordinate rotations.
For each shared-pencil query the spatially routed input is produced once,
then the coefficient acts on that stream. No spatial Q_j call is repeated
once per monomial path. All endpoint sharing and low-rank conversions use
the source's actual recursive-call invoice.

The on-demand F4 repair computes a polynomial-size check map from the m
comparison labels, with every nonzero discrepancy in F4*. The data may lie
in the extension E=F_(4^ceil(log_4 B)); the discrepancy-cube identity is
applied only to the embedded F4 values. The check map acts as H0 tensor
I_(32w), including the specified zero padding. Each converter phase has
exactly R/16 rows. Regrouping 16 parent copies rearranges only the finite
(copy,half,check) coordinates and leaves the module payload independent.
Neither free spectral access nor zero initial module rows are assumed.

Together with HS/HA and the small-radix interface, the actual nonrecursive
work is m^C V. Before every paid spatial or converter child, remove row
keys, spectral masks and temporary tags. The child sees the original
fixed-width E-symbol payload. Grouping identical module-row calls preserves
their summed volume invoice. An individual one-label group has fraction
at most 2/N_label<=2/3, not the erroneous single-row fraction 2/W_I.
Finite repair children have fraction 1/16. Full-volume reserve calls run
only after the main arrays have been merged and cleared.

Therefore the depth-first marked-region schedule has geometric parked
payload. Fixed-degree binary descriptor arithmetic is paid by the node
volume. Reuse of work and stack intervals bounds all cells ever visited.
After the one-time E encoding and binary exterior padding, the result is

    interchange on width-u fields:
    time <= m^C V (1+u^rho_J),     visited <= m^C V.      (P3)

One fixed E encoding is used at all internal spatial depths. There is no
per-level field-coordinate expansion. All constants in P3 are independent
of arbitrary prefix, gap and suffix ranges.

## 4. Outer address permutations with a polynomial coefficient

Use the actual guarded-XOR proof in `permutations.tex`. Its offset,
exceptional-rank and control calculations consist of a fixed menu of
binary integer operations and scans of the compact descriptions. A safe
bound is m^c (1+k)^e for absolute c,e. The controlled short CRT tables
have the same fixed-degree k bound as the source; no exponent depends on
J, an arbitrary control program or an expanded instruction list.

Choose

    G=(e+4+ceil(c log2 m)) ceil(log2(2k)).                (P4)

The exceptional fraction is at most 80k 2^-G. It pays the polynomial
rank/control arithmetic and O(k) stable binary radix passes over the
exceptional records. Each complete target fibre has at least 2^G records
when a guarded segment is used, paying its once-per-prefix offset work.
All spectator counters are amortized; their entire long prefix is not
reread per symbol. There are O((1+log m)log(2k)) passes. For active widths
shorter than G use the explicit individual-bit operations; this costs at
most O(GV), already inside the polynomial-m/log-k bound.

Use P3 for the equal-width interchanges in the eight-shift construction.
The two-involution position-permutation proof then has polynomial-m
coefficient. Controlled blocks add the source's two powers of log k from
batching and Beneš stages. Their resulting cost is bounded by

    m^C V (1+k)^rho_J (1+log(2k))^3
        + 2^{m^C}(1+k)^{m^C}.                           (P5)

The very generous second term covers preparation separately. Space is
m^C V plus the similarly charged preparation/descriptors. Tags have O(k)
bits and numerical records have an absolute Theta(k) width, so adding
those exceptional tags causes no unbounded proportional factor.

The outer CRT instance has at most k/2+O(log k) control positions. Its
free-bit fraction is at least one fixed positive constant above an
absolute cutoff. Each axis has at most 20ceil(log2 k) bits and the source
short construction uses blocks of at most seven axes. Thus even naive
explicit table work on at most 2^140 k^140 entries has a fixed polynomial
degree. Trial division, block matching, switch schedules, phase series,
square-root bisection and positional products use ordinary fixed algorithms.
This supplies the uniform e in P4 rather than inferring it from poly_J(k).

## 5. The separate numerical Walsh caller

Use the rational binary-label/Newton/division family from predecessor Q5,
with the source's normalized endpoint Fourier factorization. Its row
batch and completed finite contraction have polynomial-m dimensions and
branch count. Its ordinary source-map types are explicitly enumerated in
`routes/B/polynomial-auxiliary-cost-audit.md`: binary column matrices,
column parities, rational row coefficients, endpoint changes, representative
changes and their signs. Normalization cancels all slot-width-dependent
powers of two from the nonrecursive scalar list. The child transforms
supply those normalizations; no f-dependent coefficient height is hidden.

Apply the emitted binary column matrices through Gaussian elimination into
polynomially many slot exchanges/additions. P3 and the guarded XOR bound
implement these on occupied spectator ranges. Scan the O(k)-bit address
to calculate column parities once per numerical record; record width is
Theta(k), so polynomial-m repetitions cost m^C V. A full list of all
2^m spectral cases is never scanned per record. W2 computes just the
needed rational repair coefficients in polynomial-m bit operations, and
W1 applies each h-bit rational to a k-bit fixed-point record in
O((k+h+1)(h+1)) actual transitions. With h<=m^C and k>=m^C this is
m^C k per record. Every rounding error is less than one grid unit.

Apply dense small row maps by serial role scans, preserving source/target
alignment and the paid spectral converters. Their number is polynomial
m. Coefficient emission and scalar application are separate operations;
W2 does not claim to process arbitrary k-bit payload in time independent
of k. General long-times-long products, including the irrational butterfly
and outer phase/product arithmetic, still use the source fixed O(k log k)
short multiplier. Replacing that primitive by schoolbook k^2 would spoil
the final bound and is not done here.

For active width a, after excluding additive setup, the normalized physical
recurrence is bounded by

    T_F(a) <= m^C (1+a^rho_J)(1+log(2k))
                         +(sigma_F/W_F) T_F(a/A_F).     (P6)

The margin in P2 gives a geometric sum with absolute ratio at most 1/2.
Summing base-A pieces costs another polynomial m factor: even the crude
sum of at most A_F pieces per scale is polynomial m times s^rho_J.
The spectator row padding uses W_F^j with j=O(log_A s). Since W_F<=m^C
and A_F>=m, W_F^j<=(1+s)^C with an absolute C. Selected width
s<=c k/log(2+k) leaves at least 2^(k/2) spectator rows beyond an absolute
cutoff, so padding is at most two; polynomial-m guards are more than enough.
This argument never pads by the exponentially large characteristic-two
module batch, which belongs to the other processor.

The local numerical logarithmic norm gain is at most m^C. W3 proves,
using the common-ancestor argument and a polynomial number of events,
that a fixed absolute C_*k signed/fractional record width suffices whenever
k>=m^K for an absolute K. The same threshold bounds every intermediate
norm and cumulative error, not just the final boundary. Exact rational
scaling adds no coefficient approximation error. The source fixed phase
and square-root preparation supplies the remaining errors at the chosen
absolute precision. Thus the application may use the source fixed norm
and accuracy budgets (including exponent 13 and error exponent 50).

Numerical repair children have the predecessor's strict volume contraction;
Walsh spatial children have volume V/W_F. Temporary role metadata is not
passed as child payload. Process siblings, pieces and successive outer
layers in the same marked regions, parking the other arrays at current
ends. The geometric series bounds all visited payload cells by m^C V.
Fixed-degree descriptor/setup work is counted separately. This proves
both numerical and physical premises of the direct-selector transfer.

## 6. Exact integer assembly and the separated full profile

Keep the source digit length b_digit=ceil(log2 u), h=ceil(u/b_digit),
k=ceil(log2(4h)), N=2^k, and its short cyclic axis construction. Then
Nk=Theta(u) and k=Theta(L(u)), with absolute constants. The prime interval
and prime shape checks are entirely in this outer construction. Their
unknown sufficient cutoff U_abs is absolute and independent of m or J;
the algorithm tests the actual required product-size/coprimality/width
conditions and can use exact schoolbook multiplication when they fail.
The address radix in Section 2 is a different object from these primes.

The source CRT maps and their inverse satisfy P5. Three synchronized short
Fourier transforms have O(log k) layers; a selected-bit Walsh layer is
covered by Section 5, a controlled permutation by Section 4, and phases
and the one coordinatewise product use the fixed O(k log k) arithmetic.
Their schedules restore all borrowed occupied coordinates in the exact
ideal transformation. The source error analysis, with W3's fixed absolute
precision, leaves every desired convolution coefficient at distance less
than 1/2 from its exact integer. Rounding and ordinary carry propagation
therefore produce the full 2u-bit product. All scans, reverse passes,
erasures, clock and end-marker moves are charged.

After increasing absolute constants/exponents, the complete accepted
candidate has the following bound on all lengths satisfying its tested
shape and threshold conditions:

    time_m(u) <= m^K u L(u)^rho_J (1+log2 L(u))^4
                     + 2^{m^K} L(u)^{m^K},
    visited_m(u) <= m^K u + 2^{m^K} L(u)^{m^K},
    sufficient u >= max(U_abs, 2^{m^K'}).                (P7)

The large additive bound includes generation, validation, every repeated
non-volume preparation over all recursion trees, and retained descriptors.
It may overcount them. It is not multiplied into the proportional bill.
There are polynomially many actual compact child types at each stage;
spatial width shrinks by m and Walsh width by A_F>=m. Even a coarse
m^{O(1)} branching bound makes the total non-volume tree work polynomial
in the logarithmic input width, with fixed or polynomial-m degree. P7
allows the larger m^K degree in all cases.

For t=log2 L(u), the elementary supremum of
(1+t)^4 2^{-t/(2J)} is O(J^4). Since J<=m, absorb this into m^K, obtaining

    time_m(u) <= m^K u L(u)^theta_J + additive_m(u).      (P8)

For R>=2 and v<=R, the S1 calculation gives
2^R(1+log2 u)^v<=sqrt(u) whenever log2 u>=64(R+1)^2.
With R=m^K and a larger absolute K', this absorbs P7's additive time and
visited cells at a polynomial-m logarithmic threshold. The proportional
coefficients in the candidate are therefore polynomial m. The sufficient
threshold remains 2^{m^{O(1)}} plus the independent U_abs.

## 7. One actual uniform selector and common visited-cell bound

Fix once and for all exponents large enough for P2--P8. Given the contiguous
inputs, count their length n by amortized binary counters and compute an
integer q with q=x(n)+O(1) by successive bit lengths. Select the largest
dyadic J=2^h, h>=2, such that

    J^4 h <= q.                                         (P9)

If none exists, use the exact fallback. Construct the compact plan for J
and take r to be the least power of two at least 8m^K, where K covers the
proportional space coefficient. Split each input into r padded positional
chunks of u=ceil(n/r) bits. Use the source diagonal positional wrapper:
r^2 chunk products, exact positional accumulation, and O(nr) movement and
carry work. This is an actual selected machine, not an infimum over a
collection of programs or an uncharged weighted-search index.

Run all construction/validation under marked space and actual step caps
n/16, and run the complete proposed multiplication under an O(n^2) time
cap and one fixed O(n) visited-cell allowance. These caps use fixed tapes,
end markers and amortized binary clocks. An attempted advance outside a
marked allowance aborts before crossing it. A failed test, exhausted cap,
or rejected parameter erases only the already visited regions and invokes
schoolbook multiplication. The fallback is exact, takes O(n^2) time and
O(n) visited cells. Thus every input length has a total exact computation
on one fixed machine, regardless of when the eventual theorem applies.
No numerical value of U_abs is needed to run this algorithm.

Put Z=J^3 log2(J+2). Dyadic maximality in P9 gives, eventually,

    J=Theta((x/log2(x+2))^(1/4)),
    Z=Theta(x^(3/4)(log2(x+2))^(1/4))=o(x),
    log2 m=O(Z),       log2 r=O(Z).                      (P10)

In particular r<=n and log2 u=log2 n-O(Z)=(1-o(1))log2 n.
Generation and every permitted repeated additive setup have logarithm at
most 2^{O(Z)}(1+x)=2^{o(x)}, whereas log2 n is of order 2^x. Their total
is n^{o(1)} and eventually passes the n/16 construction/time/space caps.
The sufficient 2^{m^K'} threshold is also eventually satisfied because
m^K'=2^{O(Z)}=o(log2 u). The independent fixed U_abs is eventually passed.

The chunk workspace satisfies m^K u<=n/8+m^K<=n/4 for large n. Additive
regions consume at most n/16 after the same threshold argument. Reuse
those regions for every chunk product and reuse the positional assembly
buffers. Input, output, clocks and wrappers add only a fixed multiple of
n. This is one uniform bound on the union of visited cells. A per-call
space constant depending on J has not been left unnormalized.

The successful total time is at most

    m^K r^2 u L(u)^(1/2+1/J) + O(nr) + n^{o(1)}
       <= n sqrt(L(n)) 2^{O(log2 m)+O(x/J)}.             (P11)

Here r^2u<=2rn, r=m^{O(1)}, and L(u)<=L(n). The same bound is n^{1+o(1)},
so the O(n^2) outer clock does not abort at sufficiently large n. P10
turns P11 into P1. Only finitely many exceptional lengths use the fallback;
the absolute eventual big-O bound can absorb that finite range. This
completes the proof.

## 8. Scope and verification gate

The new logarithmic overhead scale is smaller than the predecessor
x(log log x/log x)^(1/3): their ratio tends to zero. This compares two
explicit proved upper envelopes; it does not compare runtimes against an
unspecified published o(1) or prove a lower bound on any machine.

The argument replaces the expanded execution coefficient, not the
cubic-logarithmic geometry construction. The latter is still present in
P2 and produces the 3/4 power after balancing. A separate variable-arity
research route is not a premise of P1. Its radix, space and numerical
interfaces must be proved before any stronger envelope is admitted.

Current evidence is a written mathematical construction, source audit,
independent component reviews and isolated exact finite replays with
negative controls. No full tape multiplier, proof-assistant refinement,
human refereeing, numerical practical cutoff or exhaustive novelty audit
is claimed. Independent global reviews must check every P2--P11 interface,
especially grouped child volumes, unchanged query sharing, metadata
stripping, distinct scalar domains, branch/setup bounds and common space.
