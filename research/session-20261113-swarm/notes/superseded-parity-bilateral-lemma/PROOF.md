# A bilateral radial half-unit bound from total parity

Scoped precision lemma; no global attaining construction and no forward-only
unrestricted lower bound. Prepared with substantial OpenAI Codex assistance,
Apache-2.0. The candidate witness family and bilateral question were supplied
by the current CubeJerry workstream; this proof checks the complete local
minimum independently. No standalone PR is proposed before review.

## Statement

Let U=H4/2, where
H4=((1,1,1,1),(1,-1,1,-1),(1,1,-1,-1),(1,-1,-1,1)), and let
pi(v)=sum_i v_i mod2 on Z^4. Suppose a total map F:Z^4→Z^4 satisfies

||F(x)-Ux||<=1 and pi(F(x))=pi(x) for every x.

Then, without requiring injectivity,

sup_x | ||F(x)||-||x|| | >=1/2.

More precisely, for every integer a>=2, at x_a=(2a,1,1,1) put
n=4a^2+3 and m=n-2a+4. The exact minimum over every parity-preserving
error-one output y at this input is

mu_a=sqrt(n)-sqrt(m).

The sequence mu_a starts at mu_2=0, is strictly increasing, and tends to1/2.
This is a sharp local minimum on this family, not a globally sharp constant.

If F is bijective, define Delta_+(F)=sup_x(||F(x)||-||x||). Then

max(Delta_+(F),Delta_+(F^-1))
 =sup_x | ||F(x)||-||x|| | >=1/2.

The conclusion is bilateral: it does not specify which direction has that
outward slack. No claim Delta_+(F)>=1/2 alone is made.

## Complete candidate enumeration and norms

Ux_a=(a+3/2,a-1/2,a-1/2,a-1/2).
Every integer point within distance1 chooses one of the two nearest integers
in each coordinate. Each of these16 corners has squared error exactly1.
Any other integer point has squared error at least(3/2)^2+3(1/2)^2=3>1.

Write the corner as

y=(a+1+b,a-1+c1,a-1+c2,a-1+c3), b,c_i∈{0,1}, k=c1+c2+c3.

Its coordinate sum is4a-2+b+k, whereas pi(x_a)=1. Parity preservation is
therefore exactly b+k odd. This leaves all eight permitted corners:

| b | k | Squared output norm | Multiplicity |
|---:|---:|---|---:|
|0|1|n-2a|3|
|1|0|n-2a+4|1|
|0|3|n+2a-2|1|
|1|2|n+2a+2|3|

For a>=2 these four squared norms are strictly ordered, with
n-2a<n-2a+4<=n<n+2a-2<n+2a+2.
Among inward choices the closest radius is sqrt(m). Among outward choices
the closest is sqrt(l), where l=n+2a-2. It remains to compare their gaps;
discarding this comparison would not justify the claimed minimum.

We have m+l=2n+2, n-1>0, and

m*l-(n-1)^2=3(2a+1)^2>0.

Thus sqrt(m*l)>n-1 and
(sqrt(m)+sqrt(l))^2=2n+2+2sqrt(m*l)>4n.
Consequently

sqrt(n)-sqrt(m)<sqrt(l)-sqrt(n).

The exact minimum is mu_a and its unique corner is
y_a=(a+2,a-1,a-1,a-1). This corner has odd total parity and exact error1.
At a=2 it is x_a itself, so the zero endpoint is essential.

## Monotonicity, limit and the total-map bound

For real a>=2 set m=4a^2-2a+7 and n=4a^2+3. The derivative is

mu'(a)=4a/sqrt(n)-(4a-1)/sqrt(m).

Both compared terms are positive. Squaring preserves their ordering, and

16a^2*m-(4a-1)^2*n=60a^2+24a-3>0.

Hence mu is strictly increasing on this interval. Rationalization gives

mu_a=(2a-4)/(sqrt(4a^2+3)+sqrt(4a^2-2a+7)) →1/2.

Every admissible F must choose one of the eight corners at every x_a, so
its absolute radial change there is at least mu_a. Taking the supremum
over these integer inputs yields the bound1/2. No finite sample or monotone
sequence of unverified optima is used: the exact local minimum and its
limit have been proved for all a.

## Bijections, inverse direction and Gaussian-pair transfer

For y=F(x), bijectivity gives
||F^-1(y)||-||y||=||x||-||F(x)||.
Taking suprema proves the displayed bilateral identity, including in the
extended-real case. Also U^T=U and U^2=I, so

||F^-1(y)-Uy||=||Ux-F(x)||<=1.

The inverse preserves parity as well. These facts do not turn the absolute
radial bound into a bound for the forward direction alone. At the minimizing
local edge x_a→y_a, a>2, the forward radial change is -mu_a; its inverse
change is +mu_a. This is a local direction control, not a complete bijection.

In real coordinates for the Gaussian pair, the frozen R5 proof verifies
H4=L(2C_+)R with signed permutations
R(a,b,c,d)=(a,-b,c,d), L(a,b,c,d)=(a,c,-d,b).
Every signed permutation preserves total coordinate parity modulo2, as
well as norms, the integer lattice and Euclidean error. Hence the theorem
transfers to a C_+ rounder under the corresponding parity premise, and by
conjugation to C_-. Ali Romman's #6509 exact-sum bijection satisfies that
parity premise, so the class is nonempty. This note supplies no new global
rounder or physical implementation, and does not establish attainability1/2.

## Why the parity premise matters to this local argument

Without parity, the other eight nearest corners are available. In particular
v_a=(a+1,a,a,a-1) has even total parity, exact error1 and squared norm n-1.
For a>=3, n-1>m, so its absolute radial gap is strictly less than mu_a and
tends to zero. The previous gate's escape
w_a=(a+2,a,a-1,a-1) likewise flips parity, has squared norm n+3 and exact
error1. Its radial gap gamma_a=sqrt(n+3)-sqrt(n) tends to zero; it is smaller
than mu_a for a>=4. Indeed m+(n+3)=2n-2a+7<2n for a>=4, and strict
concavity of the square root gives sqrt(m)+sqrt(n+3)<2sqrt(n).

These are necessity controls for the pointwise witness proof. They are not
global counterexamples to an unrestricted bilateral bound and do not settle
the unrestricted forward outward infimum. The frozen unrestricted R5 Hall
lower bound sqrt21-sqrt19 is unchanged.

## Source scope and credit

#6509 at a4173e810c4d34a1d13b9745af123ad0ec6cfed5 constructs a much narrower
exact-sum reversible nearest Gaussian rounder. Its proof gives no stated
parity-only bilateral radial half-unit theorem. #6619 at
eaa967e7e8aa12cc53ec246a5fc00c5f8873a50b classifies rational orthogonal maps
under injectivity and norm nonincrease, crediting ywz65's #2589 finite-ball
argument. Those premises and conclusion differ: the local proof here needs
neither injectivity nor norm nonincrease, but requires total parity.

Exact proof pins and bounded novelty-query metadata are in SOURCES.json.
The source check is bounded, not a universal priority claim. No period,
conserved sum, equivariance of F, attaining construction, selected native
caller, precision/tape rate or new kappa is claimed. The five framework
assumptions and selected frontier are unchanged. All prior Gaussian,
finite-ball, R5, pairing and compiler notices retain their credit.
