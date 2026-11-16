# Independent continuation review of the S018 complex checkpoint6

**Accepted in its stated scope, with one wording clarification. No new κ.**
Reviewed from the frozen local checkpoint6 evidence against the published programme baseline `ac2d74578f1abd6d802f3d15f114ca672029257f`. This is a fresh mathematical read and independently written literal reconstruction by the S019 complex worker, not a rerun of the S018 author or reviewer executables. The exact bytes read are pinned in `RESULT.json`.

## The quantified ordinary-range gate

For the fixed finite tensor-word catalogue, write `E=L C U Q L` and `K=(a s a,a t a,0)^T`. Assume K is pure Gaussian rank2, Ka pure rank3, K injective, and an ordinary rank-D projector Pi satisfies `Pi K=K` and `im Pi=im K`. All ordinary coefficients and inverses stay in the declared finite monomial coefficient algebra. A complete independent421 endpoint has three ordinary output subspaces, pairwise disjoint, each of dimensionD.

I checked the complete chain:

1. Only the quartic prefix can produce Gaussian rank4. Since ordinary left multiplication commutes with the class projection and Pi fixes K, it fixes the entire rank4 component. RankD forces `im E4=im Pi=im K`, even when the quartic term contains lower Gaussian classes.
2. In the last input column, only `-Ka q12` has rank3. Its vanishing and injectivity of Ka force `q12=0`.
3. The remaining rank2 part is `K q02`. Its image is both inside `im E4` and inside the independent rank2 output image, hence it is zero. Injectivity forces `q02=0`.
4. Ordinary Q is invertible and has final column `(0,0,q22)^T`, so q22 is invertible. Absence of an ordinary endpoint part forces `c=g=0`. Invertibility of C then makes e invertible.
5. The final input column is `(0,a e q22,0)^T`, filling the middle bank with the rank1 image. If the top block of K had a kernel, an injective K would send a nonzero input into this middle-bank image, contradicting directness. Thus s is invertible. This step does not assume the individual s/t entries are initially units.
6. Projecting top/bottom gives `[M,0]` with `M=diag(a,I) B U_A Q_A L_A`, `B=[[s,b],[u,f]]`, and B,Q_A invertible by block triangularity. The selected ordinary rank4 output column remains nonzero after this projection.
7. The inverse of the left prefix expands into a fixed catalogue with at most two inverse rank1 sources per word. Applied before a rank4 Gaussian, each individual word has column support at least4. The right side is in the one-source catalogue with support at most2. These are disjoint projective word classes. Faithful tensor separation forces a zero selected output column, a contradiction.

The last step correctly separates individual unitary word catalogues; it does not assert a false support lower bound on arbitrary sums. The finite-dimensional inverse-closure argument is valid: injective left multiplication on the finite unital algebra is surjective. No physical inverse is granted free. The conclusion requires sufficiently large faithful widths for each fixed finite catalogue and does not claim every isolated small width is excluded.

## One clarification that does not affect the proof

The phrase "Equivalently one may give an ordinary injective column with an ordinary retraction" should be read as **an alternative sufficient certificate**, not a general equivalence of hypotheses in an arbitrary semisimple ordinary coefficient algebra. For example over `Q x Q`, the projector `diag(e+,e+,0)` has component ranks `(2,0)` and the same physical rank as one bank in balanced representations; one free bank has component ranks `(1,1)`. Such a projector need not be the image of a free one-bank ordinary column.

The proof uses the ordinary projector directly, then obtains a free ordinary column from the hypothesized independent endpoint. It does not use the overbroad converse. The explicit aligned construction separately supplies an ordinary decoder, so its certificate is also unaffected. Preserve the frozen proof bytes; clarify the wording in the current admission or an addendum.

## Positive controls independently reconstructed

`check.py` rebuilds the literal four-bit source, R2, the active swap J, the spectator swap S, the sign controls, and the explicit `Kdec:(a,b,c,d)->(a,b xor ad,c xor ad,d)` with phase `(-1)^(ad)`. It verifies involutions, commutations, both source intertwiners and the identity relating the lower quartic channel to B2. It independently reconstructs the two ordinary first/second interfaces and both boundary controls.

The exact quartic component reduces to a single block `-a^4` in the projector case, and to the row `[-B2,-a^4,0]` in the exterior-i case. The first-column K is an isometry, the output decoder carries it into one bank, and the advertised ordinary idempotent fixes its image. All identities are checked in bounded Gaussian-integer/dyadic arithmetic. Multiplicative one-column identities tensor; collective projector algebra is applied afterward. Exterior i remains i, and the even-width scalar-substitution negative control is retained.

These components are not two or three independent completed jobs. Existing S018 ordinary primitive invoices and omitted-ADD negative controls are covered by the separately read/pinned S018 reviewer receipts, not claimed as newly replayed in this check. The current script reconstructs the operators rather than their already reviewed primitive decompositions. The final cost boundary correctly states that C,Q,O,R counts omit any subsequent simultaneous Gaussian normalization and the entire native/supplier/recursion accounting.

## Scope retained

The original five foundational assumptions, strict complex supplier, actual full endpoint and complete κ=1/200 theorem remain open. The new next direction must change the ordinary-range/injectivity/purity premises or the architecture. No finite search failure has been promoted to a universal theorem. Credit @CubeJerry, the retained source and tensor-separation work, the S018 construction/review authors, and substantial OpenAI assistance.
