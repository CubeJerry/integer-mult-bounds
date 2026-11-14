# Analytic recovery investigation checkpoint

Base: e54523517d0f03e58352e647c403a5af3e525a57. No new kappa; all five assumptions retained.

## Completed orientation and excluded duplicates

Fine-prime transfer, row-gap/Reference admission, old-catalogue obstruction, source-first normalized recovery and original-q extraction are covered by #1786/#6977/#6982/#6987/#6991/#6993/#6995. The old accretive Toeplitz audit handoff was substantially superseded by rational-unitary-FFT, FullToeplitz downset and physical-cut proofs. Their results are source claims; no independent replay here.

The complete periodic inverse #6905 already supplies a literal prepared line service. For each successful call the unconditional extract and merge each read both W-bit components on every target coordinate; merge writes both components. Thus at least 4TW payload reads and 2TW payload writes occur, besides rewinds, scalar products, output consumption, and setup. A serial tensor call on d axes consequently pays at least 4dTW reads and 2dTW writes. The three-transform recovery requires three such compression passes. Fine-family q=Theta(p), T p=Theta(n) would therefore give Omega(n p^epsilon). At the selected near-one epsilon this cannot fit n p^(1-kappa). This is only an implementation-specific necessary lower bound; #5571 already gives the related unfused q/(1+q) outer route, so publishing this familiar observation alone is not justified.

## Candidate mathematical continuation: lexicographic displacement

Let J_m be the strict lower shift, A any nonsingular m-square matrix, B=[[1,b],[c,1]] and H=A tensor B in ordinary lexicographic order. In even/odd order the lower shift is [[0,J_m],[I,0]], while H=[[A,bA],[cA,A]]. Therefore

Delta(H)=J_(2m)H-HJ_(2m)
 = [[(cJ_m-bI)A, J_m A-A J_m],[0,A(bI-cJ_m)]].

det Delta(H)=(-b^2)^m det(A)^2. The Stein displacement is

E(H)=H-J_(2m)H J_(2m)^T
 = [[A-J_m A J_m^T,(bI-cJ_m)A],[A(cI-bJ_m^T),0]],

so det E(H)=(-bc)^m det(A)^2. Hence when b,c nonzero both have maximal rank. These identities are currently derived by hand and checked in small exact symbolic cases, not yet independently verified.

For a tensor of g normalized two-point shifted Gaussian blocks, b_i=exp(-gamma_i(1+2s_i)), c_i=exp(-gamma_i(1-2s_i)), all b_i,c_i are positive and det B_i=1-exp(-2gamma_i)>0. Thus rank is 2^g in every axis-order lexicographic flattening. Inverses satisfy the same property because B_i^-1=(1-b_i c_i)^-1 B(-b_i,-c_i). A sum of r lower-times-upper Toeplitz generator terms has Stein rank at most r, so at least 2^g such terms are necessary for that single flattened-shear representation.

CRITICAL SCOPE LIMIT: this does not show the recursive Full compiler itself is expensive. A tensor of 2-point blocks has simple scalar-identity root shears and a direct g-stage tensor circuit even though its full lexicographic displacement is maximal. The result only rules out retaining low global displacement / a constant-length single-shear generator representation. No arbitrary regrouping or general batching impossibility is established. Parent must assess whether this scope is useful enough before publication.

Next: compare actual #5571 and FullToeplitz grouping contracts. Seek a constructive grouped service or a nontrivial source-specific barrier, rather than publish a redundant factor-d or unrelated representation lemma.
