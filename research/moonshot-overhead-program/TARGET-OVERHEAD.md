# Quantitative target and first derivation

Define L(n)=1+log_2 n and s(n)=log_2 L(n). Known upper bound: T(n)<=n L(n)^(1/2+o(1)); an explicit H(n) is not yet certified.

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
