# A full120 Eisenstein cycle native and its exact physical cubic law

**Proved finite geometric construction and all-input linear native; conditionally scoped caller exclusions. No new κ.** The construction uses all120 root lines of the programme's E8 model, with no owned records, no dirty erasures, no retained public D defect and no fractional coefficients. Its forward physical cross operator has an exact order-three law. Two natural ways to embed it in the existing caller fail the complete optimistic price screen. Consequently this is a verified alternative native and a sharply delimited new caller obligation, not a supplier admission.

## 1. An order-three symmetry of the actual root geometry

Let P be the120 nine-bit vectors of weight3 or7. The existing root convention assigns

- to a weight-three v, the real vector ρ(v) with entries2 on its support and−1 elsewhere;
- to a weight-seven v missing coordinates a<b, the vector3(e_a−e_b).

Every root has squared norm18 and lies in the eight-dimensional sum-zero space. In the orthonormal root frame Z=(7,25,42,52,76,82,97,127), write g_v,i=⟨ρ(v),ρ(Z_i)⟩/18. Thus g_v has norm1 and rational coordinates.

The four pairs (7,11),(28,44),(49,50),(127,191) span four mutually orthogonal A2 planes. Within each pair the root inner product has absolute value1/2. Take the product, in the displayed order, of the two root reflections in each plane. Its matrix E satisfies

\[
E^TE=I_8,\qquad E^2+E+I_8=0.
\]

This follows from the order-three A2 Coxeter rotation on each plane and orthogonal direct sum. Direct exact arithmetic checks each premise and verifies that E permutes the120 root lines. It is the concrete Eisenstein scalar-rotation mechanism, rather than an assumed abstract E8 automorphism.

The induced permutation π of the binary normals extends to the binary linear map T with rows

\[
(47,482,62,458,59,488,213,405,341).
\]

The finite nine-dimensional calculation verifies

\[
TT^T=I_9,\quad T^3=I_9,\quad T^2+T+I_9=J_9,
\tag{1}
\]

where J_9 is the all-ones matrix. Every column of T has weight5. The120 normals split into forty three-cycles. For every v∈P,

\[
v\cdot Tv=v\cdot T^2v=Tv\cdot T^2v=0,
\qquad v+Tv+T^2v=\mathbf1.
\tag{2}
\]

Here the dot product and sums are binary, and **1** denotes511. Equations(1)–(2) are finite exact geometric statements, not conclusions extrapolated from sampled ports. `symmetry.py` constructs the four planes, their real matrix and the entire binary extension; `SYMMETRY.json` records all40 cycles and the canonical real-root signs. Real-root signs do not appear in the scalar port permutation R below.

The external inspiration is the Eisenstein description of E8 in Robert A. Wilson, *An eightfold path to E8*, version29 April2012, §3.3–3.4, especially the fixed-point-free multiplication by a cube root of unity: <https://webspace.maths.qmul.ac.uk/r.a.wilson/pubs_files/E8notes2.pdf>. No unverified classification theorem from that paper is needed for the displayed finite construction.

## 2. A complete literal paired-shear native

For h∈P let L_h=span(h), F_h=h^⊥, with ground0 and Hub F₂⁹. There are four arbitrary public fields per port, initially

\[
X_h=x_h\text{ at }L_h,\quad Y_h=y_h\text{ at }0,
\quad B_h=b_h\text{ at }L_h,\quad D_h=d_h\text{ at }0.
\]

Let (R x)_h=x_{π(h)}. R is an orthogonal permutation of order3. For each h, move D_h from0 to L_π(h), subtract it from B_π(h), then move D_h to F_h. Next move Y_h along the same route and add X_π(h) at the intermediate line. Finally move all X_h and B_h from their own lines to Hub. Every move is a genuine ascent: equation(2) gives L_π(h)⊂F_h. No source is used outside its actual current chart.

At the end the all-input logical equations are exactly

\[
X=x,\qquad Y=y+Rx,\qquad B=b-R^Td,\qquad D=d,
\tag{3}
\]

with X,B at Hub and Y,D at their respective facets. There are no owned fields or implicit helper copies. The word has960 events:240 ADDs with coefficient±1 and720 MOVEs, with profile

\[
Q=240[1]+240[7]+240[8].
\tag{4}
\]

Reversing the literal MOVEs and negating the ADDs produces the exact inverse with the same MOVE price and no owners. `build.py` replays all480 independent formal inputs, every cochart contact and every endpoint. It then replays this literal inverse and checks identity and original charts. Each nontrivial scalar row has exactly two terms and ℓ¹ norm2, so every prefix uses the integer grid; no denominator or nonlinear restoration service is concealed.

The deterministic compressed word has SHA256
`bca2056d98d0759d0c7c61104122160d13e12f099bea0cbe2de4169f9b3eac93`.
A wrong ADD sign, wrong port contact and wrong final facet are rejected. Exact scalar replay establishes equation(3) for every field dimension; it does not alone authenticate the physical column phases.

`phase.py` supplies that separate finite check. It authenticates the retained `clifford_exact.py` and `native_verify.py` engines by SHA, emits signed Gaussian decompositions for all360 distinct source chart maps, and checks each decomposition with the second engine. Their Gaussian ranks are respectively120 each of1,7,8. A deliberately altered global phase is rejected. These one-column operator equalities lift by tensor product to every positive column multiplicity V. Retained engine reuse is explicitly distinguished from a fresh independent mathematical review.

## 3. The physical cross operator really satisfies a cubic law

For a binary normal v, define the unitary Gaussian gate

\[
C_v=\frac{1+i}{2}I+\frac{1-i}{2}X_v,
\qquad C_v^2=X_v,
\]

where X_v is coordinate translation. All C_v commute. For V columns, Q_h=C_h^{⊗V}; let Q be the block-diagonal port operator. Let W=(∏_{j=1}^9 C_{e_j})^{⊗V}, acting identically at every port. In particular W²=X_**1**^{⊗V}. Scalar port matrices such as R are applied once to whole fields, not tensor-powered.

Write S_h and T_h for the actual canonical line and facet charts. The input gauges S_h Q_h⁻¹ and output gauges W Q_h⁻¹ T_h⁻¹ are coordinate monomials, hence Gaussian rank0. `phase.py` verifies all240 actual signed gauge recipes. Applying these ordinary boundary gauges to equation(3) gives the exact physical four-bank map

\[
\begin{aligned}
X'&=B X,\
Y'&=B(Y+RQ^{-1}X),\
U'&=B(U-QR^T V),\
V'&=B V,
\end{aligned}\qquad B=WQ^{-1}.
\tag{5}
\]

Thus the forward cross operator is

\[
N=WQ^{-1}RQ^{-1}.
\]

**Cubic cross theorem.** For every V≥1, N³=W exactly, including its phase.

Indeed, along one three-cycle h,πh,π²h, the product of the three port blocks is

\[
W^3(Q_hQ_{πh}Q_{π^2h})^{-2}
=W^3X_{h+πh+π^2h}^{\otimes V}
=W^3X_{\mathbf1}^{\otimes V}=W.
\]

The second equality uses C_v²=X_v and the third uses equation(2). For the internal kernel A=QR^T one similarly has A³=diag_h(Q_hQ_πhQ_π²h), A⁶=X_**1**^{⊗V} and A¹²=I. `operators.py` verifies the character exponent identities on every port and every one-column binary character; the proof above supplies the unbounded V statement. An arbitrary perturbation of the port permutation fails the cube identity.

**This is a law of N, not of the whole four-bank native.** In equation(5), the reverse cross is−WR^T and the diagonal operator is B; their products and the physical stage adapters remain in the caller. A third power of the native is not silently identified with W, and neither this law nor R³=I supplies centrality across fresh stage bodies.

## 4. The full optimistic budget blocks two immediate embeddings

Put t=199/200. The exact native movement cost is

\[
Q_t=240(1+7^t+8^t)=3803.87439569255\ldots.
\tag{6}
\]

### 4.1 Paying the existing noncentral normalizer

The retained orthogonal-port algebra can be written for any orthogonal R, with A_s=M_s⁻¹(QR^T)M_s and A_s⁻¹=M_s⁻¹(RQ⁻¹)M_s. Taking Λ_s=M_s⁻¹λR^T M_s, where λ²=Q² and λQ⁻¹ is ordinary, gives Λ_sA_s⁻¹=A_sΛ_s⁻¹=M_s⁻¹λQ⁻¹M_s. The resulting paid physical service is Q⁻¹R^TQ on each of two independent banks per native. This algebra does not assume R symmetric or R²=I. Its retained caller endpoints and all other physical duties remain premises, giving the most favorable same-template price screen.

The body-eight wrapper surplus for120 ports is120W_a, where

\[
W_a=2(1+16a)^t+4\sum_{j=1}^{a}(1+8j)^t-4-4\sum_{j=1}^{a-1}(8j)^t.
\]

There are2a native calls. Concavity makes H_a=aW_(a+1)−(a+1)W_a strictly decreasing; exact H_5>0>H_6 proves the global maximum at a=6, not merely the maximum of a finite search. The per-native allowance is

\[
\max_{a\ge1}\frac{120W_a}{2a}
=3974.33236917729\ldots,
\]

leaving only170.4579734847447... for every new expense. Two direct normalizer banks cost240·2^t=478.33932615737..., already excessive.

The stronger retained unitary entropy lemma excludes any joint unitary repair of these two banks with ordinary port entropy o(V), clean zero ancillas, and no productive helper credit. Each row of Q⁻¹R^TQ has exactly4^V equal-magnitude entries, because its sole nonzero port block is C_h⁻¹C_j for distinct h,j. Its entropy is2V. For two independent banks, the normalized full-unitary entropy potential at completion is480V. A Gaussian rank-r call changes the potential by at most rV, and ordinary port mixing changes it by at most its charged entropy C_port(V). Thus

\[
V\sum r+C_{\rm port}(V)\ge480V,
\quad\liminf\sum r\ge480,
\quad\liminf\sum r^t\ge480^t
=465.40927203048\ldots.
\]

This exceeds the entire170.46 allowance. The proof follows the programme's `unitary-normalizer-entropy` group lemma and clean-ancilla argument, with this source's single permutation block replacing the R0 four-entry port row. It does **not** exclude nonunitary arithmetic, altered endpoints, productive helpers, or other callers.

### 4.2 Fixing each full three-dimensional cycle head

A second natural proposal preserves the three orthogonal binary normals of each cycle under stage transport. This makes a common three-head/six-body geometry available, at the expense of replacing body8 by body6. Grant the same caller formula and compatible operators outright. Its per-port surplus would be

\[
W_a(c,b)=2(c+2ab)^t+4\sum_{j=1}^{a}(c+jb)^t-4c^t-4\sum_{j=1}^{a-1}(jb)^t
\]

with c=3,b=6. Subadditivity and a^(t−1)≤1 give, for every a≥1,

\[
\frac{W_a(c,b)}{2a}
\le(2-1/a)c^t+(2^t+2)a^{t-1}b^t
<2c^t+4b^t.
\]

For c=3,b=6 this strict upper bound is29.75308110158..., whereas the native alone costs Q_t/120=31.69895329743... per port. Therefore this explicit same-template common-head proposal fails for all arm counts, even before additional normalizers and ordinary work. This is not a theorem against all ways of exploiting N³=W.

`budget.py` proves the numerical inequalities with rational intervals whose200th powers are checked against exact integer powers. It imports neither floating-point certificates nor the old104-port finite-m penalty. The old caller's finite-m accounting, precision and supplier foundations are not transferred to this new source.

## 5. Status and the next genuine obligation

The package proves a new, exceptionally simple full120 paired-shear source and an exact physical cubic cross law. It pays every source MOVE and requires no owned-rank or D-restoration hypothesis. It also closes the two immediate ways to turn that law into a target-strength caller under their stated scope. These price gates justify stopping those embeddings before extended implementation.

A useful continuation must exploit the whole mixed four-bank map in a genuinely different caller, or produce a changed source/target representation that funds its head transport. Merely citing E8 symmetry, the finite-order port permutation, or the favorable raw invoice is insufficient. No compatible complex supplier, BIT supplier, complete κ=0.005 theorem, or foundational-assumption removal is claimed.

Prepared for @CubeJerry with OpenAI assistance. Worker B constructed the E8 order-three geometry, literal source and cubic cross theorem. The canonical root representation, signed Clifford engines, physical ordinary gauges, short-caller all-arm budget argument and full-unitary entropy lemma retain the programme's predecessor credit. This package is a continuation of the source-interface investigation, not a replacement for the separately active112-port caller programme.
