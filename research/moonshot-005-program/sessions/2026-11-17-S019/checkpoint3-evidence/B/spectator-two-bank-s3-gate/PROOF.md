# A universal S3 defect excludes the spectator two-bank pencil

**Universal source-specific obstruction. Independent review pending. No full421 caller or new κ.**

This proof closes the simplified Gaussian1-isolating family of the preceding two-bank reduction. It allows every finite ordinary root-four monomial catalogue, including nonlinear permutations and arbitrary sums. It does not impose diagonal endpoint alignment. The general three-bank spectator-kernel construction remains open.

## 1. Statement and exact scope

Retain the literal four-bit source a=A^tensor V, the collective spectator projector

    T=(I+S_cd^tensor V)/2, N=I-T,

and

    B_T=[[a T a,-a T a²+a N a],[N a,-N a²+T a]],
    L2=[[a,0],[I,a]].

Let R be any2x2 block matrix of ordinary operators in the retained fixed finite root-four tensor interface. It need not initially be assumed invertible. Suppose every entry of E=B_T R L2 is a finite sum of exact Gaussian rank2 and rank4 words at all sufficiently large faithful widths of its complete catalogue.

Put s=S_ab^tensor V, r=S_ad^tensor V, and let G=<s,r> be the six-element collective coordinate-permutation group S3 on the a,b,d registers. Define

    Ps=(I+s)/2, Ms=I-Ps,
    Pr=(I+r)/2, Mr=I-Pr,
    Sigma=(1/6) sum_{g in G} g,
    W=Ps-Sigma.                                    (1)

Then

    W R10=W R11=0.                                 (2)

At every positive width, writing q=2^V and D=q^4,

    rank(W)=q²(q²-1)/3 > 0.                         (3)

Consequently R is singular at every sufficiently large faithful width. No such R gives independent Gaussian(4,2) endpoints. In particular the preceding exact rank1-isolating reduction cannot complete a421 caller by changing or enlarging R's ordinary coefficient catalogue.

Independent ordinary endpoint units are included: they preserve each Gaussian class, so any endpoint-equivalent E necessarily has only the classes2,4 assumed above. No prescribed endpoint gauges, image alignment, or finite-width rank extrapolation enters the theorem.

## 2. Coefficient spaces and separation

Let M be the finite group of literal root-four monomial matrices on the16-point one-column field. Brackets [X] denote the coefficient span of collective lifts of monomials in a projective-phase-invariant subset X of M. All projective root-four phases are absorbed with their actual width-dependent scalar. At sufficiently large faithful widths, coefficient projections onto subsets of M and source-word classes are well-defined.

As in the prior component-character proof, every projective relation U=lambda V between unitary Gaussian-dyadic words has a fourth-root phase: lambda is the inner product of a corresponding pair of unit columns and lies in Z[i,1/2] with modulus1. Thus the faithful source-word separation theorem applies with the exact phases, at any sufficiently large width in the chosen residue class. Coefficients may depend on width; the complete catalogue may not grow with it.

Define four subsets of M:

    C={g: A² g A is exact Gaussian rank2},
    E={g: A³ g A is exact Gaussian rank2 or4},
    D2={g: A g A is exact Gaussian rank2},
    H={g: A g A is ordinary monomial}.               (4)

For example, if a² x a is pure rank2 with x ordinary, then x belongs to [C]. This follows because distinct projective monomials g produce distinct projective words A²gA, and faithful tensor separation excludes cancellation between different source classes.

Two elementary disjointness facts will be used repeatedly:

* The word catalogues a^k M a and a^(k+1) M a are disjoint projectively. Equality would make A times an ordinary monomial ordinary, whereas every column of A times a monomial has two nonzeros.
* The catalogues a M a and a M are disjoint for the same reason. The intersection between a² M a and a M is exactly the return coset H: A² g A=A h with h ordinary iff A g A=h is ordinary.

These are source-word statements before tensor lifting. They justify the coefficient decompositions below, without assigning a Gaussian class to a sum by its numerical rank.

## 3. Three source properties behind the S3 column lemma

All the following are literal source identities or support arguments, independently checkable on one column and then lifted collectively:

    A S_ab A^-1=S_ad,
    A S_ad A^-1=S_cd,
    A² S_ab A^-2=S_cd,
    A³ S_ad A^-3 is ordinary monomial.              (5)

The checker emits the exact table of the last monomial. The first two identities show that left multiplication by every element of G preserves D2 and H. The third shows that C is invariant under left multiplication by s. The fourth shows that E is invariant under left multiplication by r.

Also

    C cap E is empty,
    C cap H is empty,
    D2 cap H is empty.                              (6)

For the first claim, use A²=C_a C_b R2. If A²gA has Gaussian rank2, each of its columns has four nonzeros. The rightmost one-bit butterfly initially supplies two coordinates. After the monomial R2 g, if those two coordinates lie in different active(a,b) four-point fibers, C_a C_b produces eight nonzeros with disjoint support. They must therefore lie in the same fiber; the resulting rank2 column fills that entire four-point fiber. Columns of A have identical two-point supports exactly when their input coordinates differ in bit c. A four-point(a,b) fiber contains no such input pair. Thus left multiplication by A doubles each of its four nonzeros without overlap, producing exactly eight nonzeros per column. A³gA can be neither rank2 (four) nor rank4 (sixteen). This proves C cap E empty for ALL literal monomials g, including nonlinear permutations and arbitrary root-four phases.

If g belongs to H, then A²gA=A(AgA) is rank1, so it cannot belong to C. The last disjointness is immediate from the definitions.

## 4. An abstract S3 column lemma

Let p,z be ordinary operators, and suppose

    x=Pr p+Mr z belongs to[C],
    v=Ms z belongs to[C],
    y=Ps z belongs to[E].                           (7)

Then

    y=Sigma z,  W z=0.                             (8)

**Proof.** Let S be the G-saturation of C. Because s C=C and s,r generate S3,

    S=C union r C union s r C.

Let Pi_S be coefficient projection onto[S]. It commutes with left multiplication by G. The support of y avoids C by(6), and avoids r C because r E=E. Since s y=y, it also avoids s r C. Thus Pi_S y=0. Both x and v lie in[S].

The identity Mr x=Mr z, followed by projection outside[S], gives Mr y=0, since z=y+v. Hence r y=y as well as s y=y. Therefore Sigma y=y. Since Sigma v=Sigma Ms z=0, Sigma z=y. Subtracting from Ps z=y proves W z=0. ∎

This lemma does not assume that the original coefficient catalogue is itself G-invariant: adjoining its finite G-saturation is part of the complete proof catalogue.

## 5. Expand the pencil into four coefficient combinations

Write the two rows of R as(p0,p1) and(z0,z1). For j=0,1 define ordinary coefficients

    xj=Pr pj+Mr zj, uj=Mr pj+Pr zj,
    yj=Ps zj,       vj=Ms zj.                       (9)

The exact transport identities give

    E01=a² x1 a-a³ y1 a,
    E11=a u1 a-a² v1 a,
    E00=a² x0 a-a³ y0 a+a² x1-a³ y1,
    E10=a u0 a-a² v0 a+a u1-a² v1.                 (10)

No commutation between arbitrary coefficients and a is used.

The second-column source cosets in Section2 are disjoint. Since E has only Gaussian classes2,4 and its lower row has at most three source factors, (10) implies

    x1 in[C], y1 in[E], u1 in[D2], v1 in[C].        (11)

Apply the column lemma to p1,z1:

    y1=Sigma z1, W z1=0.                           (12)

## 6. The rank1 return term forces y1 to vanish

Consider the last equation of(10). The term a u1 is pure rank1, and a²v1 is pure rank2. A forbidden component of a u0 a cannot cancel either a u1 or a²v0 a: their source cosets are disjoint; a²v1 has only the allowed class2. Therefore

    u0 belongs to[D2].                             (13)

The rank1 term a u1 can be canceled only by the part of a²v0a in the return coset a M. By Section2 that is exactly H. All other non-rank2 parts of a²v0a must vanish separately. Consequently there are unique coefficient parts

    v0=c+h, c in[C], h in[H],
    u1=a h a.                                      (14)

Because H is G-invariant and v0=Ms z0, coefficient projection onto[H] gives h=Ms h. Using a Ms=Mr a from(5),

    u1=Mr u1.                                      (15)

The inverse of the two-sector routing in(9) says

    z1=Mr x1+Pr u1.

Equations(15) and(11) therefore imply z1=Mr x1, so r z1=-z1. Its G-symmetric component vanishes. By(12), y1=Sigma z1=0. In particular s z1=-z1 as well. Thus z1 lies in the alternating S3 sector. That sector is NOT zero at all widths: its rank is q*binom(q,3), which becomes positive for V>=2. No step assumes otherwise.

## 7. Eliminate the return exception and apply the column lemma again

With y1=0, the E00 equation in(10) contains a²x1 only in the allowed class2. The two remaining source cosets are disjoint. Hence

    x0 in[C], y0 in[E].                            (16)

By(9), z0=Mr x0+Pr u0. The coefficient projection onto[H] commutes with Mr,Pr, while H is disjoint from C and D2. Equations(13),(16) therefore give a zero H component in z0. Applying Ms shows that h, the H component of v0, is zero. Thus

    u1=0, v0 in[C].                                (17)

Now(16),(17) satisfy the column lemma for p0,z0. Therefore W z0=0. Together with(12), this proves(2).

The proof also yields Pr p1=p1 and z1 in the alternating S3 sector. These are additional exact constraints, not an assertion that z1 always vanishes.

## 8. Nonzero physical defect at every width

After regrouping tensor coordinates into the a,b,c,d registers, each register has dimension q=2^V. The group G permutes the a,b,d registers and fixes c. The symmetric projector Sigma has rank

    q*binom(q+2,3).

The transposition s has trace q³ on the D=q⁴ dimensional field, so Ps has rank(q⁴+q³)/2. Since Sigma is a subprojector of Ps,

    rank(W)=(q⁴+q³)/2-q*binom(q+2,3)
           =q²(q²-1)/3.

Thus(0,W) is a nonzero left annihilator of R. The bound is4 at width1 and80 at width2, exactly matching the discovered finite-width defect, but the theorem follows from Sections2-7 and the representation calculation, not from those samples.

## 9. Consequence for the continuing programme

The exact two-bank reduction remains correct, its actual fixed primitive receipts remain valid, and its pure-cubic gate remains a valid weaker obstruction. The missing ordinary R does not exist under its stated source/interface contract. This result supersedes that reduction's open feasibility status.

The broader spectator two-kernel three-bank construction is not excluded: it need not isolate its Gaussian1 output through this prescribed C_T and row-sum Q_R. The next architecture must change that restriction or change the spectator projector/source contract enough to evade the proved S3 coefficient-space properties. Every new source, endpoint, inverse and cost still has to be proved. No new supplier or complete κ follows from this scoped obstruction.

Credit @CubeJerry, the literal source and S018 native-coset framework, S019 complex construction and independent review, and substantial OpenAI assistance. All five foundational assumptions remain.
