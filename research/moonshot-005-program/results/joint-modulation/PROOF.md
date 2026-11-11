# Exact criterion for jointly neutral modulation of a common native

**Proved finite-dimensional interface and illustrative typed construction. No source-native channel or new κ is claimed.** This criterion permits controls at different common cuts to cancel jointly. Testing only individually neutral pulses does not establish the condition below.

## 1. Precisely specified data

Fix any characteristic-zero coefficient field F and every admitted positive field volume V. Let u be the arbitrary common input vector and q an unchanged actual raw-main difference field. The physical lowering below uses distinct raw donor and raw receiver carriers, so hoisting the donor does not spend the receiver's reserved route. Choose a finite set of legal control events: at event j add c_jq to the specified live common field, using a real cochart copy of q. Fix a finite list of actual common observations available on a chosen raw receiver's itinerary.

Let c∈F^p be the control coefficients. Define:

- A∈F^(a×p): every off-terminal public endpoint response and every required intermediate guard, including each zero-COPY-destination response;
- B∈F^(m×p): the responses of the m chosen observations;
- F₀∈F^(m×n): their unperturbed rows in **all** common inputs u.

The actual observations are F₀u+(Bc)q. A control vector is neutral outside terminal chart T and respects the recorded guards precisely when Ac=0. It yields a pure unit-q observation through a row d precisely when

\[
dF_0=0,\qquad dBc=1.
\]

These matrices must be authenticated from the actual source cuts and field versions. Equal endpoint algebra does not override an unrecorded source COPY constraint, a dead owned target or a noncochart control.

## 2. Joint feasibility and exact rank identity

Let K have columns forming a basis of ker A. Let Z have rows forming a basis of the left nullspace of F₀. Then the following are equivalent:

1. there exist c,d with Ac=0, dF₀=0 and dBc=1;
2. ZBK is a nonzero matrix;
3. \(\operatorname{rank}\begin{pmatrix}A&0\\B&F_0\end{pmatrix}>\operatorname{rank}A+\operatorname{rank}F_0\).

Indeed c=Kx and d=tZ for some x,t, so the signal is tZBKx. If ZBK has nonzero entry β at row i,column j, choose c=K_j and d=Z_i/β. Conversely a nonzero signal implies ZBK≠0. Division by β is a fixed coefficient obligation, not an uncharged physical operation.

More exactly,

\[
\operatorname{rank}\begin{pmatrix}A&0\\B&F_0\end{pmatrix}
-\operatorname{rank}A-\operatorname{rank}F_0
=\operatorname{rank}(ZBK).
\]

To prove it, quotient the lower output space by im F₀. The block map's rank is rank F₀ plus the rank of the map c↦(Ac,πBc), where π is that quotient. The latter rank is rank A plus the rank of πB restricted to ker A. Since ker Z=im F₀ and K parametrizes ker A, that restricted rank is rank ZBK. This proof includes zero-dimensional kernels and observation spaces.

When the excess is zero, every neutral control c has Bc∈im F₀. Choose v with F₀v=Bc. Then the modulated observations equal F₀(u+vq). For arbitrary common inputs, the modulation can be absorbed into a change of common data. Within this fixed observation/access interface, a decoder cannot identify q from those observations alone. This is not an impossibility theorem for different controls, additional data access, nonlinear source algorithms or integer multiplication.

## 3. Complete physical lowering under the typed interface

The algebra becomes a physical component when each control and observation is supplied at its certified chart/time and the coefficients are admitted. There is a concrete lowering using only existing main MOVE reservations:

1. Form the actual raw difference q with its charged input conversion. Before common execution, advance its donor carrier along its original funded itinerary. At every chart needed by a later control, INIT a fresh owned zero field and ADD q into it. Leave that record stationary. The donor's raw q itself remains unchanged and ends at T.
2. Execute the common native in its original order. At each control event use the actual local q record for the prescribed c_j ADD. Every guard in A vanishes. Retire each q record after its last use.
3. At each observation chart INIT a separate owned zero accumulator. At each actual observation add the weighted field with coefficient d_i. After observations finish, the raw receiver follows its still-unused original itinerary, collects each chart accumulator and CLEARs it. The total addition is q because dF₀=0 and dBc=1. No historical source field is reread.
4. The remaining common endpoint perturbation is supported at T. For each nonzero terminal coefficient z_i, subtract z_iq using the unchanged raw donor at T. All common endpoints are restored. The donor needs no reconstruction, γ condition or temporary recovery field.

Every reserved route is used once. This is an entry schedule and cannot reuse S003 acquisition routes already spent. A control chart must occur on the donor itinerary; an observation chart must occur on the receiver itinerary. Fresh zero-field initialization at such a chart and owned retirement retain the programme's physical contracts.

If there are s donor snapshots, L receiver accumulators, r nonzero control coefficients, d nonzero observation coefficients and t nonzero terminal corrections, this displayed lowering adds r+d+s+L+t ADDs, s+L INITs and s+L CLEARs. This incremental tariff assumes q and the raw receiver difference have already been formed; their input-conversion ADDs are separately charged when not present in the caller's baseline. Final output recoupling is likewise a caller obligation. The lowering adds no MOVE. It declares at most s+L additional labels and lifetimes, with peak at most the native peak+s+L. These are conservative actual costs; direct cochart raw-carrier reads or an ordered receiver schedule can eliminate some records only after their schedules are proved. Ordinary work, storage, precision and erasure remain charged.

All coefficients are fixed by the certificate but may have nontrivial denominators. Exact F-linear validity does not discharge the compiler, precision, uniform-family, supplier or complete-recursion obligations. One recovered raw contribution supplies only its specified receiver increment; the remaining difference-native map is still required.

## 4. Two individually nonneutral pulses can work jointly

Use a strict chart chain A⊂B⊂T. Common H=h, X=x and Y=y begin at A. The native INITs owned P at A, copies H into P, moves P to T, moves H and Y to B, performs Y+=H, moves H to T, moves P down to B, performs Y−=P, CLEARs P, and moves X directly A→T. It ends H=h,Y=y,X=x. The raw donor Q=q follows the original X route A→T; raw receiver R=r follows the original Y route A→B.

After P has reached T and while H is still at A:

- observe `R−=H` at A;
- inject `H+=Q` at A;
- move Q along its funded A→T route and inject `P+=Q` at T;
- resume common; after H reaches B, move R along its funded A→B route and observe `R+=H`;
- finish common and restore H at T by `H−=Q`.

Both Y updates use h+q and cancel. R ends r+q. Every common value and the unchanged donor q is correct. The complete typed word has18 instructions: eight ADDs,eight existing common/raw MOVEs,one INIT and one CLEAR. The baseline native has11 instructions and the two raw reservations add two, so precisely five ADDs are new. No route or owned lifetime is added.

Using only the relevant common-noise column h, the matrices are

\[
A=(1,-1),\quad F_0=\begin{pmatrix}1\\1\end{pmatrix},\quad
B=\begin{pmatrix}0&0\\1&0\end{pmatrix},\quad
K=\begin{pmatrix}1\\1\end{pmatrix},\quad Z=(-1,1).
\]

Thus ZBK=1. The block rank is3 while rank A+rank F₀=2. Either control alone has a trivial neutral kernel because its off-terminal Y response is ±1. The combined pulses are neutral and visible. The verifier includes the zero columns for the other arbitrary common inputs and checks every physical input direction.

This is an illustrative typed network, not the pinned programme native. It proves that the joint criterion is strictly broader than searching individually neutral source cuts and that its lowering can be concrete.

## 5. Verification and next source obligation

`verify.py` uses exact rational ranks and reconstructs the18-instruction illustrative word. It verifies all five independent inputs, route ownership, the original source subsequence, the two raw reservations and unchanged ownership count. Negative controls remove the second compensation pulse, the initial noise-canceling observation and the hub restoration. They fail by explicit symbolic rows. Restricting to either single control gives zero rank excess, and the non-noise-canceling decoder is rejected.

The next source certificate must give actual A,B,F₀, legal control/observation event lists, K,Z or equivalent rank witnesses, a nonzero neutral visible mode, admissible coefficients, the complete physical word and all costs. Zero excess only excludes the specified finite control/observation family. No new κ.

Credit: @CubeJerry's programme; S004 orchestrator for the joint matrix criterion and two-pulse example; bridge worker for the quotient-rank proof, explicit physical tariff and symbolic word verification; independent review is recorded separately. OpenAI assistance disclosed.
