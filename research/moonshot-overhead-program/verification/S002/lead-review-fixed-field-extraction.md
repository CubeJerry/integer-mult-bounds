# Lead gate: fixed-field count formulas and complete extraction

Session S002, November 25, 2026. **Accepted as a written, unconditional
mathematical algorithm/profile construction**, after separate finite and
whole-input reviews by Routes B, C and the lead. This acceptance is an
AI-assisted research audit. It is not human refereeing, a proof-assistant
check or execution of the complete tape machine.

The accepted conclusion, for sufficiently large n, is

    T(n)=O(n sqrt(L(n))
             2^{O(s(n)(log2 log2 s(n)/log2 s(n))^(1/3))}),
    L(n)=1+log2 n, s(n)=log2 L(n), visited cells=O(n).

The machine is one fixed deterministic finite-alphabet multitape machine,
computes the full exact product, and has a correct fallback at every
remaining length. Absolute constants and the eventual cutoff are not
numerically evaluated. The endpoint H=O(1) remains open.

## 1. What was read and accepted

The lead read A's complete `characteristic-two-count-formula.md` B1--B11
and `fixed-field-extraction-theorem.md` Q1--Q13. Both B's independent
count-formula review and physical-composition review were read in full;
so were C's independent derivation, finite review and final global review.
The lead independently replayed all three new checkers from copied files.

The physical gate also includes fresh reads of B's complete
`pairwise-newton-division.md`, `polynomial-auxiliary-cost-audit.md`,
`order-three-template-profile.md`, the accepted physical compiler ledger,
and the physical recursion/precision paragraphs of the pinned source
tape `walsh.tex`. The earlier gates already cover the characteristic-two
label geometry, order-three group word, full-rate cyclic factorization,
common cyclotomic generator, source varying-pencil interface, physical
movement, common-space wrapper and restart schedule.

Source pin: `openai/math@3344da59991ed94f9ba711217b29c1d760badfa6`.
This statement does not claim that every manuscript or every cited
predecessor has been read. The broader read-scope ledger is unchanged.

## 2. The new finite representation

For ordinary Boolean bits in characteristic two, the carry recurrence

    c_(i+1)=x_i y_i+(x_i+y_i)c_i

contains the preceding carry once. The children x_i,y_i are each copied
twice; those copies are charged. A balanced digit-sum tree consequently
has fully unfolded bit-formula size

    S_(r,k)<=8^r binom(r+k,k)<=2^(4r+k).

With r and k both O(log m), this is polynomial in m. The proof uses the
cumulative-sum recurrence, rather than a circuit reuse convention. The
bit-k syntactic degree is at most 2^k. The ternary high bit is an affine
query indicator of degree one, safely below its assigned budget two.
Each affine indicator has a constant-size expression in 1,C_j,C_j^2;
expanding its atomic leaf changes only the stated loose absolute bound.

Adding the constant residue of -u uses one further adder. For negative
as well as positive a, `(1+T)^a mod T^(2^t)` depends only on a modulo
2^t: `1+T` is a unit in the formal series ring and
`(1+T)^(2^t)=1 mod T^(2^t)`. Selected residue bits therefore compute
`binom(a,h) mod 2` for h<2^t. Their product has syntactic degree at most
h. Including the phase `omega^(u-sum beta)` gives exactly the required
predictor at every actual order-three spectral tuple.

The degree-O(sqrt m) formula is generally nonmultilinear as a formal
polynomial. Its Boolean spectral identity and its formal degree budget
are separate, valid statements. The cyclic compiler is applied to the
actual formal formula; simultaneous diagonalizability then justifies
its source operator values. No characteristic-zero polynomial identity
or factorial division is specialized to characteristic two.

The formula compiler supplies the whole scalar identity on every row,
using D affine factors and width at most D^S. All 3^m shifts receive the
same architecture and equal multiplicity. With the stated constant-tail
window, the known containing exception set has at most R/32 rows.
This meets IP4 with no designated output or uncounted zero workspace.

The common algebra `F4[Z]/Phi_(M0*tau)` includes every required odd-part
root, with tau a sufficiently large power of three. The field element
omega is supplied by F4 independently of Z. Check-node differences have
the explicit unit product three, equal to one in characteristic two.
All algebra elements are coordinate vectors. The integer cyclotomic
constructor, matrices, all frequency tables and their validation are
bounded by `2^(m^C)` in actual work and retained space. The directly
tested D<=m guard and total generic small-m branch prevent an initial
unbounded search.

## 3. Physical and numerical bridge

Both order-three query powers reduce to one shared swap pencil with
different pointwise comparison masks. The masks remain in the original
physical address order, and their scans are charged. The two-predictor
repair has four sequential child phases of relative volume 1/16. Its
final three-transform swap word gives

    sigma_Q/W <=8 D_pred R_pencil+3m 4^(-a).

The complete constants are safe: 8*12*64=6144 before the leaf remainder;
8192 covers that remainder; leading padding and occupied reserves fit
32768. The completed swap has F2 coefficients. Expanding the common
algebra basis multiplies the arbitrary independent inputs and calls
equally. Intermediate F4 transforms need not be componentwise over F2.

The numerical Walsh program uses the separate rational Newton/division
template. Its parked accumulator is space and ordinary work, while only
the active rows receive each pencil. Two V/8 conversion phases yield
the exact main coefficient 280/3 and a leaf coefficient at most four,
safely below the stated 128. Source endpoint sharing is retained.

Every rational coefficient a/b is prepared as a dyadic approximation
once at the selected O(k) precision by ordinary integer division. This
is charged setup. Record multiplication continues to use the fixed
O(k log k) short multiplier. Coefficient perturbations are bounded by
their errors times the finite row/array norm and included in the source
rounding argument. The local logarithmic norm bound is polynomial in
P; propagation, operation counts and setup fit the same k>=P^K cutoff.
Thus the rational coefficients add no profile exponential or per-record
division cost. They are never reduced into the characteristic-two ring.

Rational address dimensions, numeric magnitudes, compatibility lists and
the actual radix are included after the completed row width is known.
The same algebra is used throughout a fixed candidate's recursion.
Finite scalar work, masks, instruction interpretation, movements and
sorting all remain in the compiler's polynomial-P invoice. Depth-first
parked volumes are geometric; reserve descents clear payloads first.
The common cap bounds physical cells ever visited, including failed
attempts and cleanup, not merely live array entries.

## 4. Quantitative profile and eligibility

The least dyadic distance d>=100J satisfies d<200J. The label estimate
has excess at most `3x/d+10d^2 log2(4x)+15`, x=log2 m.
At `x0=2^40 J^3 log2 J`, all complete interchange and Fourier call
margins, including the quarter pre-padding Walsh margin, hold.
All finite trials terminate, so the first accepted trial has
`log2 m_j=O(J^3 log2 J)` in actual construction cost as well.

The combined actual data envelope is `P_m<=2^(m^C)`. Substitution into
the accepted compiler and common-cap schedule gives

    log2 D_j, log2 L(N_j)<=2^(C J^3 log2 J).

This includes generation time, additive retained workspace, chunk
products, movement, carries, restart weights and the fixed absolute
prime-shape cutoff. Put s=log2 L(n), z=log2 s and choose the largest
dyadic J below `[z/(2C log2 z)]^(1/3)`. The profile is then at most
sqrt(s), which proves actual eligibility n>=N_j. The remaining s/J
term gives the announced overhead. The scheduled machine receives no
parameter advice from this asymptotic choice.

## 5. Independently replayed checks

Copies and outputs are under `count-formula-lead-replays/`:

| Independent checker | Lead replay result |
|---|---|
| B carry/formula | 5,460 additions; 137,214 shifted Lucas coefficients; 120 serialized formula evaluations; 525 size/degree recurrences; 45,864 F4 predictions; both negative controls rejected |
| C count-bit formula | 13,996 bit assignments, including 4,786 negative offsets; 260 copied size/degree budgets; 178,330 binomial residues; 18 indicators; 9,702 predictors; 3,259 central matches; three negative controls rejected |
| A quantitative growth | 4,121 complete margins/guards and 4,121 threshold negatives; 290 exact label majorants; 546 sparse rounding cases; integer/rational arithmetic only |

The earlier exact cyclic, cyclotomic, label, repair, group-word, scheduler
and chunking replays remain dependencies. These finite checks corroborate
the specified identities and accounting; the unbounded construction and
asymptotic claim rest on the written proofs. No astronomical template or
complete multiplier was run.

## 6. Scope and credits

IP4 is established by the explicit characteristic-two count formulas.
The stronger all-odd-characteristic dyadic representation hypothesis IP
and the concurrent E001 bounded-preflight hypotheses remain open. No
poly(s), `2^(O(s^beta))` for fixed beta<1, or constant-overhead endpoint
has been established. The comparison is between this programme's
explicit upper envelopes, not a lower bound on runtime or a priority
claim against an unspecified published o(1).

Credits remain with the source authors and their cited predecessors,
the established graded tensor construction, the recovered finite repair
provenance, Jerry Chen (@CubeJerry), and the AI-assisted derivation and
independent reviews in this session. No upstream PR has been opened.
