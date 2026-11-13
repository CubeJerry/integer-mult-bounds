# Equality projectors and local operator rigidity of the canonical BIT fitting

Author mathematical package with exact finite source witnesses; independent review pending. This proves universal equality-structure facts and canonical local rigidity. It does NOT prove global uniqueness of every rank9V fitting.

## Source, target and permitted consequence

Use the actual111-port rational-chart BIT native, SHA256 `51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78`. This is a distinct graph from the complex96/104 source. Here forbidden offdiagonal blocks are the REAL NONorthogonal root pairs. The already proved parity theorem gives exact minimum fitting rank9V over every characteristic-two field and every V. Canonical K0=J+(v_i dot v_j/2 mod2) has111 diagonal ones and6470 foreign ones, rank9. Integer division precedes reduction.

The complete fixed-even-m caller's current partial nine-packet rail leaves limiting correction allowance11.542006727052... and m4 allowance7.430310278604..., while retaining all6470 foreign coefficients of K0+I. This note grants NO arbitrary saving per removed matrix entry. It asks whether changing a minimum fitting can remove those coefficients; even a successful new fitting would still owe its encoder, actual transport, decoder and all original endpoints. The formal rigidity below shows one natural deformation route cannot remove any foreign block.

## 1. Equality in the nine-frame lower bound gives orthogonal complementary blocks

Let A=CR be ANY fitting of rank9V over any characteristic-two field. Put P_i=R_i C_i. These are rankV idempotents, and P_i P_j=0 in both orders whenever i,j lie in one of the actual eight-clique frames. For the proved nine-frame parity witness define P_f=sum_(i in f)P_i, Q_f=I-P_f. Each Q_f has rankV and sum_f Q_f=I.

Their images E_f span the9V ambient space, and the sum of their nine dimensions is exactly9V. Thus E=sum_f E_f is a DIRECT sum. For x in E_g, the expression x=sum_f Q_f x is its unique decomposition in that direct sum. Therefore Q_g x=x and Q_f x=0 for f!=g. In particular

    Q_f Q_g = delta_fg Q_f.

Choose arbitrary bases of the E_f. In this simultaneous block gauge the Q_f are the nine standard coordinate projections. If source i belongs to frame f, then P_i P_f=P_f P_i=P_i, so Q_f P_i=P_i Q_f=0. Thus its entire f row and column blocks vanish. No symmetry, positivity, scalar-tensor or commutation premise is used.

For the literal witness, roles36 and37 occur in six frames. Consequently their P_i are supported respectively on coordinate triples{4,5,7} and{0,1,3} in the witness frame order, using zero-based indices. These are universal forced supports, not a claim that every further canonical coordinate zero has already been forced. Other roles can have additional canonical zeros that this argument alone does not establish.

The simultaneous Q-frame gauge above and the source-frame gauge below are SEPARATE coordinate choices. They are not assumed simultaneously normalized. No missing canonical coordinate zero is inferred by combining them.

## 2. Exact canonical tangent kernel

Fix the actual first witness frame F=[0,16,17,32,36,38,67,71]. Its identity principal block permits factor gauge C_F=[I8,0], R_F=[I8;0]. The canonical K0 has an explicit symmetric factor K0_ij=x_i dot x_j with x_i in F2^9, x_(F_a)=e_a. Source role1 supplies the ninth pivot. All12321 factor products are checked directly from the rational source; the111 vectors x_i are retained in CERTIFICATE.json.

For i outside F, coordinates a<8 with K0_(i,F_a)=0 are exactly zero in BOTH factors of ANY fitting in this gauge. Every other coordinate is a factor variable; the ninth coordinate is free. There are1120 variables: perturbations delta C_ia and delta R_ia. The111 identity diagonals and5740 forbidden offdiagonals give5851 polynomial constraints. Their linearizations at x are

    delta C_i dot x_j + x_i dot delta R_j = 0

for i=j or a prescribed-zero pair. The exact binary Jacobian has rank1009. A literal1009-by1009 nonsingular minor is identified by its constraint and variable indices; elimination over F2 certifies determinant1.

Its kernel has dimension111. It is EXACTLY the following gauge space. Choose vertex parameters t_i for all111 roles and one complement-coordinate parameter s. In the fixed frame gauge, the perturbations are

    delta C_ia = delta R_ia = x_ia*(t_i+t_(F_a)), a<8;
    delta C_i,last = delta R_i,last = x_i,last*(t_i+s).

All112 generators are checked to lie in the kernel. Their rank is111 and their only relation is the common all-one parameter choice. This is both a lower and upper kernel certificate, not a numerical rank estimate. The source contact graph is connected, so the induced MATRIX fitting tangent space has dimension110: delta K_ij=(t_i+t_j)K0_ij, with only common vertex scalars acting trivially. Exact binary ranks persist under every characteristic-two field extension. The certificate does not assert that all remote solutions lie in this tangent neighbourhood.

## 3. Exact nilpotent operator rigidity, with ordered gauges

Let A be ANY unital associative ring of characteristic two and J a two-sided ideal with J^N=0. Suppose factors C_i in A^(1 by9), R_i in A^(9 by1) satisfy the same fitting diagonal and zero constraints, and reduce modulo J to the canonical scalar vectors x_i times1_A. Coefficients inside A need not commute. Then there exist vertex units U_i in1+J such that

    K_ij=C_i R_j=U_i K0_ij U_j^(-1).

In particular EVERY canonical foreign contact remains a unit; no such block can be removed or made singular by this nilpotent lift. This is a local theorem with a specified canonical reduction, not a theorem about arbitrary A-valued fittings.

First normalize the eight-frame factors exactly. Stack C_F and concatenate R_F; C_F R_F=I8. Put Q=I9-R_F C_F and form D with first eight columns R_F and ninth column Q e_last. Modulo J this is I9, hence D is invertible by a finite geometric series in the nilpotent matrix ideal M9(J). The ordered transform C_i -> C_i D, R_i -> D^(-1) R_i makes C_F=[I8,0], R_F=[I8;0], while leaving K unchanged. The reduction remains canonical.

Assume inductively that the normalized factors equal x_i modulo J^n. Their errors in J^n/J^(n+1) obey exactly the binary linearized equations above: all base coefficients are central bits, and products of two errors lie in J^(2n), contained in J^(n+1) for n>=1. The finite kernel certificate applies with coefficients in the additive F2-vector space J^n/J^(n+1). Choose lifts t_i,s in J^n representing the corresponding gauge parameters.

Let T_i=1+t_i. Perform the vertex transformation C_i -> T_i C_i, R_i -> R_i T_i^(-1), and simultaneously the global factor-basis transformation with

    D_n=diag(T_(F_0)^(-1),...,T_(F_7)^(-1),1+s),
    C_i -> T_i C_i D_n,
    R_i -> D_n^(-1) R_i T_i^(-1).

The eight frame factors stay EXACTLY normalized. Modulo J^(n+1), the added errors are x_ia*(t_i+t_(F_a)) in the first eight coordinates and x_i,last*(t_i+s) in the last; these equal the existing error and cancel in characteristic two. No product order is changed. Thus the new factors equal canonical modulo J^(n+1). Iterate for n=1,...,N-1. The final factors are canonical. Accumulating the vertex units and inverting them gives the displayed ordered formula for the original K. Global factor-basis changes cancel from K at each step.

This also proves all formal operator deformations are vertex gauge. For a characteristic-two field k and any V, let K(t) be a fitting with V-by-V entries in k[[t]], constant term K0 tensor I_V, and rank9V over k((t)). A unit9V minor at t=0 yields a factorization over k[[t]] with9V intermediate coordinates; a constant global basis change makes its reduction the canonical x_i tensor I_V. Apply the induction with A=M_V(k[[t]]), J=tA, successively modulo t^N, and take the t-adic limit. The vertex and global gauge products converge because the n-th correction is I modulo t^n. Therefore

    K_ij(t)=U_i(t) K0_ij U_j(t)^(-1),  U_i(0)=I_V.

All6470 foreign blocks stay invertible as formal matrices. In particular K_ij(t)K_ji(t)=I_V on every allowed contact. Singular or entangled operator coefficients at higher orders do not evade the induction.

A useful exact corollary concerns rational families. If K(t) has entries rational in a CENTRAL parameter t, satisfies the fitting and rank9V conditions generically, is regular at0 and has canonical value there, the inverse-contact identities above hold as rational functions. They consequently hold at EVERY regular specialization, so such a family cannot reach a fitting with a deleted or rank-deficient foreign block. This excludes continuously tuning the canonical fitting to a cheaper foreign-support pattern along a rational one-parameter family. It does not exclude another disconnected component or an isolated extension-field/block solution.

## 4. Verification, limitations and constructive frontier

Run `python3 -I -B verify.py --repo REPO --output OUT`. The verifier authenticates the actual BIT native, reconstructs K0 directly from exact rational source vectors, derives and checks all canonical factor products, constructs the full1120-column Jacobian without a solver, verifies a1009 nonsingular minor, and proves its kernel is spanned by the111-dimensional gauge image. A single factor perturbation changing a required diagonal is rejected. An exact ordered control on an actual contact triangle uses noncommuting units in M2(F2[t]/t^3): the correct vertex order gives the identity cycle, while reversing the order gives a nonidentity cycle. Python -O is rejected before any output is created. The contact graph's connectivity is checked, giving the110-dimensional matrix gauge tangent.

The universal equality lemma uses the independently source-verified nine-frame theorem `bit-minrank-nine/PROOF.md`, SHA256 `669c8441a7f5d65e4c483f2d444160d365f754dbe5789b5588c3c0d6dad7e1cc`. Its frame/parity proof applies to all minimal fittings, even in remote or singular strata. The new local theorem uses only the exact canonical Jacobian/gauge-kernel certificate plus the ordered induction; no solver UNSAT claim is needed. The separate root scalar F2 uniqueness search is not used as a proof premise.

Open: a global algebraic proof that every rank9V fitting is vertex gauge, or an explicit minimum fitting in another component with fewer foreign blocks. Local rigidity does not eliminate those possibilities. The equality projectors alone do not yet force every canonical coordinate zero or every contact to be invertible in an arbitrary minimum fitting. A fitting alternative would still need realizable acquisition and correction within the full caller allowance. The current foreign residual, original endpoint debts and physical maps remain. All erasure/compiler/storage/precision/analytic obligations and both strict suppliers remain. No complete Q or kappa is claimed.

Credit: @CubeJerry programme and retained BIT/native authors; root's canonical fitting, nine-frame lower bound and equality-projector prompt; worker B's exact source Jacobian, gauge-span certificate, noncommuting nilpotent induction and formal/rational-family corollary; OpenAI-assisted mathematical research. Retained predecessor credit is preserved.
