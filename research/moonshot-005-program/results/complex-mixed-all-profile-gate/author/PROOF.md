# The mixed return/clock interface cannot improve the three-native invoice

**Proved within the fixed finite collective-tail ordinary model, with arbitrary
fixed prefix matrices. Every independent three-bank Gaussian endpoint for this
specified first interface has total head rank at most six. This is not a gate
on changed first interfaces. No new kappa.**

## 1. Source, scope and inherited work

Retain the S020 source on sixteen one-column letters:

    A=C_b Rsrc,
    Rsrc:(a,b,c,d) -> (b,c,d,a), phase (-1)^(abd),
    C_b=((1+i)I+(1-i)X_b)/2.

Let s=SWAP_bc and h=SWAP_bc D_b D_c^-1, with input phase i^(b-c).
For tail width W write a=A^(tensor W), and use the same notation s,h for
collective tensor lifts. Any fixed prefix factor is an identity on these
source words. Let Pg=(I+g)/2 and Ng=(I-g)/2. The first ordinary interface is

    C=Rot12(s) Rot01(h)
     =[[Ph,-Nh,0],
       [Ps Nh,Ps Ph,-Ns],
       [Ns Nh,Ns Ph,Ps]].                              (1)

Here Rot_ij(g) has two-bank block [[Pg,-Ng],[Ng,Pg]]. Its paid unit and inverse,
8 ADD/8 SCALE/4 MONO in each direction, and return/clock gauges are inherited
from S020's `complex-return-clock-mixed-interface`. The present result is the
all-profile endpoint obstruction, not a new source unit.

The three native head matrices are

    L=[[a,0,0],[I,a,0],[0,0,I]],
    U=[[a,-a^2,0],[0,a,0],[0,0,I]],
    E=L C U Q L,                                      (2)

where Q is any actual ordinary three-bank unit, with ordinary inverse. The
proposed endpoint is O diag(F_r1,F_r2,F_r3) Iin, with O,Iin actual ordinary
units and each F_r an independent Gaussian head of rank r in {0,1,2,3,4}.
Input and output head gauges may differ; only Gaussian classes matter.

Ordinary coefficients and their inverses use one fixed finite catalogue of
root-four monomial tail words, with arbitrary matrices on a fixed prefix.
Scalar coefficients may depend on W; the catalogue and prefix may not grow
with W. A uniform endpoint must hold at arbitrarily large W divisible by four.
The theorem is not about the full matrix algebra at one width or a catalogue
that grows with W.

## 2. Ordinary and nonordinary coefficient cosets cannot cancel

For a fixed finite set of projectively distinct one-column unitaries g_j,
the normalized Hilbert--Schmidt Gram entries of g_j^(tensor W) are
(tr(g_i* g_j)/16)^W. Distinct projective classes have modulus less than one;
a sufficiently large W divisible by four makes the Gram matrix nonsingular
and removes root-four scalar cocycles. Thus distinct lifted word classes are
linearly independent. Tensoring fixed prefix matrix units preserves this
independence, including for W-dependent exterior scalar coefficients.

If v is a nonmonomial unitary and z is an ordinary finite-catalogue coefficient,
the supports of z and v z lie in disjoint right cosets G and vG of the full
projective monomial group. Consequently

    z0 + v z1 = 0, with z0,z1 ordinary  => z0=z1=0.    (3)

The same statement holds with a nonzero scalar multiplying either term.
This is a collective coefficient statement, not physical injectivity of I-v.
It permits ordinary zero divisors and arbitrary fixed prefix matrices.

## 3. Two exact nonmonomial witnesses

Set

    m=A^-1 h A^2,    q=A^-1 h s h A.                  (4)

The literal sixteen-letter matrices have respectively eight and four nonzero
entries per row. Neither is projectively monomial. Their full Gaussian block
ranks are three and two. These are fixed source identities; the checker
reconstructs their sparse matrices. The second witness is an involution,
q^2=I, with a nonzero physical plus eigenspace. Thus (3), rather than a false
one-width injectivity assertion, is essential.

The inherited return is A s A=B, an ordinary monomial. The clock words A h A
and A h A^2 have Gaussian ranks one and two; A^j has rank j for j=1,2,3.
Right multiplication by an ordinary monomial preserves Gaussian class.

## 4. Every positive-head endpoint needs all three classes 1,2,3

Write Q's last column as (p,z,w)^T. The rightmost L fixes its input bank,
so E's corresponding column is L C U (p,z,w)^T. Its first output entry is

    [a^2(p-z)+(a h a)(p+z)-a^3 z-(a h a^2)z]/2.     (5)

The class-zero part of the complete column is

    (0, B(p+z)/4, Ps w)^T.                           (6)

If all three endpoint heads are positive, class zero is absent. Therefore

    p=-z,       Ps w=0.                              (7)

We must have z nonzero. Otherwise p=0 and im(w) is contained in im(Ns), a
proper subspace of a whole bank. The column (0,0,w)^T has no left inverse,
contradicting invertibility of Q. At W>=1, rank(Ns)=(16^W-8^W)/2 before the
fixed prefix factor.

The following three components cannot vanish:

* Class three in the first output is -a^3 z/2, hence nonzero.
* Class two there is -a^2 z-(a h a^2)z/2. Multiplication by a^-2 gives
  -(I+m^(tensor W)/2)z. Equation (3) forces z=0 if it vanishes.
* Class one in the third output is Ns h a z. If it vanished, multiplication
  by a^-1 h would give (I-q^(tensor W))z/2=0. Equation (3) again forces z=0.

Thus the column has nonzero classes one, two and three. An independent
three-bank endpoint supplies at most the three classes of its three heads.
Every endpoint with three positive heads therefore has multiset {1,2,3},
and total head rank six. No second-interface column or endpoint basis was
fixed in this argument.

## 5. A zero head cannot produce total rank seven or more

If class two is absent, (5)'s class-two part gives

    (p-z)-m^(tensor W) z=0.

Equation (3) forces p=z=0. The remaining last column is then

    (0,-a Ns w,Ps w)^T.                              (8)

If class one is also absent, Ns w=0. Hence w=Ps w, and the column cannot have
a left inverse because rank(Ps)=(16^W+8^W)/2<16^W for W>=1.

With three ranks in {0,1,2,3,4}, a zero head and total at least seven require
{0,3,4} or {0,4,4}. Both lack classes one and two, so (8) excludes them.
Together with Section 4 this proves

    r1+r2+r3 <= 6.                                   (9)

## 6. Complete common-body consequence

Retain the target blueprint's optimistic three-native common-body price:

    P(t)=3[1]+6[7]+3[8],   [r]=r^t, 0<t<1.

These are three rank-one services, six rank-seven native body moves, and
three whole rank-eight idle moves. Three body segments give each target role
body rank21. An independent endpoint has T(t)=sum_j [21+r_j]. By (9),
monotonicity and concavity give T(t)<=3[23]. Strict subadditivity gives

    P(t)=3(1+2*7^t+8^t) > 3*23^t >= T(t).           (10)

This fixed interface therefore cannot be profitable at any 0<t<1, including
t=199/200, before any ordinary, prefix-restoration, precision, ownership,
erasure, source-normalization or recursive charges. The exact receipt gives
an outward rational interval for P(199/200)-3[23].

Changing C, adding natives/queries, changing body incidence, or leaving the
uniform fixed catalogue/prefix model changes a premise. The retained positive
gauges and unit remain valid. A different second Q or endpoint profile alone
cannot repair Cmix under this invoice.

## Reproduction, controls and next question

Run `python -B check.py --repo REPOSITORY_ROOT --out FRESH_OUTPUT`.
The checker pins the admitted exact arithmetic engine and inherited source
proof, reconstructs formal lifted-word coefficient identities, checks both
nonmonomial witnesses, records their physical plus-space control, and rejects
missing source terms and a phase-deleted h. Finite checks support the source
identities; Sections 2,4,5,6 provide the universal proof.

An actual unit `Cmix diag(I,r,I)` changes the middle-native source and may
invalidate (5)-(6). Some such transports move the two-source words into new
cosets; this is a possible escape, not an established endpoint. A candidate
needs its own full-column and complete-cost analysis.

Credit @CubeJerry, the inherited return/source and fixed-catalogue separation
results, S020 B/C, S021 B, and substantial OpenAI assistance. No complete
complex supplier, foundational discharge or new kappa is claimed.
