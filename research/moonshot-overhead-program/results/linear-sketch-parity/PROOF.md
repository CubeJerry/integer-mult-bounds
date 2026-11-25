# Odd-characteristic linear-sketch barrier for parity prediction

Status: **accepted scoped component proof; independently reviewed and replayed by Route A**. See `routes/A/review-linear-sketch-parity.md` relative to the programme root. The predictor may use arbitrary linear summaries and an arbitrary nonlinear readout. This strengthens a single-count restriction in a different parameter range; it is not a lower bound for general multiplication or all matrix representations.

Let p be an odd prime, x uniform in {0,1}^m, and A an r-by-m matrix over F_p with columns a_1,...,a_m. Write chi(x)=(-1)^(x_1+...+x_m). The predictor receives only the sketch y=Ax in F_p^r and outputs a sign. It may use any function f:F_p^r->{-1,+1}; no degree or computation-cost restriction is imposed on f.

## 1. Exact Fourier formula and universal advantage bound

For y in F_p^r let

    g(y)=2^(-m) sum_(x:Ax=y) chi(x).

The maximum possible prediction success is (1+Delta(A))/2, where Delta(A)=sum_y |g(y)|. This follows by choosing the majority sign independently on each fiber. For zeta=exp(2*pi*i/p), Fourier transformation gives

    ghat(t)=sum_y g(y) zeta^(<t,y>)
           =prod_(j=1)^m (1-zeta^(<t,a_j>))/2.

Thus Parseval and Cauchy-Schwarz imply

    Delta(A)^2 <= p^r sum_y |g(y)|^2
               =sum_(t in F_p^r) prod_j sin^2(pi <t,a_j>/p).  (LS1)

The t=0 term vanishes for m>=1. Since p is odd, every sine magnitude in this formula is at most cos(pi/(2p)). Therefore

    Delta(A) <= min{1, sqrt(p^r-1) cos(pi/(2p))^m}
              <= min{1, p^(r/2) exp(-pi^2 m/(8p^2))}.       (LS2)

Here cos z<=exp(-z^2/2) for 0<=z<pi/2, obtained by integrating tan z>=z. Zero columns or annihilating characters only decrease the right side of LS1. No assumption about equal column weights, rank r, or independent coordinates of the sketch is needed. One may replace r by rank(A) after choosing a basis of its image.

If the error fraction is at most delta<1/2, then Delta(A)>=1-2delta. In natural logarithms (LS2) gives the necessary condition

    r ln p >= pi^2 m/(4p^2) + 2 ln(1-2delta).             (LS3)

For fixed delta<1/2 and m/p^2 growing, this requires r=Omega(m/(p^2 ln p)). This is not a sharp claim near m=p^2: the single-count source obstruction has a stronger specialized bound in that regime.

## 2. Shifted rows and a full-rate average

Replacing x by x XOR beta changes Ax to an affine function of x with columns (-1)^beta_j a_j. Its parity differs by a fixed sign. The same bound therefore applies to every shifted sketch, even if each batch row uses a different A, beta and readout function.

For arbitrary nonnegative row weights summing to one, if every row uses at most r summaries, the average success over uniform x is at most (1+the LS2 bound)/2. Consequently it is impossible for all x to have a larger weighted fraction of correct rows. Some input violates any proposed per-frequency defect guarantee that exceeds this average. This is the full-rate batch consequence; it is not merely a statement about a random input model replacing worst-case correctness.

## 3. A matrix-pencil width/depth consequence

Consider a product of D affine matrix pencils of side R over F_p, with arbitrary fixed row maps before, after or between them. Every pencil entry is an affine linear function of x. Collect all the at most D R^2 variable linear forms into one sketch. Every final matrix entry is a function of that sketch. Fixed row maps introduce no new x-dependent summaries.

If a specified diagonal entry predicts chi(x) with constant success greater than one half, (LS3) applies with r<=D R^2. More generally if at least a fixed weighted fraction 1-delta of diagonal entries equals chi(x) for every x, the preceding averaging argument gives the same necessary condition. Values other than the two signs can be mapped to either sign without reducing exact-agreement success. Thus

    D R^2 ln p >= pi^2 m/(4p^2) + 2 ln(1-2delta).          (LS4)

Over a finite extension of degree e, expand each coefficient in an F_p basis. At most e D R^2 F_p-linear forms determine the output, so e multiplies the left side. This is a representation bound with all its hypotheses explicit. It does not assert that this sketch dimension is always minimal, or that every full-rate spectral program has this particular input contract.

For scalar pencils (R=1) and small p, constant-error parity cannot be achieved with O(sqrt(m)) stages whenever p^2 ln p=o(sqrt(m)). For D=O(sqrt(m)), an R-by-R representation needs R=Omega(m^(1/4)/(p sqrt(ln p))) over the base field. Polynomial width is still allowed; no exponential lower bound is claimed. Integral divided powers, non-linear summaries, changing input contracts and a different field characteristic remain outside the scalar restriction.

In the source's optimized label regime, p is comparable to inverse exponent slack J while m grows exponentially in J^3 log J. The displayed small-p condition then holds by a large margin. Merely replacing the one count by a small number of different weighted counts does not supply the missing compact scalar predictor.

## 4. Exact prediction has an elementary degree obstruction

If parity is recovered exactly from r F_p-linear summaries, then necessarily r(p-1)>=m. To see this, any function on F_p^r has a polynomial representative of degree at most p-1 in each variable, by tensor Lagrange interpolation. Composition with Ax has total degree at most r(p-1). Reduce modulo x_i^2-x_i without increasing degree. The unique multilinear representation of parity on the Boolean cube over F_p is prod_i(1-2x_i), whose degree is m because p is odd. Hence r(p-1)>=m.

The exact bound is attained by grouping at most p-1 binary variables in each summary and reading their unreduced counts in {0,...,p-1}. It is a statement about exact linear-sketch recovery, not an efficient parity algorithm: parity itself is already easy when the input bits may be accessed individually.

## 5. Verification and limits

An exact checker enumerates small sketch fibers and computes the optimal agreement using integer counts. For p=3 the Parseval bound has an exact rational form: every nonzero Fourier factor contributes 3/4, so Delta^2<=N_good*(3/4)^m, where N_good counts t with <t,a_j> nonzero for every j. These controls test arbitrary column choices, rank deficiencies, zero columns and weighted/shifted readouts. Negative controls reject an illicit extension to p=2 and a dimension-free assertion.

This proof uses elementary finite Fourier analysis and Boolean interpolation. It makes no priority claim for either method. Its intended contribution is a precisely scoped obstruction to replacing the source's integral predictor by a compact collection of ordinary linear summaries. Developed for Jerry Chen (@CubeJerry) during S002 with AI assistance; independent review and replay are recorded separately.

## Source rare-tail depth

For D=O(sqrt(m log m)), the scalar exclusion condition becomes
p^2 ln(p) sqrt(log m)=o(sqrt m). The accepted source choice
p=Theta(J), log m=Theta(J^3 log J) satisfies it. This does not exclude
polynomial matrix widths or nonlinear summaries outside the stated sketch model.
