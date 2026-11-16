# The ordinary range of a source prefix excludes independent421

**Universal fixed-template theorem; v3 extends the separately frozen pure-quartic v2 theorem.** The statement permits noncommuting coefficients, zero divisors, and a nonzero lower-rank quartic residue. It does not exclude arbitrary isolated widths, a width-growing coefficient catalogue, or every three-native architecture.

Use the literal three-bank architecture E=L C U Q L, where C,Q are ordinary units, C=[[s,b,c],[t,d,e],[u,f,g]], and

    K=(a s a,a t a,0)^T, W=(0,s,u)^T,
    Z=(a b a,b a+a d a,f a)^T,
    F=(a c,c+a e,g)^T.

Free ordered multiplication gives

    L C U=[K+W a,-K a-W a²+Z,F].                         (1)

Assume K is pure Gaussian rank2 blockwise and K a is pure rank3. There are two sufficient hypotheses:

**A. Pure quartic.** K a[q10 a,q11 a,0] is pure rank4.

**B. Ordinary prefix range.** K is injective and there is an ordinary rank-D idempotent Pi with image(Pi)=image(K), where D is the full field dimension. Equivalently one may give an ordinary injective column V with an ordinary retraction and image(V)=image(K).

Under either A or B, independent421 is impossible for all sufficiently large faithful widths of the complete fixed finite coefficient catalogue. In B, Q is completely arbitrary ordinary and the quartic prefix need not be pure rank4.

## Proof of the range conclusion

Only the term -K a[q10 a,q11 a,0] can contribute rank4; every other source word has degree at most3. Under A the rank-D independent rank4 component is exactly that product, forcing K injective and image(E4)=image(K).

Under B, Pi K=K. Ordinary multiplication commutes with the Gaussian rank projections, so E4=Pi E4. The independent endpoint has rank(E4)=D=rank(Pi), hence image(E4)=image(Pi)=image(K). No assertion that a nonzero coefficient is a unit, or that one sector determines all sectors, has been used.

## Common conclusion

The last input column's rank3 component is -K a q12; injectivity makes q12=0. Its rank2 component is then K q02, whose image lies in image(E4). Independence of the rank2/rank4 output images forces q02=0. Q-unit makes q22 a unit. Its ordinary last-column part is(0,cq22,gq22), so c=g=0. C-unit now makes e a unit and the entire last column is(0,a e q22,0), filling the rank1 output image with the middle bank.

If the top block of K had a kernel vector, K would map it into this middle bank. Injectivity and independence of the rank4/rank1 images exclude that vector. Thus a s a and s are units. Also Q_A=[[q00,q01],[q10,q11]] and B=[[s,b],[u,f]] are units: Q is block lower triangular, and permuting C's rows gives the block triangular matrix [[B,0],[*,e]].

Project E to the top and bottom output banks using Jout. Literal multiplication gives

    Jout E=[M,0], M=diag(a,I) B U_A Q_A L_A.

Write P0=diag(a,I) B U_A. Then P0^-1 is in the source-word filtration F2, while Q_A L_A is in F1. The ordinary rank4 output column v has zero bottom block and a unit top block, because image(E4)=image(K) is a graph over the top bank. Selecting this column in an independent endpoint factorization yields

    P0^-1(Jout v) G4=Q_A L_A z,

where z is ordinary. Every nonzero left source word has column support at least4: its inverse has at most two rank-one source factors before the Gaussian rank4 word. Every right word has support at most2. The fixed finite catalogues are disjoint, so faithful tensor separation forces both sides to vanish, contradicting the unit top block. This is the reviewed inverse-support cut, not a support bound on arbitrary sums. QED.

Ordinary inverse closure used in the argument is algebraic: the full fixed root-four monomial algebra is finite dimensional and unital, so any ambient-invertible member has inverse in that algebra (injective left multiplication is surjective). The finite monomial catalogue stays fixed; coefficients may depend on width, with literal phases retained. This grants no physical inverse recipe or free service to a proposed construction.

## Concrete genuinely nonclean first column

Let F=Za, P=(I+F)/2, J the active-square swap, and

    C[:,0]=(I-P,J P,0)^T.

Use the literal monomial Kdec=A J A² S A^-3, S=SWAP_ab, whose table is

    |a,b,c,d> -> (-1)^(ad)|a,b xor ad,c xor ad,d>.

Put Fhat=a F a^-1 and O=R((I+Fhat)/2) diag(I,Kdec^-1,I), with the collective lifts understood. Kdec commutes with Fhat. Therefore O K has only its top bank nonzero. The original first C column is an isometry, and a is unitary, so K is an isometry of rankD. Hence

    Pi=O^-1 diag(I,0,0) O

is an ordinary rank-D projector onto image(K), uniformly at every width. The exact source classes AJA rank2 and AJA² rank3 prove prefix purity. Hypothesis B excludes independent421 for **every ordinary Q and every ordinary-unit completion of the remaining C columns** with this fixed first column. No assumption on Q belonging to G512 or on quartic purity is needed.

The exterior-i construction in `RESIDUE-SELECTIVE-COMPONENT-v1.md` realizes a full-D rank4 component and a full-D rank2 quartic residue with paid ordinary endpoints. It is a positive sharpness control for the distinction between A and B, and is excluded as a full caller by B. A genuinely surviving first interface must escape this ordinary-range condition (or change prefix purity/architecture), not only introduce a lower quartic residue.

## Dependencies and scope

The cut proof is `INVERSE-CUT-SUPPORT-GATE-v2.md`; v2's coefficient-algebra instance and its exact2048 checks remain valid unchanged. The generalized range argument is a proof, not an inference from those checks. The checker for the exterior-i component separately verifies literal source classes, projector range, full component ranks, exact primitive words/inverses, and external-i parity controls. No supplier, source-volume, precision, recursion, foundation or new-kappa obligation is discharged.

Credit the retained source and tensor-rank framework, @CubeJerry, root's independent ordinary-image sharpening and cut review, and OpenAI-assisted Worker B derivation/checks.
