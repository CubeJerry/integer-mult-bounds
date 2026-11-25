# Independent review of changing-field binary packing

Reviewed file: `../route-a/FULL-RATE-BINARY-FIELD-PACKING.md`, as read on
2026-11-25 at 22:36 UTC. Reviewer: E003 Route C, a genuine separate worker.
Status: **accepted within the stated permutation-call interface**.
This is a written mathematical review, not a full physical implementation.

## Checked implications

1. FP1 is an exact F2-linear bijection. The domain has dW rows of b-bit
   records, and the codomain has W rows with b E-valued components, each
   encoded in d bits. The volume is dWb|Omega| in both directions. Since
   the completed template is Pi on every E-valued row, tensoring its
   linear identity with the b-dimensional spectator identity and expanding
   the E basis gives Pi on every original bit. The target coefficient is
   in F2; no parent-field embedding is needed.
2. A paid child row has db|Omega| bits, while the parent batch has
   Wdb|Omega| bits. Thus sigma paid rows retain ratio sigma/W. Counting d
   again as an extra multiplicative volume factor would be incorrect.
3. The scan implementation uses a constant number of marked buffers.
   Forward extraction/merge processes one basis index at a time; inverse
   extraction emits basis rows in their original order. Every pass is
   bounded by the existing data volume. Binary-counter resets can be
   charged to full row/basis runs: a reset of O(log d) per group contributes
   V poly(log d) over all basis passes, and intermediate c-bit records
   pay for their own c-counter resets. This supports the stated
   O(dV)+V poly(log d) payload/control form; the global proof only needs
   its weaker polynomial-d times V consequence.
4. The complete binary batch width must be dW_E, not W_E. Enlarging the
   leading occupied batch accordingly increases its logarithmic width by
   log d. The source next-multiple padding is still strictly below two
   because the occupied leading range is at least dW_E. The factor two is
   already a charged row-padding factor; it is not silently multiplied
   anew by d at each descendant.
5. Labels each have the same number of basis coordinates. Hence grouping
   within one label retains its volume fraction, including the existing
   2/N padded bound. Finite repair fractions are unchanged when they use
   the same E and exact inherited grouping. None of these claims uses
   random access or d physical tapes.
6. At a spatial descendant the parent's entire b-bit payload is arbitrary
   and unchanged as data. The child's coefficient arithmetic occurs on
   newly grouped independent rows; its completed target returns all b
   bits by the same permutation. This proves the no-product-of-extension-
   degrees invariant by induction. Temporary metadata must still be
   stripped before the child as required by the separate local executor.

## Scope conditions that must remain in the assembled theorem

The proof applies to **completed permutation calls**. It cannot be used to
change the coefficient field midway through a nontrivial F/F^-1 spectral
transform or a numerical Walsh arithmetic operation. Those targets mix
payload coefficients and are not Pi tensor identity on arbitrary bits.
The order-three and order-five finite repair children therefore continue
to use their parent's common field and finite template. The changing-field
descent occurs only when invoking the binary spatial interchange primitive.

The field's actual arithmetic, construction, binary basis, record boundaries
and local polynomial-in-m work remain charged. The lemma supplies neither
the guarded minimum node volume nor the full O(n) visited-space bound.
Global parking, additive descriptions and full-volume reserve descents need
their separate arguments. The source's fixed-field target and geometric
space proof cannot simply be invoked without those new guards.

No blocker was found in FP1--FP3 under those scopes. In particular, the
record width may contain a product of prior basis dimensions without
creating that product in the **total** volume: the number of independent
rows decreases by the same factors. This is the precise distinction needed
by the variable-template recurrence.

Finite check: `verify_nested_packing.py` validates the nested coordinate
bijections and commutation with arbitrary spatial permutations, with distinct
symbolic bit identities and varied parent/child degrees. These are layout
checks; the field-linear identity and fixed-tape bounds are proved in the
reviewed document, not established by finite sampling.

Credits: the source full-rate scalar descent; Route A's explicit changing-field
packing proof; Jerry Chen (@CubeJerry); independent AI-assisted Route C review.
