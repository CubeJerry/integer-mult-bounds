# A barrier to compressing the literal predictor's product decomposition

Status: **proved scoped algebraic obstruction, pending independent review**.
This concerns the exact formal dyadic predictor used by the source's
monomial-to-Clifford construction. It is not a lower bound for arbitrary
matrix pencils, Boolean-quotient representations, or tape multiplication.

Source predictor: OpenAI `math@3344da59991ed94f9ba711217b29c1d760badfa6`,
Fourier `build/repair.tex`, integral count interpolation and matrix-root lemma.

## 1. The exact question

Let D<=m be the source prediction degree, beta a binary shift, and P_beta
its multilinear polynomial in the formal query variables q_1,...,q_m.
Suppose over any characteristic-zero extension field it has an exact formal
identity

    P_beta(q)=sum_{a=1}^h product_{r=1}^b ell_{a,r}(q),    (C1)

where every ell is affine-linear and D<=b<=m. Constant factors are allowed.
The source takes b to be the least power of two at least D and builds a
matrix root of dimension b^h. Could a more clever decomposition make h
polynomial in m, removing one exponential from its finite-template budget?

**Theorem C1.** For every integer k with 0<=k<=D/2,

    h >= binom(m,k)/binom(b,k) >= (m/b)^k.                (C2)

Thus for the source b<2D and D=Theta(sqrt(m log m)),

    h >= 2^{Omega(sqrt(m)*(log m)^{3/2})}.                (C3)

The elementary monomial upper bound h<=sum_{r=0}^D binom(m,r) has the
same exponential order. Merely optimizing the sum-of-products decomposition
cannot make this particular Clifford construction singly exponential in m.

## 2. The highest homogeneous part

Put I_j=(1-(-1)^{beta_j}q_j)/2. In the source formula

    P_beta=(-1)^{u-|beta|} sum_{r=0}^D (-2)^r
              [T^r](1+T)^{-u} product_j(1+I_j T),

the only contribution of query degree D uses r=D, the constant term of
(1+T)^{-u}, and D distinct indicators. Its homogeneous part is therefore

    (P_beta)_D = (-1)^{u-|beta|}
                    e_D((-1)^{beta_1}q_1,...,(-1)^{beta_m}q_m), (C4)

because (-2)^D times the highest-degree coefficient of e_D(I) is one.
Here e_D is the elementary symmetric polynomial. Sign changes of variables
preserve every derivative-space dimension, so it suffices to study e_D.

## 3. An elementary inclusion-matrix rank proof

We need the characteristic-zero fact that the incidence matrix from k-subsets
to r-subsets of [m] has full column rank when k<=min(r,m-r). This is a case
of Gottlieb's inclusion-matrix theorem. The following self-contained proof
also makes the characteristic restriction explicit.

Suppose f(x)=sum_{|S|=k}a_S x_S vanishes on every zero-one vector of weight r.
Induct on k. For k=0 the assertion is immediate. For distinct i,j, subtract
the restrictions (x_i,x_j)=(1,0) and (0,1). The resulting homogeneous
degree-(k-1) polynomial in m-2 variables vanishes at weight r-1. Its
coefficients are a_{T union {i}}-a_{T union {j}}. Since

    k-1<=r-1,   k-1<=(m-2)-(r-1),

the induction hypothesis makes them all zero. Adjacent k-subsets therefore
have equal coefficients; exchanging one element at a time connects all
k-subsets, so a_S=a is constant. At weight r,
0=f=a binom(r,k), and characteristic zero gives a=0. This proves full rank.

The square-free derivatives of order k of e_D are

    partial_S e_D = e_{D-k}(variables outside S),  |S|=k.

Their coefficient matrix has entry 1 exactly when the k-set S is disjoint
from a (D-k)-set T. Replace T by its complement, an r=m-D+k set. Then
disjointness becomes inclusion S subseteq [m]\T. The needed inequalities
are k<=r (since D<=m) and k<=m-r=D-k (since 2k<=D). The rank just proved
is binom(m,k). The top homogeneous parts of partial_S P_beta have that
rank by (C4), hence the full derivative space of P_beta has dimension at
least binom(m,k).

## 4. A product has few derivative directions

For one product of b affine forms, every derivative of total order k is a
linear combination of the at most binom(b,k) products obtained by removing
k distinct factors. Repeated differentiation of one affine factor vanishes.
For a sum of h such products, the derivative space consequently has dimension
at most h binom(b,k). Comparison with Section 3 proves the first inequality
of (C2). The second follows term by term from
(m-i)/(b-i)>=m/b for 0<=i<k and m>=b.

Take k=floor(D/2) and b<2D. For sufficiently large m,
D=Theta(sqrt(m log m)) and log(m/(2D))=Theta(log m), proving (C3).
Conversely sum_{r<=D}binom(m,r)<= (D+1)(em/D)^D for D<=m/2, which
gives the matching exponential scale for the simple monomial list.

The source's resulting dimension b^h therefore retains

    log2 log2(b^h) >= Omega(sqrt(m)*(log m)^{3/2}).        (C5)

This is a lower bound on the output size of that specified construction
after an exact product decomposition, not on the smallest possible matrix
representation of the predictor.

## 5. Scope and the changed next obligation

The bound permits arbitrary affine forms and arbitrary characteristic-zero
extension coefficients, rather than only source monomials. It applies to
an exact polynomial identity before specialization. It does not cover:

* another polynomial agreeing with P_beta only modulo q_j^2-1;
* a construction performed only in the chosen odd characteristic;
* a small matrix representation not obtained from the source tensor product
  with one b-dimensional factor for each product term;
* a different predictor or repair architecture.

The distinction matters. Characteristic-zero count factorization gives a
small Boolean-equivalent univariate representation, but its non-dyadic
denominators do not automatically specialize to the required characteristic.
Route C's count-residue obstruction is separate from the formal-polynomial
barrier proved here. Neither obstruction implies a general impossibility.

A stronger quantitative extraction must therefore change the representation
mechanism, find a suitable integral Boolean-quotient lift, or bypass the
finite-characteristic predictor. Collecting/recombining products of the
literal source polynomial cannot remove the dominant exponential layer.

## 6. Prior art, checks, and credit

The derivative-space argument is standard algebraic complexity reasoning;
no novelty is claimed for Gottlieb's rank theorem or for this general
flattening technique. The scoped application to the source predictor and
its compiler budget is the programme's observation.

Primary references: D. H. Gottlieb, *A Certain Class of Incidence Matrices*,
Proc. AMS 17 (1966), 1233--1237,
https://www.math.purdue.edu/~gottlieb/Bibliography/Incidence.pdf ;
M. Blaser, D. Eisenbud, F.-O. Schreyer, *Ulrich complexity* (2017),
https://doi.org/10.1016/j.difgeo.2017.06.001 . The latter explicitly relates
sum-of-products length to tensor-product linearization size; its general
Ulrich complexity is a different, broader minimization problem.

A finite exact checker accompanies this note. It certifies small inclusion
ranks and the top-degree predictor coefficients, and uses a modular-rank
failure to show why the characteristic-zero condition cannot be omitted.
It does not test a full tape algorithm. Credits: the cited sources,
@CubeJerry, and AI-assisted proof/application development.
