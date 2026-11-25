# From an expanded local template to a quantitative tape ledger

Status: **partial compiler derivation**. The recursion, precision and space
estimates below are explicit. A uniform coefficient for every primitive and
a bounded generator have not yet been certified. No complete conditional
overhead theorem is claimed from this note.

Source pin: OpenAI `math` `3344da59991ed94f9ba711217b29c1d760badfa6`. Read in
detail: the November tape manuscript's `interchange.tex`, `permutations.tex`,
`walsh.tex`, `integers.tex`, `uniformity.tex`; the November Fourier
`binary.tex` and `repair.tex`; and the September tape manuscript
`sections/02-streams.tex`, `sections/04-swap.tex` for primitive operations and
depth-first scheduling. A source proof being read is not a Lean/kernel build.

## 1. A noncircular size parameter

Use an **expanded local certificate**, not a final multiplication program or
its runtime. It contains:

* the interchange arity m, reserves a, batch width W_I, radix prime b,
  explicit finite scalar algebra, rational coordinate bases and their
  lower-triangular/permutation factorizations;
* the full one-level interchange instruction list, including every call,
  stream role, endpoint preparation, fixed row map and spectral table;
* Walsh arity A, batch W_W, call count sigma, every dyadic coefficient,
  column-function truth table, binary reindexing and one-level instruction;
* a rational exponent rho in (1/2,1), and positive rational margins eta_I,
  eta_W certifying the exact numerical contraction inequalities below.

Arity, dimension, row-role and instruction lists are expanded. Encode their
dimensions in unary as well as normal binary headers, so their numeric values
do not exceed the certificate length. Encode coefficient numerators,
denominators and radix b in binary. Let B>=16 be total length, enlarged by
the unary dimensions if necessary. This has no input length n and no final
runtime in its definition. In particular, all dimensions and instruction
counts are <=B, b<2^B, rational coefficient heights are <=2^B, and a positive
rational margin represented within B bits is >=2^-B.

This representation is deliberately conservative. A succinct circuit can be
expanded to it, but its succinct size is not silently substituted for B.

## 2. Exact recurrence margins

Let K_I count the main interchange calls over the W_I input streams before
the first-digit batching padding. Its actual recurrence coefficient is

    lambda_I = 2 K_I/W_I + 2a.

The local certificate must verify

    lambda_I <= (1-eta_I) m^rho,
    sigma/W_W <= (1-eta_W) A^rho.                         (C1)

The source's intermediate gamma estimate is a sufficient way to obtain the
first inequality, but the compiled ledger uses its actual integer call count.
Rational-power comparisons are decidable by raising to the denominator of
rho. The margins are finite arithmetic data, not assumed timing constants.

If local nonrecursive interchange work is <=K(B)V, induction/geometric
summation gives per-volume time <=C K(B) eta_I^-1 e^rho, after paying the
bounded base widths. The base range e<m+2a+1 contributes at most a factor
polynomial in B times the cost of a single radix-b digit operation.
Binary-to-radix padding costs <b^2<2^(2B) in both volume and time.

For Walsh, if one node costs at most
K(B)V(1+u^rho)(1+log(2+k)) plus setup, the exact child volume V/W_W gives
the normalized recurrence with coefficient sigma/W_W. Its geometric constant
is at most eta_W^-1<=2^B. Summing base-A pieces adds at most a polynomial B
factor, since rho>=1/2 and A>=3.

Thus neither recurrence introduces an unquantified inverse gap once (C1) is
included. It remains to bound K(B) from the explicit primitive processors.

## 3. Instruction counts and numerical precision

A pointwise scalar update has coefficients of height <=2^B on <=B live
registers. Giving every serialized update/copy its own instruction, a
conservative one-level gain is

    C_B <= 2^(4B^2).

This allows all partial sums and copies, rather than only the final row map.
The source depth bound d<=1+ceil(log_A(1+k)) consequently gives

    C_B^(2d+1) <= 2^(20B^2) (1+k)^(8B^2).                 (C2)

At most B child calls occur per node. P3 bounds all nodes in all Walsh pieces
by 4B(1+k)^B; multiplying by B local instructions leaves at most
4B^2(1+k)^B array instructions. Therefore their total propagation gains
have a majorant of the form

    2^(C B^2) (1+k)^(C B^2)                              (C3)

for an absolute numerical C. Combining the fixed digit-norm allowances and
error tolerances in `integers.tex` with P2 shows that, above an explicit
k=O(B^4) threshold (with a sufficiently large absolute coefficient), the
record width can be one fixed multiple of k, independent of B. The B-bit
dyadic constants are then exactly representable. This conclusion is specific
to the original dyadic Walsh template; replacing it with algebraic factors
requires the separate coefficient-approximation ledger.

The large B-dependent gain has been moved into a validity threshold; it has
not vanished. Below it a candidate must use a correct fallback or abort.

## 4. Physical space and serialization

There are at most B local roles. Encoding scalar-algebra entries as fixed
binary blocks and replacing row operations by scans adds polynomial factors
in their explicit description length. Rational field scalings are more
costly: multiplying a field by a fixed integer c has |c| increasing pieces
in the source elementary-stream proof. Since |c|<2^B, that is at most an
exponential B-dependent scan/stream factor, not a unit-cost operation.

At an interchange main descent, active volume contracts by at most 2/W_I;
the source chooses W_I>2. The parked-volume sum is therefore at most three
times its root-scale local bound. A full-volume reserve descent parks only
its descriptor, after merging/clearing the main arrays. Walsh descents shrink
volume by 1/W_W<=1/2, giving another geometric parked-volume sum. All siblings
and successive pieces reuse their marked work areas.

Rational radix padding has factor <2^(2B). Thus the stream contribution to
space is bounded by 2^{poly(B)} times input volume, provided the primitive
processors have their stated linear-space bounds. Descriptor/setup workspace
must be added separately; a bound G(B)(1+k)^{E(B)} can be absorbed into 2^k
by P2 after its explicit cutoff. Fixed retained code belongs to additive d_j,
not to proportional c_j, in A4.

## 5. The remaining primitive estimate is concrete

The following route to an explicit K(B), G(B), E(B) is under audit:

* Binary integer arithmetic, finite-field operations, and table scans on the
  expanded B-bit data have polynomial B overhead. Ordered rational scaling
  may cost 2^{O(B)} passes. Its variable-width arithmetic is polynomial in
  field width, paid by the complete field range as in September Section 2.
* Bulk XOR tags at most a 80k 2^-G fraction of records. If offset/rank
  computation is bounded by K(B)k^e, choose guard length at least
  (e+3+ceil(log2 K(B))) ceil(log2(2k)). This explicitly pays the polynomial
  exception computations and stable binary radix sorts. The number of guard
  passes increases by the same declared factor.
* Short-Fourier blocks contain at most seven axes, each of width at most
  20 ceil(log2 k), hence at most 2^140 k^140 coordinates. Trial division for
  the source prime search is polynomial of fixed degree in k. The explicit
  matching/Beneš constructions, Machin/sine/cosine series and bisection also
  have fixed polynomial degrees once implemented by the described algorithms.
  A bare phrase `poly(k)` is insufficient for the final bound: a common
  concrete degree and coefficient must be supplied for those implementations.

The source geometries make a uniform polynomial degree plausible, but this
note deliberately does not turn that plausibility into a certified numerical
exponent. In particular, a constant hidden in an unspecified processor is
not bounded just by counting its visible instructions.

## 6. Generation cannot be bounded by output size alone

A total computable generator can delay an arbitrarily long finite time before
printing the same short valid template. Therefore output-certificate length B
alone supplies no bound on its generation time g_j. The source's assertion
that an enumeration terminates is not a growth bound.

Two legitimate completions are available:

1. Specify the actual construction/search order and bound every arithmetic
   operation before reaching the given certificate.
2. Specify a finite certificate language with a proved bounded verifier, then
   enumerate certificates by length. If verifying a B-bit certificate takes
   at most 2^{B^c} steps, exhaustive search up to length B costs at most
   2^{O(B^c+B)}. The verifier must establish every required local identity and
   compatibility condition; calling an arbitrary local table 'valid' is not
   such a verifier.

No such complete verifier is implemented or proved here. Generator time and
workspace remain independent profiles g_j,d_j in A10. This is a precise
remaining uniformity obligation, not a reason to discard the valid recurrence
or precision estimates.

## Open next questions

Complete the common primitive processor bounds, then specify the finite
certificate verifier or a bounded constructive generator. Only then promote
the proposed 2^{poly(B)} ledger to an end-to-end compiler theorem and derive
an explicit envelope from a proved B_j growth law. Credits: the two cited
OpenAI tape papers and Fourier construction; @CubeJerry; AI-assisted audit.
