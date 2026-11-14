# Independent reflection and contact review

**Reviewer:** programme integrator, independently of the construction author.  
**Scope:** the exact finite source geometry and the universal phase-selection theorem. **No new kappa.**

## Different reconstruction

The author starts with the pinned eight-dimensional matrix and enumerates all real-orthogonal four-cliques. This review reconstructs the order-three isometry directly from the four stated A2 reflection pairs in the nine-coordinate, sum-zero E8 root realization. Reverse application order within each pair reproduces every signed root image and the entire pinned matrix. The orthogonal frame, integer coordinates, binary contact convention (all 7140 distinct real-root pairs), and forty-line matrices then follow separately.

The independently written checker consumes the ninety supplied pencil witnesses. It verifies their real orthogonality, complex nonorthogonality, distinct cycle labels, and disjoint complete coverage of all 540 complex-nonorthogonal edges. It does not reuse the author's clique enumerator. It also checks every relative phase contact and the strongly regular adjacency identity.

## Algebraic rank verification

Put F=(I+theta S/3)/2, where theta^2=-3. Because S^2=-3I and S is skew, F is an idempotent of trace four over Q(theta). Thus H=P F P^T/2 has rank at most four. A separate elimination modulo 103, with theta sent to 10, gives rank four for 3A+10C. This proves the lower bound in characteristic zero: a nonzero specialized minor cannot arise from an identically zero minor over Q(theta). Separate matrices A and C have rank eight by their eight-coordinate factorizations and independent rank-eight witnesses modulo 103.

This argument does not require the author's forty-by-forty identity H^2=10H, although that identity was also reproduced by executing the author checker and its output matched exactly.

For every representative section, powers of E act by complex units on the corresponding four-dimensional eigenspace; real sign normalizations only multiply by additional units. Consequently the change of section is an invertible diagonal congruence with conjugation, preserving rank.

## Universal contact theorem

In each pencil select the four witnessed pairwise-real-orthogonal roots as phase zero. Any selection gives four phase values in a three-element set, so two agree. The common E-power preserves their real orthogonality and their Hermitian product remains nonzero. Disjoint pencil edges make the ninety resulting contacts distinct. This reasoning applies to all 3^40 root-line sections; the theorem does not purport to exhaust arbitrary continuous rotations or changed physical sources.

Ninety contacts are not ninety MOVEs. Neither a correction rank nor an invoice follows from this counting argument. The simple complementary fitting has rank sixteen; no general minimum-rank claim is accepted.

## Checks and controls

The actually executed pure-JavaScript review returned PASS_INDEPENDENT_REFLECTION_AND_PENCIL_REVIEW. It rejected a duplicated pencil edge, and doubling the imaginary coefficient changed the specialized rank from four to eight. The fixed source was checked against its admitted SHA-256 before execution.

Reproduce with:

```sh
node review/check.js path/to/SYMMETRY.json author/RESULT.json
```

The wrapper checks both input hashes. The same mathematical function was executed in the cloud V8 tool after loss of the local executor. There is no claim that a fresh local Node process ran after that loss. Source dependence on the earlier admitted geometry remains explicit.

**Disposition:** accept the stated rank-four theorem, ninety-contact obstruction, and explicit complementary rank-sixteen calculation. A physical Hermitian source, paid correction mechanism, precision bridge, and complete caller remain open.
