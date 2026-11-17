# A dyadic three-bank completion of the Klein spectator source

**Constructive all-width ordinary interface. Independent endpoint separation
is still open; this is not a complete caller, supplier, or new kappa.**

The ordinary-capacity theorem permits one free bank in three complementary
plus sectors, but a split embedding alone does not give the required actual
three-bank unit. This construction completes that embedding using eight
coefficient shears, with a dyadic inverse and a literal physical source.

## 1. A universal ordinary unit with three prescribed plus entries

Let s,t be commuting ordinary involutions, and define

    e_uv=(I+u s)(I+v t)/4,      u,v in {+1,-1},
    P_s=(I+s)/2, P_t=(I+t)/2, P_st=(I+st)/2.

The four e_uv are orthogonal idempotents summing to I. Let E_ij(c)
denote the elementary coefficient shear adding c times bank j to bank i.
All three bank contents are arbitrary.

On e_++ choose L0=[[1,0,0],[1,1,0],[1,0,1]]. On e_+- choose I3.
On e_-+ choose the determinant-one rotation J01 with upper-left block
[[0,-1],[1,0]]. On e_-- choose the corresponding rotation J02. Then

    C=e_++ L0+e_+- I3+e_-+ J01+e_-- J02,             (1)
    C[:,0]=(P_s,P_t,P_st)^T.                        (2)

Its actual inverse is the same four-sector sum with each scalar matrix
inverted. This identity does not identify a physical sector with a free bank.

A chronological word for (1) is

    E10(e_++), E20(e_++),
    E10(e_-+), E01(-e_-+), E10(e_-+),
    E20(e_--), E02(-e_--), E20(e_--).                (3)

On each selected sector the relevant shear triple is J01 or J02; on every
other sector it is identity. Reversing (3) and negating every coefficient
gives the inverse word. No 1/3 scalar, zero bank, or owner is introduced.

## 2. Literal four-bit spectator instance

Retain the admitted source A=C_b D_(acd) P, a=A^(tensor V), D=16^V,
with bits (a,b,c,d) and rotation P(a,b,c,d)=(b,c,d,a). Now let

    s=SWAP_cd^(tensor V), t=(X_c X_d)^(tensor V).

These literal monomials commute and are distinct nonidentity involutions.
Their one-column traces are 8,0, while st has trace8. The projectors are
formed after tensor lifting, not as tensor powers of one-column projectors.

The exact checker emits root-four tables for

    r1s=A^-1 SWAP_cd A,    r1t=A^-1 (X_c X_d) A,
    r2s=A^-2 SWAP_cd A^2, r2t=A^-2 (X_c X_d) A^2,
    Ht=A (X_c X_d) A^-1.                            (4)

Every table in (4) is ordinary, with its actual phases. In particular
r1s=SWAP_ad and r2s=SWAP_ab. The forward conjugate A SWAP_cd A^-1 is
Gaussian rank2 and not ordinary. Thus two genuine ordinary backward
channels are supplied without granting an ordinary forward conjugate of s.

## 3. Exact kernels of the two active source banks

Use C in the retained word L C U Q L, with

    L=[[a,0,0],[I,a,0],[0,0,I]],
    U=[[a,-a^2,0],[0,a,0],[0,0,I]].

The source column governing the only possible four-source terms is

    K=(a P_s a,a P_t a,0)^T.                        (5)

Let e_--=(I-s)(I-t)/4 and set

    R1=a^-1 e_-- a, R2=a^-2 e_-- a^2.

Both are actual ordinary idempotents by (4). For every operator column X,

    K X=0 iff X=R1 X, K a X=0 iff X=R2 X.           (6)

The two entries vanish exactly when a X lies in the common minus sector
of s,t; the same argument applies after the extra a. No arbitrary X is
commuted past a source. At every positive width,

    rank(e_--)=(D-8^V-0+8^V)/4=D/4,
    rank(K)=3D/4.                                  (7)

Equivalently K* K=a^-1(P_s+P_t)a has transported-sector eigenvalues
2,1,1,0. The prefix is not injective; both ordinary kernel channels are
nonzero at every width.

## 4. A full Gaussian-four component and its actual alignment

Retain B2=A SWAP_cd A^3, the admitted exact Gaussian-two word, and use
the same symbol for its collective lift. Then

    a P_s a^3=(a^4+B2)/2,
    a P_t a^3=P'_t a^4, P'_t=(I+Ht^(tensor V))/2.

The actual ordinary unit and inverse

    H=[[2I,0,0],[-2P'_t,I,0],[0,0,I]],
    H^-1=[[I/2,0,0],[P'_t,I,0],[0,0,I]]

give the exact identity

    H K a^2=(a^4+B2,-P'_t B2,0)^T.                  (8)

The Gaussian-four component is precisely (a^4,0,0)^T, of full rankD in
one ordinary bank. The Gaussian-two residue is (B2,-P'_t B2,0)^T, also
of rankD. Their source sum has rank3D/4: class projection does not preserve
that source image.

These are not yet independent jobs. Their ordinary image columns
(I,0,0)^T and (I,-P'_t,0)^T intersect in dimensionD/2, since Ht has
trace0 at every positive width. The full Q and endpoint units must still
separate all three independent jobs, with actual inverses.

## 5. Explicit primitive invoice and complete-budget boundary

Each coefficient in (3) is four signed monomials with exterior factors
+/-1/4. To add c g(source) to a target, apply g to the source, scale by c,
ADD to the target, undo the scale, and apply g^-1. Identity monomials need
no MONO calls. The arbitrary source is restored after every term.

With this uncompressed recipe, C and C^-1 each use

    32 ADD +64 SCALE +48 MONO.

All SCALE factors are nonzero dyadics. New monomials are s,t,st and their
inverses. Every MONO is a charged full-field pass; st can be expanded into
its two spectator generators. The checker records that separate bound.

H is a factor-two scale followed by bank1 -= P'_t bank0. Its forward and
inverse recipes each use

    2 ADD +5 SCALE +2 MONO.

Exact prefix magnitude bounds and omission controls accompany the receipt.
The field volume and three arbitrary bank inputs remain unchanged.

No Gaussian query is added by C or H. The prospective three-native Gaussian
invoice remains 3[1]+6[7]+3[8] against [25]+[23]+[22], with the retained
necessary gross margin about0.560590248972... at t=199/200. The new finite
ordinary invoice must be added, together with the missing Q, endpoints,
owners, precision, compiler, erasure and recursive costs. No claim is made
that this gross margin survives complete supplier assembly.

## 6. Open next question and provenance

Find actual ordinary Q and endpoint units making L C U Q L three
independent Gaussian(4,2,1) jobs, or prove a different profitable profile.
The two rankD/4 kernels and aligned component above are concrete available
interfaces. Their projector ranges are never free whole-bank substitutes.

The prior S3 obstruction concerns a different prescribed rank-one-isolating
two-bank reduction. This package does not reclassify that theorem or claim
that every earlier gate has been evaded. It supplies a new literal source
and actual unit completion for a fresh admission test.

Credit @CubeJerry, the retained four-bit source and S019 spectator identities,
root and C's Klein-capacity observation, C's capacity theorem, B's dyadic
completion and source application, and substantial OpenAI assistance. All
five foundational assumptions remain.
