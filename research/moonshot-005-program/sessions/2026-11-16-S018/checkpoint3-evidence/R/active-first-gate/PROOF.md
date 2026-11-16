# An injective first-column obstruction for every idle-preserving first interface

**Universal fixed-template theorem, pending separate final review. No caller or new κ.** This strengthens B's triangular-first-interstage argument to a full active two-bank matrix and complementary singular pivots. It permits an arbitrary invertible ordinary second interface, including noncommuting coefficients outside the complete source-square monomial class.

## Precise interface and hypothesis

Keep the literal source a=A^⊗V and the actual three-bank natives

    L=[[a,0,0],[I,a,0],[0,0,I]],
    U=[[a,−a²,0],[0,a,0],[0,0,I]].

An ordinary block is a finite linear combination of tensor lifts of literal root-four monomials. The complete finite catalogue, including the products used below and arbitrary ordinary endpoint encodings, is fixed before V grows. Retain all absolute tensor phases. Let π_r denote the retained Gaussian rank-r component at sufficiently large faithful widths; distinct projective word classes are separated by the admitted finite-unitary tensor theorem. Ordinary left/right multiplication preserves each Gaussian rank class. The independent(4,2,1) target necessarily has rankπ_1(E)=rankπ_2(E)=rankπ_4(E)=D, with every other component zero, where D is one full bank dimension. This necessary component test is the only endpoint criterion used here.

Let

    C=[[w,v,0],[g,h,0],[0,0,k]]

be an arbitrary ordinary unit. Thus the active2×2 matrix and k are units, but its individual w,v,g,h blocks need not be. Let Q be any ordinary three-bank unit. Define

    T_w=π_3(a w a²),   T_g=π_3(a g a²).

Assume the vertical2D×D operator [T_w;T_g] is injective at the widths under consideration. Neither T_w nor T_g is required to be invertible; complementary nonunit sector pivots are explicitly included.

**Theorem.** At every sufficiently large faithful width satisfying this stack-injectivity hypothesis, E=L C U Q L cannot be ordinary-equivalent to independent(4,2,1). Consequently a fixed finite template satisfying the hypothesis at every sufficiently large width cannot realize the target uniformly. This is not an arbitrary isolated-width obstruction or a theorem for every possible first interface. A successful caller must violate the stated first-interface structure or injectivity condition.

## The idle output fixes the last two input columns

The third row of L C U is(0,0,k). Therefore the final third row is

    (k q20 a+k q21, k q21 a, k q22).

Ordinary and rank-one components are distinct, so vanishing of the target's ordinary component forces q21=q22=0. Since Q is a unit, q20 is a unit: its last block row must have rankD. The last row of π_1(E) is then(k q20 a,0,0).

The rank-one image of input block0 has an invertible projection onto the last output block and already has dimensionD. Since rankπ_1(E)=D, the images of input blocks1 and2, which have zero last output block, must vanish. Thus π_1(E)[:,1]=π_1(E)[:,2]=0. This uses the complete component rank and makes no pivot assumption on Q.

## The stacked forbidden component forces q12=0

Literal multiplication gives the active part of L C U:

    [[a w a,          a v a−a w a²],
     [w a+a g a,     v a+a h a−w a²−a g a²]].            (1)

The final input block2 of E is (1) times(q02,q12)^T. Every one-column word with at most two A factors separated by ordinary monomials has at most four nonzero entries per row and column, so it cannot lie in a rank-three Gaussian class. Ordinary right multiplication preserves the class. Therefore the entire rank-three part of this last input column is

    −[T_w;T_g;0] q12.

The target has no rank-three component. Stack injectivity gives q12=0. Together with q22=0 this makes the last column of Q equal(q02,0,0)^T; Q’s invertibility forces q02 to be a unit. Here “unit” means invertible, not necessarily norm-preserving.

## The last-column rank-one equation forces w=0

The second output block in input column2 is now(w a+a g a)q02. Its rank-one component vanishes, hence

    w a+π_1(a g a)=0.

Multiply on the right by a^-1. The first term is ordinaryw. Expand g in its fixed finite monomial tensor words. Each selected rank-one word A G A becomes A G after right multiplication by A^-1, and A G is a rank-one Gaussian because G is ordinary. Thus π_1(a g a)a^-1 lies wholly in the rank-one component. Faithful separation of ordinary and rank-one classes forces w=0. The finite catalogue includes these stripped products; no width-one span argument or scalar-phase quotient is used.

Consequently T_w=0 and the stack hypothesis makes T_g invertible. Also, invertibility of the active matrix [[0,v],[g,h]] forces v and g to be units. With q12=q21=q22=0, invertibility of Q additionally forces q11 to be a unit. For example, a vector in kerq11 would give a nonzero kernel vector(0,z,−q02^-1 q01 z) of Q.

## The rank-two image leaves no place for a remaining unit

The last input column of E is exactly

    (0, a g a q02, 0)^T.

The middle block is a unit. Every word has at most two A factors, so there is no rank-four component. Its rank-one part is zero by the idle-output argument, and every ordinary or other unwanted class is zero by the target. Hence this column is a pure rank-two unit. It fills the entire middle output bank. Since rankπ_2(E)=D, the complete rank-two image is precisely that middle bank, and the top output row of π_2(E) vanishes.

But the top output block in input column1 is

    a v a q11 a.

It is a unit because a,v,q11 are units. Its rank-one component is zero because the entire input column1 has zero rank-one part. Its rank-two component is zero because the top output row has zero rank-two part. Every word has only three A factors and hence one-column support at most8, so it has no rank-four component. All other components are prohibited by the target. Faithful finite-word separation therefore says this unit is zero, a contradiction. The support assertion is wordwise; it does not pretend that an arbitrary finite sum has the same numerical support bound at widthone.

## A broad sufficient condition and complementary singular control

If a w a^-1 and a g a^-1 are ordinary, then a w a² and a g a² are already pure rank-three. Their vertical stack is

    diag(a,a) [w;g] a²,

which is injective because the first block column of the invertible active matrix is injective. Thus the theorem excludes every idle-preserving first interface whose two first-column blocks have clean forward source transport, for every ordinary second interface.

A useful nontriangular control is H=(D_b²)^⊗V, P±=(I±H)/2, and

    C_active=[[P+,P−],[P−,P+]],   k=I.

This is an actual conditional bank swap, hence an ordinary involution with the admitted paid recipe. Both first-column pivots are singular at every positive width. Their forward conjugates are the complementary projectors of(D_a²)^⊗V; the two rank-three parts together are injective. The theorem therefore applies without dividing by either projector. In the literal16-address control each pivot has rank8 and their stack has rank16.

The injectivity hypothesis is material. Put w=0,g=S^-1 D_b,v=I,h=0,k=I. C is an ordinary unit, but the words in a g a² have support at most4 and π_3(a g a²)=0. This is an excluded-premise control, not a positive421 construction. General idle coupling, a noninjective forbidden-component stack, changed native order or a different source remain outside this theorem.

## Verification, provenance and cost boundary

The companion checker independently reconstructs the literal source and formal noncommuting product(1), the third row and last-column equations. It checks the complementary-projector unit, individual/stack ranks, literal source transport and the failed-hypothesis clock control. These finite identities support the universal component proof; they do not establish tensor faithfulness by enumeration.

The result is a correctness gate, not a cost saving. Every hypothetical endpoint still owes the full native, query, ordinary, inverse, idle/storage, precision/tape, compiler and recursive invoice. Both strict suppliers and all five foundations remain open. Credit @CubeJerry, B's triangular proof and its independent stacked-pivot sharpening, root's full-active and zero-pivot extensions, and the retained source/component/finite-tensor predecessors. Substantial OpenAI assistance. No new κ.
