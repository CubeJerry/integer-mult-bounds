# Independent review of non-diagonal cyclic ordinary implementations

**Accepted in the fixed monomial and fixed scalar primitive interface.** The
new source tables, elementary implementation and determinant normalization
are proved for their stated quantifiers. They do not give an independent
(4,2,1) endpoint or a complete profitable supplier.

## Literal monomial controls

For an arbitrary fixed Boolean table f on the sixteen addresses, split each
b-pair of H_f as (-1)^mu Z_b^nu. Direct two-by-two multiplication gives
C_b^-1 Z_b C_b=Y_b and C_b Z_b C_b^-1=-Y_b. The cubic diagonal D_acd is
independent of b and commutes with the controlled b-flip, so its conjugating
copies cancel. The rotation P then gives exactly the two input-indexed
tables in (1a). This proves the entire fixed-table family; checking eight
examples alone would not prove that statement.

Each conjugate is a unitary involution. If H_f has w negative entries with
0<w<16, its tensor-power trace is (16-2w)^V and the two sector dimensions are
(16^V +/- (16-2w)^V)/2, both positive at every positive V. For the quartic
table the literal source has all four nonzero spectral channels for both
conjugates. To lift that fact, choose one nonzero channel in one column and
the nonzero (+,+) channel in each additional column. The tensor of these
local projected operators is a nonzero compression of the corresponding
global projected operator. Hence it cannot be canceled by contributions
with different local sector tuples. This compression argument avoids any
assumption about entries in the physical basis being individually uncanceled.
Other Boolean tables need their own source-channel check.

The earlier cyclic conjugacy proof therefore applies to these two-sector
controls with a six-by-six scalar coherence matrix, under its explicit
spectral-form hypothesis. The source channels carry actual phases, not just
permutations or a width-one rank label.

## Finite elementary lowering and invoice

For any fixed admitted unitary monomial h with h^m=I, m in {2,4}, a family of
three-by-three sector units with one common nonzero determinant delta has an
explicit ordinary implementation. Left multiplication by
diag(delta^-1,1,1) makes each scalar sector special linear. Pivot elimination
uses at most three determinant-one signed swaps (three elementary additions
each) and six further additions. Two balanced diagonal matrices use six
elementary factors each. Thus 27 is a valid conservative bound; a smaller
bound is unnecessary for this existence claim.

The balanced diagonal identity has the correct order:
w_ij(t) w_ij(-1)=diag_ij(t,t^-1). The code lists chronological operations,
so the right factor is executed first. Reversing the elimination and
negating its coefficients constructs the forward recipe.

An elementary factor on sector s is expanded into m factors using the finite
Fourier formula for Pi_s. All cross terms within that expansion vanish by
E_ij^2=0. The literal monomial shear applies h^j to the source, scales it,
performs one unweighted ADD, then reverses the scale and monomial. The source
is restored at every factor, with no extra whole-field owner. Sector factors
compose correctly because distinct spectral projectors annihilate one another.
The final common determinant scale is applied on the left; its inverse is
the first operation in the reverse recipe.

The resulting forward or inverse upper bounds are 27m^2 ADD passes,
54m^2+1 SCALE passes and 54m(m-1) monomial services. The +1 disappears for
delta=1. Every monomial and scalar call is separately charged under the
retained implementation, storage, precision and tape contracts. These are
existence bounds, not a favorable complete caller invoice.

## Why determinant normalization does not lose native conjugacies

For the constructed inverse sector basis R_s=[u_s,z_s,w_s], replace only its
third column by w_s/det(R_s). This makes both R_s and q_s=R_s^-1 determinant
one. It leaves R_s e0=u_s unchanged, and it leaves the second row
e1^T q_s=v_s unchanged. Therefore every cross-sector active product
-R_s E01 q_t remains fixed, not just the diagonal ones. The third-coordinate
projector also remains fixed under this column rescaling. Thus the sufficient
common-determinant implementation condition imposes no extra restriction on
the previously admitted native simultaneous-conjugacy criterion.

The analogous statement for a complete ordered triple of rank-one
projectors uses mutually orthogonal idempotents summing to I: one image vector
from each is a basis, and rescaling a column preserves all three projectors.
The left endpoint encoding still needs its own ordinary-membership proof.

## Stability, independent checks and corrections

The general Euclidean norm statement is an upper bound by max_s ||q_s||_2.
Equality requires all sectors to occur. The draft's unconditional equality
was corrected before admission; it is valid for both nonconstant involutions
at every positive width. Products of norms of the finite elementary recipes
bound every prefix independently of V. Coordinate maximum-norm bounds also
remain independent of width because each monomial has norm one in that norm.

The root checker imports no author code. Independent SymPy matrices verify
every primitive of four emitted forward and inverse schedules, both
polynomial inverse products, the balanced diagonal identities, all four
two-by-two sign cases, sixteen literal source addresses for eight nonlinear
tables, all quartic source channels and idle-column normalization across all
cross-sector products. Omitting a monomial service in each schedule fails;
conjugating the source phases breaks the exact intertwining identity. Two
checker-development comparisons required canonical expansion of both sides
of a Gaussian-rational identity; no construction or proof changed for those
normalization fixes.

The theorem is universal by the finite algebraic argument above. The exact
finite controls are supplementary evidence. Every global foundation,
native/body/clock/endpoint service, strict supplier and recursive assembly
obligation remains. No new complete kappa. Credit @CubeJerry, retained source
and ordinary compiler contributors, Worker B and independent root review,
with substantial OpenAI assistance. Proof and result hashes are in RESULT.json.
