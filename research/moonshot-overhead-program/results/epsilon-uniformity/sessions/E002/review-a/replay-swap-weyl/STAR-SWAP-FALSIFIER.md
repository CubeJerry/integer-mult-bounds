# A retained free rectangle that does not admit termwise Weyl batching

Status: **proved scoped algebraic falsifier; independent review requested**.
This checks whether WEYL-STAR-BATCHING.md can immediately replace the
retained source middle maps. It cannot in the specific valid endpoint
coordinates exhibited below. This is not a physical lower bound and
not an obstruction to a new complete kernel.

## 1. An exact binary source geometry

Use the pinned Fourier construction at OpenAI math commit
3344da59991ed94f9ba711217b29c1d760badfa6, kernel.tex, with q=4 and L=2.
The labels are (a,b) in {0,1,2,3}^2 and their nondegenerate quotient
has Gram form

    <d_v,d_w> = 1 + HammingDistance(v,w) mod 2.

Write e_a=d_(a,0), for a=0,1,2,3. These four vectors are orthonormal:
<e_a,e_b> is one exactly when a=b. Put

    p = d_(0,1)+e_1+e_2+e_3,
    q = d_(0,2)+e_1+e_2+e_3.

They are orthogonal to every e_a, and

    <p,p>=<q,q>=0,  <p,q>=1.

Thus the six displayed vectors are independent in the actual quotient.
They span it. The sum of the four d_(a,0) and the sum of the four d_(0,b)
have the same Gram row (the constant-one row), so the corresponding
third nonzero b-direction is p+q. Every label direction then lies in
the displayed six-dimensional space. No larger formal label space is
substituted for the quotient.

The canonical first-differing-bit rectangle

    I={ (0,0),(1,0) },   J={ (2,0),(3,0) }

has distance one on every cross pair and nonzero weight -p_source(1).
Here p_source(k)=1-k/2, so its weight is -1/2. It is a genuine free
rectangle, not a zero-weight geometric enlargement. Its destination
span is H=span(e_2,e_3), with common complement
C=H^perp=span(e_0,e_1,p,q).

## 2. Valid source and destination coordinate lists

Fix source v=(0,0) and destination w=(2,0) within this rectangle.
For query j, choose at the source the ordinary coordinate basis

    query_j: e_0;
    auxiliary slots: [e_1,e_2,e_3,p,q].

Choose at the destination

    query_j: e_2;
    auxiliary slots: [e_1,e_0,e_3,p,q].

Use the paired dual list in the second half, as the source requires;
only p and q exchange their dual positions. These bases are fixed
independently of j. Every unrelated query coordinate stays a spectator.
The first endpoint transforms run along H, using auxiliary slots for
e_2,e_3. The final transposed endpoint transforms run along H^perp,
using destination auxiliary slots for e_0,e_1,p,q. All their axes are
therefore genuinely auxiliary, exactly as in the source proof.

The cross kernel pairs input C coordinates with output C-dual coordinates,
and H-frequency coordinates with output H coordinates. Use X_j,Z_j for
the two physical query fields and X_b,Z_b for the two fields of the
shared auxiliary slot that is e_2 at the source and e_0 at the destination.
Its middle permutation cross-swaps

    X_j with Z_b,   Z_j with X_b.

The other auxiliary coordinates undergo a fixed paired-half exchange,
independent of j, and the other distinguished query fields are untouched.
In particular there is no uncharged exchange of spectator query halves.
Define the composite registers

    x_j=(X_j,Z_j),   z=(Z_b,X_b).

After removing only the fixed exchange on the other auxiliary slots,
the exact middle permutation is

    P_j = swap(x_j,z).                                  (SS1)

These are complete 2f-bit registers, of alphabet size 2^(2f). The reversed
order in z is fixed once, independent of j. This is a relabelling of the
two physical coordinates, not an extra spectral transform. The removed
exchange acts on disjoint slots and commutes with every P_j.

Endpoint diagonal phases may multiply this map by nonzero signs. They
cannot change its underlying address permutation. The statement concerns
one fixed source/destination contribution in the chosen valid endpoint
coordinates, not the sum after rectangle cancellation.

## 3. No common scalar diagonalization of these query terms

For m>=3, let P_1,P_2,P_3 swap the shared auxiliary field with three
distinct query fields. The relative operators

    R_2=P_2 P_1^(-1),  R_3=P_3 P_1^(-1)

do not commute. In coordinate order
(auxiliary,query_1,query_2,query_3), the word (1,0,0,0) is sent by
R_2 R_3 to (0,0,1,0), and by R_3 R_2 to (0,0,0,1).
This holds for every composite alphabet containing 0 and 1; the source
already has four composite values at f=1. Interpret 1 as the pair (1,0)
in the displayed composite coordinates and keep other auxiliaries and
spectators zero. This is an address basis vector in the full occupied
array, not a restricted promise on the input data.

Suppose invertible common input/output changes L,R and scalar diagonal
matrices D_j gave A_j=L D_j R for every signed middle map A_j. Then

    A_j A_1^(-1)=L D_j D_1^(-1) L^(-1)

would commute for every j. Their underlying permutations include R_2,R_3
above and do not commute. Nonzero phases cannot identify two different
permutations of basis vectors. Thus even arbitrary common linear input
and output bases cannot simultaneously scalar-diagonalize this specified
middle-map family.

In particular one common change of basis cannot transform it to the
commuting Weyl-star family of the companion note. Different auxiliary
bases or complementary layouts change the proposed component and must
be analysed afresh; this note does not quantify over every such choice
or every way of sharing rectangle operations.

## 4. Exact limits of this falsifier

A single fixed weighted sum of the P_j can still have its own spectral
basis despite noncommuting summands. Newton stages often use the same
query weights, so this leaves an actual opportunity. Constructing and
applying that basis with the required tape and workspace invoice is a
separate unsupplied problem. Block diagonal representations are also not
excluded by the scalar-diagonal argument.

The complete original queries Q_j commute. Their full rectangle sum
cancels off-diagonal label transfers and restores those operators. The
obstruction above concerns termwise reuse inside one retained free
rectangle. It permits a basis obtained only after all cancellations,
or a different endpoint architecture. Applying the original full Fourier
basis would diagonalize all Q_j, but charging that basis is part of the
task and cannot be taken as a free solution.

No quantitative movement cost follows from noncommutativity. The result
explains why the Weyl-star executor is not immediately NI5 or RV-W. The
admitted unconditional multiplier remains V.

Credits: @CubeJerry, the pinned Fourier Gram/endpoint construction,
standard simultaneous-diagonalization algebra, and substantial ChatGPT
multi-agent assistance. This is a scoped written calculation, not a
runtime lower bound, full implementation, or formal certificate.
