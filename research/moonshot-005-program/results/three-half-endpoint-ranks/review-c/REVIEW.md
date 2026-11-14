# Independent review: fresh inverse-cross path ranks

**Accepted with the stated source, fresh-stage and endpoint scope. No new κ.** This review binds author proof `a59e5484f347863607b87c44dfdc25125fd89d43620f38adaf34b87160d0b2f5` and freeze `bb2861c8428b6402256e5ec771ac45bac08644fbabacbd9876bbe5c98c2a5530` at `worker-a/three-half-endpoint-ranks`.

## Direct proof review

Write each path operator as a Gaussian convolution followed by an invertible binary linear permutation. If K is the convolution's binary symmetric Pauli kernel, a left permutation conjugates K and a left C_q or C_q inverse adds qq^T. Translations affect only signs. These rules are exact for the source's orthogonal routes; scalar whole-array R coefficients multiply path amplitudes without changing support.

Initially K is the projection onto all8m fresh axes. For the new edge j to h in stage s, P=P_(s,h)P_(s,j). The pullback P^T q_h=P_(s,j)q_h lies entirely in the unused fresh-s block because the actual edge normals are orthogonal. Thus it is a unit eigenvector of the old K. After conjugation, q_h is a unit eigenvector. Adding qq^T removes exactly its one-dimensional orthogonal summand: the new symmetric idempotent projection has rank one less. Every other unused fresh block is still fixed and uncoupled. This proves rank8m−r for all distinct-stage paths, without relying on the finite enumeration or assuming any properties of the summed operator.

The exact support assertion also holds. For a normalized Fourier multiplier i^φ(z) with polarization2 z^T K w, the squared magnitude of its Fourier sum reduces to a character sum over ker(K). On that kernel φ is even and defines a linear sign character. The character sum is supported on one affine coset of ker(K)^perp=image(K), of size2^rank(K), and all surviving squared magnitudes are2^-rank(K). Hence a nonzero width-V path has exactly2^(rank(K)V) support per row. Different paths may cancel or coincide; summing at most4^r paths gives only the claimed upper bound.

At m=3 this yields first-bank bound4·2^(23V) and second-bank bound64·2^(21V). For V>=2 their joint maximum is4·2^(23V). Using the joint maximum is essential once arbitrary bank mixing is allowed. A scalar ADD can at most double this support bound, while a monomial on either side preserves it. Therefore a rank25 target requires at least2V−2 such branching factors. A fixed or sublinear ordinary recipe cannot supply the missing support. This is not a paid-moment lower bound, a general ordinary-complexity theorem, or an exclusion of additional Gaussian layers or width-growing decoders.

The all-positive three-half caller chronology remains a separate dependency: this package proves the stated operators' path ranks and support even before that chronology is independently admitted. It does not claim that a path sum is a single productive Gaussian job.

## Independent computational evidence

`check.py` imports no author code. It replays112 independent source columns, recovers448 authentic symmetric orthogonal edges, and constructs all actual stage permutations from their pinned orthonormal bases. Unlike the author's sum-of-outer-products representation, this review directly conjugates33-column binary K matrices. It checks448 first paths of rank23,1792 two-stage paths of rank22, and7168 triple paths of rank21, including exact projection identities. A repeated stage restores rank24, and a nonorthogonal self edge gives rank25, confirming that both central hypotheses matter.

The checker additionally evaluates1024 exact Gaussian-integer Fourier-sum cases in dimension three, including singular/dependent kernels and all linear translations. Every case has the proved support and amplitude. These controls illustrate the general Gauss-sum argument; they do not replace it.

```bash
python check.py --output RESULT.json
python -O check.py --output RESULT-OPTIMIZED.json
cmp RESULT.json RESULT-OPTIMIZED.json
```

Both receipts are byte-identical. Credit Worker A for the theorem and source-bound package, Worker B for the source and separate caller, and Worker C for this independent proof review and direct-matrix reconstruction. Prepared for @CubeJerry with OpenAI assistance.
