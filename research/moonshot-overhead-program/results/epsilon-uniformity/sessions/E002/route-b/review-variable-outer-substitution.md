# Independent check of the variable outer substitution

Verdict: **PASS as a source-substitution theorem conditional on its two
physical suppliers**. Reviewed Route A VARIABLE-OUTER-SUBSTITUTION.md,
SHA-256 782ccc6677a2343a7797eaf72c4e27c50b25b722d4ec4fd2207a2ccba0408602,
including the added local-active-width routing supplement.
This independently checks that theorem's outer scope. It does not use an
outer multiplication conclusion as a premise for the interchanger.

Source pin: OpenAI math 3344da59991ed94f9ba711217b29c1d760badfa6,
November tape permutations.tex and integers.tex in full, plus the
selected-bit Walsh layout and precision paragraphs in walsh.tex.
These source files were reread for this review.

## 1. Replace the interchanger in the source proof operations

Put \(E_C(k)=2^{C\Phi(\log_2(k+2))}\). The exact-interchanger supplier
has time \(V\sqrt{U+1}E_C(U)\) and visited space \(VE_C(U)\).
The ordinary guard proof uses eight shifts and a fixed number of
interchanges of width L for each guarded pass. It therefore gives
\(V\sqrt{L+1}E_C(L)\) before its O(log k) pass count. This is a
substitution in the actual operations, not a choice of a different
fixed rho in a theorem whose implicit constants could grow.

Control, offset and destination-rank calculations have one absolute
polynomial-k bound. Growing numerical parameters have m<=k and
polynomial(m,k) control complexity, so a fixed guard
G=C_G ceil(log2(2k)) still suffices. The exceptional fraction
80k 2^-G pays the polynomial rank computation and all O(k) sorting
passes. Destination tags have O(k) bits, a constant factor of the
numerical record width. Widths L<G use direct moves, whose LV bill is
bounded by GV. There is no per-record call to the finite generator.

The two-involution position proof uses a bounded number of bulk XORs
and has polynomial-k preparation. Controlled small blocks then use
the same fixed free-control fraction, O(log k) block batches and
O(log k) Beneš stages. These multiply only the visible logarithmic
time factor, not the visited-volume coefficient. Work regions are
reused, and borrowed auxiliary coordinates are restored.

## 2. The source integer shape does not acquire a variable-family loss

The source digit and record choices satisfy Nk=Theta(v) and
k=Theta(log v), with absolute constants. Its odd primes on short
cyclic axes are independent of the interchange address radix.
They are found by polynomial-k enumeration/trial division, have
one absolute prime-gap cutoff, and are protected by actual size and
coprimality tests with exact fallback.

The balanced CRT tree has O(log k) levels. At each level its controls
occupy at most k/2+O(log k) bits, leaving the fixed free fraction.
Each table has polynomial-k size. No m-dependent short-axis size,
prime gap, or CRT depth is introduced by replacing the two suppliers.

The occupied-neighbor Fourier construction has its fixed 64-reflection
amplification and fixed blocks of four to seven axes. Its phase
denominators stay bounded away from zero. Schedules and tables remain
polynomial k. The O(log k) global layers are exactly a controlled
permutation, a phase stream or a selected-bit Walsh transform on
O(k/log k) bits. The new W supplier has precisely this interface.

Phase products use the source prefix streaming: fewer than 2N total
products with O(k)-bit operands. The fixed O(k log k) short multiplier
is retained. This costs O(Nk log k), uses two reused coefficient
tapes, and never multiplies by the number of block combinations.

## 3. Precision is charged at the right boundary

The source invokes a complete Walsh layer with input allowance
2^(13k) and absolute error 2^(-50k). Its internal variable-template
gain is handled by W's O(k) format and explicit precision guard.
At a completed layer boundary the exact transform is unitary.
It would double-count amplification to reinsert its internal gains
at every outer layer.

Phases prepared to error 2^(-70k), and equally fine rounded products,
have operator error bounded by the largest coefficient error. The
source Euclidean induction over O(log k) layers gives transform error
2^(-40k). The coordinatewise-product inequality gives error 2^(-30k)
on a vector within the source norm bound. The adjoint transform and
sqrt(S) scaling leave every convolution coefficient within less than
one half. Nearest-integer recovery and the O(k)-bit carry scan
therefore return the full exact 2v-bit product.

The internal selected-bit recursion must not repeat a full k-position
gather at every child. The source gives each child one already
contiguous active slot and leaves other ranges as spectators.
Route B's recurrence now states this explicitly: gather and undo
are charged once at the layer root; local column changes have
active width at most a. This is necessary for its local a-dependent
recurrence and is compatible with the source physical layout.

## 4. Preparation and the resulting digit profile

I accept A's preparation correction. A root interchanger at U=Theta(k)
may generate an archive of size \(2^{k^\eta}\), eta<1 fixed.
It is not generally \(2^{k^{o(1)}}\). The combined conservative
\(2^{k^{\eta'}}\), eta<eta'<1, bound absorbs polynomially many
invocations, while Walsh-only preparation has the smaller form.
Both are \(2^{o(k)}\), hence negligible against Nk.

The source layer list consequently yields time
\(Nk\sqrt{k+1}E_C(k)(1+\log k)^C\) and visited cells \(NkE_C(k)\),
plus absorbed preparation. All numerical, phase, sorting, descriptor
and constructor regions start at marked positions and are reused.
Increasing C absorbs the fixed logarithmic powers. With Nk=Theta(v),
this gives the required digit time and space profile V18.

The linear-space positional wrapper is separately proved in the
Route B transfer: its subpower chunk factor multiplies the same
Phi overhead, and capped preparation/execution with exact fallback
makes a total fixed machine. This outer audit has no remaining
proportional exponential-in-m term.

## Limits

This is a written source audit of the outer transfer. The common-field,
composite-radix, sharp-space and variable-arity recurrence suppliers
require their own reviews. No complete tape machine, full multiplier
or asymptotic running time was experimentally executed.

Credits: @CubeJerry; the pinned source; Route A's source-substitution
proof; E002 component authors; substantial ChatGPT multi-agent assistance.
