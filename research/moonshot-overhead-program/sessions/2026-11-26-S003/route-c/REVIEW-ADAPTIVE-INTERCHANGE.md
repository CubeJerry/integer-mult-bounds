# Independent review of the varying-arity exact interchanger

Decision: **accepted as the written exact physical component AI1–AI11** in `route-b/adaptive-interchange.md`. This acceptance supplies the stated I-var premise for a separate numerical theorem. It does not by itself assert a new integer-multiplication bound.

I read AI in full and its complete checker, together with FP, UP and the optional streamed-key lemma. The earlier C reviews accepted the compact factor, endpoint, packed-batch and fixed-profile composition. The present review separately checks the uniform payload and changing-parameter deductions; the fixed-profile theorem alone would not establish them.

## Uniform payload and field changes

The two-pass UP schedule is algebraically valid. The entire query-by-rank gather array has volume(mr/N)V<=V. Rectangle source subsets and destination accumulators each have volume at most V. The first pass completes all negative deliveries and all rank gathers, the middle applies the scalar rank inverse and query matrices, and the second completes positive deliveries. The extra destination inverse preparation is an absolute factor in the invoice, covered by Cg=2^22. No endpoint is prepared separately for each query. Immutable source data are retained, so singular scalar slices do not require inversion to recover a gather input.

The one-role spectral implementation is sufficient without relying on the optional SK scanner. A raw repair parent has32B coarse roles, B>=2m+1. A current role's2m comparison bits per scalar inflate that one role by at most1+m, since the scalar already has at least two bits. Its tags therefore fit within a single parent volume. Repeated input/output check-row scans retain raw input and output accumulators; all such arithmetic is pointwise scalar work. Crucially, each complete forward converter finishes before these scans, and the complete inverse converter starts after them. No converter is repeated for each coarse pair. Tags are discarded before any recursive converter call, preserving the exact1/16 phase volumes.

FP uses a bijection from h independent binary rows to one extension-field row, rather than embedding one bit and adding h-1 zero coordinates. Its correctness follows from the completed whole-row identity I tensor Q over F2. The partial field operations need not act componentwise. Moving the power-of-two coordinate index across the complete physical suffix is a sequence of single-bit stream moves, using O(V) payload space. The exponential module remains a prefix and is not transposed bit by bit.

When a child chooses a different field, it receives the parent's encoded bits with the old coordinate index as an unchanged suffix spectator. Its completed binary permutation returns exactly the parent's representation. This proves composition across changing fields without a multiplicative field-degree loss in child volume. Only the explicitly paid leading-row padding remains, always below two.

## Exact varying parameters and the recurrence

The integer version u0=ceil(log₂m), v=ceil(log₂(u0+2)), and the largest power of two with d³v<=u0 has the asserted asymptotic scale. Rounding changes fixed constants only. At sufficiently large fixed m, the label estimates give N<=m^5, a<=m^(1/4), rank occupancy at most one and

    log₂[Dg(1+lambda)]=O((log m)^(2/3)(log log m)^(1/3)).

Actual generation is polynomial in m because all label, rectangle, rank and operation-list dimensions are polynomial. The full-rate module is executed by B1 and described by its polynomial-length grades. Its entire matrix is not generated. The leading-batch descriptor stores log W, not W instruction entries.

Choose the fixed root degree R only after fixing the absolute polynomial exponent K. Then m(e)<=e^delta and delta K<=1/8 pay all polynomial local scans. The leading-width and reserve budgets leave a genuine child

    f=floor((e-ell)/(m+2a)),

with f<=e/m and logarithmic width contracting by a fixed factor. The lower width bound confirms that this is the intended regular descent; the time upper bound only needs the upper contraction. The local descriptor cost can be absorbed into m^K V with an absolute constant, since its degree in log V is absolute.

Normalizing by sqrt(e) gives a local term at most c e^(-3/8) and multiplier at most2^{C phi(log m)}. The logarithmic widths contract geometrically, and

    phi(ry)<=r^(2/3)phi(y),  0<=r<=1.

Thus all logarithmic multipliers sum to O(phi(log e_root)). The local negative-power terms are summable along the actual width chain, read backwards. This pays both recursive branches and local polynomial work. It is a proof for the executed varying-parameter recursion, not an insertion of m(e) into an O_m estimate.

## All cells visited

At each node only an absolute number of payload arrays is retained. Main spatial children have at most half the parent volume after padding; finite repair has the stronger1/16 contraction. At a full-volume reserve descent, the parent clears the main arrays and transfers ownership of its current data region. It does not park a second full parent copy. Consequently intervening reserve chains do not break the geometric payload sum.

Descriptors and field/parameter scratch are additive polynomials in m and log V. Since V>=3^(2e) and m<=e^delta, every parked descriptor has size polynomial(log V_root), with absolute degree. The depth and finite repair depth are also polynomially bounded in log V_root. Their total fits C V_root for an absolute C. Reusing marked regions across siblings and phases bounds the union of visited cells, rather than only live allocations.

The binary-to-ternary conversion increases volume by less than nine and restores it exactly. The finite algebraic identity remains correct for every chosen parameter; induction on the decreasing width gives exactness with arbitrary occupied spectators. These facts establish AI1 with one fixed alphabet, tape count and absolute payload coefficient.

## Replay and scope

An isolated copy under `python3 -I -B` passed96 integer-root boundary checks,3,597 width/normalized-mass/local-toll invoices,36 complete recurrence calculations and32 leading batches, reaching228 levels. Every omitted-budget and omitted-toll negative control was rejected. Source SHA256:

    e0b89f773f5b8f18bd3b42325ff9549ec07dce1fd17b77ac39e3712b834914a3

Receipts and the copied checker are under `route-c/replays/adaptive-interchange/`. These are exact tests of the declared toy profile; they do not instantiate the optimized asymptotic geometry or execute a full tape machine. The analytic argument and the separately reviewed finite identities carry those mathematical obligations. No Lean build or independent human referee certification is claimed.

Prepared for Jerry Chen (@CubeJerry), with substantial ChatGPT assistance and the source/predecessor credits retained in AI.
