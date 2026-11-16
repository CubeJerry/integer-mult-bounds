# An exact non-Clifford three-head source with Gaussian square and cube

**Proved operator algebra and all-width endpoint gauges; physical nonlinear-permutation admission remains open in this author package. No new κ.** This changes the common-head representation itself. It gives an infinite-projective-order head with exact rank-one, rank-two and rank-three whole-job forms, exiting the finite collective-Clifford group-algebra obstruction for a precise mathematical reason. It does not give a profitable retained-role caller or treat a nonlinear address table as an already admitted physical service. A separate root-reviewed physical bridge may subsequently discharge the new movement obligation.

## 1. Conventions and proposition

Let the one-column address be `(a,b,c)∈{0,1}³`, encoded by `a+2b+4c`. Matrices act on columns; products execute right to left. Write `X_a,X_b,X_c` for the three coordinate flips and

\[
 C_u=\alpha I+\beta X_u,\qquad \alpha=(1+i)/2,\quad\beta=(1-i)/2.
\]

A monomial `M(p,q)` sends `|j>` to `i^{q_j}|p_j>`. The column permutation `P` is `(0,4,1,5,2,6,3,7)`; it sends old `a,b,c` bits to new `c,a,b` positions. Define

\[
 D|a,b,c\rangle=(-1)^{abc}|a,b,c\rangle,\quad S=DP,\quad A=C_bS.       \tag{1}
\]

For every integer `V≥1`, put `a_V=A^{⊗V}` and tensor all one-column monomials similarly. Exterior field ADD/SCALE coefficients are never tensor-powered. The exact claims are:

1. Explicit monomial `R` satisfies `C_b S=A`, `S⁻¹ C_a R=A`, and `C_a C_b R=A²`. The pinned source's forward lower and upper halves consequently become `[[a_V,0],[I,a_V]]` and `[[a_V,-a_V²],[0,a_V]]`, conditional on execution of the specified ordinary monomial services.
2. Explicit monomials `L₃,R₃` satisfy `A³=L₃ C_a C_b C_c R₃`. The square and cube have actual whole-job Gaussian ranks two and three with separately charged two-sided adapters.
3. The projective order of `A` is infinite. No full lattice over the Gaussian local ring at `(1+i)` is preserved by `A`. Thus the finite-group invariant-lattice premise of the programme's modular parabolic gate fails.
4. These are literal operator identities including phases, valid on every independent input and at every tensor width.

'Rank' here refers to the displayed exact Gaussian factorizations. A row-support count is not an admission proof for a non-Clifford matrix.

## 2. Monomial source admission beyond the Clifford subgroup

Fix any `d≥2` one-column bits and distinct axes `a,b`. Let `S` be any unitary monomial and set `q=S X_b S⁻¹`. Its underlying permutation `τ` is fixed-point-free and involutive. Write `q|x>=c_x|τx>`, with `|c_x|=1` and `c_{τx}=conjugate(c_x)`. Put

\[
 R=C_a^{-1}SC_bS=(C_a^{-1}C_q)S^2.
\]

Then `R` is monomial if and only if

\[
 \tau x=x+e_a\text{ for every }x,\qquad c_x\in\{1,-1\}.             \tag{2}
\]

Equivalently `q=X_a E`, with `E` a diagonal sign invariant under the `a` flip. If `c_x=(-1)^{f(x)}`, then

\[
 R=J_fS^2,\qquad J_f|x\rangle=i^{f(x)}|x+f(x)e_a\rangle.             \tag{3}
\]

The Boolean function `f` is independent of bit `a`; no affine/quadratic restriction is imposed by the algebra.

**Proof.** Direct multiplication gives

\[
 C_a^{-1}C_q=\tfrac12(I+X_aq+iX_a-iq).                              \tag{4}
\]

On column `x` the possible output addresses are `x,x+e_a,τx,τx+e_a`. If `τx≠x+e_a`, these four are distinct with nonzero coefficients. If `τx=x+e_a`, the two coefficients are `(1+c_x)/2` at `x` and `i(1-c_x)/2` at `x+e_a`. Exactly one is nonzero precisely for `c_x=±1`; its modulus is one. The equation `q²=I` makes the sign constant on the `a` pair. This gives (3). Right multiplication by `S²` preserves the monomial property. Finally `C_aR=SC_bS`, so `S⁻¹C_aR=A`; since `C_a,C_b` commute,

\[
 C_aC_bR=C_bSC_bS=A^2.                                              \tag{5}
\]

Together with the unchanged field ADD and body transforms these establish the exact source equations. Formula (3), not a Gaussian inverse, is the proposed physical residual service. ∎

## 3. Explicit source and endpoint tables

For (1), `P X_b P⁻¹=X_a` and `D X_a D=X_a CZ_{bc}`, so (2) holds with `f=bc`. The phase `D` commutes with `P` and squares to the identity; hence `S²=P²`. Each table is indexed by input address `0,…,7`, with phases modulo four.

| Operator | Output permutation | Input phase exponents |
| --- | --- | --- |
| `S` | `0,4,1,5,2,6,3,7` | `0,0,0,0,0,0,0,2` |
| `J_f` | `0,1,2,3,4,5,7,6` | `0,0,0,0,0,0,1,1` |
| `R=J_fP²` | `0,2,4,7,1,3,5,6` | `0,0,0,1,0,0,0,1` |
| `L₃` | `0,1,2,3,4,7,6,5` | `0,0,0,0,0,3,0,1` |
| `R₃` | `0,1,2,7,4,5,6,3` | `0,0,0,1,0,0,0,1` |

`J_f` flips `a` when `bc=1`, with phase `i^{bc}`. `L₃` flips `b` when `ac=1`, with input phase `i^{ac(2b-1)}`. `R₃` flips `c` when `ab=1`, with input phase `i^{ab}`. In particular

\[
 A^2=C_aC_bR,\qquad A^3=L_3C_aC_bC_cR_3.                            \tag{6}
\]

For a symbolic check of the second identity, use `PDP⁻¹=D`, `PC_bP⁻¹=C_a`, `P²C_bP⁻²=C_c` to write `A³=C_bDC_aDC_cD`. For input `(a,b,c)` and output `(u,v,w)` its entry is

\[
 \alpha^3(-i)^{(u\oplus a)+(v\oplus b)+(w\oplus c)}
 (-1)^{abc+abw+ubw}.                                                 \tag{7}
\]

Substitute `F(u,v,w)=(u,v⊕uw,w)` and `G(a,b,c)=(a,b,c⊕ab)` in the three-axis Gaussian kernel. The identity

\[
 F(y)\cdot G(x)=ua+vb+wc+ubw+abw\pmod2
\]

and its one-sided `(-i)` phases give (7), with exactly the `L₃,R₃` phases above. This proves (6); the verifier also multiplies all 64 entries exactly.

Tensoring a product equality preserves it, giving for example `a_V³=L₃^{⊗V}(C_aC_bC_c)^{⊗V}R₃^{⊗V}`. The phase on `(x₁,…,x_V)` is `i^{Σq(x_j) mod4}`, not a width-independent one-column phase. The upper source's field minus remains `-a_V²`, not `(-A²)^{⊗V}`.

## 4. Infinite projective order and failure of the integral-lattice premise

The diagonal entries of (7) are `α³(-1)^{abc}`. Seven are `α³` and one is `-α³`, so

\[
 \operatorname{tr}(A^3)=6\alpha^3=\frac{-3+3i}{2}.                   \tag{8}
\]

This is not in `Z[i]`, the algebraic integers of `Q(i)`. Finite-order complex matrices have algebraic-integer traces on every power; hence `A` has infinite order. More explicitly, `det C_b=1` because eigenvalues `1,i` each occur four times, `det P=1` because its permutation has two three-cycles and two fixed points, and `det D=-1`. Thus `det A=-1`. If `A^m=ζI`, then `ζ⁸=(-1)^m`, so `ζ` is a root of unity and a power of `A` is the identity, contradicting (8). This proves infinite projective order.

At `(1+i)`, the numerator in (8) has valuation one and the denominator has valuation two. If a full lattice over that local ring were preserved by `A`, the matrix of `A³` in a lattice basis would have integral entries and integral trace, a contradiction. The negative valuation remains negative at every prime over two in a finite number-field extension. There is therefore no stable full lattice even for the cyclic group generated by `A`.

This identifies a failed premise of the earlier modular gate. It proves neither a profitable caller nor the failure of every possible conservation theorem.

## 5. Physical interface and complete optimistic budget

The retained `SPECIALIZATION.md` §§1–3 explicitly lowers affine binary permutations and quadratic unit phases using selected-bit row addition. A nonlinear eight-point table alone does not establish membership in that physical grammar. This author package retains the following service obligation:

> Implement each fixed Toffoli orientation on three full `V`-bit address slots, `(a_j,b_j,c_j)↦(a_j⊕b_jc_j,b_j,c_j)` simultaneously for `j=1,…,V`, on arbitrary complete payload fields and all spectators. Restore all borrowed compact controls, with no new productive credit, initialized payload or erasure. Prove a uniform fixed-tape/descriptor/layout tariff `Π_T(D,V)` compatible with the selected movement exponent and actual parameter domain. Execute the fixed unit-phase functions above, including cubic CCZ phases, with full setup and traversal costs.

All one-column functions have fixed lookup tables. In lexicographic head-digit traversal, a radix-eight odometer maintains the phase residue using fewer than `(8/7)D` digit updates over `D` coordinates; an update subtracts one old lookup value and adds one new value modulo four. This gives uniform linear combinatorial phase generation with `O(V)` control storage, not the missing payload-permutation tariff. Unit phases are exact sign changes and swaps of real/imaginary components. All monomials and their inverses have norm one.

Each native half retains its original Gaussian prices `[1]+[7]+[8]`, original ADD, full positive seven-axis body, and three source services `S,R,S⁻¹`. Each service has its actual fixed coordinate permutation and unit-phase pass. More finely, these are two three-axis cycle permutations, a Toffoli composed with a third three-axis cycle, and three phase passes. Thus all three actual layout services and their inverses remain charged; no net cancellation is presumed. Every native physical, tape, control, precision and complete-child expense remains.

The smallest useful whole-word target is still a three-role, three-native endpoint with ranks `(3,2,2)`, with all three fresh seven-axis bodies delivered to every role. Its optimistic Gaussian histogram is

\[
 P=3[1]+6[7]+3[8],\qquad T=[24]+2[23],\qquad [r]=r^{199/200}.         \tag{9}
\]

The prior rigorous arithmetic margin `T-P=0.56100733960089153867…` is unchanged. Ambient geometry is `3+3·7=24` axes per column, including the third head spectator on each square output. Exact target normalization costs two monomial services `L₃,R₃` on the cube and one `R` on each square, with inverse directions as prescribed by the actual whole-job wrapper. Even a successful caller therefore retains nine native boundary services, four endpoint services, the caller's actual ADD/SCALE/permutation catalogue, three inactive-role seven-axis idles, the nonlinear movement proof/costs, and all compiler, precision, storage and recursive expenses. A positive Gaussian margin alone does not establish a supplier theorem.

An exact baseline already exists: the universal identity `(L(a)T)³=diag(a²,a²,a²)` remains true for this `a_V`, giving `(2,2,2)` with nine total ADDs, nine native services and three bank cycles, plus square endpoint wrappers. Its Gaussian margin `-0.4184102652401057…` is negative. A paid rank-one application upgrading one output leaves margin `-0.4389926603991084…`. The new construction must obtain an upgrade without an unpriced Gaussian call, or produce another positive complete profile.

No complete supplier saving, κ improvement, unconditional compiler theorem or selected-frontier change follows. The immediate mathematical task is a role-dependent caller using this non-Clifford source; the immediate physical task is the nonlinear complete-slot movement bridge above.

## 6. Verification, provenance and exact limits

Run `python3 check.py --repo REPO --out RESULT.json`. The author checker verifies the literal source equations, table phases, square/cube factorizations and inverse wrappers, diagonal/trace formula, determinant factors, all input columns at widths one and two, exterior upper sign, and finite phase-odometer controls. It checks all 26,880 Hermitian fixed-point-free monomial involutions on eight addresses with fourth-root phases against criterion (2). This finite census corroborates the general proof; it does not replace it.

Negative controls omit CCZ, Toffoli or phase data, replace a cube by a square job, tensor an exterior upper minus, and collapse tensor phases. Dependency bytes are pinned in `DEPENDENCIES.json` and the local file manifest is separate. Checks reuse the existing exact arithmetic helper and are author verification, not independent proof review.

Source/framework credit remains with the actual native/source authors and retained provenance. This extends the programme's monomial source-admission proof and three-role source reduction; it retains @CubeJerry attribution and predecessor credit. Prepared by @CubeJerry with substantial OpenAI assistance. Exact claim: new operator-level source structure and precise movement/caller obligations. **No new κ.**
