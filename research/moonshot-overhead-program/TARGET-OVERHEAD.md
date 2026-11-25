# Quantitative target and first derivation

Define L(n)=1+log_2 n and s(n)=log_2 L(n). Published upper bound: T(n)<=n L(n)^(1/2+o(1)). The latest S002 section records an accepted explicit source extraction; earlier sections retain their checkpoint-specific scope.

The consolidated current statement is E002 Theorem P in the final section below. Earlier sections are dated research history, including the preceding S002 fixed-field result.

## Lemma (scheduler envelope, conditional on actual candidate completion bound)
Read the schedule in openai/math `uniformity.tex`. Suppose a fixed attempt i=(j,k), with r=2^k<=n, completes in t_i(n) actual operations and fits the common space cap. Its round is reached by s=i+ceil(log_2(t_i(n)+1)); each round costs O(2^s), so one machine halts in
T(n)<=C n + C' 2^i(t_i(n)+1).
This follows from a geometric sum over rounds, including clocks, cleanup and output. If for all n>=N_i one proves t_i(n)<=A_i n L(n)^(1/2+1/(j+2)), then
T(n)=O(n sqrt(L) [1+inf_{i usable} (2^i A_i)L(n)^(1/(j(i)+2))]).
The constants in O are universal; the infimum must only contain certified usable attempts. This is a **proved conditional arithmetic consequence of the source scheduler**, not a new multiplication bound. Candidate generation, fixed programme sizes, r^2 chunk calls, cleanup and all unsuccessful runs must be included in t_i.

## Parametric calibration
If for a valid sequence of candidates j, D_j=2^(i_j) A_j <= 2^(C j^p) and log_2 L(N_j)<=C' j^(p+1) (same positive p; sufficiently large j), then taking j=floor(c s^(1/(p+1))) for small fixed c>0 yields log_2 H=O(s^(p/(p+1))). This is a purely conditional calibration; no bound on D_j or N_j has been shown. In particular, a finite-template existence proof by enumeration alone does not establish any usable growth law.

## Endpoint
Exact H=O(1) would require uniform bounded overhead by a genuinely stronger family/direct algorithm or a different schedule. Even D_j>=2^j at optimal j implies an unbounded overhead for the displayed fixed-exponent family; this does not exclude other architectures. Any proposed poly(s) overhead must be proved with its own complete cost ledger.

## S002: stronger scheduling interface, still no complete envelope

The first scheduler above is the published schedule. A new prefix-weighted schedule is proved in [Route A](routes/A/scheduler-and-chunking.md): a valid interpreted attempt i completing in actual cost t_i gives

T(n) <= C[n + i(1+log i)^2(t_i+1)].

The proof includes round enumeration, clocks, cap checks, cleanup and a schoolbook fallback. The source candidate family is sampled at j=2^h-2, so its excess exponent is 2^-h. A candidate with certified runtime coefficient a_j, proportional space c_j, fixed setup space d_j, generator cost g_j and applicability threshold U_j can be chunked using r_j<8c_j and common linear space. The resulting bound (A10) keeps all five quantities and the index weight visible. See that note for exact rounding and eligibility thresholds.

This is a proved interface conditional on concrete candidate profiles, not a complete conditional overhead theorem: those profiles still need to be obtained from an actual source compiler. The older exponential-index estimate remains a correct description of the original scheduler, but is no longer the best scheduler available in this programme. No particular H, alpha or kappa_ov has been certified.

## Focused E001 quantitative diagnostics and new source obstruction

The all-length scheduler certificate, including schoolbook fallback and nonattained-infimum details, is reconstructed in [CERTIFICATE.md](results/epsilon-uniformity/CERTIFICATE.md). Under explicitly specified nondecreasing `j+k` enumeration, its normalized constants force `F(x)=Omega(x^(2/3))`; this restricts that sufficient estimate, not actual machine time. Distinct unbounded schedule indices alone rule out a bounded certificate without giving that quantitative rate.

A new source-specific obstruction [proves](results/epsilon-uniformity/INTERCHANGE-OBSTRUCTION.md) `D>=2^(2p-1)+1` for the rational address Gram construction. The retained reserve inequality then forces `p<sqrt(m)`, while the central count window has width at least `sqrt(m)`. Raising p cannot rescue scalar count prediction within this construction. The characteristic-zero compact predictor therefore needs a different bridge into interchange.

The independent [nonstationary recurrence](results/epsilon-uniformity/route-c/NONSTATIONARY-RECURSION.md) gives a complete conditional endpoint for interchange when local excess is summable across logarithmic-logarithmic scales, with all local setup and space contracts stated. Current Walsh routing toll and [radix padding](results/epsilon-uniformity/route-c/SOURCE-PADDING-BARRIER.md) remain distinct obstacles. No new complete multiplication envelope is admitted.

## E001 checkpoint 3 — Scope of the current positive and negative drafts

A proved input-dependent-radix preparation lemma removes the literal fixed-radix padding obstruction. It supplies no complete varying-parameter multiplier. A proposed elementary-tower extraction of the original templates is undergoing a full compiler/threshold audit; its terminal envelope is not yet admitted. A separate written proof shows a factor-rank loss for the literal label matrix modulo p² and is awaiting independent review. The strongest admitted complete multiplication bound therefore remains the published qualitative residual exponent.

## S002 accepted complete envelope

The [theorem](routes/A/explicit-extraction-theorem.md) and [completed review gates](verification/S002/lead-review-explicit-extraction.md) establish

    H(n) <= 2^{O(s(n)/(log2 log2 s(n))^(1/6))}

for one exact deterministic finite-alphabet multitape full-product machine with a common O(n) visited-cell cap. A correct fallback covers every length. No conjectural assumptions are used. Absolute constants and the fixed eventual prime-shape cutoff are not numerically evaluated.

The explicit search accepts with log2 m_j=O((j+2)^6). Complete generator/physical profiles imply log2 D_j and log2 L(N_j)<=2^(2^(C(j+2)^6)). An eligible sparse j of order (log2 log2 s)^(1/6), with exact rounding and threshold checks, gives the displayed envelope. This quantifies the qualitative source theorem; it remains slower than every H=2^{O(s^beta)}, beta<1. No kappa_ov, polynomial-in-s overhead or constant endpoint is established. Earlier E001 sections describe that concurrent session's own checkpoint state and remain as provenance.

## E001 checkpoint 4 — Sharper admitted quantitative profile

The focused source extraction now gives, for one exact fixed multitape machine with uniform O(n) visited cells,

    H(n) <= 2^{O(x (log2(y+2)/y)^(1/3))},
    x=log2(1+log2 n),  y=log2 log2(x+16).

A weaker simple form is H<=2^{O(x/y^(1/4))}. Proof: `results/epsilon-uniformity/THEOREM.md`; physical costs: its `route-a/compiler-invoice.md`; independent audit: `route-c/ELEMENTARY-TOWER-REVIEW.md`. The sharper log m=O(j³ log j) choice refines S002's preceding j^6 certificate. This quantifies the source scheme without an actual-runtime, priority, practical-crossover or endpoint claim. No kappa_ov is assigned on this scale.

The separate bounded-preflight theorem proves H=O(x^a), including a=0, only under its explicit quantitative execution, threshold, preparation and common-space plan contracts. Fixed candidate constants can be absorbed into slack at an explicit later threshold, so those quantities must be controlled jointly.

## S002 third wave — independent cubic-logarithmic extraction

The accepted source family also satisfies log2 m_j=O((j+2)^3 log2(j+2)), using absolute actual call inequalities, the existing quarter pre-padding Walsh margin, and all physical/compiler constants. Its complete profiles obey log2 D_j, log2 L(N_j)<=2^(2^(C (j+2)^3 log2(j+2))). Exact dyadic candidate rounding and eligibility give

    H(n)<=2^{O(s (log2(y+2)/y)^(1/3))},
    s=log2 L(n), y=log2 log2(s+16).

This is the same scale recorded by E001, now independently derived and reviewed in S002. The [lead review](verification/S002/lead-review-sharper-extraction.md) records all reused gates. The correct fallback and common O(n) visited-cell cap persist. This rate remains larger than 2^{O(s^beta)} for every fixed beta<1; no kappa_ov is assigned.

The new characteristic-two order-three physical family changes the finite algebra and repair closure but retains a large generic representation. Proposed compact IP/IP4 hypotheses would remove one exponential layer and give a stronger conditional iterated-logarithm rate. Those hypotheses are open and do not alter this unconditional envelope or replace E001's separately scoped conditional selector theorem.


## E001 compact-root conditional target — 15:20 UTC

The complete MR implication in `results/epsilon-uniformity/route-a/single-exponential-root-hypothesis.md` gives H<=2^{O(x(log2(z+2)/z)^(1/3))}, z=log2(x+16), under a precise actual-bit-construction hypothesis for a full-rate matrix root. It charges both transform branches, all shifts, repair, scalar descent, refined rational heights, physical compilation, thresholds, chunking and search. MR remains unproved. This is the same asymptotic scale as S002's more general IP conditional bridge at4689161c; neither changes the unconditional bound. The bounded-preflight poly-x conditional result remains separately scoped.

## S002 fourth wave — unconditional formula extraction

The [formula theorem](routes/A/formula-extraction-theorem.md) and [lead/independent gates](verification/S002/lead-review-formula-extraction.md) replace the literal monomial evaluator by a complete full-rate cyclic factorization of a balanced arithmetic formula. The actual finite profile becomes

    P_m<=2^{2^{C(log2(m+2))^2}},
    log2 D_j, log2 L(N_j)<=2^{C J^6(log2 J)^2}.

For s=log2 L(n), the largest dyadic J below [log2 s/(2C(log2 log2 s)^2)]^(1/6) is eligible and has logarithmic prefactor at most sqrt(s). Thus

    H(n)<=2^{O(s (log2 log2 s)^(1/3)/(log2 s)^(1/6))}

for one fixed exact finite-alphabet multitape machine with uniform O(n) visited cells. This supersedes the earlier explicit programme envelopes. Its proof uses no compact-IP assumption. The displayed upper-bound scale still grows faster than s^beta in log H for every fixed beta<1; this is not a lower bound on actual machine time. No benchmark kappa_ov, polynomial-s overhead or constant endpoint is claimed.

## S002 fifth wave — IP4 established and stronger unconditional envelope

The [explicit count formula](routes/A/characteristic-two-count-formula.md) establishes IP4. The [complete theorem](routes/A/fixed-field-extraction-theorem.md) gives

    P_m<=2^(m^C),
    log2 D_j, log2 L(N_j)<=2^(C J^3 log2 J),
    H(n)<=2^{O(s (log2 log2 s/log2 s)^(1/3))}.

Every fixed candidate has a bounded constructor and charged physical caller; the single scheduled machine has uniform O(n) visited cells and exact full output. Choosing a dyadic J of order (log2 s/log2 log2 s)^(1/3) makes the actual log-prefactor and eligibility threshold at most sqrt(s). Both independent global gates and the lead gate passed.

The characteristic-two formulas use nonmultilinear intermediates and equality on actual order-three spectral tuples. They do not prove the separate dyadic IP or E001 MR representation hypotheses. They nevertheless remove the IP4 premise from this complete bound. All previous envelopes remain historical valid estimates. Constants/cutoffs are unevaluated; the constant endpoint and stronger fixed-beta subexponential scales remain open.

## E001 independent formula envelope and representation limit

The focused [complete theorem](results/epsilon-uniformity/THEOREM.md) independently obtains the same earlier formula envelope: H<=2^{O(x[(log_2(z+2))²/z]^{1/6})}, x=log_2 L, z=log_2(x+16). It uses one repeated dyadic affine root, all-row identities and a literal bit generator. Both transform branches and the complete physical invoice are included. The preceding baseline is preserved verbatim in BASELINE-THEOREM.md.

The [general formula-size transfer](results/epsilon-uniformity/FORMULA-SIZE-TRANSFER.md) supplies intermediate conditional rates. The [matching recipe lower bound](results/epsilon-uniformity/route-c/FORMULA-RECIPE-LOWER-BOUND.md) shows that optimizing only multilinear formulas within the same unreduced composition cannot reach singly-exponential row size. This is not an actual multiplier-time or arbitrary representation lower bound. Both sessions' independent provenance is preserved.

## Fresh concurrent fixed-field result — 16:09 UTC

Before publishing this focused checkpoint, remote848fbf1d7a5e192aa352d79b4d3e36fa06be21ee was read and preserved. S002's new characteristic-two count formulas establish IP4 and its stronger third-root envelope. E001's dyadic formula theorem remains a separate weaker result. Root has read the new finite formula, complete extraction and lead review; additional E001 finite and physical reviews are in progress. The dyadic MR hypothesis remains open even though its displayed rate is now attained by S002's different fixed-field construction.

## E001 closing integration — 16:23 UTC

The strongest shared third-root envelope is now also covered by separate E001 finite-count and physical-composition reviews. E001 Theorem F remains the weaker independent dyadic construction. The general formula-size theorem and matching unreduced-recipe obstruction retain their precise scopes. Full results and remaining obligations are in results/epsilon-uniformity/FINAL-REPORT.md.

## E002: first admitted fixed-beta envelope

The current strongest written theorem is [P](results/epsilon-uniformity/sessions/E002/lead/polynomial-profile-theorem.md):

    H(n)<=2^{O(x^(3/4)(log2(x+2))^(1/4))}, x=log2(1+log2 n).

It has one exact fixed multitape machine and uniform O(n) visited space.
Every fixed beta>3/4 follows; no pure beta=3/4 or polynomial-x/constant
overhead is asserted. Proportional time/space are m^{O(1)}, whereas allowed
additive setup is 2^{m^K}L(u)^{m^K}. The source geometry still needs
log m=O(J^3 log J). The actual dyadic selector J^4 log2 J<=x+O(1),
chunk factor r=m^{O(1)} and charged fallback give the complete envelope.
See [parameters](results/epsilon-uniformity/sessions/E002/PARAMETERS.md) and
[admission](results/epsilon-uniformity/sessions/E002/lead/ADMISSION-P.md).
The result improves the programme's preceding explicit envelope. A current
scoped search is not a priority certification. kappa_ov remains undefined
on this scale. All earlier sections above retain their historical status.

## E003 candidate with two distinct recursion scales

E003's separate local schedules give a conditional transfer draft on the
scale `log H=O(x^(2/3)(log2(x+2))^(1/3))`, with `x=log2(1+log2 n)`.
Interchange uses a power-size arity so its logarithmic losses sum
geometrically; Walsh uses `log m=Theta(x^(2/3)(log(x+2))^(1/3))` locally
to pay its genuine polynomial routing toll. All physical gates remain
explicit in `results/epsilon-uniformity/sessions/E003/route-b/TWO-SCALE-RECURSION.md`.
This candidate is not yet an E003 unconditional bound, and no kappa_ov
is assigned to it. The concurrent admitted E002/S003 result is preserved.

## S004 alternative-partition conditional transfer

The precise JR hypothesis in `sessions/2026-11-26-S004/lead/joint-rectangle-transfer.md` asks for an exact disjoint partition of the all-coordinates-unequal relation with local load exp(O(k)) poly(log q). Under JR, Section 9 proves H<=2^{O(s^(3/4))} for the same fixed exact multitape model and common O(n) visited cap. A/lead accepted the composition; JR is unproved. This conditionally removes (log s)^(1/4) from the S003/E002 displayed log-overhead. A small q=4,k=2 example does not prove JR. The unconditional target remains unchanged by S004.
