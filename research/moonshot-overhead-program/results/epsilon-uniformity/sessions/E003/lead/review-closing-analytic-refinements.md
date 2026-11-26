# Lead review of closing local-invoice and channel-rank results

Disposition: **accept both scoped theorems**. The lead read B's complete
optimal-local note at SHA-256
`991a31bd50685619602aeadae9e0a35f64ccde6853751d841581d282b156d86c`
and C's complete charged-rank note, including CR1--CR7, at
`9d4774510f8d2ab89c53ecfbcb5a5a3e2a5fb2deb024f2ef30dcb89da9cf55b2`.
This is mathematical reading and independent derivation, without a new
numerical replay claim.

For B's theorem, b<=4sqrt(x log2 x) and Lt>=2(x-b) give
t>=sqrt(x)/(8sqrt(log2 x)), hence log2 t>=log2(x)/4 eventually.
If t<8L, the two incidence inequalities imply
b>=sqrt(x)log2(t)/sqrt(32), contradicting the competitive range once
log2 x>8192. The stated larger cutoff suffices. The actual two-sided
moment now applies. Using F_L>=L!, t<=b and Lt>=2(x-b) gives
log2 L>=(log2 x-log2 log2 x)/2-2. With R=log2 x-log2 log2 x-7,
AM--GM yields b>=2sqrt((x-b)R), hence
b>=2sqrt(xR+R^2)-2R. The integer-profile upper bound matches up to
a bounded term inside the square root; additive O(log x) terms are
absorbable because (log x)^(3/2)/sqrt(x) tends to zero. This is exactly
the declared positive invoice, not arbitrary machine time.

For C's theorem, norm-one auxiliary restrictions force U_v!=V_v-perp.
Distinct scalar keys give invertible B-A, while permitted free support
gives BF=FA. Rank subadditivity proves N<=2rank(I-F). Native bit-flip
matching produces charged all-ones two-by-two blocks and proves sharpness
over every field. The field extension is only a rank-proof device.

The lead independently derived the g-channel extension. The maps
X -> B_a X-X A_a commute because all coefficient matrices are diagonal.
Their product kills each F_a and maps I to the invertible diagonal
product of B_a-A_a. Its expansion has at most 2^g multiples of C, each
of rank at most rank(C). Opposite-bit spans in the abstract orthonormal
model satisfy the endpoint conditions; first-difference channels sum
to minus all off-diagonal entries and leave a rank-one all-ones matrix.
No native multi-channel sharpness or free physical implementation follows.

The final report's routing review binds an earlier completion header.
Reverting only the three header lines of the current report reproduces
its reviewed hash
`8c7a0824fb7e7726542fa8a94b04f40e33979f6aec6b60a5515e4da340a01038`.
C's review binds the current report hash
`49f38dc699cae7aaa438928cb56c4fd6e880d751d37411c9382eccb54b2624cf`.
Scientific content is unchanged between those snapshots. Late results
are isolated in FINAL-ADDENDUM.md with their own proofs and reviews.
