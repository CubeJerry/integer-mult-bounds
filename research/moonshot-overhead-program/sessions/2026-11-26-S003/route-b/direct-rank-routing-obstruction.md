# Direct coefficient-rank routing cannot replace the geometric pencil

Status: **proved scoped algebraic obstruction; independent review requested**. This tests a proposed route outside the retained rectangle invoice. It lower-bounds the coefficient-rank invoice of formal full-identity affine factorizations, not general interchange time or integer multiplication.

Pins: programme `0607d044d1d09489580da0e5828588820e1a6775`; OpenAI math `3344da59991ed94f9ba711217b29c1d760badfa6`. The concrete application uses `routes/A/power-two-degree-predictor.md`, `routes/A/characteristic-two-count-formula.md`, and `routes/B/structured-shift-check-refinement.md`. The proof uses elementary determinant degree and exact Boolean interpolation.

## 1. Proposed escape and optimistic budget

An affine stage is F_t=A_(t,0)+sum_j A_(t,j)Q_j, where Q_j is one physical query on an f-bit field pair. Instead of geometric shared delivery, factor each A_(t,j) through its rank r_(t,j), perform Q_j only on those intermediate rows, then expand and accumulate. Give this proposal every favorable local assumption: compact descriptions, polynomial-m ordinary scalar scans, absolute payload space, and free constant row-basis changes in the recursive invoice. On W independent rows its declared query mass is

    C_rank=(1/W)sum_(t,j)rank(A_(t,j)).                  (DR1)

Replacing stages by arbitrarily many query-selector stages, each row using only one query, cannot have a smaller separate-query invoice than the corresponding rank sum. Enlarging W is allowed if the complete identity holds on every row. The theorem gives C_rank>=m for the retained predictor, independently of the number of affine stages. This fails the required sqrt(m)m^o(1) local budget before any scalar work is charged.

## 2. A general determinant-degree theorem

Let K be a field and p in K[x_1,...,x_m] have degree D, 1<=D<=m. Assume that setting all but any D chosen variables to zero leaves degree D. Suppose square W-by-W affine pencils satisfy the formal identity

    F_l(x)...F_1(x)=p(x)I_W,
    F_t(x)=A_(t,0)+sum_j x_j A_(t,j).                   (DR2)

There is no bound on l or W.

**Theorem DR.** Every such factorization satisfies

    sum_(t,j)rank_K(A_(t,j))>=mW.                       (DR3)

**Proof.** Fix a D-element subset S. In factor t all variable-dependent images lie in U=sum_(j in S)im(A_(t,j)), whose dimension is at most the corresponding rank sum. A constant invertible row change puts U in the first dim(U) coordinates. The remaining rows are constant, so the determinant degree of this restricted pencil is at most dim(U).

After restriction, (DR2) has determinant p^W of degree DW. It is nonzero, so factor determinants are nonzero and their degrees add. Consequently

    DW<=sum_t sum_(j in S)rank(A_(t,j)).                 (DR4)

Sum over all binom(m,D) sets S. Each j occurs binom(m-1,D-1) times, and their ratio is m/D. This proves (DR3). QED.

The argument includes free constant mixing, arbitrary degree slack l>D and constant invertible conjugations. Enlarging a full-rate width scales both sides equally.

## 3. The retained characteristic-two predictor meets the hypothesis

Take K containing F4, with omega^2+omega+1=0. The accepted predictor has T a power of two, D=T-1<=m, a shift beta and window start u. Its formal degree is at most D. Make the affine substitution

    q_j=omega^(-beta_j)(1+(omega-1)x_j),
    q_j_squared=omega^(-2beta_j)(1+(omega^2-1)x_j).       (DR5)

The two query-power symbols are independent formal inputs to the affine construction; (DR5) is a valid formal substitution. On Boolean x_j, it makes the shifted ternary digit equal x_j. The predictor's value is then

    p(x)=gamma omega^((sum_j x_j-u) mod T),
    gamma=omega^(u-sum_j beta_j).                       (DR6)

This follows directly from its product of binary count-bit formulas. It is an equality of values on Boolean inputs, not an assertion that the right side is a formal polynomial expression.

Fix a D-element set S. The coefficient of squarefree monomial product_(j in S)x_j in the Boolean multilinearization is, in characteristic two,

    sum_(U subset S) p(1_U)
      =gamma sum_(c=0)^(T-1) binom(T-1,c)
                 omega^((c-u) mod T)
      =gamma sum_(r=0)^(T-1) omega^r != 0.              (DR7)

All binomial coefficients in that row are odd because T is a power of two. The residues (c-u) mod T permute 0,...,T-1. The geometric sum is nonzero because T is not divisible by three. Since the formal polynomial has degree at most D, a monomial of larger degree cannot reduce to this degree-D squarefree monomial; its coefficient in the original polynomial is the same. Thus every D-variable restriction has degree exactly D, as required by DR.

For an original stage with coefficients A_(t,j,1), A_(t,j,2), substitution gives

    A'_(t,j)=omega^(-beta_j)(omega-1)A_(t,j,1)
              +omega^(-2beta_j)(omega^2-1)A_(t,j,2).

Rank subadditivity gives rank(A')<=rank(A_1)+rank(A_2). Applying DR yields

    (1/W)sum_(t,j,epsilon=1,2)rank(A_(t,j,epsilon))>=m. (DR8)

Thus separately routing ranks of the two powers cannot remove the obstruction. The statement concerns every formal full-identity affine factorization of this predictor, not only the currently implemented cyclic factorization.

## 4. Optimistic recurrence and exact limits

Even with all scalar preparation free, the direct-rank proposal's positive invoice has main mass at least m. With a regular spatial split e/(C m)<=f<=e/m, its retained recurrence is therefore

    B(e)>=m B(f),                                      (DR9)

in addition to any positive ordinary-work bill. For a fixed minimum m0>C, let p0=log(m0)/log(Cm0)>1/2. For every m>=m0, m>=(Cm)^p0>=(e/f)^p0. Iterating (DR9) to a fixed base gives B(e)>=c e^p0. At AI's geometrically contracting logarithmic widths, there are O(log log e) levels, so the sharper telescoping bound is B(e)>=e/(log e)^C1 for an absolute C1. Either is asymptotically worse than sqrt(e) exp(O((log e)^(2/3)(log log e)^(1/3))).

This is a barrier for the proposed **declared sum-of-coefficient-ranks execution**, not for the runtime of all possible ways to execute these pencils. The accepted geometric executor already lies outside it: it shares distinct spatial queries through address-dependent endpoint maps rather than paying every coefficient rank separately.

Other possible escapes are explicit: identities required only on the allowed finite spectral set instead of formally; nonlinear query factors; a partial-output representation with a separately paid occupancy change; or a different physical query-sharing theorem. The determinant argument does not decide any of those cases. The formal full-rate hypothesis and direct-rank price must remain visible when using the conclusion.

`verify_direct_rank_obstruction.py` checks finite exact interpolation and determinant-rank cases, including a finite-spectral-only identity that defeats the formal hypothesis. It does not execute an interchanger or certify a lower bound outside this stated price model.

Prepared for Jerry Chen (@CubeJerry), with substantial OpenAI AI assistance.
