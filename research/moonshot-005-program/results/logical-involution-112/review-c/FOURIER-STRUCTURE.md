# Native cross-half couplings are Fourier kernels on their common radical

**Proved for the fourteen exact native classes.** This is a source-specific
geometric lemma, not a caller commutation or physical interface theorem.

Use the112-port root domain and exact pin of `REVIEW.md`. In each of the
fourteen classes let T,S be its negative-product and positive-product Gram
sign halves. Put U_T=span_F2{v_h:h∈T}, U_S=span_F2{v_h:h∈S}, and
W=U_T∩U_S. Then:

1. Both U_T and U_S have dimension three, W has dimension two, and
   U_T+U_S has dimension four.
2. U_T⊥U_S under the binary dot product. W is exactly the radical of the
   restriction to either three-space.
3. For any chosen native base normals u∈T and v∈S, the two half sets are the
   affine planes u+W and v+W.
4. Choose a basis a,b of W and write x=x₁a+x₂b, y=y₁a+y₂b. Let
   K(x,y)=〈ρ(u+x),ρ(v+y)〉/18 and J(x,y)=2K(x,y). Every J is±1, and after
   normalizing its first row and column,

   \[
   J(x,y)J(x,0)J(0,y)J(0,0)
   =(-1)^{x_1y_2+x_2y_1}.
   \]

The fourteen W's are exactly the seven two-planes inside
E=span_F2{30,45,75}, each repeated twice. Thus a single normalized four-point
symplectic Fourier kernel describes every class, with explicit native
permutations and diagonal sign changes.

## Exact proof and certificates

The finite native domain is part of this proposition. `check.py` constructs
the actual real roots from their nine-bit normals; no author geometry or
Gram routine is imported. It reconstructs each class by its four nonzero
omitted-frame coordinates, divides by the sign product, enumerates both
binary spans and their intersection, and checks every displayed equality.
All spaces have at most sixteen elements. For each class the selected basis,
base normals, entire sixteen-entry J matrix and normalized matrix appear in
`RESULT.json:fourier_radical_geometry`.

For the chosen bases the equation is an exact equality of sixteen signs in
each of fourteen specified finite instances. This exhaustive calculation
proves the finite proposition. Changing the basis of W preserves the unique
nonzero alternating form in dimension two overF2. Changing either affine
base modifies Fourier rows/columns by characters and is absorbed by the
normalization. Hence the basis/base formulation follows from those exact
witnesses, rather than from a numerical pattern fit.

In each class the R0 coupling is

\[
\begin{pmatrix}0&-K\\-K^T&0\end{pmatrix}.
\]

The recorded row/column signs conjugate this symmetric coupling to the
standard cross-half Fourier swap. Diagonal signs commute with every diagonal
phase matrix. Therefore an eventual conjugacy argument for physical caller
phases can concentrate on the remaining exact permutation of the phase
family and its native port/frame interpretation. This last sentence is a
reduction, not a claim that the required physical phases are already common
across stages or commute with fresh body transformations.

The coordinatewise scalar identity tensors with an arbitrary value module.
That algebraic extension does not provide a uniform physical compiler,
precision budget, or port-transport service.

Credit: exact native root and class data are inherited; Worker C established
and independently reconstructed this Fourier/radical formulation during
review of Worker B's new112 source, under @CubeJerry's direction with OpenAI
assistance. No new κ.
