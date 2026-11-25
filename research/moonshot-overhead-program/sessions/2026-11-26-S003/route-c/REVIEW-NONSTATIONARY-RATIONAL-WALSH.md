# Independent review of varying-arity numerical Walsh execution

Decision: **accepted as the conditional numerical theorem NW1–NW17**, with I-var supplied separately by B's AI theorem. C's independent AI review is `REVIEW-ADAPTIVE-INTERCHANGE.md`. This review does not itself replace the complete integer caller and its final exact-recovery proof.

I read `route-a/nonstationary-rational-walsh.md` and its checker completely, including the later optional Gram padding. I also checked the relevant actual source `kernel.tex`, `binary.tex`, `permutations.tex` and `integers.tex` passages during the present global review. The earlier compact rational theorem establishes local coefficient arithmetic; it does not alone establish the changing-arity or absolute-payload claims reviewed here.

## Local physical and algebraic interface

The numerical pencil can process one rectangle at a time. A free rectangle retains its transformed source subset across all queries and accumulates its destination subset before the shared final transform. Each subset is at most one whole volume. Charged rectangles keep only their current common sum and destination work. Immutable input, output, Newton work and one current rectangle therefore require an absolute number of payload arrays. Polynomially many scans are paid ordinary work and do not repeat the shared child transforms. The finite repair stack shrinks by one eighth.

The optional padded dimension D_F=1+L_Fq_F is valid. The actual source uses any nondegenerate symmetric pairing and vectors with the specified Gram entries. Adjoining a nondegenerate orthogonal summand preserves all those pairings and places the new directions in every d_v-perpendicular space. The endpoint proof uses a basis and its dual in the full nondegenerate pairing, even when the restricted form is degenerate. It therefore remains valid in the padded space. The call count and arity use the padded D_F explicitly.

All source selector functions are explicit binary column parities and bilinear phases. Their address work is polynomial(m)k per numerical record and is paid by its Theta(k)-bit encoded width. The rational coefficient compiler has polynomial-m heights and avoids every exponential spectral table. Bounded-divisor preparation costs O(B²+pB) for B=poly(m), followed by the separately charged O(k log k) short-record product. Source normalization cancels f-dependent factors outside the recursive calls. No variable-width rational divisor is hidden in a nominal linear record operation.

The source packed-XOR proof accepts any complete field-swap primitive. Replacing its cost by I-var preserves its exactness and space argument. Since the eventual m is at most k, all control, offset, rank and description computations have a fixed polynomial degree in k. One absolute guard coefficient can therefore pay their exceptional-record work. The local physical cost retains the entire polynomial(m) times J(a) address toll in NW7. This is essential: the arithmetic-only predecessor's faster rate does not transfer without that term.

## Exact batching with changing arities

The integer choices x=ceil(log₂(a+2)), y=ceil((x²ceil(log₂(x+2)))^(1/3)), m=2^y-1 are constructive, with y=Theta(F(x))=o(x). The child is the largest even f<=a/A_m; the even remainder has fewer than2A_m bits and is charged as direct butterflies. A bounded initial active-width range uses a fixed direct routine.

At every completed numerical spatial descent, a_(i+1)=f_i<=a_i/A_i. Hence

    sum_i log₂m_i <= sum_i log₂A_i <=log₂a_0.

The last inequality follows by telescoping the actual widths; no assumption about a continuous ideal recurrence is needed. Since W_i<=m_i^K and every W_i is a power of two, their entire path product is at most a_0^K. The root leading spectator range is2^(k-s), with k-s>=k/2 eventually. It is therefore divisible by that product. Repeated divisibility is established for the full path, not inferred from divisibility by each W_i separately.

All spatial children at a depth have the same active width and arity. The finite contraction factors also have a product polynomial in k, either already contained in the completed W_i or bounded by an additional fixed power. Every active numerical array retains at least2^(k/2)/poly(k) records. Thus the smallest numerical child still pays all fixed-degree setup and control workspace. No per-depth spectator padding accumulates.

## The actual recurrence and precision

After dividing by sqrt(a), the local physical term is at most2^{(C_I+2K+O(1))F(x)} times the fixed log k factor. The child multiplier is at most2^{C_B sqrt(y log(y+2))}. The genuine decrement x-x_f is at least y/2 above a fixed base. On this interval,

    F(x)-F(x-y/2) >= c sqrt(y log(y+2))

with an absolute c. The stated1/32 has considerable slack: F'(t) contains the positive term(2/3)t^(-1/3)log₂(t+2)^(1/3), and F is concave. Choosing one sufficiently large exponent constant therefore leaves a strict margin for both the local toll and the recursive term. Floor/ceiling differences change F by a bounded amount. The induction proves NW16; the two global position permutations and fixed log powers fit the final envelope.

The product of the polynomial branching counts along a path is polynomial in k because the sum of log m_i is O(log k). Finite repair does not change that conclusion. Rebuilding every compact template at every node still has only polynomial(k) total setup. This reasoning counts actual polynomially many row roles and calls; it does not treat a normalized call-volume quotient as a branching bound.

The one-node logarithmic norm gain and coefficient height are at most m_i^K. Their sum along a path is bounded by

    (1+log k)2^{O(F(log(k+2)))}=k^{o(1)}.

It is eventually a fixed fraction of k. Completed child transforms are unitary and completed exact permutations preserve norm. The source path-to-common-ancestor argument therefore controls fault propagation with the same sublinear logarithmic gain. The polynomial number of arithmetic stages, coefficient perturbations and sqrt(N) array-rounding factors fit an absolute p=C0k error ledger. Ideal and represented intermediate norms remain within2^{O(k)}, and all exact temporary numerical products have O(k) bits. This justifies a single numerical format for the entire changing-arity execution.

At numerical recursive descents, payload volume contracts by at least one half; finite repair contracts by one eighth. I-var has an absolute linear-space coefficient. An absolute number of parked arrays per frame therefore sums geometrically. Additive polynomial(k) control storage is negligible against the guaranteed smallest child volume and is reused. This proves an absolute bound on all cells ever visited, not only a polynomial-m bound for a fixed candidate.

## Replay and limitations

I ran an isolated copy with `python3 -I -B`, copying the inherited compact-rational receipt only as a declared hashed reference. The new replay passed six exact integer/batch paths with logarithmic root widths512 through16,384,169 log-domain grid points at100 decimal digits,117 norm-absorption checks and all3 countermodel controls. Source SHA256:

    2c5bd2e268c2fedee118004564d817a187194e59b9279e6f28efa438cb0177b7

Receipts are under `route-c/replays/nonstationary-walsh/`. The decimal tests are finite recurrence evidence with explicitly illustrative constants, not interval-certified asymptotics or the compiler's universal constants. The exact paths do not enumerate the enormous label geometry. No old rational replay is recounted as new evidence. The written proof supplies the calculus, physical scheduling and precision conclusions; no complete multiplier run, Lean proof or human referee certification is claimed.

Prepared for Jerry Chen (@CubeJerry), with substantial ChatGPT assistance and the source/predecessor attribution retained in NW.
