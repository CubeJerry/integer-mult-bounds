# Compact exact count prediction over characteristic zero

Status: **partial/enabling**. A one-level exact spectral program, not an integer-multiplication bound. Source: OpenAI `math` at `3344da59991ed94f9ba711217b29c1d760badfa6`, Fourier `build/repair.tex`, count prediction, matrix-root and Hermite-repair lemmas. All-characteristic specialization is not claimed.

These changes remove exhaustive shift enumeration and generalized Clifford enlargement from the characteristic-zero predictor. Routing, repair, setup and precision remain charged obligations. Standard tools are applied to the source interface; novelty beyond this application is unchecked. The lead and Route C found real factorization independently. Route B studies a distinct constant-tail recurrence and rational Newton evaluation.

## A. Explicit translated shifts

For integer m>=2 set r=ceil(log2(4m^3)), t=2r, d=ceil(log2 m), q=2^d and M=q^t. In F_q choose distinct a_1,...,a_m and a nonzero F_2-linear functional ell. For each seed (v_0,...,v_{t-1}) assign one independent row the shift

    beta_j(v) = ell(sum_{h=0}^{t-1} v_h a_j^h).

Repeated shifts remain separate rows. Vandermonde evaluation has full row rank on at most min(t,m) positions. Therefore these field values, and their images under ell, are independent uniform values. XOR with any fixed frequency pattern k preserves this property.

Put c=sum_j(beta_j XOR k_j), S=m-2c. Each monomial in S^(2r) involves at most 2r positions, so its expectation is the independent Rademacher expectation. Counting pairings of surviving even-multiplicity tuples gives

    E S^(2r) <= (2r-1)!! m^r <= (2rm)^r.

Each surviving tuple has at least one pairing; there are (2r-1)!! m^r pairing/label assignments. Choose B=ceil(sqrt(rm)), u=max(0,floor(m/2-B)), v=min(m,ceil(m/2+B)), D=v-u. Markov gives, for EVERY k,

    Pr[c outside [u,v]] <= Pr[|S|>2B]
        <= (2rm)^r/(2B)^(2r) <= 2^(-r) <= 1/(4m^3).

This is a deterministic simultaneous guarantee, with no union-bound failure event. We have log2 M=dt=O(log^2 m) and D<=min(m,2ceil(sqrt(rm))+1)=O(sqrt(m log m)).

Enumerating degree-d monic binary polynomials and testing divisibility by monic polynomials of degree at most d/2 constructs F_q in 2^{O(d)}poly(d) steps. Finite-field existence ensures termination. Enumerating all seeds costs M poly(m,t,d) bit operations. This bounds SHIFT generation only.

## B. A real-root predictor without batch enlargement

Over Q let

    P(x)=(-1)^u sum_{h=0}^D (-2)^h binom(x-u,h).

For integer c in [u,v], P(c)=(-1)^c by the binomial theorem. Its degree is D and its leading coefficient is a=(-1)^(u+D)2^D/D!. Alternation forces a root in each open interval (u+i,u+i+1), 0<=i<D. Degree D forces precisely these D roots, all simple and real. Thus

    P(x)=a product_{i=0}^{D-1}(x-z_i),
    z_i in (u+i,u+i+1) subset (0,m).

Exact rational-sign bisection in each known unit bracket gives error 2^-p in O(p+1) evaluations. An exact midpoint root is retained exactly. Evaluating the binomial expression on a dyadic number has polynomial bit complexity in m,D,p. There is no numerical convergence assumption, root-separation oracle, or splitting-field construction.

Let Q_j be commuting unitary involutions with common eigenvalues (-1)^k_j. On the row with shift beta define

    C_beta=(m I - sum_j (-1)^beta_j Q_j)/2.

Its eigenvalue is c. The predictor P_beta=(-1)^|beta| P(C_beta) equals F=product_j Q_j on good rows. Apply the D affine factors C_beta-z_i I successively, then a and the sign. On M independent rows this uses **D pencil stages with M independent inputs**, without Clifford enlargement. Row matrices are diagonal, and every factor has the source form A_0 tensor I + sum A_j tensor Q_j. No zero workspace coordinate is counted as independent input.

This rational polynomial divides by factorials. It does NOT replace the integral multivariate predictor over F_p when p divides those factorials: counts separated by an odd p have the same field image and opposite parity. The finite-characteristic interchange path remains separate.

## C. Coefficients and norms

C_beta is self-adjoint with spectrum in [0,m]. Thus ||C_beta-z_i I||<=m, and |a|<=2 for D>=1. Any contiguous product has norm at most 2m^D including a leading scalar if present. If root errors are at most eta<=1, telescoping products gives

    ||P_tilde_beta-P_beta|| <= 2D eta (m+1)^(D-1).

Operator error 2^-p therefore requires at most

    p+ceil(log2(2D))+(D-1)ceil(log2(m+1))+1

fractional bits for roots. Error xi in a separately contributes <=xi(m+1)^D. Intermediate arithmetic rounding needs a caller charge. These are effective parameter-dependent bounds, NOT uniformly bounded conditioning as m grows or a complete recursive precision proof.

## D. Exact repair and scope

Set s=floor(M/(2m^3)). Each known exceptional set has cardinality <=M/(4m^3), hence <=s. Over C use distinct Vandermonde nodes 1,...,M. The source Hermite lemma with ell=2 applies: four predictor applications, one spectral table on 2s rows (at most 4s full forward/inverse conversions), and pointwise maps. This computes F on all M independent inputs in <=4D pencil stages. Constants are real algebraic; the spectral tables are rational because P(c) is rational at integer counts. Actual smaller exception sets may be used.

This is a complete ONE-LEVEL algebraic implication. It does not price construction/access of all frequency tables, row movement, spectral conversions or the complete fixed-tape caller. M=2^{O(log^2 m)} is not a total template-size, norm, setup-time, space or threshold bound. Route B's discrepancy-division repair is a separate option; no combination is admitted without a shared audited cost sheet.

## Open next questions

1. Compose with Fourier routing and bound the entire template, including repair table coefficient heights. Replace the tape Walsh dyadic-only premise by charged algebraic coefficient preparation and multiplication.
2. Quantify repair norms separately from root-factor norms.
3. Compare with Route B's pairwise-independent constant-tail recurrence without adding incompatible gains.

Credits: OpenAI November 24 Fourier construction and predecessors; standard finite-field t-wise independence, moments, interpolation and factorization; @CubeJerry's programme with OpenAI GPT-6 Astra Pro assistance. The source multiplication theorem is not a programme result.
