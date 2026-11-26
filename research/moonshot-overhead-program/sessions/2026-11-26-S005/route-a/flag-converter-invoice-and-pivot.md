# Flag-converter invoice, external cancellation lead, and portfolio pivot

Status: **proved coordinate identity and charged implementation; no new
global envelope**. Written during S005's second discovery wave.
The accepted RO local compiler remains useful, but scalar Grassmann
cancellation and an address formula do not supply its tape converter.

Pins: programme `62d9d8e917379cb2edc17c9761e12e2345bc01f4`; OpenAI math
`3344da59991ed94f9ba711217b29c1d760badfa6`. Dependencies:
`rowspace-orbit-compiler.md` (RO), route-b's
`critical-template-transfer.md` (CT), and lead's
`rowspace-walsh-rank-gate.md`.

## 1. Prospective complete invoice before implementation

Write a=A f for active address width, V for encoded bit volume, and
I(a) for an admitted interchange supplier per incoming bit. The hoped-for
joint local representation would pay

    T_node <= T_children + V poly(A)
              + V B_entry(A,f) + V B_child(A,f) + V B_exit(A,f).

The local term may absorb polynomially many columnwise GL_A maps and
scalar row combinations, with numerical coefficient arithmetic separate.
A polynomial-loglog conclusion also needs bounded normalized child mass,
error, outer source factors and absolute linear visited space, as in CT.
Changing one layout term never certifies the final theorem.

For fixed-power arity A=a^delta, polynomial A is affordable if delta is
small enough. A converter paid once per node at O(sqrt(a) polylog(a))
is potentially affordable. Its actual generic price from RO is

    B_entry+B_exit = O(poly(A)+a),

which is not. Repeating a converter once per child multiplies its cost
by child volume and must use that child's actual width.

## 2. A constant-density chart isolates the nontrivial operation

For f>=A, on the chart with first A columns invertible, every address is

    X=[C | C Z], C in GL_A(F2), Z in F2^(A by (f-A)).       (FC1)

The canonical rowspace basis is [I | Z]. Orbit conversion here changes
the major order of C and Z, and performs the controlled address map

    (C,Z) <-> (C,CZ).                                     (FC2)

The chart's density is product_(j=1)^A(1-2^(-j))>=9/32. Indeed the
first two factors give 3/8, and the remaining product is at least
1-sum_(j>=3)2^(-j)=3/4. Padding C to all A^2 bits therefore costs only
an absolute volume factor on this chart.

The field-order change has shorter width at most A^2 and is affordable
by elementary interchange. Computing CZ for one record in poly(A) f
bit work only computes a destination address. Delivering all independent
payloads to those destinations remains a separate operation.

Gaussian elimination writes C as polynomially many elementary row
operations. Executing them on long f-A slots with existing suppliers gives

    V poly(A) (1+I(f-A)) (1+log(k+2)) + poly(A,k),         (FC3)

where k is the unchanged global numerical record/address parameter.
The common logarithm and additive setup are the retained packed-XOR
compiler's actual costs, not an interchange counted as a free row add.
For f=A the tail is empty and this controlled operation is the identity.

This recreates the repeated long-width toll. Generic radix conversion
instead costs O(V[poly(A)+Af]). Neither upper bound is a lower bound,
and neither achieves the target. Other ranks and pivot charts also need
a proved assembly; FC1 alone is not an all-input numerical supplier.

## 3. The flag bridge has a dual coordinate change

The transfer route fixes the other ordered rows B, puts U=span(B), and
chooses a basis matrix M_B=[U_basis,C]. Writing x=M_B(alpha,beta)
groups input rowspaces by beta. Walsh output uses dual coordinates
y=M_B^(-T)(gamma,delta). Returning to primal coset coordinates requires

    (alpha',beta')=(M_B^T M_B)^(-1)(gamma,delta).           (FC4)

FC4 is invertible even for degenerate U. Setting output orbit solely
from delta fails without a nondegeneracy/orthogonal-complement hypothesis.
The transfer note gives the all-rank algebra. FC4 is recorded here as
another priced physical delivery, not a free basis calculation.

## 4. Primary literature: cancellation accelerates scalar incidence

Shlomo A. Perles and Omri Weinstein, *A Fast Algorithm for Subspace
Convolution*, arXiv:2611.13134, submitted 2026-11-09:

- <https://arxiv.org/abs/2611.13134>
- Author repository <https://github.com/shlomi-perles/subspace-convolution>
- Inspected revision `f9b0a122432aa18f3ce292fc798437c1b5bc2692`,
  `paper/subspace-convolution.pdf`, sections 1.2.1--1.2.2 and Appendix D;
  `lean/README.md` and `lean/docs/unverified.tex`.

For fixed q, the paper gives O_q(S log S) arithmetic algorithms for
fixed-rank incidence and intersection-invariant Grassmann kernels.
Its positive mechanism is relevant: crossing a hyperplane represents a
subspace by direction B and coset x+B; Fourier transformation in the
coset removes the affine containment condition. It then regroups

    (B,lambda), B<=ker(lambda), into (lambda,B),

and recurses within ker(lambda). Cancellation replaces an addition-only
incidence expansion; counting incidence edges would miss the algorithm.

Three scope checks prevent an unsupported import into S005:

1. Appendix D explicitly uses elimination and sorting to group records,
   charging table size times poly(n) index construction, with ambient
   dimension n. This is not a poly(A) physical converter at ambient
   dimension f. Reported implementation timings exclude index construction.
2. Its scalar input is one independent value per subspace. Our full-rank
   matrix addresses have h(A,A)=|GL_A(F2)| independent values per rowspace.
   Replacing them by an aggregate loses data. Applying the theorem once
   per frame coordinate requires reconciling frame changes across
   incidences; it does not remove the stated arithmetic factor.
3. Even a free framed lift of the stated fixed-rank estimate has
   log S=Theta(A(f-A)) when A<<f. As a full transform bill, this is an
   O(Af) per-record upper estimate, not the required square-root supplier.

The Lean documentation models nonuniform straight-line programs and
explicitly excludes index construction. We read that scope statement;
we did not build its Lean project or claim a verified fixed-tape transfer.
This is a useful cancellation lead, with no automatic binding-invoice gain.

## 5. Portfolio decision and constructive pivot

Retain the rowspace compiler and converter target, without prolonging
the route by counting more incidence edges. The new mechanism includes
whole-row Walsh before choosing a representation: paired-column Bell
encoding sends real Clifford tensor actions to signed permutations at
exactly the original payload dimension.

Its identity and first complete invoice are in
`paired-column-bell-executor.md`. The encoder has a numerical cost:
two half-width Walsh calls have normalized child mass sqrt(2), so this
identity alone is not a faster transform. The next question is whether
the actual source graph lets one encoding persist across enough
operations to erase a repeated physical toll without moving it into
the endpoints or address-dependent scalar masks.
