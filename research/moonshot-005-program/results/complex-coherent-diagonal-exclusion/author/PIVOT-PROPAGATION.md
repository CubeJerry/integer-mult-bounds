# Full column propagation excludes the coherent diagonal second interface

**Author theorem, pending independent review. No caller or new kappa.**

Fix the admitted literal four-bit source `A=C_b S`, `a=A^(tensor V)`, the natives
`L=[[a,0,0],[I,a,0],[0,0,I]]`, `U=[[a,-a^2,0],[0,a,0],[0,0,I]]`, and
`h=(S^-1 D_b^theta)^(tensor V)` for any theta in {0,1,2,3}. Write `x=D_a^(tensor V)`
and `y=D_b^(tensor V)`. Let `R_b=R(y)` be an arbitrary invertible three-bank matrix
in the quarter-control algebra, with first column `(s(y),t(y),u(y))^T` and remaining
columns `(b(y),d(y),f(y))^T`, `(c(y),e(y),g(y))^T`. All coefficient templates are
fixed before V grows. More precisely, for each fixed finite catalogue of
one-column tensor words used by R,Q and their endpoint encodings, choose the
faithful-separation threshold V0 of the retained tensor-independence theorem.
The exclusion proved here applies at every V>=max(3,V0). In particular there is
no fixed finite template realizing the required endpoint at every sufficiently
large width, or at all positive widths. No impossibility at an arbitrary
isolated width1 or width2 is claimed. Let Q be any invertible ordinary three-bank matrix whose
entries are in the fixed full diagonal root-four tensor algebra. Thus each actual
q_ij is diagonal, even though it may be singular or have many zero sectors.

If `E=L R_b diag(I,h,I) U Q L` is ordinary-equivalent, in the retained fixed finite
tensor-word interface, to independent Gaussian heads (4,2,1), then necessarily

    s=0, u=0, and t is a unit in every quarter sector.                (1)

Consequently no conditional switching of the first routing column between active
banks can work with diagonal Q. Nor can a first column with any idle-bank part.
The first-column reduction is proved first. The residual `(0,t,0)^T` case is
also excluded below, so **no such invertible R_b and diagonal Q give the target**.
The theorem does not exclude a genuinely non-diagonal Q, a different first-clock
placement, or an arbitrary first ordinary interface.

## Column propagation lemma

For every V>=3, every nonzero function F on the four quarter sectors, either
z=x or z=y, and every diagonal operator D on the actual bank,

    F(z) a^2 D=0  implies D=0.                                    (2)

The source identity `a^2=(C_a C_b)^(tensor V) R2^(tensor V)` gives the proof.
R2 is a monomial unit. In each column of a^2, all 2^(2V) choices of the output
a-bits and b-bits have nonzero amplitude, independently. Their total a and b
Hamming weights independently attain every residue modulo four when V>=3.
Thus every column has a nonzero entry in every joint x/y sector. If D has any
nonzero diagonal entry, that column survives after multiplication by F(z),
contradiction. No invertibility of F, no division by a zero divisor, and no
parity restriction on V is used. The result holds for all V>=3, including every
residue class. V=1,2 cannot support this statement for arbitrary nonzero
four-sector F: the weight-three sector is absent there.

## Exact eight-support equations

Use `a F(y)=F(x) a`. Set

    v=(s(x),t(x),0)^T,  w=(0,s(y),u(y))^T.

All one-column words in the clocked products `a B(y) h a` have at most two
nonzero entries per row. Every word in `a^2 d a` and `a^3 d`, for a diagonal
root-four unit d, has exactly eight entries per row. Every word in `a^3 d a`
has exactly sixteen. These are precisely the source support facts retained
from the source-transport package; arbitrary diagonal sums are treated linearly.
The sufficiently large faithful-width tensor separation therefore forces the
entire eight-support contribution to vanish, since (4,2,1) has only the
2-,4-,16-support Gaussian classes. The first two block columns give the exact
operator equations

    v a^2 q01 a - w a^2 q11 a =0,                               (3)
    v(a^2 q00 a - a^3 q11) - w a^2 q10 a =0.                    (4)

These are projections of the literal ordered product, not commutations of q
through a. The full sixteen-support contribution can only arise through

    -v [a^3 q10 a, a^3 q11 a, 0].                             (5)

Any other terms have at most eight support; no Gaussian classification is
inferred merely from four- or sixteen-support size. For the necessary argument,
vanishing of (5) suffices to exclude a nonzero rank-four Gaussian component.

If s is not identically zero, row0 of (3) and (2) force q01=0. Row1 of (3)
then forces q11=0. Row0 of (4) now forces q00=0, and row1 forces q10=0.
Equation (5) vanishes, contrary to the target rank-four component rank D.
Thus s=0. If u is nonzero, row2 of (3) forces q11=0, and row2 of (4) forces
q10=0, with the same contradiction. Thus u=0. Finally invertibility of R_b
makes t a unit in each occupied sector, and every quarter sector is occupied
for V>=3. This proves (1).

## The residual first column is also impossible

Now put

    R_b=[[0,b,c],[t,d,e],[0,f,g]], t a unit,
    H=h a, v=a H=a h a.

The scalar-sector matrix [[b,c],[f,g]] is invertible. Direct multiplication gives

    L R_b diag(I,h,I) U =
      [[0, b(x) v, c(x) a],
       [t(x) a^2, -t(x) a^3 + b(y) H + d(x) v, c(y)+e(x) a],
       [0, f(y) H, g(y)]].                                (6)

The eight-support equations force q01=q12=0 and q00 a=a q11. The remaining
argument retains the actual ordinary and four-support components, with their
ranks under arbitrary ordinary outer encodings. No scalar-sector invertibility
is inferred for an individual R entry unless the displayed full minor proves it.

At one column, H=D_c^theta C_c is always a rank-one Gaussian unit. For odd theta,
v=C_b D_b^theta C_b S is rank one; for even theta it is a monomial unit.
For every diagonal root-four unit d, H d A has four entries per row. When theta
is odd, v d A also has four entries per row; their two path choices affect
different bits, so no diagonal phases can cancel a path. When theta is even,
v d A instead has two entries per row. These exact support facts also follow
from the literal one-column tables and unique-path incidence checks. All
phases, including tensor powers of scalar phases, are retained.

### Odd theta

The only ordinary terms in columns0 and2 are, in rows1,2,

    c q21, g q21, c q22, g q22.

Their vanishing forces q21=q22=0, because each sector column (c,g)^T is nonzero
(the two-by-two minor is invertible). The resulting Q pattern is

    Q=[[q00,0,q02],[q10,q11,0],[q20,0,0]],

and invertibility forces q02,q11,q20 to be units. The four-support component
of E's column2 is supported solely in output row1, with invertible block
`t(x) a^2 q02`. In column1 its projection to output rows0,2 is

    [b(x) v; f(y) H] q11 a
      = diag(a,I) [b(y);f(y)] H q11 a,                     (7)

which has column rank D, since (b,f)^T is nonzero in every sector. Thus the
four-support component has rank at least2D: column2 supplies D independent
vectors in the kernel of the row0/row2 projection, while column1 supplies D
independent projected vectors. The target four-support component has rank D.
Contradiction.

### Even theta

Ordinary absence still forces c q22=g q22=0, hence q22=0. With q01=q12=0,
invertibility of Q forces q02 to be a unit. The four-support component of
column2 is again supported solely in row1 and has invertible block
`t(x) a^2 q02`. To have total four-support rank D, every block of that
component in rows0 and2 must therefore vanish. The row2 blocks in columns0,1
are exactly

    f H q10 a, f H q11 a.

The block row [q10,q11] is surjective because it is row1 of the invertible Q
(with q12=0). Hence f H[q10,q11]=0 implies f=0. The invertible scalar-sector
minor [[b,c],[0,g]] now forces b and g to be units. Its ordinary row2,column0
term g q21 forces q21=0. Invertibility of Q with q21=q22=0 then forces q11
to be a unit. But the ordinary row0,column0 term is b(x) v q11, which is an
invertible operator and cannot vanish. Contradiction.

Together with the first-column reduction, this proves the claimed universal
exclusion for **every coherent quarter-controlled R_b and every fixed diagonal
second interface Q**, including nonunit conditional pivots and idle-bank first
column routing. The conclusion depends on the stated first-clock placement,
not on a finite failed search or a width-one component-rank census.

## Constructive limitation of the lemma

Diagonality of D in (2) is essential. For a diagonal projection P and an ordinary
monomial involution H satisfying `a^2 H=Z a^2`, where `P=(I+Z)/2`, the ordinary
non-diagonal projection `D=(I-H)/2` obeys `P a^2 D=0` while D is nonzero. Such H
exists explicitly here: take `Z=Z_a^(tensor V)` and
`H=(A^-2 Z_a A^2)^(tensor V)`. Since `A^2=C_a C_b R2`, its one-column base is a
monomial involution (conjugating Z_a by C_a gives a phased bit flip; R2 is
monomial). This is an explicit ordinary escape from the propagation lemma,
not a complete caller. Its physical forward/inverse services remain paid.

## Costs, dependencies, next question

The theorem changes no invoice and supplies no strict supplier. The gross
three-native (4,2,1) comparison remains the retained positive arithmetic target,
before all ordinary/source/compiler/precision/recursive obligations. All five
global foundations remain.

Dependencies are the literal source square and transport identities, the fixed
finite tensor separation and support facts in `complex-source-transport`, and
the ordinary-bimodule interpretation of independent Gaussian heads. Exact pins
are in RESULT.json generated by check_pivot_propagation.py. The finite checker
confirms the literal source support, all-sector coverage, ordered formulas and
negative controls; the universal theorem is the argument above.

Open next questions: (i) build an actual three-role endpoint using genuinely
non-diagonal Q, starting with explicit pulled-back phase involutions; (ii) vary the first clock placement or move outside its coherent quarter-control
family; (iii) pay every admitted ordinary interface and
complete the strict uniform supplier before claiming any new kappa.

Credit @CubeJerry and retained four-bit/source-transport/tensor-separation and
ordinary-compiler contributors; Worker B with substantial OpenAI assistance.
