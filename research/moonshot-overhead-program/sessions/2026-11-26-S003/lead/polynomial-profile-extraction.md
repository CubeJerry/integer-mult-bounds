# A polynomial physical profile and fixed-power overhead envelope

Status: **accepted complete written unconditional construction**, after independent Route C global review and lead admission. See `../route-c/REVIEW-POLYNOMIAL-PROFILE-EXTRACTION.md` and `ADMISSION-PP.md`. All local constructions are explicit; no additional representation hypothesis remains.

Write L(n)=1+log₂n and s(n)=log₂L(n). Logarithms are binary. The model is exact full-product multiplication by one fixed deterministic finite-alphabet multitape machine, head movement charged, with one uniform O(n) bound on all visited cells. Exact fallback covers every exceptional length.

## 1. Theorem and dependency boundary

**Theorem PP.** The compact constructions, pinned OpenAI integer caller and established common-cap wrapper give

\[
T(n)=O\!\left(n\sqrt{L(n)}\,2^{O(s(n)^{3/4}(\log_2(s(n)+2))^{1/4})}\right),
\qquad\text{visited cells}=O(n).\tag{PP1}
\]

| Gate | Supplier |
|---|---|
| Independent finite inputs | S002 count/full-rate identities; S003 B1 executes scalar slices without listing the module matrix. |
| Geometric maps | B2: explicit small-dyadic endpoints and reserve-only maps at radix 3. |
| Spectral correction | SR: computed check-space maps, ordered comparison keys, independent modules and paid padding. |
| Leading rows | PB: multidigit packed batch with no radix above the batch width. |
| Complete interchanger | B3/CI: actual shared endpoint order, child volumes, fixed encoding and reused tapes. |
| Numerical Walsh | CW: rational selectors, bounded-divisor arithmetic and absolute O(k) precision above a polynomial-m guard. |
| Outer multiplication | Pinned `permutations.tex`, `integers.tex`, `uniformity.tex`; S002 audit of unchanged source operations. |
| Common cap | S002 `routes/A/scheduler-and-chunking.md`, A1–A5 and A8–A10. |

Pins: OpenAI math `3344da59991ed94f9ba711217b29c1d760badfa6`; predecessor `0607d044d1d09489580da0e5828588820e1a6775`. E002's independently developed separated-setup transfer, imported at `9d5abf18ff741ff6f8b9f82790e0475fc662b4fe`, gives the same envelope under a more permissive setup contract and a different selector. Here we use the established weighted scheduler and polynomial compact descriptions. No priority claim follows from the convergence.

The exact characteristic-two field executes address permutations. Numerical Walsh retains rational/complex coefficients on encoded records. No numerical coefficient is reduced modulo two and no arithmetic circuit is substituted for a tape processor.

## 2. Explicit parameters and complete call margin

Use dyadic J=2^h, h>=2, with theta_J=1/2+1/J and rho_J=1/2+1/(2J). Let d be the least power of two at least100J, hence d<200J. For numerical Fourier labels take the least even v>=100J. Let u be the least power of two at least2^60 J³h, and m=2^u+1. These are exact integer operations. The constructor checks its finite call counts and guards. We have

    log₂m <=2^61 J³h+1 = O(J³log₂J).                  (PP2)

Put D_old=2+(2d-1)q^(2d-1), the prior coarse address-dimension bound. The characteristic-two labels have mr*/N<=1 and, for x=log₂m,

    log₂[D_old(1+lambda)]<=3x/d+10d²log₂(4x).

B2 uses Dg=2D_old. B3 prices a pencil by Rpen=2^20 Dg(1+lambda)(1+mr*/N). Its predictor degree Dp<=24sqrt(m). At depth a0=ceil(x/4), the completed swap word costs Qm=8Dp Rpen+3m4^(-a0). Padding is below two. Including occupied-reserve calls gives

    log₂(2Qm+2(Dg-2))
       <=x/2+3x/d+10d²log₂(4x)+40.                  (PP3)

This pays the new geometry constant, doubled dimension and wider window. At x0=2^60 J³log₂J, log₂(4x0)<=40log₂J for J>=4. The ratio log₂(4x)/x decreases thereafter. Thus

    3x/d+10d²log₂(4x)+41
       <=(3/100)x/J+400002J²log₂(4x)<x/(2J),

the second term already being below x/(4J). B3 therefore has eta=1/2:

    2Qm+2(Dg-2)<=m^rho_J/2.                          (PP4)

The same range gives N<=m^5 and polynomial bounds for Dg,lambda,d. Numerical Walsh retains sigma_F/W_F<=128sqrt(m)D_Flambda_F, D_F<=m and A=2(m+D_F-1) in[m,4m]. Its logarithmic loss is at most2x/v+vlog₂(3x)+log₂(3v)+O(1), giving sigma_F/W_F<=A^rho_J/4 at this larger threshold. Integer-power comparisons check both rational-power margins.

## 3. Complete candidate profile

For one absolute effectively enlargable K, the compact candidate has

\[
a_J,c_J,g_J,d_J\le m_J^K,\quad
\tau_J(z)\le a_JzL(z)^{\theta_J},\quad
\operatorname{space}_J(z)\le c_Jz+d_J\quad(z\ge U_J),\tag{PP5}
\]
\[
U_J\le\max\{U_{\rm abs},2^{m_J^K}\}.\tag{PP6}
\]

Generation time is g; d includes retained descriptions. Tau includes interpreted digit execution, preparation at that length, return, erasure and movement. U_abs is the source's fixed prime-shape cutoff, independent of J; its numerical value is unnecessary for correctness.

**Generation/dispatch.** Formulas, graded modules, labels, rectangles, binary rank factors, dyadic lists, field/nodes, coarse role maps and integer W have polynomial size/construction time in m. The module may be exponential; only log W is retained. No step scans W instruction entries. One fixed processor handles the compact grammar; rescanning polynomial descriptions adds a fixed power of m. Coefficient algorithms and norm majorants have polynomial descriptions. The machine does not construct all-frequency verification archives.

**Interchange.** CI provides m^C V(1+e)^rho_J work and m^C V visited cells for arbitrary spectators. Encoding occurs once per invocation and stays fixed internally. Grouping preserves summed child volume; a main child is confined to one label or small repair leaf. Full-volume reserve descents retain descriptors after clearing main arrays. Tags are stripped before children. Binary radix padding is below nine.

**Numerical Walsh.** CW supplies polynomial-m costs/generation, actual scalar arithmetic, absolute O(k) widths and the rho_J recurrence at k>=m^C. Newton/Vandermonde work and coefficient rounding are charged. Child ratios are retained. Full address scans are used only for Theta(k)-bit numerical records; raw interchange uses amortized masks.

**Outer caller.** Guarded XOR and controlled blocks have a fixed polynomial degree in k. Enlarging guards by O(log m) changes only polynomial-m coefficients. Exceptional sorts, ranks, occupied borrowed coordinates and returns are paid. Synchronized short Fourier schedules, roots/phases, CRT, coordinatewise products, carries and contiguous output retain fixed-degree construction and O(log k) layers. Boundary norm exponents are absolute. CW gives absolute widths above a polynomial-m guard. Accepted shapes have k=Theta(log z), Nk=Theta(z), with absolute constants.

**Setup/space/thresholds.** CI has polynomially many grouped call types and arity>=m, giving polynomial(m) times a fixed polynomial in k nodes; individual module rows are not separate recursion nodes. Walsh has the same property since W_F,sigma_F are polynomial and A>=m. Finite unrolling is polynomial. Descriptor/phase setup has an absolute degree in k. A total bound m^C(1+k)^E, for absolute C,E, fits2^(k/4) above an enlarged fixed power of m. Descriptor storage is bounded by setup work. Marked-region reuse and fixed child contractions leave a polynomial-m cell coefficient. This k guard also pays numerical gains and spectator padding. Only U_abs remains separate. This proves the form PP5–PP6 without a template-dependent polynomial exponent.

**Slack.** The initial bill is m^C zL(z)^rho_J(1+log₂L(z))^b for absolute b. Maximizing(1+t)^b2^(-t/(2J)) bounds it by C_bJ^b; since J<=m this is polynomial in m and gives theta_J. Log factors are paid.

Every candidate has exact guarded fallback. Failed shapes, caps, timeouts or unprepared plans return no partial result. These profiles claim no practical cutoff or instantiated enormous template.

## 4. Common-cap assembly and actual scheduling

Use the audited wrapper with r_J the least power of two at least4c_J and

    N_J=ceil(max{8c_J,4(c_J+d_J),r_JU_J}).

For n>=N_J, z=ceil(n/r_J) is admissible and c_Jz+d_J<=n/2. Diagonal chunk assembly produces the exact2n-bit output in

    g_J+O((a_J+1)c_JnL(n)^theta_J)

steps, including r_J² digit products and O(nr_J) movement/carries. Marked regions bound all visited cells by one absolute O(n).

The fixed prefix-weight restart schedule runs the dyadic exponent/chunk pairs. Decoding, generation, clocks, cleanup, failed attempts and input scans are charged. For h=log₂J and k_J=log₂r_J the successful-attempt penalty is

    O((h+k_J+1)²[1+log₂(h+k_J+1)]²).

It is polynomial in log m and h since k_J=O(log m). PP2,PP5,PP6 give absolute C₁,C₂ with

\[
T(n)\le C_1n\sqrt{L(n)}[1+D_JL(n)^{1/J}]
\quad(n\ge N_J),
\]
\[
\log_2D_J,\ \log_2L(N_J)\le C_2J^3\log_2J.\tag{PP7}
\]

The additive generator is included. U_abs adds only a fixed term. These are actual attempts in one fixed schedule, not free length-dependent advice.

## 5. Eligible dyadic inversion and scope

For large s let h>=2 be maximal with2^(4h)h<=s and J=2^h. This analyzes the defined schedule. Maximality gives J⁴h<=s<(2J)⁴(h+1), so J=Theta((s/log₂(s+2))^(1/4)). Then J³log₂J=O(s/J)=o(s); PP7 proves n>=N_J eventually, including its fixed constants. This eligible attempt gives

\[
\log_2H(n)\le O(1)+C_2J^3\log_2J+s/J
=O(s^{3/4}(\log_2(s+2))^{1/4}).\tag{PP8}
\]

This proves PP1. Exact fallback covers smaller lengths.

The prior admitted scale was log₂H_old=O(s(log₂log₂s/log₂s)^(1/3)). The new displayed scale divided by that scale is

    s^(-1/4)(log₂s)^(7/12)/(log₂log₂s)^(1/3) ->0.

Thus the explicit envelope scale improves. An old O-envelope is not a lower bound on actual overhead. This also does not purport to beat an unspecified published o(1) without a quantitative comparison. PP1 implies H=2^{O(s^beta)} for every fixed beta>3/4, e.g.4/5. It does not remove the log factor at beta=3/4, prove polynomial-s overhead or reach constant overhead. No kappa_ov is assigned; Weak ETH is not an upper-bound premise.

The compact execution and explicit dyadic realization are source-specific construction refinements; inversion of the profile is elementary. Finite tests and independent AI-assisted written reviews are not full tape execution, Lean builds, human referee reports or exhaustive novelty certification.

## Credits

Jerry Chen(@CubeJerry); the November24 OpenAI manuscripts and credited predecessors; S002/E001 count, full-rate, label, repair, compiler and common-cap work; S003 A/B/C proofs/reviews; concurrent E002 physical/separated-setup work; substantial ChatGPT assistance in derivation, verification and integration. Source-paper authorship and standard algebra/arithmetic facts retain their respective credit.
