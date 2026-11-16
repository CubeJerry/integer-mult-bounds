# A constructive ordinary family with non-diagonal monomial controls

**Exact finite construction under the retained fixed-monomial and fixed-scalar
contracts. No `(4,2,1)` endpoint is claimed.** This enlarges the preceding
diagonal quarter-control family to genuine address permutations. It does not
postulate a free spectral projector or an arbitrary ordinary matrix inverse.

## 1. Two actual source controls outside the diagonal family

Keep the literal four-bit source `A=C_b D_acd P` and put

    H|a,b,c,d> = (-1)^(abcd)|a,b,c,d>,
    K_minus=A^-1 H A,              K_plus=A H A^-1.

Both K operators are ordinary root-four monomials, with the exact tables

    K_minus: (a,b,c,d) -> (a,b,c xor abd,d), phase i^[abd(1-2c)],
    K_plus:  (a,b,c,d) -> (a,b xor acd,c,d), phase i^[acd(2b-1)].       (1)

They are involutions, each with trace14 and eigenvalue multiplicities15 and1.
They genuinely permute physical addresses. Their powers and inverses have
fixed sixteen-entry tables and the retained compact-monomial implementation.
For `k=K_minus` or `K_plus` and `k_V=k^(tensor V)`, both eigenvalues occur at
every positive V. Thus

    Q(k_V)=Q_0 tensor I+Q_1 tensor k_V

is a unit for all positive widths exactly when `q_+=Q_0+Q_1` and
`q_-=Q_0-Q_1` are scalar three-by-three units. Its inverse is the same finite
Fourier interpolation of `q_+^-1,q_-^-1` as in the quarter-control lemma.

The source relations `A K_minus=H A` and `K_plus A=A H` are retained with
their actual phases. The four spectral blocks `Pi_s A Pi_t`, s,t in {+,-},
are all nonzero for each control. The checker verifies this on the literal
sixteen-address source. This finite fact gives every-width witnesses: select
one supported eigenvector matrix entry for (s,t) in the first column and a
supported (+,+) entry in each additional column. Their tensor product is a
nonzero entry of `Pi_s(k_V) A^(tensor V) Pi_t(k_V)`.

Consequently the simultaneous-conjugacy criterion of `CYCLIC-CONJUGACY.md`
also applies here with two sectors and a six-by-six scalar block matrix,
provided the candidate P and T have that explicitly declared spectral form.

### 1.1 A larger literal sign-table family

The source controls need not be confined to a reflection of one address.
For any fixed Boolean table f on the sixteen addresses, let
`H_f|x>=(-1)^f(x)|x>`. Both `A^-1 H_f A` and `A H_f A^-1` are ordinary
monomials. Their exact input-indexed tables are

    mu_minus=f(b,0,d,a),
    nu_minus=f(b,0,d,a) xor f(b,1,d,a),
    (a,b,c,d) -> (a,b,c xor nu_minus,d),
    phase i^[2mu_minus+nu_minus(1-2c)],

    mu_plus=f(d,a,0,c),
    nu_plus=f(d,a,0,c) xor f(d,a,1,c),
    (a,b,c,d) -> (a,b xor nu_plus,c,d),
    phase i^[2mu_plus+nu_plus(2b-1)].                                 (1a)

To prove (1a), write each b-pair of H_f as `(-1)^mu Z_b^nu`. The exact
two-by-two identities are `C_b^-1 Z_b C_b=Y_b` and
`C_b Z_b C_b^-1=-Y_b`. The cubic phase D_acd is independent of b, so it
commutes with these controlled b flips; its two appearances cancel in the
conjugation. The remaining rotation P gives the displayed argument orders.
This proves the whole fixed-table family, including nonlinear balanced
controls that move every address in one of the two conjugates.

If f is nonconstant with w negative entries, both involution sectors occur
at every positive V, with exact dimensions
`(16^V+(16-2w)^V)/2` and `(16^V-(16-2w)^V)/2`. The two-sector unit and
implementation arguments therefore apply unchanged. Nonvanishing of every
source channel is a separate condition: the four-channel statement above
was proved for the stated quartic control and is not automatically asserted
for every f.

## 2. A physical implementation for a definite large subfamily

Let m be2 or4, let h be any admitted fixed monomial with `h^m=I`, and let
`Pi_s=(1/m)sum_j zeta^(-sj) h_V^j`, where `zeta=i^(4/m)`. Suppose all fixed
scalar matrices q_s are invertible and have one common nonzero determinant

    det(q_s)=delta in Q(i), independent of s.                         (2)

Then `Q=sum_s q_s tensor Pi_s` and its inverse have explicit finite ordinary
recipes on the existing three banks. No additional field or initialized
payload is needed. Condition (2) is a sufficient implementation condition;
it is not asserted necessary for an arbitrary ordinary implementation.
The preceding diagonal-control implementation continues to allow unequal
sector determinants because it applies the scalar matrices directly at each
address. That argument is not used for a non-diagonal h.

For the **native simultaneous-conjugacy construction**, the common
determinant condition causes no loss at all. The preceding criterion builds
`R_s=[u_s,z_s,w_s]`, where w_s is any nonzero vector spanning `image(P_s)`.
Replace w_s by `w_s/det(R_s)`. This makes `det(R_s)=det(q_s)=1`, while leaving
`R_s E_22 R_s^-1=P_s` and every `-R_s E_01 q_t=M_st` unchanged. The active
column u_s and row v_s are unaffected. Therefore every solution admitted by
the finite native-conjugacy criterion has a representative implemented by
(3)--(5), even for these non-diagonal controls.

The same determinant normalization applies to a complete triple of
rank-one spectral-sector projectors: select one nonzero image vector from
each projector as the columns of R_s, and scale one column to determinant
one. It gives an explicit ordinary conjugator to the three bank projectors.
An endpoint still owes the left ordinary membership check after that
conjugator, so this is not an automatic Gaussian endpoint admission.

First factor out the single ordinary scalar operation
`D_delta=diag(delta,1,1)`, leaving scalar sector matrices in SL_3(Q(i)).
Every such matrix has an elementary factorization with at most27 factors
`e_ij(c)=I+c E_ij`, i !=j. One explicit algorithm uses Gauss-Jordan
elimination without row scaling: replace a pivot swap by

    w_ij(1)=e_ij(1)e_ji(-1)e_ij(1),

which swaps the two rows with the needed sign and determinant one. At most
three such pivot moves and six row additions leave a diagonal matrix with
determinant one. Two balanced diagonal scalings finish the reduction, each
using the six-factor identity

    diag_ij(t,t^-1) = w_ij(t) w_ij(-1),
    w_ij(t)=e_ij(t)e_ji(-t^-1)e_ij(t).                               (3)

Reversing and negating elementary coefficients gives the forward recipe.

To apply a particular factor only on spectral sector s, use
`I+c E_ij tensor Pi_s`. Its exact finite lowering is

    I+c E_ij tensor Pi_s
      = product_(j'=0)^(m-1)
          [I+(c/m)zeta^(-s j') E_ij tensor h_V^(j')].                 (4)

The cross terms vanish because `E_ij^2=0`. Each factor on the right is a
source-restoring monomial shear. For nonzero scalar alpha and fixed monomial
g its literal chronological implementation is

    apply g to source bank j;
    SCALE(source,alpha);
    ADD(destination i,source j);
    SCALE(source,alpha^-1);
    apply g^-1 to source bank j.                                    (5)

Every ADD in (5) is the unweighted retained primitive. All monomial services
and fixed-scalar arithmetic are separately charged. The source bank returns
to its original contents. Different spectral sectors act independently, so
concatenating the finitely many sector recipes realizes Q; apply D_delta
last. Reverse the complete schedule for the inverse.

## 3. Explicit conservative invoice and stability

There are at most27m spectral elementary factors and at most27m^2 monomial
shears. Since the j'=0 term needs no monomial adapter, a conservative bound
per forward or inverse application is

    27m^2 unweighted whole-field ADD passes,
    54m^2+1 fixed-scalar whole-field SCALE passes,
    54m(m-1) fixed monomial services,
    no extra whole-field owner or assumed spectral-control primitive.       (6)

The final extra SCALE is absent when delta=1. A specific q_s may require far
fewer operations; the checker emits its actual elementary and expanded
recipes. For m=2, (6) is108 ADD,217 SCALE and108 monomial services. For m=4,
it is432 ADD,865 SCALE and648 monomial services. These are implementation
bounds, not profitable caller invoices.

Every h^j and its inverse has the retained fixed-table tariff
`O(volume*((f log p)^tau+1))`, including compact reservations, spectators,
exceptional repair, source restoration and tape obligations. Every scalar
and its inverse is fixed before V or the layer parameters vary; the retained
Q(i) scalar arithmetic and precision contract is still required. Products
of the finite elementary norm bounds give width-independent amplification
constants, and all prefix norms remain finite constants. For the completed
unit itself, orthogonal spectral decomposition gives the Euclidean operator
norm bound `norm_2(Q)<=max_s norm_2(q_s)` and the corresponding inverse bound.
Equality holds when every sector occurs at the width in question, as it
does for both nonconstant involution controls at every positive V. The
general `h^m=I` interface can have absent sectors. The finite elementary
recipes also give width-independent coordinate maximum-norm bounds directly,
since each monomial has maximum-norm operator bound one.

This construction supplies no numerical discount to a native call. The
three-native body price, idle services, all clocks, endpoint encodings,
precision and recursive expenses remain in the complete supplier invoice.

## 4. Validation and exact scope

The checker constructs the actual controls in (1), their inverse tables and
all four source channels. It derives elementary recipes for scalar sector
units, verifies the lifted polynomial identity modulo `z^m-1`, and checks
the source-restoring lowering (5) with exact Gaussian-rational arithmetic.
It tests both m=2 and m=4 and reverses the full recipes. A unit with unequal
sector determinants is rejected by this construction interface without
being labelled impossible in the full ordinary class.

This opens a concrete non-diagonal interstage class for the earlier-coupling
problem. Finding an actual independent `(4,2,1)` endpoint with the required
ordinary encodings remains open. All five foundations remain. **No new
complete kappa.** Credit @CubeJerry and the retained source, finite-group,
compact-monomial and ordinary-compiler contributors; Worker B with
substantial OpenAI assistance. Independent review is separate.
