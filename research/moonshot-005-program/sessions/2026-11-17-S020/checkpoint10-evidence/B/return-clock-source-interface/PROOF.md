# Return and clock gauges with a paid mixed three-bank interface

**Exact local source identities and an actual ordinary unit. No complete
endpoint or supplier. The simplest mixed interface is excluded from (4,2,1)
in Section 4; the source gauges remain available for a changed interface.**

## 1. Source and inherited credit

Use A=C_b Rsrc on sixteen letters, where
Rsrc:(a,b,c,d)->(b,c,d,a), phase (-1)^(abd), and
C_b=((1+i)I+(1-i)X_b)/2. Write D_j for phase i^(bit j).
The fact that s=SWAP_bc gives an ordinary A s A is **inherited**:
S019/checkpoint3-evidence/C/s3-review/REVIEW.md explicitly checks this return
and its six left S3 translates. Its checker records
`actual_return_monomial_A_Sbc_A`. This package supplies explicit gauges,
adds a phase-sensitive involution, and applies both in a paid interface.

Every formula tensors over the tail width W. Each monomial has a fixed
per-column address and root-four phase rule. No growing catalogue or
Gaussian-class extraction is introduced.

## 2. Two involutions and complete ordinary gauges

Set

    s=SWAP_bc, h=SWAP_bc D_b D_c^-1,
    K=Rsrc s, L=K D_b,
    r0=D_c D_d^-1, r1=D_d D_a^-1, r2=D_a D_b^-1.

Both s and h square to I. The action of h is (a,b,c,d)->(a,c,b,d),
with input phase i^(b-c); the phase reverses on its second application.
K maps (a,b,c,d)->(c,b,d,a), with phase (-1)^(acd). Thus K fixes b and
commutes with C_b and D_b.

The inherited return is the particularly simple monomial

    A s A = B,
    B:(a,b,c,d)->(d,1-c,a,b), with no phase.             (1)

Indeed C_b^2=X_b and the two cubic Rsrc phases cancel. Consequently
A s A^j=B A^(j-1) for every j>=1, with an actual ordinary inverse gauge.

The exact two-dimensional identity C_b D_b C_b=D_b C_b D_b gives

    A h A   = L A   r0,
    A h A^2 = L A^2 r1,
    A h A^3 = L A^3 r2.                                (2)

For the first identity commute K and D_c through C_b and use
Rsrc^-1 D_b D_c^-1 Rsrc=r0. The next two follow from
A^-1 r0 A=r1 and A^-1 r1 A=r2. These are literal monomial identities,
including their phases, so all tensor versions hold exactly at every width.

Applying or undoing an intervening s or h costs one MONO. Normalizing a
clock head in (2) to the retained A^j head uses one MONO at each endpoint;
the inverse uses the reverse monomials. Normalizing (1) uses the one left
MONO B or B^-1. Each pass has norm factor one. The native calls remain
charged; a source identity does not supply a free Gaussian query.

| g in A g A^j | j=1 | j=2 | j=3 |
|---|---:|---:|---:|
| I | 2 | 3 | 4 |
| h | 1 | 2 | 3 |
| s | 0 | 1 | 2 |
| sh=D_b D_c^-1 | 2 | 3 | 4 |

These are exact Gaussian ranks. The independent review reconstructs full
root-four monomial gauges to standard Walsh blocks. The h branch lowers
rank by one and the inherited s branch lowers it by two. No ordinary
backward conjugate of h is assumed.

## 3. Paid mixed interface and its active kernel

For an ordinary involution g write Pg=(I+g)/2 and Ng=I-Pg. Let Rot_ij(g)
act as [[Pg,-Ng],[Ng,Pg]] on those two banks. The mixed interface is

    Cmix=Rot12(s) Rot01(h)
        =[[Ph,-Nh,0],
          [Ps Nh,Ps Ph,-Ns],
          [Ns Nh,Ns Ph,Ps]].                           (3)

It couples three arbitrary input banks. Its inverse reverses and inverts
the two rotations. Each rotation is a literal controlled bank swap followed
by one MONO. Both directions cost 8 ADD + 8 SCALE + 4 MONO. The checker
replays all 48 input columns, both inverses, and all sixteen single-ADD
omissions, and records a uniform primitive prefix bound. No zero bank,
Gaussian query, new owner or erased input is used.

The native active first-column paths are

    a c00 a^2 = (a^3+a h a^2)/2,
    a c10 a^2 = (a^3-a h a^2+a s a^2-a sh a^2)/4.      (4)

They contain Gaussian classes 3,2,1. The previous Scd interface's pure
class-three kernel premise cannot be transplanted to this mixed source.

The actual active first-column kernel also deserves care. For
Kact=(Ph,Ps Nh)^T it is ran Nh intersect ran Ns. With d=sh,
s d s=d^-1 and d^4=I, its ordinary projector is

    E=(I-s)(I+d+d^2+d^3)/8.

The group-algebra relations give E^2=E=E*, Ph E=Ps Nh E=0; conversely the
two kernel equations force h v=s v=-v. At width W>=1 its dimension is

    (16^W-2*8^W)/8.

Here tr I=16, tr d=tr d^3=8, tr d^2=0, and all four reflections have trace8.
The kernel is zero at W=1 but has dimension16 at W=2. Its existence is not
an independent Gaussian endpoint or a free physical extraction operation.
Credit C's independent review for this exact D8 kernel calculation.

## 4. Scoped (4,2,1) obstruction for this simplest mixed interface

Keep Cmix fixed and write Q[:,2]=(p,z,w) in L Cmix U_native Q L. The
rightmost L fixes this input bank. Its first output entry is exactly

    [a^2(p-z)+(a h a)(p+z)-a^3 z-(a h a^2)z]/2.       (5)

Work in the retained fixed finite ordinary collective-tail catalogue
(with arbitrary fixed prefix matrices if desired). Uniform tensor class
separation makes its class-three part precisely -a^3 z/2. A (4,2,1)
endpoint has no class three, so z=0. The ordinary part of output1 is
B(p+z)/4: only the s terms in Ps Nh and Ps Ph have rank zero. Therefore
p+z=0, and p=0.

The remaining source column is (0,-a Ns w,Ps w). Class zero must vanish,
so Ps w=0. Then w maps into the proper subspace Ns. The column (0,0,w)
has no left inverse and cannot belong to an invertible Q. This excludes
(4,2,1) for this particular Cmix, including arbitrary ordinary Q and
endpoint units in the stated uniform finite-catalogue scope.

This is compatible with the active D8 kernel: that physical kernel is
not automatically the image of an ordinary z after the native a^2 path,
and the proof uses actual class separation at arbitrarily large widths,
not injectivity inferred from the width-one control.

The source gauges (1)-(2), paid unit (3), inverse and invoice survive. A
changed first interface must avoid the injective class-three coefficient
in (5), or establish a different endpoint profile with actual encoder and
decoder units. All supplier and physical compiler obligations remain open.

Credit @CubeJerry, the retained source, C's S019 return verification and
new D8 calculation, the retained controlled-swap compiler, and substantial
OpenAI assistance. No improved kappa or foundational discharge is claimed.
