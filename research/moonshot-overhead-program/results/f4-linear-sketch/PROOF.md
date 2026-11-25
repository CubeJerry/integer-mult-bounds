# Additive-sketch obstruction for the order-three target over F4

Status: **accepted scoped theorem; independently reviewed and replayed by Route A**. See `routes/A/review-f4-linear-sketch.md` relative to the programme root. The proof
allows every F2-linear sketch, including entries involving both X_j and
X_j^2. It is a restriction on a specific predictor interface, not a lower
bound for arbitrary matrix representations or integer multiplication.

Let F4={0,1,omega,omega^2}, omega^2+omega+1=0. Let X_1,...,X_m be
independent and uniform on F4*, and put Z=product_j X_j. A predictor sees
only A(X), where A:F4^m -> F4^r is additive (equivalently F2-linear), and
may apply any nonlinear readout. Let k=rank_F2(A). No cost or polynomial
degree restriction is imposed on the readout.

## 1. Exact character energy

Let zeta be a complex primitive cube root, chi(omega)=zeta, and
psi(a)=(-1)^Tr_(F4/F2)(a). On the image group G=im(A), of size M=2^k,
define the complex signed fiber measure

    g(y)=E[chi(Z) 1_(A(X)=y)],  Delta=sum_(y in G) |g(y)|.

Every character t of G pulls back under A to a unique additive character
of F4^m, and hence has the form product_j psi(c_j(t)X_j). Nondegeneracy
of the trace pairing gives this expression even when A is not F4-linear.
For c=0, E_(X uniform F4*) chi(X)=0. For c!=0, the change Y=cX gives

    E chi(X) psi(cX)=chi(c)^(-1) E chi(Y) psi(Y).

Since Tr(1)=0 and Tr(omega)=Tr(omega^2)=1, the latter Gauss sum is
(1-zeta-zeta^2)/3=2/3. Thus its magnitude is exactly 2/3. Let N(A) be the
number of characters t of G for which all c_j(t) are nonzero. For m>=1,
the trivial character is excluded and N(A)<=M-1. Independence, Parseval
and Cauchy-Schwarz give

    Delta^2 <= M sum_y |g(y)|^2
            =sum_t |ghat(t)|^2
            =N(A) (4/9)^m
            <=(2^k-1)(4/9)^m.                         (F4-1)

Only the first inequality is generally strict. The Fourier energy identity
is exact. Codomain dimension r yields the weaker bound with 2^k<=4^r.

For any readout h:G->F4*, the root-of-unity equality indicator gives

    Pr[h(A(X))=Z]
       =1/3+(2/3) Re sum_y chi(h(y))^(-1) g(y)
       <=1/3+(2/3) Delta.                             (F4-2)

Outputs outside F4* can be replaced by any nonzero value without reducing
exact agreement, so this also bounds arbitrary scalar readouts. If the
error is at most delta<2/3, put alpha=1-3delta/2>0. Equations F4-1--2 imply

    k ln 2 >= 2m ln(3/2)+2 ln(alpha),                 (F4-3)
    r ln 4 >= 2m ln(3/2)+2 ln(alpha).

Consequently any constant-error predictor of this form needs Omega(m)
additive bits, or Omega(m) F4-valued summaries. This is a necessary bound,
not a matching characterization for approximate recovery.

## 2. Exact recovery requires injectivity

Suppose A has a nonzero additive-kernel vector v. For every v_i=0 choose
u_i arbitrarily in F4*. For every v_i!=0 choose u_i in F4* excluding v_i.
Then both u_i and u_i+v_i are nonzero, and

    (u_i+v_i)/u_i = 1+v_i/u_i

can independently equal either omega or omega^2. Because v has nonempty
support, two choices differing at one such coordinate give different
product ratios. At least one choice therefore has product ratio !=1.
It gives u,u+v in (F4*)^m with equal sketches and unequal targets. No
readout can recover Z exactly on both. Hence

    exact recovery on every input <=> ker A={0},
    necessarily k=2m and r>=m.                       (F4-4)

Injectivity is also sufficient by inverting the sketch on its image.
The proof uses additivity only. In particular the presence of Frobenius
terms X_j^2 does not avoid the obstruction.

## 3. Affine matrix-pencil consequence and scope

Consider a depth-D product of R-square affine pencils over a finite
F4-algebra E of vector-space dimension e, with queries X_j and X_j^2.
After expanding each coefficient in the explicit E basis, all variable
entries depend on at most e D R^2 F4-valued additive summaries. Fixed
scalar row maps do not add input-dependent summaries. Any output entry
is some function of this sketch. For a full-rate row to agree with the
scalar target on arbitrary independent row inputs, its diagonal entry
must agree with Z; off-diagonal terms can only impose further conditions.
Thus a constant-error family must satisfy

    e D R^2 ln 4 >= 2m ln(3/2)+O_delta(1).             (F4-5)

For D=O(sqrt m), this gives R=Omega(m^(1/4)/sqrt e). It excludes scalar
bounded-algebra-width predictors with that depth, but permits polynomial
matrix width and therefore does not refute a compact full-rate family.
For rectangular varying-width programs the same reasoning bounds the
sum of the actual affine entry counts instead of D R^2.

Multiplicative coordinate shifts, inversion of individual nonzero
coordinates, and fixed target phases permute the uniform domain and
preserve the character argument. Inversion on F4* equals squaring, hence
is itself additive on F4. Arbitrary nonnegative averages of separately
bounded row predictors obey the same success bound. Therefore a claimed
worst-frequency full-row guarantee stronger than this averaged bound must
fail at some frequency. No independence of different predictors' errors
is assumed.

The theorem concerns additive summaries of the independent order-three
eigenvalues. It does not exclude nonlinear summaries, high-width pencils,
general many-stage representations, or another multiplication algorithm.
It does not turn a low rank in physical address space into a cheap repair
map. The actual fixed-F4 construction and its large generic representation
remain consistent with every bound here.

## 4. Verification and provenance

The adjacent checker enumerates exact F4 fibers and computes squared
complex norms as integers in Z[zeta]. It verifies the exact Parseval
energy, the success upper bound, additive rank and explicit kernel
collisions. No floating-point approximation is needed. The finite cases
support the proof and are not its all-size justification.

The lead derived the F4 character and collision arguments. Route A
independently checked their constants and supplied the extension from
F4-linear to all F2-linear sketches, which is needed for pencils containing
both query powers. This is AI-assisted mathematics, not formal kernel
certification or an exhaustive literature/priority claim.
