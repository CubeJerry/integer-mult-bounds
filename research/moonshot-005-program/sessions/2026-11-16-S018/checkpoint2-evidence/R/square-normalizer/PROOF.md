# All monomial controls transported through the literal source square

**Working classification and constructive interface, pending separate review. No caller or new κ.**

Keep the literal four-bit source A and the admitted exact identity A²=U R, where U=C_a C_b and R=R2 is the actual phased monomial. Call a matrix monomial if each row and column has one nonzero entry; here every such entry is a fourth root of unity. We classify every monomial B for which A^{-2} B A² is also monomial.

## Exact class and count

Write a four-bit address as (x,z), with active pair x=(a,b) in F2² and spectator pair z=(c,d) in F2². Let W be the normalized two-bit Walsh matrix, W[k,x]=(-1)^(k·x)/2, and D[x,x]=(-i)^wt(x). The literal C convention gives U=i D W D on each spectator fibre.

Every admissible B is specified uniquely by:

- a permutation σ of the four spectator fibres;
- for each fibre z, an affine permutation π_z(x)=L_z x+t_z of F2², with L_z invertible;
- an input character q_z in F2² and a fourth root λ_z=i^e_z.

Its actual action is

    B|x,z> = λ_z (-1)^(q_z·x) i^[wt(x)-wt(π_z(x))]
                 |π_z(x), σ(z)> .                         (1)

There are24*384^4=521838526464 such literal monomials:24 choices of σ, and6*4*4*4=384 independent choices per fibre. No projective phase quotient is taken. The integer counts describe a finite family fixed before tensor width grows; they are not an enumeration of all its members.

Define l=L_z^{-T}(k+q_z). The conjugated core has the exact action

    U^{-1} B U |k,z>
       = λ_z (-1)^(l·t_z) i^[wt(l)-wt(k)] |l,σ(z)> .        (2)

Therefore Q_B=R^{-1}(U^{-1} B U)R is an explicit16-address root-four monomial, and

    A² Q_B = B A².                                         (3)

Every wrapper phase in R and R^{-1} is retained. If R|j>=i^r(j)|ρ(j)>, apply(2) at ρ(j), then ρ^{-1} to its output, and add exponent r(j)-r(final output). This is a concrete permutation/phase table for Q_B and its inverse.

## Proof of completeness

Since R is monomial, it suffices to classify B with U^{-1} B U monomial. Every column of U is supported on exactly one whole four-address spectator fibre. If N=U^{-1}BU is monomial, the identity BU=UN says that B maps the support of each such column to the support of another U column. Thus B sends each entire fibre bijectively to a fibre. Disjointness forces one permutation σ of the four fibres; an isolated cross-fibre address swap is excluded.

On a fibre put T=D^{-1}BD, taking D on the appropriate input/output fibres. Then U^{-1}BU=D^{-1}WTWD, so monomiality is equivalent to that of WTW. Write T|x>=η(x)|π(x)>. Every permutation of the four points of F2² is affine: an affine map is uniquely determined by the image of0 and an ordered basis, giving4*6=24 maps, exactly all permutations.

The image T W|0> has entries η(π^{-1}(u))/2. If WTW is monomial, this vector must be a scalar multiple of one Walsh column. Hence η composed with π^{-1} is a character times a constant, so η(x)=λ(-1)^(q·x). The constant is a fourth root because every η is. Conversely an affine π and such η send every Walsh character to another character. Directly,

    W T W |k> = λ (-1)^[L^{-T}(k+q)·t] |L^{-T}(k+q)>.

Undoing the two diagonal gauges gives(1) and(2). This proves necessity, sufficiency and uniqueness. It is a complete source-specific monomial classification, not a numerical-rank search claim.

## Relation to the Boolean square controls

For diagonal B, σ and every π_z are identity. Equation(1) becomes a constant fourth root times a character on each fibre:16 choices per fibre, hence16^4=65536 diagonal controls with monomial pullback. Restricting B to signs leaves8 choices per fibre and8^4=4096 Boolean controls, exactly Worker B's affine-on-(a,b) family. This extension does not replace that family's shorter implementation.

The Boolean pullbacks, and indeed every member with σ=identity, preserve the original a,b address pair: R sends that pair to the spectator pair, the core preserves spectators, and R^{-1} sends it back. Hence these pullbacks commute with both original quarter controls D_a,D_b. A nontrivial σ changes that pair and provides source-square controls outside this commuting class. This is a concrete structural freedom for the next interstage construction, not evidence that a new caller already works.

## All-width identities and actual cost

For every positive V, define a=A^⊗V, b=B^⊗V and q=Q_B^⊗V. Tensoring(3) gives a²q=ba², exactly. All one-column phases multiply, so the tensor phase is i raised to the sum of the actual input-indexed exponents. A constant factor i becomes i^V; no parity or projective phase is discarded. Each operator and inverse is a fixed finite monomial table with norm1 in Euclidean and coordinate maximum norms.

If a one-column pullback is not monomial, some column has at least two nonzero entries. Its V-fold repeated tensor column has at least2^V nonzero entries. Thus its own tensor power is not monomial at any positive width. This statement concerns the literal tensor power, not all linear combinations or arbitrarily redesigned ordinary bank interfaces.

The retained fixed-monomial compact bridge gives actual forward and inverse services for each emitted16-address table. A conservative generic recipe has at most(16−1)(2*4−1)=105 three-control hypercube edge gates, their separately paid translations for negative controls, and one input-indexed Z4 phase pass, per service. This is a conditional physical lowering with the inherited tariff O(N_field*((f log p)^tau+1)), where N_field is the full physical field volume (at least16^V), not the tensor width V; it is not a free permutation oracle. The smaller Boolean recipe can be used on that subfamily. No complete uniform supplier tariff is inferred from this finite list.

As one useful ordinary bank primitive, a shear destination += q(source) is implemented by applying q to the source bank, doing one whole-field ADD into the destination, then applying the actual q inverse to restore the source. It uses one ADD and two paid monomial services, no new whole-field owner, and norm1 monomial prefixes plus the usual ADD amplification. Inverse shear uses the negative ADD or a separately paid sign. Projector combinations, controlled bank permutations and more general interfaces require their own emitted recipes and costs; no arbitrary matrix inverse is granted.

## Verification, credit and remaining task

The planned independent local census checks all24*4^4=6144 root-four monomials on one active fibre and confirms exactly384, with the explicit dual-affine formula. Global source controls reconstruct the literal A,R phases and test all24 fibre permutations with varied conditional affine/phase data, plus a broken-fibre permutation and a noncharacter phase. These finite controls support the complete structural proof above; no521-billion-instance enumeration is claimed.

Root's classification extends Worker B's constructive Boolean square-control theorem. Retain @CubeJerry, four-bit source, phase/compiler and source-transport predecessor credit; substantial OpenAI assistance. Independent review remains required. A source-valid independent(4,2,1) endpoint, all ordinary/source/query/idle/precision costs, both strict suppliers, full recursion and all five foundations remain open.
