# Recoverable encoders and coordinated common-state modulation

**Universal sufficient-and-necessary algebraic criterion for the stated one-donor interface. No source feasibility or new kappa.** This strictly contains unchanged-q additive modulation and permits a linear common mode instead of a prescribed helper value.

Fix a common encoder cut before any of the considered controls. Its actual
cochart common fields have unperturbed input-row matrix E. Let W_T be the
original common endpoint rows at terminal chart T. All common inputs u are
independent. A raw donor Q=q is at the encoder chart and has funded remaining
routes ending at T. The raw receiver is a distinct field whose collection
route is still unused. Any preparation before this encoder cut is part of
the supplied prefix contract and is charged separately. Define the row subspace

R = row(E) intersect row(W_T).

Fix later control events accessible from that remaining donor route, actual
receiver-history observations, and every source guard. As in the joint-
modulation theorem, A maps control coefficients to off-T endpoint/guard
responses, B maps them to observation responses, and F0 maps original common
inputs to the observations. Observations before the encoder have zero control
response. All matrices refer to the fixed original common chronology.

Choose a row r in R, with r=ell E=lambda W_T. At the encoder execute the actual
cochart additions Q-=ell_i common_i. Thus Q=delta=q-r u. Seed stationary delta
records along its remaining funded itinerary as needed. A control vector c
injects c_j delta at its prescribed events; receiver observations are

F0 u + (B c) delta.

The desired unit-q observation through row d requires exactly

Ac=0, d F0=r in R, d B c=1.

Indeed these equations give d(observations)=r u+delta=q. Conversely a pure q
observation for every independent u,q in this encoder family forces these
same equations by comparing their coefficients. Here neutrality and guards
are part of the stated interface, not inferred from successful decoding.

Let L have columns spanning the annihilator of R: R L=0. The finite-dimensional
double-annihilator identity gives v L=0 iff v belongs to R. Let Z_R span the
left nullspace of F0 L, and K span ker A. Then d F0 belongs to R iff d=t Z_R.
Consequently a channel exists algebraically iff

Z_R B K is nonzero.

Equivalently the rank of the block matrix [[A,0],[B,F0 L]] exceeds
rank(A)+rank(F0 L). The exact excess is rank(Z_R B K), by the same quotient-
image proof as the adjacent additive theorem. This includes empty R and
zero-dimensional kernels, with matrix shapes retained.

For a nonzero entry beta, take d to be the corresponding row of Z_R and c
the corresponding column of K divided by beta. Set r=d F0; solve the two
row representations ell E=r=lambda W_T. The common endpoint response z to
c delta is supported at T. Once Q reaches T, subtract z_i Q from each
affected common endpoint. Then add lambda_i times the RESTORED common
endpoints into Q. It becomes delta+r u=q. No gamma condition is needed.

Receiver observations can be accumulated in one real owned field per used
receiver-itinerary chart. Each weighted observation is read only at its
actual source event. After common execution the raw receiver follows its
still-unused funded route, collects the accumulators and retires them. This
is a physical schedule, not a simultaneous historical oracle.

If there are s donor snapshots, J receiver accumulators, c0 nonzero controls,
d0 nonzero observations, t terminal corrections, e encoder coefficients and
l recovery coefficients, the displayed lowering adds e+c0+d0+s+J+t+l ADDs,
s+J INITs and s+J CLEARs, and no new MOVE. It needs real labels, lifetimes and
storage for those s+J fields. Input difference formation and final recoupling
are additional inherited boundary costs. Fixed coefficients, especially
1/beta, must be admitted and priced; field-linear rank feasibility alone is
not an implementation in a more restrictive coefficient grammar.

R={0} gives the unchanged-q additive theorem: no encoder or recovery terms,
and Z_R is the left nullspace of F0. Restricting r to a single helper row
recovers the earlier difference-carrier search. General R can contain a local
combination even when no individual helper row satisfies the necessary
decoder/recovery conditions. This is a genuine enlargement of the tested
family, not proof that a source witness exists.

For a minimal algebraic strictness check, take A to be the 0-by-1 matrix,
B=[1], F0=[1], E=[1], W_T=[1]. The additive case has zero left nullspace and
no pure-q decoder. With R=span([1]), L has zero columns and Z_R=[1]; the
encoded channel uses delta=q-h, observes h+delta=q, restores h at T and
recovers Q. This check is not an instantiated native route certificate.

The next consequential source test is the exact projected matrix Z_R B K
at a concrete encoder cut, with every E/A/B/F0/W_T row source-authenticated.
A zero result excludes only that fixed encoder/control/observation family.
Joint encodings at several cuts, added geometric access, recoding the common
native itself and other suppliers remain separate possibilities. Prepared
for @CubeJerry by the S004 orchestrator with OpenAI assistance.
