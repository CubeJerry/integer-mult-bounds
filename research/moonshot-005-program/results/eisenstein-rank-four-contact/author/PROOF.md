# A rank-four Eisenstein quotient and its unavoidable real-contact debt

**Status: proved finite geometry and universal phase-selection obstruction. No new kappa.** This package does not construct a physical Hermitian native, prove a movement lower bound, or complete a caller.

## Pinned input and provenance

The sole source geometry is `research/moonshot-005-program/results/eisenstein-cycle-native/author/SYMMETRY.json` at programme commit `12b269a98e461ebf5e83e24cc16765540bec9626`, Git blob `8b0fc7779990f0a3ad15494af97f082be3592944`, SHA-256 `ffe061f5986a5982a18fca2ff479447db06cf22b5a8db6bd305c8de3c11315cf`. It supplies the already proved order-three real E8 isometry E and its forty cycles on the 120 real root lines.

This is newly reconstructed and actually re-executed exact JavaScript evidence after loss of the local executor. It is not an assertion that the earlier unpublished Python geometry files were recovered. The supplied JavaScript uses only bounded integers in its mathematical checks; its largest intermediates are far below the exact-integer limit of binary64. It checks this one complete finite geometry. The universal statement about all \(3^{40}\) phase selections follows from the proof below, not from enumerating them.

The Eisenstein interpretation is classical: Robert A. Wilson, *An eightfold path to E8*, 29 April 2012, Sections 3.3–3.4, https://webspace.maths.qmul.ac.uk/r.a.wilson/pubs_files/E8notes2.pdf; M. Waegell and P. K. Aravind, *The Penrose dodecahedron and the Witting polytope are identical in CP3*, https://arxiv.org/abs/1701.06512. The generalized-quadrangle connection appears in S. G. Hoggar, *A complex polytope as generalized quadrangle*, DOI https://doi.org/10.1017/S0308210500015754. Those references motivate the search; every numerical incidence and matrix identity asserted here is independently recoverable from the pinned input and supplied checker.

Prepared for @CubeJerry with predecessor credits preserved and OpenAI assistance.

## 1. Exact rank-four form

The 120 binary normals are the nine-bit vectors of weight three or seven. Put
\[
 \rho(v)_i=2 \text{ on the support of a weight-three }v,\qquad
 \rho(v)_i=-1 \text{ elsewhere}.
\]
For a weight-seven vector whose missing coordinates are \(a<b\), put
\(\rho(v)=3(e_a-e_b)\).
All these vectors have squared norm 18 and sum of coordinates zero. Let
\(Z=(7,25,42,52,76,82,97,127)\) be the pinned orthogonal eight-root frame and put
\[
 p_v=\bigl(\langle \rho(v),\rho(z)\rangle/9\bigr)_{z\in Z}\in\mathbb Z^8.
\]
The old unit Gram coordinates are \(g_v=p_v/2\).

Let \(S=2E+I\). The exact pinned matrix gives
\[
 S^T=-S,\qquad S^2=-3I.
\]
For one representative from each of the forty E-cycles define the integer matrices
\[
 A_{vw}=p_v^Tp_w,\qquad C_{vw}=p_v^TSp_w.
\]
Over \(K=\mathbb Q(\theta)\), \(\theta^2=-3\), define
\[
 H=A/4+\theta C/12.
\]
This is Hermitian for \(\bar\theta=-\theta\). Every diagonal entry is one.

For the canonical cycle representatives the exact checker proves, entry by entry,
\[
 3A^2-C^2=120A,\qquad AC+CA=40C.
\]
Consequently \(H^2=10H\). Since \(\operatorname{tr}H=40\) and characteristic zero makes \(x(x-10)\) square-free, \(H\) is diagonalizable with four nonzero eigenvalues, all 10. Thus
\[
 \operatorname{rank}_K H=4.
\]
Changing a representative within its E-cycle multiplies its complex root by a unit, possibly with the real root's canonical sign. This diagonally conjugates H, so rank four holds for every choice of one representative per cycle. Equivalently, \(S/\sqrt3\) is an orthogonal complex structure on the eight-dimensional real span, making it four-dimensional over \(\mathbb C\).

The separate rational matrices A and C both have rank eight for the canonical section. Upper bounds follow from their eight-coordinate factorizations; the checker obtains rank-eight lower bounds modulo 101, hence over \(\mathbb Q\). No assertion of rational rank eight for every possible section is needed.

## 2. What rank four costs at the old physical contacts

For distinct normals \(v,w\), the exact root list gives
\[
 \langle g_v,g_w\rangle=0
 \quad\Longleftrightarrow\quad v\cdot w=1 \text{ in }\mathbb F_2.
\]
These are precisely the old forbidden point/facet incidences. The physical zero contract is a real contact contract; replacing the Gram form by H does not retain it automatically.

Among the \(\binom{40}{2}=780\) complex-line pairs, exactly 240 have \(H_{ij}=0\). The remaining 540 are complex-nonorthogonal. For each such pair there is exactly one relative phase \(k_{ij}\in\mathbb Z/3\) for which its selected real roots are orthogonal. Explicitly, if the representatives in the two cycles have phase indices a,b, then
\[
 A_{(i,a),(j,b)}=0
 \quad\Longleftrightarrow\quad b-a=k_{ij}\pmod3 .
\]
The checker verifies all nine phase pairs for each of the 540 pairs.

These 540 pairs partition into ninety complete four-vertex graphs, called pencils here. For each pencil the receipt includes four real representatives which are pairwise real-orthogonal while all six complex inner products are nonzero. There are exactly ninety such four-line class sets, and every complex-nonorthogonal pair appears in exactly one. This is verified from the complete finite root list, without relying on an external generalized-quadrangle identification.

**Theorem.** Every choice of one of the three real root lines from each of the forty E-cycles creates at least ninety unordered forbidden contacts at which the rank-four Hermitian form is nonzero.

**Proof.** In one pencil, use the four supplied pairwise-real-orthogonal representatives as phase zero. A selected representative at each vertex has one of three relative phases. Four vertices receive three values, so two receive the same value. Applying the same E-power to a real-orthogonal pair preserves its real orthogonality, while its complex inner product remains nonzero. Thus every pencil contributes at least one forbidden nonzero Hermitian contact. The ninety pencils have disjoint unordered edge sets, so these ninety contributions are distinct. This proves the claim for all phase selections. \(\square\)

The checker additionally tests all \(90\cdot81=7290\) local phase assignments; the minimum per pencil is one. That finite test is an adversarial control for the proof and gain convention. For the canonical section there are 176 forbidden nonzero Hermitian contacts.

**This is not a claim of ninety required MOVEs.** Contacts may share work, factor through a small bank, or be served by a changed source or geometry. The theorem proves that a naive rank-four replacement fails the old fitting zeros. A useful architecture must construct and pay for a compatible correction, or change the physical contact interface.

## 3. Merely reversing the Hermitian zero convention does not give rank four

Let B be the 40 by 40 adjacency matrix of complex orthogonality. The exact checker gives the strongly regular parameters \((40,12,2,4)\):
\[
 B{\bf1}=12{\bf1},\qquad B^2=8I-2B+4J.
\]
On \({\bf1}^{\perp}\) its eigenvalues are 2 and -4. Trace and dimension give multiplicities 24 and 15, respectively. Therefore the elementary complementary fitting
\[
 I-\tfrac12B
\]
has eigenvalues -5 once, zero 24 times, and 3 fifteen times: its characteristic-zero rank is 16. The checker also gives the rank-16 lower witness modulo 101 for \(2I-B\).

This disposes only of this explicit complementary fitting. It does not prove a minimum-rank theorem for all fitting matrices, and finite-characteristic ranks from the literature cannot be silently substituted for the required complex rank.

## 4. Verification and remaining construction obligation

Run, with the pinned source file present:
\[
 \texttt{node check.js /absolute/path/to/SYMMETRY.json > RESULT.reproduced.json}.
\]
The standalone checker verifies the source SHA-256 before parsing. Its exported `check(source)` can also run in a pure JavaScript execution tool; that path was actually executed after workspace loss using the fetched pinned source. Expected status:
`PASS_JS_RECOVERY_EISENSTEIN_CONTACT_GATE`.

The receipt contains A, C, all forty-cycle contact gains, all ninety pencil witnesses, and all pair-count/rank checks. Critical independent review remains a separate task for the integrator. This author execution is not independent verification.

The next positive obligation is an actual source with the four-complex-coordinate representation, paid nonzero forbidden-contact services, all original arbitrary fields retained, correct physical access, uniform coefficient/precision control, and a completed productive caller. The rank reduction alone supplies none of those prices. Both strict complex and BIT supplier requirements, recursive accounting, and all retained foundations are unchanged.
