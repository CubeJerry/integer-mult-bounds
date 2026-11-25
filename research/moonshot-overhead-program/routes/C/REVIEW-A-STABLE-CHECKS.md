# Independent review of stable Hermite checks

Status: **passed within the stated algebraic and finite-search scope**.
Independent agent review, not human review, a tape implementation or a kernel build.

Reviewed: `routes/A/stable-hermite-checks.md`, SHA-256
`dcbd5de6d0283903f7f891422979327a86ed9b103b78d2f7d87c2777fa3b008f`.
Later edits require delta review.

Both MGF bounds (S3) hold. For the positive bound the derivative of
`2t^2+t+(1/2)ln(1-2t)` is `2t(1-4t)/(1-2t)>=0` on `[0,1/4]`.
The negative bound follows from the fourth-moment estimate and `1+x<=exp(x)`.
Chernoff at `t=delta/4` gives the stated exponent `-delta^2 r/8`.
The sphere-net count `9^j`, quadratic-form factor two and union bound give
(S5) with room to spare. The separate bilinear net uses variance proxy one
and conversion factor `16/9`, yielding `(64/9)sqrt(M+r)<8sqrt(M+r)`.

The exact positive-definiteness search is valid, including when r>M.
Its tests and candidate enumeration have the stated charged exponential time
and polynomial workspace, apart from the separately declared enumeration of F.
This is not an efficient explicit construction.

The identities `L V=I` and `V^T R=I` hold. For z=+/-1,
`g(y)-z=-(y-z)^2(y+2z)/2`, confirming the supplied `D_z`. Extra correct rows
in J are harmless. Four predictor applications and the two-r-row table suffice.
The least singular value gives `||L||=||R||<sqrt(2/r)`; differencing and
duplication each cost sqrt(2), confirming both constants in (S8).
The denominator `2(det G)^2` and the determinant/norm estimates imply (S10).

The grouped one-level gain (S9) is valid when each dense row map is evaluated
out of place with fresh accumulators and retained inputs. Every partial map
then has a Frobenius bound polynomial in M,r times its maximum coefficient;
one must not multiply a whole-matrix norm for each scalar addition. Only a
fixed number of dense maps occurs, and the scalar-pencil factors add
O(D log m) to logarithmic gain. Physical routed-pencil norms remain outside
this proof, as the note correctly states. At the stated thresholds both terms
of (S11) are at most 1/32. Search, preparation, movement and space remain paid
obligations. No mathematical correction was needed.

Independent exact test:
`python3 -B research/moonshot-overhead-program/routes/C/verify_stable_checks_review.py`.
Final result passed: a deterministic 64-by-5 sign matrix satisfied 50 strict
Gram tests on all supports of size at most three; 100 rational all-input
Hermite matrix identities passed, including 50 exception-superset cases.
Omitting the right inverse caused 90 detected failures. These toy checks test
the algebra and strict inequalities, not the huge search space or the
probabilistic existence theorem. See `stable-review-verification.json`.

Implementation convention to preserve in a future caller: out-of-place dense
stage evaluation for the grouped gain estimate. No global overhead claim.
