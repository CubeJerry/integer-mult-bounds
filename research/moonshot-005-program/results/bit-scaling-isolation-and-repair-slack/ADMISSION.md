# Scaling isolation and sharp shared-repair slack

**Admitted algebraic consequences; no new kappa.** For a fixed proper code B,
canonical quotient repair rank is the codimension of its fixed space inside
the canonical nullspace. At bank size 5,760 and target r<=202, that fixed space
must have dimension at least 587,318.

Within the actual seventy-coordinate family, scaling the unselected input
coordinates preserves all foreign invertibility and corrected rows. Among
distinct nonzero scalars, at most one can have repair rank<=202. If one does,
every other has rank at least 580,178. The proof uses distinct eigenspaces,
without assuming that B is diagonalizable. It does not exclude the exceptional
structured point.

For one port U shared by s receivers and one repair space of dimension r,
the valid linear intersection loss is at most (s-1)r. This is sharp. The old
scalar information deficit 48,876 cannot be carried over by adding r once,
because its exact saturation premise changes.

- [All-field proofs and open next questions](author/REPAIR-GATES.md)
- [Author exact checks](author/output/RESULT.json)
- [Source pins](author/output/SOURCE-PINS.json)
- [Independent mathematical review](review/REVIEW.md)
- [Separate GF(4) and binary controls](review/output/RESULT.json)

Reproduce from repository root:

```sh
python3 research/moonshot-005-program/results/bit-scaling-isolation-and-repair-slack/author/check_repair_gates.py --repo . --out /tmp/s026-repair-gates-author
python3 research/moonshot-005-program/results/bit-scaling-isolation-and-repair-slack/review/check.py --out /tmp/s026-repair-gates-review
```

Author checks additionally require NumPy; their command line is documented
in the source. The exploratory pooled-cut screen is not a universal theorem.
Credit @CubeJerry, the retained native/atlas/source authors and S026 Worker C;
substantial OpenAI assistance. No new supplier, foundation discharge or
complete exponent is established.
