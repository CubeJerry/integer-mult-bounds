# Independent review of the conditional rectangle-volume transfer

Reviewer: E002 conditional review C. Gate: **PASS for the complete conditional implication at the amended snapshot below**. The physical hypotheses RV-I and RV-W remain open. This review does not promote the admitted unconditional Theorem V or claim a physical implementation of either hypothesis.

Reviewed complete lead artifact `rectangle-volume-conditional-transfer.md`, SHA-256:

`d97f69a4b002f42dd2d0c5716975066ebcde8251220697361ce0d32ef5dadd15`.

The initial snapshot was `4fa76bd6072958dbb32402b194568500d963797a5d391adbd8c78fc14e65c79a`. I requested that retained payload space be strengthened to an actual visited-region invoice, and that the main/reserve/finite-repair child-volume bounds used in the proof be stated explicitly. The amended snapshot does both. My acceptance applies to its complete text.

## 1. Inputs inspected and conditional scope

I read the complete conditional theorem, the complete E002 admitted `variable-profile-theorem.md`, `variable-interchanger-space.md`, `variable-arity-outer-transfer.md`, `rectangle-volume-invoice-target.md`, and `fourier-free-rectangle-counts.md`. I also read the pinned Fourier `kernel.tex` in full, including its charged/free decomposition, its common-coordinate endpoint transforms, its row-normalized call invoice, and its word-cost uniformity paragraph. The latter is not used as a free tape primitive. The tape costs are supplied by the completed E002 interchanger and routing wrappers.

The conditional statement retains the previously reviewed finite predictors, repair, compatible radix, field representation, numerical precision and exact assembly. It changes two local physical delivery contracts. Such contracts are meaningful finite-parameter hypotheses: they specify full occupied data, recursive call volume, ordinary work, workspace, construction and layouts, rather than assuming the desired multiplier bound directly. They are nevertheless strong and currently unproved. Counting rectangle outputs cannot verify them.

## 2. Exact-label count and optimized envelope

Write `B=binom(2d-1,d)`, `h=2d-1`, and `n0=q^h`. The independently supplied inner count is

`R_in=B 2^(d-1) [q(q-1)]^d`.

There are B choices of the d affected outer positions, n0 choices in every unaffected position, and one inner rectangle in every affected position. Thus

`R=B n0^(h-d) R_in^d`.

Dividing by `N=n0^h` gives exactly RV4: the remaining power of q is `q^d (1-1/q)^(d^2)`. In particular the canonical incidence factor `t^(d(d-1))` does not appear in this output count.

For the retained sufficient rank guard, minimal integer t obeys `t<3+z/d^2`, where z=log2 m. Since `log2 B<=2d-1`,

`log2(1+R/N)=O(d^2+dt)` and `log2 D=O(dt+log d)`.

The same bounds hold with any fixed power D^K. A power-of-two d within a constant factor of z^(1/3) therefore gives `O(z^(2/3))`. Its alphabet and label counts are still polynomial m: `log2 N=t(2d-1)^2<=4z+O(d^2)` and d^2=o(z). No enormous dictionary beyond the stated fixed-degree construction allowance is introduced by changing the optimum.

The normalized finite predictor and repair supplier contributes O(sqrt m), including the constant padding and reserve terms. The implication RV1 to RV6 is consequently correct. The rank factor `1+mr*/N` is bounded by two. Both the free and low-rank parts must actually satisfy RV1; the text expressly requires this.

## 3. Numerical-label count and its distinct optimization

For ell=2 and even L, the source polynomial vanishes at every positive even distance and is nonzero at every odd distance. Fixing an unequal set of k positions gives `binom(L,k) q^(L-k)[2(q-1)]^k` canonical rectangles. Summing over odd k gives RV7. The bound `R_f/N<=3^L` follows directly, without replacing incidence by output count in the existing implementation.

The match-subset expansion contains at most `sum_(j<=L/2) binom(L,j)q^j` charged rectangles, proving RV8 even if some coefficients vanish. In characteristic two the direction Gram matrix is the all-ones matrix plus a sum of L equality matrices for even L, so `D_F<=1+Lq` is valid.

The least dyadic q with `q^(L/2)>=2^L m` has `4m^(2/L)<=q<8m^(2/L)`. It makes the normalized charged term at most one. RV9 then has logarithmic size `O(z/L+L+log L)`. Taking even L of order sqrt z gives O(sqrt z), and still `q^L<=m^2 2^(O(L))`. Predictor, batch and finite-repair factors remain polynomial m under the retained suppliers. This proves the conditional call envelope RV10.

This second improvement is essential. An improved exact interchanger alone leaves the original numerical kernel loss of order `sqrt(log m log log m)` and does not close the log-free two-thirds recurrence displayed here.

## 4. Physical time and visited-space interfaces

The amended RV2 bounds the union of visited bit cells in reused marked contiguous regions, including endpoint, query-accumulator and temporary arrays. This closes the distinction between retaining little data and having traversed a much larger tape region. The added main-child bound `16V0/N`, reserve inflation at most eight, and local finite-repair contraction at most 1/16 are sufficient for the existing exact space proof. Address widths alone would not have implied these volume statements.

The fixed exponent gamma can be chosen after the common polynomial degree K. Then `m=Theta(u^gamma)` makes every local polynomial-m ordinary toll subcritical relative to sqrt u. The unchanged root degree s contributes only powers of log U. Child logarithmic widths decrease geometrically, and the sum of their two-thirds powers is bounded by a fixed multiple of the root two-thirds power. The exact recurrence therefore proves RV12, including direct bases and the one-time field representation.

For visited space, main and finite-repair descendants contract, reserve descents clear the main arrays, and their bounded inflation over O(log log U) levels is only a fixed power of log U. RV2 supplies the improved local envelope that this argument needs. Global cache scans remain at external invocation boundaries; small spatial children keep their local compact chain. No global polynomial-root lookup is silently charged per tiny child.

For RV-W, an m^K count of ordinary arrays and address calls is acceptable because the numerical schedule is slower: `log m=Theta(y^(2/3))`. The amended ordinary workspace invoice is in visited cells. Its local tape bound is obtained by actually invoking the completed exact interchanger, not by treating a monomial map as a unit-cost word operation. Every child retains the source occupied layout and exact batch fraction, as required explicitly by the hypothesis.

## 5. Numerical recurrence, accuracy and final assembly

The numerical choice gives a logarithmic step at least `c y^(2/3)`. The polynomial-m ordinary work and the RV12 interchanger envelope form a local term `2^(C2 y^(2/3))`, up to one common polylog(k) factor. RV10 divided by the square-root child-width ratio contributes `2^(C3 y^(1/3))`. For y large, the interval is within [y/2,y], and

`y^(2/3)-(y-c y^(2/3))^(2/3)>=c' y^(1/3)`.

Choosing the induction constant strictly larger than both requirements makes the two normalized terms sum to less than one. Integer rounding and the finite base are correctly handled. This proves RV13's majorant, rather than only balancing its exponents heuristically.

The product of polynomial-m branch factors is polynomial k because the sum of the logarithmic arities is O(log k). Fixed-degree operation/height bounds therefore give logarithmic path gain at most `log(k+2) 2^(C(log(k+2))^(2/3))=k^o(1)`. The existing computed event/gain guard supplies absolute O(k) precision. This is a justified transfer from the completed numerical supplier; no extra favorable precision assumption is required. Exact batch divisibility, direct remainders and direct failed-guard branches remain present.

The outer wrapper uses only monotonicity, fixed rescaling and absorption of fixed powers of log k by the interchanger/Walsh envelope. The log-free envelope has all of those properties. Its guarded routing, occupied short Fourier transform and exact rounding/carry composition therefore remain applicable in the same proof order. The short multiplier is retained, so there is no circular use of the proposed near-root bound.

The integer-selected chunk count has `log r=O(x^(2/3))=o(x)`. It absorbs the digit workspace into the fixed marked O(n) regions; `r^2 ceil(n/r)<=2rn` gives the claimed time. Combined preparation `2^(L(n)^eta')`, eta'<1, is n^o(1), eventually fits the actual preflight cap, and is not mislabeled as `2^(k^o(1))`. The quadratic clock, stop-before-crossing rule, scratch cleanup and schoolbook fallback ensure correctness and the visited-cell bound at every length. Eventual success then yields one absolute big-O constant after covering the finite remaining range.

## 6. Decision

I accept the complete amended implication:

`RV-I and RV-W => T(n)=O(n sqrt(1+log2 n) 2^(C (log2(1+log2 n))^(2/3)))`, with O(n) cells ever visited, on one fixed exact deterministic finite-alphabet multitape machine.

The hypotheses are still open. Neither the rectangle counts, this review, nor the finite geometry checkers provide those processors. This is not an unconditional improvement beyond Theorem V, a polynomial-x overhead, the square-root endpoint, a runtime lower bound, a formal refinement, a full-machine execution or a claim of literature priority.

Credits: @CubeJerry; the pinned OpenAI source and prior programme; E002's exact-count and physical suppliers; the lead conditional proof and its explicit interface corrections; substantial ChatGPT multi-agent assistance.
