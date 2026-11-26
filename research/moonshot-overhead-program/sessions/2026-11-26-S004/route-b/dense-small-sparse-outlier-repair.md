# Dense small errors with sparse outliers

Status: **proved composition draft; exact finite controls passed;
independent review pending**. This corollary combines the charged small-modulus
convolution engine with the admitted sparse residual correctors. It was
suggested by the session lead after the amplitude audit. It broadens the
repair interface; it supplies no fast candidate with this mixed promise
and no new complete integer multiplication bound.

## 1. Signed promise and exact splitting

Let A,B have degree below h and nonnegative b-bit coefficients. Let
D=2h, let C have integer coefficients of absolute value at most Cmax,
and define

    E=AB-C,  Emax=h 2^(2b)+Cmax,
    tau=ceil(log2(2Emax+2)),  V=D tau.

Choose an integer a with `1<=a<=tau`, and put M=2^a. The mixed promise
is that at most S coefficients satisfy `|E_i|>=M/2`, where `1<=S<=D`.
The remaining coefficients may all be nonzero. Their positions and the
exceptional coefficients' values are unknown. Larger choices of a are
unnecessary: M=2^tau already exceeds 2Emax.

Use the small-modulus convolution engine in
`bounded-amplitude-residual-repair.md` to obtain every coefficient of
AB modulo M. Subtract C modulo M and choose the centered representative

    r_i in [-M/2,M/2),
    C'=C+r,       F=AB-C'=E-r.                              (Hyb1)

The half-open convention makes the endpoint unambiguous. Whenever
`|E_i|<M/2`, we have r_i=E_i, so F_i=0. Therefore F has at most S
nonzero coefficients. Each F_i is a multiple of M; that extra divisibility
is not needed by the sparse corrector. The safe height bounds are

    |C'_i|<=Cmax+M/2,
    |F_i|<=Emax+M/2.                                       (Hyb2)

Since `M<=2^tau<4(Emax+1)`, both bounds increase the required coefficient
bit length by only an absolute constant. Apply the signed sparse
corrector to the same A,B and the explicitly computed candidate C'.
It recovers F, so C'+F is exactly AB. The final carry scan produces the
integer product.

This correctness proof uses the mixed promise. Its sparse verification
only distinguishes residuals within the promised support class. It does
not turn arbitrary signed modular residues into a general verifier.

## 2. Complete summed invoice

Fix alpha>1/2 and the same fixed exact short integer multiplier as in
the two component theorems. To make the sparse parameters concrete, put

    q=ceil(log2 D),
    K=2 binom(2S,2) q+4,
    Emax'=h 2^(2b)+Cmax+M/2,
    beta=min{j: 2^j>8D(S+1)(Emax'+1)},
    k=beta K(K+1)/2.

We have beta=Theta(tau), with absolute constants, since S<=D and
tau already dominates log D and b. The volume D beta is thus Theta(V).
All parameter construction, stream preparation and recoding is included
in the component invoices. The total promised repair time is

    O_alpha(
       V
       +h a(1+log h)
          [1+log log(h+2)+(1+log(a+1))^alpha]
       +V(1+log(k+1))^alpha+k^6
    ).                                                     (Hyb3)

There is one O(V) bound on cells ever visited. Run the modular engine,
form and retain the O(V)-bit candidate C', and reuse its work regions
for the sparse engine. Each component has fixed tapes and a uniform
visited-space constant. The sparse branch k>V uses its already charged
packed schoolbook fallback; the composition does not allocate k cells
when k exceeds V. A fixed number of input/candidate copies changes only
the constant. Signed correction and carries take O(V) additional time.

For S=0 the mixed promise is just the amplitude promise and the sparse
stage is omitted. For a supplied S>D, cap S at D. Taking larger allowed
error amplitude raises the modular cost and may lower the outlier budget;
the formula states the cost of each chosen pair (a,S), without presuming
that an optimal pair is known or can be verified for a signed candidate.

## 3. Sound one-sided budgeted composition

Now assume the candidate construction independently guarantees E_i>=0.
Use the least nonnegative modular representative instead:

    0<=r_i<M,    C'=C+r,    F=E-r.                         (Hyb4)

Then F_i=M floor(E_i/M)>=0. It is supported exactly at those positions
where E_i>=M, and F_i<=E_i<=Emax. Consequently C' remains a
coefficientwise lower bound for AB. Apply the dense-safe, three-moment
one-sided sparse certificate to A,B,C' with a chosen budget S. This
procedure accepts only the complete exact product even if the actual
number of outliers exceeds S. If at most S coefficients satisfy E_i>=M,
completion is guaranteed within the budgeted time. Otherwise it may
still recover all outliers and accept, or report an incomplete budget;
it never accepts an incorrect result under the nonnegativity premise.

For this branch replace K by

    K_+=2 binom(S,2) ceil(log2 D)+4,
    beta_+=min{j:2^j>8D^3(Emax'_++1)},
    Emax'_+=h 2^(2b)+Cmax+M-1,
    k_+=beta_+ K_+(K_++1)/2.

Again beta_+=Theta(tau). The full attempted-work invoice is (Hyb3)
with k_+ in place of k, plus the explicit scalar mass product

    O_alpha(tau(1+log(tau+1))^alpha).                       (Hyb5)

This product computes A(1)B(1) in the test
`F(1)=A(1)B(1)-C'(1)`. Its input sums have O(tau) bits because
tau>=2b+log h up to an absolute constant. The sums themselves cost O(V).
For S>=1 the scalar product can also be absorbed into the coarse k_+^6
allowance, with a constant depending on alpha, but it is displayed so
that no O(V) absorption is silently used when h is constant and b is
arbitrarily large. The space remains O(V).

For a zero-outlier budget, use the simpler mass test
`sum r_i=A(1)B(1)-C(1)` from the amplitude note. It is sound under
nonnegativity and completes whenever every E_i<M. Its full cost is the
modular term of (Hyb3), O(V), and the scalar term (Hyb5), without sparse
fold construction. A failed one-sided budget may be followed by a fixed
exact full-length fallback, whose cost is additional unless covered by
the already stated k>V branch.

## 4. Regimes and limitations

In the usual packed regime `h=Theta(n/log n)`, b=Theta(log n), and
log(Cmax+2)=O(log n), one has V=Theta(n) and

    k=O(log n * S^4 * (log n)^2).

If a=O((log n)^nu) for a fixed nu<1/2, and S is a fixed power of
log n, every term of (Hyb3) is o(n sqrt(log n)); k^6 is only a fixed
power of log n. The same is true when
`S<=2^((log n)^rho)` for fixed rho<1 and a fixed alpha>1/2 satisfying
rho*alpha<1/2. Indeed log k=O((log n)^rho), k^6=n^o(1), and the
modular and sparse terms are both below the target. Constants may depend
on the fixed choices nu,rho,alpha.

The known low-degree linear spectral predictors have no demonstrated
full-rate guarantee of this kind. The amplitude note's one-hot witness
rules out a small absolute-error budget at its stated ordinary linear
interface, and the earlier sparse supplier gates rule out several fixed
forms. Their combination does not establish a lower bound for every
mixed-error supplier or for arbitrary nonlinear product compositions.
Any such supplier must provide its own deterministic guarantee and paid
cost before (Hyb3) can become a complete multiplication recurrence.

The mechanism uses established sparse interpolation and the classical
Schönhage cyclotomic engine, with references and actual read scope in
the two component notes. This composition makes no priority claim.

## 5. Exact finite controls

The checker `verify_hybrid_residual.py` uses the separately checked
modular-convolution, signed-sparse and positive-certificate engines.
It passes 24 complete signed mixed repairs with height and integer-carry
checks, 24 one-sided attempted repairs (18 accepted and six incomplete),
12 deliberately false outlier budgets, a dense-positive rejection,
both zero-outlier mass outcomes, and both centered half-modulus endpoints.
It also verifies that a signed error M times the square of the fold
annihilator still defeats a false sparse promise after the modular
stage. The JSON pins all three dependency hashes. These are arithmetic
controls, not a simulation of the multitape time invoice.

Prepared for @CubeJerry with substantial ChatGPT assistance.
