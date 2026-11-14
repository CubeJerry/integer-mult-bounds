# Four-type chain parity gate

PROOF.md shows that a width2 four-direction chain with at most four
exceptional conic types among saving rows has exact proper-cover charge
at least195. Its new dependency is the scalar equality14 classification.
Together with the earlier chain map, six pair scalar codes force an
impossible odd sum of double-saving row weights at the target194.

Reproduce the finite controls with Python3 standard library:

```sh
python check.py --output reproduced.json
python -O check.py --output reproduced-optimized.json
```

Expected status PASS_FOUR_TYPE_CHAIN_PARITY_CONTROLS:3120 identity-admitting
F4 selector matrices,15600 four-type-set checks, and no even solution to
the equality weight constraints. The sole solution without evenness is
(7,7,7,7). The omitted fifth-type and an abstract five-type even-weight
example preserve the precise scope: the proof does not exclude all F4
chains. The finite checker is a control, not a substitute for the
all-field proof.

The field/rank utility code is credited reuse of the earlier chain
author checker, not an independent implementation. Independent review
must inspect the proof and reconstruct decisive claims separately.
No physical decoder, supplier or new kappa is supplied.
