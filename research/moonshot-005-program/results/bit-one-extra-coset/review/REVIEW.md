# Independent review: one-extra-coset availability theorem

Status: **the source theorem and scalar gluing argument are sound in the stated scope**: the actual pinned BIT code (C+\operatorname{span}(h)), scalar coefficients over every characteristic-two field, and its vertex-gauge equivalent. The proof does not classify arbitrary rank-ten spaces or operator-valued extra rows. I independently reconstructed the source matrices and all requested zero-set ranks. I found one proof detail that should be written explicitly before freezing the extension-field sharpness sentence: transfer the binary distance-48 fact to every characteristic-two extension.

## Independent exact source reconstruction

I read the authenticated native directly, reconstructed the 111 integer norm-four roots from rational source-line charts, and formed the symmetric canonical fitting (K_{ij}=1) iff (i=j) or the real roots are orthogonal. I used a separate low-bit-pivot F2 elimination and a separately selected basis of nine original rows; I did not use B's source certificate or verifier.

Results:

- (operatorname{rank}_{\mathbb F_2}K=9), with 111 distinct nonzero binary coefficient normals.
- Every one of the 111 zero-restriction feature-column sets has rank 8.
- Every one of the 6,105 pairwise zero-set intersections has rank exactly 7.
- The maximum closed-neighborhood intersection (|T_i\cap T_j|) is 36, with the same histogram as the pinned receipt.
- The nine-dimensional binary row code has 512 words and minimum nonzero weight 48.
- The sharp witness (h=e_1+e_{10}) has exactly 36 available rows over (\mathbb F_2).

These data imply the corresponding ranks over every field extension: all tested matrices have entries in (\mathbb F_2), so their rank is determined by zero/nonzero minors, unchanged by field extension. In particular, the single-zero annihilator is exactly \(\langle a_i\rangle\), and the pair-zero annihilator is exactly \(\langle a_i,a_j\rangle\) over every such field.

## Extension-field distance and sharpness detail

The proof's sharp-witness sentence currently cites the binary minimum distance but quantifies over every characteristic-two field. The missing bridge is short and exact. Let (G) be the (9\times111) binary generator matrix from the independently selected basis. If an extension-field codeword had support of size at most 47, it would vanish on at least 64 coordinates (Z). Its nonzero coefficient vector would lie in the left kernel of (G_Z), so (operatorname{rank}_F G_Z<9). Since every minor of (G_Z) is binary, (operatorname{rank}_{\mathbb F_2}G_Z<9) as well. There is then a nonzero binary coefficient vector producing a binary codeword vanishing on (Z), of weight at most 47, contradicting the exact binary distance 48. Thus the extended code also has distance at least 48.

For any extension scalar (c) and coordinate (\ell), (h+c e_\ell) is nonzero and has support at most 3; hence it cannot lie in the extension code. This rules out (h+C=c e_\ell+C) for every (c\ne0), and (h\notin C) is the (c=0) case. So (h+C) is nonzero and noncoordinate over every characteristic-two extension. The 36 binary availability witnesses remain available after extension; the theorem's upper bound gives exactly 36 there too. This addition fixes the only logical omission I found in the finite-distance-to-extension transition.

Availability itself is extension-stable for binary (h): (h|_{Z_i}) lies in the extension rowspace of (G_{Z_i}) iff the binary augmented matrix has unchanged rank, iff it lies in the base-field rowspace. This also independently supports the sharp count.

## Gluing proof and dependent normals

For each available role (i), the restriction (h|_{Z_i}) has a code representative (q_i\cdot p). The pair-intersection rank-7 certificate makes the annihilator of its feature points exactly (operatorname{span}(a_i,a_j)), so all pair differences (q_i-q_j) lie in those two-normal spans.

The global glue is valid once the available normals have rank at least 3. Choose an independent triple (a_1,a_2,a_3). The three pair relations force the coefficient of (a_1) in (q_1-q_2) and (q_1-q_3) to agree; subtract that multiple from (q_1) to obtain (q) with (q_i=q+\lambda_i a_i) on the triple. For any additional normal (a), the pair relations put (q_a-q) in each (operatorname{span}(a,a_k)). Modulo \(operatorname{span}(a)\), at least two of the three (a_k)'s remain independent: if (a) lies in their 3-space the quotient has dimension 2; otherwise their three images remain independent. Thus the intersection of the three spans is just \(operatorname{span}(a)\), and (q_a=q+\lambda_a a). This covers selected normals and dependent sums without a general-position assumption.

An availability set of at least 37 distinct nonzero binary normals necessarily spans rank at least 3 even over an extension. A two-dimensional extension span contains at most three binary projective normals: choose a nonsingular binary 2-by-2 minor of two independent binary vectors and solve for the coefficients of any other binary vector; both coefficients must be binary. This proves the cardinality threshold used by the theorem.

Rank 2 must remain excluded. An explicit negative control has (a_1=01,a_2=10,a_3=11) and (q_1=00,q_2=00,q_3=01). Every pair difference lies in the corresponding two-normal span, yet no single q satisfies (q_i-q\in\langle a_i\rangle) for all three. The verifier reproduces this. The theorem correctly uses rank at least 3 for gluing; the 37-availability argument ensures it.

## Availability and fitting consequences

After gluing, (g=h-q\cdot p) represents the same coset and is supported on the intersection of all available closed neighborhoods. If (g) has two support coordinates (j,k), symmetry places every available index in (T_j\cap T_k), whose size is at most 36. Therefore a nonzero coset with at least 37 available rows must be a coordinate coset. This proves the one-extra-coset classification; it does not classify sums of two extra dimensions or arbitrary rank-ten fittings.

For a fitting with rows (A_i=c_i+t_i h), (t_i=0) gives (A_i=K_i) by the rank-8 local injectivity. A noncoordinate h has at most36 active rows, leaving at least75 canonical rows and 150 required arrivals. If the active set has at least37 rows, the coset is (c e_j+C); after absorbing a codeword, the fitting form is (A_i=(1-t_i g_i)K_i+t_i g). All 110 rows other than j retain at least 54 foreign entries and require two arrivals each. The row-support/arrival consequences are conditional on the admitted singular-cell generalized-scattering normal form and E7 52-line bound.

The q8 and q9 path interfaces supply only119 and120 original X/packet facet visits. The universal one-extra-code lower bound is 150, so at least31 or30 added upward arrivals are needed. Each distinct new proper contribution costs a positive-rank MOVE. The admitted movement ceilings (<4 q8 at any finite multiplicity, <12 q9) cannot pay these arrivals. This excludes only (C+\operatorname{span}(h)) and vertex-gauge equivalents in the stated scalar route interface. It says nothing about arbitrary rank-ten rowspaces or noncommuting block extensions.

## Frozen pins

Independent checker: `audit_one_extra_coset.py`; independent receipt: `RESULT.json`.

- Root proof: `worker-b/one-extra-coset/PROOF.md`, SHA256 `a6b0a34517fd550c1565be4af47c975c464c5373bf52f0aea5a487a68fdc04fd`.
- Root receipt: `worker-b/one-extra-coset/RESULT.json`, SHA256 `17f3ef72890ae5fb6e75825a83c06a4cad0d89b1e68fc9012ba704c62c0d31bb`.
- Root source certificate: SHA256 `51ae7b7442c63f3a038c78203adb47a08d2f6c09fb9768a30e472516f64a3c99`; not used in the independent reconstruction.
- Native source: SHA256 `51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78`.
- Singular-cell generalized-scattering dependency: `worker-b/scattering-feedback/next/PROOF.md` (pinned separately in the receipt package).

Run `python audit_one_extra_coset.py --repo programme --root-package worker-b/one-extra-coset --output worker-c/one-extra-coset-review`. The proof adds the extension-field distance transfer above; no author replay code is imported.
