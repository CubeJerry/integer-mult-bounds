# Independent C review of the lead order-five classification

Reviewer: E003 Route C. Result: **accepted in the exact stated word model**.
The reviewer authored the concrete O5 construction, but did not author
the lead's universal classification. This is independent AI-assisted
review of the classification proof, not independent authorship of the
gate, human refereeing or a formal-kernel certificate.

Reviewed `../lead/order-five-word-classification.md` in full, SHA-256
`489836f28e9b4da4f903a45f4af1d8ad2d0d5627bbbc7f8f5d8150231edab7c2`.

## 1. One-converter condition

For a symmetric determinant-one C with distinct reciprocal eigenvalues,
b is nonzero and neither eigenvector's second coordinate vanishes. If a
or d were zero, diagonal rescaling of C could not produce the everywhere
nonzero eigenbasis. Equivalently the displayed cross-ratio equation U4
would fail. Thus using the nonzero-entry criterion introduces no omitted
solution branch.

Multiplying U4 and substituting ad=1+b^2 gives

    a=lambda+tau b^2.

Putting v=b^2 and using the characteristic equation yields

    v=tau^2 v(1+v).

Division by v is valid by hypothesis, so
`v=(tau^2+1)/tau^2`. The formulas for a and d follow from
`tau mu=1+mu^2`. This also verifies the claimed general-characteristic
formula with Delta=lambda-mu; its signs agree with det C=1.

In characteristic two the square root already lies in K explicitly:

    b=(tau+1)/tau.

Thus the phrase "whenever the indicated nonzero b exists" causes no
hidden field extension. Tau=0 is excluded by distinct eigenvalues and
tau=1 forces b=0. The latter is precisely the reciprocal order-three
case. The one-converter condition by itself permits other orders.

## 2. Two-power swap condition

Cayley-Hamilton gives C^2=tau C+I. The two zero-diagonal equations for
C diag(s,t) C^2 are exactly U6. Its off-diagonal coefficient tau b^2
is nonzero. If its determinant vanishes, the rank is one and every
nonzero null vector has both coordinates nonzero. Therefore D is
invertible. The resulting product is invertible and off-diagonal,
which permits an invertible diagonal left normalization E.

Expanding the determinant independently gives

    ad(tau^2 ad+tau^2+1)+tau^2 b^4
      =1+b^2(tau^2+1).

Combining with U5 gives `(tau^2+tau+1)^2=0`. Because K is a field,
this implies tau^2+tau+1=0. After multiplication by lambda^2, it is
the fifth cyclotomic polynomial. Lambda cannot be one; hence it has
exact order five. Conversely the same equalities reconstruct the word,
and Frobenius injectivity forces b=tau. Both directions of Theorem U
therefore hold over every characteristic-two field in its stated model.

The normalized eigenbasis U1 and the concrete displayed O5 eigenbasis
differ by invertible column scaling. This is already allowed by B and
does not change the condition. All concrete finite-field codes match
the O5 construction's polynomial-basis encoding.

## 3. Independent finite replay and scope

Copied the lead note and checker into `review-o5-replay/` and ran that
copy. The receipt passes all 196 admissible ordered symmetric matrices,
12 one-converter solutions (eight of order fifteen and four of order
five), four simultaneous solutions, 2,700 invertible-diagonal trials,
three concrete identities and two negative controls. These finite
counts support the implementation; Sections 1--2 are the universal proof.

The classification fixes symmetry, determinant one, reciprocal distinct
eigenvalues, one left/right-diagonally scaled converter and the word
`E C D C^2`. It does not classify arbitrary powers, larger blocks,
nonsymmetric gates or general row mixing. In particular it is not a
proof that every possible useful spectral period must be five, nor a
running-time or multiplication lower bound. Those restrictions are
stated correctly in the lead note.

Credit: the lead classification, the Route C gate/repair construction,
the source interfaces and predecessor mechanisms, @CubeJerry, and
AI-assisted independent review.
