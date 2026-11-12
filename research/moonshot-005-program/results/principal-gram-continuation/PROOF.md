# Closed principal Gram blocks and the next rank-87 continuation

**Proved algebraic continuation gate with an exact source certificate. No new κ.**
Prepared for @CubeJerry with OpenAI assistance. The literal parent is the
independently reviewed two-frame source word. No new source word is supplied
by this package. Its assertions about arbitrary volume concern the stated
linear maps, conditional on realizing their coefficients in the retained
physical interface.

## 1. Source, current state, and scope

The frozen native source has compressed SHA256
`2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883`.
The actual two-frame word has compressed SHA256
`3d7ada763346a5658ef481f84bf895b668005a558e999be431d2257e16fbd101`
and decompressed payload SHA256
`2e0853ba95763f5182d675fbf08317871ca4b5df7328066230e446ef959f782a`.
Its complete source and tariff review is in the separate independent
`review-frame` package. This verifier independently replays its prefix to
extract every coefficient of the current hosted reverse matrix.

Let H be the 96 hosted ports. The eight coupled ports have no independent
reverse bank and are excluded. Let A be the rational E8 root matrix, scaled
so its columns have squared norm 8, and G=AᵀA/8. Equivalently the source's
integer nine-coordinate realization has squared norm18 and gives the same
G by division by18. Every rank below is over Q, or any characteristic-zero
extension. Tensoring with an identity of positive dimension V multiplies
all dimensions by V. The real Gram-rank identity is first proved over Q;
it is not asserted for arbitrary isotropic Gram matrices over other fields.

Write b_h for the independent current hosted-X2 input before additions and
d_h for the authentic hosted-Y2 input. The desired reverse output is b−d.
If the implemented additions are R d, the remaining reverse map is M=I+R.
The actual two-frame word realizes the disjoint orthogonal hosted frames

    B = [5,56,65,69,77,96,100,103],
    S = [0,7,20,27,36,46,57,111].

In the order B,U=H\B, put L=G_UB and C=G_BS. The current matrix is

    M = [[I8, C E_Sᵀ], [L, I88]],

where E_S inserts the S coordinates into U. Both frames are complete root
bases, so C is orthogonal. Its rank is88. This statement uses coefficients
extracted from the current word, not the names of previously authentic
inputs or the rank of R alone.

## 2. A general obstruction from columns that remain unchanged

Let M be an n-by-n matrix of rank r over a field, and let Z be an n-by-k
matrix whose columns form a basis of ker M, where k=n−r. For a coordinate
set J, write Z_J for its rows in J. If an arbitrary update E has zero columns
outside J, then

    rank(M+E) ≥ r − |J| + rank(Z_J).                 (1)

The lower bound is sharp for unrestricted column replacement, though an
attaining replacement need not preserve the diagonal or obey any physical
source interface.

**Proof.** The unchanged columns M_{:,Jᶜ} form a restriction of M to vectors
whose J coordinates vanish. Its kernel consists of Zz with Z_J z=0 and has
dimension k−rank(Z_J). Consequently

    rank(M_{:,Jᶜ}) = (n−|J|)−(k−rank(Z_J))
                   = r−|J|+rank(Z_J).

These columns remain present after the update. The claimed lower bound
follows. Setting all replacement columns to zero attains it. More precisely,
the exact new rank equals this fixed-column rank plus the dimension spanned
by the replacement columns in the quotient by the fixed column space. QED.

For the current matrix a right-kernel basis is

    Z_B = −G_BS,       Z_U = G_US,

with Z_S=I8. Its row at h is the coordinate vector of the actual root a_h in
the S basis, up to a sign for h∈B. Thus for every J⊆H,

    rank(Z_J) = rank(A_J).

Combining this identity with (1), every update confined to receiver columns
J satisfies the sharp algebraic lower bound

    rank(M+E) ≥ 88 − |J| + rank(A_J).               (2)

Every two distinct hosted projective roots are linearly independent. Hence
no update confined to one or two receiver columns can reduce rank88,
irrespective of its number of output rows or coefficient values. One actual
new reciprocal contact can be useful for later composition while giving no
immediate rank improvement. Equation(2) does not charge routes or show that
an attaining update is legal. It is a necessary current-state gate, not a
lower bound on codes that also alter other columns or earlier row variables.

## 3. A closed principal block is sufficient

Let K⊆H and suppose the current residual, in order K,H\K, is

    N = [[G_KK, 0], [D, I]],                       (3)

where D is arbitrary. Then

    rank N = 96−|K|+rank(A_K).                     (4)

Its right kernel consists precisely of

    x_K∈ker G_KK,     x_(H\K)=−D x_K,

and its left kernel consists of (y_K,0) with y_K∈ker G_KK. To prove this,
the outside identity block can eliminate D without changing the principal
block. Since G_KK is a rational positive-semidefinite Gram matrix, its rank
equals rank(A_K). The displayed right and left kernels also prove the rank
formula directly.

The zeros in the top-right block are essential. Arbitrary outside rows D
are allowed; there is no need to complete all transpose entries from K into
every outside output. This strictly weakens a full-column-completion
interface. If B⊆K, then rank(A_K)=8 and (4) becomes104−|K|.

The actual two-frame matrix is exactly of the form(3) for K=B∪S. The
outside block is D=[G_(H\K),B, 0]. Thus it already contains a closed
principal Gram block on16 hosted roles. A further hosted role t can lower
rank by one if the enlarged principal block K∪{t} is supplied, even when
many entries from the old S columns into other outside rows remain absent.

## 4. The exact twelve missing entries for every next hosted role

Fix any t∈H\(B∪S). Every such root has exactly four nonzero inner products
with B and four with S; each is±1/2. Let

    B(t)={b∈B:G_bt≠0},    S(t)={s∈S:G_st≠0}.

In the current matrix, the principal block on K∪{t} is missing exactly:

* the eight entries (h,t) with h∈B(t)∪S(t), of values G_ht;
* the four entries (t,s) with s∈S(t), of values G_ts.

All twelve entries are currently zero. The four entries(t,b), b∈B(t),
are already present. Add exactly these twelve coefficients, and call the
new matrix M_t. It satisfies(3) with |K∪{t}|=17. Therefore

    rank M_t = 87,       nullity M_t = 9.           (5)

This is an exact count for this prescribed principal-Gram extension; it
does not assert a universal minimum number of scalar entries among all
possible rank-reducing updates. A constructive right-kernel basis is
indexed by u∈S∪{t}:

    (z_u)_B = −G_Bu;
    (z_u)_(S∪{t}) = e_u;
    (z_u)_h = G_hu,           h∈H\(B∪S∪{t}).

The nine pivot coordinates on S∪{t} prove independence. Deleting those nine
rows and columns leaves a unit block-triangular87-by-87 minor, proving the
matching lower bound. The left-kernel basis has the same B and S∪{t}
coordinates and is zero outside this set.

The twelve-entry update is supported on exactly the five columns
J={t}∪S(t). Their roots have rank4 because the four orthogonal S(t) roots
are independent and a_t=Σ_(s∈S(t)) G_st a_s. Thus equation(2) permits a
drop of at most one, and the specified extension attains it. This explains
why the four reciprocal links back into t matter: the eight entries in
column t alone cannot reduce the current rank.

## 5. Relation to whole-column continuation and the physical frontier

For comparison, completing entire new transpose columns on a subset
Q⊆H\(B∪S), while retaining the current partially filled S columns, gives

    rank = 88−|Q|+rank(A_Q).

This follows by eliminating the B block in coordinate order B,S,Q,V:
the S rows vanish, Q rows retain only −G_QB G_BS in S columns, and V has an
identity block. It also attains the fixed-column lower bound(2). A single
new complete column therefore has zero rank gain. Completing missing S
entries first, or using the much smaller principal-block extension above,
changes the set of columns that is actually updated. These scopes must
not be confused.

The twelve requested coefficients are reverse-output instructions only.
If realized as twelve genuine reciprocal source contacts, their matching
forward effects must also be verified from authentic current first-bank
rows, and their extra source expenses must be charged. Reverse-only
preconditioning or explicit copies can instead realize the matrix without
those forward improvements. Neither variant is supplied by the algebra.
All old B and S routes already consumed by the two-frame word remain spent.
New work must establish cochart availability, compatibility with the
existing paired inverse, chart maps, ownership, erasure, and the complete
tariff. A single coefficient delivered by a funded dependent-carrier
construction is partial progress toward this block, not a rank87 word.

The source certificate checks all80 possible t, their exact missing-entry
sets, all paired-root independence tests, the explicit kernels/minors, and
negative controls. It does not perform an unbounded search or infer a
physical supplier from finite algebra. All five foundational assumptions,
the compatible complex and BIT suppliers, and complete recursive accounting
remain. There is no new complete conditional or unconditional κ.

## Reproduction

```sh
python verify.py --repo /path/to/integer-mult-bounds --output output
```

The verifier requires the source and admitted frame word at their preserved
repository paths and exact pins above. Expected: rank88 for the current
actual word; all80 prescribed principal extensions have rank87 and exactly
12 missing coefficients; all80 five-column supports have root rank4.
