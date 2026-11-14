# Independent review: both orientations of retained interstage transport

**Accepted within the stated source and route scope. No new κ.** The positive ordinary orientation and the all-width support obstruction for the opposite orientation are both correct. The review does not rule out a changed encoded caller, a new inverse boundary, or a paid shared normalizer.

Reviewed author proof: `worker-a/interstage-normalizer-screen/PROOF.md`, SHA256 `65ab1163df3eefb6684439ee2f4eec7f24db5fbbfa5a59ab2e22d6e828a080b6`. Author freeze: `38b1c6795c625da4fd06214e8602a8a81f138cee266581978b25889d8759dbb2`.

## Mathematical review

The inherited, separately reviewed physical interface is

\[
A_s=M_s^{-1}(QR_0)M_s=QR_s,\qquad R_s=M_s^{-1}R_0M_s,\qquad R_s^2=I.
\]

Its two products must be distinguished. Direct multiplication gives

\[
A_s^{-1}A_t=R_sR_t,
\qquad A_sA_t^{-1}=QR_sR_tQ^{-1}.
\]

The first is a genuine fixed ordinary bank circuit. No commutation of a port matrix with the port-dependent Gaussian operator is used. Ordinary work still has its ordinary tariff, and the identity alone does not establish a changed caller's final map.

The second has the claimed growing support for the precise retained routes. For each nonzero output/input block, all four possible intermediate ports must be included. Their scalar coefficients are ±1/4, and their full spatial maps are affine orthogonal permutations. These maps include the native translations. Grouping identical complete maps and summing their coefficients before inspecting support is essential: the same calculation at equal stages cancels to the full112-bank identity.

For distinct stages the four maps in each of448 nonzero blocks remain distinct. Gaussian conjugation of one affine map has a four-point support plane. At every output port the source supplies an explicit spatial coordinate at which the four planes are disjoint for each of the four possible input ports. Hence the full output row contains sixteen disjoint terms, rather than an unverified sum of potentially canceling terms.

The extension to every positive width V follows exactly. The maps act coordinatewise on the V columns, so each four-point plane becomes its Cartesian Vth power. The supports remain disjoint already in their first coordinate. The scalar port coefficient ±1/4 occurs once: R acts on whole arrays and is not tensor-powered. Consequently the row has exactly16·4^V entries, each of magnitude2^(−V−2), and squared norm1. No finite-width extrapolation is involved.

A circuit using coordinate monomials, scalar additions and initially zero workspaces has at most2^L original-input coordinates in one output row after L scalar additions. Monomials preserve support counts, an addition at most doubles the maximum, and erasure cannot create new dependencies. Therefore L≥2V+4. This is a fixed ordinary-template obstruction, not a lower bound on arbitrary paid Gaussian moment or on a redesigned caller. Productive helper credits would need their own complete accounting.

The all-stage extension is by exact renaming of the disjoint fresh eight-axis blocks, with all other coordinates as spectators. The checked translations at stages1 and2 obey this renaming, so no stage-independent geometry is being assumed without source evidence.

## Independent finite reconstruction

`check.py` imports neither the author's checker nor its builder. It reads the authenticated R0 word and route records. The literal source's R rows are inherited from the separate complete448-column independent source review; this package checks their new interstage composition.

The checker constructs each spatial route from transvections

\[
P=I+\sum_i(b_i+e_i)(b_i+e_i)^T
\]

using the actual orthonormal complement and fresh axes. This differs from the author's Fourier-coordinate derivation. It composes the four physical affine maps in their actual order, checks orthogonality and every pair-coordinate affine control, and only then converts the result to its Fourier row when needed.

The independent receipt verifies:

- all448 nonzero blocks, each with four surviving ±1/4 affine maps after complete path grouping;
- all448 claimed covariance defects after summing coefficients that reach the same Fourier input frequency;
- all112 complete row-support separators, including every point and signed port coefficient;
- exact equal-stage cancellation to112 identity blocks, with every off-diagonal block zero;
- all actual orthonormal bases and the fresh-axis translation renaming.

The covariance test alone would not imply the ordinary-template obstruction. The separately checked disjoint support certificates supply that implication.

The checker also forms one complete width-two row with exact Gaussian rational coefficients. Its256 entries all have squared magnitude1/256 and total norm1. Removing one actual intermediate path gives norm15/16. Incorrectly raising the whole-bank scalar coefficient to the second power gives norm1/16. These controls expose both missing paths and the tensor convention error. Normal and optimized Python receipts are byte-identical; correctness checks use explicit exceptions rather than removable assertions.

## Reproduction and scope

From the session root:

```sh
python worker-c/interstage-review/check.py --author worker-a/interstage-normalizer-screen --output worker-c/interstage-review/RESULT.json
python -O worker-c/interstage-review/check.py --author worker-a/interstage-normalizer-screen --output worker-c/interstage-review/RESULT-OPTIMIZED.json
```

The receipt includes exact author proof, source-word, route and result pins. The authenticated R0 word is `d27892c4934f9b6fa08fd10b53a665f455020e6711db9378ab01f439ede2c56c`; the route file is `ff3464b51b7240c97294c9a843dace84f17e717db1c7299a85646cd9c70f6c3a`.

The conclusion is restricted to the retained forward routes. A literal inverse source with a separately justified reversed boundary, different adapters, encoded-role changes, or a complete paid implementation can change the available chronological interfaces. This review therefore preserves the positive orientation as a constructive resource. It does not promote the native source into a complete multiplication theorem, discharge precision or compiler foundations, or establish a new κ.

Credit: Worker A authored the interstage proof and certificates; Worker B supplied the112-port source; the preceding physical interface and source reviews retain their original attribution. Worker C independently reconstructed the affine composition and reviewed the universal support argument for @CubeJerry with OpenAI assistance.
