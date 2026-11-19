# The Clifford adjoint and the precise mirrored endpoint contract

**Proved algebraic interface identities. No causal shared decoder or new
kappa.** A transpose exchanges input and output actions; it does not
automatically preserve the receiver-wise covariance of the current source
architecture. This package identifies the correct pairing and the exact
additional endpoint condition for a mirrored covariant construction.

## 1. A pairing fixed by every native Clifford root

Let F be any characteristic-two field. Use the pinned split spinor
S=F^16 with basis e_I indexed by subsets I of four hyperbolic coordinates.
Define J e_I=e_(I complement), so J is symmetric, alternating, invertible
and J squared is I. The creation and annihilation operators in each
coordinate are self-adjoint for the bilinear form

    <u,v>_S = u^T J v.

Indeed a creation at one coordinate pairs complementary remaining
subsets in the same way on either side; the annihilation identity is
identical. Each native gamma(v) is a binary linear combination of these
eight operators. Hence gamma(v)^T J=J gamma(v) for every v.

For a matrix A on S put A dagger=J A^T J. This is an involutive
anti-automorphism: (AB) dagger=B dagger A dagger. In particular every
gamma(v) is self-adjoint. On End(S) use the nondegenerate trace pairing

    <X,Y>_E = Tr(X dagger Y).

Its matrix in row-major matrix-unit coordinates is the 256-coordinate
complement permutation: E_rc pairs with E_(15-r,15-c). Nondegeneracy
does not depend on Tr(I), which vanishes in this characteristic.

## 2. Adjoint of the full covariant source family

For a local plane H, let A_H=Cl(H), a copy of M2(F) acting on S. Write
one full covariant source map as

    F_H(X) = sum_t C_t X e_t,      C_t in A_H.

For a general vector u, write u dagger=u^T J. Directly expanding the
trace shows that the paired adjoint is

    F_H dagger(y) = sum_t C_t dagger y e_t dagger.   (1)

More generally a summand A X u has adjoint y -> A dagger y u dagger.
Equation (1) is an injection whenever F_H is surjective. It uses the
specified nondegenerate pairings; ordinary coordinate transpose is a
different matrix in the original bases.

If L commutes with A_H then F_H(LX)=L F_H(X). Taking paired adjoints
shows that F_H dagger also intertwines L dagger, with the left action on
End(S). Since the commutant is stable under dagger, the whole commuting
algebra is preserved. This gives the correct algebraic source/dual
interface. It does not select any native K port or make an output-frame
inverse causally available.

## 3. A terminal root is in a different algebra

At an output K, the native receiver i lies in K. In contrast, the source
equivariance above concerns roots perpendicular to K. These are distinct
conditions. Suppose a terminal injection is restricted to the adjoint
family (1), and additionally has to intertwine the receiver left action:

    F_K dagger gamma_i = L_(gamma_i) F_K dagger.

Taking adjoints makes this equivalent to F_K L_(gamma_i)=gamma_i F_K.
The sixteen original matrix columns are independent, so the condition
is exactly

    [C_t,gamma_i]=0 for every t.                    (2)

Inside A_K=M2(F), gamma_i=I+N is a non-scalar square-zero Jordan
perturbation. Its centralizer is span{I,gamma_i}, of dimension two.
Consequently the full 64-parameter covariant source-dual family reduces
to 32 parameters under this one receiver condition.

If one and the same injection must intertwine two distinct native roots
of K, those two roots generate A_K and their common centralizer inside
A_K is its scalar centre. All C_t are scalar, leaving sixteen parameters:
F_K(X)=X u and F_K dagger(y)=y u dagger. A receiver-dependent family of
different injections does not satisfy this common-injection hypothesis
and is not excluded. Neither is a more general terminal representation.

This is a precise local restriction, not an impossibility theorem for
K transport. It explains why a full64 source cannot simply be transposed
and declared to satisfy every terminal receiver action.
## 4. Exact two-sided endpoint criterion for a mirrored architecture

Let G carry self-adjoint actions Gamma_i, for example the left gamma_i
actions on End(S)^r with the direct-sum trace pairing. Let B be a block
operator on G^111, with receiver index first. Its paired adjoint satisfies

    (B dagger)_ij = (B_ji) dagger.

Call a block operator receiver-covariant when

    B_ij Gamma_i = Gamma_i B_ij

at every foreign pair. Then **B and B dagger are both receiver-covariant
if and only if every B_ij commutes with both Gamma_i and Gamma_j.**

One direction is immediate. For the other, receiver covariance of
(B dagger)_ji says B_ij dagger Gamma_j=Gamma_j B_ij dagger. Taking the
adjoint and using self-adjointness of Gamma_j yields donor covariance
of B_ij. No matrices are commuted past unrelated factors.

Thus joint donor/receiver commutation is exactly the endpoint contract
for a construction whose algebraic forward and reverse maps are both
required to belong to the receiver-covariant family. This requirement
is additional. The theorem does not claim every native implementation
must meet it, or that every two-sided covariant endpoint has such an
implementation.

The actual prior receiver-only target fails this stronger contract at
two modified row80 blocks. At donors0 and2 its donor commutator ranks
are16 and4 respectively, while receiver commutators vanish. The separate
S028 target review checks this at s=1,4,12, including the former b3840
instance. The new two-sided target repairs that algebraic incompatibility
at the same rank(I+B)=34688; it still owes source and shared-middle gluing.

Purely algebraically rank(I+B dagger)=rank(I+B), since taking an adjoint
is transpose followed by invertible conjugations. Symmetry of the native
foreign mask also preserves the support and foreign-block invertibility.
This rank identity does not supply a physical transposed word for free:
owner directions, source availability, frames, phases and paid movement
must be re-established in any reversed native implementation.

## 5. Verification, limits and next question

`check.py` reconstructs the actual Clifford representation independently
of the source/target author code. It checks all120 native self-adjoint
gamma identities, all64 local coefficient/column adjoints as complete
matrices, and the local centralizer dimensions at K370. Ordinary
transpose differs from the paired adjoint on all64 tested basis maps.
A noncommuting local coefficient and a transpose left/right action
example reject the omitted-intertwiner shortcut.

Run:

```sh
python -B check.py --repo REPOSITORY --out /tmp/clifford-dual-review
```

Expected marker: `PASS_CLIFFORD_DUAL_INTERFACE`. Finite exact identities
authenticate the native coordinate choice; the written linear-algebra
proof establishes the field-general assertions. No finite experiment
is promoted to a physical uniform multiplication theorem.

**Open next question:** pick terminal source-dual injections and actual
early/late frames satisfying the same donor quotients and target equations
as the H-side inverse lifts. The paired adjoint and the repaired endpoint
only make that question well specified. All physical costs, strict
suppliers, whole recursion and five foundational assumptions remain.

Credit @CubeJerry, the native Clifford/source and target packages,
S028 worker C's algebraic bridge and separate target review, and the
orchestrator's repaired target, with substantial OpenAI assistance.
