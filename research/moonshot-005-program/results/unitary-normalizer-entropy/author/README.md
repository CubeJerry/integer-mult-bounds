# Scoped unitary normalizer entropy gate

`PROOF.md` proves the exact finite-width inequality

`V sum(r) + C_port(V) >= 224 b (V+1)`

for b independent actual N=Q^-1 R0 Q service banks, unitary Gaussian/coordinate-monomial/port gates, clean restored zero ancillary fields, and no productive helper credit. If ordinary port entropy is o(V), the paid moment has cap-free asymptotic lower bound `(224 b)^(199/200)`. A rank-nine restriction gives the stronger `224 b * 9^(-1/200)`.

For one bank these bounds are218.0202223577417 and221.55257693456625, above the inherited conditional75.78579625756281 allowance. For two jointly processed independent banks they are434.5318593803482 and443.1051538691325, above151.57159251512562. No restriction to separately computed banks is imposed.

The rank-mass constant224 is sharp in the relaxed unitary model. The explicit ordinary-budget boundary control uses one clean field to implement each one-column C_q with four dyadic port unitaries and no Gaussian calls. Repetition requires linear-in-V ordinary work, showing why the uniform/o(V) condition matters.

This does not exclude arbitrary nonunitary arithmetic, productive-helper constructions, new caller endpoints or the mixed-orientation caller. No new κ.

## Reproduction

From the session root:

```sh
python worker-c/unitary-normalizer-entropy/author/check.py
python -O worker-c/unitary-normalizer-entropy/author/check.py --output worker-c/unitary-normalizer-entropy/author/RESULT-OPTIMIZED.json
```

Explicit `--source`, `--budget`, and `--interface` arguments locate the three pinned inputs after integration. The checker imports no author builder or verifier. It checks source unitarity, all112 distinct normals and448 neighbor pairs,28 four-port unitary blocks, exact rows at widths1/2/3, the clean-ancilla boundary identity, and rational moment comparisons. Universal claims rely on the mathematical proof, not the finite widths.

Root proposed the question and supplied the cap-free concavity strengthening. Worker C authored the proof and checks; source and interface credit remains with their original authors. @CubeJerry/OpenAI assistance.
