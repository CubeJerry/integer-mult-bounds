# A free ordinary range needs an actual ordinary kernel channel

**Constructive interface, a scoped exclusion and an exact missing-channel reduction; independent review pending. No complete421 caller or new κ.**

The new ordinary-character gate excludes repeating the plus sector in both active outputs. The following family instead has an explicit ordinary one-bank ambient range at every width. Its two-source column is singular. The next distinction is whether that physical kernel contains any nonzero ordinary operator image.

Use the pinned source A and monomial controls F=Z_a, J=R2^-1 SWAP_ab R2, Fhat=A F A^-1=Z_d, and S=SWAP_ab in original coordinates. All are collective tensor lifts at width V. J commutes with F. Put

    P=(I+F)/2, M=I−P,
    Phat=(I+Fhat)/2, Mhat=I−Phat.

Let T0 be a specified literal monomial involution of trace0, T=(I+T0^tensor V)/2 and N=I−T. Thus T has rankD/2 for every positive V. We analyze two exact controls:

    failed T0 = J Z_a,
    surviving T0 = S Z_c.                              (1)

“Surviving” means it passes the proved gates below; it is not a successful caller.

## 1. Actual first interface and a free ambient range

Take

    C_old=diag(I,J,I) R01(P),
    C_new=C_old R02^−(T0),

where R01(P)=[[M,P,0],[P,M,0],[0,0,I]] and
R02^−(T0)=[[T,0,N],[0,I,0],[N,0,T]]. These are actual ordinary units. The first column is

    C[:,0]=(M T,J P T,N)^T.                             (2)

The full first column preserves arbitrary input: the missing T directions are carried by the third bank. The two-active-bank source column is

    K=(a M T a,a J P T a,0)^T
     =K_old a^-1 T a,
    K_old=(a M a,a J P a,0)^T.                           (3)

K_old is an isometry: M,P are orthogonal complementary projectors, J is unitary, and a is unitary. Thus K has rankD/2. The ordinary idempotent

    Pi=diag(Mhat,Phat,0)

fixes K. The actual ordinary decoder O=R01(Phat) satisfies

    O Pi O^-1=diag(I,0,0),
    O K=(a(M+JP)T a,0,0)^T.                            (4)

This is an all-width free-bank certificate, stronger than matching one character multiplicity. Its epsilon rank is1 and every other representation has the correct one-bank multiplicity. The old physical-injectivity gate does not apply to K.

## 2. The ordinary-column kernel lemma

Let G be any fixed nonmonomial one-column unitary. For every ordinary block R in the finite root-four tensor interface,

    (I+G^tensor V)R=0  implies R=0                      (5)

at all sufficiently large faithful widths of the complete finite catalogue. Expand R as a finite combination of monomial tensor lifts. The words in R are monomial, while every Gg is nonmonomial: right multiplication by a monomial preserves that property. The two projective catalogues are disjoint. Faithful tensor separation forces R itself to vanish. The coefficients may depend on width; the catalogue may not grow with width.

This is injectivity against ordinary operator columns, not physical injectivity. I+G^tensor V may have a large numerical kernel. An arbitrary vector from that kernel is not thereby an available ordinary input channel.

Apply this with

    H0=A^-1 T0 A, H2=A^-2 T0 A².

Since K_old is injective, K R=0 is equivalent to
`(I+H0^tensor V)R=0`. Likewise Ka R=0 is equivalent to
`(I+H2^tensor V)R=0`.

## 3. The first correct-character attempt is still excluded

For failed T0=J Z_a, exact literal matrices show both H0 and H2 are nonmonomial. Therefore K and Ka have no nonzero ordinary right annihilator, despite each having a physical kernel of dimensionD/2. Their rank2/rank3 source purity follows from exact Gaussian gauges for a², aJa, a³ and aJa².

Consider any ordinary-unit completion C of this first column and arbitrary ordinary Q in E=L C U Q L. All rank4 terms pass through K, so Pi fixes E4. An independent421 endpoint would give rank(E4)=D, hence im(E4)=im Pi.

The last input column's rank3 component is −Ka q12. Equation(5) forces q12=0. Its rank2 component is then K q02. Its image lies both in im Pi=im E4 and in the independent rank2 output image, so it vanishes; equation(5) forces q02=0. Q's last column becomes `(0,0,q22)`, making q22 a unit. Absence of an ordinary endpoint part forces C02=C22=0, and C-unit makes C12 a unit. The last input column now fills the middle bank with rank1. That contradicts directness because im Pi contains the nonzero middle-bank Phat subspace.

Thus the failed first column is excluded for every ordinary Q and every completion of the other C columns at all sufficiently large faithful widths. This is a new ordinary-kernel obstruction after the character test has passed. It does not rely on a failed finite search or on physical injectivity.

A sharp component control remains useful. For this failed T0, J P T=P T and M T+P T=T. With Q_seed=SWAP01, after O the quartic term has only its top-left block nonzero:

    −a T a³=−(a⁴+Fhat Kdec B2)/2,
    Kdec=A J A² S A^-3, B2=A³ S A.                     (6)

The rank4 and rank2 components are both full-D and occupy ordinary whole input/output banks, while their sum has rankD/2. So even a fully aligned rank4 component and a free ambient output image do not supply the missing ordinary kernel channel.

## 4. An exact source transport changes the kernel contract

For surviving T0=S Z_c, exact source algebra gives

    H2=A^-2 (S Z_c) A²=J Z_a.                           (7)

Indeed A²=C_a C_b R2, S commutes with C_a C_b, and
R2^-1 Z_c R2=Z_a. H0=A^-1(S Z_c)A is an exact rank2 Gaussian with actual monomial gauges, hence nonmonomial. Therefore:

* K R=0 still forces every ordinary R to vanish at sufficiently large faithful widths.
* Ka has the genuine nonzero ordinary right-kernel projector

      Rminus=(I−(J Z_a)^tensor V)/2.                    (8)

More precisely,

    Ka R=0  iff  R=Rminus R.                            (9)

This is an exact identity at every positive width. It is not inferred from a small-width nullspace. Both projectors have rankD/2, and their source/control tables and phases are explicit.

For this surviving source, K and Ka remain pure Gaussian rank2 and rank3. The checker supplies exact constructive gauges for A T0 A, A J T0 A, A T0 A² and A J T0 A², in addition to the baseline words. Thus the last input column's forbidden rank3 part forces

    q12=Rminus q12.                                    (10)

Moreover q12 must be nonzero. If q12=0, the ordinary-column injectivity of K forces q02=0 by the same independent-image argument, and the middle-bank rank1 contradiction from Section3 follows. A successful caller in this family must therefore use a genuine nonzero entry q12 through(8).

This is the next exact continuation interface. The source SWAP/sign construction changes a previously inaccessible physical kernel into a legal ordinary channel after the extra source factor. It does not prove that the remaining endpoint equations or invoice can be completed.

## 5. Physical controls and next proof task

C_new and its inverse each have an explicit8 ADD,9 SCALE,3 MONO word: two H2/H2^-1 conjugations implement the controlled routes, plus the literal J on bank1. T0=SZ_c is a coordinate SWAP and a sign pass; T0=JZ_a has J's retained coordinate/Toffoli implementation plus a sign pass. The words preserve all three arbitrary banks and add no owner. Q_seed and its inverse cost3 ADD,3 SCALE. O and its inverse cost4 ADD,5 SCALE,1 MONO. Exact invoices, prefix bounds and omitted-ADD controls are recorded by the checker.

These are actual ordinary interface costs only. Every native source, Gaussian normalization, full field volume, precision/tape, compiler and recursive expense remains. The prospective complete Gaussian421 invoice remains the existing `3[1]+6[7]+3[8]` against `[25]+[23]+[22]`, before the rest of the complete theorem. No supplier or exponent follows from these controls.

The concrete next task is to choose q12 through Rminus, complete Q to a genuine ordinary unit, and choose C's other columns so the rank2 residue cancels in the rank4 output while independent rank2 and rank1 jobs survive elsewhere. The simplest fixed C_new completions have been subjected only to finite exploratory filters; sampled failures do not exclude the surviving first-column family.

Credit @CubeJerry, the retained four-bit source and S018 selective-channel/coset framework, the S019 complex worker, and substantial OpenAI assistance. All five foundational assumptions remain.
