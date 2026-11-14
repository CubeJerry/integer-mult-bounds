# Four exceptional chain types cannot attain the native proper-cover target

**Proposed all-field obstruction, conditional on admission of the separately
proved scalar equality classification. Independent review pending. No new kappa.**

## 1. Statement

Let k be any characteristic-two field. Let h0,h1,h2,h3 be independent
scalar directions modulo the native canonical code C. Consider a width2
native fitting A whose canonical quotient is contained in the chain

    E=span{(h0,h1),(h1,h2),(h2,h3)}.

Write chi for the exact capped proper-subspace-cover charge and S=222-chi.
At every positive-saving row the quotient selector U is a full-rank2-by3
matrix. Its exceptional type is the parameter t when

    ker U=span(1,t,t^2), or ker U=span(0,0,1) for t=infinity.

Rows whose kernel is not on this conic are called nonexceptional.

**Theorem.** If at most four distinct exceptional parameters occur among
the positive-saving rows, then S<=27, equivalently chi>=195. In particular
a chain fitting meeting the retained target chi<=194 needs at least five
distinct exceptional types with positive savings. Over F4 it must use all
five conic parameters. This is necessary, not sufficient.

If the four scalar directions are dependent, the separately reviewed
envelope-three theorem and sharp14 composition give chi>=201. Thus
degenerate chain representations do not create an omitted target case.

## 2. Inherited scalarization interface

For a deleting row the coefficient map is

    Phi(g)=U H(g),
    H(g)=[(g0,g1,g2)^T,(g1,g2,g3)^T].

The reviewed chain theorem proves I2 belongs to im(Phi). A scalar vector
c gives a support-contained scalar fitting row in the global code
C+span(sum c_j h_j) whenever c annihilates ker(Phi) and c dot a!=0 for
an identity preimage Phi(a)=I2. This follows by factoring c through Phi
as a matrix functional and applying that functional to the whole block
row. It requires no individually available scalar h_j and introduces no
physical-history claim.

Phi is invertible at nonexceptional rows. At exceptional type t its
kernel is the cubic line

    gamma(t)=(1,t,t^2,t^3), or gamma(infinity)=(0,0,0,1).

Every identity preimage a has rank(H(a))=2. Every cubic point has rank1.
The scalar proper-cover capacity is14 over every scalar extension. Its
equality classification states that a scalar fitting saving14 has exactly
seven positive-saving rows, each saving2, on an orthogonal seven-root set.
Only the absence of single-saving rows in that equality case is needed.

## 3. Six globally fixed scalar codes

Pad the occurring exceptional parameters to four distinct values after
extending k if necessary. Cubic points gamma1,...,gamma4 are linearly
independent by the Vandermonde determinant, including the infinity case.
Extension does not alter any fitting zero or real support geometry.

For each of the six pairs ij, put P_ij=span(gamma_i,gamma_j). Choose a
basis b,d of its two-dimensional annihilator and a fresh transcendental
z_ij, and set c_ij=b+z_ij d. All choices live in one common rational
function extension. For any base-field vector a,

    c_ij dot a=0 if and only if a belongs to P_ij.       (1)

Each c_ij therefore defines one globally fixed scalar quotient code.
Use its support-contained scalar row wherever the functional criterion
applies, and the canonical row elsewhere.

At an exceptional row of type i, every incident pair code ij is local.
Its identity preimage a cannot belong to P_ij: Phi kills gamma_i, while
Phi(gamma_j) has rank at most1, so no vector in that pair plane maps to
I2. Hence all three incident pair codes dominate the row. For a
nonincident pair, gamma_i is outside P_jl; genericity gives
c_jl dot gamma_i!=0, so this particular functional criterion does not
provide a row. We use only the three incident pair codes there.

At a nonexceptional row all six codes are local. An identity preimage
a belongs to at most one pair plane. Distinct planes for disjoint pairs
intersect only at0; planes sharing one index intersect in that cubic
line. A nonzero rank2 H(a) lies in neither kind of intersection. Thus at
least five of the six scalar codes dominate every nonexceptional row.

Let S_non be the saving weight of nonexceptional rows. Support containment
makes scalar chi no larger than block chi, including for rows saving2.
Summing the six scalar capacities gives

    3S+2S_non <= 6*14=84.                              (2)

This proof uses the six same global directions for all receivers. It
does not choose a different scalar code separately at each row.

## 4. Equality would require odd sums of even row weights

Suppose S>=28. Inequality(2) forces S=28 and S_non=0. All six scalar
capacities must be saturated, and every rowwise support-domination
inequality used in their sum must also be an equality.

Let w_i be the block-saving weight on exceptional type i. Only the two
incident types are used in scalar pair fitting ij, whose saving is at
least w_i+w_j. We have sum_i w_i=28, so

    sum_(i<j)(w_i+w_j)=3*28=84.

The sum of the six scalar savings is at most84. Consequently each pair
has scalar saving exactly14 and w_i+w_j=14, with no additional saving
created by scalarizing a covered row. The six pair equations force
w_1=w_2=w_3=w_4=7.

But each pair scalar fitting attains the classified equality14 and
therefore has only double-saving rows. Rowwise equality forces every
positive block-saving row it covers also to save2. Every exceptional
type occurs in three pairs, so each w_i is a sum of2s and is even. This
contradicts w_i=7. Thus S cannot reach28. Since S is integral, S<=27.

The argument also covers fewer than four occurring types: unused padded
types have weight0 and already contradict the equality pair equations.
It strengthens the previous three-type chi201 gate in a different scope,
without replacing that stronger numerical result when only three types
occur. Five or more types remain outside this six-code parity proof.

## 5. Verification and boundary controls

The universal argument is the exact linear-algebra and integer-equality
proof above. A separate finite checker enumerates the F4 selector maps,
all five choices of four conic parameters, the pair-plane incidences and
the identity-preimage rank condition. It checks that nonexceptional rows
miss at most one pair plane and exceptional rows of a chosen type avoid
all three incident planes. It also exhausts nonnegative integer weights
with sum28 under all six pair bounds14; the unique solution is(7,7,7,7),
which fails evenness. Removing the evenness premise admits that solution.

The fifth conic parameter gives a meaningful scope control: the six pair
annihilators from a chosen four-type set are generically nonlocal at a
row of the omitted type. The result does not exclude all F4 chains.
The known native chain fitting has cardinality216 and exact chi220, so
it remains a valid positive fitting control outside the target; its
existence is not new evidence of physical availability.

Dependencies and exact proof pins are recorded in SOURCES.json. Credit
the scalar equality, sharp14, chain-functional and canonical-rigidity
authors, @CubeJerry and OpenAI assistance. No physical acquisition, owned
restoration, recursive supplier, complete multiplication exponent or
foundational assumption is resolved by this theorem alone.
