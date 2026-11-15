# Independent review of the one-native rank-two gate

Root accepts the abstract theorem h2<=q for the stated fixed finite Clifford
algebra, retained R independent roles, one native and q one-role queries.
The mathematical argument is independently reviewed; it is not inferred from
running the author's test code.

The pre-native right kernel must kill each query SOURCE (or in-place affected
role) in the ordinary-only reference prefix. Induction then deletes all such
queries simultaneously on that kernel. Reverse-time deletion uses query
DESTINATIONS on the left. The respective codimensions are at most q_pre D and
q_post D. Orthogonal kernel projectors belong to the ordinary matrix algebra
because that finite algebra is *-closed and polynomial functional calculus
of the constraint Gram matrix gives its nullspace projector. These projectors
are proof devices and incur no claimed free physical operation.

The previously proved eventual tensor-independence and ordinary Gaussian-rank
bimodule statements apply to the enlarged fixed finite monomial Clifford
family, with its exact scalar cocycle on every width residue. They justify
projecting the compressed identity. The low-rank native component stays
invertible for all eight sign/orientation choices: its diagonal is B^sigma,
and the surviving cross term is either zero or a triangular identity term.
The endpoint low component has rank (R-h2)D even after invertible ordinary
boundary changes. Sylvester gives (R-q)D on the compressed native side, hence
h2<=q. No old parity character is assumed.

## Separate scalar-C5 obstruction certificate

Root independently derived a different special-case argument before reading
the broad proof. Normalize every scalar-ordinary gate at z=1. The active native
has N=I+(z^sigma-1)P+z^sigma(z^epsilon-1)J, where P has rank2,
J^2=0 and PJ=JP=J. Two one-role query differences have total rank at most2,
regardless of placement, so a three-role endpoint D requires det(D-N)=0.
For a mixed rank-two endpoint write D=dI+(e-d)uv^T, v^T u=1,
{d,e}={z^2,z^3}; put p=v^T Pu, j=v^T Ju, alpha=z^sigma and
beta=z^sigma(z^epsilon-1). Its determinant is

    (d-alpha)^2(d-1)
      +(e-d)[p(d-alpha)(d-1)+beta*j(d-1)+(1-p)(d-alpha)^2].

Reduction modulo z^5-1 gives five linear constraints on p,j. For each of the
eight orientation/multiplicity cases, check.py produces an exact rational
left-kernel vector annihilating both variable coefficients with nonzero
constant residual. Uniform endpoints have determinant
(d-alpha)^2(d-1), nonzero at every nontrivial fifth root. Faithfulness at V>=2
is essential to normalization at every character; a one-column polynomial
identity is insufficient. This special case is independently computed with
SymPy exact rational elimination and does not replace the broader proof.

Three or more queries, multiple native halves, changed retention, width-growing
operator families and arbitrary ordinary maps outside the stated Clifford
bimodule are not excluded. The result supplies no new kappa and discharges
none of the five foundational assumptions. Credit the tensor-component and
ordinary-kernel predecessors, Worker B's new theorem, @CubeJerry and OpenAI
assistance. No independent human or proof-kernel verification is claimed.
