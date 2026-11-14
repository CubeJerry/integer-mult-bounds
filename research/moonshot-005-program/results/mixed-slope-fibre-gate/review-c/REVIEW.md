# Independent review: actual four-fibre mixed-source obstruction

**Accepted in the author's stated adapter scope. No new κ.** Worker C independently checked the proof and reconstructed its new native premises. The author proof is SHA256 `9015d6cdb3a02c2a5c5922bf5463c82393e8e668e0fe165b800425bbc68210ae`, within freeze `1071e3bac6b2e91a935d8385fa408ae80ca01615de7b812d7df7e6ade2badd79` at `worker-a/mixed-slope-fibre-gate`.

## Mathematical review

The declared class has eight ports. Its actual whole-array matrix R is closed, invertible and involutory. Each retained head-complement basis begins with the same vector e=1, and the corresponding normal is perpendicular to e. Hence the actual stage permutation sends the first fresh axis to e for all eight ports. For z=ε1·2^9+ε2·2^17, every port route in a fixed stage sends z to the same vector. The route on a second port sends that vector back to z. This proves that the conjugated matrices R_s and R'_s preserve the relevant class-frequency fibre, not merely that the individual route matrices have similar spectra.

The array frequency (z,z,0,...,0) makes every retained tensor-uniform translation phase cancel. The head phase is zero, while stage s contributes twice ε_s to its Z4 body phase. Thus Q=I, D_s=(-1)^ε_s I, and both inverse mixed cross coefficients restrict to the same actual R. Appending zero columns proves the statement at every width V>=2. R acts once on the whole array; raising its scalar coefficients to the V-th power would be incorrect.

The permitted adapter property is stronger than preserving a union of fibres: each of the four fibres is preserved individually, with exactly the same induced sixteen-dimensional matrix under the declared identification. This property is satisfied by the author's listed generators, including tensor-uniform translations and head queries, and is closed under products and inverses. An invertible operator preserving a finite-dimensional fibre restricts invertibly to it. The two-source word therefore has a nonzero d2 Walsh coefficient O2 E2 O1 C1 O0 of rank eight. Two full fresh-body targets have only the d1d2 component. The mismatch proves the claimed scoped obstruction on actual input vectors.

The arbitrary number of head queries is harmless within this scope, because their restrictions do not depend on either body sign. The proof does not treat raw spatial M/O adapters as body-even. A raw route explicitly leaves the selected fibre; a translation acting on only one tensor column distinguishes the signs. Additional fields, repeated body occurrences, other paid jobs, class-changing maps or a different source remain outside the theorem. The proof should not be cited as a general two-half-source impossibility statement.

## Independent checks

`check.py` imports no author builder, checker or replay. It uses the pinned earlier Worker C Fourier-polynomial engine, credited and retained as `fourier_review.py`, and writes new checks for this theorem. It replays all112 source X columns through the literal448-field R0 word, recovers the complete scalar contact matrix, and verifies the eight-port closed involution. It reconstructs sixteen actual routes, checks all64 body-fibre diagonal cases and1024 actual conjugated/inverse-cross blocks, including zero-column extensions. Four nontrivial full sixteen-dimensional Walsh controls have exact rank eight. Controls retain the actual raw-route escape, single-column translation escape, and invalid tensor-power distinction.

Run from this directory:

```bash
python check.py --output RESULT.json
python -O check.py --output RESULT-OPTIMIZED.json
cmp RESULT.json RESULT-OPTIMIZED.json
```

Normal and optimized receipts are byte-identical. Finite checks establish the source premises and controls; the invariant-fibre and unique-Walsh-component arguments establish the universal width and arbitrary-adapter conclusions in the stated model. Credit Worker A for this physical bridge, Worker C for the independent review and separately proved formal grading lemma, and Worker B for the source. Prepared for @CubeJerry with OpenAI assistance.
