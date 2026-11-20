# Binary and nonlinear geometric-source port gates

This S031 package strengthens the separately reviewed field-linear gap15
obstruction. It preserves that earlier theorem and its independent review.

* [Binary proof](BINARY-PROOF.md): receivers5 and76 see the same D108 exit and
  have derivative triples(30,18,12) and(38,18,52). Their difference factors as
  D(56) M D(18)^(-1), excluding arbitrary invertible binary amplitudes at all
  widths without commuting scalars through M.
* [Proposed nonlinear extension](NONLINEAR-PROOF.md): a precise finite
  coset-partition lemma makes an arbitrary bank bijection affine-additive
  on each relevant geometric core coset. This supplies the same contradiction
  without assuming global additivity. Separate independent review is required.

Run from the repository root:

```sh
OPENBLAS_NUM_THREADS=1 python -I -B research/moonshot-005-program/results/bit-shared-h-s031-review/binary-gap15-port-gate/check.py --repo . --out FRESH
```

Expected:

```text
PASS_BINARY_GAP15_DERIVATIVE_COLLISION 108 5 76 56 18 40320 1344
```

The source/core theorem and native atlas remain pinned dependencies. The
checker uses the pinned independent geometric review's arithmetic, rebuilds
the actual receiver data and supplies separate binary matrix controls and
finite nonlinear-core controls. Tests do not replace the universal proofs.

No new kappa, complete physical word, return-excess tariff or foundational
discharge is claimed. Credit @CubeJerry, the retained predecessors and the
S031 root/worker contributions, with substantial OpenAI assistance.
