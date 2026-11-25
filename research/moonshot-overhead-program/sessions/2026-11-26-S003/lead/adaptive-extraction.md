# Adaptive physical extraction at the two-thirds scale

Status: **complete written construction accepted after independent global C review, independent A source-caller audit, and lead review**. The exact physical supplier AI and numerical supplier NW have separate C reviews. This file closes their actual integer caller; the admission record is `ADMISSION-AQ.md`. It supersedes the conditional transfer draft, not the archived PP proof.

## AQ1. Statement and scope

Put L(n)=1+log₂n, s(n)=log₂L(n), and

    F(x)=(x² log₂(x+2))^(1/3), x>=0.

There is one fixed deterministic finite-alphabet multitape Turing machine, with a fixed number of tapes and heads, that multiplies two n-bit integers, writes their exact full product in the prescribed contiguous binary format, and satisfies

\[
 T(n)=O\!\left(n\sqrt{L(n)}\,2^{O(F(s(n)))}\right),
 \qquad \text{all cells ever visited}=O(n).                 \tag{AQ1}
\]

All constants in this statement are absolute. Head movement, generation of parameters and compact templates, coefficients, control, padding, clearing and output recovery are charged. The upper bound has no complexity-theoretic hypothesis. The proof uses the pinned OpenAI source theorems and the new written finite/physical constructions below, rather than a new oracle or representation hypothesis. This is not a claim of a full machine implementation, formal-kernel validation, independent human refereeing, or literature priority.

## AQ2. Exact dependencies and provenance

The manuscript pin is OpenAI `math` commit `3344da59991ed94f9ba711217b29c1d760badfa6`. Paths below are inside `preprints/`:

| Dependency | Exact obligation used here |
|---|---|
| Tape paper `The-logarithmic-exponent-of-integer-multiplication-on-tapes-November-24-2026/build/interchange.tex` | Independent-input scalar identity, shared endpoint order, bounded-rank correction, finite prediction/repair, geometric field-swap recursion. |
| Same paper `walsh.tex` and `permutations.tex` | Partial numerical Walsh interface, guarded packed XOR, full binary-position and controlled-block permutations with occupied spectators restored. |
| Same paper `integers.tex` | Actual integer shapes, synchronized short transforms, phases, CRT, coordinate products, norm/error bounds, exact convolution rounding and carry recovery. |
| Fourier paper `build/kernel.tex`, `binary.tex`, `repair.tex` | Normalized finite pencil and rational coefficient algebra used in CW/NW. Exact directory and audit references are retained in the cited supplier files. |
| [B adaptive interchange AI](../route-b/adaptive-interchange.md) | One uniform exact field-swap machine with an absolute linear visited-cell coefficient and the quantitative cost below. |
| [A nonstationary Walsh NW](../route-a/nonstationary-rational-walsh.md) | One numerical processor using AI, with a single absolute O(k)-bit numerical format and the quantitative cost below. |
| [C AI review](../route-c/REVIEW-ADAPTIVE-INTERCHANGE.md), [C NW review](../route-c/REVIEW-NONSTATIONARY-RATIONAL-WALSH.md) | Independent written audits of the new suppliers, including full-rate packing, uniform payload, actual recurrences and precision. |
| [A caller audit](../route-a/audit-adaptive-integer-caller.md), [C global review](../route-c/REVIEW-ADAPTIVE-EXTRACTION.md) | Independent checks of the exact outer source substitution and the complete AQ construction. |

AI depends on B's compact factor and explicit dyadic geometry, C's compact spectral repair, A's two-pass uniform-payload pencil, B's full-rate field packing, and the lead's packed-batch construction. NW depends on the earlier S002 binary-label construction, A's compact rational Walsh arithmetic, its constant-array schedule, and AI. Their finite identities remain the pinned source identities; the changes concern constructive representation, scheduling and quantitative choice of parameters.

## AQ3. The two uniform physical interfaces

For u-bit address fields and complete arbitrary prefix, gap and suffix ranges, AI implements their exact interchange on V encoded bits in

    C V J(u),   J(u)=sqrt(1+u) 2^(C F(log₂(u+2))),             (AQ2)

and at most C V visited cells. Here and below enlarging the same letter C denotes an absolute constant, not a parameter-dependent constant. Every input payload is independent. No zero-filled field embedding loses occupancy: h binary rows are bijectively packed into one field row. A child may change its finite field and still returns the parent's original bits in the completed permutation. Binary-to-ternary padding occurs once per complete invocation, by less than nine; native recursive children retain the native radix. Leading batching costs less than two and is included in AI's mass recurrence.

For N=2^k numerical records and a permitted selected set of a<=c k/log(k+2) address bits, NW performs the normalized partial Walsh transform and its adjoint with

    C Nk sqrt(1+k) 2^(C F(log₂(k+2)))                        (AQ3)

steps and C Nk visited cells. For any fixed boundary norm exponent and requested fixed error exponent, one absolute multiple of k integer/fraction bits suffices. The constants can depend on those fixed requested exponents, which the source caller fixes once; they do not depend on k or the changing arities. Exact permutations do not add numerical error. The two outer position permutations are included in AQ3.

The internal, pre-position-permutation bound is stronger: for active width a it is

    C Nk sqrt(1+a) 2^(C F(log₂(a+2))) (1+log(k+2)),

plus polynomial(k) construction. This precise form explains why the outer caller can change selected bit sets without losing the target scale.

## AQ4. Why the arities differ in the two suppliers

AI chooses, at native width e, the largest odd m not exceeding the integer R-th root of e. R is one fixed integer chosen after the absolute degree K of its compact compiler, with K/R<=1/8. Its optimized dyadic label geometry has

    log₂[D_g(1+lambda)]=O(F(log₂m)),
    N_label<=m^5,  a_reserve<=m^(1/4),  m r/N_label<=1.

Its literal completed call-volume coefficient is at most sqrt(m) times 2^(C F(log₂m)). The actual next width is

    f=floor((e-ell)/(m+2a_reserve)),

where ell includes the full-rate field-coordinate and module-prefix batches. For sufficiently large fixed base widths, f is between e^(1-1/R)/8 and 2e^(1-1/R), and f<=e/m. Dividing time by sqrt(e) leaves a summable local toll O(e^(-3/8)) and logarithmic multipliers whose sum is O(F(log₂e)): the logarithmic widths contract geometrically. This proves AQ2 for the executed recursion.

NW must also pay AI for every nonrecursive address operation. It therefore uses a slower-growing arity. Precisely, with

    x=ceil(log₂(a+2)), v_x=ceil(log₂(x+2)),
    y=ceil((x²v_x)^(1/3)), m=2^y-1,

it takes the largest even f<=a/A_m, where 2m<=A_m<=4m, and handles the fewer than 2A_m remaining bits by direct butterflies. These are NW's actual integer choices. The earlier lead draft's plus-one family is not substituted into this proof.

The numerical label penalty is only 2^(O(sqrt(y log(y+2)))). With x_f the next logarithmic width,

    x-x_f>=y/2,
    F(x)-F(x-y/2)>=c sqrt(y log₂(y+2))                      (AQ4)

above a fixed base. The normalized local address toll is at most 2^(C F(x)); it is retained, not discarded. A sufficiently large absolute exponent constant in the induction pays both that toll and the recursive multiplier using AQ4. The exact integer path satisfies sum log₂m_i<=log₂a_0. Consequently the product of the power-of-two batch widths is a fixed polynomial in a_0 and divides the large power-of-two root spectator range. There is no per-level spectator padding. These facts prove AQ3.

## AQ5. Substitution into the actual outer tape caller

The source chooses accepted transform shapes with k=Theta(log n), Nk=Theta(n), and short numerical record widths O(k), using absolute constants. This is an actual shape test and construction, not a choice of a continuous ideal transform size. Its source prime-shape threshold is one absolute cutoff, independent of our arity choices.

The source packed-XOR and controlled-block constructions consume a complete exact field-swap interface, not a particular exponent rho. Insert AQ2 into their actual stream operations. The offset, rank, comparison and compact-control descriptions have fixed polynomial degree in k: every adaptive m is at most k, and every compiler degree is absolute. Thus a single guard C₀log(k+2), with an absolute coefficient, pays their exceptional-record sorts and occupied borrowed coordinates. Guarded work adds only a fixed power of log(k+2) to J(k), together with fixed-degree polynomial(k) preparation. All borrowed coordinates are restored. No O_m constant is reinterpreted as uniform.

The synchronized short-transform schedule uses the permitted partial numerical Walsh calls with the source's fixed boundary norm/error exponents. AQ3 supplies those calls. Source roots and phases are constructed to the same fixed O(k) precision; the existing certified algorithms have polynomial(k) preparation. Completed numerical pieces are unitary; pointwise products and short-record arithmetic have their separately paid k log k costs. CRT maps, cyclic permutations and the synchronized schedule contribute a fixed number of families and O(log(k+2)) layers. Carries and the final contiguous binary output are paid as in the source.

More precisely, the source controlled-block ledger adds three logarithmic factors, and CRT/short-transform depth adds one. It follows, with b=4 and absolute C,E, that the complete accepted attempt costs

    C Nk sqrt(k) 2^(C F(log₂(k+2))) (1+log(k+2))^b
        + C(1+k)^E.                                         (AQ5)

The source outer functions do not instantiate an enormous m-by-module table. AI and NW construct only their polynomial-m descriptors and scalar data. Their own varying-arity setup is already charged in AQ2–AQ3; fixed-degree outer preparation is the additive term in AQ5.

## AQ6. Absolute precision and exact recovery

NW bounds a path's logarithmic intermediate amplification and coefficient heights by

    (1+log(k+2)) 2^(C F(log₂(k+2)))=k^o(1).                 (AQ6)

This is eventually less than k/100 after enlarging a fixed guard. For a concrete preflight bound, compute the actual adaptive width chain and use CW's polynomial-m coefficient-height and norm majorants. Their fixed-degree integer calculations take polynomial(k) preparation; no all-key or all-frequency maximum table is enumerated. This computes a safe error ledger and tests its guard before numerical execution. The number of actual numerical nodes is polynomial in k, since each local branching count is polynomial in m_i and sum log m_i<=log a_0. The bound concerns executed nodes, not merely a normalized volume quotient. The source path-to-common-ancestor propagation argument, the sqrt(N) factor from rounded coordinates, on-demand coefficient errors, and the fixed outer norm factors are all covered by p=C₁k with one absolute C₁. Bounded-divisor preparation and exact temporary products are charged and use O(k) scalar bits above that guard.

The caller's phase errors, coordinate products and transforms therefore satisfy the same fixed global error target as the source integer algorithm. Rounding the recovered convolution is exact; deterministic carry propagation writes the full product. No correctness decision is made from an unverified numerical approximation. Short or rejected shapes use an independently correct exact fallback.

## AQ7. One visited-cell cap and one fixed program

AI's two-pass rank schedule keeps the whole query-by-rank gather array within one payload volume because m r/N_label<=1. It keeps an absolute number of source, destination and current-rectangle arrays. Compact spectral repair tags only one of its 32B coarse roles at a time, with B>=2m+1, and removes the tags before recursive converters. FP preserves raw binary volume through field changes. Main spatial children have at most half the parent's incoming volume after charging padding, finite repair children have at most one sixteenth, and a full-volume reserve descent clears parent arrays and transfers ownership rather than parking another full copy. Descriptors on the whole path are additive polynomial(log V) data, absorbed by the root volume. These are bounds on marked regions ever visited, with sibling reuse.

NW likewise retains an absolute number of numerical arrays by preparing and finishing one rectangle at a time. Main children shrink by at least one half and finite repair by one eighth. Its smallest retained numerical arrays have exponentially many records divided by a fixed polynomial in k, which pays all polynomial(k) scalar and descriptor workspace. AI has an absolute space coefficient within those calls. The same marked intervals are reused after every completed phase. Hence AQ3 and the outer caller together visit C Nk=O(n) cells with one absolute coefficient.

No parameter-dependent chunking or weighted candidate search is needed for this stronger construction. The arity rules, exact roots, checks, finite-field constructors and template generators are fixed integer algorithms. All fixed numerical constants and thresholds are justified by the explicit majorants in the suppliers; increasing them affects only the machine's fixed program and its absolute complexity constants. Source shape tests are executed, and fixed marked work regions permit safe rejection before exceeding the cap. The exact fallback runs for small or rejected input lengths. The proofs show that the adaptive attempt succeeds at every sufficiently large length, so the finitely many exceptional lengths are absorbed into the global constant. No advice about an input length or uncharged precomputation is used.

## AQ8. Final asymptotic comparison

For accepted shapes k=Theta(L(n)), so log₂(k+2)=s(n)+O(1), and the additive polynomial(k) setup is negligible against Nk. Also log log k=O(log(s+2))=o(F(s)). Absorb the fixed logarithmic powers in AQ5 into its exponential to obtain AQ1.

The displayed log-overhead scale is strictly smaller than the admitted PP/E002 scale:

    F(s) / [s^(3/4)(log₂(s+2))^(1/4)]
      = (log₂(s+2)/s)^(1/12) -> 0.                         (AQ7)

This compares explicit proved envelopes, not lower bounds on the older machines' actual running time. The published L^(o(1)) notation alone does not supply an ordering against every possible quantitative consequence of its full proof. Our staged source/literature audit and the explicit new compilation steps support the provenance claim; broad mathematical priority remains unverified.

AQ1 implies H(n)=2^(O(s(n)^beta)) for every fixed beta>2/3, including beta=3/4. It does not remove the logarithmic factor at beta=2/3, establish H=O(s^alpha), or attain H=O(1). The programme's kappa_ov therefore remains null. Weak ETH is not a premise of this upper bound.

## AQ9. Verification boundary

The suppliers have separately reviewed unbounded proofs and exact finite identities. The lead replayed isolated copies of both new recurrences with `python3 -I -B`; receipts, copied source and source hashes are under `lead/replays/adaptive/`. AI's finite checker uses a declared toy profile; NW's numerical grid uses declared illustrative constants and 100-digit Decimal arithmetic. Neither is an execution of the enormous optimized label family, a formal proof of its asymptotics, or a full multiplication implementation. The inherited rational receipt is a hashed reference, not a newly rerun test. Global acceptance and any corrections belong in the separate admission/review files.

## Credits

Prepared for Jerry Chen (@CubeJerry), with substantial ChatGPT assistance. The pinned OpenAI manuscripts supply the foundational finite identities, endpoint constructions, numerical caller and integer recovery. The previous programme and S002 supply the documented extraction and binary-label work. S003's independent A/B/C routes supply the compact arithmetic, changed physical representation, uniform payload schedules and adversarial reviews; concurrent E002 independently established the preceding three-quarter scale through a different physical compiler. Concurrent E003 checkpoint df91e4c8e31b1020e05056db5b0eb16169ef3421 independently records a conditional two-scale candidate with the same final scale; its supplier/admission status is maintained in its own scoped record. These convergent paths are credited without a priority claim. All predecessor and contributor credits in those files are retained. No authorship of the OpenAI manuscripts or independent human validation is implied.

Concurrent update: E002 checkpoint8af1911b independently admits the same2/3-scale complete envelope using composite radix, one root field and a chunk-space wrapper. S003 uses direct absolute-space components. The lead read its theorem/admission; its separate supplier review provenance is preserved.
