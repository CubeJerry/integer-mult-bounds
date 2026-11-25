# Why order five appears in the one-converter, two-power word

Status: **proved algebraic classification of the specified local word model;
independent review pending**. This explains and independently checks the
gate in Route C's `ORDER-FIVE-ONE-TRANSFORM-CONVERTER.md`. It is not a
classification of arbitrary converters, arbitrary target powers, or all
finite-field repair algorithms. It supplies no new asymptotic multiplication
envelope by itself.

## 1. Exact model and statement

Let K be a field of characteristic two. Let lambda and mu be distinct
nonzero elements with lambda mu=1, and put tau=lambda+mu. Consider a
symmetric determinant-one matrix

    C = [[a,b],[b,d]],     b != 0,
    a+d=tau,             ad+b^2=1.

The ordered eigenbasis, with first coordinates normalized to one, is

    S = [[1,1],[(lambda+a)/b,(mu+a)/b]].                 (U1)

Every entry of S is nonzero: if a were an eigenvalue, the characteristic
equation would force b=0. Reversing the order of the eigenvalues is allowed
by applying the theorem with their names reversed.

**Theorem U.** There are invertible diagonal matrices A,B,E,D such that

    S = A C B,             Q = E C D C^2,
    Q = [[0,1],[1,0]],                                      (U2)

if and only if lambda has multiplicative order five and

    a=mu^2/tau,       d=lambda^2/tau,       b=tau.         (U3)

The matrices E,D may depend on C. The statement fixes the swap word to
the powers one and two; it does not allow an arbitrary pair of powers.

## 2. One-transform converters alone

Two two-by-two matrices with no zero entries are equivalent under
invertible left and right diagonal scaling exactly when their cross
ratios agree. Necessity follows by cancellation of the four diagonal
factors. For sufficiency, scale the first row to match and then scale
the second row to match its first entry; the cross ratio forces the
last entry. Consequently U1 is diagonally equivalent to C exactly when

    ad/b^2 = (mu+a)/(lambda+a).                         (U4)

Using ad=b^2+1, this is a=lambda+tau b^2. Substitute into
b^2=a(tau+a)+1, cancel the nonzero b^2, and obtain

    b^2=(tau^2+1)/tau^2,
    a=mu^2/tau,           d=lambda^2/tau.              (U5)

Conversely, these identities give trace tau, determinant one and U4,
whenever the indicated nonzero b exists in K. The entries a,d are
nonzero. The only excluded trace is tau=1, where U5 would force b=0.
In particular the nontrivial reciprocal order-three eigenvalues have
tau=1 and admit no such converter with b nonzero. Other eigenvalue
orders can satisfy U5; the one-transform converter alone does not force
order five.

The same derivation over an arbitrary characteristic, with
Delta=lambda-mu, gives

    a=-mu^2/Delta,   d=lambda^2/Delta,
    b^2=-(1+Delta^2)/Delta^2.

Only the characteristic-two specialization is used below.

## 3. The two-power swap word

Write D=diag(s,t). Cayley-Hamilton gives C^2=tau C+I. The two diagonal
entries of C D C^2 vanish exactly when

    [[a(tau a+1), tau b^2],
     [tau b^2, d(tau d+1)]] [s,t]^T = 0.              (U6)

The off-diagonal coefficients tau b^2 are nonzero. A singular matrix
in U6 therefore has a one-dimensional kernel whose nonzero vectors
have both coordinates nonzero. Such a vector gives an invertible D;
then C D C^2 is invertible with zero diagonal, so both off-diagonal
entries are nonzero and an invertible diagonal E scales them to one.
Thus existence of E,D is equivalent to vanishing of the determinant
in U6. Direct simplification using a+d=tau and ad+b^2=1 gives

    det(U6) = 1+b^2(tau^2+1).                          (U7)

Combine U5 and U7. The resulting condition is

    tau^4+tau^2+1 = (tau^2+tau+1)^2 = 0.

In a field this is equivalent to tau^2+tau+1=0. Multiplying that
equation, with tau=lambda+lambda^-1, by lambda^2 gives

    lambda^4+lambda^3+lambda^2+lambda+1=0.

Multiplication by lambda+1 shows lambda^5=1. Lambda cannot be one
because lambda and mu are distinct, so its order is exactly five.
Conversely order five gives this equation and hence U7=0. Moreover
U5 now says b^2=tau^2, so b=tau in characteristic two. This proves U.

## 4. Concrete F16 instance and scope

Use K=F2[alpha]/(alpha^4+alpha+1), with the coefficient-vector encoding
used in Route C. Lambda=alpha^3 has encoding 8; mu=15 and tau=7.
Then U3 gives C=[[9,7],[7,14]], precisely Route C's gate. Its explicit
diagonals realize U2 with a column-rescaled eigenbasis. Rescaling
eigenvectors does not change diagonal equivalence.

The accompanying exact verifier enumerates every nonzero lambda other
than one in F16 and every symmetric, nontrivial C of determinant one
with its reciprocal eigenvalues. It checks U4/U5, enumerates all
invertible diagonal D for the swap word, and compares simultaneous
solutions with U3/order five. It also checks the actual displayed Route C
matrices. Negative controls include the order-three gate and the false
claim that one-converter existence alone forces order five.

Finite enumeration checks the implementation and constants; the field-
universal argument is the proof in Sections 2--3. A different word
E C^r D C^s is outside the theorem. A nonsymmetric gate, a larger
block, or more general pointwise/row conversions is outside it too.
The result therefore does not exclude a better finite repair mechanism.

Credits: Jerry Chen (@CubeJerry); Route C's E003 finite gate and repair
construction; the pinned OpenAI repair/shared-pencil interfaces; the
programme's earlier characteristic-two construction; substantial
AI-assisted derivation and review. No priority or formal-kernel claim.
