# All-width capacity bounds for decomposable canonical quotients

**Author theorem; independent review pending. No new kappa.**

This extends the frozen width-two, three-generator theorem. Scalar
directions may now be dependent, and the value width is arbitrary. The
result concerns algebraic fittings, not physically available histories.

## 1. Setup and statements

Let C be the native111-port canonical code over a characteristic-two field,
and A a width-V fitting with identity diagonal and native forbidden zeros.
Put E=(row(A)+C tensor k^V)/(C tensor k^V). Suppose after a field extension
L/k it has a basis h_a tensor v_a, 1<=a<=r=dim E, with nonzero scalar
quotient directions h_a and nonzero value rows v_a in L^V. The h_a need
not be scalar-linearly independent. Write S=222-ell(A).

**Theorem A.** If V>=2 and r<=V+1, then

    S<=floor(17r/V).

If r<V, the stronger S=0 holds. This class cannot supply the28 savings
needed for ell<=194.

**Theorem B.** If r>=V, every V value rows v_a are independent, and r<2V,
then again S<=floor(17r/V). In this MDS value-row class, a target fitting
therefore requires r>=ceil(28V/17), within the stated r<2V range. This is
necessary, not sufficient, and is not a physical packet bound.

Both theorems retain native rigidity C intersect L^{J_i}=span(K_i), own
coefficient one, and the established one-direction scalar cap: every
fitting in C+span(h) has ell>=205 over every characteristic-two extension.
The new rank arguments hold over arbitrary fields; characteristic two
enters through those native dependencies.

## 2. Scalar projection and weighted charging

For a nonzero value column x, contract E against x. If the scalar image has
dimension at most one, choose f with f(x)=1 and set F_ij=f(A_ij x). This is
a support-dominated scalar fitting, so S<=17. If the scalar image is zero,
S=0. In particular a value-row span of dimension less than V permits no
whole-block saving.

At a receiver, write A_ij=B_ij+sum_a h_a(j) M_a, where every scalar entry of
B is a word in C and M_a=m_a v_a has rank at most one. At a row deleting a
canonical contact, I belongs to T=span{M_a}: any matrix functional
annihilating T gives a local canonical scalar row K_i times its own value;
the deleted contact forces that own value tozero. Duality gives I in T.

If the active M_a are independent, dual matrix functionals extract local
representatives h_a^(i). Subtract their own coefficients times K_i. The
representatives are now own-zero, and rigidity gives

    A_ij=K_ij I+sum_active h_a^(i)(j) M_a.

At every deleted contact, the same unique coefficient tuple satisfies
sum_a [h_a^(i)(j)/K_ij] M_a=-I. At least V coefficients are nonzero, since
fewer than V rank-one terms cannot have rank V. For each nonzero coefficient
t_a, the row K_i-h_a^(i)/t_a is in C+span(h_a) and supported inside A_i.

Thus, whenever active matrices are independent at every saving row, every
saving w_i=2-ell_i(A) is charged to at least V of the r fixed global scalar
codes. Complete each scalar fitting with canonical rows where it is not
charged. Each saves at most17, so

    V*S<=17r.                                           (1)

This is weighted: a two-unit saving contributes two to each qualifying
code. No scalar independence of the h_a was used in the functional
extraction, and no common receiver coefficients are required.
The codes are indexed by basis tensors; coincident scalar codes are counted
with multiplicity on both sides of this inequality. This supplies a valid
upper bound, not additional independent physical resources.

## 3. A rank-one dependence inequality

Suppose identity lies in the span of a active rank-one matrices m_b v_b.
The full left vectors and the full value rows both span dimension V,
otherwise every matrix combination has a proper image or a common kernel.
In a minimal dependent subset of size c, absorb its nonzero coefficients
into the left columns of X, and let Y have the corresponding value rows.
Then XY=0 and rank X+rank Y<=c, because image(Y) lies in kernel(X).
Adding the other a-c columns/rows must complete both full spans. Hence

    V<=rank X+a-c, V<=rank Y+a-c,
    c<=2(a-V)<=2(r-V).                                  (2)

No spectral or characteristic-zero theorem is involved.

## 4. Proof of Theorem A

Assume the value rows span V. If their lines are pairwise distinct and
r<=V+1, equation(2) forces a minimal dependence to have size at most two.
An active matrix is nonzero, and proportional nonzero rank-one matrices
have the same value-row line. Both sizes one and two are impossible.
The active matrices are independent and(1) applies.

If a value line repeats, a spanning family with r<=V+1 necessarily has
r=V+1, exactly V distinct basis lines, one repeated twice and V-1 occurring
once. Otherwise its span is smaller than V. Since V>=2, a singleton line
exists. A dual value column isolating it gives a scalar contraction of
dimension one, so S<=17<=floor(17r/V). This separate projection argument
is necessary: active-matrix independence can fail for repeated lines.

For r=V+1 the cap is17+floor(17/V). The ell floors are197,200,201,202,203,
204,205 at widths2,3,4,5,6--8,9--17,18 and above, respectively. At V>=18
the prior general quotient-density theorem already excludes r=V+1 from
the28-savings target; the new target force is especially relevant at
widths2 through17. The mathematical all-width statement remains valid.

## 5. Proof of Theorem B

In a nontrivial active dependence, c>=V+1: if c<=V, the MDS value rows
give Y full row rank, so XY=0 forces X=0. If c>=V+1, rank Y=V and
rank X<=c-V. Including the other a-c left columns, the total left span
has dimension at most(c-V)+(a-c)=a-V<=r-V<V. This contradicts identity
belonging to the active matrix span. Thus all active matrices are
independent and(1) proves the theorem.

The first small arithmetic case not excluded is V=3,r=5: five scalar
capacities give85 units while28 savings require84. This identifies a
strongly constrained possible construction, not its existence. Scalar
near-extremizers, their receiver overlap, local access and complete
physical costs still have to compose.

## 6. Controls and precise limits

For V=3,r=4 with repeated value line e0, the active matrices P0,P0,P1,P2
are dependent and span identity. Theorem A handles this by singleton
projection, not an incorrect independence assertion.

At the strict MDS boundary V=2,r=4 over F4, take value rows
(1,0),(0,1),(1,1),(1,alpha), alpha^2+alpha+1=0, and left columns
(1,0),(0,1),(alpha+1,alpha),(alpha,alpha). Their four rank-one matrices
sum tozero, while the first two sum to identity. Every pair of value rows
is independent. Thus active independence can fail at r=2V; no extension
of that argument is claimed there.

The checker exhausts V=3,r=4 binary left-column choices for both an MDS
and a non-MDS family, and all4096 right inverses of a V=3,r=5 MDS value
matrix over F4. Exact near-width right-inverse controls cover additional
widths. Source-bound controls extend the prior nontriangularizable native
example to V=2,3,4,8,17 by adding one scalar pure tensor in each extra value
channel. Their actual quotients are V+1 and ell216. The scalar modes become
dependent as V grows, exercising the newly allowed case. The sum of their
scalar charge witnesses equals V times the six actual saving units. These
are algebraic controls, not physical implementations or sharpness claims.

Field extension preserves the native ranks and block zeros. The theorem
therefore applies to the original fitting, but does not implement the
extension-field scalar reductions as an algorithm. No new supplier,
chronological source, precision/erasure service, complete caller invoice,
or foundational discharge is proved. No new kappa.

Prepared for @CubeJerry with OpenAI assistance. Credit native/scalar-cap
predecessors, the frozen decomposable quotient-three package, and the
root's independent Sylvester review and proof feedback.
