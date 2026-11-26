# Independent review of the source star-swap falsifier

Reviewer: E002 conditional review C. Gate: **PASS for the exhibited valid endpoint coordinates and the simultaneous scalar-diagonalization falsifier**.

Reviewed complete `STAR-SWAP-FALSIFIER.md`, SHA-256
`5db06e11c67fba3e0ed5db2a060bf3616a40f42c5d2281853f58f50f50fd3ceb`.
I checked it against the pinned Fourier `kernel.tex` endpoint formula and common/paired-dual basis requirements. The conclusion is deliberately about this specified family of termwise middle maps, not every choice of endpoint bases or the full corrected query sum.

## 1. Actual quotient geometry

For q=4,L=2 the Gram formula is `1+Delta mod2`. The four e_a=d_(a,0) are orthonormal. The proposed p and q have zero pairing with every e_a, zero self-pairing, and mutual pairing one. Their six-by-six Gram matrix is therefore I4 direct-sum the nonsingular alternating two-by-two matrix, so the six vectors are independent in the actual radical quotient.

To see spanning explicitly, the Gram rows give

`d_(a,b)=d_(a,0)+d_(0,b)+d_(0,0)`

in the quotient. Moreover `sum_a d_(a,0)=sum_b d_(0,b)` because both sums pair as the constant-one row. Hence the third nonzero b-direction is p+q, and the displayed six vectors span all sixteen generators. This verifies the claimed rank six without treating the generators as formally independent.

The selected I x J has distance one on every cross pair. The source polynomial for L=2 is 1-k/2, making its free weight -1/2, so it is an actual nonzero source rectangle. H=span(e2,e3) is nondegenerate and its orthogonal complement is exactly span(e0,e1,p,q).

## 2. Endpoint bases and middle permutation

The source query direction e0 and the five auxiliary directions form a valid basis, as do the destination query direction e2 and its listed auxiliaries. Their paired duals exchange p and q only, since the other basis vectors are orthonormal. All bases are fixed independently of j.

The first partial transform acts along the source auxiliary e2,e3 axes; the final transposed transform acts along the destination auxiliary e0,e1,p,q axes. Thus the endpoint transforms obey the source's genuine auxiliary-only requirement.

After the first transform, the input C coordinates retain the query value in the e0 direction and the input H frequencies include the e2 coordinate. The cross kernel sends the former to the opposite-half destination auxiliary e0 slot and the latter to the opposite-half destination query e2 slot. Thus the actual two-half permutation cross-swaps X_j with Z_b and Z_j with X_b. Other auxiliary slots undergo only their fixed paired-half exchange, while every spectator query remains in its original half. Defining complete composite registers x_j=(X_j,Z_j) and z=(Z_b,X_b) makes those cross-swaps exactly swap(x_j,z). The reversed auxiliary order is fixed, and the other auxiliary exchange is disjoint from all these composite registers. This verifies the corrected SS1 on the entire occupied address space, without exchanging any unrelated query half.

The source diagonal factors may add nonzero phases but cannot change this underlying address permutation. This identifies a valid retained component, without claiming it is the only permissible component obtained from all possible basis choices.

## 3. Relative-operator criterion

For P_j swapping one shared auxiliary with query j, the relative permutations R2=P2 P1 and R3=P3 P1 send (1,0,0,0) to distinct positions when composed in opposite orders, exactly as displayed. The witness works over every address alphabet with at least two values. In the full array it tests the action on one address basis vector; it is not a promise that other occupied data are zero.

If invertible A_j have one common input/output scalar diagonalization `A_j=L D_j R`, each D_j is invertible and

`A_j A_1^(-1)=L D_j D_1^(-1) L^(-1)`.

All relative operators would commute. The actual relative monomial maps have the noncommuting relative permutations above. Nonzero phase coefficients cannot make distinct image addresses equal. Thus no such common scalar diagonalization exists for the stated family, even allowing arbitrary linear L and R.

This is stronger than merely observing that the unrelativized P_j do not commute: different input and output bases require the relative-operator argument, which the note supplies correctly. Only the fixed exchange on the other auxiliary slots is removed; it commutes with each P_j and cancels in the relative permutations. The composite register alphabet is 2^(2f), so the source already supplies at least four values at f=1. The witness value 1 means the pair (1,0) in those composite coordinates.

## 4. Correction history and scope

The initial 578b2ab snapshot described a common exchange of halves too broadly. The source kernel exchanges the active query and auxiliary halves, not the spectator query halves. My initial review repeated that overstatement. Its admission is withdrawn and superseded by this review of the complete 5db06e snapshot. The corrected full two-half cross-swap calculation above closes the issue and preserves the stated noncommutativity result. No historical unconditional result depended on that wording.


The result does not exclude a basis for one fixed weighted sum, a block-diagonal representation, another set of endpoint coordinates, sharing after cancellation, or a different kernel. The original complete Q_j commute; that fact is compatible with the noncommutativity of one rectangle's termwise middle maps. The note correctly keeps these distinct.

It therefore establishes a concrete reason that the proved Weyl-star component cannot simply be substituted term by term in this valid retained endpoint layout. No quantitative tape cost, unavoidable pass count, global lower bound or new multiplication envelope follows.

Credits: @CubeJerry; the pinned Fourier endpoint geometry; the batching author's exact witness; standard relative simultaneous-diagonalization criterion; substantial ChatGPT multi-agent assistance. This is a written source/algebra review, not a formal build or full-machine execution.
