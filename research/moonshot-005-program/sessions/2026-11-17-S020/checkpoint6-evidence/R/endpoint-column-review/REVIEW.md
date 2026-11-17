# Independent review of the literal three-bank endpoint column

## Decision and exact scope

Accept the positive one-column identity and all five ordinary unit programs,
including their inverses. The construction has actual invertible input and
output endpoints on three arbitrary banks. It establishes one input column
of the desired quartic/quadratic/linear factorization. The displayed words
do not establish the other two input columns and are not a complex supplier.
Their full identity has the exact defect (-3+5i)/16 at row0,column0 of the
reduced prefix/tail-one realization. A subsequent obstruction to extending
this particular column must be stated separately from this positive result.

The review pins the author's WORDS.json at
`5fc8f08284825e5314edb4b35a19ac8afdf890bfa2a1863fab1d9ab8fac35979`
and PROOF.md at
`5eb77f12da9888d1efddf7ba444be788b9ab93b3652700775d3b464da34715ab`.
It imports only C's independent sparse rational-complex arithmetic, SHA256
`410c8426e31bc60e76d88095b2ef568c766b46f6dd5a66ff9e8ae9a980a542e2`.
It does not import or execute the author's matrix engine or construction.

## Mathematical review

Write a=I_prefix tensor A^(tensor W), after the explicitly paid first-column
normalization. Two of the four prefix bits carry sigma,tau controls; the
other two are identities. They contribute a common factor four suppressed
by the finite matrices in this review. No tensor width is inferred merely
from a finite numerical test.

The literal one-column source and R2 monomial are reconstructed directly
from their bit address and root-four phase rules. Exact arithmetic confirms
the one-tail identities that define S,S1,J,K,G. Their tensor products, with
the fixed sigma flip, prove a^-1 S a=S1, a J S a^-1=K, [J,S]=0 and
G S1 G^-1=-S for every W. The tau flip satisfies XT=-TX and commutes with
the tail source. The distinguished flip is essential: removing it gives
the opposite sign, at both tested widths and by the same tensor identity.

The three domain sectors N, P N1 and P P1 are orthogonal and sum to I.
Consequently p=N, z=X P N1, w=X G P P1 form an isometric column. The
literal Q0 word completes it to a unit; this is stronger than asserting
that the column has full rank. Its inverse is replayed on arbitrary inputs.

Using the source identities and Pz=Pw=0, S1z=-z, Sw=-w gives the entire
H L C U column

    (-a^2 z,-a^2 z,-a^2 z) + (-x,x,a p),
    x=a(-S J z+w).

There is no analytic projection or uncharged Gaussian query in this
equality. The displayed O0 sends the complete vector
(0,-c^-1 z,c^-1(-S J z+w)+X p) through diag(a^4,a^2,a) to this same column.
O=H^-1 O0 therefore gives the actual output endpoint. The input endpoint
I0 completes that vector by a paired prefix scale, a controlled bank swap,
monomials and a final shear. Its scale on one bank is accompanied by the
inverse scale on another bank and compiled through literal coefficient
shears. Both banks may contain arbitrary values throughout.

These are operator equalities over the exact coefficient field. The proof
uses only the preceding tensor identities and projector relations, so it
applies for every nonnegative tail width W. The reduced finite checks at
W=0 and W=1 additionally audit the detailed programs and source conventions.

## Primitive and inverse verification

Every stored ADD, SCALE and root-four MONO is replayed on every input column
of the three-bank unit. Both product orders with the stored inverse equal
the identity. Conditional monomials are reconstructed explicitly from the
prefix selectors and tail permutations, and checked to have exactly one
root-four entry in every row and column.

| Unit | Forward ADD/SCALE/MONO | Inverse ADD/SCALE/MONO |
|---|---|---|
|C|8/8/5|8/8/5|
|Q0|8/8/4|8/8/4|
|O0|20/28/15|20/28/15|
|O|22/32/16|22/30/16|
|I0|14/20/13|14/20/13|

The review also reconstructs each coefficient-service expansion from its
macro description and compares every resulting primitive instruction with
the stored word. A source bound is restored only after its explicit inverse
SCALE and MONO have executed. Thus the triangle bounds22/22,74/74,331/948,
958/2954 and74/47, respectively, are valid uniformly in W. Exact finite
prefix row bounds are recorded separately and never substituted for the
uniform argument.

The checker covers12 unit input columns and4 endpoint-column inputs at
reduced W=0, and192 unit input columns and64 endpoint-column inputs at W=1.
All104 omitted-ADD controls for C,Q0,O,I0 and their inverses fail, including
the paired-scale service. O0 is checked in both directions but not counted
again in that omission total. The exact complete-column identity is checked
independently of the unit replay. The two remaining input columns fail.

## Accounting and continuation

These receipts are local ordinary costs. The paid native prefix gauges,
three native calls, restoration of original-width target prefixes, and the
full source/body/precision/compiler/ownership/erasure/recursive invoice
remain additional obligations. No complete supplier, closed compiler
foundation, target saving or new complete kappa follows.

Run `check.py --repo PINNED_SOURCE --author AUTHOR_PACKAGE --out OUT`.
Credit B for the construction, C for independent arithmetic, the retained
source and prefix-normalizer predecessors, @CubeJerry and OpenAI assistance.
